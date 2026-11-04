"""Copy a finished direction render into the production folder structure of OneDrive\\Business\\05 Produktion.

Creates `05 Produktion\\<date> <short title>\\` from `_Vorlage Video` (never overwrites an existing video file without
--force) and fills it from storage/direction/<video_id>-<version>/ and the plan:

  01 Skript\\Skript.md                    hook, scene table, close, sources, unverified items
  03 Schnittprojekt\\                     plan.timed.json, manifest.json, report.json (render provenance)
  04 Export\\<date> <short> – 9x16.mp4    the finished video
  05 Thumbnail und Cover\\<date> <short> – Cover.jpg
  06 Untertitel\\<date> <short>.srt + captions.json
  Veröffentlichung.md                    title, description, hashtags per platform, sources, AI labels

Without a render (`--plan-only`) only the script and a draft Veröffentlichung.md are written.
Nothing is published and nothing is deleted.

Run: .venv\\Scripts\\python.exe scripts\\export_production_folder.py data\\direction\\<id>.json --version V1 --short "KI-Kennzeichnung"
"""
from __future__ import annotations

import argparse
import difflib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fn.brands import load_brand  # noqa: E402
from fn.config import STORAGE_DIR, brands_config, mirror_dir, production_folder  # noqa: E402

# Scutoria's closing sentence; other brands set `production.closing_sentence.<lang>` in brands/<id>/brand.yaml
SCUTORIA_SENTENCE = "Mehr Informationen: https://scutoria.com · Folge Scutoria für weitere Tipps zur KI-Sicherheit im Betrieb."
PLATFORMS = [("TikTok", "is_aigc"), ("Instagram Reels", "is_ai_generated"), ("YouTube Shorts", "containsSyntheticMedia")]
SENTENCE = ""   # set per plan in main()
# caption limits incl. hashtags; Instagram 2,200 (Prüfrunde 03.11.2026), YouTube description 5,000; TikTok not checked
CAPTION_LIMITS = {"Instagram Reels": 2200, "YouTube Shorts": 5000}


def brand_texts(plan: dict) -> dict:
    """Closing sentence, domain and template reference of the plan's brand (brand.yaml `production`, brands.yaml)."""
    brand = load_brand(plan["brand_id"])
    prod = brand.design.get("production", {})
    lang = plan.get("language", "de")
    entry = next((e for e in brands_config()["brands"] if e["id"] == brand.id), {})
    sentence = (prod.get("closing_sentence") or {}).get(lang) or (SCUTORIA_SENTENCE if brand.id == "ai_security" else "")
    domain = prod.get("domain") or ("scutoria.com" if brand.id == "ai_security" else "")
    doc = entry.get("template_doc", "")
    template = f"{brand.name} {entry.get('brand_version', '')}".strip() + (f" (`{doc}`)" if doc else "")
    fmt = plan.get("layout", {}).get("format")
    if fmt:                                       # own format since 02.11.2026: name the format bible, not the old template
        template = f"Format „{fmt}“ (`02 Marke\\{brand.name}\\Format-Bibel.md`)"
    return {"sentence": sentence, "domain": domain, "template": template}


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(captions: list[dict], dst: Path) -> None:
    lines = []
    for i, c in enumerate(captions, 1):
        lines += [str(i), f"{srt_time(c['start'])} --> {srt_time(c['end'])}", c["text"], ""]
    dst.write_text("\n".join(lines), encoding="utf-8")


def script_md(plan: dict, date: str, short: str, duration: float | None, texts: dict) -> str:
    hook = next((h for h in plan["hook_candidates"] if h["id"] == plan["hook"]["id"]), {})
    rows = []
    for i, b in enumerate(plan["beats"], 1):
        d = b.get("data", {})
        shown = d.get("headline") or d.get("question") or ""
        rows.append(f"| {i} | {b['function']} · {b['scene_type']} | {b['spoken']} | {shown} | {', '.join(b.get('source_ids', [])) or '–'} |")
    cands = "\n".join(f"- {h['id']} ({h['type']}): „{h['spoken']}“ · Wahrheit {h['scores']['truth']}/5" for h in plan["hook_candidates"])
    srcs = "\n".join(f"- [{s['id']}] {s['title']} – {s['url']} (abgerufen {s['checked_at']})" for s in plan["sources"])
    unv = "\n".join(f"- {u}" for u in plan.get("unverified", [])) or "- keine"
    bg = plan.get("assets", {}).get("background", {})
    return f"""# Skript – {short}

- Geplante Veröffentlichung: {date}
- Kanäle und Formate: TikTok, Instagram Reels, YouTube Shorts · 9:16, 1080 × 1920
- Länge: {f'{duration:.1f} s' if duration else 'Ziel 65–90 s'}
- Ziel des Videos: {plan['layout'].get('description', plan['title'])}
- Vorlage: {texts['template'] or '–'}; Plan `{plan['video_id']}.json`

## Hook (erste 3 Sekunden)

Gewählt: {hook.get('id')} – „{hook.get('spoken')}“ (Bildschirm: „{hook.get('on_screen')}“). {plan['hook'].get('note', '')}

Kandidaten:
{cands}

## Ablauf
| # | Funktion · Szenentyp | Text / Sprecher | Einblendung | Quellen |
|---|---|---|---|---|
{chr(10).join(rows)}

{f"Roter Faden: {plan['layout']['status_bar'].get('file', '–')} mit Statusleiste (Amber = offen, Rot = Sperre). " if plan['layout'].get('status_bar') else ''}{f"Hintergründe: {', '.join(f'{k} → {v}' for k, v in bg.items())}." if bg else ''}

## Abschluss und Handlungsaufforderung

{plan['beats'][-1]['spoken']}{f" {texts['domain']} ist die letzten Sekunden lesbar." if texts['domain'] else ''}

## Quellen

{srcs}

## Nicht verwendet (unbelegt oder außerhalb des Themas)

{unv}
"""


def publish_md(plan: dict, post: dict | None, short: str, export_name: str, cover_name: str) -> str:
    title = (post or {}).get("title") or plan["title"]
    desc = (post or {}).get("description") or plan["layout"].get("description", "")
    tags = (post or {}).get("hashtags") or plan["layout"].get("hashtags", [])
    if SENTENCE and not _has_similar(desc, SENTENCE):
        desc = desc + "\n\n" + SENTENCE
    tag_line = " ".join(f"#{t}" for t in tags)
    parts = [f"# Veröffentlichung – {short}\n",
             "Je Kanal ein Abschnitt. Nach dem Posten Link und Datum eintragen und den Status im `Redaktionsplan.csv` setzen. "
             "Nichts ist veröffentlicht. KI-Kennzeichnung ist bei jedem Kanal Pflicht (Stefans Vorgabe).\n"]
    for name, flag in PLATFORMS:
        size = len(desc) + 2 + len(tag_line)
        limit = CAPTION_LIMITS.get(name)
        if limit and size > limit:
            print(f"warning: {name} text has {size} characters, limit {limit}")
            parts.append(f"> **Achtung:** Text für {name} hat {size} Zeichen, erlaubt sind {limit}. Vor dem Posten kürzen.\n")
        parts.append(f"""## {name}
- Datei: `04 Export\\{export_name}`
- Titel: {title}
- Beschreibung:

```
{desc}
```
- Hashtags: {tag_line}
- KI-Kennzeichnung: `{flag}` = true
- Thumbnail / Cover: `05 Thumbnail und Cover\\{cover_name}`
- Veröffentlicht am / Link:
""")
    parts.append("## Quellen\n\n" + "\n".join(f"- [{s['id']}] {s['title']} – {s['url']} (abgerufen {s['checked_at']})" for s in plan["sources"]) + "\n")
    return "\n".join(parts)                       # the closing sentence is already part of each description


def _has_similar(text: str, sentence: str, ratio: float = 0.8) -> bool:
    """True when `sentence` or a near-identical paragraph (companion_text vs. closing_sentence) is already in `text`."""
    if sentence in text:
        return True
    norm = lambda s: " ".join(s.lower().split())
    return any(difflib.SequenceMatcher(None, norm(p), norm(sentence)).ratio() >= ratio for p in text.split("\n") if p.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--version", default="V1")
    ap.add_argument("--short", required=True, help="short title for folder and file names")
    ap.add_argument("--date", default=None, help="YYYY-MM-DD (default: from video_id)")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    texts = brand_texts(plan)
    global SENTENCE
    SENTENCE = texts["sentence"]
    vid = plan["video_id"]
    date = a.date or f"{vid.split('-')[1][:4]}-{vid.split('-')[1][4:6]}-{vid.split('-')[1][6:8]}"
    base = mirror_dir()
    folder = production_folder(plan["brand_id"], date, a.short)   # 05 Produktion\<Marke>\<JJJJ-MM>\...
    tmpl = base / "_Vorlage Video"
    if not folder.exists():
        shutil.copytree(tmpl, folder)
    export_name = f"{date} {a.short} – 9x16.mp4"
    cover_name = f"{date} {a.short} – Cover.jpg"
    render = STORAGE_DIR / "direction" / f"{vid}-{a.version}"
    duration = None
    post = None
    if not a.plan_only:
        if not (render / "video.mp4").exists():
            print(f"no render in {render}; use --plan-only")
            return 2
        prov = json.loads((render / "manifest.json").read_text(encoding="utf-8")).get("tts", {}).get("provider")
        if prov not in ("gemini",):
            print(f"render voice is {prov!r}; only Google/Gemini voices may be exported (Stefan, 30.10.2026)")
            return 4
        dst = folder / "04 Export" / export_name
        if dst.exists() and not a.force:
            print(f"{dst} exists; use --force to replace it")
            return 3
        shutil.copy2(render / "video.mp4", dst)
        shutil.copy2(render / "cover.jpg", folder / "05 Thumbnail und Cover" / cover_name)
        caps = json.loads((render / "captions.json").read_text(encoding="utf-8"))
        write_srt(caps, folder / "06 Untertitel" / f"{date} {a.short}.srt")
        shutil.copy2(render / "captions.json", folder / "06 Untertitel" / "captions.json")
        for n in ("plan.timed.json", "manifest.json", "report.json", "post.json"):
            if (render / n).exists():
                shutil.copy2(render / n, folder / "03 Schnittprojekt" / n)
        man = json.loads((render / "manifest.json").read_text(encoding="utf-8"))
        duration = man.get("render", {}).get("duration")
        post = json.loads((render / "post.json").read_text(encoding="utf-8")) if (render / "post.json").exists() else None
    (folder / "01 Skript" / "Skript.md").write_text(script_md(plan, date, a.short, duration, texts), encoding="utf-8")
    (folder / "Veröffentlichung.md").write_text(publish_md(plan, post, a.short, export_name, cover_name), encoding="utf-8")
    print(f"folder: {folder}")
    print(f"export: {'(no render yet)' if a.plan_only else folder / '04 Export' / export_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
