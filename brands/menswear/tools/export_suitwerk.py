"""Copy a finished Suitwerk render into OneDrive\\Business\\05 Produktion\\Suitwerk\\<JJJJ-MM>\\<date> <short>\\
(fn.config.production_folder, from `_Vorlage Video`).

Suitwerk version of scripts/export_production_folder.py (that one carries Scutoria texts); same folder layout:
01 Skript\\Skript.md, 03 Schnittprojekt\\ (plan, manifest, report, post), 04 Export\\<date> <short> – 9x16.mp4,
05 Thumbnail und Cover\\, 06 Untertitel\\ (.srt + captions.json), Veröffentlichung.md. Nothing is published or deleted.

Run: .venv/Scripts/python.exe brands/menswear/tools/export_suitwerk.py data/direction/<id>.json --version V1 --short "<Kurztitel>"
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from fn.config import STORAGE_DIR, mirror_dir, production_folder  # noqa: E402

_spec = importlib.util.spec_from_file_location("export_production_folder", ROOT / "scripts" / "export_production_folder.py")
_epf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_epf)
write_srt = _epf.write_srt

CTA = "Folge Suitwerk für Herrenstil mit Blick fürs Detail."
PLATFORMS = [("TikTok", "is_aigc"), ("Instagram Reels", "is_ai_generated"), ("YouTube Shorts", "containsSyntheticMedia")]


def script_md(plan: dict, date: str, short: str, duration: float | None) -> str:
    hook = next((h for h in plan["hook_candidates"] if h["id"] == plan["hook"]["id"]), {})
    rows = []
    for i, b in enumerate(plan["beats"], 1):
        d = b.get("data", {})
        shown = d.get("headline") or d.get("question") or d.get("statement") or ""
        rows.append(f"| {i} | {b['function']} · {b['scene_type']} | {b['spoken']} | {shown} | {', '.join(b.get('source_ids', [])) or '–'} |")
    cands = "\n".join(f"- {h['id']} ({h['type']}): „{h['spoken']}“ · Bildschirm „{h['on_screen']}“ · Wahrheit {h['scores']['truth']}/5" for h in plan["hook_candidates"])
    srcs = "\n".join(f"- [{s['id']}] {s['title']} – {s['url']} (abgerufen {s['checked_at']})" for s in plan["sources"])
    unv = "\n".join(f"- {u}" for u in plan.get("unverified", [])) or "- keine"
    words = sum(len(b["spoken"].split()) for b in plan["beats"])
    kw = plan["layout"].get("format") == "kreidestrich"
    basis = ("Format „Kreidestrich“ (`02 Marke\\Suitwerk\\Format-Bibel.md`)" if kw
             else "Vorlage Suitwerk 1.0 (`02 Marke\\Suitwerk\\Vorlage Suitwerk.md`)")
    thread = ("Roter Faden: der Zuschneidetisch von oben, Schneiderkreide für jede Markierung, Fadenzähler für die Nahaufnahme; "
              f"Reihe „{plan['layout'].get('series_topic', '')}“." if kw else
              f"Roter Faden: ein Sakko als Linienillustration (Suitwerk-Szenen, `data.look = garment`), Statusleiste „{plan['layout'].get('status_bar', {}).get('file', '–')}“ mit dem Zustand des unteren Knopfs je Abschnitt.")
    close = ("Im Bild: Urteil in Kreide unter den Stoffmustern, Merksatz unterstrichen, Markenzeile mit Test für zuhause." if kw else
             "Im Bild wird der falsch geschlossene Knopf geöffnet, die Zugfalten verschwinden, Ring um den offenen Knopf.")
    return f"""# Skript – {short}

- Marke: Suitwerk (`menswear`), {basis}; Plan `{plan['video_id']}`, Sprache {plan.get('language', 'de')}
- Geplante Veröffentlichung: {date} (Kalender Woche 1; nichts veröffentlicht, Konten fehlen)
- Kanäle und Formate: TikTok, Instagram Reels, YouTube Shorts · 9:16, 1080 × 1920
- Länge: {f'{duration:.1f} s' if duration else 'Ziel 65–90 s'} · {words} Wörter
- Ziel des Videos: {plan['layout'].get('description', plan['title'])}

## Hook (erste 3 Sekunden)

Gewählt: {hook.get('id')} – „{hook.get('spoken')}“ (Bildschirm: „{hook.get('on_screen')}“). {plan['hook'].get('note', '')}

Kandidaten:
{cands}

## Ablauf
| # | Funktion · Szenentyp | Text / Sprecher | Einblendung | Quellen |
|---|---|---|---|---|
{chr(10).join(rows)}

{thread}

## Abschluss und Handlungsaufforderung

{plan['beats'][-1]['spoken']} {close}

## Quellen

{srcs}

## Nicht verwendet (unbelegt oder außerhalb des Themas)

{unv}
"""


def publish_md(plan: dict, post: dict | None, short: str, export_name: str, cover_name: str, man: dict | None = None) -> str:
    title = (post or {}).get("title") or plan["title"]
    desc = (post or {}).get("description") or plan["layout"].get("description", "")
    tags = (post or {}).get("hashtags") or plan["layout"].get("hashtags", [])
    tag_line = " ".join(f"#{t}" for t in tags)
    tts = (man or {}).get("tts") or {}
    parts = [f"# Veröffentlichung – {short}\n",
             "Je Kanal ein Abschnitt. Nichts ist veröffentlicht; Suitwerk-Konten gibt es noch nicht. KI-Kennzeichnung ist bei jedem Kanal Pflicht. "
             "Keine Markennamen, keine Affiliate-Links, keine Produktempfehlung.\n",
             f"Stimme: {tts.get('provider', '?')} `{tts.get('model', '?')}`, Sprecher {tts.get('voice', '?')}.\n"]
    if "Entwurf" in export_name:
        parts.append("**Achtung:** Die Exportdatei ist ein Entwurf mit Windows-Entwurfsstimme (SAPI) und darf nicht veröffentlicht werden. "
                     "Vertonung mit Gemini offen (Tageskontingent am 30.10.2026 erschöpft); danach neu rendern und exportieren.\n")
    for name, flag in PLATFORMS:
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
    parts.append("## Quellen\n\n" + "\n".join(f"- [{s['id']}] {s.get('label') or s['title']} – {s['url']} (abgerufen {s['checked_at']})" for s in plan["sources"]) + "\n")
    return "\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--version", default="V1")
    ap.add_argument("--short", required=True)
    ap.add_argument("--date", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--draft", default="", help="marker in the export file name, e.g. 'Entwurf SAPI' for a non-publishable voice")
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    vid = plan["video_id"]
    date = a.date or f"{vid.split('-')[1][:4]}-{vid.split('-')[1][4:6]}-{vid.split('-')[1][6:8]}"
    folder = production_folder(plan["brand_id"], date, a.short)
    if not folder.exists():
        folder.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(mirror_dir() / "_Vorlage Video", folder)
    tag = f" ({a.draft})" if a.draft else ""
    export_name, cover_name = f"{date} {a.short} – 9x16{tag}.mp4", f"{date} {a.short} – Cover.jpg"
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
    (folder / "01 Skript" / "Skript.md").write_text(script_md(plan, date, a.short, man.get("render", {}).get("duration")), encoding="utf-8")
    (folder / "Veröffentlichung.md").write_text(publish_md(plan, post, a.short, export_name, cover_name, man), encoding="utf-8")
    print(f"folder: {folder}\nexport: {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
