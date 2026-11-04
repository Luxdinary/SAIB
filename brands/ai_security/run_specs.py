"""Produce Scutoria videos from specs, one after another, without supervision.

Usage: .venv\\Scripts\\python.exe brands\\ai_security\\run_specs.py [--book-only] <spec.yaml> [...]

Per spec: build the plan (build_plan.py) -> dry run (mock voice, 90-s excerpt) -> Gemini render through
scripts/render_queue.py -> overlap_check.mjs on the rendered project -> export_production_folder.py with the spec's
`short` title -> calendar status `produced` and a row in OneDrive\\Business\\04 Redaktionsplan\\Redaktionsplan.csv.
A failed step stops that spec and is written to the summary; a Gemini quota error (429) stops the whole run.
`--book-only` skips building, rendering and export (for videos that are already exported, e.g. the pilot).
Summary: storage/direction/scutoria_run_<timestamp>.json. Nothing is published or deleted.
"""
from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import time
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import yaml  # noqa: E402

import build_plan  # noqa: E402
from fn.config import production_folder  # noqa: E402

PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
CAL = ROOT / "data" / "calendars" / "ai_security_2026-11.json"
CSV = Path(r"C:\Users\Stefa\OneDrive\Business\04 Redaktionsplan\Redaktionsplan.csv")
PROD = Path(r"C:\Users\Stefa\OneDrive\Business\05 Produktion")
KANAL = "Scutoria: TikTok, Instagram Reels, YouTube Shorts"


def run(args: list[str], timeout: int = 3600, env_extra: dict | None = None) -> tuple[int, str]:
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                       env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", **(env_extra or {})})
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def book(spec: dict, plan_path: Path, version: str, seconds: float | None, model: str = "") -> None:
    vid = spec["id"]
    rows = json.loads(CAL.read_text(encoding="utf-8"))
    row = next(r for r in rows if r["topic_id"] == vid)
    row["status"] = "produced"
    CAL.write_bytes((json.dumps(rows, indent=2, ensure_ascii=False) + "\n").replace("\n", "\r\n").encode("utf-8"))
    pub = datetime.fromisoformat(row["publish_at"]).strftime("%Y-%m-%d %H:%M")
    date = vid.split("-")[1]
    full = production_folder("ai_security", f"{date[:4]}-{date[4:6]}-{date[6:]}", spec["short"])   # 05 Produktion\Scutoria\<JJJJ-MM>\...
    folder = "05 Produktion\\" + str(full.relative_to(full.parents[2]))
    lang = vid.rsplit("-", 1)[-1].upper()
    length = f"Kurzvideo 9:16, {seconds:.1f} s".replace(".", ",") if seconds else "Kurzvideo 9:16"
    note = (f"Format \"Was tust du?\" (Format-Bibel 1.0), Reihe {spec.get('reihe', '')}; Fassung {version}, Gemini-Stimme Charon, "
            f"Prüfbericht VALIDATED, Überschneidungs-Prüfung ohne Befund. Nicht veröffentlicht."
            + (f" Stimmenmodell {model}." if model else ""))
    new = [vid, f"{spec['title']} ({lang})", length, KANAL, "fertig", "", pub, folder, "", note]
    buf = io.StringIO()
    csv.writer(buf, delimiter=";", lineterminator="").writerow(new)
    lines = CSV.read_bytes().decode("utf-8-sig").split("\r\n")      # line-based: other rows stay byte-identical
    hit = [i for i, ln in enumerate(lines) if ln.startswith(vid + ";")]
    if hit:
        lines[hit[0]] = buf.getvalue()
    else:
        while lines and lines[-1] == "":
            lines.pop()
        lines += [buf.getvalue(), ""]
    CSV.write_bytes(("﻿" + "\r\n".join(lines)).encode("utf-8"))


def paid_voice(spec: dict, plan: dict, vid: str, version: str) -> str | None:
    """A Gemini recording of exactly this text (spec `reuse_voice`, or the one an earlier run of this version paid for)."""
    if spec.get("reuse_voice"):
        return spec["reuse_voice"]
    wav = ROOT / "storage" / "direction" / f"voice_{vid}_{version}_gemini.wav"
    side = wav.with_suffix(".json")
    if wav.exists() and side.exists():
        spoken = " ".join(b["spoken"].strip() for b in plan["beats"] if b["spoken"].strip())
        if json.loads(side.read_text(encoding="utf-8")).get("spoken_text", "").strip() == spoken.strip():
            return str(wav.relative_to(ROOT))
    return None


BUDGET = ROOT / "storage" / "direction" / "scutoria_tts_budget.json"


PRO = "gemini-2.5-pro-preview-tts"        # fallback voice model, approved by Stefan on 02.11.2026 (main session)
STATE = {"flash_429": False, "pro_429": False}


def tts_gate(vid: str) -> tuple[str | None, str | None]:
    """Gemini quota of the main session (02.11.2026): allowed ids only, not before `not_before`, at most `max` Flash
    requests (attempts count). After a Flash 429 or with the Flash budget used, one Pro attempt per video if
    `pro_fallback` is set; after a Pro 429 nothing. Returns (blocking step, model); model None means Flash."""
    if not BUDGET.exists():
        return None, None
    b = json.loads(BUDGET.read_text(encoding="utf-8"))
    if vid not in b.get("allow", []):
        return "tts_not_allowed", None
    start = datetime.fromisoformat(b["not_before"])
    while datetime.now(start.tzinfo) < start:
        print(f"{vid}: waiting for the Gemini window ({b['not_before']})", flush=True)
        time.sleep(min(600, (start - datetime.now(start.tzinfo)).total_seconds() + 1))
    b = json.loads(BUDGET.read_text(encoding="utf-8"))    # may have been edited while waiting
    model = None
    if STATE["flash_429"] or b.get("used", 0) >= b.get("max", 0):
        if not b.get("pro_fallback") or STATE["pro_429"]:
            return "tts_budget_used", None
        model, key = PRO, "pro_used"
    else:
        key = "used"
    b[key] = b.get(key, 0) + 1
    BUDGET.write_text(json.dumps(b, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return None, model


def note_voice(vid: str, version: str, folder: Path) -> str:
    """Write the speaking model into Veröffentlichung.md (main session rule 6, 02.11.2026); returns it."""
    man = json.loads((ROOT / "storage" / "direction" / f"{vid}-{version}" / "manifest.json").read_text(encoding="utf-8"))
    tts = man.get("tts") or {}
    model = tts.get("model") or "unbekannt"
    pub = folder / "Veröffentlichung.md"
    if pub.exists() and "Stimme (Modell)" not in pub.read_text(encoding="utf-8"):
        with pub.open("a", encoding="utf-8") as f:
            f.write(f"\n\n**Stimme (Modell):** Google Gemini `{model}`, Sprecher {tts.get('voice', '?')}"
                    + (" (Pro-Stimme als Ausweich, freigegeben von Stefan am 02.11.2026)" if "pro" in model else "") + ".\n")
    return model


def produce(spec_file: Path, book_only: bool) -> dict:
    spec = yaml.safe_load(spec_file.read_text(encoding="utf-8"))
    vid, version = spec["id"], spec.get("version", "F1")
    plan_path = ROOT / "data" / "direction" / f"{vid}.{version}.json"
    res = {"id": vid, "version": version, "spec": spec_file.name, "ok": False}
    if book_only:
        rep = json.loads((ROOT / "storage" / "direction" / f"{vid}-{version}" / "report.json").read_text(encoding="utf-8"))
        book(spec, plan_path, version, rep.get("duration_s") or spec.get("seconds"))
        return {**res, "ok": True, "step": "booked"}
    plan, problems = build_plan.build(spec)
    plan_path.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if problems:
        return {**res, "step": "build", "detail": problems}
    # the mock voice estimates words/s and overshoots texts with many short words; only then use a 90-s excerpt
    # (an excerpt longer than the mock voice stretches the last scene and fails the static check)
    dry = [PY, "scripts/render_direction.py", str(plan_path), "--version", version, "--tts", "mock", "--no-render", "--assets"]
    rc, out = run(dry, timeout=900)
    if "outside 65-90" in out:
        rc, out = run(dry + ["--excerpt", "90"], timeout=900)
    if "dry run: ok" not in out:
        return {**res, "step": "dry_run", "detail": out[-1500:]}
    voice = paid_voice(spec, plan, vid, version)
    for _attempt in range(2):                       # Flash, then at most one Pro attempt for this video
        model = None
        if voice is None:
            gate, model = tts_gate(vid)
            if gate:
                return {**res, "step": gate, "stop": gate == "tts_budget_used"}
        rc, out = run([PY, "scripts/render_queue.py", "ai_security", "--", "scripts/render_direction.py", str(plan_path),
                       "--version", version, *(["--reuse-voice", voice] if voice else ["--tts", "gemini"]),
                       "--assets", "--mirror", f"scutoria-format/{vid}"], timeout=7200,
                      env_extra={"GEMINI_TTS_MODEL": model} if model else None)
        (ROOT / "storage" / "direction" / f"{vid}-{version}.log").write_text(out, encoding="utf-8")
        if voice is None and ("429" in out or "RESOURCE_EXHAUSTED" in out):
            STATE["pro_429" if model else "flash_429"] = True
            if model or STATE["pro_429"]:
                return {**res, "step": "tts_quota_pro" if model else "tts_quota", "detail": out[-800:], "stop": True}
            continue                                # Flash refused: try this video once with Pro
        break
    else:
        return {**res, "step": "tts_quota", "stop": True}
    m = re.search(r"status (\w+) · ([\d.]+) s", out)
    if not m or m.group(1) != "VALIDATED":
        return {**res, "step": "render", "detail": out[-1500:]}
    seconds = float(m.group(2))
    project = f"storage/direction/{vid}-{version}/project"
    rc, out = run(["node", "scripts/overlap_check.mjs", project], timeout=900)
    if rc != 0 or '"overlaps":[]' not in out or ('"small_text":' in out and '"small_text":[]' not in out):
        return {**res, "step": "overlap", "seconds": seconds, "detail": out[-1500:]}
    rc, out = run([PY, "scripts/export_production_folder.py", str(plan_path), "--version", version, "--short", spec["short"]], timeout=900)
    if rc != 0:
        return {**res, "step": "export", "seconds": seconds, "detail": out[-1500:]}
    date = vid.split("-")[1]
    used_model = note_voice(vid, version, production_folder("ai_security", f"{date[:4]}-{date[4:6]}-{date[6:]}", spec["short"]))
    book(spec, plan_path, version, seconds, used_model)
    return {**res, "ok": True, "step": "done", "seconds": seconds, "model": used_model, "export": out.strip().splitlines()[-1]}


def main(argv: list[str]) -> int:
    book_only = "--book-only" in argv
    specs = [Path(a) for a in argv if not a.startswith("--")]
    summary_path = ROOT / "storage" / "direction" / f"scutoria_run_{datetime.now():%Y%m%d_%H%M%S}.json"
    results = []
    for s in specs:
        try:
            r = produce(s, book_only)
        except Exception as exc:  # keep going with the next spec
            r = {"spec": s.name, "ok": False, "step": "exception", "detail": repr(exc)}
        results.append(r)
        summary_path.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{r.get('id', s.name)}: {r['step']}" + (f" {r.get('seconds')} s" if r.get("seconds") else ""), flush=True)
        if r.get("stop"):
            break
    ok = sum(r["ok"] for r in results)
    print(f"{ok}/{len(specs)} ok · summary {summary_path}")
    return 0 if ok == len(specs) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
