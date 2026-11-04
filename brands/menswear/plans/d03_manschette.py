"""D03 Wie viel Manschette unter dem Sakkoärmel? Eine Spanne statt eines festen Werts (13.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261113-2"


def J(cuff: float) -> dict:
    """Einreiher (zwei Knöpfe, oberer zu) mit sichtbarer Hemdmanschette in viewBox-Einheiten (etwa 10 = 1 cm)."""
    return {"kind": "jacket", "variant": "sb2", "fastened": [0], "cuff": cuff}


CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://suitsupply.com/en-us/journal/how-it-should-fit-jacket.html", "title": "Suitsupply, How it should fit (Jacket): Ärmel endet knapp über dem Handgelenkknochen, etwa 1,5 cm (half an inch) Hemd sichtbar; gar keine Manschette sichtbar: zuerst kleinere Größe probieren", "checked_at": CHECKED, "label": "Suitsupply"},
        {"id": "S2", "url": "https://www.moss.co.uk/inside-pocket/post/the-suit-fit-guide", "title": "Moss, The suit fit guide: Sakkoärmel etwa auf dem Handgelenkknochen, Hemdmanschette 1 bis 2 cm länger", "checked_at": CHECKED, "label": "Moss"},
        {"id": "S3", "url": "https://tmlewin.co.uk/blogs/the-fitting-room/how-a-suit-should-fit", "title": "T.M. Lewin, How a suit should fit: 1/4 bis 1/2 Zoll (ca. 0,6 bis 1,3 cm) Manschette bei entspannten Armen", "checked_at": CHECKED, "label": "T.M. Lewin"},
        {"id": "S4", "url": "https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/", "title": "Proper Cloth, Advanced tips for tailored jacket fit: 0,25 bis 0,5 Zoll; weniger wirkt konservativer, mehr moderner", "checked_at": CHECKED, "label": "Proper Cloth"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Wie viel Manschette unter dem Sakkoärmel?",
        q="Wie viel Manschette?",
        b1="Unter dem Sakkoärmel schaut ein Streifen Hemd hervor. Aber wie viel davon solltest du eigentlich sehen? Einen festen Wert gibt es nicht.",
        b1_at=("w:Streifen", "w:sehen"),
        b2="Erst der klare Fehler: Sieht man gar keine Manschette, stimmt die Passform nicht. Suitsupply rät dann, zuerst eine kleinere Größe zu probieren. Null ist hier also keine Stilvariante, sondern ein Hinweis auf die Größe.",
        b2_head="Gar keine Manschette?", b2_label="Suitsupply: kleiner probieren",
        b2_at=dict(pointer_at="w:Fehler", zoom_at="w:gar", flip_at="w:keine", error_at="w:Passform", label_at="w:kleinere"), b2_marker="w:Suitsupply",
        b3="Der Maßstab ist der Ärmel, nicht das Hemd. Laut Suitsupply endet er knapp über dem Handgelenkknochen, laut Moss etwa auf ihm. Die Hemdmanschette ist etwas länger und schaut deshalb unter dem Ärmel hervor.",
        b3_head="Wo der Ärmel endet", b3_stage="Ärmel und Hemd",
        b3_tags=[("sleeve", "Ärmel: Handgelenk", "knapp über dem Knochen", "always", "w:Handgelenkknochen"),
                 ("cuff", "Hemd: etwas länger", "zeigt sich darunter", "always", "w:Hemdmanschette")],
        b3_focus="w:hervor", b3_marker="w:Suitsupply",
        b4="Die Zahlen der Hersteller gehen etwas auseinander. T.M. Lewin nennt sechs Millimeter bis gut einen Zentimeter, bei locker hängenden Armen. Moss nennt einen bis zwei Zentimeter. Suitsupply liegt mit rund einem Zentimeter dazwischen.",
        b4_head="Wie viel genau?", b4_l=("T.M. Lewin", "0,6 bis 1,3 cm"), b4_r=("Moss", "1 bis 2 cm"), b4_tag2="Suitsupply: rund 1 cm",
        b4_at=dict(left_at="w:Lewin", left_tag_at="w:sechs", right_at="w:Moss", right_tag_at="w:zwei", tag2_at="w:Suitsupply",
                   pulse_l="w:Armen", pulse_r="w:Zentimeter#2"), b4_marker="w:Lewin",
        b5="Wo du in dieser Spanne landest, ist Geschmack. Proper Cloth beschreibt es so: Weniger Manschette wirkt konservativer, mehr wirkt moderner. Die Obergrenze in unseren Quellen liegt bei zwei Zentimetern.",
        b5_head="Weniger oder mehr?",
        b5_stages=(("Weniger", 0.0, [("cuff", "konservativer", "laut Proper Cloth", "sometimes", "w:konservativer")]),
                   ("Mehr", "w:mehr", [("cuff", "moderner", "laut Proper Cloth", "sometimes", "w:moderner"),
                                       ("sleeve", "höchstens 2 cm", "Obergrenze bei Moss", "sometimes", "w:zwei")])),
        b5_focus="w:Obergrenze", b5_marker="w:Proper",
        b6="Kurz gesagt: Der Ärmel endet am Handgelenk, darunter zeigen sich rund sechs Millimeter bis zwei Zentimeter Hemd. Wie viel genau, ist Geschmack. Gar keine Manschette dagegen ist ein Passformfehler.",
        b6_head="Kurz gesagt",
        b6_items=[("Ärmel: am Handgelenk", "knapp über dem Knochen", "w:Ärmel", "w:Handgelenk"),
                  ("Hemd: 0,6 bis 2 cm", "wie viel genau: Geschmack", "w:sechs", "w:Geschmack"),
                  ("Null: Passformfehler", "Suitsupply: kleiner probieren", "w:Gar", "w:Passformfehler")],
        b7="Ein schmaler Streifen Hemd, rund ein Zentimeter. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Rund ein Zentimeter.", b7_at=dict(fix_at="w:schmaler", ring_at="w:Hemd", statement_at="w:Zentimeter", chip_at="w:Blick"),
        status="Hemdmanschette",
        states=["Manschette: wie viel?", "keine: Passformfehler", "Ärmel: Handgelenk", "0,6 bis 2 cm", "Spanne: Geschmack", "Spanne, kein Fixwert", "rund 1 cm sichtbar"],
        desc="Wie viel Hemdmanschette unter dem Sakkoärmel? Kein fester Wert, sondern eine Spanne: T.M. Lewin, Suitsupply, Moss und Proper Cloth nennen rund 0,6 bis 2 cm. Gar keine gilt als Passformfehler.",
        tags=["herrenmode", "sakko", "hemd", "passform", "anzug"],
        hooks=[("H1", "question", "Wie viel Manschette?"), ("H2", "misconception", "Keine Manschette sichtbar? Das ist ein Passformfehler"),
               ("H3", "surprising_fact", "Einen festen Wert gibt es nicht, nur eine Spanne"), ("H4", "concrete_risk", "Gar keine Manschette? Dann lieber kleiner probieren"),
               ("H5", "demonstration", "Wie viel Hemd unter den Ärmel gehört")],
    ),
    "en": dict(
        title="How much shirt cuff should show?",
        q="How much shirt cuff?",
        b1="Below the jacket sleeve, a strip of shirt shows. How much of it should you see? There is no single fixed number.",
        b1_at=("w:strip", "w:see"),
        b2="First, the clear mistake: if no cuff shows at all, the fit is off. Suitsupply's advice is to try a smaller size first. So zero is not a style choice.",
        b2_head="No cuff at all?", b2_label="Suitsupply: try a size down",
        b2_at=dict(pointer_at="w:mistake", zoom_at="w:no", flip_at="w:shows", error_at="w:fit", label_at="w:smaller"), b2_marker="w:Suitsupply",
        b3="The sleeve sets the mark. Suitsupply ends it just above the wrist bone, Moss roughly on it. The shirt cuff is a little longer, so it peeks out below the sleeve.",
        b3_head="Where the sleeve ends", b3_stage="Sleeve and shirt",
        b3_tags=[("sleeve", "Sleeve: wrist bone", "just above it", "always", "w:wrist"),
                 ("cuff", "Shirt: longer", "shows below", "always", "w:shirt")],
        b3_focus="w:peeks", b3_marker="w:Suitsupply",
        b4="The numbers differ a little. T.M. Lewin gives a quarter to half an inch, with relaxed arms. Moss says one to two centimetres. Suitsupply sits in between, at about one centimetre.",
        b4_head="How much exactly?", b4_l=("T.M. Lewin", "0.6 to 1.3 cm"), b4_r=("Moss", "1 to 2 cm"), b4_tag2="Suitsupply: about 1 cm",
        b4_at=dict(left_at="w:Lewin", left_tag_at="w:quarter", right_at="w:Moss", right_tag_at="w:two", tag2_at="w:Suitsupply",
                   pulse_l="w:relaxed", pulse_r="w:centimetres"), b4_marker="w:Lewin",
        b5="Where you land in that range is a matter of taste. Proper Cloth puts it this way: less cuff looks more conservative, more looks more modern. The upper limit in our sources is two centimetres.",
        b5_head="Less or more?",
        b5_stages=(("Less", 0.0, [("cuff", "more conservative", "says Proper Cloth", "sometimes", "w:conservative")]),
                   ("More", "w:more#2", [("cuff", "more modern", "says Proper Cloth", "sometimes", "w:modern"),
                                         ("sleeve", "2 cm at most", "upper limit, Moss", "sometimes", "w:two")])),
        b5_focus="w:limit", b5_marker="w:Proper",
        b6="In short: the sleeve ends at the wrist, and below it shows about six millimetres to two centimetres of shirt. Exactly how much is taste. No cuff at all, though, is a fit problem.",
        b6_head="In short",
        b6_items=[("Sleeve: at the wrist", "just above the bone", "w:sleeve", "w:wrist"),
                  ("Shirt: 0.6 to 2 cm", "the exact amount is taste", "w:six", "w:taste"),
                  ("Zero: a fit problem", "Suitsupply: try a size down", "w:No", "w:problem")],
        b7="A narrow strip of shirt, about one centimetre. For more eye for detail: follow Suitwerk.",
        b7_stmt="About one centimetre.", b7_at=dict(fix_at="w:narrow", ring_at="w:shirt", statement_at="w:centimetre", chip_at="w:eye"),
        status="Shirt cuff",
        states=["cuff: how much?", "none: a fit problem", "sleeve: wrist bone", "0.6 to 2 cm", "range: taste", "a range, not a number", "about 1 cm showing"],
        desc="How much shirt cuff should show below the jacket sleeve? Not one fixed number but a range: T.M. Lewin, Suitsupply, Moss and Proper Cloth give roughly 0.6 to 2 cm. No cuff at all counts as a fit problem.",
        tags=["menswear", "jacketfit", "shirt", "tailoring", "suit"],
        hooks=[("H1", "question", "How much shirt cuff?"), ("H2", "misconception", "No cuff showing? That is a fit problem"),
               ("H3", "surprising_fact", "There is no fixed number, only a range"), ("H4", "concrete_risk", "No cuff at all? Try a size down first"),
               ("H5", "demonstration", "How much shirt belongs below the sleeve")],
    ),
}


def _tags(rows):
    return [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in rows]


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"], "Sakko, Lupe auf der Hemdmanschette") for h, ty, os in t["hooks"]]
    objs = [(J(12), None, "sleeve"), (J(7), {"cuff": 20}, None), (J(0), {"cuff": 12}, "cuff")]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    stages5 = [{"object": J((7, 20)[k]), "at": at, "title": title, "tags": _tags(rows)} for k, (title, at, rows) in enumerate(t["b5_stages"])]
    stages5[1]["focus_at"] = t["b5_focus"]
    a2, a4 = t["b2_at"], t["b4_at"]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": J(12), "target": "cuff", "badge": "?", "question_at": 0.3,
                  "badge_at": t["b1_at"][0], "loupe_at": t["b1_at"][0], "nie_at": t["b1_at"][1], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 10, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "from": J(12), "to": J(0), "target": "cuff", "zoom": 1.6, "strain": False, "label": t["b2_label"],
                  "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 751, "y": 879, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b2_marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": J(12), "at": 0.0, "title": t["b3_stage"], "tags": _tags(t["b3_tags"]), "focus_at": t["b3_focus"]}],
                  "backdrop": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": J(8), "target": "cuff", "tag": t["b4_l"][1],
                           "pulses": [{"target": "cuff", "at": a4["pulse_l"]}]},
                  "right": {"title": t["b4_r"][0], "object": J(20), "target": "cuff", "tag": t["b4_r"][1], "tag2": t["b4_tag2"], "tag2_at": a4["tag2_at"],
                            "pulses": [{"target": "cuff", "at": a4["pulse_r"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S3", "S2", "S1"], "overlay": {"marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": stages5, "backdrop": True, "hold_end": True},
         "source_ids": ["S4", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3", "S4"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], J(0), J(12), "cuff", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "amber", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema D03 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S4; Obergrenze 2 cm (Moss), Suitsupply als 'rund ein Zentimeter'; null als Passformfehler.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Frage nach der Menge am sichtbaren Detail, Antwort: eine Spanne.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Alte Obergrenze 2,5 cm nicht belegt, nicht im Video.",
                             "Suitsupply schreibt 'half an inch (1.5cm)'; rechnerisch 1,27 cm, daher 'rund ein Zentimeter'."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
