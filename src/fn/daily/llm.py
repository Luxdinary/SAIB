"""Model providers for the daily runner.

Default (Stefan, 03.11.2026, 16:50: "Wir machen es über den normalen Ultra-Plan"): `claude -p` headless with the stored
claude.ai login of Claude Code, `--model claude-sonnet-5-5`, no tools, no session, JSON result with token usage.
Every call is a short standalone job (prompt via stdin, system prompt one line). Costs: tokens only, no USD
("Abo, kein Einzelpreis"). The Anthropic SDK provider stays available for a later API key; Gemini writes no scripts
(voices only). The mock answers with queued plans (the approved example under a new id) when no model is wanted.
Keys and tokens are never printed.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass

from ..config import ROOT, env, has_secret
from ..costs import CostEntry, CostLogger

SHORT_SYSTEM = ("Du bist Regie- und Skriptschreiber eines Kurzvideo-Netzwerks. Befolge die Regeln im Auftrag wörtlich und antworte "
                "ausschließlich mit einem JSON-Objekt: kompakt (keine Einrückung, keine Leerzeilen), ohne Text davor oder danach, "
                "ohne Markdown-Zaun.")


class RateLimited(RuntimeError):
    """The subscription limit of `claude -p` is reached (or the CLI says so): stop the whole run instead of hammering it."""


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_tokens: int = 0          # cache creation + cache read (claude -p)
    usd: float = 0.0
    note: str = ""


class Provider:
    name = "base"
    model = ""

    def complete(self, system: str, user: str, *, max_tokens: int, temperature: float) -> LLMResult:  # pragma: no cover
        raise NotImplementedError


class ClaudeCLIProvider(Provider):
    """`claude -p` with the stored login (subscription). Prompt via stdin (Windows command lines are limited)."""
    name = "claude_cli"

    def __init__(self, model: str, timeout: float = 1800.0, effort: str | None = None, extra_args: list[str] | None = None):
        self.model = model
        self.timeout = timeout
        self.effort = effort
        self.extra_args = list(extra_args or [])
        self.exe = shutil.which("claude") or shutil.which("claude.cmd") or shutil.which("claude.exe")
        if not self.exe:
            raise RuntimeError("claude CLI not found on PATH")

    def _env(self) -> dict:
        # like brands/claude_workflows/echtlauf/record_run.py: without the desktop app's variables the CLI behaves as in a plain terminal
        e = {k: v for k, v in os.environ.items() if not (k.startswith("CLAUDE") or k.startswith("ANTHROPIC"))}
        e["PYTHONIOENCODING"] = "utf-8"
        return e

    def complete(self, system: str, user: str, *, max_tokens: int, temperature: float) -> LLMResult:
        # stream-json: a long answer may span several assistant turns; `result` would hold only the last one
        cmd = [self.exe, "-p", "--model", self.model, "--output-format", "stream-json", "--verbose", "--tools", "", "--no-session-persistence",
               "--disable-slash-commands", "--strict-mcp-config", "--setting-sources", "", "--system-prompt", SHORT_SYSTEM]
        if self.effort:
            cmd += ["--effort", self.effort]
        cmd += self.extra_args
        r = subprocess.run(cmd, input=system.strip() + "\n\n" + user.strip(), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=self._env(), timeout=self.timeout, cwd=ROOT)
        texts: list[str] = []
        result: dict | None = None
        rate = ""
        for line in (r.stdout or "").splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            typ = ev.get("type")
            if typ == "assistant":
                for b in (ev.get("message") or {}).get("content") or []:
                    if b.get("type") == "text" and b.get("text"):
                        texts.append(b["text"])
            elif typ == "result":
                result = ev
            elif typ == "rate_limit_event":
                info = ev.get("rate_limit_info") or {}
                rate = f"rate_limit {info.get('status', '')}"
                if str(info.get("status", "")).lower() in ("rejected", "blocked", "exceeded", "limit_reached"):
                    raise RateLimited(f"claude -p: {rate} (resetsAt {info.get('resetsAt')})")
        if result is None:
            raise RuntimeError(f"claude -p exit {r.returncode}, kein result-Ereignis: {(r.stdout or '')[-200:]!r} {(r.stderr or '')[:200]!r}")
        if result.get("is_error") or result.get("subtype") != "success":
            msg = f"claude -p {result.get('subtype')}: {str(result.get('result'))[:300]}"
            if result.get("api_error_status") == 429 or re.search(r"(usage|rate)[ _-]?limit|hit your limit|limit reached", msg, re.I):
                raise RateLimited(msg)
            raise RuntimeError(msg)
        text = "".join(texts) or str(result.get("result", ""))
        u = result.get("usage") or {}
        cache = int(u.get("cache_creation_input_tokens", 0) or 0) + int(u.get("cache_read_input_tokens", 0) or 0)
        models = ",".join(sorted((result.get("modelUsage") or {}).keys()))
        return LLMResult(text=text, provider=self.name, model=self.model,
                         input_tokens=int(u.get("input_tokens", 0) or 0), output_tokens=int(u.get("output_tokens", 0) or 0),
                         cache_tokens=cache, usd=0.0,
                         note=(f"Abo, kein Einzelpreis (CLI-Schätzung {result.get('total_cost_usd')} USD); Modelle {models}; "
                               f"{result.get('num_turns')} Turn(s); {result.get('duration_ms')} ms; {rate}"))


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, model: str):
        import anthropic  # imported lazily: the CLI path needs no SDK
        self.model = model
        key = env("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY not set in .env")
        self._client = anthropic.Anthropic(api_key=key, max_retries=2, timeout=900.0)

    def complete(self, system: str, user: str, *, max_tokens: int, temperature: float) -> LLMResult:
        resp = self._client.messages.create(model=self.model, max_tokens=max_tokens, temperature=temperature,
                                            system=system, messages=[{"role": "user", "content": user}])
        text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "") == "text")
        usage = getattr(resp, "usage", None)
        return LLMResult(text=text, provider=self.name, model=self.model,
                         input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
                         output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
                         note=f"stop={getattr(resp, 'stop_reason', '')}")


class MockProvider(Provider):
    """No model: answers with whatever the pipeline queued (the approved example plan with new ids)."""
    name = "mock"
    model = "mock"

    def __init__(self):
        self.queue: list[str] = []

    def complete(self, system: str, user: str, *, max_tokens: int, temperature: float) -> LLMResult:
        if not self.queue:
            raise RuntimeError("mock provider has no queued answer")
        return LLMResult(text=self.queue.pop(0), provider=self.name, model=self.model,
                         input_tokens=len(system) // 4 + len(user) // 4, output_tokens=0, note="Attrappe, keine API")


def make_provider(cfg: dict, requested: str | None = None) -> Provider:
    want = (requested or cfg.get("provider") or "claude_cli").lower()
    if want == "auto":
        want = "claude_cli"
    if want in ("claude_cli", "claude", "cli"):
        return ClaudeCLIProvider(cfg.get("claude_model", "claude-sonnet-5-5"), timeout=float(cfg.get("cli_timeout_s", 1800)),
                                 effort=cfg.get("cli_effort") or None, extra_args=list(cfg.get("cli_extra_args") or []))
    if want == "anthropic":
        if not has_secret("ANTHROPIC_API_KEY"):
            raise RuntimeError("provider anthropic needs ANTHROPIC_API_KEY in .env (Stefan, 03.11.2026: none; use claude_cli)")
        return AnthropicProvider(cfg.get("anthropic_model", "claude-sonnet-5-5"))
    if want == "mock":
        return MockProvider()
    raise ValueError(f"unknown llm provider {want!r} (claude_cli | anthropic | mock; Gemini writes no scripts)")


def price_usd(cfg: dict, model: str, input_tokens: int, output_tokens: int) -> tuple[float, str]:
    table = (cfg.get("price_usd_per_million") or {}).get(model)
    if not table:
        return 0.0, "Preis nicht ermittelbar"
    usd = input_tokens / 1e6 * float(table.get("input", 0)) + output_tokens / 1e6 * float(table.get("output", 0))
    return round(usd, 5), f"{table.get('input')}/{table.get('output')} USD je Mio. Token (Listenpreis laut Konfiguration)"


def log_llm_cost(costs: CostLogger, video_id: str, purpose: str, res: LLMResult, cfg: dict) -> float:
    if res.provider == "claude_cli":
        usd, note = 0.0, "Abo, kein Einzelpreis"
    elif res.provider == "mock":
        usd, note = 0.0, "Attrappe"
    else:
        usd, note = price_usd(cfg, res.model, res.input_tokens, res.output_tokens)
    costs.log(CostEntry(video_id, "llm", res.input_tokens + res.output_tokens + res.cache_tokens, "tokens", usd, res.provider,
                        f"{purpose}; model={res.model} in={res.input_tokens} out={res.output_tokens} cache={res.cache_tokens}; {note}; {res.note}"))
    return usd


def extract_json(text: str) -> dict:
    """The first JSON object in a model answer (with or without a ```json fence)."""
    t = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", t, re.S)
    if m:
        t = m.group(1)
    start = t.find("{")
    if start < 0:
        raise ValueError("no JSON object in the model answer")
    if '"video_id"' in t:                       # a plan: start at the object that carries it (skips leading fragments)
        k = t.find('"video_id"')
        cand = t.rfind("{", 0, k)
        if cand >= 0 and t[cand:k].count("}") == 0:
            start = cand
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(t)):
        ch = t[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(t[start:i + 1])
    return json.loads(t[start:])
