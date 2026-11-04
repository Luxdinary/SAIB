"""Explainer layer: anchors, default marker, source label, problems."""
from types import SimpleNamespace

import pytest

from fn.direction import story
from fn.render import explainer


def _w(text, start):
    return SimpleNamespace(text=text, start=start, end=start + 0.3)


def _plan(overlay=None, layout=None):
    b1 = story.Beat("b1", "hook", "cinematic_hook", "Hallo Welt", start=0.0, duration=3.0)
    b2 = story.Beat("b2", "problem", "comparison", "Der Grund ist einfach", source_ids=["S1"], start=3.0, duration=4.0,
                    overlay=overlay or {})
    return story.DirectionPlan("v", "demo", "de", "t", [b1, b2], layout=layout or {},
                               sources=[{"id": "S1", "title": "NASA Glenn Research Center: Four Stroke Engine", "checked_at": "2026-10-30"}])


def _brand(cfg):
    return SimpleNamespace(design={"explainer": cfg})


CAPS = [SimpleNamespace(words=[_w("Hallo", 0.2), _w("Welt", 0.6), _w("Der", 3.1), _w("Grund", 3.4), _w("ist", 3.8), _w("einfach", 4.1)])]
PAL = {"bg": "#000", "text": "#fff", "surface": "#111", "muted": "#999", "accent": "#f0f"}


def _build(plan, cfg):
    return explainer.build(plan, _brand(cfg), CAPS, total=9.0, outro_start=7.0, pal=PAL, display="D", display_w=800,
                           mono="M", zone_top=290, lang="de")


def test_enabled_by_brand_or_plan():
    assert explainer.enabled(_brand({"enabled": True}), _plan())
    assert not explainer.enabled(_brand({}), _plan())
    assert not explainer.enabled(_brand({"enabled": True}), _plan(layout={"explainer": False}))


def test_default_marker_and_source_label():
    out = _build(_plan(overlay={"title": "Vier Hübe", "head_at": "w:Grund", "transition": {"type": "iris"}}), {"opening": {"de": "Synthetische Stimme"}})
    joined = "".join(out.html)
    assert "Quelle: NASA Glenn Research Center · abgerufen 30.10.2026" in joined
    assert "Fakt" in joined and "2 · DAS PROBLEM" in joined and "SYNTHETISCHE STIMME" in joined
    assert 'data-start="3.400"' in joined            # head anchored to the word "Grund"
    assert out.transitions[1]["type"] == "iris" and not out.problems


def test_missing_anchor_and_long_title_are_reported():
    with pytest.raises(ValueError):
        _build(_plan(overlay={"head_at": "w:Nirgends"}), {})
    out = _build(_plan(overlay={"title": "x" * 40, "marker": "fakt", "source": False}), {})
    assert any("head title" in p for p in out.problems)
