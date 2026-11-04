"""Brand-specific scene types from brands/<id>/scenes.py (fn.render.brand_scenes)."""
from fn.direction import story
from fn.render import brand_scenes, templates

SCENES_PY = '''
from fn.render.templates import SceneOut

def demo_cutaway(c, d):
    return SceneOut(html="<div>cut</div>", events=[c.start, c.start + 1.0])

def demo_hook(c, d):
    return SceneOut(html="<div>" + " ".join(w.text for w in c.words) + "</div>", events=[c.start])

TEMPLATES = {"demo_cutaway": demo_cutaway, "demo_hook": demo_hook}
LIMITS = {"demo_cutaway": {"headline": 10}}
HOOK_SCENE_TYPES = ["cinematic_hook", "demo_hook"]

def CSS(pal, *rest):
    return ".demo{color:" + pal["accent"] + ";}"
'''


def _setup(tmp_path, monkeypatch, content=SCENES_PY):
    (tmp_path / "demo").mkdir()
    (tmp_path / "demo" / "scenes.py").write_text(content, encoding="utf-8")
    monkeypatch.setattr(brand_scenes, "BRANDS_DIR", tmp_path)
    brand_scenes._cache.clear()


def test_brand_types_are_per_brand(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert "demo_cutaway" in brand_scenes.scene_types("demo")
    assert "demo_cutaway" not in brand_scenes.scene_types("other")
    assert brand_scenes.template_for("demo", "data_flow") is templates.TEMPLATES["data_flow"]
    assert brand_scenes.template_for("other", "demo_cutaway") is None
    assert brand_scenes.css_for("demo", {"accent": "#123456"}) == ".demo{color:#123456;}"
    assert brand_scenes.text_limits("demo", "demo_cutaway", {"headline": "x" * 11})
    brand_scenes._cache.clear()


def test_story_accepts_brand_hook_type(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    beats = [story.Beat("b1", "hook", "demo_hook", "Frage?"),
             story.Beat("b2", "problem", "demo_cutaway", "Satz.", source_ids=["S1"]),
             story.Beat("b3", "close", "key_takeaway", "Ende.")]
    plan = story.DirectionPlan("v", "demo", "de", "t", beats,
                               sources=[{"id": "S1", "url": "https://example.org", "checked_at": "2026-10-30"}])
    assert story.validate(plan) == []
    plan.brand_id = "other"
    assert any("hook scene types" in p for p in story.validate(plan))
    brand_scenes._cache.clear()


def test_shared_name_override_is_per_brand(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, "def own(c, d):\n    return None\nTEMPLATES = {'data_flow': own}\n"
                                  "def scene_css(pal, display):\n    return display\n")
    own = brand_scenes.template_for("demo", "data_flow")
    assert own is not templates.TEMPLATES["data_flow"] and own.__name__ == "own"
    assert brand_scenes.template_for("other", "data_flow") is templates.TEMPLATES["data_flow"]
    assert brand_scenes.css_for("demo", {}, "Manrope", 800, "Inter", "Mono", 290, 910, True) == "Manrope"
    brand_scenes._cache.clear()
