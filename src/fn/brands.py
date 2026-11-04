"""Brand registry: config/brands.yaml plus the design-system files in brands/<id>/."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .config import BRANDS_DIR, brands_config, read_yaml


@dataclass
class Brand:
    id: str
    name: str
    niche: str
    style: str
    phase: int
    enabled: bool
    risk_default: str
    rules: list[str]
    palette: dict[str, str]
    languages: list[str]
    design: dict = field(default_factory=dict)        # brands/<id>/brand.yaml
    subtitle_style: dict = field(default_factory=dict)
    intro: dict = field(default_factory=dict)
    outro: dict = field(default_factory=dict)
    audio: dict = field(default_factory=dict)

    @property
    def dir(self) -> Path:
        return BRANDS_DIR / self.id

    @property
    def fonts(self) -> dict:
        return self.design.get("fonts", {})

    def cta(self, language: str) -> str:
        return self.outro.get("cta", {}).get(language, "")

    def ai_label(self, language: str) -> str:
        return self.design.get("ai_label", {}).get(language, "AI-generated")

    def voice(self, language: str) -> str:
        return self.audio.get("tts", {}).get("voices", {}).get(language, "Kore")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_brand(brand_id: str) -> Brand:
    cfg = brands_config()
    entry = next((b for b in cfg["brands"] if b["id"] == brand_id), None)
    if entry is None:
        raise KeyError(f"unknown brand_id {brand_id!r}")
    d = BRANDS_DIR / brand_id
    design = read_yaml(d / "brand.yaml") if (d / "brand.yaml").exists() else {}
    palette = dict(entry["palette"])
    palette.update(design.get("palette", {}))
    return Brand(
        id=entry["id"], name=entry["name"], niche=entry["niche"], style=entry["style"],
        phase=entry["phase"], enabled=bool(entry["enabled"]), risk_default=entry["risk_default"],
        rules=list(entry.get("rules", [])), palette=palette,
        languages=list(cfg["defaults"]["languages"]), design=design,
        subtitle_style=_load_json(d / "subtitle_style.json"),
        intro=_load_json(d / "intro_config.json"),
        outro=_load_json(d / "outro_config.json"),
        audio=read_yaml(d / "audio_style.yaml") if (d / "audio_style.yaml").exists() else {},
    )


def all_brand_ids() -> list[str]:
    return [b["id"] for b in brands_config()["brands"]]


def enabled_brand_ids() -> list[str]:
    return [b["id"] for b in brands_config()["brands"] if b.get("enabled")]
