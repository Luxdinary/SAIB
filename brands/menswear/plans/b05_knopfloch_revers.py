"""B05 Knopfloch im Revers: gedacht für eine Blume (15.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261115-1"
HOLE = {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel_hole": True}
FLOWER = {"kind": "jacket", "variant": "sb2", "fastened": [0], "flower": True}
DINNER = {"kind": "jacket", "variant": "sb1", "fastened": [0], "dinner": True, "neck": "bow", "lapel": "peak", "lapel_hole": True}
FLOWER_SB1 = {"kind": "jacket", "variant": "sb1", "fastened": [0], "flower": True}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://www.savilerowbespoke.com/wp-content/uploads/2015/06/Savile-Row-Inside-Out.pdf",
     "title": "Savile Row Bespoke Association, Savile Row: Inside Out: Knopflöcher von Hand genäht, linkes Revers-Knopfloch mit genähter Blumenschlaufe",
     "checked_at": CHECKED, "label": "Savile Row Bespoke"},
    {"id": "S2", "url": "https://debretts.com/wedding-flowers/",
     "title": "Debrett's, Wedding Flowers: Ansteckblumen links über dem Herzen, eine Halterung unter dem Revers hält den Stiel",
     "checked_at": CHECKED, "label": "Debrett's, Wedding Flowers"},
    {"id": "S3", "url": "https://www.anderson-sheppard.co.uk/bespoke-gallery/",
     "title": "Anderson & Sheppard, Bespoke Gallery: mehrere Jacken mit flower buttonholes, teils links und rechts, auch am Dinnerjacket",
     "checked_at": CHECKED, "label": "Anderson & Sheppard"},
]

T = {
    "de": dict(
        title="Wozu das Knopfloch im Revers?",
        q="Ein Knopfloch ohne Knopf?",
        b1="Oben im linken Revers sitzt ein kleines Knopfloch. Aber einen passenden Knopf dazu findest du nirgends. Wofür ist es also da?",
        hook_at=dict(badge_at="w:Knopfloch", loupe_at="w:Knopfloch", nie_at="w:Wofür"),
        b2="Vorn am Sakko hat jedes Knopfloch seinen Knopf. Das im Revers nicht. Trotzdem wird es sorgfältig gearbeitet: Laut der Savile Row Bespoke Association nähen die Häuser ihre Knopflöcher von Hand, auch dieses hier.",
        b2_head="Ein Loch ohne Knopf", b2_stage="Das Revers",
        b2_tags=[("button:0", "Knopf vorn", "mit Knopfloch", "always", "w:Knopfloch"),
                 ("lapel_hole", "im Revers", "kein Knopf dazu", "sometimes", "w:Revers"),
                 ("lapel_r", "von Hand genäht", "Savile Row", "always", "w:Hand")],
        b2_marker="w:Savile",
        b3="Die Antwort steckt auf der Rückseite des Revers. Dort hat das Knopfloch im linken Revers eine genähte Blumenschlaufe, so beschreibt es die Savile Row Bespoke Association. Das Loch ist also für eine Blume gedacht, nicht für einen Knopf.",
        b3_head="Der Blick nach hinten", b3_label="gedacht für eine Blume",
        b3_at=dict(pointer_at="w:Antwort", zoom_at="w:Rückseite", flip_at="w:Blumenschlaufe", label_at="w:gedacht"),
        b3_marker="w:Dort",
        b4="Erst ohne Blume, dann mit. Für Hochzeiten beschreibt Debrett's, der britische Ratgeber für Etikette, wo sie sitzt: links, über dem Herzen. Unter dem Revers hält eine Halterung den Stiel fest.",
        b4_head="So sitzt die Blume", b4_l=("Ohne Blume", "nur das Knopfloch"), b4_r=("Mit Blume", "links, über dem Herzen"),
        b4_at=dict(left_at="w:Erst", left_tag_at="w:ohne", right_at="w:dann", right_tag_at="w:Herzen", p1="w:links", p2="w:Halterung", marker="w:Debrett"),
        b5="Auch in der Galerie des Maßschneiders Anderson and Sheppard tragen mehrere Jacken solche Blumenknopflöcher. Manche haben sogar zwei, links und rechts. Und auch ein Dinnerjacket ist dabei.",
        b5_head="Anderson & Sheppard",
        b5_s0=("Sakko", [("lapel_hole", "Blumenknopfloch", "Anderson & Sheppard", "always", "w:Blumenknopf"),
                         ("lapel", "teils beidseitig", "links und rechts", "sometimes", "w:zwei")]),
        b5_s1=("Dinnerjacket", "w:Dinnerjacket", [("lapel_hole", "auch hier", "am Dinnerjacket", "always", None)]),
        b5_marker="w:Anderson",
        b6="Kurz gesagt: Das kleine Knopfloch im linken Revers ist für eine Blume gedacht, nicht für einen Knopf. Auf der Rückseite hält eine genähte Schlaufe den Stiel. Getragen wird die Blume links, über dem Herzen.",
        b6_head="Kurz gesagt",
        b6_items=[("Für eine Blume", "nicht für einen Knopf", "w:Knopfloch", "w:Blume"),
                  ("Schlaufe hinten", "von Hand genäht, Savile Row", "w:Rückseite", "w:Stiel"),
                  ("Links, über dem Herzen", "laut Debrett's", "w:Getragen", "w:Herzen")],
        b6_marker="w:gesagt",
        b7="Kein Knopf, sondern eine Blume. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Für die Blume.", b7_at=dict(fix_at="w:sondern", ring_at="w:Blume", statement_at="w:Blume", chip_at="w:Blick"),
        status="Revers links",
        states=["Knopfloch: ?", "kein Knopf dazu", "Schlaufe hinten", "links, überm Herzen", "auch am Dinnerjacket", "für eine Blume", "für die Blume"],
        desc="Wozu ist das Knopfloch im linken Revers? Für eine Blume: Savile-Row-Häuser nähen es mit Blumenschlaufe auf der Rückseite, Debrett's beschreibt das Anstecken links über dem Herzen. Auch Anderson & Sheppard zeigt es, sogar am Dinnerjacket.",
        tags=["herrenmode", "sakko", "revers", "anstecker", "savilerow"],
        hooks=[("H1", "question", "Ein Knopfloch ohne Knopf?"), ("H2", "misconception", "Das Reversknopfloch ist kein Zierstich"),
               ("H3", "surprising_fact", "Hinter dem Revers sitzt eine Schlaufe für Blumen"), ("H4", "concrete_risk", "Ohne Blume bleibt dieses Loch einfach leer"),
               ("H5", "demonstration", "Was gehört in dieses Knopfloch?")],
        visual="Sakko, Lupe auf dem Knopfloch im linken Revers",
    ),
    "en": dict(
        title="The lapel buttonhole is for a flower",
        q="A buttonhole without a button?",
        b1="High on the left lapel there is a buttonhole. But you will not find a button to go with it anywhere. So what is it for?",
        hook_at=dict(badge_at="w:buttonhole", loupe_at="w:buttonhole", nie_at="w:what"),
        b2="On a jacket front, every buttonhole has its button. The one in the lapel does not. Yet it is made with care: the Savile Row Bespoke Association says the houses sew their buttonholes by hand, this one included.",
        b2_head="A hole without a button", b2_stage="The lapel",
        b2_tags=[("button:0", "front button", "with its buttonhole", "always", "w:buttonhole"),
                 ("lapel_hole", "in the lapel", "no button for it", "sometimes", "w:lapel"),
                 ("lapel_r", "sewn by hand", "Savile Row", "always", "w:hand")],
        b2_marker="w:Savile",
        b3="The answer is on the back of the lapel. There, the left lapel buttonhole has a sewn flower loop. So the hole is meant for a flower, not for a button.",
        b3_head="A look at the back", b3_label="meant for a flower",
        b3_at=dict(pointer_at="w:answer", zoom_at="w:There", flip_at="w:flower", label_at="w:meant"),
        b3_marker="w:sewn",
        b4="First without a flower, then with one. For weddings, Debrett's describes where it sits: on the left, over the heart. Under the lapel, a holder keeps the stem in place.",
        b4_head="Where the flower sits", b4_l=("No flower", "just the buttonhole"), b4_r=("With a flower", "left, over the heart"),
        b4_at=dict(left_at="w:First", left_tag_at="w:without", right_at="w:then", right_tag_at="w:heart", p1="w:left", p2="w:holder", marker="w:Debrett"),
        b5="In the gallery of the tailors Anderson and Sheppard, several jackets have these flower buttonholes. Some even have two, on the left and on the right. There is even a dinner jacket among them, with a flower buttonhole as well.",
        b5_head="Anderson & Sheppard",
        b5_s0=("Jacket", [("lapel_hole", "flower buttonhole", "Anderson & Sheppard", "always", "w:flower"),
                          ("lapel", "some on both sides", "left and right", "sometimes", "w:two")]),
        b5_s1=("Dinner jacket", "w:dinner", [("lapel_hole", "here too", "on a dinner jacket", "always", None)]),
        b5_marker="w:Anderson",
        b6="In short: the buttonhole in the left lapel is meant for a flower. On the back, a sewn loop holds the stem. And the flower is worn on the left, over the heart.",
        b6_head="In short",
        b6_items=[("For a flower", "not for a button", "w:buttonhole", "w:flower"),
                  ("A loop on the back", "hand-sewn, Savile Row", "w:back", "w:stem"),
                  ("Left, over the heart", "according to Debrett's", "w:worn", "w:heart")],
        b6_marker="w:short",
        b7="Not a button, but a flower. For more eye for detail: follow Suitwerk.",
        b7_stmt="Made for a flower.", b7_at=dict(fix_at="w:button", ring_at="w:flower", statement_at="w:flower", chip_at="w:eye"),
        status="Left lapel",
        states=["buttonhole: ?", "no button for it", "loop at the back", "left, over the heart", "on dinner jackets too", "for a flower", "for the flower"],
        desc="What is the buttonhole in the left lapel for? A flower: Savile Row houses sew it with a flower loop at the back, and Debrett's describes wearing one on the left, over the heart. Anderson & Sheppard shows it too, even on a dinner jacket.",
        tags=["menswear", "jacket", "lapel", "boutonniere", "savilerow"],
        hooks=[("H1", "question", "A buttonhole without a button?"), ("H2", "misconception", "The lapel buttonhole is not just decoration"),
               ("H3", "surprising_fact", "Behind the lapel sits a loop for a flower"), ("H4", "concrete_risk", "Without a flower, this hole simply stays empty"),
               ("H5", "demonstration", "What belongs in this buttonhole?")],
        visual="Jacket, loupe on the buttonhole in the left lapel",
    ),
}


def _tags(rows):
    return [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in rows]


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"] if 1 <= i <= 3 else ["S1"], t["visual"]) for i, (h, ty, os) in enumerate(t["hooks"])]
    a3, a4 = t["b3_at"], t["b4_at"]
    objs = [(HOLE, {"flower": True}, "then"), (FLOWER, None, "ring"), (FLOWER_SB1, None, "ring")]
    items = []
    for (title, sub, at, second), (obj, then, mode) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if mode == "then":
            it.update({"then": then, "then_at": second})
        else:
            it.update({"ring": "lapel_hole", "ring_at": second})
        items.append(it)
    s0_title, s0_tags = t["b5_s0"]
    s1_title, s1_at, s1_tags = t["b5_s1"]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": HOLE, "target": "lapel_hole", "badge": "?", "question_at": 0.3, **t["hook_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "stages": [{"object": HOLE, "at": 0.0, "title": t["b2_stage"], "tags": _tags(t["b2_tags"])}],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": t["b2_marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "from": HOLE, "to": FLOWER, "target": "lapel_hole", "zoom": 1.6, "label": t["b3_label"],
                  "strain": False, "backdrop": True, "hold_end": True, **a3},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 10, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": HOLE, "target": "lapel_hole", "tag": t["b4_l"][1]},
                  "right": {"title": t["b4_r"][0], "object": FLOWER, "tag": t["b4_r"][1],
                            "pulses": [{"target": "lapel_hole", "at": a4["p1"]}, {"target": "lapel_r", "at": a4["p2"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "backdrop": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": a4["marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "stages": [{"object": HOLE, "at": 0.0, "title": s0_title, "tags": _tags(s0_tags)},
                             {"object": DINNER, "at": s1_at, "title": s1_title, "tags": _tags(s1_tags)}],
                  "hold_end": True},
         "source_ids": ["S3"], "overlay": {"marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2"], "overlay": {"marker": "auslegung", "marker_at": t["b6_marker"]}},
        closing_beat(lang, t["b7"], HOLE, FLOWER, "lapel_hole", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"],
                 notes="Suitwerk Woche 1 (Vorlage 1.0). Thema B05 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; keine Herkunftsgeschichte, Debrett's ausdrücklich im Hochzeitskontext.",
                 sources=SOURCES, hooks=hooks, hook_note="Ein Knopfloch ohne Knopf: das Rätsel, das das Video auflöst.",
                 beats=beats, status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Herkunftsgeschichten (Royals, Legenden) nicht belegt; nicht im Video.",
                             "Debrett's beschreibt das Anstecken für Hochzeiten; für den Alltag nur, dass das Knopfloch dafür gedacht ist."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
