"""B03 Rückenschlitz: keiner, einer, zwei (12.11.2026, menswear-20261112-1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261112-1"
NONE = {"kind": "jacket_back", "vents": "none"}
CENTRE = {"kind": "jacket_back", "vents": "centre"}
SIDE = {"kind": "jacket_back", "vents": "side"}
DINNER = {"kind": "jacket", "variant": "sb1", "fastened": [0], "dinner": True, "lapel": "shawl", "neck": "bow"}
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://www.woolmark.com/hk/z.archive/archive-industry/suiting/on-the-row-henry-poole/", "title": "Woolmark, On the Row: Henry Poole: Anzug mit oder ohne Seitenschlitze, auf Wunsch Mittelschlitz; die Grundform bleibt gleich", "checked_at": CHECKED, "label": "Woolmark, Henry Poole"},
        {"id": "S2", "url": "https://debretts.com/etiquette-category/events-and-dress-codes/", "title": "Debrett's, Events and dress codes: Black-Tie-Dinnerjacket ein- oder zweireihig, ohne Schlitze", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
        {"id": "S3", "url": "https://www.woolmark.com/ko/z.archive/archive-industry/suiting/black-tie-dress-code-explained/", "title": "Woolmark, Black tie dress code explained: ohne Schlitz bevorzugt, Doppelschlitz akzeptabel, Einzelschlitz meiden, weil zu lässig", "checked_at": CHECKED, "label": "Woolmark, Black Tie"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Rückenschlitz: keiner, einer oder zwei?",
        q="Keiner, einer oder zwei?",
        b1="Dreh das Sakko einmal um. Hinten unten gibt es drei Möglichkeiten: kein Schlitz, einer in der Mitte oder zwei an den Seiten. Welche ist richtig?",
        b1_at=dict(badge_at="w:Hinten", loupe_at="w:zwei", nie_at="w:Welche"),
        b2="Am Tagesanzug gibt es darauf keine feste Antwort. Die Schneiderei Henry Poole an der Londoner Savile Row fertigt Anzüge mit oder ohne Seitenschlitze. Auf Wunsch kommt statt der zwei ein Mittelschlitz. Die Grundform des Anzugs bleibt dabei gleich.",
        b2_head="Am Tagesanzug", b2_label="Schlitz nach Kundenwunsch",
        b2_at=dict(pointer_at="w:Henry", zoom_at="w:Seitenschlitze", flip_at="w:Mittelschlitz", label_at="w:Grundform"),
        b3="Am Abend sieht das anders aus. Für das Dinnerjacket, also den Smoking, schreibt der britische Etikette-Ratgeber Debrett's: ein- oder zweireihig, aber ohne Schlitze. Hinten bleibt der Stoff also geschlossen.",
        b3_head="Am Smoking", b3_l=("Vorne", "ein- oder zweireihig"), b3_r=("Hinten", "ohne Schlitz"),
        b3_at=dict(left_at="w:Dinnerjacket", left_tag_at="w:zweireihig", right_at="w:ohne", right_tag_at="w:Hinten", pulse="w:geschlossen", mark="w:Debrett"),
        b4="Für den Smoking ordnet Woolmark es noch genauer: Ohne Schlitz ist bevorzugt. Zwei Seitenschlitze sind akzeptabel. Einen Mittelschlitz solltest du meiden, er gilt als zu lässig.",
        b4_head="Smoking, laut Woolmark",
        b4_items=[("Ohne Schlitz: bevorzugt", "die erste Wahl", "w:Ohne", "w:bevorzugt"),
                  ("Zwei Schlitze: akzeptabel", "an den Seiten", "w:Zwei", "w:akzeptabel"),
                  ("Mittelschlitz: meiden", "gilt als zu lässig", "w:Einen", "w:lässig")],
        b4_mark="w:Woolmark",
        b5="Der Mittelschlitz ist also kein Fehler an sich. Am Tagesanzug ist er eine Frage des Geschmacks, Henry Poole fertigt ihn auf Wunsch. Nur am Smoking gilt er als zu lässig.",
        b5_head="Derselbe Schlitz", b5_s1="Tagesanzug", b5_s2="Smoking",
        b5_t1=("nach Geschmack", "Henry Poole: auf Wunsch", "sometimes", "w:Tagesanzug"),
        b5_t2=("zu lässig", "laut Woolmark", "never", "w:gilt"), b5_s2_at="w:Nur", b5_mark="w:Henry",
        b6="Kurz gesagt: Am Tagesanzug wählst du frei, ob keiner, einer oder zwei Schlitze. Am Smoking ist ohne Schlitz die erste Wahl, zwei gehen auch, einer eher nicht.",
        b6_head="Kurz gesagt", b6_l=("Tagesanzug", "keiner, einer, zwei", "nach Wunsch"), b6_r=("Smoking", "am besten ohne", "zwei gehen auch"),
        b6_at=dict(left_at="w:Tagesanzug", left_tag_at="w:keiner", left_tag2="w:frei", right_at="w:Smoking", right_tag_at="w:erste",
                   right_tag2="w:zwei#2", pulse="w:ohne"),
        b7="Tagsüber nach Wunsch, abends am besten ohne. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Abends: ohne Schlitz.", b7_at=dict(fix_at="w:abends", ring_at="w:besten", statement_at="w:ohne", chip_at="w:Blick"),
        status="Sakko, Rücken",
        states=["Schlitz: ?", "Tag: nach Wunsch", "Smoking: ohne", "einer: zu lässig", "Mitte: je nach Anlass", "Tag frei, Abend ohne", "Abend: ohne Schlitz"],
        desc="Rückenschlitz am Sakko: keiner, einer oder zwei? Am Tagesanzug Kundenwunsch (Henry Poole), am Smoking ohne Schlitz bevorzugt, zwei akzeptabel, Mittelschlitz zu lässig (Debrett's, Woolmark).",
        tags=["herrenmode", "sakko", "smoking", "maßschneiderei", "anzug"],
        hooks=[("H1", "question", "Keiner, einer oder zwei?"), ("H2", "misconception", "Mittelschlitz falsch? Nur am Smoking."),
               ("H3", "surprising_fact", "Am Tagesanzug entscheidet der Kunde"), ("H4", "concrete_risk", "Mittelschlitz am Smoking gilt als zu lässig"),
               ("H5", "demonstration", "Dreh das Sakko um: Was siehst du?")],
    ),
    "en": dict(
        title="Jacket vents: none, one or two?",
        q="None, one or two?",
        b1="Turn the jacket around. Down at the back there are three options: no vent, one in the centre, or two at the sides. Which one is right?",
        b1_at=dict(badge_at="w:back", loupe_at="w:two", nie_at="w:Which"),
        b2="On a day suit there is no fixed answer. Henry Poole, a Savile Row tailor, makes suits with or without side vents. On request, a single centre vent replaces the two. The basic shape stays the same.",
        b2_head="On a day suit", b2_label="Vent to the client's wish",
        b2_at=dict(pointer_at="w:Henry", zoom_at="w:side", flip_at="w:centre", label_at="w:basic"),
        b3="In the evening it changes. For the dinner jacket, Debrett's, the British etiquette guide, says: single or double-breasted, but without vents. So the back stays closed.",
        b3_head="On a dinner jacket", b3_l=("Front", "single or double-breasted"), b3_r=("Back", "no vent"),
        b3_at=dict(left_at="w:dinner", left_tag_at="w:single", right_at="w:without", right_tag_at="w:So", pulse="w:closed", mark="w:Debrett"),
        b4="For the dinner jacket, Woolmark ranks it more precisely: no vent is preferred. Two side vents are acceptable. A single centre vent is best avoided; it counts as too casual.",
        b4_head="Dinner jacket, per Woolmark",
        b4_items=[("No vent: preferred", "the first choice", "w:no", "w:preferred"),
                  ("Two vents: acceptable", "at the sides", "w:Two", "w:acceptable"),
                  ("Centre vent: avoid", "counts as too casual", "w:single", "w:casual")],
        b4_mark="w:Woolmark",
        b5="So the centre vent is not a fault in itself. On a day suit it is a matter of taste, and Henry Poole makes it on request. Only on a dinner jacket does it count as too casual.",
        b5_head="The same vent", b5_s1="Day suit", b5_s2="Dinner jacket",
        b5_t1=("a matter of taste", "Henry Poole: on request", "sometimes", "w:day"),
        b5_t2=("too casual", "per Woolmark", "never", "w:count"), b5_s2_at="w:Only", b5_mark="w:Henry",
        b6="In short: on a day suit you choose freely, none, one or two vents. On a dinner jacket, no vent is the first choice, two will do, one rather not.",
        b6_head="In short", b6_l=("Day suit", "none, one or two", "your choice"), b6_r=("Dinner jacket", "best without", "two will do"),
        b6_at=dict(left_at="w:day", left_tag_at="w:none", left_tag2="w:freely", right_at="w:dinner", right_tag_at="w:first",
                   right_tag2="w:two#2", pulse="w:vent#2"),
        b7="By day as you wish, in the evening best without. For more eye for detail: follow Suitwerk.",
        b7_stmt="Evenings: no vent.", b7_at=dict(fix_at="w:evening", ring_at="w:best", statement_at="w:without", chip_at="w:eye"),
        status="Jacket, back",
        states=["vent: ?", "day: your choice", "dinner: no vent", "single: too casual", "centre: by occasion", "day free, evening none", "evening: no vent"],
        desc="Jacket vents: none, one or two? On a day suit it is the client's choice (Henry Poole); on a dinner jacket no vent is preferred, two are acceptable and a centre vent counts as too casual (Debrett's, Woolmark).",
        tags=["menswear", "jacket", "blacktie", "tailoring", "suit"],
        hooks=[("H1", "question", "None, one or two?"), ("H2", "misconception", "A centre vent is wrong? Only on a dinner jacket."),
               ("H3", "surprising_fact", "On a day suit, the client decides"), ("H4", "concrete_risk", "A centre vent makes a dinner jacket too casual"),
               ("H5", "demonstration", "Turn the jacket around: what do you see?")],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S3"], "Sakko von hinten, Lupe auf dem Seitenschlitz") for h, ty, os in t["hooks"]]
    a2, a3, a6 = t["b2_at"], t["b3_at"], t["b6_at"]
    i1, i2, i3 = t["b4_items"]
    cards = [
        {"title": i1[0], "sub": i1[1], "object": NONE, "at": i1[2], "ring": "hem", "ring_at": i1[3]},
        {"title": i2[0], "sub": i2[1], "object": SIDE, "at": i2[2], "ring": "vent_l", "ring_at": i2[3], "ring_tone": "amber"},
        {"title": i3[0], "sub": i3[1], "object": CENTRE, "at": i3[2], "ring": "vent", "ring_at": i3[3], "ring_tone": "red"},
    ]

    def tag(row):
        tx, sub, tone, at = row
        return [{"spot": "vent", "text": tx, "sub": sub, "tone": tone, "at": at}]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 8, "spoken": t["b1"],
         "data": {"question": t["q"], "object": SIDE, "target": "vent_l", "badge": "?", "question_at": 0.3, "hold_end": True, **t["b1_at"]},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 15, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "object": SIDE, "from": SIDE, "to": CENTRE, "target": "vent", "zoom": 1.3,
                  "label": t["b2_label"], "strain": False, "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a2["pointer_at"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_compare", "duration_hint": 11, "spoken": t["b3"],
         "data": {"headline": t["b3_head"],
                  "left": {"title": t["b3_l"][0], "object": DINNER, "tag": t["b3_l"][1]},
                  "right": {"title": t["b3_r"][0], "object": NONE, "target": "hem", "tag": t["b3_r"][1],
                            "pulses": [{"target": "hem", "at": a3["pulse"]}]},
                  "left_at": a3["left_at"], "left_tag_at": a3["left_tag_at"], "right_at": a3["right_at"], "right_tag_at": a3["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": a3["mark"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "items": cards, "backdrop": True, "hold_end": True},
         "source_ids": ["S3"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b4_mark"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 11, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": [
             {"object": CENTRE, "at": 0.0, "title": t["b5_s1"], "tags": tag(t["b5_t1"])},
             {"object": CENTRE, "at": t["b5_s2_at"], "title": t["b5_s2"], "tags": tag(t["b5_t2"])}], "backdrop": True},
         "source_ids": ["S1", "S3"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_mark"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_compare", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"],
                  "left": {"title": t["b6_l"][0], "object": SIDE, "tag": t["b6_l"][1], "tag2": t["b6_l"][2], "tag2_at": a6["left_tag2"]},
                  "right": {"title": t["b6_r"][0], "object": NONE, "target": "hem", "tag": t["b6_r"][1], "tag2": t["b6_r"][2],
                            "tag2_at": a6["right_tag2"], "pulses": [{"target": "hem", "at": a6["pulse"]}]},
                  "left_at": a6["left_at"], "left_tag_at": a6["left_tag_at"], "right_at": a6["right_at"], "right_tag_at": a6["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], CENTRE, NONE, "hem", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "muted", "muted", "red", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema B03 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3. Keine Länderzuordnung (britisch/italienisch), keine Herkunft vom Reiten. Rückenansicht nur in Marineblau gezeichnet, auch für den Smoking.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Die drei Varianten als Frage; Antwort hängt vom Anlass ab.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["'Seitenschlitze britisch, ohne Schlitz italienisch': nicht belegt, nicht im Video.",
                             "Herkunft des Schlitzes vom Reiten: nicht belegt, nicht im Video."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
