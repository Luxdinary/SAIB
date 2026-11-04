from pathlib import Path

from fn.brands import load_brand
from fn.direction import story
from fn.render import assets

ROOT = Path(__file__).resolve().parents[1]


def test_assets_missing_files_are_problems():
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    aset = assets.resolve_assets(plan, load_brand("ai_security"), {"background": {"data_flow": "nope.mp4"}, "hero": {"b1": "nope2.mp4"}})
    assert len(aset.problems) == 2 and not aset.enabled


def test_assets_resolve_with_licence(tmp_path, monkeypatch):
    plan = story.load_plan(ROOT / "data" / "direction" / "ai_security-20261105-1-de.json")
    brand = load_brand("ai_security")
    folder = tmp_path / "assets" / "higgsfield"
    folder.mkdir(parents=True)
    (folder / "bg.mp4").write_bytes(b"0")
    (folder / "hero.mp4").write_bytes(b"0")
    (folder / "LICENSE.md").write_text("bg.mp4: Higgsfield, generated 2026-10-30\n", encoding="utf-8")
    monkeypatch.setattr(type(brand), "dir", property(lambda self: tmp_path))
    aset = assets.resolve_assets(plan, brand, {"background": {"cinematic_hook": "bg.mp4"}, "hero": {"b1": "hero.mp4"}})
    assert aset.enabled and aset.background_for("cinematic_hook").name == "bg.mp4"
    assert aset.hero_for("b1") is not None
    assert any("without licence" in p for p in aset.problems)          # hero.mp4 has no licence line
    a, lic = aset.manifest_entries()
    assert len(a) == 2 and len(lic) == 1
    rel = assets.copy_assets(aset, tmp_path / "proj")
    assert rel["bg.mp4"].startswith("assets/clips/")
