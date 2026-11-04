import json
from pathlib import Path

from fn.direction import hooks, story
from fn.direction.checks import check_direction
from fn.compliance import Report
from fn.render import templates
from fn.render.compose import CaptionGroup, Word
from fn.render.director import assign_timing, build_direction_project

ROOT = Path(__file__).resolve().parents[1]


def _cand(i, typ, truth=5, **over):
    s = {"clarity": 4, "relevance": 4, "curiosity": 4, "truth": truth, "visual": 4}
    s.update(over)
    return hooks.HookCandidate(id=f"H{i}", type=typ, spoken="Frage?", on_screen="Frage?", scores=s, source_ids=["S1"])


def test_hook_truth_gate_and_ranking():
    cands = [_cand(1, "question", truth=5, curiosity=3), _cand(2, "misconception", truth=3, curiosity=5, clarity=5),
             _cand(3, "surprising_fact"), _cand(4, "concrete_risk"), _cand(5, "demonstration", visual=5)]
    assert hooks.validate_set(cands) == []
    ranked = hooks.rank(cands)
    assert ranked[-1].id == "H2" and not ranked[-1].eligible        # dramatic but not defensible loses
    assert hooks.winner(cands).id == "H5"
    assert hooks.validate_set(cands[:4])                                # a type is missing


def test_plan_file_validates_and_scores():
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    assert story.validate(plan) == []
    assert len({b.scene_type for b in plan.beats}) >= 3
    cands = [hooks.from_dict(c) for c in plan.hook_candidates]
    assert hooks.validate_set(cands) == []
    assert all(c.eligible for c in cands)


def test_story_order_and_variety_rules():
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    plan.beats[1], plan.beats[2] = plan.beats[2], plan.beats[1]
    assert any("story order" in p for p in story.validate(plan))
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    for b in plan.beats[1:]:
        b.scene_type = "cinematic_hook"
    assert any("representation forms" in p for p in story.validate(plan))
    plan.beats[2].spoken = "UNVERIFIED: something"
    assert any("UNVERIFIED" in p for p in story.validate(plan))


def test_text_limits():
    assert templates.text_limits("cinematic_hook", {"question": "x" * 65})
    assert not templates.text_limits("cinematic_hook", {"question": "x" * 64})
    assert templates.text_limits("comparison", {"left": {"rows": [{"text": "y" * 45}]}})


def test_director_builds_all_five_templates(tmp_path):
    from fn.brands import load_brand
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    n = len(plan.spoken_text.split())
    words = [Word(w, round(1.0 + i * 0.4, 3), round(1.3 + i * 0.4, 3)) for i, w in enumerate(plan.spoken_text.split())]
    total = words[-1].end + 5.0
    assign_timing(plan, words, first_start=0.0, outro_start=total - 4.0)
    assert all(b.start is not None and b.duration > 0 for b in plan.beats)
    assert abs(sum(b.duration for b in plan.beats) - (total - 4.0)) < 0.01
    caps = [CaptionGroup(start=w.start, end=w.end, words=[w], highlight=0) for w in words[:5]]
    build = build_direction_project(plan, load_brand("ai_security"), caps, total=total, project_dir=tmp_path / "p", outro=True)
    html = build.index.read_text(encoding="utf-8")
    for t in ("cinematic_hook", "ui_demo", "data_flow", "comparison", "key_takeaway"):
        assert f'class="clip scene {t}"' in html
    assert 'data-composition-id="main"' in html and "window.__timelines" in html
    assert 'tl.fromTo("#b1"' not in html and 'tl.to("#b1"' not in html     # never tween the .clip itself
    assert len(build.events) > len(plan.beats)
    assert n > 150


def test_direction_checks():
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    t = 0.0
    for b in plan.beats:
        b.start, b.duration = t, 10.0
        t += 10.0
    rep = Report("x")
    check_direction(rep, plan, events=[2, 5, 12, 15, 22, 25, 32, 35, 42, 45, 52, 55, 62, 65], total=70.0,
                    template_problems=["b4: ui_demo: schematic UI"], caption_font_px=58)
    ids = {f.id: f for f in rep.findings}
    assert ids["scene_variety"].ok and ids["visual_cuts_static"].ok and ids["readability_text_limits"].ok
    assert not ids["schematic_ui"].ok and rep.needs_review and rep.passed
    rep2 = Report("y")
    check_direction(rep2, plan, events=[], total=70.0, template_problems=["b1: cinematic_hook.question: 70 chars > 64"])
    ids2 = {f.id: f for f in rep2.findings}
    assert not ids2["readability_text_limits"].ok and not rep2.passed
    assert not ids2["visual_cuts_static"].ok or ids2["visual_cuts_static"].detail
