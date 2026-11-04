"""Configuration of the daily runner: config/daily.yaml (defaults merged with the brand block)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from ..config import CONFIG_DIR, DATA_DIR, ROOT, mirror_dir, read_yaml

BUSINESS_DIR = mirror_dir().parent          # OneDrive\Business (mirror_dir is 05 Produktion)
DAILY_DIR = DATA_DIR / "daily"
RUNS_DIR = DAILY_DIR / "runs"
STATE_FILE = DAILY_DIR / "state.json"
LOCK_FILE = DAILY_DIR / "runner.lock"
REDAKTIONSPLAN = BUSINESS_DIR / "04 Redaktionsplan" / "Redaktionsplan.csv"


@lru_cache(maxsize=None)
def daily_config() -> dict:
    return read_yaml(CONFIG_DIR / "daily.yaml")


@dataclass
class BrandSettings:
    brand_id: str
    cfg: dict                     # defaults merged with the brand block (brand wins)

    def get(self, key: str, default=None):
        return self.cfg.get(key, default)

    @property
    def name(self) -> str:
        return self.cfg.get("name", self.brand_id)

    @property
    def enabled(self) -> bool:
        return bool(self.cfg.get("enabled", False))

    @property
    def reason(self) -> str:
        return str(self.cfg.get("reason", ""))

    def business_path(self, key: str) -> Path | None:
        v = self.cfg.get(key)
        return (BUSINESS_DIR / v) if v else None

    def repo_path(self, value: str) -> Path:
        return ROOT / value

    def example_plan(self, lang: str) -> Path | None:
        v = (self.cfg.get("example_plan") or {}).get(lang)
        return (ROOT / v) if v else None

    def extra_example_plan(self, lang: str) -> Path | None:
        v = (self.cfg.get("extra_example_plan") or {}).get(lang)
        return (ROOT / v) if v else None

    @property
    def scene_types(self) -> list[str]:
        return list(self.cfg.get("scene_types") or [])

    @property
    def hook_types(self) -> list[str]:
        return list(self.cfg.get("hook_types") or [])

    @property
    def material_folders(self) -> list[Path]:
        from ..config import BRANDS_DIR
        return [BRANDS_DIR / self.brand_id / f for f in (self.cfg.get("material_folders") or [])]

    @property
    def llm(self) -> dict:
        return dict(self.cfg.get("llm") or {})

    @property
    def topic_source(self) -> dict:
        return dict(self.cfg.get("topic_source") or {})

    @property
    def aufbau(self) -> dict:
        return dict(self.cfg.get("aufbau") or {"available": [], "default": None})

    def chars_per_second(self, lang: str) -> float:
        return float((self.cfg.get("chars_per_second") or {}).get(lang, 15.0))

    def char_window(self, lang: str) -> tuple[int, int, int]:
        """(min, target, max) characters of spoken text for the target voice length."""
        target = float(self.cfg.get("target_voice_seconds", 76)) * self.chars_per_second(lang)
        tol = float(self.cfg.get("length_tolerance", 0.07))
        return int(target * (1 - tol)), int(target), int(target * (1 + tol))

    @property
    def render_script(self) -> Path:
        return ROOT / self.cfg.get("render_script", "scripts/render_direction.py")

    @property
    def render_args(self) -> list[str]:
        return list(self.cfg.get("render_args") or [])


AUFBAUTEN_OK_DIR = DAILY_DIR / "aufbauten_ok"        # last valid copy of every brand's aufbauten.yaml (a brand session may be mid-edit)
AUFBAUTEN_WARNINGS: list[str] = []                    # filled when a file was invalid and the last valid copy was used; read by planner and runner
_REMEMBERED: dict[str, tuple[float, int]] = {}


def _remember_valid(brand_id: str, p: Path) -> None:
    """Keep a copy of the file as it was when it parsed, so a half-written version later can be replaced by it. Never raises."""
    try:
        st = p.stat()
        if _REMEMBERED.get(brand_id) == (st.st_mtime, st.st_size):
            return
        AUFBAUTEN_OK_DIR.mkdir(parents=True, exist_ok=True)
        dst = AUFBAUTEN_OK_DIR / f"{brand_id}.yaml"
        data = p.read_bytes()
        if not dst.exists() or dst.read_bytes() != data:
            dst.write_bytes(data)
        _REMEMBERED[brand_id] = (st.st_mtime, st.st_size)
    except OSError:
        pass


def _parse_aufbauten(p: Path) -> list[dict]:
    data = read_yaml(p) or {}
    items = data.get("aufbauten") if isinstance(data, dict) else data
    out = []
    for it in items or []:
        if not isinstance(it, dict) or not it.get("kuerzel"):
            continue
        out.append({"kuerzel": str(it["kuerzel"]).strip().upper(), "name": str(it.get("name", "")), "gebaut": bool(it.get("gebaut", False)),
                    "szenentypen": [str(x) for x in (it.get("szenentypen") or [])], "beispielplan": it.get("beispielplan"),
                    "beispielplan_en": it.get("beispielplan_en"), "themen": list(it.get("themen") or []),
                    "themen_declared": "themen" in it, "hinweis": str(it.get("hinweis", ""))})
    return out


def load_aufbauten(brand_id: str) -> list[dict]:
    """brands/<id>/aufbauten.yaml (maintained by the brand sessions, read at run time):
    aufbauten: [{kuerzel: A, name: ..., gebaut: true, szenentypen: [...], beispielplan: data/direction/<id>.json,
                 beispielplan_en: ..., themen: [{nr: 103, quellen: [{url, titel, checked_at}]} | 103, ...], hinweis: ...}]
    A file that does not parse (a brand session is writing it) is replaced by the last valid copy and reported in AUFBAUTEN_WARNINGS."""
    from ..config import BRANDS_DIR
    p = BRANDS_DIR / brand_id / "aufbauten.yaml"
    if not p.exists():
        return []
    try:
        out = _parse_aufbauten(p)
    except Exception as exc:  # noqa: BLE001 - invalid YAML or an unexpected structure
        ok = AUFBAUTEN_OK_DIR / f"{brand_id}.yaml"
        reason = " ".join(str(exc).split())[:160]
        if ok.exists():
            msg = (f"{brand_id}: aufbauten.yaml ist ungültig ({reason}); geplant und produziert wird mit dem letzten gültigen Stand "
                   f"vom {datetime.fromtimestamp(ok.stat().st_mtime):%d.%m.%Y %H:%M}")
            try:
                out = _parse_aufbauten(ok)
            except Exception:  # noqa: BLE001
                out = []
        else:
            msg = f"{brand_id}: aufbauten.yaml ist ungültig ({reason}) und es gibt keinen letzten gültigen Stand; Bildaufbauten laut config/daily.yaml"
            out = []
        if msg not in AUFBAUTEN_WARNINGS:
            AUFBAUTEN_WARNINGS.append(msg)
        return out
    _remember_valid(brand_id, p)
    return out


def brand_settings(brand_id: str) -> BrandSettings:
    cfg = daily_config()
    defaults = dict(cfg.get("defaults") or {})
    block = dict((cfg.get("brands") or {}).get(brand_id) or {})
    merged = {**defaults, **block}
    if "llm" in defaults or "llm" in block:
        merged["llm"] = {**(defaults.get("llm") or {}), **(block.get("llm") or {})}
    return BrandSettings(brand_id, merged)


def configured_brands(enabled_only: bool = True) -> list[str]:
    out = []
    for bid, block in (daily_config().get("brands") or {}).items():
        if enabled_only and not (block or {}).get("enabled", False):
            continue
        out.append(bid)
    return out
