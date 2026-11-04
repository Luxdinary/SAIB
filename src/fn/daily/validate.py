"""Plan checks before any cost: story and hook engines, scene types, text limits, word anchors, sources, files, length."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from ..config import BRANDS_DIR, ROOT
from ..direction import hooks, story
from .context import BrandContext, SourceRef

MEDIA_RE = re.compile(r"^[\w./\\-]+\.(?:jpe?g|png|webp|mp4|webm|mov)$", re.I)
W_ANCHOR = re.compile(r"^w:(.+?)(?:#(\d+))?(?:[+-]\d+(?:\.\d+)?)*$")
AT_ANCHOR = re.compile(r"^@(.+?)(?:[+-]\d+(?:\.\d+)?)*$")
_OFFSETS = re.compile(r"(?:[+-]\d+(?:\.\d+)?)+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
OPTIONAL_DATA_KEYS = {"audio_cues", "sound", "cues", "note", "notes", "source"}   # may differ between the DE and EN plan


_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def spoken_numbers(text: str) -> list[str]:
    """Standalone numbers of a text (not glued to letters: 'H4', '100s', '50Hz' are skipped)."""
    out = []
    for m in _NUM.finditer(text or ""):
        before = text[m.start() - 1] if m.start() > 0 else " "
        after = text[m.end()] if m.end() < len(text) else " "
        if before.isalpha() or after.isalpha():
            continue
        out.append(m.group(0))
    return out


def evidence_digits(text: str) -> set[str]:
    """Digit strings of every number in the evidence: '18,75' -> '1875' (and its parts '18', '75'), '20.07.2020' -> '20', '07', '2020'."""
    s: set[str] = set()
    for m in _NUM.finditer(text or ""):
        s.add(re.sub(r"\D", "", m.group(0)))
    s.update(re.findall(r"\d+", text or ""))
    return s


def ungrounded_numbers(texts: dict[str, str], evidence: str) -> list[tuple[str, str]]:
    """(where, number) for every number of the public texts that the evidence does not contain. Plain integers up to 12
    (counts like 'zwei Auslöser') are not checked; decimals, dates and years always are. A number counts as grounded when its
    digits appear in the evidence (decimal comma or point, thousands point or space do not matter)."""
    ev = evidence_digits(evidence)
    bad: list[tuple[str, str]] = []
    for where, text in texts.items():
        for tok in spoken_numbers(text):
            digits = re.sub(r"\D", "", tok)
            if not digits:
                continue
            has_sep = bool(re.search(r"[.,]\d", tok))
            if not has_sep and int(digits) <= 12:
                continue
            if digits in ev:
                continue
            parts = re.findall(r"\d+", tok)
            if len(parts) > 1 and all(p in ev for p in parts):
                continue
            bad.append((where, tok))
    return bad


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


_EDGE = ",.;:!?()[]{}\"„“”‚‘’«»'"


def _tokens(text: str) -> list[str]:
    return [t.strip(_EDGE) for t in text.split() if t.strip(_EDGE)]


def _norm_word(s: str) -> str:
    """Like the brand templates' `_norm` for anchors: case-insensitive, punctuation stripped."""
    return re.sub(r"[^\w]+", "", s.lower())


def _word_hits(spoken: str, word: str) -> int:
    key = _norm_word(word)
    if not key:
        return 0
    return sum(1 for t in _tokens(spoken) if _norm_word(t).startswith(key))


def _walk(obj, path: str = ""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk(v, f"{path}[{i}]")
    else:
        yield path, obj


def _check_anchors(beat: dict, res: ValidationResult, where: str) -> None:
    spoken = beat.get("spoken", "")
    for path, val in _walk(beat.get("data", {})):
        if not isinstance(val, str):
            continue
        key = path.rsplit(".", 1)[-1]
        word = None
        n = 1
        m = W_ANCHOR.match(val)
        if m:
            word, n = m.group(1), int(m.group(2) or 1)
        else:
            m2 = AT_ANCHOR.match(val)
            if m2 and not val.startswith("@@"):
                word = m2.group(1)
            elif (key.endswith("_word") or key == "at_word") and val and not val.replace(".", "").isdigit():
                word = val
        if word is None:
            continue
        word = _OFFSETS.sub("", re.sub(r"#\d+$", "", word))
        hits = _word_hits(spoken, word)
        if hits >= n:
            continue
        if hits == 0:
            res.errors.append(f"{where} {path}: Anker '{val}' ist kein Wort des Sprechtexts dieses Beats")
        else:
            res.errors.append(f"{where} {path}: Anker '{val}' braucht Vorkommen Nr. {n}, gefunden {hits}")


def _check_limits(beat: dict, limits: dict, res: ValidationResult, where: str) -> None:
    lim = limits.get(beat.get("scene_type"), {})
    if not lim:
        return
    data = beat.get("data", {})
    for fieldname, maxlen in lim.items():
        v = data.get(fieldname)
        if isinstance(v, str) and len(v) > int(maxlen):
            res.errors.append(f"{where} data.{fieldname}: {len(v)} Zeichen > {maxlen}")
        elif isinstance(v, dict) and isinstance(v.get("text"), str) and len(v["text"]) > int(maxlen):
            res.errors.append(f"{where} data.{fieldname}.text: {len(v['text'])} Zeichen > {maxlen}")
        elif isinstance(v, list):
            for i, item in enumerate(v):
                t = item.get("text") if isinstance(item, dict) else item
                if isinstance(t, str) and len(t) > int(maxlen):
                    res.errors.append(f"{where} data.{fieldname}[{i}]: {len(t)} Zeichen > {maxlen}")


def resolve_media(name: str, brand_id: str, plan: dict, extra_bases: list[Path] | None = None) -> Path | None:
    """Find a media file named in a plan: plan.assets.folder, layout.media_folder, the configured material folders,
    assets/higgsfield, assets, brand folder."""
    brand_dir = BRANDS_DIR / brand_id
    p = Path(name)
    if p.is_absolute():
        return p if p.exists() else None
    bases = list(extra_bases or [])
    folder = (plan.get("assets") or {}).get("folder")
    if folder:
        bases.append(brand_dir / folder)
    media_folder = (plan.get("layout") or {}).get("media_folder")
    if media_folder:
        bases.append(brand_dir / media_folder)
    bases += [brand_dir / "assets" / "higgsfield", brand_dir / "assets", brand_dir]
    for b in bases:
        c = b / name
        if c.exists():
            return c
    return None


def validate_plan(plan: dict, ctx: BrandContext, refs: list[SourceRef], lang: str, *,
                  char_window: tuple[int, int, int], require_recording: bool = False,
                  allowed_types: set[str] | None = None, chars_per_second: float = 15.0,
                  evidence: str | None = None, expected_recording: str | None = None, check_length: bool = True) -> ValidationResult:
    res = ValidationResult()
    s = ctx.settings
    # 1) schema + story engine
    try:
        dp = story.from_dict(plan)
    except (KeyError, TypeError) as exc:
        res.errors.append(f"Plan nicht lesbar: {exc!r}")
        return res
    for p in story.validate(dp):
        res.errors.append(f"story: {p}")
    for a in story.advice(dp):
        res.warnings.append(f"story: {a}")
    if plan.get("language") != lang:
        res.errors.append(f"language muss {lang!r} sein")
    if plan.get("brand_id") != ctx.brand.id:
        res.errors.append(f"brand_id muss {ctx.brand.id!r} sein")
    # 2) hooks (field types first, so the model gets a readable message)
    raw_cands = plan.get("hook_candidates")
    if not isinstance(raw_cands, list):
        raw_cands = []
        res.errors.append("hook_candidates muss eine Liste von fünf Objekten sein")
    for i, c in enumerate(raw_cands):
        if not isinstance(c, dict):
            res.errors.append(f"hook_candidates[{i}] muss ein Objekt sein")
            continue
        for k in ("id", "type", "spoken"):
            if not isinstance(c.get(k), str) or not c.get(k):
                res.errors.append(f"hook_candidates[{i}].{k} fehlt oder ist kein Text")
        sc = c.get("scores")
        if not isinstance(sc, dict) or any(not isinstance(v, int) or isinstance(v, bool) for v in sc.values()):
            res.errors.append(f"hook_candidates[{i}].scores muss ein Objekt mit ganzen Zahlen sein: {{\"clarity\": 4, \"relevance\": 4, \"curiosity\": 4, \"truth\": 5, \"visual\": 4}}")
        if c.get("why") is not None and not isinstance(c.get("why"), dict):
            res.errors.append(f"hook_candidates[{i}].why muss ein Objekt sein (Kriterium -> Begründung), keine Liste und kein Text")
        if c.get("source_ids") is not None and not isinstance(c.get("source_ids"), list):
            res.errors.append(f"hook_candidates[{i}].source_ids muss eine Liste sein")
    try:
        cands = [hooks.from_dict(c) for c in raw_cands if isinstance(c, dict) and isinstance(c.get("scores"), dict)
                 and isinstance(c.get("why", {}), dict)]
    except (KeyError, TypeError, ValueError) as exc:
        cands = []
        res.errors.append(f"hook_candidates nicht lesbar: {exc!r}")
    for p in hooks.validate_set(cands):
        res.errors.append(f"hooks: {p}")
    chosen = next((c for c in cands if c.id == (plan.get("hook") or {}).get("id")), None)
    if chosen is None:
        res.errors.append("hook.id nennt keinen Kandidaten")
    else:
        for p in chosen.problems():
            res.errors.append(f"hook {chosen.id}: {p}")
        if dp.beats and not dp.beats[0].spoken.strip().startswith(chosen.spoken.strip()[:40]):
            res.warnings.append("erster Beat beginnt nicht mit dem Text des gewählten Hooks")
    # 3) scene types, limits, anchors
    allowed = set(allowed_types) if allowed_types is not None else set(s.scene_types)
    for b in plan.get("beats", []):
        where = f"beat {b.get('id')}"
        if allowed and b.get("scene_type") not in allowed:
            res.errors.append(f"{where}: Szenentyp {b.get('scene_type')!r} nicht erlaubt (erlaubt: {sorted(allowed)})")
        _check_limits(b, ctx.limits, res, where)
        _check_anchors(b, res, where)
    beats_by_id = {b.get("id"): b for b in plan.get("beats", [])}
    for i, c in enumerate((plan.get("layout") or {}).get("sound_cues") or []):
        at = c.get("at")
        b = beats_by_id.get(c.get("beat"))
        if b is None:
            res.errors.append(f"sound_cues[{i}]: Beat {c.get('beat')!r} gibt es nicht")
            continue
        if isinstance(at, str):
            m = W_ANCHOR.match(at)
            if m and _word_hits(b.get("spoken", ""), re.sub(r"#\d+$", "", m.group(1))) <= 0:
                res.errors.append(f"sound_cues[{i}]: Anker '{at}' ist kein Wort des Sprechtexts von {c.get('beat')}")
    # 4) sources
    allowed_urls = {r.url.rstrip("/") for r in refs}
    date_by_url = {r.url.rstrip("/"): r.checked_at for r in refs}
    for src in plan.get("sources", []):
        url = str(src.get("url", "")).rstrip("/")
        if url.startswith("file:"):
            rel = url[5:].lstrip("/")
            if not ((ROOT / rel).exists() or Path(rel).exists()):
                res.errors.append(f"source {src.get('id')}: Datei-Quelle {url[:80]} gibt es nicht")
            continue
        if allowed_urls and url not in allowed_urls:
            res.errors.append(f"source {src.get('id')}: URL nicht in der Quellenliste ({url[:80]})")
        if not DATE_RE.match(str(src.get("checked_at", ""))):
            res.errors.append(f"source {src.get('id')}: checked_at muss JJJJ-MM-TT sein")
        elif url in date_by_url and date_by_url[url] and src.get("checked_at") != date_by_url[url]:
            res.warnings.append(f"source {src.get('id')}: checked_at {src.get('checked_at')} statt {date_by_url[url]} (wird gesetzt)")
            src["checked_at"] = date_by_url[url]
    if not plan.get("sources"):
        res.errors.append("keine Quelle im Plan")
    # 5) material files
    for path, val in _walk({k: v for k, v in plan.items() if k in ("beats", "layout", "assets")}):
        if isinstance(val, str) and MEDIA_RE.match(val) and not val.startswith("file:"):
            if path.startswith("assets.folder") or path.endswith("sfx_folder"):
                continue
            if resolve_media(val, ctx.brand.id, plan, s.material_folders) is None:
                res.errors.append(f"{path}: Datei {val!r} nicht gefunden (nur Dateien aus der Materialliste)")
    # 6) recording (Promptwerk)
    if require_recording:
        rec = ((plan.get("layout") or {}).get("echtlauf") or {}).get("recording")
        if not rec or rec not in ctx.recordings:
            res.errors.append(f"layout.echtlauf.recording {rec!r} ist keine vorhandene Aufzeichnung ({', '.join(ctx.recordings[:12])} …)")
        elif expected_recording and rec != expected_recording:
            res.errors.append(f"layout.echtlauf.recording muss {expected_recording!r} sein (die Aufzeichnung zu diesem Thema), nicht {rec!r}")
    # 7) length and texts
    spoken = " ".join(b.get("spoken", "").strip() for b in plan.get("beats", []))
    lo, target, hi = char_window
    est = len(spoken) / max(chars_per_second, 1.0)          # estimated voice seconds; video = lead 0.4 s + voice + tail ~2.6 s
    if check_length and (est + 3.0 < 65.0 or est + 3.0 > 90.0):
        res.errors.append(f"Sprechtext {len(spoken)} Zeichen = etwa {est:.0f} s Stimme, Video außerhalb 65–90 s; Ziel {target} Zeichen ({lo}–{hi})")
    elif check_length and (len(spoken) < lo or len(spoken) > hi):
        res.warnings.append(f"Sprechtext {len(spoken)} Zeichen (etwa {est:.0f} s Stimme), Ziel {lo}–{hi}")
    if "!" in spoken:
        res.warnings.append("Ausrufezeichen im Sprechtext")
    if evidence is not None:                                    # numbers, years and dates must stand in the evidence
        lay = plan.get("layout") or {}
        texts = {f"beat {b.get('id')} (Sprechtext)": b.get("spoken", "") for b in plan.get("beats", [])}
        texts.update({"title": str(plan.get("title", "")), "layout.description": str(lay.get("description", "")),
                      "layout.companion_text": str(lay.get("companion_text", ""))})
        own = json.dumps(lay.get("computations", ""), ensure_ascii=False) + " " + " ".join(
            json.dumps((b.get("data") or {}).get("calcs", ""), ensure_ascii=False) for b in plan.get("beats", []))
        bad = ungrounded_numbers(texts, evidence + " " + own)
        for where, tok in bad[:8]:
            res.errors.append(f"{where}: Zahl {tok} steht in keinem Beleg (Kalenderansatz, Belegsätze, Quellentitel, Hinweise); "
                              f"weglassen oder ohne Zahl formulieren, sonst als Satz in `unverified`")
    if "UNVERIFIED" in spoken.upper():
        res.errors.append("UNVERIFIED im Sprechtext")
    title = str(plan.get("title", ""))
    if not title or len(title) > 100:
        res.errors.append("title fehlt oder länger als 100 Zeichen")
    short = str((plan.get("layout") or {}).get("short_title") or "")
    if not short:
        res.warnings.append("layout.short_title fehlt (Kurztitel wird aus dem Titel gebildet)")
    elif len(short) > 40 or re.search(r"[<>:\"/\\|?*]", short):      # the prompt asks for 28; the brand examples reach 32; 40 is the cut of the export name
        res.errors.append("layout.short_title: höchstens 40 Zeichen (Ziel 28), keine Sonderzeichen")
    return res


def compare_structure(de: dict, en: dict) -> list[str]:
    """The English plan must be the same video: beats, scene types, data keys, sources, files, layout numbers."""
    p: list[str] = []
    bd, be = de.get("beats", []), en.get("beats", [])
    if len(bd) != len(be):
        p.append(f"EN hat {len(be)} Beats, DE {len(bd)}")
    for x, y in zip(bd, be):
        if x.get("id") != y.get("id") or x.get("function") != y.get("function") or x.get("scene_type") != y.get("scene_type"):
            p.append(f"Beat {x.get('id')}: id/function/scene_type weichen ab ({y.get('id')}, {y.get('function')}, {y.get('scene_type')})")
        kx, ky = set(x.get("data", {}).keys()), set(y.get("data", {}).keys())
        if (kx - OPTIONAL_DATA_KEYS) != (ky - OPTIONAL_DATA_KEYS):
            p.append(f"Beat {x.get('id')}: Datenfelder weichen ab (fehlt: {sorted(kx - ky)}, zu viel: {sorted(ky - kx)})")
        if x.get("source_ids") != y.get("source_ids"):
            p.append(f"Beat {x.get('id')}: source_ids weichen ab")
    sd = [(s.get("id"), "file:" if str(s.get("url", "")).startswith("file:") else str(s.get("url")).rstrip("/")) for s in de.get("sources", [])]
    se = [(s.get("id"), "file:" if str(s.get("url", "")).startswith("file:") else str(s.get("url")).rstrip("/")) for s in en.get("sources", [])]
    if sd != se:
        p.append("Quellen (id, url) weichen ab")
    ad = {k: v for k, v in (de.get("assets") or {}).items() if k not in ("note", "notes")}
    ae = {k: v for k, v in (en.get("assets") or {}).items() if k not in ("note", "notes")}
    if ad != ae:
        p.append("assets weichen ab (Dateien, Ordner oder scrim)")
    files_de = sorted(v for _, v in _walk(de.get("beats", [])) if isinstance(v, str) and MEDIA_RE.match(v))
    files_en = sorted(v for _, v in _walk(en.get("beats", [])) if isinstance(v, str) and MEDIA_RE.match(v))
    if files_de != files_en:
        p.append("Bildmaterial in den Beats weicht ab")
    ld, le = de.get("layout", {}), en.get("layout", {})
    text_keys = {"description", "companion_text", "hashtags", "short_title", "sound_cues", "sound_note", "series_topic", "stamp"}
    for k, v in ld.items():
        if k in text_keys:
            continue
        if isinstance(v, (int, float, bool)) and le.get(k) != v:
            p.append(f"layout.{k}: {le.get(k)!r} statt {v!r}")
        if k not in le:
            p.append(f"layout.{k} fehlt im EN-Plan")
    if (en.get("hook") or {}).get("id") != (de.get("hook") or {}).get("id"):
        p.append("hook.id weicht ab")
    return p
