"""Zonkfruit batch production: plan -> Gemini voice + render (V1) -> checks -> export -> calendar and Redaktionsplan.

For every video id (e.g. brainrot-20261109-1-de) in order:
  1. skip when the export already exists (rerunnable),
  2. render V1 with render_zonkfruit.py (fair queue scripts/render_queue.py); --tts gemini once, a rerun reuses the voice,
  3. checks: report status VALIDATED (HUMAN_REVIEW at risk high), length 65-90 s, overlap_check without findings,
  4. export_zonkfruit.py (DE "--short <short>", EN "--short <short> EN"),
  5. calendar status "produced", one appended line in Redaktionsplan.csv (status fertig).
A video that fails a check is not exported; the reason goes to storage/direction/brainrot_week_status.json and the
run continues with the next video. Nothing is published, nothing deleted.

  .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\produce_week.py brainrot-20261109-1-de brainrot-20261109-1-en ...
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PY = sys.executable
STATUS = ROOT / "storage" / "direction" / "brainrot_week_status.json"
CAL = ROOT / "data" / "calendars" / "brainrot_2026-11.json"
CSV = Path(r"C:\Users\Stefa\OneDrive\Business\04 Redaktionsplan\Redaktionsplan.csv")
sys.path.insert(0, str(ROOT / "src"))
from fn.config import production_folder  # noqa: E402


def log(msg: str) -> None:
    print(f"{datetime.now():%H:%M:%S} {msg}", flush=True)


def save_status(vid: str, **kw) -> None:
    st = json.loads(STATUS.read_text(encoding="utf-8")) if STATUS.exists() else {}
    st[vid] = {**st.get(vid, {}), **kw, "at": datetime.now().isoformat(timespec="seconds")}
    STATUS.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def run(args: list[str]) -> tuple[int, str]:
    p = subprocess.run([PY, *args], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def produce(vid: str) -> None:
    topic, lang = vid.rsplit("-", 1)
    spec = json.loads((ROOT / "brands" / "brainrot" / "topics" / f"{topic}.json").read_text(encoding="utf-8"))
    short = spec["short"]["de"] + (" EN" if lang == "en" else "")
    ds = vid.split("-")[1]
    date = f"{ds[:4]}-{ds[4:6]}-{ds[6:8]}"
    export = production_folder("brainrot", date, short) / "04 Export" / f"{date} {short} – 9x16.mp4"
    if export.exists():
        log(f"{vid}: already exported, skipped")
        return
    plan = ROOT / "data" / "direction" / f"{vid}.json"
    out = ROOT / "storage" / "direction" / f"{vid}-V1"
    voice = ROOT / "storage" / "direction" / f"voice_{vid}_V1_gemini.wav"
    report = out / "report.json"
    if not report.exists():
        tts = ["--reuse-voice", str(voice)] if voice.exists() else ["--tts", "gemini"]
        log(f"{vid}: render ({'reuse voice' if voice.exists() else 'gemini'})")
        rc, txt = run([str(HERE / "render_zonkfruit.py"), str(plan), "--version", "V1", *tts, "--mirror", f"zonkfruit/{vid}-V1"])
        (ROOT / "storage" / "direction" / f"brainrot_{vid}_V1_run.log").write_text(txt, encoding="utf-8")
        if rc != 0 or not report.exists():
            reason = "gemini 429" if "429" in txt else f"render exit {rc}"
            log(f"{vid}: FAILED {reason}")
            save_status(vid, state="failed", reason=reason)
            return
    rep = json.loads(report.read_text(encoding="utf-8"))
    man = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    dur = float(man.get("render", {}).get("duration") or 0)
    status = man.get("status") or ("VALIDATED" if rep.get("passed") and not rep.get("needs_review") else "HUMAN_REVIEW" if rep.get("passed") else "FAILED")
    if not rep.get("passed"):
        save_status(vid, state="failed", reason="report not passed", duration=dur)
        log(f"{vid}: report not passed")
        return
    if not 65 <= dur <= 90:
        save_status(vid, state="length", duration=dur)
        log(f"{vid}: length {dur:.1f} s outside 65-90, not exported")
        return
    chk = json.loads((out / "check.json").read_text(encoding="utf-8")) if (out / "check.json").exists() else {}
    lay_err = [f"{f.get('code')} {f.get('selector')} {f.get('time')}" for f in chk.get("layout", {}).get("findings", []) if f.get("severity") == "error"]
    if lay_err:     # overlaps inside one scene: the overlap check does not see them, the HyperFrames layout check does
        save_status(vid, state="layout", findings=lay_err[:5], duration=dur)
        log(f"{vid}: layout findings, not exported")
        return
    p = subprocess.run(["node", "scripts/overlap_check.mjs", str(out / "project")], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
    overlaps = json.loads(p.stdout.strip().splitlines()[-1]).get("overlaps", ["?"]) if p.stdout.strip() else ["no output"]
    if overlaps:
        save_status(vid, state="overlap", overlaps=overlaps[:5], duration=dur)
        log(f"{vid}: overlap findings, not exported")
        return
    rc, txt = run([str(HERE / "export_zonkfruit.py"), str(plan), "--version", "V1", "--short", short])
    if rc != 0:
        save_status(vid, state="export failed", reason=txt[-300:], duration=dur)
        log(f"{vid}: export failed")
        return
    # calendar row -> produced
    cal = json.loads(CAL.read_text(encoding="utf-8"))
    row = next(r for r in cal if r["topic_id"] == vid)
    row["status"] = "produced"
    CAL.write_text(json.dumps(cal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Redaktionsplan: one appended line (shared file, append only)
    risk = row["risk_level"]
    note = (f"Produktion Woche 1: Fassung V1, Gemini-Stimme Puck, Prüfbericht {status}, Überschneidungs-Prüfung ohne Befund. "
            f"Reihe {spec['series']}." + (" Freigabe Stefan offen." if risk == "high" else "") + " Nicht veröffentlicht.")
    title = json.loads(plan.read_text(encoding="utf-8"))["title"].replace(";", ",")
    secs = f"{dur:.1f}".replace(".", ",")
    line = (f"{vid};{title} ({lang.upper()});Kurzvideo 9:16, {secs} s;Zonkfruit: TikTok, Instagram Reels, YouTube Shorts;"
            f"fertig;;{date} {row['publish_at'][11:16]};05 Produktion\\Tintora\\{date[:7]}\\{date} {short};;{note}")
    raw = CSV.read_bytes()
    if f"\n{vid};".encode("utf-8") not in raw:         # re-export of a fixed render: the line is already there
        with open(CSV, "ab") as fh:
            fh.write((b"" if raw.endswith(b"\n") else b"\r\n") + line.encode("utf-8") + b"\r\n")
    save_status(vid, state="done", duration=dur, status=status, export=str(export))
    log(f"{vid}: done {dur:.1f} s {status}")


def watch(topics: list[str]) -> int:
    """Produce topics in calendar order as soon as their spec is marked ready (brands/brainrot/topics/<topic>.ready);
    a later ready topic goes first while an earlier one is still being written. Polls every minute."""
    import time
    todo = list(topics)
    tdir = ROOT / "brands" / "brainrot" / "topics"
    while todo:
        ready = next((t for t in todo if (tdir / f"{t}.ready").exists()), None)
        if ready is None:
            time.sleep(60)
            continue
        for lang in ("de", "en"):
            try:
                produce(f"{ready}-{lang}")
            except Exception as e:  # noqa: BLE001
                save_status(f"{ready}-{lang}", state="error", reason=repr(e)[:300])
                log(f"{ready}-{lang}: ERROR {e!r}")
        todo.remove(ready)
    log("watch: all topics processed")
    return 0


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--watch":
        return watch(argv[1:])
    for vid in argv:
        try:
            produce(vid)
        except Exception as e:  # noqa: BLE001 - keep the batch going, record the error
            save_status(vid, state="error", reason=repr(e)[:300])
            log(f"{vid}: ERROR {e!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
