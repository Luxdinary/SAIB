"""Thumbnail drafts for all ten videos: 3 backgrounds × DE/EN, text from the approved scripts (Thumbnail-Text).
Output: storage/longform/thumbs/<NN>_<lang>_<a|b|c>.png and a contact sheet thumbs/_kontaktbogen.jpg (with a
168 px preview row per video for the readability rule). Skips backgrounds that are not downloaded yet.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[2] / "src"))

from fn.config import STORAGE_DIR  # noqa: E402
from longform.compose import LIB  # noqa: E402
from longform.thumbnail import build  # noqa: E402

TEXT = {  # approved "Thumbnail-Text" lines of SKRIPTE/NN-*.md, one accent word marked with *
    "01": ("Womit fangen *KI-Regeln* an?", "Where do *AI rules* start?"),
    "02": ("*Noch nicht*, mit Termin", "*Not yet*, with a date"),
    "03": ("Sieben Dokumente, vier *Marker*", "Seven documents, four *markers*"),
    "04": ("Im Zweifel *nichts* eingeben", "In doubt, enter *nothing*"),
    "05": ("Kein Zertifikat. Ein *Nachweis*.", "No certificate. A *record*."),
    "06": ("Wonach sie *zuerst* fragen", "What they ask *first*"),
    "07": ("Drei Fälle, eine *Ausnahme*", "Three cases, one *exception*"),
    "08": ("*72 Stunden*. Wen anrufen.", "*72 hours*. Who to call."),
    "09": ("Sieben *Fragen* je Tool", "Seven *questions* per tool"),
    "10": ("Betrifft uns *NIS2*?", "Does *NIS2* apply to us?"),
}
STAND = {"de": "Stand Nov. 2026", "en": "As of Nov 2026"}


def main() -> int:
    out = STORAGE_DIR / "longform" / "thumbs"
    made = []
    only = set(sys.argv[1:])
    for num, (de, en) in TEXT.items():
        if only and num not in only:
            continue
        for v in "abc":
            bg = LIB / "yt" / f"thumb_{num}_{v}.png"
            if not bg.exists():
                continue
            for lang, text in (("de", de), ("en", en)):
                dst = out / f"{num}_{lang}_{v}.png"
                build(num, text, str(bg), STAND[lang], dst)
                made.append(dst)
    from PIL import Image
    if made:
        W, H = 640, 360
        rows = sorted({p.name[:5] for p in made})
        sheet = Image.new("RGB", (W * 3 + 180, H * len(rows)), "black")
        for r, key in enumerate(rows):
            for c, v in enumerate("abc"):
                p = out / f"{key}_{v}.png"
                if p.exists():
                    im = Image.open(p).convert("RGB")
                    sheet.paste(im.resize((W, H)), (c * W, r * H))
                    if c == 0:
                        sheet.paste(im.resize((168, 94)), (W * 3 + 6, r * H + 10))
        sheet.save(out / "_kontaktbogen.jpg", quality=85)
    print(f"{len(made)} thumbnails in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
