"""Export a finished Scutoria long video (DE and EN) into OneDrive\\Business\\05 Produktion\\<Datum> <Kurztitel>\\.

Copies the 16:9 videos, the reels, thumbnails and SRT files, writes Skript.md from the plans (new text marked) and
Veröffentlichung.md with title, description (chapters from the render, sources from the plan, free offers and
toolkit lines from the approved script metadata, standard paragraphs from VORLAGEN/METADATEN.md), tags and upload
notes per channel. Missing renders are listed as open, never invented.

  .venv\\Scripts\\python.exe brands\\ai_security\\longform\\export_long.py --slug 01-ai-rules-start --date 2026-11-17 --short "KI-Regeln"
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from fn.config import STORAGE_DIR, mirror_dir, production_folder  # noqa: E402

SCRIPTS = Path(r"C:\Users\Stefa\OneDrive\scutoria\marketing\youtube\SKRIPTE")
TEMPLATE = mirror_dir() / "_Vorlage Video"
MARK = {"de": {"fakt": "Fakt", "auslegung": "Auslegung", "unsicher": "Unsicher", "luecke": "Lücke", "beispiel": "Beispiel"},
        "en": {"fakt": "Fact", "auslegung": "Interpretation", "unsicher": "Uncertain", "luecke": "Gap", "beispiel": "Example"}}
STD = {
    "de": {"not": "Was dieses Video nicht ist: Rechtsberatung. Es ist eine Information auf Grundlage der unten genannten Quellen, am Original gelesen, mit Abrufdatum. Ihr Betrieb entscheidet selbst.",
           "about": "Über diesen Kanal\nScutoria macht datierte Dokument-Toolkits für Betriebe ohne IT-Abteilung, bis etwa fünfzig Beschäftigte, überall in der EU. Die Marke spricht; keine Person tritt auf. Die Stimme in diesem Video ist synthetisch (Google Gemini Text-to-Speech); das Skript wurde mit einem KI-Tool entworfen und von uns vor der Veröffentlichung Satz für Satz geprüft. Bild und Hintergrundclips sind computer- beziehungsweise KI-generiert (Higgsfield). Redaktionell verantwortlich: siehe Impressum.\n\nImpressum: https://scutoria.com/de/impressum\nDatenschutz: https://scutoria.com/de/datenschutz\nEnglish: https://scutoria.com/",
           "chapters": "Kapitel", "sources": "Quellen", "pin": "Die Quellen mit Abrufdatum stehen in der Beschreibung. Die Stimme ist synthetisch; das Skript wurde von uns vor der Veröffentlichung geprüft. Fragen zum eigenen Fall: Wir geben keine Rechtsberatung und beantworten hier keine Einzelfälle. Memo und Tools auf scutoria.com sind frei."},
    "en": {"not": "What this video is not: legal advice. It is information based on the sources listed below, read at the originals with the retrieval date next to each. Your business decides for itself.",
           "about": "About this channel\nScutoria makes dated document toolkits for businesses without an IT department, up to about fifty staff, anywhere in the EU. The brand speaks; no person appears. The voice in this video is synthetic (Google Gemini text-to-speech); the script was drafted with an AI tool and checked by us sentence by sentence before publication. Graphics and background clips are computer- or AI-generated (Higgsfield). Editorially responsible: see the legal notice.\n\nLegal notice: https://scutoria.com/legal\nPrivacy: https://scutoria.com/privacy\nDeutsch: https://scutoria.com/de/",
           "chapters": "Chapters", "sources": "Sources", "pin": "Sources with retrieval date are in the description. The voice is synthetic; the script was checked by us before publication. Questions about your own case: we do not give legal advice, and we answer no individual cases here. The memo and the tools on scutoria.com are free."},
}


def safe_name(title: str) -> str:
    """Title as part of a Windows file name: letters, digits, spaces and hyphens only."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w äöüÄÖÜß-]", "", title)).strip()


def script_meta(slug: str, lang: str) -> dict:
    """First sentence, free offers and toolkit block, tags and thumbnail text from the approved script header."""
    p = SCRIPTS / f"{slug}.{lang}.md"
    t = p.read_text(encoding="utf-8") if p.exists() else ""
    desc = re.search(r"```\n(.*?)```", t, re.S)
    body = desc.group(1) if desc else ""
    first = body.strip().split("\n\n")[0] if body else ""
    free = re.search(r"\n((?:Frei auf scutoria\.com|Free on scutoria\.com).*?)\n\[", body, re.S)
    tags = re.search(r"^Tags:\s*(.+)$", t, re.M)
    thumb = re.search(r"^Thumbnail-Text[^:]*:\s*(.+)$", t, re.M)
    return {"first": first, "free": (free.group(1).strip() if free else ""), "tags": tags.group(1).strip() if tags else "",
            "thumb": thumb.group(1).strip() if thumb else ""}


def script_md(plan: dict) -> str:
    lang = plan["lang"]
    src = {s["id"]: s["label"] for s in plan["sources"]}
    out = [f"# {plan['title']}", "", plan.get("version", ""), "",
           "Neue, noch nicht freigegebene Stellen sind mit „(neu, zur Freigabe)“ markiert." if lang == "de" else
           "New passages awaiting approval are marked “(new, for approval)”.", ""]
    for ch in plan["chapters"]:
        out += [f"## {ch.get('num') or '0'} {ch['title']}", ""]
        for k, sc in enumerate(ch["scenes"]):
            tag = (" (neu, zur Freigabe)" if lang == "de" else " (new, for approval)") if sc.get("new") else ""
            out.append(f"[{ch['id']}s{k} · {sc['type']}{' · ' + sc['bg'] if sc.get('bg') else ''}]{tag}")
            for p in sc["say"]:
                if p.get("marker"):
                    out.append(f"[MARKER: {MARK[lang][p['marker']]}]")
                out.append(p["text"])
                if p.get("source"):
                    out.append(f"[{'QUELLE' if lang == 'de' else 'SOURCE'}: {src.get(p['source'], p['source'])}]")
                out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--short", required=True)
    ap.add_argument("--langs", default="de,en")
    a = ap.parse_args()
    folder = production_folder("ai_security", a.date, a.short)     # 05 Produktion\Scutoria\<JJJJ-MM>\<Datum Kurztitel>
    if not folder.exists():
        folder.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(TEMPLATE, folder)
    num = a.slug.split("-")[0]
    pub = [f"# Veröffentlichung – {a.short} (YouTube-Langvideo {num})", "",
           "Stand: Entwurf, nicht veröffentlicht. Stefan gibt jedes Video vor der Veröffentlichung frei. Upload-Einstellungen: "
           "`OneDrive\\scutoria\\marketing\\youtube\\VORLAGEN\\METADATEN.md` (KI-Nutzung „Ja“, nicht für Kinder, Kommentare halten, Endscreen 20 s).", ""]
    open_points = []
    for lang in a.langs.split(","):
        plan = json.loads((HERE / "plans" / f"{a.slug}.{lang}.json").read_text(encoding="utf-8"))
        vid = plan["video_id"]
        st = STORAGE_DIR / "longform" / vid
        meta = script_meta(a.slug, lang)
        L = lang.upper()
        (folder / "01 Skript" / f"Skript {L}.md").write_text(script_md(plan), encoding="utf-8")
        name = f"{a.date} {a.short}{'' if lang == 'de' else ' EN'} – YouTube 16x9.mp4"
        if (st / "video.mp4").exists():
            shutil.copy2(st / "video.mp4", folder / "04 Export" / name)
        else:
            open_points.append(f"{L}: Langvideo noch nicht gerendert ({st / 'video.mp4'})")
        if (st / "captions.srt").exists():
            shutil.copy2(st / "captions.srt", folder / "06 Untertitel" / f"{a.date} {a.short} {L}.srt")
        reels = []
        for r in plan.get("reels", []):
            rv = st / "reels" / r["id"] / "video.mp4"
            rn = f"{a.date} {a.short}{'' if lang == 'de' else ' EN'} – Reel {r['id'][1:]} {safe_name(r['title'])} 9x16.mp4"
            if rv.exists():
                shutil.copy2(rv, folder / "04 Export" / rn)
            else:
                open_points.append(f"{L}: Reel {r['id']} noch nicht gerendert")
            reels.append((r, rn))
        for th in sorted((STORAGE_DIR / "longform" / "thumbs").glob(f"{num}_{lang}_*.png")):
            shutil.copy2(th, folder / "05 Thumbnail und Cover" / th.name)
        chapters = (st / "chapters.txt").read_text(encoding="utf-8").strip() if (st / "chapters.txt").exists() else "(Zeitmarken nach dem Render)"
        sources = "\n".join(s["label"] for s in plan["sources"])
        desc = "\n\n".join(x for x in [meta["first"], f"{STD[lang]['chapters']}\n{chapters}", STD[lang]["not"],
                                         f"{STD[lang]['sources']}\n{sources}", meta["free"], STD[lang]["about"]] if x)
        pub += [f"## YouTube {L}", f"- Datei: `04 Export\\{name}`", f"- Titel: {plan['title']}", f"- Thumbnail: `05 Thumbnail und Cover\\{num}_{lang}_*.png` (Entwürfe, Stefan wählt einen)",
                f"- Untertitel: `06 Untertitel\\{a.date} {a.short} {L}.srt`", f"- Tags: {meta['tags']}", f"- Angepinnter Kommentar: {STD[lang]['pin']}",
                "- Veröffentlicht am / Link:", "", "Beschreibung:", "```", desc, "```", ""]
        pub += [f"## Reels {L} (TikTok, Instagram Reels, YouTube Shorts)", ""]
        for r, rn in reels:
            cap = (f"{r['title']}. Aus unserem Video „{plan['title']}“ auf YouTube. Quellen in der Videobeschreibung. KI-generiert (Stimme und Grafik). Keine Rechtsberatung."
                   if lang == "de" else f"{r['title']}. From our video “{plan['title']}” on YouTube. Sources in the video description. AI-generated (voice and graphics). Not legal advice.")
            pub += [f"### Reel {r['id'][1:]}: {r['title']}", f"- Datei: `04 Export\\{rn}`", f"- Text: {cap}",
                    "- Hashtags: #kisicherheit #datenschutz #kleinunternehmen" if lang == "de" else "- Hashtags: #aisecurity #dataprotection #smallbusiness",
                    "- KI-Kennzeichnung der Plattform einschalten (TikTok „KI-generiert“, Instagram „KI-Info“, YouTube „veränderte oder synthetische Inhalte“).",
                    "- Veröffentlicht am / Link:", ""]
    if open_points:
        pub += ["## Offen", *[f"- {p}" for p in open_points], ""]
    (folder / "Veröffentlichung.md").write_text("\n".join(pub), encoding="utf-8")
    print(folder)
    for p in open_points:
        print("open:", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
