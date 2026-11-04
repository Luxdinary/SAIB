"""E01 Black Tie: Was zum Smoking gehört (10.11.2026, Thema 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261110-2"
DAY = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "notch", "strain": False}
DJ = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "peak", "dinner": True, "neck": "bow", "strain": False}
DJ_TIE = {**DJ, "neck": "tie"}
DJ_DB = {**DJ, "variant": "db6"}
DJ_OPEN = {**DJ, "fastened": []}
LEGS = {"kind": "legs", "break": "none", "shoe": "oxford"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://debretts.com/etiquette-category/events-and-dress-codes/", "title": "Debrett's, Events and Dress Codes (Black Tie): schwarzes Dinnerjackett aus Barathea oder feinem Fischgrat, ein- oder zweireihig, ohne Schlitze, seidene steigende Revers oder Schalkragen, bezogene Knöpfe; Hose mit einer Borte je Außennaht; weißes Abendhemd mit Umlegekragen; handgebundene schwarze Fliege; Weste oder Kummerbund, nie beides; schwarze polierte oder Lack-Schnürschuhe, schwarze Seidensocken; lange Krawatte bei formellen Privatanlässen meist unpassend", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
    {"id": "S2", "url": "https://www.moss.co.uk/inside-pocket/post/black-tie-dressing", "title": "Moss, Black tie dressing: traditioneller Look mit Satinrevers, weißem Abendhemd, schwarzer Seidenfliege, schwarzer Weste oder Kummerbund und schwarzen Lackschuhen", "checked_at": CHECKED, "label": "Moss, Inside Pocket"},
]

T = {
    "de": dict(
        title="Black Tie: Was zum Smoking gehört",
        q="Black Tie: Was gehört dazu?",
        b1="Auf der Einladung steht Black Tie. Was gehört dann wirklich dazu, und was eher nicht?",
        b1_at=dict(badge_at="w:Black", loupe_at="w:Black", nie_at="w:Was"),
        b2="Black Tie ist mehr als ein dunkler Anzug. Debrett's beschreibt ein klar umrissenes Ensemble, Stück für Stück. Moss zeigt den traditionellen Look genauso: Satinrevers, weißes Hemd, schwarze Fliege.",
        b2_head="Anzug oder Smoking?", b2_l=("Dunkler Anzug", "Tagesanzug, Krawatte"), b2_r=("Dinnerjackett", "ein festes Ensemble"),
        b2_at=dict(left_at="w:dunkler", left_tag_at="w:Anzug", right_at="w:Debrett", right_tag_at="w:Ensemble", lpulse="w:Satinrevers", rpulse="w:Fliege"),
        b3="Das Jackett ist laut Debrett's schwarz, aus Barathea oder feinem Fischgrat. Es hat seidenbelegte steigende Revers oder einen Schalkragen und bezogene Knöpfe. Es darf ein- oder zweireihig sein, aber ohne Schlitze.",
        b3_head="Das Jackett",
        b3_st=[("Einreihig", [("lapel", "Seidenrevers", "steigend oder Schal", "w:seidenbelegte"), ("button:0", "bezogene Knöpfe", "laut Debrett's", "w:Knöpfe")]),
               ("Zweireihig", [("hem", "ohne Schlitze", "ein- oder zweireihig", "w:Schlitze")])],
        b3_stage2="w:zweireihig",
        b4="Dann zum Hals. Die Hollywood-Variante mit langer Krawatte gilt laut Debrett's bei formellen privaten Anlässen meist als unpassend. Gemeint ist eine schwarze Fliege, von Hand gebunden. Dazu ein weißes Abendhemd mit Umlegekragen statt Kläppchenkragen.",
        b4_head="Fliege oder Krawatte?", b4_label="Fliege, von Hand gebunden",
        b4_at=dict(pointer_at="w:Hals", zoom_at="w:Hollywood", error_at="w:Krawatte", flip_at="w:Fliege", label_at="w:Hand"),
        b5="Unter dem Jackett gilt laut Debrett's: Die Weste ist die elegante Wahl, der Kummerbund optional, aber nie beides zusammen. Die Hose trägt eine Borte an jeder Außennaht. Dazu schwarze polierte oder Lackschuhe zum Schnüren und schwarze Seidensocken.",
        b5_head="Darunter und dazu",
        b5_st=[("Darunter", [("waist", "Weste: elegant", "laut Debrett's", "always", "w:Weste"), ("pocket", "oder Kummerbund", "optional", "sometimes", "w:Kummerbund"),
                             ("quarters", "nie beides", "nie zusammen", "never", "w:beides")]),
               ("Hose, Schuh", [("crease", "Borte je Bein", "an der Außennaht", "always", "w:Borte"), ("lacing", "Schnürschuh", "Lack oder poliert", "always", "w:Lackschuhe")])],
        b5_stage2="w:Hose",
        b6="Kurz gesagt: Schwarzes Jackett mit Seidenrevers, die Hose mit Borte. Eine schwarze Fliege, von Hand gebunden. Und darunter Weste oder Kummerbund, aber nie beides zusammen.",
        b6_head="Kurz gesagt",
        b6_items=[("Seidenrevers", "steigend oder Schal", "w:Jackett", "w:Seidenrevers"),
                  ("Fliege, von Hand", "keine lange Krawatte", "w:Fliege", "w:Hand"),
                  ("Weste oder Kummerbund", "nie beides zusammen", "w:Weste", "w:beides")],
        b7="Vom dunklen Anzug zum Ensemble: So sieht Black Tie aus. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Black Tie, komplett.", b7_at=dict(fix_at="w:Ensemble", ring_at="w:Black", statement_at="w:Black", chip_at="w:Blick"),
        status="Black Tie",
        states=["Black Tie: ?", "mehr als ein Anzug", "Jackett: Seidenrevers", "Fliege, nicht Krawatte", "Weste oder Kummerbund", "Seide, Fliege, Weste", "Ensemble komplett"],
        desc="Was gehört zu Black Tie? Debrett's beschreibt ein festes Ensemble: Dinnerjackett mit Seidenrevers, Hose mit Borte, weißes Abendhemd, handgebundene Fliege, Weste oder Kummerbund, Schnürschuhe. Dazu Moss.",
        tags=["herrenmode", "blacktie", "smoking", "dresscode", "stilregeln"],
        hooks=[("H1", "question", "Black Tie: Was gehört dazu?", []),
               ("H2", "misconception", "Black Tie heißt nicht einfach dunkler Anzug", ["S1", "S2"]),
               ("H3", "surprising_fact", "Weste oder Kummerbund, aber nie beides", ["S1"]),
               ("H4", "concrete_risk", "Lange Krawatte zum Smoking? Laut Debrett's meist unpassend.", ["S1"]),
               ("H5", "demonstration", "Vom Anzug zum Dinnerjackett in einem Bild", [])],
    ),
    "en": dict(
        title="Black tie: what the dinner suit really needs",
        q="Black tie: what belongs?",
        b1="The invitation says black tie. So what does that really include, and what does it not?",
        b1_at=dict(badge_at="w:black", loupe_at="w:black", nie_at="w:what"),
        b2="Black tie is more than a dark suit. Debrett's describes a clearly defined ensemble, piece by piece. Moss shows the traditional look the same way: satin lapels, a white shirt, a black bow tie.",
        b2_head="Suit or dinner suit?", b2_l=("Dark suit", "a day suit with a tie"), b2_r=("Dinner jacket", "a defined ensemble"),
        b2_at=dict(left_at="w:dark", left_tag_at="w:suit", right_at="w:Debrett", right_tag_at="w:ensemble", lpulse="w:satin", rpulse="w:bow"),
        b3="According to Debrett's, the jacket is black, in barathea or a fine herringbone. It has silk-faced peak lapels or a shawl collar, and covered buttons. It may be single or double-breasted, but without vents.",
        b3_head="The jacket",
        b3_st=[("Single", [("lapel", "silk facings", "peak or shawl", "w:silk"), ("button:0", "covered buttons", "says Debrett's", "w:covered")]),
               ("Double-breasted", [("hem", "no vents", "single or double", "w:vents")])],
        b3_stage2="w:double",
        b4="Then the neck. Debrett's finds the Hollywood look, with a long tie, usually out of place at formal private events. Instead: a black bow tie, tied by hand, and a white evening shirt with a turn-down collar.",
        b4_head="Bow tie or long tie?", b4_label="Bow tie, tied by hand",
        b4_at=dict(pointer_at="w:neck", zoom_at="w:Hollywood", error_at="w:tie", flip_at="w:bow", label_at="w:hand"),
        b5="Under the jacket, Debrett's rule: the waistcoat is the elegant choice, the cummerbund optional, but never both together. The trousers carry one braid on each outside seam. With them, black polished or patent lace-ups and black silk socks.",
        b5_head="Underneath and below",
        b5_st=[("Underneath", [("waist", "waistcoat: elegant", "says Debrett's", "always", "w:waistcoat"), ("pocket", "or cummerbund", "optional", "sometimes", "w:cummerbund"),
                               ("quarters", "never both", "not together", "never", "w:never")]),
               ("Trousers, shoes", [("crease", "one braid per leg", "on the outside seam", "always", "w:braid"), ("lacing", "lace-ups", "patent or polished", "always", "w:patent")])],
        b5_stage2="w:trousers",
        b6="In short: a black jacket with silk lapels, trousers with a braid. A black bow tie, tied by hand. And underneath, a waistcoat or a cummerbund, but never both.",
        b6_head="In short",
        b6_items=[("Silk lapels", "peak or shawl", "w:black", "w:silk"),
                  ("Bow tie, tied by hand", "no long tie", "w:bow", "w:hand"),
                  ("Waistcoat or cummerbund", "never both together", "w:waistcoat", "w:never")],
        b7="From a dark suit to a full ensemble: that is black tie. For more eye for detail: follow Suitwerk.",
        b7_stmt="Black tie, complete.", b7_at=dict(fix_at="w:ensemble", ring_at="w:black", statement_at="w:black", chip_at="w:eye"),
        status="Black tie",
        states=["black tie: ?", "more than a suit", "jacket: silk lapels", "bow tie, not a tie", "one, never both", "silk, bow, waistcoat", "ensemble complete"],
        desc="What belongs to black tie? Debrett's describes a defined ensemble: dinner jacket with silk lapels, braided trousers, white evening shirt, hand-tied bow tie, waistcoat or cummerbund, lace-ups. Plus Moss.",
        tags=["menswear", "blacktie", "dinnersuit", "dresscode", "styletips"],
        hooks=[("H1", "question", "Black tie: what belongs?", []),
               ("H2", "misconception", "Black tie is not just a dark suit", ["S1", "S2"]),
               ("H3", "surprising_fact", "Waistcoat or cummerbund, but never both", ["S1"]),
               ("H4", "concrete_risk", "A long tie with a dinner suit? Debrett's says usually not.", ["S1"]),
               ("H5", "demonstration", "From suit to dinner jacket in one picture", [])],
    ),
}


def _stages(spec, objs, second):
    out = []
    for k, ((title, tags), obj) in enumerate(zip(spec, objs)):
        out.append({"object": obj, "at": 0.0 if k == 0 else second, "title": title,
                    "tags": [{"spot": tg[0], "text": tg[1], "sub": tg[2], "tone": tg[3] if len(tg) == 5 else "always", "at": tg[-1]} for tg in tags]})
    return out


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Dinnerjackett, Lupe auf dem seidenbelegten Revers") for h, ty, os, src in t["hooks"]]
    a2, a4 = t["b2_at"], t["b4_at"]
    objs = [(DJ, None, "lapel"), (DJ_TIE, {"neck": "bow"}, None), (DJ_OPEN, None, "waist")]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 5, "spoken": t["b1"],
         "data": {"question": t["q"], "object": DJ, "target": "lapel", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 11, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": DAY, "target": "neck", "tag": t["b2_l"][1]},
                  "right": {"title": t["b2_r"][0], "object": DJ, "tag": t["b2_r"][1],
                            "pulses": [{"target": "lapel", "at": a2["lpulse"]}, {"target": "neck", "at": a2["rpulse"]}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": a2["right_at"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": _stages(t["b3_st"], (DJ, DJ_DB), t["b3_stage2"]), "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": DJ_TIE, "to": DJ, "target": "neck", "zoom": 1.5, "label": t["b4_label"],
                  "backdrop": True, "hold_end": True, **a4},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 330, "y": 470, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a4["zoom_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 14, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": _stages(t["b5_st"], (DJ_OPEN, LEGS), t["b5_stage2"]), "backdrop": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], DAY, DJ, "lapel", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "red", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema E01 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S2; keine Gürtelschlaufen-Regel, keine Herkunftsgeschichte, kein weißes Dinnerjackett.",
                 sources=SOURCES, hooks=hooks, hook_note="Die Einladung als Ausgangslage, die Lupe auf dem Seidenrevers.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Gürtelschlaufen und Hosenträger: in den Quellen nicht belegt, nicht im Video.",
                             "Herkunft des Smokings (Edward VII., Henry Poole): nicht als Fakt, nicht im Video.",
                             "Weißes Dinnerjackett und weißes Einstecktuch (Debrett's): aus Zeitgründen nicht im Video."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
