"""B01 Revers: fallend, steigend oder Schal (09.11.2026, Thema 2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261109-2"
NOTCH = {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel": "notch"}
PEAK = {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel": "peak"}
DB_PEAK = {"kind": "jacket", "variant": "db6", "fastened": [0], "lapel": "peak"}
DAY_SHAWL = {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel": "shawl"}
DJ_PEAK = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "peak", "dinner": True, "neck": "bow", "strain": False}
DJ_SHAWL = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "shawl", "dinner": True, "neck": "bow", "strain": False}
DJ_DB = {"kind": "jacket", "variant": "db6", "fastened": [0], "lapel": "peak", "dinner": True, "neck": "bow", "strain": False}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://moss.co.uk/inside-pocket/post/everything-you-need-to-know-about-lapels", "title": "Moss, Everything you need to know about lapels: die meisten Einreiher und Blazer haben fallendes Revers, Schalkragen meist nur am Dinnerjacket, steigendes Revers ist die angezogenere Variante", "checked_at": CHECKED, "label": "Moss, Inside Pocket"},
    {"id": "S2", "url": "https://www.anderson-sheppard.co.uk/thenotebook/linen-checked-jacket-with-peak-lapel/", "title": "Anderson & Sheppard, Linen checked jacket with peak lapel: steigendes Revers meist am Zweireiher, im Vergleich zum fallenden recht formell", "checked_at": CHECKED, "label": "Anderson & Sheppard"},
    {"id": "S3", "url": "https://debretts.com/deconstructing-dress-codes/", "title": "Debrett's, Deconstructing Dress Codes: Dinnerjacket mit seidenbelegtem steigendem Revers oder Schalkragen, ein- oder zweireihig", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
    {"id": "S4", "url": "https://www.woolmark.com/ko/z.archive/archive-industry/suiting/black-tie-dress-code-explained/", "title": "Woolmark, Black tie dress code explained: steigendes Revers ist der formellste Stil, ein- wie zweireihig; Schalkragen als feine Variante", "checked_at": CHECKED, "label": "Woolmark, Black Tie"},
]

T = {
    "de": dict(
        title="Revers: fallend, steigend oder Schal",
        q="Fallend, steigend oder Schal?",
        b1="Drei Reversformen, und jede sagt etwas anderes über dein Sakko. Fallend, steigend oder Schal: Woran erkennst du, wofür sie stehen?",
        b1_at=dict(badge_at="w:Fallend", loupe_at="w:Fallend", nie_at="w:Woran"),
        b2="Zwei Sakkos, gleicher Schnitt, nur das Revers ist anders. Links hat es eine Kerbe am Kragen, das ist fallend. Rechts zeigen die Spitzen nach oben, das ist steigend. Laut Moss ist das steigende Revers die angezogenere Variante.",
        b2_head="Kerbe oder Spitze?", b2_l=("Fallend", "Kerbe am Kragen"), b2_r=("Steigend", "die angezogenere Variante"),
        b2_at=dict(left_at="w:Links", left_tag_at="w:Kerbe", right_at="w:Rechts", right_tag_at="w:Moss", lpulse="w:fallend", rpulse="w:Spitzen"),
        b3="Wo sitzt welches Revers? Laut Moss haben die meisten Einreiher und Blazer ein fallendes Revers. Das steigende findet sich laut Anderson and Sheppard meist am Zweireiher und gilt im Vergleich als recht formell.",
        b3_head="Wo sitzt welches?",
        b3_st=[("Einreiher", [("lapel", "fallend", "Einreiher, Blazer", "w:Einreiher"), ("lapel_r", "der Normalfall", "laut Moss", "w:fallendes")]),
               ("Zweireiher", [("lapel", "steigend", "meist am Zweireiher", "w:Zweireiher"), ("lapel_r", "recht formell", "Anderson & Sheppard", "w:formell")])],
        b3_stage2="w:steigende",
        b4="Beim Dinnerjacket wird die Auswahl kleiner. Debrett's nennt seidenbelegtes steigendes Revers oder Schalkragen, ein- oder zweireihig. Den Schalkragen sieht man laut Moss normalerweise nur dort.",
        b4_head="Und am Smoking?", b4_label="Schal: meist am Dinnerjacket",
        b4_at=dict(pointer_at="w:Dinnerjacket", zoom_at="w:Debrett", flip_at="w:Schalkragen", label_at="w:Moss"),
        b5="Meist heißt aber nicht immer. Woolmark nennt das steigende Revers beim Smoking den formellsten Stil, einreihig wie zweireihig. Anderson and Sheppard zeigt es sogar an einem karierten Leinensakko. Steigend heißt also nicht automatisch Zweireiher.",
        b5_head="Nur am Zweireiher?", b5_l=("Einreihig", "formellster Stil"), b5_r=("Zweireihig", "nicht nur hier"),
        b5_at=dict(left_at="w:Meist", left_tag_at="w:einreihig", right_at="w:zweireihig", right_tag_at="w:automatisch", lpulse="w:formellsten", rpulse="w:Anderson", marker="w:Woolmark"),
        b6="Kurz gesagt: Fallend ist der Normalfall an Einreihern und Blazern. Steigend wirkt formeller und sitzt meist am Zweireiher. Und den Schalkragen siehst du meist nur am Dinnerjacket.",
        b6_head="Kurz gesagt",
        b6_items=[("Fallend: Normalfall", "Einreiher und Blazer, laut Moss", "w:Fallend", "w:Normalfall"),
                  ("Steigend: formeller", "meist am Zweireiher", "w:Steigend", "w:Zweireiher"),
                  ("Schal: Dinnerjacket", "dort mit Seide belegt", "w:Schalkragen", "w:Dinnerjacket")],
        b7="Fallend als Normalfall, steigend formeller, Schal fürs Dinnerjacket. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Schal: Black Tie.", b7_at=dict(fix_at="w:Schal", ring_at="w:Dinnerjacket", statement_at="w:Dinnerjacket", chip_at="w:Blick"),
        status="Revers",
        states=["Revers: ?", "fallend oder steigend", "Einreiher: fallend", "Smoking: zwei Formen", "auch am Einreiher", "drei Formen", "Schal: Dinnerjacket"],
        desc="Fallend, steigend oder Schal: was die Reversform über ein Sakko sagt. Nach Moss, Anderson & Sheppard, Debrett's und Woolmark, mit dem Blick aufs Dinnerjacket.",
        tags=["herrenmode", "revers", "sakko", "smoking", "stilregeln"],
        hooks=[("H1", "question", "Fallend, steigend oder Schal?", []),
               ("H2", "misconception", "Steigendes Revers? Nicht nur am Zweireiher.", ["S2", "S4"]),
               ("H3", "surprising_fact", "Den Schalkragen siehst du meist nur am Smoking", ["S1"]),
               ("H4", "concrete_risk", "Schal am Tagesanzug? Moss kennt ihn vom Dinnerjacket.", ["S1", "S3"]),
               ("H5", "demonstration", "Eine Kerbe am Kragen, und das Sakko wirkt anders", [])],
    ),
    "en": dict(
        title="Notch, peak or shawl: what the lapel says",
        q="Notch, peak or shawl?",
        b1="Three lapel styles, each with its own message. Notch, peak or shawl: how do you read them?",
        b1_at=dict(badge_at="w:Notch", loupe_at="w:Notch", nie_at="w:how"),
        b2="Two jackets, same cut, different lapels. On the left, a notch where lapel meets collar. On the right, the points rise upwards: that is a peak. According to Moss, the peak is the dressier option.",
        b2_head="Notch or peak?", b2_l=("Notch", "a notch at the collar"), b2_r=("Peak", "the dressier option"),
        b2_at=dict(left_at="w:left", left_tag_at="w:notch", right_at="w:right", right_tag_at="w:Moss", lpulse="w:collar", rpulse="w:points"),
        b3="Where does each belong? Moss says most single-breasted jackets and blazers have a notch lapel. The peak, according to Anderson and Sheppard, is mostly found on double-breasted jackets, and is quite formal by comparison.",
        b3_head="Where does each belong?",
        b3_st=[("Single-breasted", [("lapel", "notch", "jackets and blazers", "w:blazers"), ("lapel_r", "the usual case", "according to Moss", "w:notch")]),
               ("Double-breasted", [("lapel", "peak", "mostly double-breasted", "w:double"), ("lapel_r", "quite formal", "Anderson & Sheppard", "w:formal")])],
        b3_stage2="w:peak",
        b4="On a dinner jacket the choice narrows. Debrett's lists a silk-faced peak lapel or a shawl collar, single or double-breasted. And Moss says you will normally only see the shawl on a dinner jacket.",
        b4_head="And on a dinner jacket?", b4_label="Shawl: mostly dinner jackets",
        b4_at=dict(pointer_at="w:dinner", zoom_at="w:Debrett", flip_at="w:shawl", label_at="w:Moss"),
        b5="Mostly does not mean always. Woolmark calls the peak the most formal style for a dinner jacket, single or double-breasted. Anderson and Sheppard even show one on a checked linen jacket. So a peak does not automatically mean double-breasted.",
        b5_head="Only double-breasted?", b5_l=("Single", "the most formal style"), b5_r=("Double", "not only here"),
        b5_at=dict(left_at="w:Mostly", left_tag_at="w:single", right_at="w:double", right_tag_at="w:automatically", lpulse="w:formal", rpulse="w:Anderson", marker="w:Woolmark"),
        b6="In short: the notch is the usual choice on single-breasted jackets and blazers. The peak is dressier and mostly sits on a double-breasted jacket. And the shawl collar you will mostly see only on a dinner jacket.",
        b6_head="In short",
        b6_items=[("Notch: the usual case", "single-breasted, blazers (Moss)", "w:notch", "w:usual"),
                  ("Peak: dressier", "mostly double-breasted", "w:peak", "w:double"),
                  ("Shawl: dinner jacket", "silk-faced there", "w:shawl", "w:dinner")],
        b7="Notch as the norm, peak for formality, shawl for the dinner jacket. For more eye for detail: follow Suitwerk.",
        b7_stmt="Shawl: black tie.", b7_at=dict(fix_at="w:shawl", ring_at="w:dinner", statement_at="w:dinner", chip_at="w:eye"),
        status="Lapels",
        states=["lapel: ?", "notch or peak", "single: notch", "dinner: two styles", "peak: single too", "three styles", "shawl: dinner jacket"],
        desc="Notch, peak or shawl: what the lapel says about a jacket. Based on Moss, Anderson & Sheppard, Debrett's and Woolmark, with a look at the dinner jacket.",
        tags=["menswear", "lapels", "suitjacket", "blacktie", "styletips"],
        hooks=[("H1", "question", "Notch, peak or shawl?", []),
               ("H2", "misconception", "Peak lapels? Not only on double-breasted.", ["S2", "S4"]),
               ("H3", "surprising_fact", "The shawl collar mostly lives on dinner jackets", ["S1"]),
               ("H4", "concrete_risk", "A shawl on a day suit? Moss knows it from dinner jackets.", ["S1", "S3"]),
               ("H5", "demonstration", "One notch at the collar changes the whole jacket", [])],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Sakko mit fallendem Revers, Lupe auf der Kerbe am Kragen") for h, ty, os, src in t["hooks"]]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    stages = []
    for k, ((title, tags), obj) in enumerate(zip(t["b3_st"], (NOTCH, DB_PEAK))):
        stages.append({"object": obj, "at": 0.0 if k == 0 else t["b3_stage2"], "title": title,
                       "tags": [{"spot": sp, "text": tx, "sub": sub, "tone": "always", "at": at} for sp, tx, sub, at in tags]})
    objs = [(NOTCH, None, "notch"), (PEAK, {"variant": "db6"}, None), (DAY_SHAWL, {"variant": "sb1", "dinner": True, "neck": "bow"}, None)]
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
         "data": {"question": t["q"], "object": NOTCH, "target": "notch", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": NOTCH, "target": "notch", "tag": t["b2_l"][1], "pulses": [{"target": "notch", "at": a2["lpulse"]}]},
                  "right": {"title": t["b2_r"][0], "object": PEAK, "tag": t["b2_r"][1], "pulses": [{"target": "notch", "at": a2["rpulse"]}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": a2["right_tag_at"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": stages, "backdrop": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Moss"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": DJ_PEAK, "to": DJ_SHAWL, "target": "lapel", "zoom": 1.4, "label": t["b4_label"],
                  "hold_end": True, **a4},
         "source_ids": ["S3", "S1"], "overlay": {"vignette": True, "marker": "fakt", "marker_at": a4["zoom_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "left": {"title": t["b5_l"][0], "object": DJ_PEAK, "target": "notch", "tag": t["b5_l"][1], "pulses": [{"target": "notch", "at": a5["lpulse"]}]},
                  "right": {"title": t["b5_r"][0], "object": DJ_DB, "tag": t["b5_r"][1], "pulses": [{"target": "notch", "at": a5["rpulse"]}]},
                  "left_at": a5["left_at"], "left_tag_at": a5["left_tag_at"], "right_at": a5["right_at"], "right_tag_at": a5["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S4", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": a5["marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], DAY_SHAWL, DJ_SHAWL, "lapel", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema B01 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S4; 'meist' statt 'immer', keine Herkunft der Reversformen.",
                 sources=SOURCES, hooks=hooks, hook_note="Die drei Namen als Frage, die Lupe zeigt die Kerbe.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Herkunft der Reversformen: nicht belegt, nicht im Video.",
                             "Kariertes Leinensakko mit steigendem Revers: nur gesprochen (S2), keine eigene Zeichnung."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
