"""Build week-1 plans in the format "Nahaufnahme" from the existing week-1 plans (Dewlane, 02.11.2026).

The spoken text, sources, hook candidates and description of every old plan stay unchanged (checked on 01.11.2026);
only the scenes are rebuilt with the general nh_* types (nahaufnahme/scenes.py) and a neutral product per topic.
Topics that fit the format badly (Format-Bibel, section 9) are skipped and listed for Stefan.

    .venv\\Scripts\\python.exe brands\\beauty\\nahaufnahme\\convert_w1.py        -> data/direction/beauty-<topic>-<lang>.N1.json
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "data" / "direction"

SERIES = {
    "lupe": {"de": "Unter der Lupe", "en": "Close-up"},
    "sonne": {"de": "Unter der Lupe · Sonnenschutz", "en": "Close-up · Sunscreen"},
    "mythos": {"de": "Direkter Vergleich · Mythos", "en": "Side by side · Myth"},
    "werbung": {"de": "Direkter Vergleich · Werbeaussage", "en": "Side by side · Claim"},
    "wissen": {"de": "Beauty verständlich", "en": "Beauty explained"},
}
KICK = {
    "problem": {"de": "Worum es geht", "en": "The issue"},
    "explanation": {"de": "Unter der Lupe", "en": "Close-up"},
    "demonstration": {"de": "Im Vergleich", "en": "Side by side"},
    "insight": {"de": "Laut Quelle", "en": "Per source"},
    "benefit": {"de": "Im Alltag", "en": "Everyday use"},
    "close": {"de": "Merksatz", "en": "Key point"},
}

# topic: series, product per language (neutral, invented), lens word(s), closing question per language
SPEC = {
    "20261109-1": {"series": "lupe", "product": {"kind": "jar", "line1": {"de": "CREME", "en": "CREAM"}}, "zoom": "AQUA",
                   "q": {"de": "Was steht bei dir in Zeile 1?", "en": "What's in line 1 on yours?"}},
    "20261109-2": {"series": "wissen", "product": {"kind": "bottle", "line1": {"de": "LOTION", "en": "LOTION"}},
                   "zoom": {"de": "Kosmetik?", "en": "Cosmetic?"}, "q": {"de": "Pflege oder Heilung auf der Packung?", "en": "Does your pack promise care or cure?"}},
    "20261109-3": {"series": "mythos", "product": {"kind": "jar", "line1": {"de": "CREME", "en": "CREAM"}}, "zoom": "PARABEN",
                   "q": {"de": "Welche Parabene stehen auf deiner Liste?", "en": "Which parabens are on your list?"}},
    "20261110-3": {"series": "sonne", "product": {"kind": "tube", "line1": {"de": "SONNENSCHUTZ", "en": "SUNSCREEN"}, "line2": {"de": "LSF", "en": "SPF"}, "big": "30"},
                   "zoom": {"de": "LSF 30", "en": "SPF 30"}, "q": {"de": "Welche Kategorie steht auf deiner Tube?", "en": "Which category is on your tube?"}},
    "20261111-1": {"series": "lupe", "product": {"kind": "jar", "line1": {"de": "CREME", "en": "CREAM"}}, "zoom": {"de": "7 Angaben", "en": "7 items"},
                   "q": {"de": "Findest du alle sieben auf der Creme?", "en": "Can you find all seven on yours?"}},
    "20261111-3": {"series": "mythos", "product": {"kind": "spray", "line1": {"de": "DEO", "en": "DEO"}}, "zoom": "Aluminium",
                   "q": {"de": "Steht Aluminium auf deinem Deo?", "en": "Does your deo list aluminium?"}},
    "20261112-1": {"series": "werbung", "product": {"kind": "dropper", "line1": {"de": "SERUM", "en": "SERUM"}, "big": "X"},
                   "zoom": {"de": "mit X", "en": "with X"}, "q": {"de": "Was steht groß auf deiner Packung?", "en": "What's in big letters on your pack?"}},
    "20261112-3": {"series": "sonne", "product": {"kind": "tube", "line1": {"de": "SONNENSCHUTZ", "en": "SUNSCREEN"}, "line2": {"de": "LSF", "en": "SPF"}, "big": "30"},
                   "zoom": "UVA", "q": {"de": "Steht UVA auf deiner Tube?", "en": "Does your tube mention UVA?"}},
    "20261113-1": {"series": "lupe", "product": {"kind": "jar", "line1": {"de": "CREME", "en": "CREAM"}, "big": "12M"}, "zoom": "12M",
                   "q": {"de": "Wie viele Monate zeigt dein Tiegel?", "en": "How many months does your jar show?"}},
    "20261114-1": {"series": "werbung", "product": {"kind": "bottle", "line1": {"de": "LOTION", "en": "LOTION"}},
                   "zoom": {"de": "Pflicht", "en": "Required"}, "q": {"de": "Wirbt deine Packung mit einer Pflicht?", "en": "Does your pack sell a legal duty?"}},
    "20261114-3": {"series": "sonne", "product": {"kind": "tube", "line1": {"de": "SONNENSCHUTZ", "en": "SUNSCREEN"}, "line2": {"de": "LSF", "en": "SPF"}, "big": "50"},
                   "zoom": "100 %", "q": {"de": "Was verspricht deine Sonnencreme?", "en": "What does your sunscreen promise?"}},
    "20261115-1": {"series": "lupe", "product": {"kind": "jar", "line1": {"de": "CREME", "en": "CREAM"}}, "zoom": {"de": "30 Monate", "en": "30 months"},
                   "q": {"de": "Sanduhr oder Tiegel auf deiner Creme?", "en": "Hourglass or open jar on yours?"}},
    "20261115-3": {"series": "sonne", "product": {"kind": "tube", "line1": {"de": "MINERALISCH", "en": "MINERAL"}, "line2": {"de": "LSF", "en": "SPF"}, "big": "30"},
                   "zoom": "(nano)", "q": {"de": "Steht (nano) auf deiner Liste?", "en": "Does your list say (nano)?"}},
}
SKIPPED = ["20261110-1", "20261110-2", "20261111-2", "20261112-2", "20261113-2", "20261113-3", "20261114-2", "20261115-2"]
OLD_FILE = {("20261109-1", "de"): "beauty-20261105-1-de"}    # the DE INCI plan is the test video plan
ICON_MAP = {"doc": "doc", "shield": "shield", "hourglass": "hourglass", "drop": "drop", "lens": "lens", "book": "doc", "scale": "check"}


def _l(v, lang):
    return v.get(lang, v.get("de")) if isinstance(v, dict) else v


def product(spec: dict, lang: str, *, text: bool = True) -> dict:
    p = spec["product"]
    out = {"kind": p["kind"]}
    if text:
        for k in ("line1", "line2", "big"):
            if k in p:
                out[k] = _l(p[k], lang)
    return out


def inci_beats(old: dict, lang: str, P: dict) -> list[dict]:
    """The INCI plans use the old Q1 scene types; their scenes are rebuilt by hand from the same spoken text."""
    b = {x["id"]: x for x in old["beats"]}
    de = lang == "de"
    D = lambda x, y: x if de else y  # noqa: E731
    data = {
        "b1": ("nh_hook", {"question": b["b1"]["data"]["question"], "badge": b["b1"]["data"]["badge"]}),
        "b2": ("nh_facts", {"headline": b["b2"]["data"]["headline"], "zoom": "AQUA",
                            "doc": {"act": D("Glossar (EU) 2019/701", "Glossary (EU) 2019/701"), "ref": D("gemeinsame Bezeichnungen", "common ingredient names")},
                            "rows": [{"text": D("Liste mit der Überschrift Ingredients", "a list headed Ingredients")},
                                     {"text": D("Namen aus einem EU-Glossar", "names from an EU glossary")},
                                     {"text": D("AQUA = Wasser", "AQUA = water"), "at": "@Aqua"}]}),
        "b3": ("nh_list", {"headline": b["b3"]["data"]["headline"], "caption": D("Art. 19 VO 1223/2009: Gewicht beim Hinzufügen", "Reg. (EC) 1223/2009, Art. 19: weight when added"),
                           "rows": [{"label": D("Zeile 1", "Line 1"), "value": D("am meisten", "most"), "at": "@vorne" if de else "@top"},
                                    {"label": D("Zeile 2", "Line 2"), "value": D("weniger", "less")},
                                    {"label": D("Zeile 3", "Line 3"), "value": D("weniger", "less")},
                                    {"label": D("Zeile 4", "Line 4"), "value": "…"}]}),
        "b4": ("nh_versus", {"headline": b["b4"]["data"]["headline"],
                             "left": {"tag": D("über 1 %", "over 1 %"), "title": D("nach Gewicht", "by weight"), "rows": [{"text": D("Reihenfolge = Menge", "order = amount")}]},
                             "right": {"tag": D("unter 1 %", "under 1 %"), "title": D("Reihenfolge frei", "any order"),
                                       "rows": [{"text": D("beliebige Reihenfolge", "can follow in any order"), "at": "@beliebiger" if de else "@any"},
                                                {"text": D("Grenze steht nicht drauf", "line not shown on pack"), "mark": "open", "at": "@Grenze" if de else "@line"}]}}),
        "b5": ("nh_facts", {"headline": b["b5"]["data"]["headline"], "zoom": "INCI", "flip": True,
                            "doc": {"act": D("VO (EG) 1223/2009", "Reg. (EC) 1223/2009"), "ref": "Art. 19"},
                            "rows": [{"text": D("welche Stoffe enthalten sind", "which substances are in it"), "mark": "fact"},
                                     {"text": D("was mengenmäßig vorne liegt", "what's there in the largest amounts"), "mark": "fact"},
                                     {"text": D("keine genauen Prozentwerte", "no exact percentages"), "mark": "gap", "at": "@Prozent" if de else "@percentages"},
                                     {"text": D("nicht, ob es zu deiner Haut passt", "not whether it suits your skin"), "mark": "gap", "at": "@Und" if de else "@whether"}]}),
        "b6": ("nh_steps", {"headline": b["b6"]["data"]["headline"],
                            "items": [dict(title=i["title"], sub=i["sub"], icon=ic, at="@" + i["at"][2:]) for i, ic in
                                      zip(b["b6"]["data"]["items"], ("lens", "drop", "doc"))]}),
    }
    beats = []
    for x in old["beats"]:
        nb = {k: v for k, v in x.items() if k not in ("data", "overlay", "scene_type")}
        if x["id"] in data:
            nb["scene_type"], nb["data"] = data[x["id"]][0], dict(data[x["id"]][1])
        else:
            nb["scene_type"], nb["data"] = "nh_close", {}
        beats.append(nb)
    return beats


def convert(topic: str, lang: str) -> dict:
    spec = SPEC[topic]
    name = OLD_FILE.get((topic, lang), f"beauty-{topic}-{lang}")
    old = json.loads((DIR / f"{name}.json").read_text(encoding="utf-8"))
    P = product(spec, lang)
    new = copy.deepcopy(old)
    new["video_id"] = f"beauty-{topic}-{lang}"
    new["notes"] = (f"Woche 1 im Format \"Nahaufnahme\" (Format-Bibel 1.0, freigegeben 02.11.2026), erzeugt mit "
                    f"brands/beauty/nahaufnahme/convert_w1.py aus {name}.json: Sprechtext, Quellen und Hook unverändert, Szenen neu "
                    f"mit neutralem, erfundenem Produkt ({spec['product']['kind']}), nur Code-Grafik. Alte Notiz: {old.get('notes', '')}")
    lay = {k: v for k, v in old["layout"].items() if k not in ("status_bar", "status_y", "explainer")}
    lay.update({"format": "nahaufnahme", "explainer": False, "outro": False, "tail_seconds": 2.4, "progress_y": 1548, "ai_label_bottom_px": 430,
                "zone_top": 330, "zone_h": 810, "zone_lower_right_px": 930})   # R5: stage 40 px lower, captions from y ~1310
    new["layout"] = lay
    new["assets"] = {"folder": "assets/clips", "background": {}, "hero": {}, "scrim": 0.0,
                     "note": "Hintergrund aus dem LAYER des Formats Nahaufnahme, keine Clips, keine KI-Bilder."}
    if topic == "20261109-1":
        beats = inci_beats(old, lang, P)
    else:
        beats, n_facts = [], 0
        for x in old["beats"]:
            d, st = x.get("data") or {}, x["scene_type"]
            nb = {k: v for k, v in x.items() if k not in ("data", "overlay", "scene_type")}
            if st == "dw_hook":
                nb["scene_type"], nb["data"] = "nh_hook", {"question": d.get("question", ""), "badge": d.get("badge", "")}
            elif st == "dw_facts":
                n_facts += 1
                z = spec.get("zoom2") if n_facts > 1 and spec.get("zoom2") else spec["zoom"]
                nb["scene_type"], nb["data"] = "nh_facts", {"headline": d.get("headline", ""), "zoom": _l(z, lang), "flip": n_facts > 1,
                                                             "doc": d.get("doc") or {}, "rows": d.get("rows", [])}
            elif st == "dw_bars":
                nb["scene_type"], nb["data"] = "nh_list", {"headline": d.get("headline", ""), "caption": d.get("caption", ""),
                                                           "rows": [{"label": r.get("label", ""), "value": r.get("value", "")} for r in d.get("rows", [])]}
            elif st == "dw_versus":
                nb["scene_type"], nb["data"] = "nh_versus", {"headline": d.get("headline", ""),
                                                             "left": d.get("left") or {}, "right": d.get("right") or {}}
            elif st == "dw_timeline":
                nb["scene_type"], nb["data"] = "nh_time", {"headline": d.get("headline", ""), "nodes": d.get("nodes", [])}
            elif st == "dw_steps":
                nb["scene_type"], nb["data"] = "nh_steps", {"headline": d.get("headline", ""),
                                                            "items": [dict(it, icon=ICON_MAP.get(it.get("icon", ""), "check")) for it in d.get("items", [])]}
            elif x["function"] == "close":
                nb["scene_type"], nb["data"] = "nh_close", {}
            else:
                raise SystemExit(f"{name}: unknown scene type {st}")
            beats.append(nb)
    for nb in beats:
        dd, f = nb["data"], nb["function"]
        if nb["scene_type"] == "nh_close":
            hl = next(x for x in old["beats"] if x["function"] == "close")["data"].get("headline", "")
            dd.update({"kicker": KICK["close"][lang], "rule": hl.rstrip(".") + ".", "rule_at": 0.2, "product": P,
                       "question": {"text": _l(spec["q"], lang), "at": 1.6}, "sign_at": "@Beauty",
                       "claim": "Wissen statt Versprechen." if lang == "de" else "Knowledge, not promises.",
                       "disclaimer": "Keine medizinische Beratung." if lang == "de" else "Not medical advice."})
        elif f == "hook":
            dd.update({"kicker": SERIES[spec["series"]][lang], "product": P, "question_at": 0.25})
        else:
            dd["kicker"] = KICK.get(f, KICK["insight"])[lang]
            if nb["scene_type"] == "nh_versus":
                for side in ("left", "right"):
                    dd[side] = dict(dd.get(side) or {}, product=product(spec, lang, text=False))
            else:
                dd["product"] = P
    new["beats"] = beats
    return new


def main() -> int:
    written = []
    for topic in SPEC:
        for lang in ("de", "en"):
            plan = convert(topic, lang)
            out = DIR / f"beauty-{topic}-{lang}.N1.json"
            out.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
            written.append(out.name)
    print("\n".join(written))
    print(f"{len(written)} plans; skipped topics (fit badly, open for Stefan): {', '.join(SKIPPED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
