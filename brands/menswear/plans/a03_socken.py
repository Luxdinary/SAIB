"""A03 Socken zum Anzug: zur Hose, nicht zum Schuh, und lang genug zum Sitzen (12.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261112-3"
STAND = {"kind": "legs", "break": "slight", "shoe": "oxford"}
SHORT = {"kind": "legs", "seated": True, "sock": "short", "shoe": "oxford"}
LONG = {"kind": "legs", "seated": True, "sock": "long", "shoe": "oxford"}
NAVY = {"kind": "swatch", "weave": "worsted", "colour": "#26344D"}
BLACK = {"kind": "swatch", "weave": "worsted", "colour": "#17181C"}
BROWN = {"kind": "swatch", "weave": "twill", "colour": "#4A3324"}      # Ton der braunen Schuhe (Schluss)
TROUSER = {"kind": "swatch", "weave": "twill", "colour": "#26344D"}    # Ton der Hose (Schluss)
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://www.falke.com/sk_en/journal/knee-high-guide-men/", "title": "Falke, Knee-high guide for men: im Business feine, blickdichte Kniestrümpfe im Ton der Hose; Socken eher zur Hose als zum Schuh abstimmen oder bewusst kontrastieren", "checked_at": CHECKED, "label": "Falke, Kniestrumpf-Ratgeber"},
        {"id": "S2", "url": "https://suitsupply.com/en-us/men/accessories/socks", "title": "Suitsupply, Socken (FAQ): Sockenfarbe zur Hose statt zum Schuh; Crew-Länge bedeckt beim Sitzen ausreichend", "checked_at": CHECKED, "label": "Suitsupply, Socken-FAQ"},
        {"id": "S3", "url": "https://www.marksandspencer.com/content/guide-to-suit-colour-combinations", "title": "Marks & Spencer, Guide to suit colour combinations: zum blauen Anzug Socken passend zur Hose, zum schwarzen dunkle Socken, nichts zu Grelles", "checked_at": CHECKED, "label": "M&S, Anzugfarben"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Socken zum Anzug: zur Hose, nicht zum Schuh",
        q="Hose oder Schuh?",
        b1="Dunkler Anzug, braune Schuhe. Und die Socken? Wählst du sie passend zum Schuh oder passend zur Hose?",
        b1_at=("w:Socken", "w:Hose"),
        b2="Die Frage stellt sich vor allem im Sitzen. Im Stehen verdeckt die Hose die Socken fast ganz. Setzt du dich, rutscht der Saum nach oben, und man sieht die Socke. Ist sie zu kurz, sogar Haut.",
        b2_head="Stehen oder sitzen?", b2_label="Im Sitzen: Socke sichtbar",
        b2_at=dict(pointer_at="w:Frage", zoom_at="w:stellt", flip_at="w:Setzt", label_at="w:sieht", error_at="w:Haut"),
        b3="Die Faustregel kommt vom Sockenhersteller Falke und von Suitsupply: Stimm die Socken auf die Hose ab, nicht auf den Schuh. Falke rät im Business zu feinen, blickdichten Strümpfen im Ton der Hose. Bewusster Kontrast bleibt trotzdem eine Option.",
        b3_head="Die Faustregel", b3_stage="Socke zur Hose",
        b3_tags=[("crease", "Hose: der Maßstab", "nicht der Schuh", "always", "w:Hose"),
                 ("sock", "im Ton der Hose", "fein und blickdicht", "always", "w:feinen"),
                 ("shoe", "Kontrast: bewusst", "laut Falke möglich", "sometimes", "w:Kontrast")],
        b3_focus="w:Option", b3_marker="w:Falke",
        b4="Marks and Spencer wird konkret. Zum blauen Anzug wählst du Socken passend zur Hose. Zum schwarzen Anzug dunkle Socken. Und bei beiden gilt: nichts zu Grelles.",
        b4_head="Welcher Anzug?", b4_l=("Blau", "Socken wie die Hose"), b4_r=("Schwarz", "dunkle Socken"),
        b4_at=dict(left_at="w:blauen", left_tag_at="w:Socken", right_at="w:schwarzen", right_tag_at="w:dunkle", pulse="w:Grelles"), b4_marker="w:Marks",
        b5="Bleibt die Länge. Zu kurze Socken zeigen im Sitzen Haut. Suitsupply hält die Crew-Länge für ausreichend, Falke empfiehlt im Business Kniestrümpfe. Bei beiden bleibt das Bein auch im Sitzen bedeckt.",
        b5_head="Wie lang?",
        b5_stages=(("Zu kurz", [("sock", "Haut im Sitzen", "Bein nicht bedeckt", "never", "w:Haut")]),
                   ("Lang genug", [("sock", "Crew-Länge", "laut Suitsupply genug", "sometimes", "w:Crew"),
                                   ("crease", "Kniestrumpf", "Falke, im Business", "sometimes", "w:Kniestrümpfe")])),
        b5_at=dict(stage2="w:Suitsupply", focus="w:bedeckt"),
        b6="Kurz gesagt: Die Socke richtet sich nach der Hose, nicht nach dem Schuh. Sie ist lang genug für den Moment, in dem du dich setzt. Und wer Kontrast will, wählt ihn bewusst.",
        b6_head="Kurz gesagt",
        b6_items=[("Farbe: wie die Hose", "Falke, Suitsupply, M&S", "w:Socke", "w:Hose"),
                  ("Lang genug im Sitzen", "Crew oder Kniestrumpf", "w:lang", "w:setzt"),
                  ("Kontrast: bewusst", "laut Falke eine Option", "w:Kontrast", "w:bewusst")],
        b7="Nicht im Ton der Schuhe, sondern im Ton der Hose. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Im Ton der Hose.", b7_at=dict(fix_at="w:sondern", ring_at="w:Hose", statement_at="w:Hose", chip_at="w:Blick"),
        status="Socken zum Anzug",
        states=["Socke: Hose? Schuh?", "Sitzen: Haut sichtbar", "Regel: wie die Hose", "Schwarz: dunkel", "Länge: Crew, Knie", "Hose, lang, bewusst", "Socke: wie die Hose"],
        desc="Socken zum Anzug: Falke und Suitsupply stimmen sie auf die Hose ab, nicht auf den Schuh, Marks & Spencer nennt Blau und Schwarz. Dazu die Länge fürs Sitzen und bewusster Kontrast.",
        tags=["herrenmode", "socken", "anzug", "stilregeln", "businessoutfit"],
        hooks=[("H1", "question", "Hose oder Schuh?"), ("H2", "misconception", "Socken passend zum Schuh? Eher zur Hose."),
               ("H3", "surprising_fact", "Die Hose bestimmt die Sockenfarbe, nicht der Schuh"), ("H4", "concrete_risk", "Zu kurze Socken zeigen im Sitzen Haut"),
               ("H5", "demonstration", "Was man sieht, wenn du dich hinsetzt")],
    ),
    "en": dict(
        title="Suit socks: match the trousers, not the shoes",
        q="Trousers or shoes?",
        b1="Dark suit, brown shoes. And the socks? Do you match them to the shoes, or to the trousers?",
        b1_at=("w:socks", "w:trousers"),
        b2="It matters most once you are seated. Standing, your trousers almost hide the socks. Sit down, the hem rides up, and the socks come into view. If they are too short, so does bare skin.",
        b2_head="Standing or seated?", b2_label="Seated: the socks show",
        b2_at=dict(pointer_at="w:matters", zoom_at="w:most", flip_at="w:Sit", label_at="w:view", error_at="w:skin"),
        b3="The rule of thumb comes from the sock maker Falke and from Suitsupply: match your socks to the trousers, not to the shoes. For business, Falke suggests fine, opaque socks in the tone of the trousers. A deliberate contrast is still an option.",
        b3_head="The rule of thumb", b3_stage="Socks to trousers",
        b3_tags=[("crease", "Trousers set it", "not the shoes", "always", "w:trousers"),
                 ("sock", "trouser tone", "fine and opaque", "always", "w:fine"),
                 ("shoe", "Contrast: chosen", "an option, says Falke", "sometimes", "w:contrast")],
        b3_focus="w:option", b3_marker="w:Falke",
        b4="Marks and Spencer gets specific. With a navy suit, pick socks that match the trousers. With a black suit, go for dark socks. And with either one: nothing too loud.",
        b4_head="Which suit?", b4_l=("Navy", "socks like the trousers"), b4_r=("Black", "dark socks"),
        b4_at=dict(left_at="w:navy", left_tag_at="w:socks", right_at="w:black", right_tag_at="w:dark", pulse="w:loud"), b4_marker="w:Marks",
        b5="That leaves the length. Socks that are too short show skin when you sit. Suitsupply finds crew length enough, while Falke recommends knee-highs for business. Either way, your leg stays covered when you sit down.",
        b5_head="How long?",
        b5_stages=(("Too short", [("sock", "skin when seated", "leg not covered", "never", "w:skin")]),
                   ("Long enough", [("sock", "crew length", "enough, says Suitsupply", "sometimes", "w:crew"),
                                    ("crease", "knee-high", "Falke, for business", "sometimes", "w:knee")])),
        b5_at=dict(stage2="w:Suitsupply", focus="w:covered"),
        b6="In short: your socks follow the trousers, not the shoes. They are long enough for the moment you sit down. And if you want a contrast, you choose it on purpose.",
        b6_head="In short",
        b6_items=[("Colour: like the trousers", "Falke, Suitsupply, M&S", "w:socks", "w:trousers"),
                  ("Long enough to sit", "crew or knee-high", "w:long", "w:sit"),
                  ("Contrast: on purpose", "an option, says Falke", "w:contrast", "w:purpose")],
        b7="Not the tone of the shoes, but the tone of the trousers. For more eye for detail: follow Suitwerk.",
        b7_stmt="The tone of the trousers.", b7_at=dict(fix_at="w:but", ring_at="w:trousers", statement_at="w:trousers", chip_at="w:eye"),
        status="Socks",
        states=["socks: trousers? shoes?", "seated: skin shows", "rule: like the trousers", "black: dark socks", "length: crew, knee", "trousers, long, chosen", "socks: like the trousers"],
        desc="Socks with a suit: Falke and Suitsupply match them to the trousers, not the shoes, and Marks & Spencer covers navy and black. Plus the length for sitting down and a deliberate contrast.",
        tags=["menswear", "socks", "suit", "styletips", "businessattire"],
        hooks=[("H1", "question", "Trousers or shoes?"), ("H2", "misconception", "Socks to match the shoes? Better the trousers."),
               ("H3", "surprising_fact", "The trousers pick the sock colour, not the shoes"), ("H4", "concrete_risk", "Short socks show skin the moment you sit"),
               ("H5", "demonstration", "What shows when you sit down")],
    ),
}


def _tags(rows):
    return [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in rows]


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"], "Bein im Sitzen, Lupe auf der Socke") for h, ty, os in t["hooks"]]
    objs = [(LONG, None, "sock"), (SHORT, LONG, None), (LONG, None, "sock")]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    stages5 = []
    for k, (title, rows) in enumerate(t["b5_stages"]):
        st = {"object": (SHORT, LONG)[k], "at": 0.0 if k == 0 else a5["stage2"], "title": title, "tags": _tags(rows)}
        if k == 1:
            st["focus_at"] = a5["focus"]
        stages5.append(st)
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": LONG, "target": "sock", "badge": "?", "question_at": 0.3,
                  "badge_at": t["b1_at"][0], "loupe_at": t["b1_at"][0], "nie_at": t["b1_at"][1], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "from": STAND, "to": SHORT, "target": "sock", "zoom": 1.4, "label": t["b2_label"],
                  "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 751, "y": 879, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a2["flip_at"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 14, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": LONG, "at": 0.0, "title": t["b3_stage"], "tags": _tags(t["b3_tags"]), "focus_at": t["b3_focus"]}],
                  "backdrop": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 10, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": NAVY, "tag": t["b4_l"][1], "pulses": [{"target": "center", "at": a4["pulse"]}]},
                  "right": {"title": t["b4_r"][0], "object": BLACK, "tag": t["b4_r"][1], "pulses": [{"target": "center", "at": a4["pulse"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S3"], "overlay": {"marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": stages5, "backdrop": True, "hold_end": True},
         "source_ids": ["S2", "S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": a5["stage2"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], BROWN, TROUSER, "center", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema A03 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Länge: Falke Kniestrumpf, Suitsupply Crew, beides genannt; Kontrast nicht verboten.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Farbfrage am Detail, das erst im Sitzen auffällt.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Sockenfarbe in der Zeichnung fest (Navy); Blau/Schwarz und der Schlusswechsel Schuhton -> Hosenton nur als Stoffmuster gezeigt.",
                             "Bunte Socken: nicht verboten, Falke nennt Kontrast als Möglichkeit; keine Farbempfehlung im Video."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
