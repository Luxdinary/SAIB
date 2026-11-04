"""C04 Flanell, Tweed, Fresko: drei Tuche, drei Bauweisen (14.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261114-3"
GREY, BROWN, NAVY = "#4E5562", "#5A4A38", "#2A3550"
WORSTED = {"kind": "swatch", "weave": "worsted", "colour": GREY, "layers": 2}     # glatt, Webbild sichtbar
FLANNEL = {"kind": "swatch", "weave": "flannel", "colour": GREY, "layers": 2}     # gewalkt und geraut
TWEED = {"kind": "swatch", "weave": "tweed", "colour": BROWN, "layers": 3}
FRESCO = {"kind": "swatch", "weave": "fresco", "colour": NAVY, "layers": 1}
Y_WOOL = {"kind": "yarn", "spin": "woollen"}
Y_WORST = {"kind": "yarn", "spin": "worsted"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://foxflannel.com/pages/heritage",
     "title": "Fox Brothers, Heritage: Flanell als gewalktes Tuch (milled cloth); Fox webt auch Kammgarnflanell aus langen, gekämmten Fasern",
     "checked_at": CHECKED, "label": "Fox, Heritage"},
    {"id": "S2", "url": "https://foxflannel.com/products/fd188-old-english-blue-chalk-stripe",
     "title": "Fox Brothers, FD188 Chalk Stripe: Muster werden durch das sanfte Rauen der Flanellausrüstung sichtbar",
     "checked_at": CHECKED, "label": "Fox, FD188"},
    {"id": "S3", "url": "https://www.harristweed.org/the-process/",
     "title": "Harris Tweed Authority, The Process: nach dem Weben gewaschen, gewalkt und leicht verfilzt, getrocknet und geschoren",
     "checked_at": CHECKED, "label": "Harris Tweed Authority"},
    {"id": "S4", "url": "https://www.hfwltd.com/heritage",
     "title": "Huddersfield Fine Worsteds, Heritage: 1907 erfand und registrierte Martin Sons & Co Fresco, hochgedrehtes Kammgarn in poröser Leinwandbindung",
     "checked_at": CHECKED, "label": "HFW, Heritage"},
    {"id": "S5", "url": "https://www.woolmark.com/globalassets/_06-new-woolmark/_industry/certification/_old-certification/_licensee-portal/learn-about-wool/training-manuals/intro-to-wovenwear.pdf",
     "title": "Woolmark, Introduction to Wovenwear (Schulungshandbuch): Harris Tweed, Donegal und Cheviot zählen zum Streichgarn",
     "checked_at": CHECKED, "label": "Woolmark-Handbuch"},
]

T = {
    "de": dict(
        title="Flanell, Tweed, Fresko: drei Tuche, drei Bauweisen",
        q="Flanell, Tweed, Fresko: Was trennt sie?",
        b1="Flanell, Tweed und Fresko. Drei Wolltuche für Anzug und Sakko, die oft in einem Atemzug fallen. Was macht sie eigentlich so verschieden?",
        hook_at=dict(badge_at="w:Wolltuche", loupe_at="w:Wolltuche", nie_at="w:verschieden"),
        b2="Schon beim Garn trennen sich die Wege. Das Woolmark-Handbuch zählt Tweed zum Streichgarn. Fresko entsteht aus hochgedrehtem Kammgarn. Und Flanell gibt es in beiden Varianten: Fox Brothers webt ihn auch aus langen, gekämmten Fasern.",
        b2_head="Erst das Garn", b2_l=("Streichgarn", "Tweed, laut Woolmark"), b2_r=("Kammgarn", "Fresko, hochgedreht"),
        b2_tag2="Flanell: beides möglich",
        b2_at=dict(left_at="w:Woolmark", pl="w:Streichgarn", left_tag_at="w:Tweed", right_at="w:Fresko", pr="w:Kammgarn",
                   right_tag_at="w:hochgedrehtem", tag2_at="w:Flanell", marker="w:Woolmark"),
        b3="Flanell entsteht erst richtig nach dem Weben. Fox Brothers nennt ihn ein gewalktes Tuch. Danach wird er sanft geraut, daher die weiche Oberfläche. Selbst Kreidestreifen zeigen sich laut Fox erst durch dieses Rauen.",
        b3_head="Flanell: gewalkt, geraut", b3_label="gewalkt und sanft geraut",
        b3_at=dict(pointer_at="w:Weben", zoom_at="w:gewalktes", flip_at="w:geraut", label_at="w:weiche"),
        b3_marker="w:Fox",
        b4="Tweed geht einen ähnlichen Weg, nur kräftiger. Die Harris Tweed Authority beschreibt ihn so: Nach dem Weben wird das Tuch gewaschen, gewalkt und leicht verfilzt. Dann wird es getrocknet und geschoren.",
        b4_head="Tweed: nach dem Weben", b4_stage="Harris Tweed",
        b4_tags=[("weave", "gewaschen", "nach dem Weben", "always", "w:gewaschen"),
                 ("center", "gewalkt", "leicht verfilzt", "always", "w:gewalkt"),
                 ("corner", "geschoren", "nach dem Trocknen", "always", "w:geschoren")],
        b4_focus="w:getrocknet", b4_marker="w:Harris",
        b5="Fresko ist anders gebaut. Laut Huddersfield Fine Worsteds hat Martin Sons and Co es 1907 erfunden und registriert. Das Garn ist hochgedrehtes Kammgarn. Gewebt wird es in einer porösen Leinwandbindung.",
        b5_head="Fresko: hochgedreht", b5_label="porös, aus Kammgarn",
        b5_at=dict(pointer_at="w:Huddersfield", zoom_at="w:1907", flip_at="w:Gewebt", label_at="w:porösen"),
        b5_marker="w:Huddersfield",
        b6="Kurz gesagt: Flanell wird nach dem Weben gewalkt und sanft geraut. Tweed ist ein Streichgarntuch und wird nach dem Weben gewalkt. Fresko ist hochgedrehtes Kammgarn, porös in Leinwandbindung gewebt.",
        b6_head="Kurz gesagt",
        b6_items=[("Flanell: geraut", "gewalkt, dann sanft geraut", "w:Flanell", "w:geraut", None),
                  ("Tweed: Streichgarn", "nach dem Weben gewalkt", "w:Tweed", None, "w:gewalkt#2"),
                  ("Fresko: porös", "hochgedrehtes Kammgarn", "w:Fresko", "w:porös", None)],
        b6_marker="w:gesagt",
        b7="Drei Tuche, drei Bauweisen. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Drei Tuche, drei Wege.", b7_at=dict(fix_at="w:drei", ring_at="w:Bauweisen", statement_at="w:Bauweisen", chip_at="w:Blick"),
        status="Wolltuch, Probe",
        states=["Unterschied: ?", "Garn: zwei Arten", "Flanell: geraut", "Tweed: gewalkt", "Fresko: porös", "drei Bauweisen", "Bauweise erkannt"],
        desc="Flanell, Tweed und Fresko unterscheiden sich vor allem in der Bauweise: Flanell wird gewalkt und geraut (Fox Brothers), Tweed nach dem Weben gewalkt (Harris Tweed Authority), Fresko ist hochgedrehtes Kammgarn in poröser Leinwandbindung (Huddersfield Fine Worsteds).",
        tags=["herrenmode", "anzugstoff", "flanell", "tweed", "fresko"],
        hooks=[("H1", "question", "Flanell, Tweed, Fresko: Was trennt sie?"), ("H2", "misconception", "Flanell ist nur ein Muster? Nein, eine Bauweise."),
               ("H3", "surprising_fact", "Tweed wird erst nach dem Weben gewalkt"), ("H4", "concrete_risk", "Gleich im Regal, verschieden gebaut"),
               ("H5", "demonstration", "Drei Tuchproben unter der Lupe")],
        visual="Tuchprobe Fresko, Lupe auf der porösen Bindung",
    ),
    "en": dict(
        title="Flannel, tweed, fresco: three cloths, three builds",
        q="Flannel, tweed, fresco: what sets them apart?",
        b1="Flannel, tweed and fresco. Three wool cloths that often get mentioned in one breath. So what actually makes them so different?",
        hook_at=dict(badge_at="w:wool", loupe_at="w:wool", nie_at="w:different"),
        b2="The paths split at the yarn. The Woolmark training manual counts tweed as a woollen-spun cloth. Fresco is made from high-twist worsted yarn. And flannel comes both ways: Fox Brothers also weaves it from long, combed fibres.",
        b2_head="It starts with the yarn", b2_l=("Woollen", "tweed, says Woolmark"), b2_r=("Worsted", "fresco, high-twist"),
        b2_tag2="flannel: either one",
        b2_at=dict(left_at="w:Woolmark", pl="w:woollen", left_tag_at="w:tweed", right_at="w:Fresco", pr="w:worsted",
                   right_tag_at="w:high", tag2_at="w:flannel", marker="w:Woolmark"),
        b3="Flannel only really takes shape after weaving. Fox Brothers calls it a milled cloth. Then it is gently raised, which gives it that soft surface. According to Fox, even chalk stripes only show up through this raising.",
        b3_head="Flannel: milled, raised", b3_label="milled and gently raised",
        b3_at=dict(pointer_at="w:weaving", zoom_at="w:milled", flip_at="w:raised", label_at="w:soft"),
        b3_marker="w:Fox",
        b4="Tweed takes a similar route, only more robust. The Harris Tweed Authority describes it like this: after weaving, the cloth is washed, milled and lightly felted. Then it is dried and cropped.",
        b4_head="Tweed: after weaving", b4_stage="Harris Tweed",
        b4_tags=[("weave", "washed", "after weaving", "always", "w:washed"),
                 ("center", "milled", "lightly felted", "always", "w:milled"),
                 ("corner", "cropped", "after drying", "always", "w:cropped")],
        b4_focus="w:dried", b4_marker="w:Harris",
        b5="Fresco is built differently. According to Huddersfield Fine Worsteds, Martin Sons and Co invented and registered it in 1907. The yarn is high-twist worsted. And it is woven in an open, porous plain weave.",
        b5_head="Fresco: high twist", b5_label="porous, from worsted",
        b5_at=dict(pointer_at="w:Huddersfield", zoom_at="w:1907", flip_at="w:woven", label_at="w:porous"),
        b5_marker="w:Huddersfield",
        b6="In short: flannel is milled and gently raised. Tweed is a woollen-spun cloth that gets milled after weaving. Fresco is high-twist worsted, woven porous and open.",
        b6_head="In short",
        b6_items=[("Flannel: raised", "milled, then gently raised", "w:flannel", "w:raised", None),
                  ("Tweed: woollen-spun", "milled after weaving", "w:Tweed", None, "w:milled#2"),
                  ("Fresco: porous", "high-twist worsted", "w:Fresco", "w:porous", None)],
        b6_marker="w:short",
        b7="Three cloths, three ways of building them. For more eye for detail: follow Suitwerk.",
        b7_stmt="Three ways to build.", b7_at=dict(fix_at="w:three", ring_at="w:building", statement_at="w:building", chip_at="w:eye"),
        status="Wool cloth",
        states=["difference: ?", "yarn: two kinds", "flannel: raised", "tweed: milled", "fresco: porous", "three builds", "build understood"],
        desc="Flannel, tweed and fresco differ mostly in how they are made: flannel is milled and raised (Fox Brothers), tweed is milled after weaving (Harris Tweed Authority), fresco is high-twist worsted in a porous plain weave (Huddersfield Fine Worsteds).",
        tags=["menswear", "suitfabric", "flannel", "tweed", "fresco"],
        hooks=[("H1", "question", "Flannel, tweed, fresco: what sets them apart?"), ("H2", "misconception", "Flannel is a pattern? No, it is a way of making cloth."),
               ("H3", "surprising_fact", "Tweed is milled after it is woven"), ("H4", "concrete_risk", "Alike on the rail, built differently"),
               ("H5", "demonstration", "Three swatches under the loupe")],
        visual="Fresco swatch, loupe on the porous weave",
    ),
}


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S3", "S4"] if 1 <= i <= 3 else ["S4"], t["visual"]) for i, (h, ty, os) in enumerate(t["hooks"])]
    a2, a3, a5 = t["b2_at"], t["b3_at"], t["b5_at"]
    tags = [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in t["b4_tags"]]
    objs = [(WORSTED, {"weave": "flannel"}, None), (TWEED, None, "weave"), (Y_WORST, {**FRESCO}, None)]
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
         "data": {"question": t["q"], "object": FRESCO, "target": "weave", "badge": "?", "question_at": 0.3, **t["hook_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 14, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": TWEED, "target": "weave", "tag": t["b2_l"][1],
                           "pulses": [{"target": "center", "at": a2["pl"]}]},
                  "right": {"title": t["b2_r"][0], "object": FRESCO, "target": "weave", "tag": t["b2_r"][1],
                            "pulses": [{"target": "center", "at": a2["pr"]}], "tag2": t["b2_tag2"], "tag2_at": a2["tag2_at"]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S5", "S4", "S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": a2["marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "from": WORSTED, "to": FLANNEL, "target": "weave", "zoom": 1.45, "label": t["b3_label"],
                  "backdrop": True, "hold_end": True, **a3},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_ladder", "duration_hint": 12, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "stages": [{"object": TWEED, "at": 0.0, "title": t["b4_stage"], "tags": tags, "focus_at": t["b4_focus"]}],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S3"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "from": Y_WORST, "to": FRESCO, "target": "center", "zoom": 1.35, "label": t["b5_label"],
                  "backdrop": True, "hold_end": True, **a5},
         "source_ids": ["S4"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S3", "S4", "S5"], "overlay": {"marker": "auslegung", "marker_at": t["b6_marker"]}},
        closing_beat(lang, t["b7"], WORSTED, FLANNEL, "center", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"],
                 notes="Suitwerk Woche 1 (Vorlage 1.0). Thema C04 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S5; Fresco als Markenname nur mit Herkunft (HFW) genannt, keine Empfehlung; Fox-Werbesatz nicht übernommen.",
                 sources=SOURCES, hooks=hooks, hook_note="Frage nach dem Unterschied; die Antwort ist die Bauweise, nicht der Name.",
                 beats=beats, status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Gewichte und Jahreszeiten der Tuche: nicht belegt, nicht im Video.",
                             "'If it's not Fox, it's not flannel' ist Werbung; nicht übernommen."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
