"""Build a Scutoria direction plan ("Was tust du?" format) from a short YAML spec.

Usage: .venv\\Scripts\\python.exe brands\\ai_security\\build_plan.py brands\\ai_security\\specs\\<spec>.yaml [...]
Writes data/direction/<id>.<version>.json (default version F1; never overwrites the week-1 plans of the old format,
which live at data/direction/<id>.json) and prints validation problems and the estimated spoken length.

Spec keys (see specs/ for examples; format bible: OneDrive\\Business\\02 Marke\\Scutoria\\Format-Bibel.md):
  id, title, reihe, note, description, hashtags[], version (optional, default F1)
  sources: [{id, url, title, label, checked_at}]
  unverified: [text]
  hooks: five candidates {type, spoken, screen, src[]}, one per hook type; `pick` names the chosen type
  beats: [{f: function, t: scene type, s: spoken, d: data, src: [source ids]}]
Layout, assets and the companion text come from brand.yaml `format` and the defaults below.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import yaml  # noqa: E402

from fn.direction import hooks, story  # noqa: E402
from fn.render import brand_scenes  # noqa: E402
from fn.render.templates import SceneCtx  # noqa: E402

BRAND = "ai_security"
CHARS_PER_S = {"de": 15.0, "en": 15.0}       # Gemini Charon in the case format, measured on 20 renders (02.11.2026): DE 15.5, EN 15.3
TAIL = 2.4
BACKGROUND = {"sc_case": "bg_ui_desk.mp4", "sc_inspect": "bg_hook_dataroom.mp4", "sc_choice": "bg_compare_split.mp4",
              "sc_timeline": "bg_flow_lanes.mp4", "sc_step": "bg_takeaway_calm.mp4", "sc_close": "bg_outro_orbit.mp4"}
COMPANION = {
    "de": "Mehr Informationen: https://scutoria.com · Folge Scutoria für weitere Tipps zur IT- und KI-Sicherheit im Betrieb. Quellenbasiert. Keine Rechtsberatung.",
    "en": "More information: https://scutoria.com · Follow Scutoria for more tips on IT and AI security at work. Source-based. No legal advice.",
}
DEFAULT_SCORES = {"clarity": 4, "relevance": 4, "curiosity": 3, "truth": 5, "visual": 3}
PICK_SCORES = {"clarity": 5, "relevance": 5, "curiosity": 5, "truth": 5, "visual": 5}


def build(spec: dict) -> tuple[dict, list[str]]:
    brand = yaml.safe_load((ROOT / "brands" / BRAND / "brand.yaml").read_text(encoding="utf-8"))
    vid = spec["id"]
    lang = vid.rsplit("-", 1)[-1]
    layout = dict(brand["format"]["plan_layout"])
    layout.update({"caption_transform": "none", "tail_seconds": TAIL, "description": spec.get("description", ""),
                   "companion_text": COMPANION[lang], "hashtags": list(spec.get("hashtags", []))})
    pick = spec.get("pick", "demonstration")
    cands = []
    for i, h in enumerate(spec["hooks"], 1):
        chosen = h["type"] == pick
        cands.append({"id": f"H{i}", "type": h["type"], "spoken": h["spoken"], "on_screen": h["screen"],
                      "scores": dict(PICK_SCORES if chosen else DEFAULT_SCORES), "source_ids": list(h.get("src", [])),
                      "visual": h.get("visual", ""), "why": {"truth": h.get("why", "")}})
    hook_id = next(c["id"] for c in cands if c["type"] == pick)
    beats = [{"id": f"b{i}", "function": b["f"], "scene_type": b["t"], "spoken": b["s"].strip(), "data": b.get("d", {}),
              "source_ids": list(b.get("src", []))} for i, b in enumerate(spec["beats"], 1)]
    used = sorted({b["scene_type"] for b in beats})
    plan = {
        "video_id": vid, "brand_id": BRAND, "language": lang, "title": spec["title"],
        "notes": f"Format \"Was tust du?\" (Format-Bibel 1.0), Reihe \"{spec.get('reihe', '')}\". {spec.get('note', '')}".strip(),
        "layout": layout,
        "assets": {"background": {t: BACKGROUND[t] for t in used if t in BACKGROUND}, "hero": {}, "scrim": 0.62,
                   "note": "Higgsfield-Clips aus brands/ai_security/assets/higgsfield (Lizenz in LICENSE.md), je Szenentyp ein Clip."},
        "sources": spec.get("sources", []), "unverified": spec.get("unverified", []),
        "hook_candidates": cands, "hook": {"id": hook_id, "note": "Fall-Einstieg des Formats; Wahrheit mindestens 4."},
        "beats": beats,
    }
    problems = story.validate(story.from_dict(plan))
    hc = [hooks.from_dict(c) for c in cands]
    problems += hooks.validate_set(hc) + [f"{c.id}: {p}" for c in hc for p in c.problems()]
    if (w := hooks.winner(hc)) is None or w.id != hook_id:
        problems.append(f"chosen hook {hook_id} is not the winner")
    for b in beats:
        problems += [f"{b['id']}: {p}" for p in brand_scenes.text_limits(BRAND, b["scene_type"], b["data"])]
        # nested limits (options, rows, items ...) are checked inside the templates; word anchors need the real voice
        tpl = brand_scenes.template_for(BRAND, b["scene_type"])
        ctx = SceneCtx(sid="x", start=0.0, duration=12.0, pal={}, display_font="", body_font="", mono_font="", lang=lang)
        problems += [f"{b['id']}: {p}" for p in tpl(ctx, b["data"]).problems if "word anchor" not in p]
    # format rules from the review of 03.11.2026: exactly one step (numbered steps only as one emergency block of
    # at most two, lists inside the one step carry marks), no "Merk dir" (Whisper hears "Merkt ihr"), no "Berlin police" in EN
    for b in beats:
        numbered = [s for s in b["data"].get("steps", []) if not s.get("mark")]
        if numbered and (b["data"].get("mode") != "fallback" or len(numbered) > 2):
            problems.append(f"{b['id']}: numbered steps outside one emergency block (max 2); use marks for list content")
    if sum(1 for b in beats if b["data"].get("steps") and not all(s.get("mark") for s in b["data"]["steps"])) > 1:
        problems.append("more than one block of numbered steps")
    spoken = " ".join(b["spoken"] for b in beats)
    if "Merk dir" in spoken:
        problems.append("'Merk dir' in the spoken text (use 'Entscheide dich jetzt.')")
    if lang == "en" and "Berlin police" in spoken:
        problems.append("'Berlin police' in the EN text (say 'German police')")
    return plan, problems


def main(argv: list[str]) -> int:
    bad = 0
    for arg in argv:
        spec = yaml.safe_load(Path(arg).read_text(encoding="utf-8"))
        plan, problems = build(spec)
        lang = plan["language"]
        chars = len(" ".join(b["spoken"] for b in plan["beats"]))
        est = chars / CHARS_PER_S[lang] + TAIL
        if not 70 <= est <= 80:
            problems.append(f"estimated length {est:.1f} s (aim 72-78 s, allowed 70-80)")
        out = ROOT / "data" / "direction" / f"{plan['video_id']}.{spec.get('version', 'F1')}.json"
        out.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{out.name}: {chars} chars, ~{est:.0f} s" + ("" if not problems else "  PROBLEMS: " + "; ".join(problems)))
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
