"""C02 Super 100s: was die Zahl bedeutet und was nicht (11.11.2026, menswear-20261111-3)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261111-3"
CLOTH = {"kind": "swatch", "weave": "worsted", "layers": 2}
FIBRE = {"kind": "fibres", "microns": [18.75]}
LADDER = {"kind": "fibres", "microns": [18.75, 16.25]}
THICK = {"kind": "fibres", "microns": [20.0]}
FINE = {"kind": "fibres", "microns": [17.0]}
YARN = {"kind": "yarn", "spin": "worsted"}
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://www.woolmark.com/globalassets/_06-new-woolmark/_industry/certification/_old-certification/product-specifications/f-6_fibre_quality_2016-1_22oct14_f.pdf", "title": "Woolmark, Spezifikation F-6: Super-S-System der IWTO, von Woolmark verwaltet; Super 100s höchstens 18,75 µm, Super 150s 16,25 µm; gemessen am Endprodukt ohne Toleranz; nur reine Schurwolle (bis 5 % Ziergarn)", "checked_at": CHECKED, "label": "Woolmark, Spezifikation F-6"},
        {"id": "S2", "url": "https://www.law.cornell.edu/cfr/text/16/300.20a", "title": "16 CFR 300.20a (US-Verordnung): 'Super 100's' falsch etikettiert, wenn der mittlere Faserdurchmesser nicht 18,75 µm oder feiner ist", "checked_at": CHECKED, "label": "US-Recht, 16 CFR 300.20a"},
        {"id": "S3", "url": "https://cashmere.org/definition-cashmere-wool.php", "title": "CCMI, Definition of wool: 'Super' nur für reine Schurwolle, Wert durch maximalen mittleren Faserdurchmesser bestimmt (IWTO-Code)", "checked_at": CHECKED, "label": "CCMI, Definition Wolle"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Super 100s: Was die Zahl auf dem Stoff bedeutet",
        q="Was heißt Super 100s?",
        b1="Super 100s steht auf manchem Anzugstoff. Es klingt nach einer Note für Qualität. Doch die Zahl misst genau eine Sache. Welche?",
        b1_at=dict(badge_at="w:Note", loupe_at="w:Zahl", nie_at="w:Welche"),
        b2="Geh ganz nah an den Stoff heran, bis zur einzelnen Wollfaser. Super 100s beschreibt den mittleren Durchmesser dieser Fasern. Das System gehört der IWTO, dem internationalen Wollverband, verwaltet wird es von Woolmark.",
        b2_head="Was wird gemessen?", b2_label="mittlerer Faserdurchmesser",
        b2_at=dict(pointer_at="w:Geh", zoom_at="w:nah", flip_at="w:Wollfaser", label_at="w:mittleren"), b2_mark="w:IWTO",
        b3="Wichtig: Die Zahl ist eine Obergrenze, kein Messwert. Super 100s heißt: im Mittel höchstens 18,75 Mikrometer. Super 150s heißt: höchstens 16,25. Mit jeder Zehnerstufe wird die Grenze einen halben Mikrometer feiner.",
        b3_head="Eine Obergrenze",
        b3_tags=[("fibre:0", "Super 100s", "höchstens 18,75 µm", "always", "w:100"),
                 ("fibre:1", "Super 150s", "höchstens 16,25 µm", "always", "w:150"),
                 ("scale", "je Stufe 0,5 µm", "feiner", "always", "w:Zehnerstufe")],
        b3_mark="w:Obergrenze",
        b4="Ein Beispiel aus dem US-Recht, der Verordnung zur Wollkennzeichnung: Steht auf dem Etikett Super 100s, die Wolle ist im Mittel aber dicker als 18,75 Mikrometer, dann gilt das Produkt als falsch etikettiert. Feinere Wolle ist dagegen erlaubt, die Grenze gilt nur nach oben.",
        b4_head="Was das US-Recht sagt", b4_l=("über 18,75 µm", "als Super 100s: falsch"), b4_r=("bis 18,75 µm", "als Super 100s: erlaubt"),
        b4_at=dict(left_at="w:Etikett", left_pulse="w:dicker", left_tag_at="w:falsch", right_at="w:Feinere", right_pulse="w:Grenze",
                   right_tag_at="w:erlaubt", mark="w:US"),
        b5="Gemessen wird laut Woolmark am fertigen Produkt, ohne Messtoleranz. Und die Bezeichnung gilt nur für reine Schurwolle, mit höchstens fünf Prozent Ziergarn. Der Branchenverband CCMI sagt es genauso.",
        b5_head="Wo wird gemessen?", b5_label="am fertigen Produkt",
        b5_at=dict(pointer_at="w:Woolmark", zoom_at="w:fertigen", flip_at="w:Produkt", label_at="w:Messtoleranz"),
        b6="Kurz gesagt: Super 100s ist eine Obergrenze für den mittleren Faserdurchmesser. Gemessen am fertigen Produkt, nur bei reiner Schurwolle. Über Gewicht oder Bindung sagt die Zahl nichts.",
        b6_head="Kurz gesagt",
        b6_items=[("Eine Obergrenze", "für den mittleren Faserdurchmesser", "w:Obergrenze", "w:Faserdurchmesser"),
                  ("Nur reine Schurwolle", "gemessen am fertigen Produkt", "w:Gemessen", "w:Produkt"),
                  ("Kein Maß für Gewicht", "und keins für die Bindung", "w:Gewicht", "w:Bindung")],
        b7="Eine Zahl, ein Durchmesser, sonst nichts. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Nur ein Durchmesser.", b7_at=dict(fix_at="w:Zahl", ring_at="w:Durchmesser", statement_at="w:sonst", chip_at="w:Blick"),
        status="Stoff, Super 100s",
        states=["Super 100s: ?", "misst die Faser", "eine Obergrenze", "dicker: falsch", "nur reine Wolle", "nur der Durchmesser", "eine Zahl: klar"],
        desc="Was bedeutet Super 100s auf dem Anzugstoff? Eine Obergrenze für den mittleren Faserdurchmesser: höchstens 18,75 Mikrometer, laut Woolmark-Spezifikation und US-Verordnung. Über Gewicht oder Bindung sagt die Zahl nichts.",
        tags=["herrenmode", "anzugstoff", "wolle", "super100s", "anzug"],
        hooks=[("H1", "question", "Was heißt Super 100s?"), ("H2", "misconception", "Super 100s ist keine Qualitätsnote"),
               ("H3", "surprising_fact", "Super 100s: höchstens 18,75 Mikrometer"), ("H4", "concrete_risk", "Zu dicke Wolle? In den USA falsch etikettiert"),
               ("H5", "demonstration", "Was diese Zahl auf dem Stoff wirklich misst")],
    ),
    "en": dict(
        title="Super 100s: what the number on the cloth means",
        q="What is Super 100s?",
        b1="Super 100s appears on plenty of suit cloth. It sounds like a quality grade. But the number measures exactly one thing. Which one?",
        b1_at=dict(badge_at="w:grade", loupe_at="w:number", nie_at="w:Which"),
        b2="Move in close, right down to a single wool fibre. Super 100s describes the average diameter of those fibres. The system belongs to the IWTO, the international wool body, and Woolmark administers it.",
        b2_head="What is measured?", b2_label="average fibre diameter",
        b2_at=dict(pointer_at="w:Move", zoom_at="w:close", flip_at="w:fibre", label_at="w:average"), b2_mark="w:IWTO",
        b3="The number is an upper limit, not a measurement. Super 100s means an average of 18.75 microns at most. Super 150s means 16.25 at most. Each step of ten makes the limit half a micron finer.",
        b3_head="An upper limit",
        b3_tags=[("fibre:0", "Super 100s", "18.75 µm at most", "always", "w:100"),
                 ("fibre:1", "Super 150s", "16.25 µm at most", "always", "w:150"),
                 ("scale", "0.5 µm per step", "finer", "always", "w:step")],
        b3_mark="w:upper",
        b4="An example from US law, the rules on wool labelling: if a label says Super 100s but the wool averages thicker than 18.75 microns, the product counts as mislabelled. Finer wool is allowed: the limit only caps thickness.",
        b4_head="What US law says", b4_l=("over 18.75 µm", "as Super 100s: mislabelled"), b4_r=("up to 18.75 µm", "as Super 100s: allowed"),
        b4_at=dict(left_at="w:label", left_pulse="w:thicker", left_tag_at="w:mislabelled", right_at="w:Finer", right_pulse="w:limit",
                   right_tag_at="w:allowed", mark="w:US"),
        b5="According to Woolmark, it is measured on the finished product, with no tolerance. And the name applies only to pure new wool, with at most five per cent decorative yarn. The trade body CCMI says the same.",
        b5_head="Where is it measured?", b5_label="on the finished product",
        b5_at=dict(pointer_at="w:Woolmark", zoom_at="w:finished", flip_at="w:product", label_at="w:tolerance"),
        b6="In short: Super 100s is an upper limit for the average fibre diameter. Measured on the finished product, and only for pure new wool. About weight or weave, the number says nothing.",
        b6_head="In short",
        b6_items=[("An upper limit", "for the average fibre diameter", "w:upper", "w:diameter"),
                  ("Pure new wool only", "measured on the finished product", "w:Measured", "w:product"),
                  ("Not weight, not weave", "the number says nothing on that", "w:weight", "w:weave")],
        b7="One number, one diameter, nothing more. For more eye for detail: follow Suitwerk.",
        b7_stmt="Just a diameter.", b7_at=dict(fix_at="w:number", ring_at="w:diameter", statement_at="w:nothing", chip_at="w:eye"),
        status="Cloth, Super 100s",
        states=["Super 100s: ?", "measures the fibre", "an upper limit", "thicker: mislabelled", "pure wool only", "diameter only", "one number: clear"],
        desc="What does Super 100s on suit cloth mean? An upper limit for the average fibre diameter: 18.75 microns at most, per the Woolmark specification and US labelling rules. It says nothing about weight or weave.",
        tags=["menswear", "suitcloth", "wool", "super100s", "suit"],
        hooks=[("H1", "question", "What is Super 100s?"), ("H2", "misconception", "Super 100s is not a quality grade"),
               ("H3", "surprising_fact", "Super 100s: 18.75 microns at most"), ("H4", "concrete_risk", "Wool too thick? Mislabelled under US rules"),
               ("H5", "demonstration", "What this number on the cloth really measures")],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"], "Stoffmuster, Lupe auf der Webstruktur") for h, ty, os in t["hooks"]]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in t["b3_tags"]]
    i1, i2, i3 = t["b6_items"]
    items = [
        {"title": i1[0], "sub": i1[1], "object": FIBRE, "at": i1[2], "ring": "fibre:0", "ring_at": i1[3]},
        {"title": i2[0], "sub": i2[1], "object": YARN, "at": i2[2], "then": CLOTH, "then_at": i2[3]},
        {"title": i3[0], "sub": i3[1], "object": {"kind": "swatch", "weave": "twill"}, "at": i3[2],
         "then": {"weave": "herringbone"}, "then_at": i3[3]},
    ]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 7, "spoken": t["b1"],
         "data": {"question": t["q"], "object": CLOTH, "target": "weave", "badge": "?", "question_at": 0.3, "hold_end": True, **t["b1_at"]},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "object": CLOTH, "from": CLOTH, "to": FIBRE, "target": "center", "zoom": 1.4,
                  "label": t["b2_label"], "strain": False, "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b2_mark"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": LADDER, "at": 0.0, "tags": tags}], "backdrop": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b3_mark"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 14, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": THICK, "tag": t["b4_l"][1],
                           "pulses": [{"target": "fibre:0", "at": a4["left_pulse"], "tone": "red"}]},
                  "right": {"title": t["b4_r"][0], "object": FINE, "tag": t["b4_r"][1],
                            "pulses": [{"target": "fibre:0", "at": a4["right_pulse"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S2"], "overlay": {"marker": "fakt", "marker_at": a4["mark"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "object": YARN, "from": YARN, "to": CLOTH, "target": "center", "zoom": 1.3,
                  "label": t["b5_label"], "strain": False, "backdrop": True, "hold_end": True, **a5},
         "source_ids": ["S1", "S3"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a5["zoom_at"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], THICK, FIBRE, "fibre:0", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "muted", "muted", "red", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema C02 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Werte laut Woolmark-Anhang (Stand 1. Juli 2013). Keine Aussage, eine höhere Zahl sei besser oder empfindlicher.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Die Zahl auf dem Stoff als Frage; Antwort: ein Durchmesser, eine Obergrenze.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["'Über Gewicht oder Bindung sagt die Zahl nichts': Folgerung aus der Definition (nur Faserdurchmesser), nicht wörtlich zitiert.",
                             "Ob höhere Super-Zahlen besser, weicher oder empfindlicher sind: keine Primärquelle geöffnet, nicht im Video.",
                             "Aussprache 'Super 100s' durch die Stimme beim Vertonen prüfen (gemeint: Super Hundert)."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
