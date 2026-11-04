"""Render world chapters with sound: each chapter project (built by welt_probe.py) renders as picture, the pictures
are joined, and the continuous sound mix of the range (tonmix.py) goes underneath. No Gemini.

Short probe in one queue job:

  .venv\\Scripts\\python.exe scripts\\render_queue.py ai_security -- brands\\ai_security\\longform\\welt_render.py ^
      brands\\ai_security\\longform\\plans\\01-ai-rules-start.de.json c0,c1 "Zwischenprobe 01 DE"

Whole video: one queue job per chapter with --render-only, then --join without the lock (concat, mix, encode,
chapters.txt, captions.srt, manifest.json, one still per chapter):

  ... render_queue.py ai_security -- ...\\welt_render.py <plan> c3 "Video 01 DE" --render-only
  ... python.exe ...\\welt_render.py <plan> c0,c1,c2,c3,c4,c5,c6,c7 "Video 01 DE" --join

Output: storage/longform/<video_id>-welt-probe/<name>/<name>.mp4 plus report.json.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[2] / "src"))
os.environ.setdefault("LONGFORM_NO_TTS", "1")

from fn.config import STORAGE_DIR  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.render.director import group_phrases  # noqa: E402
from fn.render import ffmpeg, hyperframes  # noqa: E402
from longform import render_long as rl, tonmix, welt_scene  # noqa: E402


def timing(plan: dict) -> tuple[dict, list[str]]:
    vdir = STORAGE_DIR / "longform" / plan["video_id"] / "voice"
    timed, order = {}, []
    for i, ch in enumerate(plan["chapters"]):
        wav, info = rl.voice_for(ch, plan["lang"], vdir, "gemini", CostLogger(), plan["video_id"])
        words = rl.words_for(ch, wav, info, plan["lang"], vdir)
        tm = rl.time_chapter(ch, words, info["seconds"], plan, first=(i == 0), last=(i == len(plan["chapters"]) - 1))
        tm.update({"wav": wav, "info": info, "index": i})
        timed[ch["id"]] = tm
        order.append(ch["id"])
    return timed, order


def render_chapter(project: Path, raw: Path, seconds: float) -> dict:
    t0 = time.perf_counter()
    hyperframes.render(project, raw, quality="looks", gpu=True, workers=4, timeout=max(3600, int(seconds * 30)))
    dt = time.perf_counter() - t0
    return {"seconds": seconds, "render_s": round(dt, 1), "factor": round(dt / seconds, 2), "at": datetime.now().isoformat(timespec="seconds")}


def main() -> int:
    plan_path = Path(sys.argv[1])
    plan = rl.load_plan(plan_path if plan_path.is_absolute() else Path.cwd() / plan_path)
    ids, name = sys.argv[2].split(","), sys.argv[3]
    render_only, join_only = "--render-only" in sys.argv, "--join" in sys.argv
    timed, order = timing(plan)
    _, offsets, _ = welt_scene.global_words(timed, order)
    root = STORAGE_DIR / "longform" / f"{plan['video_id']}-welt-probe"
    out = root / name
    out.mkdir(parents=True, exist_ok=True)
    projects = {cid: root / cid / "project" for cid in ids}
    for cid, p in projects.items():
        if not (p / "index.html").exists() or not (p / "cues.json").exists():
            print(f"{cid}: project missing, build it first with welt_probe.py")
            return 2
    rlog = out / "renders.json"
    renders = json.loads(rlog.read_text(encoding="utf-8")) if rlog.exists() else {}
    if not join_only:
        for cid in ids:                               # picture per chapter (the composition's own audio is dropped)
            renders[cid] = render_chapter(projects[cid], out / f"raw_{cid}.mp4", timed[cid]["total"])
            print(cid, renders[cid], flush=True)
            rlog.write_text(json.dumps(renders, indent=1), encoding="utf-8")
        if render_only:
            return 0
    raws = [out / f"raw_{cid}.mp4" for cid in ids]
    missing = [r.name for r in raws if not r.exists()]
    if missing:
        print("missing chapter renders:", missing)
        return 3
    report: dict = {"plan": plan_path.name, "chapters": ids, "renders": {c: renders.get(c) for c in ids}}
    lst = out / "concat.txt"
    lst.write_text("".join(f"file '{r.as_posix()}'\n" for r in raws), encoding="utf-8")
    picture = out / "picture.mp4"
    ffmpeg.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-an", "-c", "copy", str(picture)])
    mix = tonmix.mix_range(plan, timed, offsets, ids, projects, out / "ton", brand_dir=HERE.parent, final=(ids[-1] == order[-1]))
    report["mix"] = {k: mix[k] for k in ("seconds", "cues", "measured", "problems", "music", "licenses")}
    final = out / f"{name}.mp4"
    t0 = time.perf_counter()
    report["encode"] = ffmpeg.encode_nvenc(picture, final, audio=out / "ton" / "mix.wav", loudness_lufs=-16.0, loudnorm="linear",
                                           timeout=max(1800, int(mix["seconds"] * 4)))
    report["encode"]["seconds"] = round(time.perf_counter() - t0, 1)
    picture.unlink(missing_ok=True)
    # chapters and subtitles on the joined timeline
    base = offsets[ids[0]]
    marks, srt, n = [], [], 1
    for cid in ids:
        ch = next(c for c in plan["chapters"] if c["id"] == cid)
        t = offsets[cid] - base
        marks.append(f"{rl.yt_time(t)} {ch['title']}")
        for g in group_phrases(timed[cid]["words"], min_words=3, max_words=9):
            srt.append(f"{n}\n{rl.srt_time(t + g.start)} --> {rl.srt_time(t + g.end)}\n{g.text}\n")
            n += 1
        ffmpeg.extract_frame(final, out / f"still_{cid}.jpg", t + min(12.0, timed[cid]["total"] / 2))
    (out / "chapters.txt").write_text("\n".join(marks) + "\n", encoding="utf-8")
    (out / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    report["duration_s"] = round(ffmpeg.audio_duration(final), 2)
    manifest = {"video_id": plan["video_id"], "brand_id": "ai_security", "language": plan["lang"], "title": plan["title"], "mode": "welt",
                "duration_s": report["duration_s"], "chapters": ids,
                "tts": {"provider": "gemini", "per_chapter": {c: timed[c]["info"].get("provider") for c in ids},
                        "model": {c: timed[c]["info"].get("model") for c in ids}, "voice": "Charon"},
                "sound": {"setting": tonmix.SETTING, "music": mix["music"], "licenses": mix["licenses"]},
                "ai_disclosure": {"in_picture": "KI-GENERIERT · SYNTHETISCHE STIMME (oben rechts), Einstiegszeile, an jedem Einschub "
                                                "KI-GENERIERTE DARSTELLUNG · SYNTHETISCHE STIMME (unten rechts), gesprochener Hinweis im Schluss",
                                  "labels": {"is_ai_generated": True, "containsSyntheticMedia": True}},
                "inserts": "Higgsfield, Nachweis brands/ai_security/assets/higgsfield/LICENSE.md",
                "sources": plan["sources"], "created": datetime.now().isoformat(timespec="seconds")}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    report["output"] = str(final)
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print("done", final, report["duration_s"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
