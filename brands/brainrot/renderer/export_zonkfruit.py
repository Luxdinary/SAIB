"""Copy a finished Zonkfruit render into OneDrive\\Business\\05 Produktion\\Tintora\\<JJJJ-MM>\\<date> <short>\\ (structure of _Vorlage Video).

Like scripts/export_production_folder.py (whose SRT writer it reuses), but with Zonkfruit texts: no Scutoria sentence,
per-platform title/description/hashtags from plan.layout.platform_texts, character and sound-effect licences.
Never overwrites an exported video without --force; nothing is published, nothing deleted.

Run: .venv\\Scripts\\python.exe brands\\brainrot\\renderer\\export_zonkfruit.py data\\direction\\<id>.json --version V1 --short "Erdbeere keine Beere"
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from fn.config import STORAGE_DIR, mirror_dir, production_folder  # noqa: E402

_spec = importlib.util.spec_from_file_location("export_production_folder", ROOT / "scripts" / "export_production_folder.py")
_epf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_epf)
write_srt = _epf.write_srt

PLATFORMS = [("tiktok", "TikTok", "is_aigc"), ("instagram", "Instagram Reels", "is_ai_generated"), ("youtube", "YouTube Shorts", "containsSyntheticMedia")]


def script_md(plan: dict, date: str, short: str, man: dict | None) -> str:
    hook = next((h for h in plan["hook_candidates"] if h["id"] == plan["hook"]["id"]), {})
    beats = (man or {}).get("render", {}).get("beats") or plan["beats"]
    timing = {b["id"]: b for b in beats}
    rows = []
    for i, b in enumerate(plan["beats"], 1):
        d = b.get("data", {})
        shown = d.get("head") or d.get("headline") or d.get("merke") or d.get("cta") or (f"{d.get('word_a', '')}{d.get('word_b', '')}" if d.get("word_a") else "") or d.get("display", "")
        t = timing.get(b["id"], {})
        when = f"{t['start']:.1f}–{t['start'] + t['duration']:.1f} s" if t.get("start") is not None else "–"
        rows.append(f"| {i} | {when} | {b['function']} · {b['scene_type']} | {b['spoken']} | {shown.replace('*', '')} | {', '.join(b.get('source_ids', [])) or '–'} |")
    cands = "\n".join(f"- {h['id']} ({h['type']}, Score {h.get('score', '–')}): „{h['spoken']}“ · Bildschirm „{h['on_screen'].replace('*', '')}“ · Wahrheit {h['scores']['truth']}/5" for h in plan["hook_candidates"])
    srcs = "\n".join(f"- [{s['id']}] {s['title']} – {s['url']} (abgerufen {s['checked_at']})" for s in plan["sources"])
    unv = "\n".join(f"- {u}" for u in plan.get("unverified", [])) or "- keine"
    dur = (man or {}).get("render", {}).get("duration")
    return f"""# Skript – {short}

- Marke: Zonkfruit (`brainrot`), Figur Plümo (freigegeben 01.11.2026)
- Geplante Veröffentlichung: {date}
- Kanäle und Formate: TikTok, Instagram Reels, YouTube Shorts · 9:16, 1080 × 1920
- Länge: {f'{dur:.1f} s' if dur else 'Ziel 65–90 s'}
- Ziel des Videos: {plan['layout'].get('description', plan['title'])}
- Vorlage: Zonkfruit 1.0 (`02 Marke\\Tintora\\Vorlage Zonkfruit.md`); Plan `data\\direction\\{plan['video_id']}.json`
- Stimme: Gemini Flash TTS, Stimme {(man or {}).get('tts', {}).get('voice', 'Puck')}; Soundeffekte selbst erzeugt; keine Musik

## Hook (erste 3 Sekunden)

Gewählt: {hook.get('id')} – „{hook.get('spoken')}“ (Bildschirm: „{hook.get('on_screen', '').replace('*', '')}“). {plan['hook'].get('note', '')}

Kandidaten:
{cands}

## Ablauf

| # | Zeit | Funktion · Szenentyp | Text (Plümo spricht) | Einblendung | Quellen |
|---|---|---|---|---|---|
{chr(10).join(rows)}

## Abschluss und Loop

{plan['beats'][-1]['spoken']} Plümo steht wieder auf und hüpft an den Startplatz; das letzte Bild entspricht dem ersten Bild des Hooks (nahtloser Loop).

## Quellen

{srcs}

## Nicht verwendet (unbelegt)

{unv}
"""


def publish_md(plan: dict, post: dict | None, short: str, export_name: str, cover_name: str) -> str:
    texts = plan["layout"].get("platform_texts", {})
    srcs = "\n".join(f"- [{s['id']}] {s['url']} (abgerufen {s['checked_at']})" for s in plan["sources"])
    src_line = "Quellen: " + " · ".join(s["url"] for s in plan["sources"])
    parts = [f"# Veröffentlichung – {short}\n",
             "Je Kanal ein Abschnitt. Nichts ist veröffentlicht. KI-Kennzeichnung ist bei jedem Kanal Pflicht (Stefans Vorgabe). "
             "Nach dem Posten Link und Datum eintragen und den Status in `04 Redaktionsplan\\Redaktionsplan.csv` setzen.\n"]
    for key, name, flag in PLATFORMS:
        t = texts.get(key, {})
        title = t.get("title") or (post or {}).get("title") or plan["title"]
        desc = t.get("description") or plan["layout"].get("description", "")
        tags = " ".join(f"#{h}" for h in (t.get("hashtags") or plan["layout"].get("hashtags", [])))
        parts.append(f"""## {name}
- Datei: `04 Export\\{export_name}`
- Titel: {title}
- Beschreibung:

```
{desc}

{src_line}
KI-generiertes Video (Stimme und Grafik). Plümo ist eine erfundene Figur.
```
- Hashtags: {tags}
- KI-Kennzeichnung: `{flag}` = true
- Cover: `05 Thumbnail und Cover\\{cover_name}`
- Veröffentlicht am / Link:
""")
    parts.append("## Quellen\n\n" + srcs + "\n")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--version", default="V1")
    ap.add_argument("--short", required=True)
    ap.add_argument("--date", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--draft", default="", help="draft note, e.g. 'Entwurf Windows-Stimme': added to the export name and as a warning")
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    vid = plan["video_id"]
    ds = vid.split("-")[1]
    date = a.date or f"{ds[:4]}-{ds[4:6]}-{ds[6:8]}"
    folder = production_folder("brainrot", date, a.short)     # 05 Produktion\Tintora\<JJJJ-MM>\<Datum Kurztitel>
    if not folder.exists():
        folder.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(mirror_dir() / "_Vorlage Video", folder)
    suffix = f" ({a.draft})" if a.draft else ""
    export_name, cover_name = f"{date} {a.short} – 9x16{suffix}.mp4", f"{date} {a.short} – Cover.jpg"
    render = STORAGE_DIR / "direction" / f"{vid}-{a.version}"
    if not (render / "video.mp4").exists():
        print(f"no render in {render}")
        return 2
    dst = folder / "04 Export" / export_name
    if dst.exists() and not a.force:
        print(f"{dst} exists; use --force")
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
    post = json.loads((render / "post.json").read_text(encoding="utf-8")) if (render / "post.json").exists() else None
    (folder / "01 Skript" / "Skript.md").write_text(script_md(plan, date, a.short, man), encoding="utf-8")
    pub = publish_md(plan, post, a.short, export_name, cover_name)
    if a.draft:
        warn = (f"\n> **Nicht veröffentlichen: {a.draft}.** Die Stimme ist ein Platzhalter (Prüfbericht FAILED wegen `tts_provider_publishable`). "
                "Nach der Gemini-Vertonung neu rendern und exportieren.\n")
        pub = pub.replace("\n", "\n" + warn, 1)
    (folder / "Veröffentlichung.md").write_text(pub, encoding="utf-8")
    print(f"folder: {folder}\nexport: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
