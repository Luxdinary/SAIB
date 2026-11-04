"""C01 Stoffgewicht: Was die Zahl wirklich misst (10.11.2026, Thema 1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261110-1"
NAVY = {"kind": "swatch", "weave": "twill", "colour": "#2A3550", "layers": 2}
TARTAN = {"kind": "swatch", "weave": "twill", "colour": "#2E4A3A", "layers": 2}
LIGHT = {"kind": "swatch", "weave": "worsted", "colour": "#2A3550", "layers": 1}
FLANNEL = {"kind": "swatch", "weave": "flannel", "colour": "#555B66", "layers": 4}
FLANNEL3 = {"kind": "swatch", "weave": "flannel", "colour": "#555B66", "layers": 3, "strain": False}
HERRING3 = {"kind": "swatch", "weave": "herringbone", "colour": "#555B66", "layers": 3, "strain": False}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://foxflannel.com/pages/cloth-weight-explained", "title": "Fox Brothers, Cloth weight explained: Gramm je laufendem Meter bei fester Webbreite nach dem Ausrüsten, teils mit Unzen; 230-260 g (Golden Fox) bis 530-560 g (Authentic Flannel); schwerer nicht automatisch wärmer, Bindung und Ausrüstung zählen mit", "checked_at": CHECKED, "label": "Fox Brothers, Cloth Weight"},
    {"id": "S2", "url": "https://www.lochcarron.co.uk/edinburgh-heavy-weight-tartan-fabric", "title": "Lochcarron, Edinburgh Heavy Weight Tartan: 490/500 g je laufendem Meter und 16 oz je laufendem Yard bei 140 cm Breite", "checked_at": CHECKED, "label": "Lochcarron, Tartan"},
    {"id": "S3", "url": "https://www.woolmark.com/globalassets/_06-new-woolmark/_industry/certification/_old-certification/_licensee-portal/learn-about-wool/training-manuals/intro-to-wovenwear.pdf", "title": "Woolmark, Intro to Wovenwear (Schulungshandbuch): Stoffgewichte etwa 100 bis 700 g je laufendem Meter, typisch für Herren-Kammgarn 350 g", "checked_at": CHECKED, "label": "Woolmark, Wovenwear"},
]

T = {
    "de": dict(
        title="Stoffgewicht: Was die Zahl wirklich misst",
        q="350 Gramm, aber wovon?",
        b1="Auf dem Stoffmuster steht 350 Gramm. Aber 350 Gramm wovon? Und sagt dir die Zahl, wie warm der Anzug wird?",
        b1_at=dict(badge_at="w:350", loupe_at="w:350", nie_at="w:wovon"),
        b2="Zu vielen Anzugstoffen gibt es eine Gewichtszahl. Aber in welcher Einheit? Die Weberei Lochcarron nennt für einen Tartan beides nebeneinander: rund 500 Gramm je laufendem Meter und 16 Unzen je laufendem Yard, bei 140 Zentimetern Breite.",
        b2_head="Gramm oder Unzen?", b2_l=("Gramm", "rund 500 g je Meter"), b2_r=("Unzen", "16 oz je Yard"), b2_tag2="Umrechnung je nach Breite",
        b2_at=dict(left_at=0.4, left_tag_at="w:Gramm", marker="w:Lochcarron", right_at="w:16", right_tag_at="w:Yard", tag2_at="w:Breite", lpulse="w:Meter", rpulse="w:Zentimetern"),
        b3="Fox Brothers erklärt, was gemeint ist: das Gewicht eines laufenden Meters Stoff, bei fester Webbreite, gewogen nach dem Ausrüsten. Teils steht der Wert in Unzen daneben. Gemeint ist bei Fox also nicht der Quadratmeter.",
        b3_head="Was gewogen wird", b3_stage="Fox Brothers",
        b3_tags=[("weave", "1 laufender Meter", "Gramm je Meter", "w:laufenden"),
                 ("center", "feste Webbreite", "laut Fox Brothers", "w:Webbreite"),
                 ("corner", "nach Ausrüstung", "der fertige Stoff", "w:Ausrüsten")],
        b3_focus="w:Quadratmeter",
        b4="Wie weit das reicht, zeigt Fox Brothers selbst: von 230 bis 260 Gramm beim leichten Golden Fox bis zu 530 bis 560 Gramm beim Authentic Flannel. Woolmark nennt 350 Gramm als typisch für Kammgarn im Herrenanzug.",
        b4_head="Leicht bis schwer", b4_l=("Golden Fox", "230–260 g je Meter"), b4_r=("Authentic Flannel", "530–560 g je Meter"),
        b4_at=dict(left_at="w:von", left_tag_at="w:Golden", right_at="w:530", right_tag_at="w:Authentic", lpulse="w:Woolmark", rpulse="w:Kammgarn"),
        b5="Und schwerer heißt nicht automatisch wärmer. Laut Fox Brothers zählen Bindung und Ausrüstung mit. Die Zahl gibt dir also eine erste Richtung für die Saison, mehr nicht.",
        b5_head="Schwerer gleich wärmer?", b5_label="Bindung und Ausrüstung zählen",
        b5_at=dict(pointer_at="w:schwerer", error_at="w:automatisch", zoom_at="w:wärmer", flip_at="w:Bindung", label_at="w:Ausrüstung"),
        b6="Kurz gesagt: Die Zahl meint bei Webereien meist Gramm je laufendem Meter, bei fester Breite. Unzen stehen teils daneben. Und für die Wärme zählen auch Bindung und Ausrüstung.",
        b6_head="Kurz gesagt",
        b6_items=[("Gramm je Meter", "laufend, feste Breite (Fox)", "w:Gramm", "w:Breite"),
                  ("Unzen teils daneben", "je Yard, etwa bei Lochcarron", "w:Unzen", "w:daneben"),
                  ("Bindung zählt mit", "und die Ausrüstung", "w:Wärme", "w:Bindung")],
        b7="Die Zahl zeigt die Richtung, den Rest machen Bindung und Ausrüstung. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Eine erste Richtung.", b7_at=dict(fix_at="w:Richtung", ring_at="w:Bindung", statement_at="w:Ausrüstung", chip_at="w:Blick"),
        status="Stoff, Gewicht",
        states=["Gewicht: ?", "Gramm oder Unzen?", "Gramm je lfd. Meter", "230 bis 560 g", "schwerer, nicht wärmer", "Zahl plus Bindung", "erste Richtung"],
        desc="Was misst das Stoffgewicht? Bei Fox Brothers Gramm je laufendem Meter bei fester Breite, nach dem Ausrüsten. Dazu Lochcarron mit Gramm und Unzen und Woolmark mit typischen Werten.",
        tags=["herrenmode", "anzugstoff", "stoffkunde", "anzug", "wolle"],
        hooks=[("H1", "question", "350 Gramm, aber wovon?", []),
               ("H2", "misconception", "Schwerer Stoff, wärmerer Anzug? Nicht automatisch.", ["S1"]),
               ("H3", "surprising_fact", "Das Stoffgewicht meint meist einen laufenden Meter", ["S1", "S2"]),
               ("H4", "concrete_risk", "Gramm oder Unzen? Ohne Einheit sagt die Zahl wenig.", ["S2", "S3"]),
               ("H5", "demonstration", "Was ein Meter Stoff auf der Waage verrät", [])],
    ),
    "en": dict(
        title="Cloth weight: what the number actually measures",
        q="350 grams, but of what?",
        b1="The swatch says 350 grams. But 350 grams of what? And does that number tell you how warm the suit will be?",
        b1_at=dict(badge_at="w:350", loupe_at="w:350", nie_at="w:what"),
        b2="Many cloths come with a weight figure, but in which unit? The mill Lochcarron lists both side by side for one tartan: around 500 grams per running metre and 16 ounces per running yard, at a width of 140 centimetres.",
        b2_head="Grams or ounces?", b2_l=("Grams", "about 500 g per metre"), b2_r=("Ounces", "16 oz per yard"), b2_tag2="conversion depends on width",
        b2_at=dict(left_at=0.4, left_tag_at="w:grams", marker="w:Lochcarron", right_at="w:16", right_tag_at="w:yard", tag2_at="w:width", lpulse="w:metre", rpulse="w:centimetres"),
        b3="Fox Brothers explains what is meant: the weight of one running metre of cloth, at a fixed loom width, weighed after finishing. Some listings add ounces alongside. So at Fox, the figure is not per square metre.",
        b3_head="What gets weighed", b3_stage="Fox Brothers",
        b3_tags=[("weave", "1 running metre", "grams per metre", "w:running"),
                 ("center", "fixed loom width", "says Fox Brothers", "w:width"),
                 ("corner", "after finishing", "the finished cloth", "w:finishing")],
        b3_focus="w:square",
        b4="Fox Brothers shows the range: from 230 to 260 grams for the light Golden Fox, up to 530 to 560 grams for Authentic Flannel. Woolmark gives 350 grams as typical for a men's worsted suit cloth.",
        b4_head="Light to heavy", b4_l=("Golden Fox", "230–260 g per metre"), b4_r=("Authentic Flannel", "530–560 g per metre"),
        b4_at=dict(left_at="w:from", left_tag_at="w:Golden", right_at="w:530", right_tag_at="w:Authentic", lpulse="w:Woolmark", rpulse="w:worsted"),
        b5="And heavier does not automatically mean warmer. According to Fox Brothers, weave and finishing count too. So the number gives you a first direction for the season, nothing more.",
        b5_head="Heavier means warmer?", b5_label="Weave and finishing count",
        b5_at=dict(pointer_at="w:heavier", error_at="w:automatically", zoom_at="w:warmer", flip_at="w:weave", label_at="w:finishing"),
        b6="In short: mills usually mean grams per running metre, at a fixed width. Ounces sometimes sit alongside. And for warmth, weave and finishing count too.",
        b6_head="In short",
        b6_items=[("Grams per metre", "running metre, fixed width (Fox)", "w:grams", "w:width"),
                  ("Ounces alongside", "per yard, e.g. at Lochcarron", "w:Ounces", "w:alongside"),
                  ("Weave counts too", "and so does finishing", "w:warmth", "w:weave")],
        b7="The number shows the direction, weave and finishing do the rest. For more eye for detail: follow Suitwerk.",
        b7_stmt="A first direction.", b7_at=dict(fix_at="w:direction", ring_at="w:weave", statement_at="w:finishing", chip_at="w:eye"),
        status="Cloth, weight",
        states=["weight: ?", "grams or ounces?", "grams per metre", "230 to 560 g", "heavier, not warmer", "number plus weave", "a first direction"],
        desc="What does cloth weight measure? At Fox Brothers, grams per running metre at a fixed width, after finishing. Plus Lochcarron with grams and ounces, and Woolmark with typical values.",
        tags=["menswear", "suitcloth", "fabric", "suit", "wool"],
        hooks=[("H1", "question", "350 grams, but of what?", []),
               ("H2", "misconception", "Heavier cloth, warmer suit? Not automatically.", ["S1"]),
               ("H3", "surprising_fact", "Cloth weight usually means one running metre", ["S1", "S2"]),
               ("H4", "concrete_risk", "Grams or ounces? Without the unit, the number says little.", ["S2", "S3"]),
               ("H5", "demonstration", "What one metre of cloth on the scales tells you", [])],
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Stoffmuster, Lupe auf der umgeschlagenen Ecke") for h, ty, os, src in t["hooks"]]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": "always", "at": at} for sp, tx, sub, at in t["b3_tags"]]
    objs = [(NAVY, None, "measure"), (TARTAN, None, "corner"), (FLANNEL3, {"weave": "herringbone"}, None)]
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
         "data": {"question": t["q"], "object": NAVY, "target": "corner", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": TARTAN, "target": "measure", "tag": t["b2_l"][1], "pulses": [{"target": "center", "at": a2["lpulse"]}]},
                  "right": {"title": t["b2_r"][0], "object": TARTAN, "tag": t["b2_r"][1], "tag2": t["b2_tag2"], "tag2_at": a2["tag2_at"],
                            "pulses": [{"target": "measure", "at": a2["rpulse"], "tone": "amber"}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": a2["marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": [{"object": NAVY, "at": 0.0, "title": t["b3_stage"], "tags": tags, "focus_at": t["b3_focus"]}],
                  "backdrop": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Fox"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": LIGHT, "target": "measure", "tag": t["b4_l"][1], "pulses": [{"target": "center", "at": a4["lpulse"]}]},
                  "right": {"title": t["b4_r"][0], "object": FLANNEL, "tag": t["b4_r"][1], "pulses": [{"target": "measure", "at": a4["rpulse"]}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "hold_end": True},
         "source_ids": ["S1", "S3"], "overlay": {"marker": "fakt", "marker_at": a4["left_tag_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_fitting", "duration_hint": 10, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "from": FLANNEL3, "to": HERRING3, "target": "weave", "zoom": 1.4, "label": t["b5_label"],
                  "backdrop": True, "hold_end": True, **a5},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 738, "y": 860, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a5["flip_at"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 10, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], {**FLANNEL3, "layers": 1}, HERRING3, "weave", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "red", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema C01 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; keine Unzen je Quadratyard, keine feste Sommer-Grenze, Lochcarron-Wert gerundet (490/500 g).",
                 sources=SOURCES, hooks=hooks, hook_note="Eine konkrete Zahl als Frage, die Lupe auf dem Stoff.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Umrechnung Gramm/Unzen: hängt von der Breite ab, keine Formel im Video.",
                             "Bindung der Golden-Fox-Stoffe: nicht belegt; das Muster im Bild ist neutral gewählt."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
