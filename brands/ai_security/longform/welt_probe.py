"""Dry probe "welt im Composer": builds one chapter of a plan as a world chapter and takes stills (no video render,
no Gemini). Usage:

  set LONGFORM_NO_TTS=1
  .venv\\Scripts\\python.exe brands\\ai_security\\longform\\welt_probe.py plans\\01-ai-rules-start.de.json c1 2,8,20,40,70,95
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[2] / "src"))
os.environ.setdefault("LONGFORM_NO_TTS", "1")

from fn.config import STORAGE_DIR  # noqa: E402
from fn.costs import CostLogger  # noqa: E402
from fn.render import hyperframes  # noqa: E402
from longform import compose, cues, fmt as fmts, render_long as rl, tonmix, welt_scene  # noqa: E402


def probe(plan: dict, timed: dict, offsets: dict, words, total: float, cid: str, times: list[float], out: Path) -> Path:
    """Build, check and photograph one chapter; returns its project folder (with cues.json)."""
    tm = timed[cid]
    ch = next(c for c in plan["chapters"] if c["id"] == cid)
    seg = {"lang": plan["lang"], "title": f"Probe welt {cid}", "total": tm["total"], "scenes": [], "heads": [],
           "cards": [{"start": 0.0, "dur": tm["card"], "num": ch.get("num", ""), "title": ch.get("title", "")}] if tm["card"] else [],
           "voice": tm["wav"], "voice_start": tm["vstart"], "voice_seconds": tm["info"]["seconds"]}
    seg["welt"] = welt_scene.layer(plan, offsets[cid], tm["total"])
    seg["inserts"], ip = rl.resolve_inserts(ch, tm)
    print(f"== {cid}")
    for p_ in ip:
        print("  problem:", p_)
    compose.build(seg, fmts.get("16x9"), out / "project")
    welt_scene.copy_assets(out / "project", plan, words, total)
    chk = hyperframes.check(out / "project")
    print("offset", offsets[cid], "chapter", tm["total"], "video", total, "lint", chk.get("lint", {}).get("errorCount"),
          "layout", chk.get("layout", {}).get("errorCount"))
    for it in (chk.get("lint", {}).get("findings") or [])[:8]:
        print("  lint:", it.get("severity"), it.get("code"), (it.get("message") or "")[:140])
    cq = cues.write(out / "project", offsets[cid], tm["total"], seg)
    print("cues:", len(cq["cues"]), "missing anchors:", cq["check"]["missing_anchors"], "errors:", cq["check"]["errors"])
    shots = hyperframes.snapshot(out / "project", [t for t in times if t < tm["total"] - 0.2], out / "stills")
    print("stills:", *shots, sep=chr(10) + "  ")
    return out / "project"


def main() -> int:
    plan = rl.load_plan(HERE / sys.argv[1] if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1]))
    cid, times = sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
    vdir = STORAGE_DIR / "longform" / plan["video_id"] / "voice"
    timed, order = {}, []
    for i, ch in enumerate(plan["chapters"]):
        wav, info = rl.voice_for(ch, plan["lang"], vdir, os.environ.get("WELT_VOICE", "gemini"), CostLogger(), plan["video_id"])
        words = rl.words_for(ch, wav, info, plan["lang"], vdir)
        tm = rl.time_chapter(ch, words, info["seconds"], plan, first=(i == 0), last=(i == len(plan["chapters"]) - 1))
        tm.update({"wav": wav, "info": info, "index": i})
        timed[ch["id"]] = tm
        order.append(ch["id"])
    words, offsets, total = welt_scene.global_words(timed, order)
    ids = cid.split(",")
    root = STORAGE_DIR / "longform" / f"{plan['video_id']}-welt-probe"
    projects = {}
    for cid in ids:
        projects[cid] = probe(plan, timed, offsets, words, total, cid, times, root / cid)
    if "--mix" in sys.argv:
        rep = tonmix.mix_range(plan, timed, offsets, ids, projects, root / ("ton-" + "-".join(ids)),
                               brand_dir=HERE.parent, final=(ids[-1] == order[-1]))
        m = rep["measured"]
        print("mix:", rep["seconds"], "s, cues", rep["cues"], "| voice LUFS", m.get("voice_lufs"), "| bed LUFS", m.get("music_lufs"),
              "| bed under voice", m.get("music_below_voice_db"), "dB | sfx peak", m.get("sfx_peak_dbfs"), "| mix LUFS", m.get("mix_lufs"),
              "peak", m.get("mix_peak_dbfs"))
        for p_ in rep["problems"]:
            print("  mix problem:", p_)
    return 0


if __name__ == "__main__":
    sys.exit(main())
