"""Baut je Marke eine statische Linkseite mit Impressum (Ordner 03 Kanäle\\Linkseite).

Quelle der Texte: Profilpaket.md je Marke (Instagram-Bios DE und EN, Handle, Anzeigename),
Farben aus brands\\<id>\\brand.yaml im Code-Ordner, Impressum-Angaben aus impressum.json.
Aufruf: python build_linkseiten.py   (schreibt <marke>.html und index.html neben dieses Skript)
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
KANAELE = HERE.parent
BRANDS_DIR = Path(r"C:\Automation\faceless-network\brands")

MARKEN = [  # Anzeigename, Ordner in 03 Kanäle, Marken-ID im Code, Slug
    ("Scutoria", "Scutoria", "ai_security", "scutoria"),
    ("Promptwerk", "Promptwerk", "claude_workflows", "promptwerk"),
    ("Tintora", "Tintora", "brainrot", "tintora"),
    ("Dewlane", "Dewlane", "beauty", "dewlane"),
    ("Revlore", "Revlore", "engines", "revlore"),
    ("Gigastruct", "Gigastruct", "megaconstruction", "gigastruct"),
    ("Suitwerk", "Suitwerk", "menswear", "suitwerk"),
    ("Frontlore", "Frontlore", "military_history", "frontlore"),
    ("Gritwerk", "Gritwerk", "motivation", "gritwerk"),
]


def profil(ordner: str) -> dict:
    t = (KANAELE / ordner / "Profilpaket.md").read_text(encoding="utf-8")
    handle = re.search(r"^\| Handle[^|]*\|\s*(@[\w.]+)", t, re.M).group(1)
    # Instagram-Abschnitt: die längeren Bios (150 Zeichen)
    ig = t.split("## Instagram", 1)[1].split("\n## ", 1)[0]
    de = re.search(r"Bio DE \([^)]*\):\s*(.+)", ig).group(1).strip()
    en = re.search(r"Bio EN \([^)]*\):\s*(.+)", ig).group(1).strip()
    kids = "speziell für Kinder" in t
    return {"handle": handle, "de": de, "en": en, "kids": kids}


def farben(brand_id: str) -> dict:
    out = {"bg": "#0b1120", "text": "#e9eef8", "accent": "#4f8cff"}
    f = BRANDS_DIR / brand_id / "brand.yaml"
    if f.exists():
        t = f.read_text(encoding="utf-8")
        for k in out:
            m = re.search(rf"^\s*{k}\s*:\s*['\"]?(#[0-9A-Fa-f]{{6}})", t, re.M)
            if m:
                out[k] = m.group(1)
    return out


def impressum_html(imp: dict, marke: str) -> str:
    e = html.escape
    zeilen = "<br>".join(e(z) for z in imp["anschrift"])
    offen = "".join(f"<li>{e(x)}</li>" for x in imp["offen"])
    return f"""
<section id="impressum" class="imp">
  <h2>Impressum und Offenlegung</h2>
  <p><strong>Medieninhaber und Diensteanbieter:</strong><br>{zeilen}<br>E-Mail: <a href="mailto:{e(imp['email'])}">{e(imp['email'])}</a></p>
  <p><strong>Unternehmensgegenstand:</strong> {e(imp['gegenstand'])}</p>
  <p><strong>Grundlegende Richtung:</strong> {e(imp['richtung'].replace('{marke}', marke))}</p>
  {f'<ul class="offen">{offen}</ul>' if imp['offen'] else ''}
  <p><strong>KI-Hinweis:</strong> {e(imp['ki_de'])}</p>
  <p lang="en"><strong>Legal notice (English):</strong> Media owner and service provider as above. {e(imp['ki_en'])}</p>
</section>"""


def seite(name: str, slug: str, p: dict, c: dict, imp: dict) -> str:
    e = html.escape
    h = p["handle"].lstrip("@")
    links = [
        ("TikTok", f"https://www.tiktok.com/@{h}"),
        ("Instagram", f"https://www.instagram.com/{h}/"),
        ("YouTube", f"https://www.youtube.com/@{h}"),
    ]
    knoepfe = "".join(f'<a class="btn" href="{e(u)}" rel="noopener">{e(n)} <span>{e(p["handle"])}</span></a>' for n, u in links)
    kinder = ('<p class="hint">Familienserie. Auf YouTube als „speziell für Kinder“ eingestuft. '
              'Auf TikTok und Instagram richtet sich der Kanal an Familien, nicht an Kinder unter 13.</p>') if p["kids"] else ""
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(name)} · Links und Impressum</title>
<meta name="robots" content="noindex">
<style>
:root {{ --bg:{c['bg']}; --text:{c['text']}; --accent:{c['accent']}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
main {{ max-width:520px; margin:0 auto; padding:40px 16px 56px; }}
h1 {{ font-size:28px; margin:0 0 6px; letter-spacing:.02em; }}
.lead {{ margin:0 0 4px; }}
.lead[lang=en] {{ opacity:.75; font-size:14px; margin-bottom:24px; }}
.btn {{ display:flex; justify-content:space-between; align-items:center; gap:12px; padding:14px 16px; margin:10px 0;
       border:1.5px solid var(--accent); border-radius:10px; color:var(--text); text-decoration:none; font-weight:600; }}
.btn span {{ font-weight:400; opacity:.75; font-size:14px; }}
.btn:hover, .btn:focus-visible {{ background:var(--accent); color:var(--bg); }}
.hint {{ font-size:14px; opacity:.8; }}
.jump {{ display:inline-block; margin-top:18px; color:var(--accent); }}
.imp {{ margin-top:40px; padding-top:20px; border-top:1px solid color-mix(in srgb, var(--text) 25%, transparent); font-size:14px; }}
.imp h2 {{ font-size:17px; }}
.imp a {{ color:var(--accent); }}
.offen {{ color:var(--accent); }}
</style>
</head>
<body>
<main>
  <h1>{e(name)}</h1>
  <p class="lead">{e(p['de'])}</p>
  <p class="lead" lang="en">{e(p['en'])}</p>
  {knoepfe}
  {kinder}
  <a class="jump" href="#impressum">Impressum</a>
  {impressum_html(imp, name)}
</main>
</body>
</html>
"""


def main() -> None:
    imp = json.loads((HERE / "impressum.json").read_text(encoding="utf-8"))
    eintraege = []
    for name, ordner, bid, slug in MARKEN:
        p = profil(ordner)
        (HERE / f"{slug}.html").write_text(seite(name, slug, p, farben(bid), imp), encoding="utf-8")
        eintraege.append(f'<li><a href="{slug}.html">{html.escape(name)}</a> {html.escape(p["handle"])}</li>')
    (HERE / "index.html").write_text(
        "<!doctype html><html lang=de><meta charset=utf-8><meta name=viewport content='width=device-width, initial-scale=1'>"
        "<title>Linkseiten Vorschau</title><body style='font:16px system-ui;max-width:520px;margin:40px auto;padding:0 16px'>"
        "<h1>Linkseiten (Vorschau, nicht veröffentlicht)</h1><ul>" + "".join(eintraege) + "</ul></body></html>",
        encoding="utf-8")
    print("geschrieben:", len(eintraege), "Seiten + index.html")


if __name__ == "__main__":
    main()
