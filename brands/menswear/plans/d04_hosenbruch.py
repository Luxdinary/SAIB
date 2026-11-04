"""D04 Hosenbruch: kein, halb, voll (15.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261115-2"
NONE = {"kind": "legs", "break": "none", "shoe": "oxford"}
HALF = {"kind": "legs", "break": "slight", "shoe": "oxford"}
FULL = {"kind": "legs", "break": "full", "shoe": "oxford"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://propercloth.com/reference/what-is-pant-break/",
     "title": "Proper Cloth, What is pant break: kein Bruch = Saum berührt den Schuh; halber Bruch = etwas Stoff staut sich, keine Socke sichtbar; voller Bruch = deutliche Falte, weitere Fußweite, am traditionellsten; gilt für Schnürschuhe, beim Loafer anders",
     "checked_at": CHECKED, "label": "Proper Cloth"},
    {"id": "S2", "url": "https://www.moss.co.uk/inside-pocket/post/the-suit-fit-guide",
     "title": "Moss, The Suit Fit Guide: Slim ohne Bruch, Tailored weicher Bruch (höchstens eine Falte), Regular und Relaxed ausgeprägter Bruch",
     "checked_at": CHECKED, "label": "Moss, Fit Guide"},
    {"id": "S3", "url": "https://suitsupply.com/en-de/journal/how-it-should-fit.html",
     "title": "Suitsupply, How it should fit: klassisch ein Bruch, modern ohne Bruch bis zur Schuhoberkante",
     "checked_at": CHECKED, "label": "Suitsupply"},
    {"id": "S4", "url": "https://www.hackett.com/intl/en/men/b/trousers/suit-trousers/",
     "title": "Hackett, Suit Trousers: halber Bruch als idealer Saumabschluss, Saum liegt leicht auf dem Schuh, eine saubere Falte",
     "checked_at": CHECKED, "label": "Hackett"},
]

T = {
    "de": dict(
        title="Hosenbruch: kein, halb oder voll",
        q="Kein, halb oder voll: Welcher Bruch?",
        b1="Unten am Schuh wirft die Hose eine kleine Falte. Oder gar keine. Oder eine tiefe. Welche ist die richtige?",
        hook_at=dict(badge_at="w:Falte", loupe_at="w:Falte", nie_at="w:richtige"),
        b2="Die Häuser sind sich nicht einig. Hackett nennt den halben Bruch den idealen Abschluss, mit einer sauberen Falte. Suitsupply sagt: Klassisch ist ein Bruch. Modern endet die Hose ohne Bruch an der Schuhoberkante.",
        b2_head="Wer hat recht?", b2_l=("Laut Hackett", "halber Bruch: ideal"), b2_r=("Laut Suitsupply", "modern: ohne Bruch"), b2_tag2="klassisch: ein Bruch",
        b2_at=dict(left_at="w:Hackett", left_tag_at="w:idealen", pl="w:Falte", right_at="w:Suitsupply", tag2_at="w:Klassisch",
                   right_tag_at="w:Modern", pr="w:Schuhoberkante", marker="w:einig"),
        b3="Proper Cloth beschreibt die Stufen genauer. Kein Bruch heißt: Der Saum berührt gerade eben den Schuh. Halber Bruch heißt: Etwas Stoff staut sich auf, und keine Socke ist zu sehen.",
        b3_head="Die Stufen",
        b3_s0=("Kein Bruch", [("hem", "berührt den Schuh", "der Saum", "always", "w:berührt")]),
        b3_s1=("Halber Bruch", "w:Halber", [("break", "Stoff staut sich", "etwas, eine Falte", "always", "w:staut"),
                                            ("sock", "keine Socke", "bleibt verdeckt", "always", "w:Socke")]),
        b3_marker="w:Proper",
        b4="Der volle Bruch wirft eine deutliche Falte, dazu kommt eine weitere Fußweite. Proper Cloth nennt ihn die traditionellste Form. Moss ordnet ihn Regular und Relaxed zu. Die schmale Slim-Hose endet dagegen ohne Bruch.",
        b4_head="Voll oder ohne", b4_l=("Voller Bruch", "deutliche Falte, weit"), b4_r=("Slim", "ohne Bruch, laut Moss"),
        b4_at=dict(left_at="w:volle", pl="w:deutliche", left_tag_at="w:Fußweite", right_at="w:Slim", right_tag_at="w:endet", pr="w:ohne", marker="w:Proper"),
        b5="Moss gibt der Tailored-Hose einen weichen Bruch mit höchstens einer Falte. Und Proper Cloth schreibt: Die Stufen gelten für Schnürschuhe. Beim Loafer ist die Kappe hinten niedriger, der Bruch wirkt dort anders.",
        b5_head="Zwei Hinweise", b5_stage="Am Schuh",
        b5_tags=[("break", "weicher Bruch", "Tailored, laut Moss", "always", "w:weichen"),
                 ("lacing", "nur Schnürschuh", "beim Loafer anders", "sometimes", "w:Schnürschuhe")],
        b5_marker="w:Moss",
        b6="Kurz gesagt: Kein Bruch passt zur schmalen Hose, der volle zur weiten, der halbe liegt dazwischen. Welche Stufe du wählst, ist eine Stilfrage, und die Häuser setzen verschiedene Ideale.",
        b6_head="Kurz gesagt",
        b6_items=[("Kein Bruch", "Saum berührt den Schuh", "w:Kein", "w:schmalen"),
                  ("Voller Bruch", "deutliche Falte, weite Hose", "w:volle", "w:weiten"),
                  ("Halber Bruch", "eine Falte, keine Socke", "w:halbe", "w:dazwischen")],
        b6_marker="w:gesagt",
        b7="Kein, halb oder voll: Der Bruch folgt dem Bein. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Bruch folgt dem Bein.", b7_at=dict(fix_at="w:Bruch", ring_at="w:Bein", statement_at="w:Bein", chip_at="w:Blick"),
        status="Hose, Saum",
        states=["Bruch: ?", "Häuser uneinig", "Stufen: kein, halb", "voll oder ohne", "Loafer: wirkt anders", "Stilfrage", "Bruch passt zum Bein"],
        desc="Hosenbruch: kein, halb oder voll? Proper Cloth beschreibt die Stufen, Moss koppelt sie an den Schnitt, Hackett nennt den halben Bruch ideal, Suitsupply den Bruch klassisch und ohne Bruch modern. Eine Stilfrage.",
        tags=["herrenmode", "anzughose", "hosenbruch", "stilregeln", "anzug"],
        hooks=[("H1", "question", "Kein, halb oder voll: Welcher Bruch?"), ("H2", "misconception", "Den einen richtigen Hosenbruch gibt es nicht"),
               ("H3", "surprising_fact", "Beim Loafer wirkt derselbe Bruch anders"), ("H4", "concrete_risk", "Sieht man beim halben Bruch die Socke? Nein."),
               ("H5", "demonstration", "Drei Stufen am Hosensaum im Vergleich")],
        visual="Hosenbein mit Schuh, Lupe auf der Falte am Saum",
    ),
    "en": dict(
        title="Trouser break: none, half or full",
        q="None, half or full: which break?",
        b1="Down at the shoe, the trouser makes a small fold. Or none at all. Or a deep one. Which of them is right?",
        hook_at=dict(badge_at="w:fold", loupe_at="w:fold", nie_at="w:right"),
        b2="The houses do not agree. Hackett calls the half break the ideal finish, with one clean fold. Suitsupply says a single break is classic, while the modern look ends with no break at the top of the shoe.",
        b2_head="Who is right?", b2_l=("Hackett says", "half break: ideal"), b2_r=("Suitsupply says", "modern: no break"), b2_tag2="classic: one break",
        b2_at=dict(left_at="w:Hackett", left_tag_at="w:ideal", pl="w:fold", right_at="w:Suitsupply", tag2_at="w:classic",
                   right_tag_at="w:modern", pr="w:top", marker="w:agree"),
        b3="Proper Cloth describes the steps more precisely. With no break, the hem just touches the top of the shoe. With a half break, no sock shows, and a little fabric gathers on the shoe.",
        b3_head="The steps",
        b3_s0=("No break", [("hem", "touches the shoe", "the hem", "always", "w:touches")]),
        b3_s1=("Half break", "w:half", [("break", "fabric gathers", "a little, one fold", "always", "w:gathers"),
                                        ("sock", "no sock shows", "stays covered", "always", "w:sock")]),
        b3_marker="w:Proper",
        b4="A full break makes a distinct fold and comes with a wider leg. Proper Cloth calls it the most traditional. Moss gives it to its Regular and Relaxed fits. The narrow Slim trouser ends with no break.",
        b4_head="Full or none", b4_l=("Full break", "distinct fold, wide leg"), b4_r=("Slim", "no break, says Moss"),
        b4_at=dict(left_at="w:full", pl="w:distinct", left_tag_at="w:wider", right_at="w:Slim", right_tag_at="w:ends", pr="w:no", marker="w:Proper"),
        b5="Moss gives the Tailored fit a soft break, one fold at most. Proper Cloth notes that these steps apply to lace-up shoes. On a loafer the back sits lower, so the same break looks different.",
        b5_head="Two more notes", b5_stage="At the shoe",
        b5_tags=[("break", "soft break", "Tailored, per Moss", "always", "w:soft"),
                 ("lacing", "lace-ups only", "loafers look different", "sometimes", "w:lace")],
        b5_marker="w:Moss",
        b6="In short: no break suits a narrow trouser, a full break a wide one, and the half break sits in between. The choice is a matter of style, and the houses name different ideals.",
        b6_head="In short",
        b6_items=[("No break", "the hem touches the shoe", "w:no", "w:narrow"),
                  ("Full break", "distinct fold, wide trouser", "w:full", "w:wide"),
                  ("Half break", "one fold, no sock showing", "w:half", "w:between")],
        b6_marker="w:short",
        b7="None, half or full: the break follows the leg. For more eye for detail: follow Suitwerk.",
        b7_stmt="Break follows the leg.", b7_at=dict(fix_at="w:break", ring_at="w:leg", statement_at="w:leg", chip_at="w:eye"),
        status="Trousers, hem",
        states=["break: ?", "houses disagree", "steps: none, half", "full or none", "loafer: different", "a matter of style", "break fits the leg"],
        desc="Trouser break: none, half or full? Proper Cloth describes the steps, Moss ties them to the cut, Hackett calls the half break ideal, Suitsupply calls one break classic and no break modern. A matter of style.",
        tags=["menswear", "suittrousers", "trouserbreak", "styletips", "suit"],
        hooks=[("H1", "question", "None, half or full: which break?"), ("H2", "misconception", "There is no single right trouser break"),
               ("H3", "surprising_fact", "On a loafer the same break looks different"), ("H4", "concrete_risk", "Does a half break show your socks? No."),
               ("H5", "demonstration", "Three trouser breaks side by side")],
        visual="Trouser leg with shoe, loupe on the fold at the hem",
    ),
}


def _tags(rows):
    return [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in rows]


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2", "S4"] if 1 <= i <= 3 else ["S1"], t["visual"]) for i, (h, ty, os) in enumerate(t["hooks"])]
    a2, a4 = t["b2_at"], t["b4_at"]
    items = [{"title": ti, "sub": sub, "object": obj, "at": at, "ring": ring, "ring_at": rat}
             for (ti, sub, at, rat), obj, ring in zip(t["b6_items"], (NONE, FULL, HALF), ("hem", "break", "break"))]
    s0_title, s0_tags = t["b3_s0"]
    s1_title, s1_at, s1_tags = t["b3_s1"]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": HALF, "target": "break", "badge": "?", "question_at": 0.3, **t["hook_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": HALF, "target": "break", "tag": t["b2_l"][1],
                           "pulses": [{"target": "break", "at": a2["pl"], "tone": "amber"}]},
                  "right": {"title": t["b2_r"][0], "object": NONE, "target": "hem", "tag": t["b2_r"][1],
                            "tag2": t["b2_tag2"], "tag2_at": a2["tag2_at"], "pulses": [{"target": "hem", "at": a2["pr"], "tone": "amber"}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S4", "S3"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "unsicher", "marker_at": a2["marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 11, "spoken": t["b3"],
         "data": {"headline": t["b3_head"],
                  "stages": [{"object": NONE, "at": 0.0, "title": s0_title, "tags": _tags(s0_tags)},
                             {"object": HALF, "at": s1_at, "title": s1_title, "tags": _tags(s1_tags)}],
                  "backdrop": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": FULL, "target": "break", "tag": t["b4_l"][1],
                           "pulses": [{"target": "break", "at": a4["pl"]}]},
                  "right": {"title": t["b4_r"][0], "object": NONE, "target": "hem", "tag": t["b4_r"][1],
                            "pulses": [{"target": "hem", "at": a4["pr"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S1", "S2"], "overlay": {"marker": "fakt", "marker_at": a4["marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": [{"object": HALF, "at": 0.0, "title": t["b5_stage"], "tags": _tags(t["b5_tags"])}],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2", "S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3", "S4"], "overlay": {"marker": "auslegung", "marker_at": t["b6_marker"]}},
        closing_beat(lang, t["b7"], FULL, HALF, "break", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"],
                 notes="Suitwerk Woche 1 (Vorlage 1.0). Thema D04 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S4; keine Stufe als allgemein richtig, die Häuser nennen verschiedene Ideale (Marker 'unsicher' in b2).",
                 sources=SOURCES, hooks=hooks, hook_note="Frage nach der richtigen Stufe; die Antwort ist: Stilfrage, an den Schnitt gekoppelt.",
                 beats=beats, status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Ideale der Häuser widersprechen sich (Hackett halber Bruch, Suitsupply klassisch ein Bruch / modern ohne); im Video als offen markiert.",
                             "Loafer: Zeichnung zeigt nur Schnürschuhe."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
