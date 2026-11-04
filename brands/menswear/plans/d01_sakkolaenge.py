"""D01 Sakkolänge: Wie lang muss ein Sakko sein? (09.11.2026, Thema 3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261109-3"
FRONT = {"kind": "jacket", "variant": "sb2", "fastened": [0], "strain": False}
FRONT_CUFF = {"kind": "jacket", "variant": "sb2", "fastened": [0], "cuff": 14, "strain": False}
BACK = {"kind": "jacket_back", "vents": "centre"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://suitsupply.com/en-de/journal/how-it-should-fit.html", "title": "Suitsupply, How it should fit: der Saum soll das Gesäß nur knapp bedecken; darüber zu kurz, deutlich darunter zu lang", "checked_at": CHECKED, "label": "Suitsupply, Journal"},
    {"id": "S2", "url": "https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/", "title": "Proper Cloth, Advanced tips for tailored jacket fit: hinten bis zum Ansatz des Gesäßes, vorn bis zum Ende des Hosenschlitzes; Regel 'fairly loose', kürzer moderner, länger klassischer", "checked_at": CHECKED, "label": "Proper Cloth, Reference"},
    {"id": "S3", "url": "https://tmlewin.co.uk/blogs/the-fitting-room/how-a-suit-should-fit", "title": "T.M. Lewin, How a suit should fit: Saum bedeckt das Gesäß; Fingerknöchel als gängiges Bild, 'depends on style'", "checked_at": CHECKED, "label": "T.M. Lewin, Fitting Room"},
]

T = {
    "de": dict(
        title="Wie lang muss ein Sakko sein?",
        q="Wie lang muss ein Sakko sein?",
        b1="Ein Sakko, das zu kurz ist, fällt auf. Eins, das zu lang ist, auch. Wie lang muss ein Sakko also sein?",
        b1_at=dict(badge_at="w:kurz", loupe_at="w:kurz", nie_at="w:Wie"),
        b2="Die Antwort liegt hinten. Dreh das Sakko um. Suitsupply schreibt: Der Saum soll das Gesäß nur knapp bedecken. Endet er darüber, ist das Sakko zu kurz. Liegt er deutlich darunter, ist es zu lang.",
        b2_head="Wo endet der Saum?", b2_l=("Vorn", "der Saum vorn"), b2_r=("Hinten", "Gesäß knapp bedeckt"),
        b2_at=dict(left_at=0.3, left_tag_at="w:Antwort", right_at="w:Dreh", right_tag_at="w:knapp", short="w:kurz", long="w:lang"),
        b3="Proper Cloth gibt dir zwei Bezugspunkte. Hinten reicht der Saum bis zum Ansatz des Gesäßes. Vorn endet er etwa dort, wo der Hosenschlitz endet. So prüfst du die Länge von beiden Seiten.",
        b3_head="Zwei Bezugspunkte",
        b3_st=[("Hinten", "bis Gesäßansatz", "laut Proper Cloth", "w:Ansatz"), ("Vorn", "bis Schlitzende", "Ende Hosenschlitz", "w:Hosenschlitz")],
        b3_stage2="w:Vorn", b3_focus="w:beiden",
        b4="Dazu nennt T.M. Lewin ein gängiges Bild: Lass die Arme hängen, dann liegt der Saum etwa auf Höhe der Fingerknöchel. Aber auch dort heißt es: Das hängt vom Stil ab.",
        b4_head="Die Hand als Maß?", b4_label="Fingerknöchel: nur ein Bild",
        b4_at=dict(pointer_at="w:Bild", zoom_at="w:Arme", flip_at="w:Saum", label_at="w:Fingerknöchel"),
        b5="Wie streng ist das? Auch Proper Cloth nennt die Regel ausdrücklich locker. Ein kürzeres Sakko wirkt moderner, ein längeres klassischer. Die Faustregel ist also ein Rahmen, kein Millimetermaß.",
        b5_head="Wie streng ist das?", b5_stage="Spielraum",
        b5_tags=[("waist", "Regel: locker", "laut Proper Cloth", "w:locker"),
                 ("pocket", "kürzer: modern", "nach Stil", "w:kürzeres"),
                 ("quarters", "länger: klassisch", "nach Stil", "w:längeres")],
        b5_focus="w:Rahmen",
        b6="Kurz gesagt: Hinten bedeckt der Saum das Gesäß gerade so, wie Suitsupply und T.M. Lewin schreiben. Vorn endet er etwa am Ende des Hosenschlitzes. Innerhalb dieses Rahmens entscheidet dein Stil.",
        b6_head="Kurz gesagt",
        b6_items=[("Hinten: Gesäß bedeckt", "knapp, laut Suitsupply", "w:Hinten", "w:Gesäß"),
                  ("Vorn: Ende Hosenschlitz", "laut Proper Cloth", "w:Vorn", "w:Hosenschlitz"),
                  ("Rahmen, kein Maß", "kürzer modern, länger klassisch", "w:Rahmens", "w:Stil")],
        b7="Dreh dich um: Der Saum bedeckt das Gesäß gerade so. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Gesäß knapp bedeckt.", b7_at=dict(fix_at="w:um", ring_at="w:Gesäß", statement_at="w:Gesäß", chip_at="w:Blick"),
        status="Sakko, Länge",
        states=["Länge: ?", "zu kurz oder zu lang", "hinten und vorn", "Knöchel: nur ein Bild", "Regel: locker", "Rahmen, kein Maß", "Gesäß bedeckt"],
        desc="Wie lang muss ein Sakko sein? Der Saum bedeckt das Gesäß gerade so, sagen Suitsupply und T.M. Lewin; Proper Cloth nennt dazu Bezugspunkte hinten und vorn und die Regel ausdrücklich locker.",
        tags=["herrenmode", "sakko", "anzug", "passform", "stilregeln"],
        hooks=[("H1", "question", "Wie lang muss ein Sakko sein?", []),
               ("H2", "misconception", "Sakkolänge nach Gefühl? Es gibt einen Bezugspunkt.", ["S1", "S2"]),
               ("H3", "surprising_fact", "Die Längenregel ist laut Proper Cloth locker", ["S2"]),
               ("H4", "concrete_risk", "Saum über dem Gesäß: Das Sakko ist zu kurz", ["S1"]),
               ("H5", "demonstration", "Dreh das Sakko um, dann siehst du es", [])],
    ),
    "en": dict(
        title="How long should a suit jacket be?",
        q="How long should a jacket be?",
        b1="A jacket that is too short gets noticed. So does one that is too long. So how long should a suit jacket be?",
        b1_at=dict(badge_at="w:short", loupe_at="w:short", nie_at="w:how"),
        b2="The answer is at the back. Turn the jacket around. Suitsupply puts it simply: the hem should just cover your seat. If it ends above, the jacket is too short. If it falls well below, it is too long.",
        b2_head="Where does the hem end?", b2_l=("Front", "the hem at the front"), b2_r=("Back", "seat just covered"),
        b2_at=dict(left_at=0.3, left_tag_at="w:answer", right_at="w:Turn", right_tag_at="w:cover", short="w:short", long="w:long"),
        b3="Proper Cloth gives you two reference points. At the back, the hem reaches the base of your seat. At the front, it ends roughly where your trouser fly ends. That way you can check the length from both sides.",
        b3_head="Two reference points",
        b3_st=[("Back", "to the seat's base", "says Proper Cloth", "w:base"), ("Front", "to the fly's end", "where the fly ends", "w:fly")],
        b3_stage2="w:front", b3_focus="w:both",
        b4="T.M. Lewin adds a common rule of thumb: let your arms hang, and the hem sits roughly level with your knuckles. But even there, it says this depends on style.",
        b4_head="The hand as a guide?", b4_label="Knuckles: just a guide",
        b4_at=dict(pointer_at="w:rule", zoom_at="w:arms", flip_at="w:hem", label_at="w:knuckles"),
        b5="How strict is this? Proper Cloth calls the rule fairly loose. A shorter jacket looks more modern, a longer one more classic. So the rule of thumb is a frame, not an exact measurement.",
        b5_head="How strict is this?", b5_stage="Leeway",
        b5_tags=[("waist", "rule: fairly loose", "says Proper Cloth", "w:loose"),
                 ("pocket", "shorter: modern", "a style choice", "w:shorter"),
                 ("quarters", "longer: classic", "a style choice", "w:longer")],
        b5_focus="w:frame",
        b6="In short: at the back, the hem just covers your seat, as Suitsupply and T.M. Lewin put it. At the front, it ends roughly where the fly ends. Within that frame, your style decides.",
        b6_head="In short",
        b6_items=[("Back: seat covered", "just, says Suitsupply", "w:back", "w:seat"),
                  ("Front: end of the fly", "according to Proper Cloth", "w:front", "w:fly"),
                  ("A frame, not a rule", "shorter modern, longer classic", "w:frame", "w:style")],
        b7="Turn around: the hem just covers your seat. For more eye for detail: follow Suitwerk.",
        b7_stmt="Seat just covered.", b7_at=dict(fix_at="w:around", ring_at="w:seat", statement_at="w:seat", chip_at="w:eye"),
        status="Jacket, length",
        states=["length: ?", "too short or too long", "back and front", "knuckles: a guide", "rule: fairly loose", "a frame, not a rule", "seat covered"],
        desc="How long should a suit jacket be? The hem just covers your seat, say Suitsupply and T.M. Lewin; Proper Cloth adds reference points at the back and front and calls the rule fairly loose.",
        tags=["menswear", "suitjacket", "suit", "fit", "styletips"],
        hooks=[("H1", "question", "How long should a jacket be?", []),
               ("H2", "misconception", "Jacket length by feel? There is a reference point.", ["S1", "S2"]),
               ("H3", "surprising_fact", "Proper Cloth calls the length rule fairly loose", ["S2"]),
               ("H4", "concrete_risk", "Hem above your seat: the jacket is too short", ["S1"]),
               ("H5", "demonstration", "Turn the jacket around and you will see it", [])],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Sakko von vorn, Lupe auf dem Saum") for h, ty, os, src in t["hooks"]]
    a2, a4 = t["b2_at"], t["b4_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": "sometimes", "at": at} for sp, tx, sub, at in t["b5_tags"]]
    objs = [(BACK, None, "hem"), (FRONT, None, "hem"), (FRONT, None, "cuff")]
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
         "data": {"question": t["q"], "object": FRONT, "target": "quarters", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": FRONT, "tag": t["b2_l"][1]},
                  "right": {"title": t["b2_r"][0], "object": BACK, "target": "hem", "tag": t["b2_r"][1],
                            "pulses": [{"target": "hem", "at": a2["short"], "tone": "red"}, {"target": "hem", "at": a2["long"], "tone": "red"}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Suitsupply"}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "backdrop": True, "hold_end": True,
                  "stages": [{"object": obj, "at": 0.0 if k == 0 else t["b3_stage2"], "title": title,
                              "tags": [{"spot": "hem", "text": tx, "sub": sub, "tone": "always", "at": at}],
                              **({"focus_at": t["b3_focus"]} if k == 1 else {})}
                             for k, ((title, tx, sub, at), obj) in enumerate(zip(t["b3_st"], (BACK, FRONT)))]},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Proper"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": FRONT, "to": FRONT_CUFF, "target": "cuff", "zoom": 1.4, "label": t["b4_label"],
                  "backdrop": True, "hold_end": True, **a4},
         "source_ids": ["S3"],
         "overlay": {"transition": {"type": "iris", "x": 330, "y": 990, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a4["pointer_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 11, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": [{"object": FRONT, "at": 0.0, "title": t["b5_stage"], "tags": tags, "focus_at": t["b5_focus"]}],
                  "backdrop": True},
         "source_ids": ["S2", "S3"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Proper"}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], FRONT, BACK, "hem", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "amber", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema D01 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Konvention mit Spielraum, keine Aussage über Körpergröße oder Figur.",
                 sources=SOURCES, hooks=hooks, hook_note="Frage aus dem Titel, die Lupe zeigt den Saum.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Daumen-Regel: in keiner Primärquelle gefunden, nicht im Video.",
                             "Rückenlänge vom Schneider nicht änderbar (Proper Cloth, Änderungsseite): Seite nicht in den Recherche-URLs, nicht im Video."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
