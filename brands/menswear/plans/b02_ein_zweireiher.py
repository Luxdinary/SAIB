"""B02 Einreiher oder Zweireiher: der Überschlag erklärt (10.11.2026, Thema 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261110-3"
SB = {"kind": "jacket", "variant": "sb2", "fastened": [0], "strain": False}
DB = {"kind": "jacket", "variant": "db6", "fastened": [0], "strain": False}
DB_ALL = {"kind": "jacket", "variant": "db6", "fastened": [0, 1], "strain": False}
DB_OPEN = {"kind": "jacket", "variant": "db6", "fastened": [], "strain": False}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://www.anderson-sheppard.co.uk/thenotebook/why-i-prefer-double-breasteds/", "title": "Anderson & Sheppard, Why I prefer double-breasteds: zum geschlossenen Tragen gemacht; Überschlag anpassbar für mehr oder weniger Hemd; Schnitt und Anprobe müssen Bewegung im geschlossenen Zustand erlauben", "checked_at": CHECKED, "label": "Anderson & Sheppard"},
    {"id": "S2", "url": "https://www.moss.co.uk/inside-pocket/post/spotlight-on-the-double-breasted-suit", "title": "Moss, Spotlight on the double-breasted suit: offen tragen geht, Linien sind für geschlossen entworfen; traditionell bis zu acht Knöpfe, Moss nimmt sechs; äußeren untersten Knopf nicht schließen", "checked_at": CHECKED, "label": "Moss, Inside Pocket"},
]

T = {
    "de": dict(
        title="Einreiher oder Zweireiher: der Überschlag erklärt",
        q="Zweireiher: offen oder zu?",
        b1="Zwei Knopfreihen, und die Vorderteile überlappen. Darfst du einen Zweireiher offen tragen, oder gehört er zu?",
        b1_at=dict(badge_at="w:Knopfreihen", loupe_at="w:Knopfreihen", nie_at="w:offen"),
        b2="Beim Einreiher treffen sich die Vorderteile in der Mitte. Beim Zweireiher überlappen sie, mit zwei Knopfreihen. Moss sagt: Offen tragen geht. Aber die senkrechten Linien sind für den geschlossenen Zustand entworfen.",
        b2_head="Mitte oder Überschlag?", b2_label="Linien: für geschlossen",
        b2_at=dict(pointer_at="w:Einreiher", zoom_at="w:Mitte", flip_at="w:Zweireiher", label_at="w:Linien"),
        b3="Für Anderson and Sheppard ist der Zweireiher zum geschlossenen Tragen gemacht. Der Überschlag lässt sich anpassen, um mehr oder weniger Hemd zu zeigen. Schnitt und Anprobe müssen dafür Bewegung im geschlossenen Zustand erlauben.",
        b3_head="So ist er gedacht", b3_stage="Geschlossen",
        b3_tags=[("button:0", "zum Schließen", "so geschnitten", "w:geschlossenen"),
                 ("break", "Überschlag", "mehr oder weniger Hemd", "w:Überschlag"),
                 ("waist", "Bewegung", "auch geschlossen", "w:Bewegung")],
        b4="Und wie schließt du ihn? Moss arbeitet mit sechs Knöpfen, traditionell waren es bis zu acht. Den äußeren untersten Knopf schließt du laut Moss nicht, er bleibt offen.",
        b4_head="Welcher bleibt offen?", b4_label="außen unten: offen",
        b4_at=dict(pointer_at="w:schließt", all_at="w:sechs", zoom_at="w:äußeren", error_at="w:untersten", flip_at="w:nicht", label_at="w:bleibt"),
        b5="Beide Häuser sind sich also nah, aber nicht gleich. Anderson and Sheppard schneidet für geschlossen, Moss lässt dir die Wahl. Welche Knöpfe genau zu sind, hängt von der Knopfstellung ab; eine allgemeine Regel geben die Quellen nicht.",
        b5_head="Zwei Häuser, eine Linie", b5_l=("Der Schneider", "zum Schließen gemacht"), b5_r=("Der Ausstatter", "offen geht auch"),
        b5_tag2="je nach Knopfstellung",
        b5_at=dict(left_at="w:Anderson", left_tag_at="w:geschlossen", right_at="w:Moss", right_tag_at="w:Wahl", tag2_at="w:Knopfstellung", rpulse="w:Knöpfe"),
        b6="Kurz gesagt: Der Zweireiher ist laut Anderson and Sheppard in der Regel zum Schließen gedacht. Offen tragen geht laut Moss. Und den äußeren untersten Knopf lässt du offen.",
        b6_head="Kurz gesagt",
        b6_items=[("In der Regel zu", "so geschnitten, laut A&S", "w:Zweireiher", "w:Schließen"),
                  ("Offen geht", "Linien für geschlossen (Moss)", "w:Offen", "w:Moss"),
                  ("Außen unten: offen", "der äußere unterste Knopf", "w:äußeren", "w:offen#2")],
        b7="Zwei Reihen, ein Überschlag, und in der Regel geschlossen getragen. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="In der Regel: zu.", b7_at=dict(fix_at="w:Regel", ring_at="w:geschlossen", statement_at="w:getragen", chip_at="w:Blick"),
        status="Sakko, zweireihig",
        states=["Zweireiher: ?", "offen geht, aber", "zum Schließen", "außen unten: offen", "Knopfstellung offen", "in der Regel zu", "geschlossen"],
        desc="Einreiher oder Zweireiher? Beim Zweireiher überlappen die Vorderteile. Anderson & Sheppard schneidet ihn zum Schließen, Moss erlaubt ihn offen und lässt den äußeren untersten Knopf offen.",
        tags=["herrenmode", "zweireiher", "sakko", "anzug", "stilregeln"],
        hooks=[("H1", "question", "Zweireiher: offen oder zu?", []),
               ("H2", "misconception", "Zweireiher offen tragen? Geht, aber er ist anders gedacht.", ["S1", "S2"]),
               ("H3", "surprising_fact", "Traditionelle Zweireiher hatten bis zu acht Knöpfe", ["S2"]),
               ("H4", "concrete_risk", "Den äußeren untersten Knopf lässt du offen", ["S2"]),
               ("H5", "demonstration", "Wie viel Hemd zeigt dein Zweireiher?", [])],
    ),
    "en": dict(
        title="Single or double-breasted: the wrap explained",
        q="Double-breasted: open or closed?",
        b1="Two rows of buttons, and the fronts overlap. Can you wear a double-breasted jacket open, or does it belong closed?",
        b1_at=dict(badge_at="w:rows", loupe_at="w:rows", nie_at="w:open"),
        b2="On a single-breasted jacket, the fronts meet in the middle. On a double-breasted one, they overlap, with two rows of buttons. Moss says wearing it open is fine. But its vertical lines are designed to be seen closed.",
        b2_head="Middle or overlap?", b2_label="Lines designed for closed",
        b2_at=dict(pointer_at="w:single", zoom_at="w:middle", flip_at="w:double", label_at="w:vertical"),
        b3="For Anderson and Sheppard, the double-breasted jacket is made to be worn closed. The overlap can be adjusted to show more or less shirt. So the cut and the fitting must allow movement while it is closed.",
        b3_head="How it is meant", b3_stage="Closed",
        b3_tags=[("button:0", "made to close", "cut that way", "w:closed"),
                 ("break", "the overlap", "more or less shirt", "w:overlap"),
                 ("waist", "movement", "even when closed", "w:movement")],
        b4="So how do you fasten it? Moss works with six buttons; traditional ones had up to eight. The outer bottom button, says Moss, you do not fasten. It stays open.",
        b4_head="Which one stays open?", b4_label="Outer bottom button: open",
        b4_at=dict(pointer_at="w:fasten", all_at="w:six", zoom_at="w:outer", error_at="w:bottom", flip_at="w:not", label_at="w:stays"),
        b5="So the two houses are close, but not identical. Anderson and Sheppard cut for closed, Moss leaves you the choice. Which buttons exactly you fasten depends on the button stance; the sources give no general rule.",
        b5_head="Two houses, one line", b5_l=("The tailor", "made to be closed"), b5_r=("The outfitter", "open works too"),
        b5_tag2="depends on button stance",
        b5_at=dict(left_at="w:Anderson", left_tag_at="w:closed", right_at="w:Moss", right_tag_at="w:choice", tag2_at="w:stance", rpulse="w:buttons"),
        b6="In short: for Anderson and Sheppard, a double-breasted jacket is generally meant to be closed. Moss says open works. And the outer bottom button stays undone.",
        b6_head="In short",
        b6_items=[("Generally closed", "cut that way, says A&S", "w:double", "w:closed"),
                  ("Open works", "lines meant for closed (Moss)", "w:Moss", "w:works"),
                  ("Outer bottom: open", "the outer bottom button", "w:outer", "w:undone")],
        b7="Two rows, one overlap, and generally worn closed. For more eye for detail: follow Suitwerk.",
        b7_stmt="Generally: closed.", b7_at=dict(fix_at="w:generally", ring_at="w:closed", statement_at="w:closed", chip_at="w:eye"),
        status="Double-breasted",
        states=["double: ?", "open works, but", "made to close", "outer bottom: open", "stance: open question", "generally closed", "closed"],
        desc="Single or double-breasted? On a double-breasted jacket the fronts overlap. Anderson & Sheppard cut it to be closed, Moss allows it open and leaves the outer bottom button undone.",
        tags=["menswear", "doublebreasted", "suitjacket", "suit", "styletips"],
        hooks=[("H1", "question", "Double-breasted: open or closed?", []),
               ("H2", "misconception", "Wear a double-breasted open? You can, but it is meant closed.", ["S1", "S2"]),
               ("H3", "surprising_fact", "Traditional double-breasteds had up to eight buttons", ["S2"]),
               ("H4", "concrete_risk", "The outer bottom button stays undone", ["S2"]),
               ("H5", "demonstration", "How much shirt does your double-breasted show?", [])],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Zweireiher, Lupe auf dem äußeren untersten Knopf") for h, ty, os, src in t["hooks"]]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": "always", "at": at} for sp, tx, sub, at in t["b3_tags"]]
    objs = [(DB, None, "button:0"), (DB, {"fastened": []}, None), (DB_ALL, {"fastened": [0]}, None)]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": DB, "target": "button:1", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "from": SB, "to": DB, "target": "break", "zoom": 1.4, "label": t["b2_label"],
                  "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": "w:Moss"}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": DB, "at": 0.0, "title": t["b3_stage"], "tags": tags}],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Anderson"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 10, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": DB_ALL, "to": DB, "target": "button:1", "zoom": 1.5, "label": t["b4_label"],
                  "backdrop": True, "hold_end": True, **a4},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 360, "y": 917, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a4["all_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "left": {"title": t["b5_l"][0], "object": DB, "target": "button:0", "tag": t["b5_l"][1]},
                  "right": {"title": t["b5_r"][0], "object": DB_OPEN, "tag": t["b5_r"][1], "tag2": t["b5_tag2"], "tag2_at": a5["tag2_at"],
                            "pulses": [{"target": "button:0", "at": a5["rpulse"], "tone": "amber"}]},
                  "left_at": a5["left_at"], "left_tag_at": a5["left_tag_at"], "right_at": a5["right_at"], "right_tag_at": a5["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": a5["left_at"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], DB_OPEN, DB, "button:0", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema B02 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S2; 'in der Regel' statt 'immer', keine allgemeine Regel zur Knopfstellung.",
                 sources=SOURCES, hooks=hooks, hook_note="Die Frage offen oder zu, die Lupe auf dem äußeren untersten Knopf.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Welche Knöpfe genau schließen: hängt von der Knopfstellung ab, keine allgemeine Regel in den Quellen.",
                             "Offen getragener Zweireiher: keine eigene Zeichnung; 'offen' ist im Bild nur an den Knöpfen zu sehen."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
