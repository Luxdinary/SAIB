"""Orchestration of one brand's daily production: topics -> plans (model) -> checks -> voice/render -> export -> records.

Nothing here renders directly: renders go through scripts/render_queue.py and the brand's render script, checks and
export through the existing scripts. With the mock provider (the approved example plan under a new id) a run stops after
the dry run. Order per topic: German plan (model, own validator) -> dry run (renderer findings go back to the model) ->
English plan from the same scenes (own validator + structure comparison) -> dry run -> voice -> render -> overlap check ->
export -> Redaktionsplan row -> marker.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from ..config import DATA_DIR, ROOT, STORAGE_DIR, voices_config
from ..costs import CostLogger
from .context import BrandContext, SourceRef, build_context, calendar_entry, check_sources, recording_for_title, research_entry, source_refs
from .llm import MockProvider, Provider, RateLimited, extract_json, log_llm_cost, make_provider
from .media import prepare_assets
from .prompts import (dry_run_repair_user, repair_prompt, repair_system, system_prompt_de, system_prompt_en, user_prompt_de,
                      user_prompt_en)
from .records import (RunLock, State, append_csv_row, csv_done_stems, csv_done_titles, csv_row, flash_used_since_quota_reset, mark_konzeptplan,
                      next_slot, next_version)
from .settings import BUSINESS_DIR, RUNS_DIR, BrandSettings, brand_settings, load_aufbauten
from .topics import Konzeptplan, Topic, _norm, limited_allowed, load_konzeptplan, ordered_candidates
from .validate import compare_structure, validate_plan

VIENNA = ZoneInfo("Europe/Vienna")
PY = sys.executable


def today_vienna() -> str:
    return datetime.now(VIENNA).strftime("%Y-%m-%d")


@dataclass
class Options:
    date: str
    topics: int = 2
    languages: tuple[str, ...] = ("de", "en")
    dry_run: bool = False
    provider: str | None = None
    no_export: bool = False
    pro_fallback: bool | None = None
    max_flash: int | None = None
    source_check: bool | None = None
    topic_nr: str | None = None
    no_mark: bool = False
    keep_going: bool = True
    prototype: bool = False         # label outputs as "Tagesläufer-Prototyp" (Redaktionsplan, Veröffentlichung.md, plan notes)
    effort: str | None = None       # claude -p --effort override (low | medium | high | xhigh | max)
    use_plan: bool = True           # topics of the day from the month plan (data/calendars/<id>_<month>.plan.json) when it has them


@dataclass
class LangResult:
    video_id: str
    version: str
    plan_path: str = ""
    plan_ok: bool = False
    validation_errors: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    llm_calls: int = 0
    llm_tokens_in: int = 0
    llm_tokens_out: int = 0
    llm_tokens_cache: int = 0
    llm_usd: float = 0.0
    dry_run_exit: int | None = None
    dry_run_note: str = ""
    dry_run_diag: str = ""
    dry_run_review: list[str] = field(default_factory=list)
    dry_run_repairs: int = 0
    dry_run_done: bool = False
    voice: str = ""                 # flash | pro | reused | none
    render_exit: int | None = None
    status: str = ""                # VALIDATED | HUMAN_REVIEW | FAILED | ...
    duration_s: float | None = None
    sfx_stem_peak: float | None = None
    overlaps: int | None = None
    small_text: int | None = None
    export_folder: str = ""
    csv_written: bool = False
    cost_usd_variable: float | None = None
    notes: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class TopicResult:
    key: str
    nr: str | None
    title: str
    aufbau: str | None
    aufbau_note: str
    langs: dict[str, LangResult] = field(default_factory=dict)
    marked: bool = False
    notes: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class BrandResult:
    brand_id: str
    brand_name: str
    date: str
    provider: str
    model: str
    dry_run: bool
    topics: list[TopicResult] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""


class DailyRunner:
    def __init__(self, brand_id: str, opts: Options, log=print):
        self.brand_id = brand_id
        self.opts = opts
        self.log = log
        self.s: BrandSettings = brand_settings(brand_id)
        self.state = State()
        self.costs = CostLogger()
        self.kp: Konzeptplan = load_konzeptplan(brand_id, self.s.business_path("konzeptplan"), self.s.topic_source)
        self.ctx: BrandContext | None = None
        llm_cfg = dict(self.s.llm)
        if opts.effort:
            llm_cfg["cli_effort"] = opts.effort
        self.provider: Provider = make_provider(llm_cfg, opts.provider)
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        self.rate_limited = False
        self._recording: str | None = None                    # recording of the topic in work (Promptwerk), for the EN checks
        self.run_log = RUNS_DIR / f"{opts.date}_{brand_id}.log"
        if isinstance(self.provider, MockProvider) and not opts.dry_run:
            self.log(f"[{brand_id}] Attrappe statt Modell: deshalb nur Trockenlauf")
            self.opts.dry_run = True

    @property
    def is_mock(self) -> bool:
        return isinstance(self.provider, MockProvider)

    # ------------------------------------------------------------------ helpers
    def _note(self, msg: str) -> None:
        RunLock.heartbeat()
        self.log(f"[{self.brand_id}] {msg}")
        with self.run_log.open("a", encoding="utf-8") as fh:
            fh.write(f"{datetime.now().isoformat(timespec='seconds')} {msg}\n")

    def _run(self, cmd: list[str], timeout: float, extra_env: dict | None = None) -> subprocess.CompletedProcess:
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", **(extra_env or {})}
        with self.run_log.open("a", encoding="utf-8") as fh:
            fh.write(f"\n$ {' '.join(cmd)}\n")
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=timeout, env=env)
        except subprocess.TimeoutExpired as exc:
            r = subprocess.CompletedProcess(cmd, 124, stdout=(exc.stdout or "") if isinstance(exc.stdout, str) else "",
                                            stderr=f"timeout after {timeout} s")
        with self.run_log.open("a", encoding="utf-8") as fh:
            fh.write((r.stdout or "") + ("\n[stderr]\n" + r.stderr if r.stderr else "") + f"\n[exit {r.returncode}]\n")
        return r

    def context(self) -> BrandContext:
        if self.ctx is None:
            self.ctx = build_context(self.s, self.kp)
        return self.ctx

    # ------------------------------------------------------------------ topics
    def _aufbau_options(self, runtime: list[dict], built: list[dict], nr: str | None) -> list[dict]:
        """Built Aufbauten that can carry topic `nr`: an Aufbau without a `themen` key is general; with a `themen` key
        (even an empty one) it carries only the listed numbers (Revlore models, Scutoria mail/chat topics)."""
        if not runtime:                                          # no aufbauten.yaml: letters from config/daily.yaml
            return [{"kuerzel": str(a), "spec": None, "quellen": [], "hinweis": ""} for a in (self.s.aufbau.get("available") or [])]
        out: list[dict] = []
        for a in built:
            if not a.get("themen_declared"):
                out.append({"kuerzel": a["kuerzel"], "spec": a, "quellen": [], "hinweis": ""})
                continue
            for th in a.get("themen") or []:
                th_nr = str(th.get("nr") if isinstance(th, dict) else th)
                if nr is not None and th_nr == str(nr):
                    out.append({"kuerzel": a["kuerzel"], "spec": a, "quellen": (th.get("quellen") if isinstance(th, dict) else None) or [],
                                "hinweis": (th.get("hinweis") if isinstance(th, dict) else "") or ""})
        return out

    def _apply_plan(self, cands: list[Topic]) -> list[Topic]:
        """The topics of the month plan for this day come first, in slot order, with their planned Bildaufbau; the rest keeps the old
        order, so a planned topic that fails a check is replaced by the next free one. Planning is optional: any problem means no change."""
        if not self.opts.use_plan or self.opts.topic_nr:
            return cands
        try:
            from .monthplan import plan_for_day
            from .topics import _norm
            rows = plan_for_day(self.brand_id, self.opts.date)
            if not rows:
                return cands
            by_nr = {t.nr: t for t in cands if t.nr}
            by_key = {t.key: t for t in cands}
            first: list[Topic] = []
            for r in rows:
                t = by_nr.get(str(r.get("nr"))) if r.get("nr") else by_key.get(f"title:{_norm(str(r.get('title', '')))}")
                if t is None or any(t is x for x in first):
                    continue
                if r.get("aufbau"):
                    t.aufbau = str(r["aufbau"])
                first.append(t)
            self._note(f"Monatsplan {self.opts.date}: " + ", ".join(f"Nr. {t.nr or t.title}" for t in first))
            ids = {id(t) for t in first}
            return first + [t for t in cands if id(t) not in ids]
        except Exception as exc:  # noqa: BLE001
            self._note(f"Monatsplan nicht gelesen ({exc!r}); bisherige Wahl")
            return cands

    def select_topics(self) -> tuple[list[Topic], list[str]]:
        quota = self.opts.topics
        if not self.opts.topic_nr:                               # a rerun on the same day never produces more than the daily target
            done_today = sum(1 for d in self.state.done_list(self.brand_id) if d.get("date") == self.opts.date)
            quota = max(0, self.opts.topics - done_today)
            if quota == 0:
                return [], [f"Tageskontingent: {done_today} Thema/Themen am {self.opts.date} schon produziert, Ziel {self.opts.topics}"]
        src = self.s.topic_source
        cands = self._apply_plan(ordered_candidates(self.kp, src))
        chosen: list[Topic] = []
        skipped: list[str] = []
        runtime = load_aufbauten(self.brand_id)                 # brands/<id>/aufbauten.yaml wins over config/daily.yaml
        built = [a for a in runtime if a.get("gebaut")]
        last = self.state.last_done(self.brand_id)
        prev_aufbau = (last or {}).get("aufbau")
        recordings = {str(k): v for k, v in (src.get("recordings") or {}).items()}
        done_stems = csv_done_stems(self.brand_id)
        done_titles = csv_done_titles(self.brand_id)
        reserved_days = [str(d) for d in (self.s.get("reserved_days") or [])]
        exclude_words = [str(w).lower() for w in (src.get("exclude_title_words") or [])]
        lim = src.get("limited_heading") or {}                    # Revlore: Motor topics at most every third topic (Hauptsitzung 03.11.)
        lim_word = str(lim.get("contains") or "").lower()
        lim_every = int(lim.get("every") or 0)
        nr_limited = {str(t.nr): lim_word in str((t.extra or {}).get("heading", "")).lower() for t in cands if t.nr} if lim_word else {}
        limited_history = [nr_limited.get(str(d.get("nr")), False) for d in self.state.done_list(self.brand_id)] if lim_word else []
        for t in cands:
            if len(chosen) >= quota:
                break
            if self.opts.topic_nr and t.nr != str(self.opts.topic_nr):
                continue
            if t.done_marker or self.state.is_done(self.brand_id, t):
                continue
            if t.reserved or (t.day and t.day in reserved_days):
                skipped.append(f"{t.describe()}: reserviert für die Marken-Sitzung ({'Zeile' if t.reserved else 'Tag ' + str(t.day)})")
                continue
            word = next((w for w in exclude_words if w in t.title.lower()), None)
            if word:
                skipped.append(f"{t.describe()}: nicht geeignet (Titel nennt {word!r}; braucht neuen Code laut config/daily.yaml)")
                continue
            if lim_word and not self.opts.topic_nr and nr_limited.get(str(t.nr), False) and not limited_allowed(limited_history, lim_every):
                skipped.append(f"{t.describe()}: Themen aus '{lim.get('contains')}' höchstens jedes {lim_every}. Thema (Hauptsitzung 03.11.)")
                continue
            cal = calendar_entry(self.brand_id, t)
            research = research_entry(self.brand_id, t, cal)
            refs = source_refs(t, cal, research)
            if cal and not t.calendar_id:
                t.calendar_id = cal.get("topic_id")
            if t.calendar_id and re.sub(r"-(de|en)$", "", t.calendar_id) in done_stems:
                skipped.append(f"{t.describe()}: im Redaktionsplan schon fertig ({t.calendar_id})")
                continue
            tn = _norm(t.title)
            if len(tn) >= 12 and any(tn in pt or (len(pt) >= 12 and pt in tn) for pt in done_titles):
                skipped.append(f"{t.describe()}: im Redaktionsplan schon fertig (Titel)")
                continue
            options = self._aufbau_options(runtime, built, t.nr)
            if not options:
                skipped.append(f"{t.describe()}: braucht Modell oder Aufbau (kein gebauter Aufbau in brands/{self.brand_id}/aufbauten.yaml trägt Nr. {t.nr})")
                continue
            by_letter = {o["kuerzel"]: o for o in options}
            letters = list(by_letter)
            planned = t.aufbau
            other = chosen[0].extra.get("aufbau_final") if chosen else None
            note = ""
            if planned in by_letter:
                final = planned
                if final == other:
                    alts = [x for x in letters if x != other]
                    if alts:
                        final = alts[0]
                        note = f"Aufbau {planned} wie Thema 1 des Tages, ersetzt durch {final}"
                    else:
                        note = f"Aufbau {planned} wie Thema 1 des Tages (kein anderer passt)"
            else:
                pool = [x for x in letters if x != other and x != prev_aufbau] or [x for x in letters if x != other] or letters
                final = pool[0]
                note = (f"Aufbau {planned} ist nicht gebaut oder passt nicht zum Thema, ersetzt durch {final}" if planned
                        else f"Aufbau {final} nach Wechselregel gewählt")
            opt = by_letter[final]
            if opt["quellen"]:                                   # sources named by the brand session for this topic
                refs = [SourceRef(id=f"S{k}", url=str(q.get("url", "")), title=str(q.get("titel") or q.get("title") or ""),
                                  checked_at=str(q.get("checked_at") or "")) for k, q in enumerate(opt["quellen"], 1) if q.get("url")]
            if opt["hinweis"]:
                t.extra["topic_hint"] = opt["hinweis"]
            if src.get("require_sources", True) and not refs:
                skipped.append(f"{t.describe()}: keine geprüfte Quelle (Kalender oder aufbauten.yaml)")
                continue
            if src.get("require_recording"):
                rec = recordings.get(str(t.nr)) or recording_for_title(self.brand_id, t.title)
                if not rec:
                    skipped.append(f"{t.describe()}: keine Aufzeichnung zugeordnet (brands/{self.brand_id}/echtlauf/specs)")
                    continue
                t.extra["recording"] = rec
            t.extra.update({"aufbau_final": final, "aufbau_note": note, "cal": cal, "research": research, "refs": refs,
                            "aufbau_spec": opt["spec"]})
            t.extra["evidence"] = self._evidence_text(t, cal, research, refs, opt, t.extra.get("recording"))
            chosen.append(t)
            limited_history.append(nr_limited.get(str(t.nr), False))
        return chosen, skipped

    def _evidence_text(self, t: Topic, cal: dict | None, research: dict | None, refs: list[SourceRef], opt: dict,
                       recording: str | None) -> str:
        """Everything a number of the script may come from: the topic row, calendar angle and notes, research evidence,
        source titles, the brand session's per-topic hint and, for Promptwerk, the recorded run itself."""
        parts = [t.title, t.hook_idea]
        if cal:
            parts += [str(cal.get("title", "")), str(cal.get("angle", "")), str(cal.get("notes", ""))]
        if research:
            parts += [str(e) for e in (research.get("source_evidence") or [])] + [str(research.get("notes", ""))]
        parts += [r.title for r in refs]
        if opt.get("hinweis"):
            parts.append(opt["hinweis"])
        if recording:
            from ..config import BRANDS_DIR
            rec_dir = BRANDS_DIR / self.brand_id / "echtlauf" / "recordings" / recording
            for name in ("transcript.json", "outcome.json", "meta.json"):
                f = rec_dir / name
                if f.exists():
                    parts.append(f.read_text(encoding="utf-8")[:30000])
        return "\n".join(p for p in parts if p)

    # ------------------------------------------------------------------ model stage
    def _mock_plan(self, lang: str, video_id: str, topic: Topic, source: dict | None = None) -> dict:
        """Attrappe: DE = the example plan of the chosen Aufbau, EN = a copy of the DE plan (always structurally identical)."""
        ex = source if source is not None else self._de_setup(topic)["example"]
        plan = json.loads(json.dumps(ex, ensure_ascii=False))
        plan["video_id"] = video_id
        plan["language"] = lang
        plan["notes"] = (f"ATTRAPPE des Tagesläufers ({self.opts.date}): Beispielplan der Marke unter neuer id, Thema laut Konzeptplan "
                         f"Nr. {topic.nr} '{topic.title}' noch nicht geschrieben (Attrappe statt Modell). Nicht rendern, nicht exportieren.")
        return plan

    @staticmethod
    def _stamp(plan: dict, video_id: str, lang: str, brand_id: str) -> dict:
        """The runner decides ids and language (a changed video_id would send the render output to another folder)."""
        plan["video_id"], plan["language"], plan["brand_id"] = video_id, lang, brand_id
        return plan

    def _expected_recording(self, topic: Topic | None, lang: str) -> str | None:
        rec = (topic.extra.get("recording") if topic else None) or self._recording
        if not rec or not self.s.topic_source.get("require_recording"):
            return None
        return rec if lang == "de" else f"{rec}-en"

    def _ask(self, system: str, user: str, video_cost_id: str, purpose: str, lr: LangResult) -> dict:
        llm = self.s.llm
        self._note(f"{purpose}: Prompt {len(system) + len(user)} Zeichen (System {len(system)}, Aufgabe {len(user)})")
        res = self.provider.complete(system, user, max_tokens=int(llm.get("max_output_tokens", 20000)),
                                     temperature=float(llm.get("temperature", 0.4)))
        usd = log_llm_cost(self.costs, video_cost_id, purpose, res, llm)
        lr.llm_calls += 1
        lr.llm_tokens_in += res.input_tokens
        lr.llm_tokens_out += res.output_tokens
        lr.llm_tokens_cache += res.cache_tokens
        lr.llm_usd += usd
        self._note(f"{purpose}: {res.provider} {res.model} in={res.input_tokens} out={res.output_tokens} cache={res.cache_tokens} {res.note}")
        with self.run_log.open("a", encoding="utf-8") as fh:
            fh.write(f"\n--- model answer ({purpose}) ---\n{res.text[:200000]}\n--- end ---\n")
        return extract_json(res.text)

    def _de_setup(self, topic: Topic) -> dict:
        """Scene types, hook types, example plan, Aufbau texts for the German prompt and the repair rounds."""
        ctx = self.context()
        aufbau = topic.extra.get("aufbau_final")
        spec = topic.extra.get("aufbau_spec") or {}
        aufbau_text = ctx.konzeptplan.aufbauten.get(aufbau or "", "") or (spec.get("name", "") if spec else "")
        hints = [n for n in (topic.extra.get("aufbau_note"), spec.get("hinweis") if spec else self.s.aufbau.get("note"),
                             ("Hinweis der Marken-Sitzung zu diesem Thema: " + topic.extra["topic_hint"]) if topic.extra.get("topic_hint") else None) if n]
        scene_types = list(dict.fromkeys(self.s.scene_types + list(spec.get("szenentypen") or [])))
        hook_types = [h for h in self.s.hook_types if h in scene_types] or self.s.hook_types
        example = ctx.example_de
        if spec and spec.get("beispielplan") and (ROOT / spec["beispielplan"]).exists():
            example = json.loads((ROOT / spec["beispielplan"]).read_text(encoding="utf-8"))
        return {"aufbau": aufbau, "aufbau_text": aufbau_text, "hints": hints, "scene_types": scene_types, "hook_types": hook_types,
                "example": example, "aufbau_types": [t for t in (spec.get("szenentypen") or []) if t in scene_types]}

    def generate_de(self, topic: Topic, video_id: str, version: str, lr: LangResult) -> dict | None:
        ctx = self.context()
        refs: list[SourceRef] = topic.extra.get("refs") or []
        cost_id = f"{video_id}-{version}"
        window = self.s.char_window("de")
        setup = self._de_setup(topic)
        topic.extra["scene_types"] = setup["scene_types"]
        if self.is_mock:
            plan = self._mock_plan("de", video_id, topic)
            self.provider.queue.append(json.dumps(plan, ensure_ascii=False))
            refs = [SourceRef(id=s["id"], url=s["url"], title=s.get("title", ""), checked_at=s.get("checked_at", "")) for s in plan.get("sources", [])]
            topic.extra["refs"] = refs
        system = system_prompt_de(ctx, window, scene_types=setup["scene_types"], hook_types=setup["hook_types"], example=setup["example"],
                                  aufbau_letter=setup["aufbau"], aufbau_text=setup["aufbau_text"],
                                  aufbau_hint="\n".join(f"- {h}" for h in setup["hints"]), aufbau_types=setup["aufbau_types"])
        user = user_prompt_de(topic, video_id, refs, topic.extra.get("cal"), topic.extra.get("research"), window)
        rounds = int(self.s.llm.get("repair_rounds", 2))
        plan = None
        base_user = user
        for attempt in range(rounds + 1):
            try:
                plan = self._stamp(self._ask(system, user, cost_id, f"plan de (round {attempt})", lr), video_id, "de", self.brand_id)
            except RateLimited:
                raise
            except Exception as exc:  # noqa: BLE001 - model or JSON problems are reported, not fatal
                lr.errors.append(f"Modellaufruf DE: {exc!r}")
                return None
            allowed = set(setup["scene_types"]) | ({b.get("scene_type") for b in setup["example"].get("beats", [])} if self.is_mock else set())
            v = validate_plan(plan, ctx, refs, "de", char_window=window, require_recording=bool(self.s.topic_source.get("require_recording")),
                              allowed_types=allowed, chars_per_second=self.s.chars_per_second("de"),
                              evidence=None if self.is_mock else topic.extra.get("evidence", ""),
                              expected_recording=None if self.is_mock else self._expected_recording(topic, "de"), check_length=not self.is_mock)
            if setup["aufbau_types"]:
                used = sum(1 for b in plan.get("beats", []) if b.get("scene_type") in setup["aufbau_types"])
                if used < 2:
                    v.warnings.append(f"Bildaufbau {setup['aufbau']}: nur {used} Beat(s) mit den Szenentypen des Aufbaus "
                                      f"({', '.join(setup['aufbau_types'])}); mindestens zwei erwartet")
            lr.validation_errors, lr.validation_warnings = v.errors, v.warnings
            if v.ok:
                if v.warnings:
                    self._note(f"DE-Plan Runde {attempt}: Hinweise: " + "; ".join(v.warnings[:4]))
                break
            self._note(f"DE-Plan Runde {attempt}: {len(v.errors)} Fehler: " + "; ".join(v.errors[:6]))
            if attempt == rounds or self.is_mock:
                return None
            user = base_user + "\n\n" + repair_prompt(v.errors, v.warnings, "de") + "\n\nDein bisheriger Plan:\n" + json.dumps(plan, ensure_ascii=False)
        return plan

    def generate_en(self, plan_de: dict, video_id_en: str, version: str, lr: LangResult, evidence: str = "") -> dict | None:
        ctx = self.context()
        evidence = evidence + "\n" + " ".join(b.get("spoken", "") for b in plan_de.get("beats", [])) + "\n" + str(plan_de.get("title", ""))
        refs = [SourceRef(id=s["id"], url=s["url"], title=s.get("title", ""), checked_at=s.get("checked_at", "")) for s in plan_de.get("sources", [])]
        cost_id = f"{video_id_en}-{version}"
        window = self.s.char_window("en")
        if self.is_mock:
            plan = self._mock_plan("en", video_id_en, Topic(brand_id=self.brand_id, nr=None, title=plan_de.get("title", "")), source=plan_de)
            self.provider.queue.append(json.dumps(plan, ensure_ascii=False))
        system = system_prompt_en()
        user = user_prompt_en(plan_de, video_id_en, window, ctx.example_en if self.s.get("en_example", False) else None)
        rounds = int(self.s.llm.get("repair_rounds", 2))
        plan = None
        base_user = user
        for attempt in range(rounds + 1):
            try:
                plan = self._stamp(self._ask(system, user, cost_id, f"plan en (round {attempt})", lr), video_id_en, "en", self.brand_id)
            except RateLimited:
                raise
            except Exception as exc:  # noqa: BLE001
                lr.errors.append(f"Modellaufruf EN: {exc!r}")
                return None
            allowed = set(self.s.scene_types) | {b.get("scene_type") for b in plan_de.get("beats", [])}
            v = validate_plan(plan, ctx, refs, "en", char_window=window, require_recording=bool(self.s.topic_source.get("require_recording")),
                              allowed_types=allowed, chars_per_second=self.s.chars_per_second("en"),
                              evidence=None if self.is_mock else evidence,
                              expected_recording=None if self.is_mock else self._expected_recording(None, "en"), check_length=not self.is_mock)
            errors = v.errors + [f"Struktur: {x}" for x in compare_structure(plan_de, plan)]
            lr.validation_errors, lr.validation_warnings = errors, v.warnings
            if not errors:
                break
            self._note(f"EN-Plan Runde {attempt}: {len(errors)} Fehler: " + "; ".join(errors[:6]))
            if attempt == rounds or self.is_mock:
                return None
            user = base_user + "\n\n" + repair_prompt(errors, v.warnings, "en") + "\n\nYour previous plan:\n" + json.dumps(plan, ensure_ascii=False)
        return plan

    def repair_after_dry_run(self, topic: Topic, plan: dict, video_id: str, version: str, lr: LangResult, lang: str,
                             compare_to: dict | None = None) -> dict | None:
        """One model round with the renderer's output of the failed dry run; None when the answer is invalid."""
        ctx = self.context()
        window = self.s.char_window(lang)
        types = [b.get("scene_type") for b in plan.get("beats", []) if b.get("scene_type")]
        refs = (topic.extra.get("refs") or []) if lang == "de" else \
            [SourceRef(id=s["id"], url=s["url"], title=s.get("title", ""), checked_at=s.get("checked_at", "")) for s in plan.get("sources", [])]
        limits = "; ".join(f"{t}: " + ", ".join(f"{k} {v}" for k, v in lim.items()) for t, lim in ctx.limits.items() if t in set(types) and lim)
        system = repair_system(lang, ctx.brand.name, ctx.scene_docs_for(list(dict.fromkeys(types))), limits)
        user = dry_run_repair_user(lang, lr.dry_run_diag, plan)
        try:
            fixed = self._stamp(self._ask(system, user, f"{video_id}-{version}", f"plan {lang} (dry-run repair)", lr), video_id, lang, self.brand_id)
        except RateLimited:
            raise
        except Exception as exc:  # noqa: BLE001
            lr.errors.append(f"Reparatur nach Trockenlauf: {exc!r}")
            return None
        evidence = None if self.is_mock else (topic.extra.get("evidence", "") + "\n" + " ".join(b.get("spoken", "") for b in plan.get("beats", [])) +
                                              "\n" + str(plan.get("title", "")) + "\n" + str((plan.get("layout") or {}).get("description", "")))
        v = validate_plan(fixed, ctx, refs, lang, char_window=window, require_recording=bool(self.s.topic_source.get("require_recording")),
                          allowed_types=set(types), chars_per_second=self.s.chars_per_second(lang), evidence=evidence,
                          expected_recording=None if self.is_mock else self._expected_recording(topic, lang))
        errors = v.errors + ([f"Struktur: {x}" for x in compare_structure(compare_to, fixed)] if compare_to else [])
        if plan.get("beats") and fixed.get("beats") and " ".join(b.get("spoken", "") for b in plan["beats"]) != " ".join(b.get("spoken", "") for b in fixed["beats"]):
            errors.append("Sprechtext wurde verändert (nicht erlaubt nach dem Trockenlauf)")
        if errors:
            lr.errors.append("Reparatur nach Trockenlauf ungültig: " + "; ".join(errors[:4]))
            return None
        if self.opts.prototype and lang == "de":
            fixed["notes"] = f"Tagesläufer-Prototyp ({self.opts.date}). {fixed.get('notes', '')}".strip()
        return fixed

    # ------------------------------------------------------------------ chain
    def dry_run(self, plan_path: Path, version: str, lr: LangResult) -> bool:
        cmd = [PY, str(self.s.render_script), str(plan_path), "--version", f"{version}dry", "--tts", "mock", "--no-render", *self.s.render_args]
        timeout = float(self.s.get("dry_run_timeout_s", 900))
        r = self._run(cmd, timeout)
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode == 5:                                   # mock voice too slow/fast: skip the length gate, check the build
            m = re.search(r"length (\d+(?:\.\d+)?) s outside", out)
            if m:
                cut = max(20.0, float(m.group(1)) - 0.3)
                msg = f"Trockenlauf: Mock-Länge {m.group(1)} s (keine echte Stimme); Prüfung als Auszug {cut:.0f} s"
                if msg not in lr.notes:
                    lr.notes.append(msg)
                r = self._run(cmd + ["--excerpt", f"{cut:.1f}"], timeout)
                out = (r.stdout or "") + (r.stderr or "")
        lr.dry_run_exit = r.returncode
        lines = [ln.rstrip() for ln in out.splitlines() if ln.strip()]
        # review findings (unresolved word anchors, placeholder assets, schematic scenes) end in HUMAN_REVIEW later: repair them too
        review = [ln.strip() for ln in lines if "[review" in ln and "NOT" in ln]
        bad = [ln.strip() for ln in lines if "[fail" in ln or "[review" in ln or "plan problems" in ln or "problems:" in ln
               or ln.strip().startswith(("assets:", "layout:"))]
        if "Traceback" in out:
            tb = lines[-14:]
            lr.dry_run_note = "; ".join(tb[-3:])[:600]
        else:
            tb = []
            lr.dry_run_note = "; ".join(bad[:8])[:600]
        lr.dry_run_diag = ("\n".join(lines[-45:]) if not tb else "\n".join(tb))[-3500:]
        lr.dry_run_review = review
        if r.returncode != 0:
            lr.errors.append(f"Trockenlauf Exit {r.returncode}: {lr.dry_run_note or (lines[-1] if lines else '')}")
        return r.returncode == 0 and not review

    def dry_run_with_repairs(self, topic: Topic, plan: dict, path: Path, video_id: str, version: str, lr: LangResult, lang: str,
                             tr: TopicResult, compare_to: dict | None = None) -> dict:
        """Dry run; renderer findings go back to the model (up to `dry_run_repairs` rounds). Returns the final plan."""
        rounds = int(self.s.get("dry_run_repairs", 2))
        ok = self.dry_run(path, version, lr)
        tries = 0
        while not ok and tries < rounds and not self.is_mock:
            tries += 1
            self._note(f"Trockenlauf {lang} fehlgeschlagen (Exit {lr.dry_run_exit}); Reparaturrunde {tries}")
            fixed = self.repair_after_dry_run(topic, plan, video_id, version, lr, lang, compare_to)
            if fixed is None:
                break
            plan = fixed
            for n in prepare_assets(plan, self.brand_id, self.s.material_folders):
                tr.notes.append(n)
            path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            lr.errors = [e for e in lr.errors if not e.startswith(("Trockenlauf", "Reparatur"))]
            lr.dry_run_repairs = tries
            ok = self.dry_run(path, version, lr)
        if lr.dry_run_exit == 0 and lr.dry_run_review:
            lr.notes.append("Trockenlauf: Befund(e) der Stufe review bleiben, der Prüfbericht wird HUMAN_REVIEW: " + "; ".join(lr.dry_run_review)[:300])
        lr.dry_run_done = True
        return plan

    def _voice_mode(self) -> str | None:
        max_flash = self.opts.max_flash if self.opts.max_flash is not None else int(self.s.get("flash_requests_per_brand_per_day", 4))
        used = self.state.tts_used(self.brand_id, self.opts.date, "flash")
        cap = int(self.s.get("flash_global_cap", 100)) - int(self.s.get("flash_global_reserve", 12))
        global_used = flash_used_since_quota_reset()
        if global_used >= cap:                                   # the quota of 100 per day is shared by all sessions
            self._note(f"gemeinsames Flash-Kontingent fast verbraucht ({global_used} Anfragen seit dem Reset, Grenze {cap})")
        elif used < max_flash:
            return "flash"
        pro = self.opts.pro_fallback if self.opts.pro_fallback is not None else bool(self.s.get("pro_fallback", False))
        return "pro" if pro else None

    def render(self, plan_path: Path, video_id: str, version: str, lang: str, lr: LangResult) -> bool:
        if (DATA_DIR / "render.pause").exists():
            lr.errors.append("data/render.pause vorhanden: Render angehalten")
            return False
        mode = self._voice_mode()
        if mode is None:
            lr.voice = "none"
            lr.errors.append("Flash-Kontingent der Marke für heute verbraucht; kein Pro-Ausweich (--pro-fallback)")
            return False
        extra_env = {}
        if mode == "pro":
            extra_env["GEMINI_TTS_MODEL"] = str(voices_config()["providers"]["gemini"].get("fallback_model", ""))
        reuse: str | None = None
        pre = (self.s.get("voice_pre") or {}).get(lang)
        if pre:                                                 # e.g. Promptwerk: TTS-only spelling, then --reuse-voice
            cmd = [PY, str(ROOT / pre[0]), str(plan_path), "--version", version, *pre[1:]]
            r = self._run(cmd, 900, extra_env)
            self.state.tts_add(self.brand_id, self.opts.date, mode)
            wav = STORAGE_DIR / "direction" / f"voice_{video_id}_{version}_gemini.wav"
            if r.returncode != 0 or not wav.exists():
                lr.errors.append(f"Stimme ({pre[0]}) Exit {r.returncode}")
                return False
            reuse = str(wav)
        cmd = [PY, str(ROOT / "scripts" / "render_queue.py"), self.brand_id, "--", str(self.s.render_script), str(plan_path),
               "--version", version, "--tts", "gemini", *self.s.render_args]
        if reuse:
            cmd += ["--reuse-voice", reuse]
        self._note(f"Render {video_id}-{version} ({'Pro' if mode == 'pro' else 'Flash'}{', Stimme wiederverwendet' if reuse else ''}) über die Warteschlange")
        r = self._run(cmd, float(self.s.get("render_timeout_s", 5400)), extra_env)
        out = (r.stdout or "") + (r.stderr or "")
        if not reuse and r.returncode not in (2, 4) and "voice: gemini" in out:
            self.state.tts_add(self.brand_id, self.opts.date, mode)
        lr.voice = "reused" if reuse else mode
        lr.render_exit = r.returncode
        man = STORAGE_DIR / "direction" / f"{video_id}-{version}" / "manifest.json"
        if r.returncode != 0 or not man.exists():
            tail = "; ".join(ln.strip() for ln in out.strip().splitlines()[-4:])
            lr.errors.append(f"Render Exit {r.returncode}: {tail[:400]}")
            return False
        m = json.loads(man.read_text(encoding="utf-8"))
        lr.status = str(m.get("status", ""))
        lr.duration_s = (m.get("render") or {}).get("duration")
        lr.sfx_stem_peak = ((m.get("sound") or {}).get("measured") or {}).get("sfx_peak_dbfs")
        lr.cost_usd_variable = (m.get("cost") or {}).get("usd_variable")
        if lr.status == "FAILED":
            failed = []
            try:
                rep = json.loads((STORAGE_DIR / "direction" / f"{video_id}-{version}" / "report.json").read_text(encoding="utf-8"))
                failed = [f"{f['id']}: {str(f.get('detail'))[:120]}" for f in rep.get("findings", []) if not f.get("ok") and f.get("severity") == "fail"]
            except (OSError, json.JSONDecodeError, KeyError):
                pass
            lr.errors.append("Prüfbericht FAILED" + (": " + "; ".join(failed[:4]) if failed else " (report.json)"))
            return False
        return True

    def overlap(self, video_id: str, version: str, lr: LangResult) -> bool:
        project = STORAGE_DIR / "direction" / f"{video_id}-{version}" / "project"
        r = self._run(["node", str(ROOT / "scripts" / "overlap_check.mjs"), str(project)], 900)
        last = next((ln for ln in reversed((r.stdout or "").splitlines()) if ln.strip().startswith("{")), "")
        try:
            data = json.loads(last) if last else {}
        except json.JSONDecodeError:
            data = {}
        lr.overlaps = len(data.get("overlaps", [])) if data else None
        lr.small_text = len(data.get("small_text", [])) if data else None
        if r.returncode != 0 or lr.overlaps is None:
            lr.errors.append(f"overlap_check Exit {r.returncode}: {lr.overlaps if lr.overlaps is not None else 'keine Auswertung'}")
            return False
        if lr.small_text:
            lr.notes.append(f"small_text: {lr.small_text} Text(e) unter 24 px")
        return True

    def export(self, plan_path: Path, version: str, short: str, lr: LangResult) -> bool:
        r = self._run([PY, str(ROOT / "scripts" / "export_production_folder.py"), str(plan_path), "--version", version, "--short", short], 600)
        m = re.search(r"^folder: (.+)$", r.stdout or "", re.M)
        if r.returncode != 0 or not m:
            lr.errors.append(f"Export Exit {r.returncode}: {(r.stdout or r.stderr).strip().splitlines()[-1:]}")
            return False
        lr.export_folder = m.group(1).strip()
        if self.opts.prototype:
            v = Path(lr.export_folder) / "Veröffentlichung.md"
            if v.exists():
                v.write_text(v.read_text(encoding="utf-8") + f"\n\n## Tagesläufer-Prototyp\n\nDieses Video entstand als Prototyp des Tagesläufers "
                             f"({self.opts.date}): Skript und Regie von claude -p (Sonnet 5.5), Prüfung wie bei den Marken-Sitzungen. "
                             f"Nicht veröffentlicht.\n", encoding="utf-8")
        return True

    # ------------------------------------------------------------------ one topic
    def produce_topic(self, topic: Topic) -> TopicResult:
        yyyymmdd = self.opts.date.replace("-", "")
        slot = next_slot(self.brand_id, yyyymmdd)
        ids = {lang: f"{self.brand_id}-{yyyymmdd}-d{slot}-{lang}" for lang in self.opts.languages}
        version = next_version(ids["de"], str(self.s.get("version_prefix", "D")))
        tr = TopicResult(key=topic.key, nr=topic.nr, title=topic.title, aufbau=topic.extra.get("aufbau_final"), aufbau_note=topic.extra.get("aufbau_note", ""))
        self._recording = topic.extra.get("recording")
        self._note(f"Thema {topic.describe()} -> {ids['de']} / {ids.get('en', '-')} Fassung {version}")
        if not self.is_mock:
            self.state.mark_started(self.brand_id, topic, self.opts.date, list(ids.values()))
        refs: list[SourceRef] = topic.extra.get("refs") or []
        do_check = self.opts.source_check if self.opts.source_check is not None else bool(self.s.get("source_check", True))
        if do_check and refs and not self.is_mock:
            check_sources(refs, self.opts.date)
            for r in refs:
                if r.reachable is False:
                    tr.notes.append(f"Quelle {r.id} {r.note}: checked_at bleibt {r.checked_at}")
        plans: dict[str, dict] = {}
        paths: dict[str, Path] = {}
        # --- German plan, then its dry run (renderer findings go back to the model)
        lr_de = LangResult(video_id=ids["de"], version=version)
        tr.langs["de"] = lr_de
        plan_de = self.generate_de(topic, ids["de"], version, lr_de)
        if plan_de is None:
            tr.errors.append("kein gültiger deutscher Plan")
            return tr
        for n in prepare_assets(plan_de, self.brand_id, self.s.material_folders):
            tr.notes.append(n)
        if tr.aufbau_note:
            plan_de["notes"] = f"{plan_de.get('notes', '')} Bildaufbau: {tr.aufbau_note}.".strip()
        if self.opts.prototype:
            plan_de["notes"] = f"Tagesläufer-Prototyp ({self.opts.date}). {plan_de.get('notes', '')}".strip()
        paths["de"] = DATA_DIR / "direction" / f"{ids['de']}.{version}.json"
        paths["de"].write_text(json.dumps(plan_de, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        lr_de.plan_path, lr_de.plan_ok = str(paths["de"]), True
        plan_de = self.dry_run_with_repairs(topic, plan_de, paths["de"], ids["de"], version, lr_de, "de", tr)
        plans["de"] = plan_de
        if lr_de.dry_run_exit != 0:
            tr.errors.append("deutsche Fassung besteht den Trockenlauf nicht: englische Fassung nicht erzeugt (spart Modellaufrufe)")
            return tr
        # --- English plan from the same scenes, then its dry run
        if "en" in self.opts.languages:
            lr_en = LangResult(video_id=ids["en"], version=version)
            tr.langs["en"] = lr_en
            plan_en = self.generate_en(plan_de, ids["en"], version, lr_en, evidence=topic.extra.get("evidence", ""))
            if plan_en is None:
                tr.errors.append("kein gültiger englischer Plan")
            else:
                paths["en"] = DATA_DIR / "direction" / f"{ids['en']}.{version}.json"
                paths["en"].write_text(json.dumps(plan_en, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                lr_en.plan_path, lr_en.plan_ok = str(paths["en"]), True
                plans["en"] = self.dry_run_with_repairs(topic, plan_en, paths["en"], ids["en"], version, lr_en, "en", tr, compare_to=plan_de)
        if self.opts.dry_run:
            return tr
        # --- voice, render, checks, export per language
        short_de = self._short_title(plan_de)
        exported: list[str] = []
        for lang, p in paths.items():
            lr = tr.langs[lang]
            if lr.dry_run_exit != 0:
                lr.errors.append("Trockenlauf nicht bestanden: kein Render")
                continue
            if lang == "en" and tr.langs["de"].render_exit != 0:
                lr.errors.append("deutsche Fassung nicht gerendert: englische übersprungen")
                continue
            if not self.render(p, ids[lang], version, lang, lr):
                continue
            if not self.overlap(ids[lang], version, lr):
                continue
            if self.opts.no_export:
                lr.notes.append("Export ausgelassen (--no-export)")
                continue
            short = short_de if lang == "de" else f"{short_de} EN"
            if not self.export(p, version, short, lr):
                continue
            exported.append(ids[lang])
            if self.s.get("write_csv", True):
                self._write_csv(plans[lang], lr, lang, topic)
        if exported and not self.opts.no_mark:
            marker = f"Tagesläufer: produziert {self.opts.date} ({', '.join(f'{v}-{version}' for v in exported)})"
            status = {lang: tr.langs[lang].status for lang in paths}
            self.state.mark_done(self.brand_id, topic, self.opts.date, [f"{v}-{version}" for v in exported], tr.aufbau, status)
            if self.s.get("mark_konzeptplan", True):
                changed = mark_konzeptplan(self.s.business_path("konzeptplan"), topic, marker)
                tr.marked = bool(changed)
                tr.notes.append(f"Konzeptplan markiert: {', '.join(changed) or 'keine Zeile gefunden'}")
        return tr

    def _short_title(self, plan: dict) -> str:
        short = str((plan.get("layout") or {}).get("short_title") or plan.get("title") or "Video")
        short = re.sub(r"[<>:\"/\\|?*]+", " ", short)
        short = re.sub(r"\s+", " ", short).strip(" .")
        return short[:40] or "Video"

    def _write_csv(self, plan: dict, lr: LangResult, lang: str, topic: Topic) -> None:
        folder = Path(lr.export_folder)
        try:
            rel = str(folder.relative_to(BUSINESS_DIR))
        except ValueError:
            rel = str(folder)
        tts_model = "Pro" if lr.voice == "pro" else "Flash"
        label = "Tagesläufer-Prototyp" if self.opts.prototype else "Tagesläufer"
        note = (f"{label} {self.opts.date}: Konzeptplan Nr. {topic.nr or '–'} ({topic.reihe or 'Reihe –'}), Bildaufbau {topic.extra.get('aufbau_final') or '–'}"
                f"{' (' + topic.extra.get('aufbau_note') + ')' if topic.extra.get('aufbau_note') else ''}. "
                f"Skript und Regie {self.provider.model} über {'claude -p (Abo, kein Einzelpreis)' if self.provider.name == 'claude_cli' else self.provider.name} "
                f"({lr.llm_calls} Aufruf(e), {lr.llm_tokens_in} ein / {lr.llm_tokens_out} aus / {lr.llm_tokens_cache} Cache Token"
                f"{', ' + str(lr.dry_run_repairs) + ' Reparatur(en) nach dem Trockenlauf' if lr.dry_run_repairs else ''}). "
                f"Gemini {tts_model}{' (Stimme wiederverwendet)' if lr.voice == 'reused' else ''}, Prüfbericht {lr.status}, overlap_check "
                f"{'ohne Befund' if lr.overlaps == 0 else str(lr.overlaps) + ' Befund(e)'}, small_text {'leer' if not lr.small_text else lr.small_text}"
                f"{', Geräusch-Stem ' + format(lr.sfx_stem_peak, '.1f').replace('.', ',') + ' dBFS' if lr.sfx_stem_peak is not None else ''}. "
                f"Variable Kosten {lr.cost_usd_variable if lr.cost_usd_variable is not None else '–'} USD. Material nur aus Bibliothek und Testvideo (0 Credits). Nicht veröffentlicht.")
        row = csv_row(f"{lr.video_id}-{lr.version}", str(plan.get("title", "")), lang, lr.duration_s, self.s.name, rel, note)
        append_csv_row(row)
        lr.csv_written = True

    # ------------------------------------------------------------------ brand run
    def run(self) -> BrandResult:
        br = BrandResult(brand_id=self.brand_id, brand_name=self.s.name, date=self.opts.date, provider=self.provider.name,
                         model=self.provider.model, dry_run=self.opts.dry_run, started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        try:
            chosen, skipped = self.select_topics()
        except Exception as exc:  # noqa: BLE001
            br.errors.append(f"Themenauswahl: {exc!r}")
            return br
        br.skipped = skipped
        from .settings import AUFBAUTEN_WARNINGS
        for w in AUFBAUTEN_WARNINGS:
            if w.startswith(self.brand_id + ":"):
                br.skipped.insert(0, "Hinweis: " + w)
                self._note("Hinweis: " + w)
        if not chosen and not (skipped and skipped[0].startswith("Tageskontingent")):
            br.errors.append("kein produzierbares Thema gefunden")
        for t in chosen:
            try:
                tr = self.produce_topic(t)
            except RateLimited as exc:
                self.rate_limited = True
                br.errors.append(f"Kontingent von claude -p erreicht, Lauf abgebrochen: {exc}")
                self._note(f"Kontingent erreicht: {exc}")
                break
            except Exception as exc:  # noqa: BLE001 - one topic must not stop the brand
                tr = TopicResult(key=t.key, nr=t.nr, title=t.title, aufbau=t.extra.get("aufbau_final"), aufbau_note="", errors=[f"Abbruch: {exc!r}"])
                self._note(f"Thema {t.describe()}: Abbruch {exc!r}")
            br.topics.append(tr)
        br.finished_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        out = RUNS_DIR / f"{self.opts.date}_{self.brand_id}_{datetime.now().strftime('%H%M%S')}.json"
        out.write_text(json.dumps(asdict(br), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return br


def summary_markdown(results: list[BrandResult]) -> str:
    lines = [f"# Tagesläufer {results[0].date if results else ''}", ""]
    for br in results:
        lines.append(f"## {br.brand_name} ({br.brand_id}) · Modell {br.provider} {br.model}{' · Trockenlauf' if br.dry_run else ''}")
        for e in br.errors:
            lines.append(f"- Fehler: {e}")
        for s in br.skipped:
            lines.append(f"- übersprungen: {s}")
        for t in br.topics:
            head = f"- Nr. {t.nr or '–'} {t.title} · Aufbau {t.aufbau or '–'}" + (f" ({t.aufbau_note})" if t.aufbau_note else "")
            lines.append(head)
            for lang, lr in t.langs.items():
                parts = [f"{lr.video_id}-{lr.version}", "Plan ok" if lr.plan_ok else "Plan fehlt",
                         f"Modell {lr.llm_calls} Aufruf(e), {lr.llm_tokens_in} ein / {lr.llm_tokens_out} aus / {lr.llm_tokens_cache} Cache Token",
                         f"Trockenlauf Exit {lr.dry_run_exit}" + (f" nach {lr.dry_run_repairs} Reparatur(en)" if lr.dry_run_repairs else "")]
                if lr.render_exit is not None:
                    parts.append(f"Render Exit {lr.render_exit}, {lr.status}, {lr.duration_s} s, Stimme {lr.voice}")
                if lr.overlaps is not None:
                    parts.append(f"overlap {lr.overlaps}, small_text {lr.small_text}")
                if lr.export_folder:
                    parts.append(f"Export {lr.export_folder}")
                if lr.cost_usd_variable is not None:
                    parts.append(f"variable Kosten {lr.cost_usd_variable} USD")
                lines.append(f"  - {lang}: " + " · ".join(parts))
                for e in lr.errors:
                    lines.append(f"    - Fehler: {e}")
                for n in lr.notes:
                    lines.append(f"    - {n}")
            for n in t.notes:
                lines.append(f"  - {n}")
            for e in t.errors:
                lines.append(f"  - Fehler: {e}")
        lines.append("")
    return "\n".join(lines)
