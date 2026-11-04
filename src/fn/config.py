"""Paths, environment and YAML configuration loading.

Never prints or logs secret values. Secrets come only from .env (see .env.example).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(os.environ.get("FN_ROOT", Path(__file__).resolve().parents[2]))
CONFIG_DIR = ROOT / "config"
BRANDS_DIR = ROOT / "brands"
PROMPTS_DIR = ROOT / "prompts"
DATA_DIR = ROOT / "data"
STORAGE_DIR = ROOT / "storage"
LOGS_DIR = ROOT / "logs"
ASSETS_DIR = ROOT / "assets"
TEMPLATES_DIR = ROOT / "templates"

QUEUE_DIRS = ("drafts", "approved", "published", "failed")


def load_dotenv(path: Path | None = None) -> dict[str, str]:
    """Load KEY=VALUE pairs from .env into os.environ (without overriding existing values)."""
    path = path or ROOT / ".env"
    loaded: dict[str, str] = {}
    if not path.exists():
        return loaded
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
        loaded[key] = "set" if value else ""
    return loaded


def env(key: str, default: str | None = None) -> str | None:
    load_dotenv()
    return os.environ.get(key, default)


def has_secret(key: str) -> bool:
    value = env(key)
    return bool(value and value.strip())


def read_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=None)
def brands_config() -> dict:
    return read_yaml(CONFIG_DIR / "brands.yaml")


@lru_cache(maxsize=None)
def platforms_config() -> dict:
    return read_yaml(CONFIG_DIR / "platforms.yaml")


@lru_cache(maxsize=None)
def policies_config() -> dict:
    return read_yaml(CONFIG_DIR / "policies.yaml")


@lru_cache(maxsize=None)
def voices_config() -> dict:
    return read_yaml(CONFIG_DIR / "voices.yaml")


@dataclass(frozen=True)
class VideoSpec:
    width: int = 1080
    height: int = 1920
    fps: int = 30
    min_seconds: float = 65.0
    max_seconds: float = 90.0
    hard_min_seconds: float = 61.0

    @classmethod
    def from_config(cls) -> "VideoSpec":
        v = brands_config()["defaults"]["video"]
        return cls(width=v["width"], height=v["height"], fps=30,
                   min_seconds=v["min_seconds"], max_seconds=v["max_seconds"],
                   hard_min_seconds=v["hard_min_seconds"])


def mirror_dir() -> Path:
    return Path(env("FN_STORAGE_MIRROR", r"C:\Users\Stefa\OneDrive\Business\05 Produktion"))


# Folder name per brand in OneDrive (Stefan, 02.11.2026: Business folder sorted by brand). brainrot is Tintora since
# the rebrand of 02.11.2026; the brand id stays until Stefan approves renaming the code.
BRAND_FOLDERS = {"ai_security": "Scutoria", "claude_workflows": "Promptwerk", "engines": "Revlore",
                 "megaconstruction": "Gigastruct", "menswear": "Suitwerk", "motivation": "Gritwerk",
                 "military_history": "Frontlore", "beauty": "Dewlane", "brainrot": "Tintora"}


def production_folder(brand_id: str, date: str, short: str) -> Path:
    """05 Produktion\\<Marke>\\<JJJJ-MM>\\<JJJJ-MM-TT Kurztitel> - the one place every exporter puts a video folder."""
    return mirror_dir() / BRAND_FOLDERS.get(brand_id, brand_id) / date[:7] / f"{date} {short}"


def min_free_gb() -> float:
    return float(env("FN_MIN_FREE_GB", "30"))


def ensure_dirs() -> None:
    for d in (DATA_DIR, DATA_DIR / "calendars", DATA_DIR / "scripts", DATA_DIR / "manifests",
              DATA_DIR / "costs", STORAGE_DIR, LOGS_DIR):
        d.mkdir(parents=True, exist_ok=True)
    for q in QUEUE_DIRS:
        (STORAGE_DIR / q).mkdir(parents=True, exist_ok=True)
