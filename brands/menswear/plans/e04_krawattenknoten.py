"""E04 Drei Krawattenknoten im Vergleich: Four-in-Hand, Half-Windsor, Windsor (15.11.2026, Thema 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261115-3"
FIH = {"kind": "knot", "knot": "four_in_hand"}
HW = {"kind": "knot", "knot": "half_windsor"}
WIN = {"kind": "knot", "knot": "windsor"}
TORSO = {"kind": "torso", "hold": "belt", "tie_tip": 585, "neck": "tie"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://debretts.com/etiquette-category/events-and-dress-codes/", "title": "Debrett's, Events and Dress Codes (Lounge Suits): Four-in-Hand und Half-Windsor sind die vielseitigsten Knoten, große Windsorknoten sollte man im Allgemeinen meiden", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
    {"id": "S2", "url": "https://www.etonshirts.com/ch/en/journal/guides/how-to-tie-a-half-windsor-knot", "title": "Eton (Hemdenmacher), How to tie a Half Windsor knot: klassischer, nicht zu komplizierter, mittelgroßer Knoten, Kompromiss zwischen Four-in-Hand und Full Windsor, vereinfachte Version des Windsor", "checked_at": CHECKED, "label": "Eton, Half-Windsor"},
    {"id": "S3", "url": "https://www.etonshirts.com/ch/en/journal/guides/how-to-tie-a-four-in-hand-knot", "title": "Eton (Hemdenmacher), How to tie a Four-in-Hand knot: schnell gebunden, passt zu breiten wie schmalen Krawatten, mit Grübchen und leichter Schräglage bewusst nicht perfekt symmetrisch", "checked_at": CHECKED, "label": "Eton, Four-in-Hand"},
]

T = {
    "de": dict(
        title="Drei Krawattenknoten im Vergleich",
        q="Welcher Knoten zum Anzug?",
        b1="Four-in-Hand, Half-Windsor oder Windsor. Drei Krawattenknoten, drei Größen. Welchen davon bindest du, und warum?",
        b1_at=dict(badge_at="w:Four", loupe_at="w:Drei", nie_at="w:Welchen"),
        b2="Gleiche Krawatte, drei Knoten. Links der Four-in-Hand, der kleinste der drei. Rechts der volle Windsor, der größte. Dazwischen liegt laut dem Hemdenmacher Eton der Half-Windsor. Doch welcher passt am besten zum Anzug?",
        b2_head="Drei Knoten, drei Größen", b2_l=("Four-in-Hand", "der kleinste"), b2_r=("Windsor", "der größte"),
        b2_at=dict(left_at="w:Gleiche", left_tag_at="w:kleinste", right_at="w:Rechts", right_tag_at="w:größte", lpulse="w:Dazwischen", rpulse="w:Half"),
        b2_marker="w:Eton",
        b3="Der Four-in-Hand ist laut Eton schnell gebunden und passt zu breiten wie zu schmalen Krawatten. Typisch sind ein kleines Grübchen und eine leichte Schräglage. Er wirkt also bewusst nicht perfekt symmetrisch.",
        b3_head="Der Four-in-Hand", b3_label="Bewusst nicht symmetrisch",
        b3_at=dict(pointer_at="w:Four", zoom_at="w:schnell", flip_at="w:Grübchen", label_at="w:bewusst"),
        b3_marker="w:Eton",
        b4="Eine Stufe größer: der Half-Windsor. Eton nennt ihn klassisch, nicht zu kompliziert und mittelgroß, einen Kompromiss zwischen Four-in-Hand und vollem Windsor. Er ist eine vereinfachte Version des Windsor, der noch einmal größer ausfällt.",
        b4_head="Eine Stufe größer",
        b4_st=[("Half-Windsor", [("blade", "nicht kompliziert", "klassisch", "always", "w:kompliziert"),
                                 ("knot", "mittelgroß", "laut Eton", "always", "w:mittelgroß"),
                                 ("dimple", "der Kompromiss", "zwischen den beiden", "always", "w:Kompromiss")]),
               ("Voller Windsor", [("knot", "noch größer", "das Vorbild", "always", "w:größer#2")])],
        b4_stage2="w:vereinfachte", b4_marker="w:Eton",
        b5="Und welcher passt zum Anzug? Debrett's, der britische Ratgeber für Etikette, nennt Four-in-Hand und Half-Windsor die vielseitigsten Knoten. Große Windsorknoten solltest du laut Debrett's im Allgemeinen meiden. Für den Anzug heißt das: klein bis mittelgroß.",
        b5_head="Was sagt Debrett's?", b5_l=("Half-Windsor", "am vielseitigsten"), b5_r=("Windsor", "meist meiden"),
        b5_at=dict(left_at="w:Debrett", left_tag_at="w:vielseitigsten", lpulse="w:Half", right_at="w:Große", right_tag_at="w:meiden", rpulse="w:meiden"),
        b5_marker="w:Debrett",
        b6="Kurz gesagt: Der Four-in-Hand ist schnell gebunden, mit Grübchen und leicht schräg. Der Half-Windsor ist mittelgroß, der Kompromiss. Beide nennt Debrett's vielseitig. Den großen Windsor meidest du beim Anzug eher.",
        b6_head="Kurz gesagt",
        b6_items=[("Four-in-Hand: schnell", "Grübchen, leicht schräg", "w:Four", "w:schräg"),
                  ("Half-Windsor: mittel", "der Kompromiss, laut Eton", "w:Half", "w:Kompromiss"),
                  ("Windsor: eher meiden", "laut Debrett's", "w:großen", "w:meidest")],
        b7="Statt großem Windsor lieber Four-in-Hand oder Half-Windsor. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Klein bis mittelgroß.", b7_at=dict(fix_at="w:Four", ring_at="w:Half", statement_at="w:Half", chip_at="w:Blick"),
        status="Krawattenknoten",
        states=["Knoten: ?", "drei Größen", "Four-in-Hand: schräg", "Half-Windsor: mittel", "Windsor: eher meiden", "klein bis mittel", "klein bis mittelgroß"],
        desc="Four-in-Hand, Half-Windsor oder Windsor? Eton beschreibt den Four-in-Hand als schnell und bewusst leicht schräg, den Half-Windsor als mittelgroßen Kompromiss. Debrett's nennt beide am vielseitigsten und rät vom großen Windsor meist ab.",
        tags=["herrenmode", "krawatte", "krawattenknoten", "anzug", "stilregeln"],
        hooks=[("H1", "question", "Welcher Knoten zum Anzug?", []),
               ("H2", "misconception", "Der größte Knoten? Debrett's rät meist ab.", ["S1"]),
               ("H3", "surprising_fact", "Der Four-in-Hand ist bewusst nicht symmetrisch", ["S3"]),
               ("H4", "concrete_risk", "Großer Windsor zum Anzug? Laut Debrett's meist meiden.", ["S1"]),
               ("H5", "demonstration", "Drei Knoten, drei Größen, ein Vergleich", [])],
    ),
    "en": dict(
        title="Three tie knots, side by side",
        q="Which knot for a suit?",
        b1="Four-in-hand, half-Windsor or full Windsor. Three tie knots, three sizes. Which one do you tie, and why?",
        b1_at=dict(badge_at="w:Four", loupe_at="w:Three", nie_at="w:Which"),
        b2="Same tie, three knots. On the left, the four-in-hand, the smallest of the three. On the right, the full Windsor, the largest. In between, says the shirtmaker Eton, sits the half-Windsor. So which one belongs with a suit?",
        b2_head="Three knots, three sizes", b2_l=("Four-in-hand", "the smallest"), b2_r=("Windsor", "the largest"),
        b2_at=dict(left_at="w:Same", left_tag_at="w:smallest", right_at="w:right", right_tag_at="w:largest", lpulse="w:between", rpulse="w:half"),
        b2_marker="w:Eton",
        b3="According to Eton, the four-in-hand is quick to tie and works with wide and slim ties alike. Typical are a small dimple and a slight slant. So it looks deliberately less than perfectly symmetrical.",
        b3_head="The four-in-hand", b3_label="Deliberately not symmetrical",
        b3_at=dict(pointer_at="w:four", zoom_at="w:quick", flip_at="w:dimple", label_at="w:deliberately"),
        b3_marker="w:Eton",
        b4="One step up: the half-Windsor. Eton calls it classic, not too complicated and medium-sized, a compromise between the four-in-hand and the full Windsor. It is a simplified version of the Windsor, which comes out larger still.",
        b4_head="One step up",
        b4_st=[("Half-Windsor", [("blade", "not complicated", "a classic", "always", "w:complicated"),
                                 ("knot", "medium-sized", "says Eton", "always", "w:medium"),
                                 ("dimple", "the compromise", "between the two", "always", "w:compromise")]),
               ("Full Windsor", [("knot", "larger still", "the original", "always", "w:larger")])],
        b4_stage2="w:simplified", b4_marker="w:Eton",
        b5="And with a suit? Debrett's, the British etiquette guide, calls the four-in-hand and the half-Windsor the most versatile knots. Large Windsor knots, Debrett's says, are generally best avoided. For everyday suits, that means small to medium.",
        b5_head="What Debrett's says", b5_l=("Half-Windsor", "most versatile"), b5_r=("Windsor", "best avoided"),
        b5_at=dict(left_at="w:Debrett", left_tag_at="w:versatile", lpulse="w:half", right_at="w:Large", right_tag_at="w:avoided", rpulse="w:avoided"),
        b5_marker="w:Debrett",
        b6="In short: the four-in-hand is quick to tie, with a dimple and a slight slant. The half-Windsor is medium-sized, the compromise. Debrett's calls both versatile. The large Windsor, you mostly avoid.",
        b6_head="In short",
        b6_items=[("Four-in-hand: quick", "a dimple and a slight slant", "w:four", "w:slant"),
                  ("Half-Windsor: medium", "the compromise, says Eton", "w:half", "w:compromise"),
                  ("Windsor: mostly avoid", "says Debrett's", "w:large", "w:avoid")],
        b7="Instead of the large Windsor: a four-in-hand or a half-Windsor. For more eye for detail: follow Suitwerk.",
        b7_stmt="Small to medium.", b7_at=dict(fix_at="w:four", ring_at="w:half", statement_at="w:half", chip_at="w:eye"),
        status="Tie knots",
        states=["knot: ?", "three sizes", "four-in-hand: slanted", "half-Windsor: medium", "Windsor: mostly avoid", "small to medium", "knot: small to medium"],
        desc="Four-in-hand, half-Windsor or Windsor? Eton describes the four-in-hand as quick and deliberately slightly slanted, the half-Windsor as a medium-sized compromise. Debrett's calls both the most versatile and mostly advises against the large Windsor.",
        tags=["menswear", "tie", "tieknots", "suit", "styletips"],
        hooks=[("H1", "question", "Which knot for a suit?", []),
               ("H2", "misconception", "The biggest knot? Debrett's mostly says no.", ["S1"]),
               ("H3", "surprising_fact", "The four-in-hand is meant to be asymmetric", ["S3"]),
               ("H4", "concrete_risk", "A large Windsor with a suit? Debrett's: best avoided.", ["S1"]),
               ("H5", "demonstration", "Three knots, three sizes, one comparison", [])],
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
    hooks = [hook(h, ty, os, os, src, "Four-in-Hand-Knoten, Lupe auf dem Grübchen") for h, ty, os, src in t["hooks"]]
    a2, a3, a5 = t["b2_at"], t["b3_at"], t["b5_at"]
    objs = [(FIH, "dimple", ""), (HW, "knot", ""), (WIN, "knot", "red")]
    items = []
    for (title, sub, at, second), (obj, ring, tone) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at, "ring": ring, "ring_at": second}
        if tone:
            it["ring_tone"] = tone
        items.append(it)
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": FIH, "target": "dimple", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 12, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": FIH, "target": "knot", "tag": t["b2_l"][1], "pulses": [{"target": "knot", "at": a2["lpulse"]}]},
                  "right": {"title": t["b2_r"][0], "object": WIN, "target": "knot", "tag": t["b2_r"][1], "pulses": [{"target": "knot", "at": a2["rpulse"]}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": t["b2_marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "from": TORSO, "to": FIH, "target": "knot", "zoom": 1.35, "label": t["b3_label"],
                  "backdrop": True, "hold_end": True, **a3},
         "source_ids": ["S3"],
         "overlay": {"transition": {"type": "iris", "x": 540, "y": 640, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "stages": _stages(t["b4_st"], (HW, WIN), t["b4_stage2"]), "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "left": {"title": t["b5_l"][0], "object": HW, "target": "knot", "tag": t["b5_l"][1], "pulses": [{"target": "knot", "at": a5["lpulse"]}]},
                  "right": {"title": t["b5_r"][0], "object": WIN, "tag": t["b5_r"][1], "pulses": [{"target": "knot", "at": a5["rpulse"], "tone": "red"}]},
                  "left_at": a5["left_at"], "left_tag_at": a5["left_tag_at"], "right_at": a5["right_at"], "right_tag_at": a5["right_tag_at"],
                  "backdrop": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S3", "S2", "S1"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], WIN, FIH, "knot", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "red", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema E04 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; keine Herkunftsgeschichten (Herzog von Windsor, Kutscherclub, Churchill), keine Kragenempfehlung.",
                 sources=SOURCES, hooks=hooks, hook_note="Die drei Knotennamen als Frage, die Lupe auf dem Grübchen.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Herkunft der Knotennamen: nicht belegt, nicht im Video.",
                             "Kragenform passend zum Knoten: nicht belegt; die Zeichnung spreizt den Kragen mit dem Knoten, im Text nicht erwähnt.",
                             "'Der kleinste' für den Four-in-Hand: abgeleitet aus Eton (Half-Windsor mittelgroß, Kompromiss zum Full Windsor)."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
