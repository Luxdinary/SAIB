"""A02 Hosenträger: statt Gürtel, nicht zusätzlich (11.11.2026, menswear-20261111-2)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261111-2"
BELT = {"kind": "torso", "hold": "belt", "tie_tip": 520}
BRACES = {"kind": "torso", "hold": "braces", "tie_tip": 520}
BRACES_OPEN = {"kind": "torso", "hold": "braces", "neck": "none"}
DINNER = {"kind": "jacket", "variant": "sb1", "fastened": [0], "dinner": True, "lapel": "shawl", "neck": "bow"}
DB = {"kind": "jacket", "variant": "db6", "fastened": [0, 1]}
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://www.drakes.com/blogs/news/why-braces-matter", "title": "Drake's, Why braces matter: Hosenträger als Alternative zu Gürtel oder Seitenverstellern; Einknöpfen traditioneller als Clips, Knöpfe mitgeliefert; Hose hängt ruhiger von den Schultern", "checked_at": CHECKED, "label": "Drake's, Why braces matter"},
        {"id": "S2", "url": "https://suitsupply.com/en-us/journal/blacktie-attire-decoded.html", "title": "Suitsupply, Black tie attire decoded: Smokinghosen ohne Gürtelschlaufen, mit innen liegenden Hosenträgerknöpfen und Seitenverstellern", "checked_at": CHECKED, "label": "Suitsupply, Black Tie"},
        {"id": "S3", "url": "https://propercloth.com/reference/custom-trouser-design-business-casual-and-formal/", "title": "Proper Cloth, Custom trouser design: zum Smoking nie ein Gürtel, traditionell Hosenträger und Seitenversteller", "checked_at": CHECKED, "label": "Proper Cloth, Trousers"},
        {"id": "S4", "url": "https://debretts.com/addressing-the-dress-code/", "title": "Debrett's, Addressing the Dress Code: kein Gürtel zur Weste oder zum Zweireiher", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Hosenträger: statt Gürtel, nicht zusätzlich",
        q="Hosenträger und Gürtel?",
        b1="Hosenträger, und dazu noch ein Gürtel, nach dem Motto: sicher ist sicher? Genau das wäre doppelt gemoppelt. Hosenträger kommen statt des Gürtels, nicht zusätzlich.",
        b1_at=dict(badge_at="w:Gürtel", loupe_at="w:Gürtel", nie_at="w:doppelt"),
        b2="Der Londoner Herrenausstatter Drake's beschreibt Hosenträger als Alternative: zum Gürtel oder zu Seitenverstellern am Bund. Die Hose hängt dann von den Schultern und fällt ruhiger. Ein Gürtel hätte darunter nichts mehr zu halten.",
        b2_head="Was hält die Hose?", b2_label="Hosenträger statt Gürtel",
        b2_at=dict(pointer_at="w:Drake", zoom_at="w:Hosenträger", flip_at="w:Alternative", label_at="w:Schultern"),
        b3="Wie werden Hosenträger eigentlich befestigt? Laut Drake's ist das Einknöpfen die traditionellere Art. Die Knöpfe für den Bund liefert Drake's gleich mit. Clips gehen auch, sie gelten nur als weniger traditionell.",
        b3_head="Knöpfe oder Clips?",
        b3_tags=[("brace", "zum Einknöpfen", "traditioneller", "always", "w:Einknöpfen"),
                 ("waistband", "Knöpfe am Bund", "liefert Drake's mit", "always", "w:Knöpfe"),
                 ("brace_r", "Clips", "weniger traditionell", "sometimes", "w:Clips")],
        b4="Am deutlichsten zeigt es der Smoking. Laut Suitsupply hat die Smokinghose nie Gürtelschlaufen, sondern innen liegende Knöpfe für Hosenträger und Seitenversteller. Proper Cloth sagt es ebenso klar: Zum Smoking kein Gürtel.",
        b4_head="Beim Smoking", b4_l=("Smoking", "Hose ohne Gürtelschlaufen"), b4_r=("Darunter", "Knöpfe innen, Versteller"),
        b4_at=dict(left_at="w:Smoking", left_tag_at="w:Gürtelschlaufen", right_at="w:innen", right_tag_at="w:Seitenversteller",
                   brace="w:Hosenträger", band="w:Seitenversteller", no="w:kein", mark="w:Suitsupply"),
        b5="Debrett's, der britische Ratgeber für Etikette, nennt zwei weitere Fälle: Zur Weste und zum Zweireiher gehört kein Gürtel. Wo Hosenträger schon halten, braucht die Hose keinen zweiten Halt mehr.",
        b5_head="Und sonst?", b5_label="Kein Gürtel zum Zweireiher",
        b5_at=dict(pointer_at="w:Debrett", zoom_at="w:nennt", error_at="w:Weste", flip_at="w:Zweireiher", label_at="w:kein"),
        b6="Kurz gesagt: Hosenträger ersetzen den Gürtel, sie ergänzen ihn nicht. Eingeknöpft ist die traditionelle Art, Clips gehen auch. Und zum Smoking trägst du nie einen Gürtel.",
        b6_head="Kurz gesagt",
        b6_items=[("Statt Gürtel, nicht dazu", "eins von beiden hält die Hose", "w:Hosenträger", "w:ersetzen"),
                  ("Knöpfe: traditionell", "laut Drake's, Clips gehen auch", "w:Eingeknöpft", "w:traditionelle"),
                  ("Smoking: nie Gürtel", "Suitsupply, Proper Cloth", "w:Smoking", "w:Gürtel")],
        b7="Die Hose hält von oben, ohne Gürtel dazu. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Statt. Nicht zusätzlich.", b7_at=dict(fix_at="w:Hose", ring_at="w:oben", statement_at="w:ohne", chip_at="w:Blick"),
        status="Hose, Bund",
        states=["Gürtel dazu: ?", "doppelter Halt", "eingeknöpft", "Smoking: nie Gürtel", "Weste: kein Gürtel", "statt, nicht dazu", "Hosenträger: allein"],
        desc="Hosenträger und Gürtel zugleich? Drake's beschreibt Hosenträger als Alternative zum Gürtel. Dazu: Knöpfe oder Clips, warum die Smokinghose keine Gürtelschlaufen hat (Suitsupply, Proper Cloth) und was Debrett's sagt.",
        tags=["herrenmode", "hosenträger", "smoking", "stilregeln", "anzug"],
        hooks=[("H1", "question", "Hosenträger und Gürtel?"), ("H2", "misconception", "Gürtel plus Hosenträger? Doppelt gemoppelt."),
               ("H3", "surprising_fact", "Smokinghosen haben keine Gürtelschlaufen"), ("H4", "concrete_risk", "Unter Hosenträgern hat ein Gürtel nichts zu halten"),
               ("H5", "demonstration", "Gürtel raus, Hosenträger rein")],
    ),
    "en": dict(
        title="Braces replace the belt, they don't join it",
        q="Braces and a belt?",
        b1="Braces, and a belt on top, just to be safe? That would be doubling up. Braces come instead of a belt, not in addition to it.",
        b1_at=dict(badge_at="w:belt", loupe_at="w:belt", nie_at="w:doubling"),
        b2="The London outfitter Drake's describes braces as an alternative: to a belt, or to side adjusters on the waistband. The trousers then hang from your shoulders and fall more cleanly. A belt underneath would have nothing left to hold.",
        b2_head="What holds the trousers?", b2_label="Braces instead of a belt",
        b2_at=dict(pointer_at="w:Drake", zoom_at="w:braces", flip_at="w:alternative", label_at="w:shoulders"),
        b3="How do they attach? According to Drake's, button-in braces are the more traditional kind, and Drake's supplies the buttons for the waistband. Clips work too; they are simply considered less traditional.",
        b3_head="Buttons or clips?",
        b3_tags=[("brace", "button-in", "more traditional", "always", "w:button"),
                 ("waistband", "buttons", "supplied by Drake's", "always", "w:buttons"),
                 ("brace_r", "clips", "less traditional", "sometimes", "w:Clips")],
        b4="The dinner suit makes it clearest. According to Suitsupply, dinner suit trousers never have belt loops; they have inside buttons for braces and side adjusters instead. Proper Cloth is just as clear: never a belt with a dinner suit.",
        b4_head="With a dinner suit", b4_l=("Dinner suit", "no belt loops on trousers"), b4_r=("Underneath", "inside buttons, adjusters"),
        b4_at=dict(left_at="w:dinner", left_tag_at="w:loops", right_at="w:inside", right_tag_at="w:adjusters",
                   brace="w:braces", band="w:side", no="w:never#2", mark="w:Suitsupply"),
        b5="Debrett's, the British guide to etiquette, adds two more cases: no belt with a waistcoat, and none with a double-breasted jacket. Once braces are doing the holding, the trousers need no second support.",
        b5_head="And elsewhere?", b5_label="No belt with double-breasted",
        b5_at=dict(pointer_at="w:Debrett", zoom_at="w:adds", error_at="w:waistcoat", flip_at="w:double", label_at="w:Once"),
        b6="In short: braces replace the belt, they don't join it. Buttoned in is the traditional way, clips work too. And with a dinner suit, you never wear a belt.",
        b6_head="In short",
        b6_items=[("Instead, not as well", "one or the other holds", "w:braces", "w:replace"),
                  ("Buttons: traditional", "per Drake's; clips work too", "w:Buttoned", "w:traditional"),
                  ("Dinner suit: no belt", "Suitsupply, Proper Cloth", "w:dinner", "w:belt#2")],
        b7="Held from above, with no belt on top. For more eye for detail: follow Suitwerk.",
        b7_stmt="Instead. Not as well.", b7_at=dict(fix_at="w:Held", ring_at="w:above", statement_at="w:with", chip_at="w:eye"),
        status="Waistband",
        states=["belt as well: ?", "double support", "buttoned in", "dinner suit: no belt", "waistcoat: no belt", "instead, not as well", "braces on their own"],
        desc="Braces and a belt at once? Drake's describes braces as an alternative to a belt. Plus: buttons or clips, why dinner suit trousers have no belt loops (Suitsupply, Proper Cloth), and what Debrett's says.",
        tags=["menswear", "braces", "blacktie", "styletips", "suit"],
        hooks=[("H1", "question", "Braces and a belt?"), ("H2", "misconception", "Belt plus braces? That's doubling up."),
               ("H3", "surprising_fact", "Dinner suit trousers have no belt loops"), ("H4", "concrete_risk", "Under braces, a belt has nothing to hold"),
               ("H5", "demonstration", "Belt out, braces in")],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"], "Hemd mit Hosenträgern, Lupe auf dem Knopf am Bund") for h, ty, os in t["hooks"]]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in t["b3_tags"]]
    i1, i2, i3 = t["b6_items"]
    items = [
        {"title": i1[0], "sub": i1[1], "object": BELT, "at": i1[2], "then": {"hold": "braces"}, "then_at": i1[3]},
        {"title": i2[0], "sub": i2[1], "object": BRACES, "at": i2[2], "ring": "brace", "ring_at": i2[3]},
        {"title": i3[0], "sub": i3[1], "object": DINNER, "at": i3[2], "ring": "waist", "ring_at": i3[3], "ring_tone": "red"},
    ]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 7, "spoken": t["b1"],
         "data": {"question": t["q"], "object": BRACES, "target": "brace", "badge": "?", "question_at": 0.3, "hold_end": True, **t["b1_at"]},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 14, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "object": BELT, "from": BELT, "to": BRACES, "target": "belt", "zoom": 1.4,
                  "label": t["b2_label"], "strain": False, "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a2["pointer_at"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": BRACES_OPEN, "at": 0.0, "tags": tags}], "backdrop": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Drake"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": DINNER, "tag": t["b4_l"][1],
                           "pulses": [{"target": "waist", "at": a4["no"], "tone": "red"}]},
                  "right": {"title": t["b4_r"][0], "object": BRACES_OPEN, "target": "brace", "tag": t["b4_r"][1],
                            "pulses": [{"target": "brace", "at": a4["brace"]}, {"target": "waistband", "at": a4["band"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S2", "S3"], "overlay": {"marker": "fakt", "marker_at": a4["mark"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "object": BELT, "from": BELT, "to": DB, "target": "belt", "zoom": 1.3,
                  "label": t["b5_label"], "strain": False, "backdrop": True, "hold_end": True, **a5},
         "source_ids": ["S4"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a5["pointer_at"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], BELT, BRACES, "brace", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "muted", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema A02 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S4. 'Nicht beides' ist Logik (Hosenträger als Alternative), keine zitierte Regel; Clips nicht als falsch dargestellt.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Die verbreitete Doppellösung als Frage; Antwort: statt, nicht zusätzlich.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Keine Quelle sagt wörtlich 'nie Gürtel und Hosenträger zugleich'; im Video als Folgerung aus 'Alternative' formuliert.",
                             "Clip-Hosenträger: laut Drake's nur weniger traditionell, nicht falsch."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
