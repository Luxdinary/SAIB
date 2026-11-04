"""E02 White Tie: Frack, weiße Weste, weiße Fliege (12.11.2026, Thema 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261112-2"
TC = {"kind": "tailcoat"}
DJ = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "peak", "dinner": True, "neck": "bow", "strain": False}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://debretts.com/etiquette-category/events-and-dress-codes/", "title": "Debrett's, Events and Dress Codes (White Tie): schwarzer einreihiger Frack mit seidenen steigenden Revers, offen getragen; Hose mit zwei Borten an der Außennaht; tief ausgeschnittene weiße Marcella-Weste; weißes Marcella-Hemd mit gestärktem, abnehmbarem Kläppchenkragen, Doppelmanschetten und Studs; schmale weiße handgebundene Fliege; schwarze Lack- oder hochglanzpolierte Schnürschuhe; Zylinder und Stock heute nur noch auf der Bühne", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
    {"id": "S2", "url": "https://www.opernball.at/en/the-evening/", "title": "Wiener Opernball, offizielle Seite: Herren tragen schwarzen Frack, weißes Frackhemd, weiße Fliege und schwarze Lackschuhe; Galauniform alternativ erlaubt", "checked_at": CHECKED, "label": "Wiener Opernball"},
    {"id": "S3", "url": "https://www.austria.info/en-us/inspiration/ball-season/", "title": "austria.info, Ballsaison: Frack mit weißer Fliege bei einigen Bällen Pflicht (Opernball, Philharmonikerball, Techniker Cercle), bei den meisten Bällen genügt ein Smoking", "checked_at": CHECKED, "label": "austria.info, Ballsaison"},
]

T = {
    "de": dict(
        title="White Tie: Was zum Frack gehört",
        q="White Tie: Was gehört zum Frack?",
        b1="White Tie auf der Einladung. Das heißt Frack. Aber was gehört wirklich dazu, und was nicht mehr?",
        b1_at=dict(badge_at="w:Frack", loupe_at="w:Frack", nie_at="w:nicht"),
        b2="Black Tie kennst du: Smoking und schwarze Fliege. Für den Wiener Opernball reicht das nicht. Die offizielle Seite schreibt Herren vor: schwarzer Frack, weißes Frackhemd, weiße Fliege und schwarze Lackschuhe.",
        b2_head="Reicht der Smoking?", b2_label="Opernball: Frack, weiße Fliege",
        b2_at=dict(pointer_at="w:Smoking", zoom_at="w:Opernball", error_at="w:reicht", flip_at="w:Frack", label_at="w:Lackschuhe"),
        b2_marker="w:offizielle",
        b3="Debrett's, der britische Ratgeber für Etikette, beschreibt den Frack genau: schwarz und einreihig, mit seidenbelegten steigenden Revers, und er wird offen getragen. Die Hose hat zwei Borten an der Außennaht.",
        b3_head="Der Frack", b3_stage="Laut Debrett's",
        b3_tags=[("lapel", "Seidenrevers", "steigend", "always", "w:seidenbelegten"),
                 ("front", "offen getragen", "einreihig", "always", "w:offen"),
                 ("trousers", "zwei Borten", "an der Außennaht", "always", "w:Borten")],
        b4="Darunter wird es weiß. Links Black Tie mit schwarzer Fliege. Rechts White Tie: eine tief ausgeschnittene weiße Weste aus Marcella, ein Hemd mit gestärktem, abnehmbarem Kläppchenkragen, dazu eine schmale weiße Fliege, von Hand gebunden.",
        b4_head="Schwarz oder weiß?", b4_l=("Black Tie", "schwarze Fliege"), b4_r=("White Tie", "Weste und Fliege weiß"),
        b4_at=dict(left_at="w:Links", left_tag_at="w:schwarzer", right_at="w:Rechts", right_tag_at="w:Marcella",
                   lpulse="w:Fliege", p_wc="w:Weste", p_col="w:Kläppchenkragen", p_bow="w:schmale"),
        b5="Gilt das auf jedem Ball? Laut austria.info ist der Frack nur bei einigen Pflicht, etwa beim Opernball. Meist genügt ein Smoking. Zylinder und Stock sieht man laut Debrett's nur noch auf der Bühne.",
        b5_head="Auf jedem Ball?",
        b5_st=[("Einige Bälle", [("tails", "Frack: Pflicht", "etwa der Opernball", "always", "w:Pflicht")]),
               ("Die meisten Bälle", [("lapel", "Smoking genügt", "laut austria.info", "sometimes", "w:genügt"),
                                      ("hem", "Zylinder, Stock", "nur auf der Bühne", "never", "w:Zylinder")])],
        b5_stage2="w:Meist", b5_marker="w:austria",
        b6="Kurz gesagt: Der Frack ist schwarz, einreihig und bleibt offen, die Hose hat zwei Borten. Weste und Fliege sind weiß, die Fliege von Hand gebunden. Und Pflicht ist er nur auf einigen Bällen.",
        b6_head="Kurz gesagt",
        b6_items=[("Frack: offen getragen", "einreihig, Hose mit zwei Borten", "w:Frack", "w:offen"),
                  ("Weiß: Weste und Fliege", "die Fliege schmal, von Hand", "w:Weste", "w:Hand"),
                  ("Pflicht: einige Bälle", "sonst genügt meist der Smoking", "w:Pflicht", "w:Bällen")],
        b7="Vom Smoking zum Frack mit weißer Fliege: Das ist White Tie. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="White Tie, komplett.", b7_at=dict(fix_at="w:Frack", ring_at="w:White", statement_at="w:White", chip_at="w:Blick"),
        status="White Tie, Frack",
        states=["White Tie: ?", "Smoking reicht nicht", "Frack: offen getragen", "Weiß: Weste, Fliege", "meist genügt Smoking", "Frack, Weiß, Borten", "White Tie komplett"],
        desc="Was gehört zu White Tie? Debrett's beschreibt Frack mit Seidenrevers, Hose mit zwei Borten, weiße Marcella-Weste, Kläppchenkragen und weiße Fliege. Der Wiener Opernball schreibt genau das vor, bei den meisten Bällen genügt laut austria.info ein Smoking.",
        tags=["herrenmode", "whitetie", "frack", "opernball", "dresscode"],
        hooks=[("H1", "question", "White Tie: Was gehört zum Frack?", []),
               ("H2", "misconception", "Smoking zum Opernball? Dort ist der Frack Pflicht.", ["S2", "S3"]),
               ("H3", "surprising_fact", "Zylinder und Stock? Laut Debrett's nur noch auf der Bühne.", ["S1"]),
               ("H4", "concrete_risk", "Schwarze Fliege am Opernball? Vorgeschrieben ist Weiß.", ["S2"]),
               ("H5", "demonstration", "Vom Smoking zum Frack in einem Bild", [])],
    ),
    "en": dict(
        title="White tie: what goes with the tailcoat",
        q="White tie: what goes with tails?",
        b1="The invitation says white tie. That means tails. But what really belongs, and what no longer does?",
        b1_at=dict(badge_at="w:tails", loupe_at="w:tails", nie_at="w:longer"),
        b2="You know black tie: dinner jacket, black bow tie. For the Vienna Opera Ball, that is not enough. The official site asks for a black tailcoat, a white shirt, a white bow tie and black patent shoes.",
        b2_head="Is a dinner suit enough?", b2_label="Opera Ball: tails, white tie",
        b2_at=dict(pointer_at="w:dinner", zoom_at="w:Vienna", error_at="w:enough", flip_at="w:tailcoat", label_at="w:patent"),
        b2_marker="w:official",
        b3="Debrett's, the British authority on etiquette, describes the tailcoat precisely: black and single-breasted, with silk-faced peak lapels, and worn open. The trousers carry two lines of braid down the outside seam.",
        b3_head="The tailcoat", b3_stage="Says Debrett's",
        b3_tags=[("lapel", "silk facings", "peak lapels", "always", "w:silk"),
                 ("front", "worn open", "single-breasted", "always", "w:open"),
                 ("trousers", "two braids", "on the outside seam", "always", "w:braid")],
        b4="Beneath, it turns white. On the left, black tie with a black bow. On the right, white tie: a low-cut white Marcella waistcoat, a stiff, detachable wing collar, and a narrow white bow, tied by hand.",
        b4_head="Black or white?", b4_l=("Black tie", "a black bow tie"), b4_r=("White tie", "white waistcoat and bow"),
        b4_at=dict(left_at="w:left", left_tag_at="w:bow", right_at="w:right", right_tag_at="w:Marcella",
                   lpulse="w:bow", p_wc="w:waistcoat", p_col="w:wing", p_bow="w:narrow"),
        b5="Does every ball need tails? According to austria.info, only some, such as the Opera Ball. At most, a dinner suit is enough. And top hat and cane? Debrett's says these days, only on stage.",
        b5_head="At every ball?",
        b5_st=[("Some balls", [("tails", "tails required", "e.g. the Opera Ball", "always", "w:only")]),
               ("Most balls", [("lapel", "dinner suit: fine", "says austria.info", "sometimes", "w:enough"),
                               ("hem", "top hat, cane", "only on stage", "never", "w:top")])],
        b5_stage2="w:most", b5_marker="w:austria",
        b6="In short: the tailcoat is black, single-breasted and worn open, the trousers have two braids. Waistcoat and bow tie are white, the bow tied by hand. And tails are required only at some balls.",
        b6_head="In short",
        b6_items=[("Tails: worn open", "single-breasted, two braids", "w:tailcoat", "w:open"),
                  ("White: waistcoat, bow", "the bow tied by hand", "w:Waistcoat", "w:hand"),
                  ("Required: some balls", "otherwise a dinner suit will do", "w:required", "w:balls")],
        b7="From dinner suit to tailcoat and white bow tie: that is white tie. For more eye for detail: follow Suitwerk.",
        b7_stmt="White tie, complete.", b7_at=dict(fix_at="w:tailcoat", ring_at="w:white#2", statement_at="w:white#2", chip_at="w:eye"),
        status="White tie",
        states=["white tie: ?", "dinner suit: not enough", "tails: worn open", "white: waistcoat, bow", "mostly: dinner suit", "tails, white, braids", "white tie complete"],
        desc="What belongs to white tie? Debrett's describes a tailcoat with silk lapels, trousers with two braids, a white Marcella waistcoat, a wing collar and a white bow tie. The Vienna Opera Ball requires exactly that; at most balls, says austria.info, a dinner suit will do.",
        tags=["menswear", "whitetie", "tailcoat", "operaball", "dresscode"],
        hooks=[("H1", "question", "White tie: what goes with tails?", []),
               ("H2", "misconception", "A dinner suit at the Opera Ball? Tails are required.", ["S2", "S3"]),
               ("H3", "surprising_fact", "Top hat and cane? Debrett's says only on stage now.", ["S1"]),
               ("H4", "concrete_risk", "A black bow at the Opera Ball? The rule says white.", ["S2"]),
               ("H5", "demonstration", "From dinner suit to tailcoat in one picture", [])],
    ),
}


def _stages(spec, objs, second):
    out = []
    for k, ((title, tags), obj) in enumerate(zip(spec, objs)):
        out.append({"object": obj, "at": 0.0 if k == 0 else second, "title": title,
                    "tags": [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in tags]})
    return out


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Frack mit weißer Weste, Lupe auf der weißen Fliege") for h, ty, os, src in t["hooks"]]
    a2, a4 = t["b2_at"], t["b4_at"]
    objs = [(TC, None, "front"), (TC, None, "bow"), (TC, DJ, None)]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    ladder3 = _stages([(t["b3_stage"], t["b3_tags"])], (TC,), None)
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": TC, "target": "bow", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "from": DJ, "to": TC, "target": "neck", "zoom": 1.45, "label": t["b2_label"],
                  "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b2_marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": ladder3, "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": DJ, "target": "neck", "tag": t["b4_l"][1],
                           "pulses": [{"target": "neck", "at": a4["lpulse"]}]},
                  "right": {"title": t["b4_r"][0], "object": TC, "tag": t["b4_r"][1],
                            "pulses": [{"target": "waistcoat", "at": a4["p_wc"]}, {"target": "collar", "at": a4["p_col"]},
                                       {"target": "bow", "at": a4["p_bow"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 540, "y": 700, "seconds": 0.7}, "marker": "fakt", "marker_at": a4["right_tag_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": _stages(t["b5_st"], (TC, DJ), t["b5_stage2"]), "backdrop": True},
         "source_ids": ["S3", "S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], DJ, TC, "bow", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema E02 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Wiener Ballregeln nicht verallgemeinert (meist genügt Smoking), keine Rangfolge der Dresscodes als Fakt.",
                 sources=SOURCES, hooks=hooks, hook_note="Die Einladung als Ausgangslage, die Lupe auf der weißen Fliege.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Galauniform als Alternative am Opernball (S2): belegt, aus Zeitgründen nicht im Video.",
                             "Schwarze Fliege tragen in Wien nur Kellner (austria.info): bewusst weggelassen.",
                             "Doppelmanschetten, Studs und Schuhe (S1): belegt, nur teils gesprochen; Schuhe ohne eigene Zeichnung."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
