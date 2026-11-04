"""B04 Taschen verraten den Anlass: gepaspelt, Patte, aufgesetzt (13.11.2026, Thema 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261113-3"
FLAP = {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel": "notch", "pockets": "flap", "strain": False}
PATCH = {**FLAP, "pockets": "patch"}
DJ = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "peak", "dinner": True, "neck": "bow", "pockets": "jetted", "strain": False}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://www.woolmark.com/ko/z.archive/archive-industry/suiting/black-tie-dress-code-explained/", "title": "Woolmark, Black tie dress code explained: Taschen gepaspelt, Schlitze ohne Patte, damit die Silhouette glatt bleibt", "checked_at": CHECKED, "label": "Woolmark, Black Tie"},
    {"id": "S2", "url": "https://www.anderson-sheppard.co.uk/bespoke-gallery/", "title": "Anderson & Sheppard, Bespoke Gallery: Dinnerjackets mit Paspeltaschen; Tweed- und Shetland-Sakkos mit geraden Pattentaschen; Leinen- und Cordsakkos mit aufgesetzten Taschen; auch Anzüge mit aufgesetzten Pattentaschen", "checked_at": CHECKED, "label": "Anderson & Sheppard, Galerie"},
    {"id": "S3", "url": "https://www.anderson-sheppard.co.uk/thenotebook/the-anderson-sheppard-linen-jacket/", "title": "Anderson & Sheppard, The linen jacket: aufgesetzte Taschen passen zum insgesamt lässigen Charakter der Jacke", "checked_at": CHECKED, "label": "A&S, Leinenjacke"},
    {"id": "S4", "url": "https://www.woolmark.com/z.archive/archive-industry/suiting/on-the-row-huntsman/", "title": "Woolmark, On the Row: Huntsman: Taschen mit Kellerfalte, damit Patronen Platz haben; in der Stadt liegt die Tasche flach", "checked_at": CHECKED, "label": "Woolmark, Huntsman"},
]

T = {
    "de": dict(
        title="Taschen verraten den Anlass",
        q="Was verraten die Taschen am Sakko?",
        b1="Ein Schlitz, eine Patte oder aufgesetzt: Die Taschen am Sakko verraten oft den Anlass. Woran erkennst du das?",
        b1_at=dict(badge_at="w:Patte", loupe_at="w:Patte", nie_at="w:Woran"),
        b2="Zwei Sakkos aus der Galerie von Anderson and Sheppard. Links ein Dinnerjacket: Paspeltaschen, nur ein Schlitz. Rechts ein Tweedsakko mit geraden Pattentaschen. Gleiche Stelle am Sakko, ganz anderer Anlass.",
        b2_head="Abend oder Tweed?", b2_l=("Dinnerjacket", "Paspeltasche, ohne Patte"), b2_r=("Tweedsakko", "gerade Pattentasche"),
        b2_at=dict(left_at="w:Zwei", left_tag_at="w:Paspeltaschen", right_at="w:Rechts", right_tag_at="w:geraden",
                   lpulse="w:Schlitz", rpulse="w:Pattentaschen", marker="w:Anderson"),
        b3="Warum hat das Dinnerjacket keine Patte? Laut Woolmark sind die Taschen bei Black Tie gepaspelt, also Schlitze ohne Patte. So bleibt die Silhouette glatt. Auch Anderson and Sheppard zeigt Dinnerjackets mit Paspeltaschen.",
        b3_head="Warum ohne Patte?", b3_stage="Black Tie",
        b3_tags=[("pocket", "Paspeltasche", "Schlitz ohne Patte", "always", "w:gepaspelt"),
                 ("waist", "glatte Silhouette", "laut Woolmark", "always", "w:Silhouette")],
        b3_focus="w:Anderson", b3_marker="w:Woolmark",
        b4="Jetzt das andere, das lässige Ende. Leinen- und Cordsakkos zeigt Anderson and Sheppard mit aufgesetzten Taschen. Zur hauseigenen Leinenjacke heißt es: Die aufgesetzten Taschen passen zum insgesamt lässigen Charakter.",
        b4_head="Und lässig?", b4_label="Aufgesetzt: lässiger Charakter",
        b4_at=dict(pointer_at="w:lässige", zoom_at="w:Leinen", flip_at="w:aufgesetzten", label_at="w:passen"),
        b4_marker="w:Anderson",
        b5="Im Woolmark-Porträt des Schneiders Huntsman heißt es: Auf dem Land bekommt die Tasche eine Kellerfalte, damit Patronen Platz haben. In der Stadt liegt sie flach. Trotzdem nur eine Tendenz: Anderson and Sheppard fertigt auch Anzüge mit aufgesetzten Taschen.",
        b5_head="Land und Stadt",
        b5_st=[("Laut Huntsman", [("pocket", "Land: Kellerfalte", "Platz für Patronen", "always", "w:Kellerfalte"),
                                  ("pocket", "Stadt: flach", "laut Huntsman", "always", "w:Stadt")]),
               ("Auch am Anzug", [("pocket", "aufgesetzt", "Anderson & Sheppard", "sometimes", "w:Anzüge")])],
        b5_stage2="w:Anderson", b5_marker="w:Woolmark",
        b6="Kurz gesagt: Paspeltaschen ohne Patte gehören zum Dinnerjacket. Gerade Pattentaschen zeigt Anderson and Sheppard an Tweed und Shetland. Aufgesetzte Taschen an Leinen und Cord, passend zum lässigen Charakter.",
        b6_head="Kurz gesagt",
        b6_items=[("Ohne Patte: Dinnerjacket", "gepaspelt, glatte Silhouette", "w:Paspeltaschen", "w:Dinnerjacket"),
                  ("Patte: Tweed, Shetland", "gerade Pattentaschen", "w:Gerade", "w:Tweed"),
                  ("Aufgesetzt: Leinen, Cord", "passend zum lässigen Charakter", "w:Aufgesetzte", "w:Leinen")],
        b7="Schlitz für den Abend, Patte für Tweed, aufgesetzt für Leinen. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Tasche verrät Anlass.", b7_at=dict(fix_at="w:Schlitz", ring_at="w:Abend", statement_at="w:Leinen", chip_at="w:Blick"),
        status="Sakko, Taschen",
        states=["Tasche: ?", "anderer Anlass", "Abend: ohne Patte", "lässig: aufgesetzt", "Tendenz, kein Gesetz", "drei Taschen", "Tasche zeigt Anlass"],
        desc="Paspeltasche, Pattentasche oder aufgesetzt: Was die Tasche am Sakko über den Anlass verrät. Nach Woolmark (Black Tie, Huntsman) und der Galerie von Anderson & Sheppard, als Tendenz, nicht als Gesetz.",
        tags=["herrenmode", "sakko", "taschen", "maßschneider", "stilregeln"],
        hooks=[("H1", "question", "Was verraten die Taschen am Sakko?", []),
               ("H2", "misconception", "Taschen sind kein Nebendetail: Sie zeigen den Anlass", ["S2"]),
               ("H3", "surprising_fact", "Eine Kellerfalte, damit Patronen Platz haben", ["S4"]),
               ("H4", "concrete_risk", "Patte am Dinnerjacket? Laut Woolmark: gepaspelt.", ["S1"]),
               ("H5", "demonstration", "Ein Schlitz, eine Patte, aufgesetzt: drei Anlässe", [])],
    ),
    "en": dict(
        title="Pockets give away the occasion",
        q="What do a jacket's pockets say?",
        b1="A slit, a flap or a patch: the pockets on a jacket often give away the occasion. How do you read them?",
        b1_at=dict(badge_at="w:flap", loupe_at="w:flap", nie_at="w:How"),
        b2="Two jackets from the Anderson and Sheppard gallery. On the left, a dinner jacket with jetted pockets, just a slit. On the right, a tweed jacket with straight flap pockets. Same spot, a different occasion.",
        b2_head="Evening or tweed?", b2_l=("Dinner jacket", "jetted, no flap"), b2_r=("Tweed jacket", "straight flap pockets"),
        b2_at=dict(left_at="w:Two", left_tag_at="w:jetted", right_at="w:right", right_tag_at="w:straight",
                   lpulse="w:slit", rpulse="w:flap", marker="w:Anderson"),
        b3="Why no flap on a dinner jacket? According to Woolmark, black tie pockets are jetted: slits without flaps. That keeps the silhouette smooth. Anderson and Sheppard's dinner jackets show the same.",
        b3_head="Why no flap?", b3_stage="Black tie",
        b3_tags=[("pocket", "jetted pocket", "a slit, no flap", "always", "w:jetted"),
                 ("waist", "smooth silhouette", "says Woolmark", "always", "w:silhouette")],
        b3_focus="w:Anderson", b3_marker="w:Woolmark",
        b4="Now the relaxed end. Anderson and Sheppard show linen and corduroy jackets with patch pockets. Of their own linen jacket, the house says the patch pockets suit its overall casual character.",
        b4_head="And casual?", b4_label="Patch: a casual character",
        b4_at=dict(pointer_at="w:relaxed", zoom_at="w:linen", flip_at="w:patch", label_at="w:suit"),
        b4_marker="w:Anderson",
        b5="A Woolmark portrait of the tailor Huntsman adds this: in the country, a pocket gets a bellows pleat so cartridges fit. In town, it lies flat. Still, it is a tendency: Anderson and Sheppard also make suits with patch pockets.",
        b5_head="Country and town",
        b5_st=[("Says Huntsman", [("pocket", "country: bellows", "room for cartridges", "always", "w:bellows"),
                                  ("pocket", "town: flat", "says Huntsman", "always", "w:town")]),
               ("On suits too", [("pocket", "patch pockets", "Anderson & Sheppard", "sometimes", "w:suits")])],
        b5_stage2="w:Anderson", b5_marker="w:Woolmark",
        b6="In short: jetted pockets without flaps belong to the dinner jacket. Straight flap pockets appear on tweed and Shetland at Anderson and Sheppard. And patch pockets on linen and corduroy, matching the casual character.",
        b6_head="In short",
        b6_items=[("No flap: dinner jacket", "jetted, a smooth silhouette", "w:jetted", "w:dinner"),
                  ("Flap: tweed, Shetland", "straight flap pockets", "w:Straight", "w:tweed"),
                  ("Patch: linen, corduroy", "matching the casual character", "w:patch", "w:linen")],
        b7="A slit for the evening, a flap for tweed, a patch for linen. For more eye for detail: follow Suitwerk.",
        b7_stmt="Slit, flap or patch.", b7_at=dict(fix_at="w:slit", ring_at="w:evening", statement_at="w:linen", chip_at="w:eye"),
        status="Jacket, pockets",
        states=["pocket: ?", "other occasion", "evening: no flap", "casual: patch", "a tendency, no law", "three pockets", "pocket shows occasion"],
        desc="Jetted, flap or patch: what the pockets on a jacket say about the occasion. Based on Woolmark (black tie, Huntsman) and the Anderson & Sheppard gallery, as a tendency rather than a law.",
        tags=["menswear", "jacket", "pockets", "tailoring", "styletips"],
        hooks=[("H1", "question", "What do a jacket's pockets say?", []),
               ("H2", "misconception", "Pockets are no side detail: they show the occasion", ["S2"]),
               ("H3", "surprising_fact", "A bellows pleat, so the cartridges fit", ["S4"]),
               ("H4", "concrete_risk", "Flaps on a dinner jacket? Woolmark says jetted.", ["S1"]),
               ("H5", "demonstration", "A slit, a flap, a patch: three occasions", [])],
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
    hooks = [hook(h, ty, os, os, src, "Sakko mit Pattentaschen, Lupe auf der Patte") for h, ty, os, src in t["hooks"]]
    a2, a4 = t["b2_at"], t["b4_at"]
    objs = [(DJ, None, "pocket"), (FLAP, None, "pocket"), (FLAP, {"pockets": "patch"}, None)]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    st3 = _stages([(t["b3_stage"], t["b3_tags"])], (DJ,), None)
    st3[0]["focus_at"] = t["b3_focus"]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": FLAP, "target": "pocket", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 12, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": DJ, "target": "pocket", "tag": t["b2_l"][1], "pulses": [{"target": "pocket", "at": a2["lpulse"]}]},
                  "right": {"title": t["b2_r"][0], "object": FLAP, "tag": t["b2_r"][1], "pulses": [{"target": "pocket", "at": a2["rpulse"]}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": a2["marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 11, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": st3, "backdrop": True, "hold_end": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": FLAP, "to": PATCH, "target": "pocket", "zoom": 1.45, "label": t["b4_label"],
                  "backdrop": True, "hold_end": True, **a4},
         "source_ids": ["S2", "S3"],
         "overlay": {"transition": {"type": "iris", "x": 300, "y": 940, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 14, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": _stages(t["b5_st"], (FLAP, PATCH), t["b5_stage2"]), "backdrop": True},
         "source_ids": ["S4", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], PATCH, DJ, "pocket", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema B04 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S4; als Tendenz erzählt, nicht als Gesetz; Ticket Pocket bewusst ausgelassen (eigenes Thema B10).",
                 sources=SOURCES, hooks=hooks, hook_note="Die drei Taschenarten als Frage, die Lupe auf der Patte.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Kellerfalte (Huntsman, S4): nur gesprochen und als Etikett, keine eigene Zeichnung; gezeigt wird das Sakko mit Pattentasche.",
                             "Aufgesetzte Pattentaschen am Anzug (S2): als aufgesetzte Tasche gezeichnet, Patte darauf gibt es nicht als Zeichnung.",
                             "Stoffe (Tweed, Leinen, Cord) nur gesprochen; alle Sakkos in derselben Grundfarbe."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
