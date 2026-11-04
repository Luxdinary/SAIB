"""Light palettes (Dewlane) and the file marker; dark brands must render exactly as before."""
from fn.render import templates, templates_file
from fn.render.templates import SceneCtx

DARK = {"accent": "#4f8cff", "text": "#e9eef8", "surface": "#121b2f", "muted": "#a1adc4", "bg": "#0b1120"}


def test_dark_palette_css_is_untouched():
    css = templates.scene_css(DARK, "Manrope", 800, "Manrope", "Plex", 290, 910, True)
    assert "rgba(0,0,0," in css and "mix-blend-mode:screen;" in css and "#3a4258" in css


def test_light_palette_recolours_shadows_and_drops_screen_blend():
    light = {**DARK, "scheme": "light", "shadow": "108, 75, 80", "toggle_off": "#d8cfcb"}
    css = templates.scene_css(light, "Manrope", 800, "Manrope", "Plex", 290, 910, True)
    assert "rgba(0,0,0," not in css and "rgba(108,75,80," in css
    assert "mix-blend-mode:screen;" not in css and "#d8cfcb" in css
    assert "rgba(0,0,0," not in templates_file.file_css(light, "Manrope", 800, "Plex", True)


def _ctx():
    return SceneCtx(sid="b2", start=5.0, duration=8.0, pal=DARK, display_font="M", body_font="M", mono_font="P", flat=True)


def test_file_marker_none_and_fact():
    d = {"file_label": "Pflege.pdf", "card": {"title": "T", "rows": [{"text": "x"}]}}
    default = templates_file.file_beside(_ctx(), d)
    assert "fcard-q" in default.html and any(".fcard-q" in line for line in default.tl)
    none = templates_file.file_beside(_ctx(), {**d, "file_marker": "none"})
    assert "fcard-q" not in none.html and not any(".fcard-q" in line for line in none.tl)
    fact = templates_file.file_beside(_ctx(), {**d, "file_marker": "fact"})
    assert "mk-fact" in fact.html and "Unsicher" not in fact.html.split("bcard")[0]
