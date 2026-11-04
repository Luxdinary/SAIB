"""A01 Weste: der unterste Knopf bleibt offen (09.11.2026, 12:00 DE / 15:00 EN)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261109-1"
WC5 = {"kind": "waistcoat", "fastened": [0, 1, 2, 3, 4]}
WC6 = {"kind": "waistcoat", "fastened": [0, 1, 2, 3, 4, 5], "strain": True}
WC6_PLAIN = {"kind": "waistcoat", "fastened": [0, 1, 2, 3, 4, 5]}
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://debretts.com/the-a-z-of-the-modern-gentleman/", "title": "Debrett's, The A-Z of the Modern Gentleman: Westen haben sechs oder sieben Knöpfe, der unterste bleibt immer offen", "checked_at": CHECKED, "label": "Debrett's, A-Z"},
        {"id": "S2", "url": "https://debretts.com/addressing-the-dress-code/", "title": "Debrett's, Addressing the Dress Code: unterster Westenknopf offen, kein Gürtel zur Weste", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
        {"id": "S3", "url": "https://kingandallen.co.uk/journal/2017/to-button-or-not-to-button/", "title": "King & Allen (Maßschneider London): unterster Knopf der einreihigen Weste offen, praktischer Grund beim Sitzen", "checked_at": CHECKED, "label": "King & Allen, Journal"},
        {"id": "S4", "url": "https://www.moss.co.uk/inside-pocket/post/how-to-wear-a-waistcoat", "title": "Moss, How to wear a waistcoat: Always leave the bottom button undone", "checked_at": CHECKED, "label": "Moss, Inside Pocket"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Weste: Warum der unterste Knopf offen bleibt",
        q="Sechs Knöpfe, nur fünf zu?",
        b1="Sechs Knöpfe an der Weste, aber nur fünf sind zu. Der unterste bleibt offen. Ist das Nachlässigkeit?",
        b2="Schließ ihn probeweise und setz dich hin. Genau hier liegt der Grund. Der Londoner Maßschneider King and Allen erklärt es ganz praktisch: Wäre der unterste Knopf zu, müsstest du ihn bei jedem Hinsetzen wieder öffnen. Also bleibt er gleich offen, im Stehen wie im Sitzen.",
        b2_head="Alle sechs zu?", b2_label="Grund: das Hinsetzen",
        b2_at=dict(pointer_at="w:Schließ", zoom_at="w:setz", flip_at="w:hin", all_at="w:Genau", label_at="w:Maßschneider", tense_at="w:Hinsetzen"),
        b3="Aus diesem praktischen Grund ist eine feste Regel geworden. Debrett's, der britische Ratgeber für Etikette, schreibt: Westen haben sechs oder sieben Knöpfe, und der unterste bleibt immer offen. Der Herrenausstatter Moss sagt es knapper: Das macht man so.",
        b3_head="Die feste Regel", b3_stage="Sechs Knöpfe",
        b3_tags=[("button:2", "fünf zu", "Knopf eins bis fünf", "always", "w:Knöpfe"), ("button:5", "nie zu", "der unterste", "never", "w:unterste")],
        b3_focus="w:Moss",
        b4="Sieh dir beide Westen nebeneinander an. Links sind alle Knöpfe zu, rechts bleibt der unterste offen. Die rechte Weste ist so getragen, wie es Debrett's und Moss beschreiben.",
        b4_head="Zu oder offen?", b4_l=("Alle zu", "so nicht üblich"), b4_r=("Unten offen", "wie Debrett's und Moss"),
        b4_at=dict(left_at="w:Links", left_tag_at="w:alle", right_at="w:rechts", right_tag_at="w:Debrett", pulse="w:unterste"),
        b5="Noch ein Detail aus dem Dresscode-Leitfaden von Debrett's: Zum dreiteiligen Anzug gehört kein Gürtel. Unter der Weste bleibt der Bund also ohne Gürtel.",
        b5_head="Und der Gürtel?", b5_l=("Mit Gürtel", "nicht zum Dreiteiler"), b5_r=("Zur Weste", "Bund ohne Gürtel"),
        b5_at=dict(left_at="w:Detail", left_tag_at="w:kein", right_at="w:Unter", right_tag_at="w:ohne", pulse="w:Gürtel"),
        b6="Kurz gesagt: Bei der einreihigen Weste schließt du alle Knöpfe bis auf den untersten. Der Grund ist das Sitzen. Und unter der Weste trägst du keinen Gürtel.",
        b6_head="Kurz gesagt",
        b6_items=[("Unten: immer offen", "einreihige Weste", "w:einreihigen", "w:untersten"),
                  ("Grund: das Sitzen", "King & Allen, Maßschneider", "w:Grund", "w:Sitzen"),
                  ("Kein Gürtel darunter", "zum dreiteiligen Anzug", "w:trägst", "w:keinen")],
        b7="Fünf Knöpfe zu, einer offen. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Fünf zu. Einer offen.", b7_at=dict(fix_at="w:einer", ring_at="w:offen", statement_at="w:offen", chip_at="w:Blick"),
        status="Weste, einreihig",
        states=["unterer Knopf: ?", "alle zu: unpraktisch", "Regel: unten offen", "unten offen", "kein Gürtel", "Sitzen: kein Problem", "unterer Knopf: offen"],
        desc="Warum bleibt der unterste Westenknopf offen? Ein praktischer Grund ist zur festen Regel geworden: Debrett's, Moss und der Maßschneider King & Allen. Dazu: kein Gürtel zur Weste.",
        tags=["herrenmode", "weste", "dreiteiler", "stilregeln", "anzug"],
        hooks=[("H1", "question", "Sechs Knöpfe, nur fünf zu?"), ("H2", "misconception", "Alle Westenknöpfe zu? Lieber nicht."),
               ("H3", "surprising_fact", "Eine Weste ist zum Offenlassen gemacht"), ("H4", "concrete_risk", "Ganz zu? Beim Hinsetzen wieder auf."),
               ("H5", "demonstration", "Was passiert, wenn dieser Knopf zugeht?")],
    ),
    "en": dict(
        title="The waistcoat's bottom button: why it stays open",
        q="Six buttons, only five done up?",
        b1="Six buttons on the waistcoat, but only five are done up. The bottom one stays open. Is that just careless?",
        b2="Fasten it for a moment and sit down. That is where the reason lies. The London tailor King and Allen explains it in practical terms: if the bottom button were closed, you would have to undo it every single time you sat down. So it simply stays open, standing or sitting.",
        b2_head="All six closed?", b2_label="The reason: sitting down",
        b2_at=dict(pointer_at="w:Fasten", zoom_at="w:sit", flip_at="w:down", all_at="w:That", label_at="w:tailor", tense_at="w:undo"),
        b3="That practical reason has turned into a firm rule. Debrett's, the British authority on etiquette, puts it plainly: waistcoats have six or seven buttons, and the bottom one is always left undone. The outfitter Moss is even shorter: it is simply the done thing.",
        b3_head="The firm rule", b3_stage="Six buttons",
        b3_tags=[("button:2", "five closed", "buttons one to five", "always", "w:buttons"), ("button:5", "never closed", "the bottom one", "never", "w:bottom")],
        b3_focus="w:Moss",
        b4="Look at the two waistcoats side by side. On the left every button is closed, on the right the bottom one stays open. The right one is worn the way Debrett's and Moss describe it.",
        b4_head="Closed or open?", b4_l=("All closed", "not the usual way"), b4_r=("Bottom open", "as Debrett's and Moss say"),
        b4_at=dict(left_at="w:left", left_tag_at="w:every", right_at="w:right", right_tag_at="w:Debrett", pulse="w:bottom"),
        b5="One more detail from the dress code guide by Debrett's: a three-piece suit is worn without a belt. Under the waistcoat, the waistband stays belt-free.",
        b5_head="And the belt?", b5_l=("With a belt", "not with three pieces"), b5_r=("With a waistcoat", "no belt underneath"),
        b5_at=dict(left_at="w:detail", left_tag_at="w:without", right_at="w:Under", right_tag_at="w:waistband", pulse="w:belt"),
        b6="In short: on a single-breasted waistcoat you fasten every button except the bottom one. The reason is sitting down. And under the waistcoat, you wear no belt.",
        b6_head="In short",
        b6_items=[("Bottom: always open", "single-breasted waistcoat", "w:single", "w:except"),
                  ("Reason: sitting down", "King & Allen, tailors", "w:reason", "w:sitting"),
                  ("No belt underneath", "with a three-piece suit", "w:wear", "w:no")],
        b7="Five buttons closed, one left open. For more eye for detail: follow Suitwerk.",
        b7_stmt="Five closed. One open.", b7_at=dict(fix_at="w:one", ring_at="w:open", statement_at="w:open", chip_at="w:eye"),
        status="Waistcoat",
        states=["bottom button: ?", "all closed: impractical", "rule: bottom open", "bottom open", "no belt", "sitting: no problem", "bottom button: open"],
        desc="Why does the bottom waistcoat button stay undone? A practical reason became a firm rule: Debrett's, Moss and the London tailor King & Allen. Plus: no belt with a waistcoat.",
        tags=["menswear", "waistcoat", "threepiecesuit", "styletips", "suit"],
        hooks=[("H1", "question", "Six buttons, only five done up?"), ("H2", "misconception", "Every waistcoat button closed? Better not."),
               ("H3", "surprising_fact", "A waistcoat made to stay open"), ("H4", "concrete_risk", "All closed? Undo it every time you sit."),
               ("H5", "demonstration", "What happens when this button closes?")],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S3"], "Weste, Lupe auf dem untersten Knopf") for h, ty, os in t["hooks"]]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in t["b3_tags"]]
    items = []
    objs = [(WC5, None, "button:5"), (WC6, {"fastened": [0, 1, 2, 3, 4], "strain": False}, None),
            ({"kind": "torso", "hold": "belt", "tie_tip": 585}, {"hold": "none"}, None)]
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 5, "spoken": t["b1"],
         "data": {"question": t["q"], "object": WC5, "target": "button:5", "badge": "?", "question_at": 0.3,
                  "badge_at": "w:" + ("unterste" if lang == "de" else "bottom"), "loupe_at": "w:" + ("unterste" if lang == "de" else "bottom"),
                  "nie_at": "w:" + ("Nachlässigkeit" if lang == "de" else "careless"), "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 14, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "object": WC5, "from": WC5, "to": WC6, "from_fastened": WC5["fastened"],
                  "to_fastened": WC6["fastened"], "target": "button:5", "zoom": 1.5, "label": t["b2_label"], "backdrop": True,
                  "hold_end": True, **a2},
         "source_ids": ["S3"],
         "overlay": {"transition": {"type": "iris", "x": 751, "y": 879, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a2["label_at"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": WC5, "at": 0.0, "title": t["b3_stage"], "tags": tags, "focus_at": t["b3_focus"]}],
                  "backdrop": True},
         "source_ids": ["S1", "S4"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 9, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "left": {"title": t["b4_l"][0], "object": WC6_PLAIN, "target": "button:5", "tag": t["b4_l"][1]},
                  "right": {"title": t["b4_r"][0], "object": WC5, "tag": t["b4_r"][1], "pulses": [{"target": "button:5", "at": a4["pulse"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"], "hold_end": True},
         "source_ids": ["S1", "S4"], "overlay": {"marker": "fakt", "marker_at": a4["right_tag_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_fitting", "duration_hint": 9, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "from": {"kind": "torso", "hold": "belt", "tie_tip": 585}, "to": WC5,
                  "target": "belt", "zoom": 1.3, "label": t["b5_r"][1], "pointer_at": a5["left_at"], "zoom_at": a5["left_tag_at"],
                  "error_at": a5["pulse"], "flip_at": a5["right_at"], "label_at": a5["right_tag_at"], "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S3", "S2"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], WC6, WC5, "button:5", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "muted", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema A01 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S4; Zweireiher-Westen und Herkunftslegenden nicht verwendet.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Frage mit dem Detail, das das ganze Video trägt.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Zweireihige Westen: King & Allen ganz zu, Debrett's unten offen; nicht im Video.",
                             "Herkunft (Edward VII.): Legende, nicht im Video."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
