from pathlib import Path

from fn.brands import all_brand_ids, load_brand
from fn.disk import check_free_space
from fn.render.compose import Composition, Scene, Word, build_project, fit_font_size, group_words


def test_all_nine_brands_have_design_files():
    ids = all_brand_ids()
    assert len(ids) == 9
    for bid in ids:
        b = load_brand(bid)
        assert b.name and b.palette["accent"].startswith("#")
        for f in ("brand.yaml", "visual_style.md", "script_prompt.md", "image_prompt.md", "subtitle_style.json",
                  "intro_config.json", "outro_config.json", "audio_style.yaml"):
            assert (b.dir / f).exists(), f"{bid}/{f}"
        assert b.cta("de") and b.cta("en")
        assert b.ai_label("de") == "KI-generiert"


def test_group_words_breaks_at_sentence_and_pause():
    words = [Word("Hallo", 0.0, 0.3), Word("Welt.", 0.35, 0.6), Word("Zweiter", 1.0, 1.3), Word("Satz", 1.35, 1.6),
             Word("hier", 1.65, 1.9), Word("weiter", 1.95, 2.2)]
    groups = group_words(words, 3)
    assert [g.text for g in groups] == ["Hallo Welt.", "Zweiter Satz hier", "weiter"]
    for a, b in zip(groups, groups[1:]):
        assert a.end <= b.start


def test_fit_font_size_shrinks_long_text():
    assert fit_font_size("kurz", 64, 42, 900, uppercase=False) == 64
    assert fit_font_size("x" * 80, 64, 42, 900, uppercase=True) < 64


def test_build_project_writes_valid_html(tmp_path):
    b = load_brand("military_history")
    scenes = [Scene("hook", 2.0, 3.0, "Hook", kind="hook"), Scene("s2", 5.0, 3.0, "Fakt", body="Text", number="42", source_label="[S1] x")]
    caps = group_words([Word("Ein", 2.3, 2.5), Word("Test.", 2.6, 2.9)], 2)
    comp = Composition(brand=b, language="de", duration=10.0, scenes=scenes, captions=caps)
    index = build_project(comp, tmp_path / "proj")
    html = index.read_text(encoding="utf-8")
    assert 'data-composition-id="main"' in html and 'data-duration="10.000"' in html
    assert "art50" in html                       # disclosure for the military brand
    assert "KI-generiert" in html
    assert (tmp_path / "proj" / "assets" / "fonts").exists()
    assert "window.__timelines[\"main\"]" in html


def test_free_space_guard():
    s = check_free_space(Path("C:/"), minimum_gb=0.001)
    assert s.ok and "ok" in s.message
    s2 = check_free_space(Path("C:/"), minimum_gb=10_000_000)
    assert not s2.ok and "WARNING" in s2.message
