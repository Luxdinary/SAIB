"""Everything the model needs to write a plan for one brand: brand files, scene docs, material, calendar sources."""
from __future__ import annotations

import difflib
import inspect
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from ..brands import Brand, load_brand
from ..config import BRANDS_DIR, DATA_DIR, brands_config
from ..render import brand_scenes
from .settings import BrandSettings
from .topics import Konzeptplan, Topic, _norm

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXT = {".mp4", ".webm", ".mov"}


@dataclass
class MaterialItem:
    folder: str          # folder relative to brands/<id> (e.g. assets/higgsfield/library)
    file: str
    kind: str            # image | video
    licensed: bool
    use: str = ""
    purpose: str = ""
    duration_s: float | None = None

    @property
    def path_in_assets(self) -> str:
        """Path relative to brands/<id>/assets/higgsfield (how most plans reference files)."""
        rel = self.folder.replace("\\", "/")
        prefix = rel.split("assets/higgsfield/", 1)[1] if "assets/higgsfield/" in rel else ""
        return f"{prefix}/{self.file}" if prefix else self.file


@dataclass
class SourceRef:
    id: str
    url: str
    title: str
    checked_at: str
    reachable: bool | None = None
    note: str = ""


@dataclass
class BrandContext:
    brand: Brand
    settings: BrandSettings
    konzeptplan: Konzeptplan
    format_bible: str
    testvideo_concept: str
    example_de: dict
    example_en: dict | None
    extra_example_de: dict | None
    extra_example_en: dict | None
    scene_docs: str
    limits: dict
    material: list[MaterialItem]
    brand_rules: list[str]
    recordings: list[str] = field(default_factory=list)
    format_essentials: str = ""
    aufbauten: list[dict] = field(default_factory=list)

    def scene_docs_for(self, scene_types: list[str]) -> str:
        docs, _ = scene_docs(self.brand.id, scene_types)
        return docs


def _license_names(folder: Path) -> set[str]:
    f = folder / "LICENSE.md"
    out: set[str] = set()
    if not f.exists():
        return out
    for line in f.read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            name = line.split(":", 1)[0].strip().strip("`*- ")
            if "." in name and " " not in name:
                out.add(name)
    return out


def material_items(settings: BrandSettings) -> list[MaterialItem]:
    items: list[MaterialItem] = []
    brand_dir = BRANDS_DIR / settings.brand_id
    for folder in settings.material_folders:
        if not folder.exists():
            continue
        rel = str(folder.relative_to(brand_dir)).replace("\\", "/")
        licensed = _license_names(folder)
        manifest = {}
        mf = folder / "manifest.json"
        if mf.exists():
            try:
                for it in json.loads(mf.read_text(encoding="utf-8")).get("items", []):
                    manifest[it.get("file")] = it
            except (json.JSONDecodeError, AttributeError):
                pass
        for p in sorted(folder.iterdir()):
            if not p.is_file() or p.suffix.lower() not in IMAGE_EXT | VIDEO_EXT:
                continue
            if p.name.endswith(".start.png") or p.name.startswith("_raw_") or p.name.startswith("Kontaktbogen"):
                continue
            m = manifest.get(p.name, {})
            items.append(MaterialItem(folder=rel, file=p.name, kind="video" if p.suffix.lower() in VIDEO_EXT else "image",
                                      licensed=p.name in licensed, use=str(m.get("use", "")), purpose=str(m.get("purpose", "")),
                                      duration_s=m.get("duration_s")))
    return items


def scene_docs(brand_id: str, scene_types: list[str]) -> tuple[str, dict]:
    """Docstrings (module table + function doc) of the allowed scene types, and their text limits."""
    bs = brand_scenes.load(brand_id)
    parts: list[str] = []
    seen_modules: set[str] = set()
    for t in scene_types:
        fn = bs.templates.get(t)
        if fn is None:
            parts.append(f"### {t}\n(nicht in brands/{brand_id} gefunden)")
            continue
        mod_doc = (getattr(fn, "__globals__", {}) or {}).get("__doc__") or ""
        mod_name = getattr(fn, "__module__", "") or str(id(fn.__globals__))
        if mod_doc and mod_name not in seen_modules:
            seen_modules.add(mod_name)
            lines = [ln for ln in mod_doc.strip().splitlines() if ln.strip()]
            table = [ln for ln in lines if ln.lstrip().startswith("|") or ln.lstrip().startswith("- ") or ln.lstrip().startswith("* ")]
            head = " ".join(lines[:2])[:300]
            parts.append("### Modul\n" + head + ("\n" + "\n".join(table[:40]) if table else ""))
        doc = inspect.getdoc(fn) or "(keine Beschreibung)"
        parts.append(f"### {t}\n{doc[:900]}")
    limits = {t: bs.limits.get(t, {}) for t in scene_types if bs.limits.get(t)}
    return "\n\n".join(parts), limits


def _business_text(settings: BrandSettings, key: str) -> str:
    p = settings.business_path(key)
    if p and p.exists():
        return p.read_text(encoding="utf-8")
    return ""


def _load_json(p: Path | None) -> dict | None:
    if p and p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


SKIP_HEADINGS = ("abgrenzung", "offene punkte", "übernahme", "produktion je video", "higgsfield", "freigabe", "stand ")


def format_essentials(text: str, max_chars: int = 9000) -> str:
    """The Format-Bibel without sections that only matter to the sessions (comparison with other brands, open points,
    week-1 conversion, production steps), capped at `max_chars`."""
    if not text:
        return ""
    out: list[str] = []
    skip = False
    for line in text.splitlines():
        if line.startswith("#"):
            h = line.lstrip("#").strip().lower()
            skip = any(k in h for k in SKIP_HEADINGS)
        if not skip:
            out.append(line)
    s = "\n".join(out).strip()
    if len(s) > max_chars:
        s = s[:max_chars].rsplit("\n", 1)[0] + "\n… (gekürzt)"
    return s


def shorten_plan(plan: dict, n_beats: int = 3, keep_layout: tuple[str, ...] = ()) -> dict:
    """Few-shot excerpt of an approved plan: the schema, two hook candidates, the first `n_beats` beats (hook plus the
    next scene types) and the last beat as patterns, one source, the layout with three sound cues."""
    p = json.loads(json.dumps(plan, ensure_ascii=False))
    p.pop("notes", None)
    p["unverified"] = (p.get("unverified") or [])[:1]
    beats = p.get("beats") or []
    if len(beats) > n_beats + 1:
        kept = beats[:n_beats] + [{"…": f"{len(beats) - n_beats - 1} weitere Beats in derselben Form (alle Szenentypen siehe Dokumentation)"}] + beats[-1:]
        p["beats"] = kept
    for b in p["beats"]:
        b.pop("overlay", None)
        b.pop("duration_hint", None)
    cands = p.get("hook_candidates") or []
    chosen = (p.get("hook") or {}).get("id")
    keep = [c for c in cands if c.get("id") == chosen][:1] + [c for c in cands if c.get("id") != chosen][:1]
    for c in keep:
        c["why"] = {k: (v[:40] + "…" if isinstance(v, str) and len(v) > 40 else v) for k, v in list((c.get("why") or {}).items())[:1]}
        if isinstance(c.get("visual"), str) and len(c["visual"]) > 60:
            c["visual"] = c["visual"][:60] + "…"
    if len(cands) > len(keep):
        keep.append({"…": f"{len(cands) - len(keep)} weitere Kandidaten, je einer je Hook-Typ"})
    p["hook_candidates"] = keep
    p["sources"] = (p.get("sources") or [])[:1]
    lay = p.get("layout") or {}
    if isinstance(lay.get("sound_cues"), list) and len(lay["sound_cues"]) > 3:
        lay["sound_cues"] = lay["sound_cues"][:3] + [{"…": f"{len(lay['sound_cues']) - 3} weitere Cues in derselben Form"}]
    for k in ("companion_text", "description", "sound_note"):
        if isinstance(lay.get(k), str) and len(lay[k]) > 110:
            lay[k] = lay[k][:110] + " …"
    for k in ("media", "model3d", "computations", "ruler"):
        if k in keep_layout:                                   # brand needs this block whole (e.g. Gigastruct model3d)
            continue
        v = lay.get(k)
        if isinstance(v, list) and len(v) > 2:
            lay[k] = v[:2] + [{"…": f"{len(v) - 2} weitere Einträge in derselben Form"}]
        elif isinstance(v, dict) and len(json.dumps(v, ensure_ascii=False)) > 1200:
            lay[k] = {"…": "wie im Beispiel der Marke (Struktur beibehalten); Details siehe Szenen-Dokumentation"}
    return p


def build_context(settings: BrandSettings, konzeptplan: Konzeptplan) -> BrandContext:
    from .settings import load_aufbauten
    brand = load_brand(settings.brand_id)
    entry = next((b for b in brands_config()["brands"] if b["id"] == brand.id), {})
    docs, limits = scene_docs(brand.id, settings.scene_types)
    recs: list[str] = []
    rec_dir = BRANDS_DIR / brand.id / "echtlauf" / "recordings"
    if rec_dir.exists():
        recs = sorted(p.name for p in rec_dir.iterdir() if p.is_dir() and not p.name.startswith("_"))
    return BrandContext(
        brand=brand, settings=settings, konzeptplan=konzeptplan,
        format_bible=_business_text(settings, "format_bible"),
        testvideo_concept=_business_text(settings, "testvideo_concept"),
        example_de=_load_json(settings.example_plan("de")) or {},
        example_en=_load_json(settings.example_plan("en")),
        extra_example_de=_load_json(settings.extra_example_plan("de")),
        extra_example_en=_load_json(settings.extra_example_plan("en")),
        scene_docs=docs, limits=limits, material=material_items(settings),
        brand_rules=list(entry.get("rules", [])) + [str(r) for r in (brand.design.get("rules") or [])],
        recordings=recs,
        format_essentials=format_essentials(_business_text(settings, "format_bible"), int(settings.get("format_bible_max_chars", 9000))),
        aufbauten=load_aufbauten(settings.brand_id),
    )


def recording_for_title(brand_id: str, title: str) -> str | None:
    """Recording id whose spec `title` is a prefix of the Konzeptplan title (brands/<id>/echtlauf/specs/<id>.json, DE only)."""
    specs = BRANDS_DIR / brand_id / "echtlauf" / "specs"
    if not specs.exists():
        return None
    want = _norm(title)
    best, best_len = None, 0
    for p in specs.glob("*.json"):
        if p.stem.endswith("-en"):
            continue
        try:
            t = str(json.loads(p.read_text(encoding="utf-8")).get("title", ""))
        except (json.JSONDecodeError, OSError):
            continue
        have = _norm(t)
        if have and want.startswith(have) and len(have) > best_len:
            rec_dir = BRANDS_DIR / brand_id / "echtlauf" / "recordings" / p.stem
            if rec_dir.exists():
                best, best_len = p.stem, len(have)
    return best


# ---------------------------------------------------------------- calendar sources

def _calendar(brand_id: str) -> list[dict]:
    out: list[dict] = []
    for p in sorted((DATA_DIR / "calendars").glob(f"{brand_id}_*.json")):
        if p.name.endswith((".research.json", ".plan.json")):      # the month plan is not a source store
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            out.extend(e for e in data if isinstance(e, dict))
        elif isinstance(data, dict):
            for k in ("topics", "items", "entries"):
                if isinstance(data.get(k), list):
                    out.extend(e for e in data[k] if isinstance(e, dict))
    return out


def _research(brand_id: str) -> list[dict]:
    out: list[dict] = []
    for p in sorted((DATA_DIR / "calendars").glob(f"{brand_id}_*.research.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            out.extend(e for e in data if isinstance(e, dict))
        elif isinstance(data, dict):
            out.extend(v for v in data.values() if isinstance(v, dict))
    return out


def calendar_entry(brand_id: str, topic: Topic) -> dict | None:
    cal = _calendar(brand_id)
    if topic.calendar_id:
        e = next((x for x in cal if x.get("topic_id") == topic.calendar_id), None)
        if e:
            return e
    want = _norm(topic.title)
    best, score = None, 0.0
    for e in cal:
        if e.get("language") not in (None, "de"):
            continue
        have = _norm(str(e.get("title", "")))
        s = difflib.SequenceMatcher(None, want, have).ratio()
        if want and (want in have or have in want):
            s = max(s, 0.85)
        if s > score:
            best, score = e, s
    return best if score >= 0.72 else None


def research_entry(brand_id: str, topic: Topic, cal: dict | None) -> dict | None:
    want = _norm(str((cal or {}).get("title") or topic.title))
    best, score = None, 0.0
    for e in _research(brand_id):
        have = _norm(str(e.get("title_de") or e.get("title") or ""))
        s = difflib.SequenceMatcher(None, want, have).ratio()
        if s > score:
            best, score = e, s
    return best if score >= 0.8 else None


def source_refs(topic: Topic, cal: dict | None, research: dict | None) -> list[SourceRef]:
    """Allowed sources for the plan: calendar URLs (with their check date), research evidence as titles."""
    refs: list[SourceRef] = []
    urls = list((cal or {}).get("source_urls") or [])
    checked = str((cal or {}).get("source_checked_at") or "")
    evidence = list((research or {}).get("source_evidence") or [])
    for k, url in enumerate(urls, 1):
        title = evidence[k - 1] if k - 1 < len(evidence) else ""
        refs.append(SourceRef(id=f"S{k}", url=url, title=title, checked_at=checked))
    return refs


def check_sources(refs: list[SourceRef], today: str, timeout: float = 12.0) -> None:
    """HTTP reachability (HEAD, GET on 405/403): reachable -> checked_at = today; else keep the calendar date."""
    try:
        import requests
    except ImportError:
        return
    headers = {"User-Agent": "Mozilla/5.0 (faceless-network daily runner; source check)"}
    for r in refs:
        try:
            resp = requests.head(r.url, allow_redirects=True, timeout=timeout, headers=headers)
            if resp.status_code in (403, 405, 404, 500, 501):
                resp = requests.get(r.url, allow_redirects=True, timeout=timeout, headers=headers, stream=True)
            r.reachable = 200 <= resp.status_code < 400
            r.note = f"HTTP {resp.status_code}"
            if r.reachable:
                r.checked_at = today
        except Exception as exc:  # noqa: BLE001 - network problems are information, not failures
            r.reachable = False
            r.note = f"nicht erreichbar: {type(exc).__name__}"
