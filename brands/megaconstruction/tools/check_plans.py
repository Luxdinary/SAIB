"""Validate built plans: story, hooks, scene field limits (renderer problems), word counts."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fn.direction import story, hooks
import scenes
for tid in sys.argv[1:]:
    p = story.load_plan(ROOT / "data" / "direction" / f"{tid}.json")
    probs = story.validate(p) + hooks.validate_set([hooks.from_dict(c) for c in p.hook_candidates])
    h1 = hooks.from_dict(p.hook_candidates[0]); probs += h1.problems()
    for b in p.beats:
        lim = scenes._FIELD_LIMITS.get(b.scene_type, {})
        d = b.data
        for k in ("kicker", "headline", "question", "statement", "note"):
            if k in d and k in lim and len(str(d[k])) > lim[k]: probs.append(f"{b.id} {k} {len(d[k])}>{lim[k]}")
        for it in d.get("items", []):
            if len(str(it.get("value", ""))) > lim.get("value", 99): probs.append(f"{b.id} value {it['value']}")
            if len(it.get("label", "")) > lim.get("item_label", 99): probs.append(f"{b.id} label {it['label']}")
        for s in d.get("steps", []):
            if len(s.get("label", "")) > 30 or len(s.get("sub", "")) > 40: probs.append(f"{b.id} step {s}")
        for c in d.get("callouts", []):
            if len(c["text"]) > 26: probs.append(f"{b.id} callout {c['text']}")
        for c in d.get("dims", []):
            if len(c["text"]) > 12: probs.append(f"{b.id} dim {c['text']}")
        for side in ("a", "b"):
            if side in d and len(d[side]["label"]) > 26: probs.append(f"{b.id} label {d[side]['label']}")
        if "badge" in d and len(d["badge"]["text"]) > 30: probs.append(f"{b.id} badge")
        if "chip" in d and len(d["chip"]["text"]) > 30: probs.append(f"{b.id} chip")
    words = sum(len(b.spoken.split()) for b in p.beats)
    print(f"{tid}: {words} words {'OK' if not probs else probs}")
