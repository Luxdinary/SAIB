"""A04 Krawattenlänge: die Spitze endet etwa am Hosenbund (14.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261114-2"
OK = {"kind": "torso", "hold": "belt", "tie_tip": 585}          # Spitze an der Oberkante der Schnalle
SHORT = {"kind": "torso", "hold": "belt", "tie_tip": 500}       # endet über dem Gürtel
LONG = {"kind": "torso", "hold": "belt", "tie_tip": 665}        # verschwindet unter dem Bund
K_SLIM = {"kind": "knot", "knot": "four_in_hand"}
K_BIG = {"kind": "knot", "knot": "windsor"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://www.thetiebar.com/blogs/faqs/where-should-tie-length-be",
     "title": "The Tie Bar (Krawattenhersteller), Where should tie length be: Spitze trifft die Oberkante von Gürtelschnalle oder Hosenbund, nie unter dem Bund, nie über dem Gürtel; Länge relativ zum Körper, dickere Knoten brauchen mehr Stoff",
     "checked_at": CHECKED, "label": "The Tie Bar, FAQ"},
    {"id": "S2", "url": "https://www.drakes.com/blogs/news/the-drakes-guide-to-ties",
     "title": "Drake's, The Drake's Guide to Ties: breites Blatt mindestens bis zum Gürtel, schmales Ende in die Schlaufe",
     "checked_at": CHECKED, "label": "Drake's, Guide to Ties"},
]

T = {
    "de": dict(
        title="Krawattenlänge: Die Spitze endet am Bund",
        q="Wo endet die Krawattenspitze?",
        b1="Die Krawatte ist gebunden. Aber wo genau soll ihre Spitze enden? Über dem Gürtel, darunter, oder genau dazwischen?",
        hook_at=dict(badge_at="w:Spitze", loupe_at="w:Spitze", nie_at="w:dazwischen"),
        b2="Links ist sie zu kurz und hängt über dem Gürtel. Rechts ist sie zu lang und verschwindet unter dem Bund. Der Krawattenhersteller The Tie Bar schließt beides aus: nie über dem Gürtel, nie unter dem Bund.",
        b2_head="Zu kurz, zu lang", b2_l=("Zu kurz", "hängt über dem Gürtel"), b2_r=("Zu lang", "unter dem Bund"),
        b2_at=dict(left_at="w:Links", left_tag_at="w:hängt", right_at="w:Rechts", right_tag_at="w:verschwindet",
                   pl="w:nie", pr="w:nie#2", marker="w:Krawattenhersteller"),
        b3="Die Regel der Tie Bar: Die Spitze trifft die Oberkante der Gürtelschnalle oder des Hosenbunds. Nicht höher und nicht tiefer. Sie endet also etwa am Bund.",
        b3_head="Wo genau?", b3_label="Spitze trifft den Bund",
        b3_at=dict(pointer_at="w:Regel", error_at="w:Tie", zoom_at="w:Spitze", flip_at="w:trifft", label_at="w:Oberkante"),
        b3_marker="w:Oberkante",
        b4="Der Krawattenmacher Drake's formuliert es als Untergrenze: Das breite Blatt reicht mindestens bis zum Gürtel. Und das schmale Ende? Das darf hinten in die Schlaufe.",
        b4_head="Die Untergrenze", b4_stage="Laut Drake's",
        b4_tags=[("tie_tip", "breites Blatt", "bis zum Gürtel", "always", "w:breite"),
                 ("placket", "schmales Ende", "in die Schlaufe", "sometimes", "w:schmale")],
        b4_focus="w:Schlaufe", b4_marker="w:Drake",
        b5="Eine feste Zentimeterzahl gibt es nicht. Laut The Tie Bar hängt die Länge vom Körper ab: vom Rumpf, von der Leibhöhe der Hose und vom Knoten. Ein dicker Knoten braucht mehr Stoff. Große Männer brauchen längere Krawatten.",
        b5_head="Keine feste Zahl", b5_l=("Dein Körper", "Rumpf und Leibhöhe"), b5_r=("Dein Knoten", "dick heißt mehr Stoff"),
        b5_at=dict(left_at="w:Körper", p1="w:Rumpf", p2="w:Leibhöhe", left_tag_at="w:Leibhöhe", right_at="w:Knoten",
                   p3="w:dicker", right_tag_at="w:braucht", marker="w:Laut"),
        b6="Kurz gesagt: Die Spitze endet etwa am Bund, nicht darüber und nicht darunter. Das breite Blatt reicht mindestens bis zum Gürtel. Und die richtige Länge misst du an deinem Körper, nicht in Zentimetern.",
        b6_head="Kurz gesagt",
        b6_items=[("Etwa am Bund", "Oberkante von Schnalle oder Bund", "w:Spitze", "w:etwa", "w:Bund"),
                  ("Mindestens zum Gürtel", "Drake's, Krawattenmacher", "w:breite", None, "w:Gürtel"),
                  ("Maß ist dein Körper", "Rumpf, Leibhöhe und Knoten", "w:richtige", "w:Körper", None)],
        b6_marker="w:gesagt",
        b7="Die Spitze trifft den Bund. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Spitze am Bund.", b7_at=dict(fix_at="w:trifft", ring_at="w:Bund", statement_at="w:Bund", chip_at="w:Blick"),
        status="Krawatte, gebunden",
        states=["Spitze: ?", "zu kurz, zu lang", "Regel: am Bund", "Blatt bis zum Gürtel", "Maß: dein Körper", "etwa am Bund", "Spitze: am Bund"],
        desc="Wie lang sollte eine Krawatte sein? Laut The Tie Bar trifft die Spitze die Oberkante von Gürtelschnalle oder Hosenbund. Drake's: das breite Blatt reicht mindestens bis zum Gürtel. Eine feste Zentimeterzahl gibt es nicht.",
        tags=["herrenmode", "krawatte", "anzug", "stilregeln", "krawattenlänge"],
        hooks=[("H1", "question", "Wo endet die Krawattenspitze?"), ("H2", "misconception", "Krawattenlänge in Zentimetern? Gibt es nicht."),
               ("H3", "surprising_fact", "Die richtige Länge misst du am Bund"), ("H4", "concrete_risk", "Über dem Gürtel? Dann ist sie zu kurz."),
               ("H5", "demonstration", "Zu kurz, zu lang, richtig: der Vergleich")],
        visual="Hemd mit Krawatte und Gürtel, Lupe auf der Krawattenspitze",
    ),
    "en": dict(
        title="Tie length: the tip meets the waistband",
        q="Where should the tie tip end?",
        b1="The tie is knotted. But where exactly should the tip end? Above the belt, below it, or right in between?",
        hook_at=dict(badge_at="w:tip", loupe_at="w:tip", nie_at="w:between"),
        b2="On the left, it's too short and hangs above the belt. On the right, it's too long and disappears below the waistband. The Tie Bar, a tie maker, rules out both: never above the belt, never below the waistband.",
        b2_head="Too short, too long", b2_l=("Too short", "hangs above the belt"), b2_r=("Too long", "disappears below the band"),
        b2_at=dict(left_at="w:left", left_tag_at="w:hangs", right_at="w:right", right_tag_at="w:disappears",
                   pl="w:never", pr="w:never#2", marker="w:maker"),
        b3="The rule from The Tie Bar: the tip meets the top edge of the belt buckle or the waistband. No higher and no lower. So it ends roughly at the waistband.",
        b3_head="Where exactly?", b3_label="The tip meets the waistband",
        b3_at=dict(pointer_at="w:rule", error_at="w:Tie", zoom_at="w:tip", flip_at="w:meets", label_at="w:edge"),
        b3_marker="w:edge",
        b4="The tie maker Drake's puts it as a minimum: the wide blade should reach at least to the belt. And the narrow end? That can go into the keeper loop at the back.",
        b4_head="The minimum", b4_stage="Drake's says",
        b4_tags=[("tie_tip", "wide blade", "at least to the belt", "always", "w:wide"),
                 ("placket", "narrow end", "into the keeper loop", "sometimes", "w:narrow")],
        b4_focus="w:keeper", b4_marker="w:Drake",
        b5="There is no fixed number of inches. According to The Tie Bar, the length depends on your body: your torso, the rise of your trousers and your knot. A thicker knot needs more fabric. And taller men need longer ties.",
        b5_head="No fixed number", b5_l=("Your body", "torso and rise"), b5_r=("Your knot", "thicker means more fabric"),
        b5_at=dict(left_at="w:body", p1="w:torso", p2="w:rise", left_tag_at="w:rise", right_at="w:knot",
                   p3="w:thicker", right_tag_at="w:needs", marker="w:According"),
        b6="In short: the tip ends roughly at the waistband, never above and never below it. The wide blade reaches at least to the belt. And you measure the right length against your own body, not in inches.",
        b6_head="In short",
        b6_items=[("Roughly at the waistband", "top edge of buckle or waistband", "w:tip", "w:roughly", "w:waistband"),
                  ("At least to the belt", "Drake's, tie makers", "w:wide", None, "w:belt"),
                  ("Your body is the measure", "torso, rise and knot", "w:measure", "w:body", None)],
        b6_marker="w:short",
        b7="The tip meets the waistband. For more eye for detail: follow Suitwerk.",
        b7_stmt="Tip at the waistband.", b7_at=dict(fix_at="w:meets", ring_at="w:waistband", statement_at="w:waistband", chip_at="w:eye"),
        status="Tie, knotted",
        states=["tie tip: ?", "too short, too long", "rule: at the band", "blade to the belt", "measure: your body", "roughly at the band", "tip: at the band"],
        desc="How long should a tie be? The Tie Bar says the tip meets the top of the belt buckle or waistband. Drake's: the wide blade reaches at least to the belt. There is no fixed number of inches.",
        tags=["menswear", "tie", "suit", "styletips", "tielength"],
        hooks=[("H1", "question", "Where should the tie tip end?"), ("H2", "misconception", "A set tie length in inches? There is none."),
               ("H3", "surprising_fact", "The right tie length is measured at the waistband"), ("H4", "concrete_risk", "Above the belt? Then it is too short."),
               ("H5", "demonstration", "Too short, too long, just right: side by side")],
        visual="Shirt with tie and belt, loupe on the tie tip",
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"] if 1 <= i <= 3 else ["S1"], t["visual"]) for i, (h, ty, os) in enumerate(t["hooks"])]
    a2, a3, a5 = t["b2_at"], t["b3_at"], t["b5_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in t["b4_tags"]]
    objs = [(LONG, {"tie_tip": 585}, "tie_tip"), (OK, None, "belt"), (K_SLIM, {"knot": "windsor"}, None)]
    items = []
    for (title, sub, at, then_at, ring_at), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": then_at})
        if ring:
            it.update({"ring": ring, "ring_at": ring_at})
        items.append(it)
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": OK, "target": "tie_tip", "badge": "?", "question_at": 0.3, **t["hook_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 14, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": SHORT, "target": "tie_tip", "tag": t["b2_l"][1],
                           "pulses": [{"target": "belt", "at": a2["pl"], "tone": "red"}]},
                  "right": {"title": t["b2_r"][0], "object": LONG, "target": "tie_tip", "tag": t["b2_r"][1],
                            "pulses": [{"target": "waistband", "at": a2["pr"], "tone": "red"}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": a2["marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_fitting", "duration_hint": 10, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "from": SHORT, "to": OK, "target": "tie_tip", "zoom": 1.4, "label": t["b3_label"],
                  "backdrop": True, "hold_end": True, **a3},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_ladder", "duration_hint": 10, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "stages": [{"object": OK, "at": 0.0, "title": t["b4_stage"], "tags": tags, "focus_at": t["b4_focus"]}],
                  "backdrop": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_compare", "duration_hint": 14, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "left": {"title": t["b5_l"][0], "object": OK, "tag": t["b5_l"][1],
                           "pulses": [{"target": "placket", "at": a5["p1"]}, {"target": "waistband", "at": a5["p2"]}]},
                  "right": {"title": t["b5_r"][0], "object": K_BIG, "target": "knot", "tag": t["b5_r"][1],
                            "pulses": [{"target": "knot", "at": a5["p3"]}]},
                  "left_at": a5["left_at"], "left_tag_at": a5["left_tag_at"], "right_at": a5["right_at"], "right_tag_at": a5["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S1"], "overlay": {"marker": "fakt", "marker_at": a5["marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 13, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2"], "overlay": {"marker": "auslegung", "marker_at": t["b6_marker"]}},
        closing_beat(lang, t["b7"], LONG, OK, "tie_tip", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "muted", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"],
                 notes="Suitwerk Woche 1 (Vorlage 1.0). Thema A04 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S2; keine Zentimeter- oder Zollangaben, 'etwa am Bund' laut Recherche-Hinweis.",
                 sources=SOURCES, hooks=hooks, hook_note="Frage nach dem Punkt, an dem die Spitze endet; das Video beantwortet sie Schritt für Schritt.",
                 beats=beats, status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Oberkante oder Mitte der Schnalle: Ratgeber uneinheitlich; im Video 'etwa am Bund'.",
                             "Zollangaben der Tie Bar sind Hausmaße; nicht im Video."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
