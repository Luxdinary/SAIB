"""C03 Kammgarn oder Streichgarn: der Weg zum Garn (13.11.2026)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261113-1"
SW_W = {"kind": "swatch", "weave": "worsted", "colour": "#2A3550"}
SW_S = {"kind": "swatch", "weave": "woollen", "colour": "#4A5068"}
YARN_W = {"kind": "yarn", "spin": "worsted"}
YARN_S = {"kind": "yarn", "spin": "woollen"}
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://www.woolmark.com/industry/product-development/wool-processing/", "title": "Woolmark, Wool processing: Streichgarn meist aus kürzeren Fasern für dicke, warme Produkte; Kammgarn aus den längsten Fasern für flachere, leichtere, glattere Stoffe; Kämmen entfernt Kurzfasern (Noils) und Pflanzenreste", "checked_at": CHECKED, "label": "Woolmark, Wool processing"},
        {"id": "S2", "url": "https://iwto.org/wp-content/uploads/2024/08/IWTO-Wool-Notes-Final-2024-Digital.pdf", "title": "IWTO Wool Notes 2024: Streichgarn ohne Kämmen, locker gedreht, luftig; Kammgarn gekämmt, eng gedreht, glatt und fest; Kammgarngewebe für Anzüge, Hosen, Röcke, Streichgarngewebe meist Oberbekleidung", "checked_at": CHECKED, "label": "IWTO, Wool Notes 2024"},
        {"id": "S3", "url": "https://iwto.org/wool-supply-chain/first-stage-processing/", "title": "IWTO, First-stage processing: kardierte Fasern meist für Streichgarn, gekämmter Kammzug (Top) für Kammgarn; zu kurze Fasern werden beim Kämmen entfernt", "checked_at": CHECKED, "label": "IWTO, erste Verarbeitung"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Kammgarn oder Streichgarn: der Weg zum Garn",
        q="Kammgarn oder Streichgarn?",
        b1="Kammgarn oder Streichgarn: Beides ist Wolle, und trotzdem fühlen sich die Stoffe ganz anders an. Woher kommt das?",
        b1_at=("w:Wolle", "w:Woher"),
        b2="Leg zwei Stoffe nebeneinander. Kammgarnstoff ist laut Woolmark flacher, leichter und glatter, typisch für die klassische Schneiderei. Streichgarnstoff ist dicker und wärmer, eher für kräftige, warme Stücke.",
        b2_head="Glatt oder füllig?", b2_label="Der Unterschied: das Garn",
        b2_at=dict(pointer_at="w:Leg", zoom_at="w:Kammgarnstoff", flip_at="w:Streichgarnstoff", label_at="w:dicker"), b2_marker="w:Woolmark",
        b3="Der Unterschied entsteht auf dem Weg zum Garn. Streichgarn entsteht meist aus kürzeren Fasern, die nur kardiert und locker gedreht werden. Für Kammgarn nimmt man die längsten Fasern, kämmt sie und dreht sie eng.",
        b3_head="Zwei Wege zum Garn",
        b3_stages=(("Streichgarn", "w:Streichgarn", [("fibre", "kürzere Fasern", "meistens", "always", "w:kürzeren"),
                                                     ("center", "nur kardiert", "locker gedreht", "always", "w:kardiert")]),
                   ("Kammgarn", "w:Kammgarn", [("fibre", "längste Fasern", "dann gekämmt", "always", "w:längsten"),
                                               ("center", "eng gedreht", "glatt und fest", "always", "w:eng")])),
        b3_marker="w:Streichgarn",
        b4="Den entscheidenden Schritt beschreibt der Wollverband IWTO: Beim Kämmen fallen die zu kurzen Fasern heraus, die Kämmlinge, und mit ihnen Pflanzenreste. Übrig bleibt der Kammzug. Aus ihm wird Kammgarn gesponnen.",
        b4_head="Der Kämmschritt", b4_label="Kurzfasern raus: Kammzug",
        b4_at=dict(pointer_at="w:Kämmen", zoom_at="w:kurzen", flip_at="w:Übrig", label_at="w:Kammzug"), b4_marker="w:IWTO",
        b5="Daraus folgt die übliche Verwendung. Laut IWTO wird Kammgarngewebe für Anzüge, Hosen und Röcke genutzt. Streichgarngewebe ist dicker und schwerer, meist für Oberbekleidung. Eine Tendenz, keine Regel: Es gibt zum Beispiel auch Kammgarnflanell.",
        b5_head="Wofür welches?", b5_l=("Kammgarn", "Anzüge, Hosen, Röcke"), b5_r=("Streichgarn", "meist Oberbekleidung"),
        b5_tag2="auch Kammgarnflanell",
        b5_at=dict(left_at="w:Kammgarngewebe", left_tag_at="w:Anzüge", right_at="w:Streichgarngewebe", right_tag_at="w:Oberbekleidung",
                   tag2_at="w:Kammgarnflanell", pulse="w:dicker"), b5_marker="w:IWTO",
        b6="Kurz gesagt: Streichgarn wird nur kardiert und locker gedreht, das macht es füllig und warm. Kammgarn wird zusätzlich gekämmt und eng gedreht, glatt und fest. Im Anzug findest du deshalb meist Kammgarn.",
        b6_head="Kurz gesagt",
        b6_items=[("Streichgarn: kardiert", "locker gedreht, füllig, warm", "w:Streichgarn", "w:locker"),
                  ("Kammgarn: gekämmt", "eng gedreht, glatt und fest", "w:Kammgarn", "w:gekämmt"),
                  ("Anzug: meist Kammgarn", "eine Tendenz, keine Regel", "w:Anzug", "w:meist")],
        b7="Gekämmt wird es glatt, kardiert bleibt es füllig. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Gekämmt wird glatt.", b7_at=dict(fix_at="w:Gekämmt", ring_at="w:glatt", statement_at="w:kardiert", chip_at="w:Blick"),
        status="Zwei Garne",
        states=["Unterschied: ?", "Stoff: glatt, füllig", "kardiert oder gekämmt", "Kämmen: Kurze raus", "Anzug: meist Kammgarn", "kardiert, gekämmt", "gekämmt: glatt"],
        desc="Kammgarn oder Streichgarn? Der Unterschied liegt im Weg zum Garn: kardiert und locker gedreht oder zusätzlich gekämmt und eng gedreht. Nach Woolmark und dem Wollverband IWTO.",
        tags=["herrenmode", "anzugstoff", "kammgarn", "wolle", "stoffkunde"],
        hooks=[("H1", "question", "Kammgarn oder Streichgarn?"), ("H2", "misconception", "Gleiche Wolle, gleicher Stoff? Nicht ganz."),
               ("H3", "surprising_fact", "Ein Schritt trennt Kammgarn von Streichgarn: das Kämmen"), ("H4", "concrete_risk", "Streichgarn im Anzug? Meist dicker und schwerer"),
               ("H5", "demonstration", "Was beim Kämmen aus der Wolle herausfällt")],
    ),
    "en": dict(
        title="Worsted or woollen: two routes to a yarn",
        q="Worsted or woollen?",
        b1="Worsted or woollen: both are wool, and yet the cloths feel completely different. Where does that come from?",
        b1_at=("w:both", "w:Where"),
        b2="Put two cloths side by side. Worsted cloth, says Woolmark, is flatter, lighter and smoother, typical of classic tailoring. Woollen cloth comes out thicker and warmer, more for thick, warm pieces.",
        b2_head="Smooth or full?", b2_label="The difference: the yarn",
        b2_at=dict(pointer_at="w:Put", zoom_at="w:Worsted", flip_at="w:Woollen", label_at="w:thicker"), b2_marker="w:Woolmark",
        b3="The difference lies in the route to the yarn. Woollen yarn is mostly spun from shorter fibres that are only carded and loosely twisted. Worsted takes the longest fibres, combs them, and twists them tightly.",
        b3_head="Two routes to a yarn",
        b3_stages=(("Woollen", "w:Woollen", [("fibre", "shorter fibres", "mostly", "always", "w:shorter"),
                                             ("center", "carded only", "loosely twisted", "always", "w:carded")]),
                   ("Worsted", "w:Worsted", [("fibre", "longest fibres", "then combed", "always", "w:longest"),
                                             ("center", "tightly twisted", "smooth and firm", "always", "w:tightly")])),
        b3_marker="w:Woollen",
        b4="The decisive step, as the wool textile body IWTO describes it: combing removes the fibres that are too short, known as noils, along with plant matter. What is left is the top, and worsted yarn is spun from it.",
        b4_head="The combing step", b4_label="Short fibres out: the top",
        b4_at=dict(pointer_at="w:combing", zoom_at="w:short", flip_at="w:left", label_at="w:top"), b4_marker="w:IWTO",
        b5="That shapes how each one is used. According to IWTO, worsted cloth goes into suits, trousers and skirts, while woollen cloth is thicker and heavier, mostly for outerwear. A tendency, not a rule: worsted flannel exists too.",
        b5_head="Which for what?", b5_l=("Worsted", "suits, trousers, skirts"), b5_r=("Woollen", "mostly outerwear"),
        b5_tag2="also worsted flannel",
        b5_at=dict(left_at="w:worsted", left_tag_at="w:suits", right_at="w:woollen", right_tag_at="w:outerwear",
                   tag2_at="w:flannel", pulse="w:thicker"), b5_marker="w:IWTO",
        b6="In short: woollen yarn is only carded and loosely twisted, which makes it full and warm. Worsted is also combed and tightly twisted, smooth and firm. So in a suit, you will mostly find worsted.",
        b6_head="In short",
        b6_items=[("Woollen: carded", "loosely twisted, full, warm", "w:woollen", "w:loosely"),
                  ("Worsted: combed", "tightly twisted, smooth, firm", "w:Worsted", "w:combed"),
                  ("Suits: mostly worsted", "a tendency, not a rule", "w:suit", "w:mostly")],
        b7="Combed, it turns smooth; carded, it stays full. For more eye for detail: follow Suitwerk.",
        b7_stmt="Combed means smooth.", b7_at=dict(fix_at="w:Combed", ring_at="w:smooth", statement_at="w:carded", chip_at="w:eye"),
        status="Two yarns",
        states=["the difference: ?", "cloth: smooth, full", "carded or combed", "combing: short out", "suits: mostly worsted", "carded, combed", "combed: smooth"],
        desc="Worsted or woollen? The difference lies in the route to the yarn: carded and loosely twisted, or combed as well and tightly twisted. Based on Woolmark and the wool textile body IWTO.",
        tags=["menswear", "suitfabric", "worsted", "wool", "tailoring"],
        hooks=[("H1", "question", "Worsted or woollen?"), ("H2", "misconception", "Worsted here has nothing to do with knitting yarn weight"),
               ("H3", "surprising_fact", "One step separates worsted from woollen: combing"), ("H4", "concrete_risk", "Woollen for a suit? Usually thicker and heavier"),
               ("H5", "demonstration", "What combing takes out of the wool")],
    ),
}


def _tags(rows):
    return [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in rows]


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S1", "S2"], "Kammgarnstoff, Lupe auf der Bindung") for h, ty, os in t["hooks"]]
    objs = [(YARN_S, None, "fibre"), (YARN_S, YARN_W, None), (SW_W, None, "center")]
    items = []
    for (title, sub, at, second), (obj, then, ring) in zip(t["b6_items"], objs):
        it = {"title": title, "sub": sub, "object": obj, "at": at}
        if then:
            it.update({"then": then, "then_at": second})
        if ring:
            it.update({"ring": ring, "ring_at": second})
        items.append(it)
    stages = [{"object": (YARN_S, YARN_W)[k], "at": 0.0 if k == 0 else at, "title": title, "tags": _tags(rows)}
              for k, (title, at, rows) in enumerate(t["b3_stages"])]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": SW_W, "target": "weave", "badge": "?", "question_at": 0.3,
                  "badge_at": t["b1_at"][0], "loupe_at": t["b1_at"][0], "nie_at": t["b1_at"][1], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_fitting", "duration_hint": 11, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "from": SW_W, "to": SW_S, "target": "weave", "zoom": 1.4, "label": t["b2_label"],
                  "backdrop": True, "hold_end": True, **a2},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 751, "y": 879, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b2_marker"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 13, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": stages, "backdrop": True},
         "source_ids": ["S1", "S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b3_marker"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 12, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": YARN_S, "to": YARN_W, "target": "fibre", "zoom": 1.4, "label": t["b4_label"],
                  "hold_end": True, **a4},
         "source_ids": ["S3", "S1"], "overlay": {"vignette": True, "marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "left": {"title": t["b5_l"][0], "object": SW_W, "tag": t["b5_l"][1], "tag2": t["b5_tag2"], "tag2_at": a5["tag2_at"]},
                  "right": {"title": t["b5_r"][0], "object": SW_S, "tag": t["b5_r"][1], "pulses": [{"target": "center", "at": a5["pulse"]}]},
                  "left_at": a5["left_at"], "left_tag_at": a5["left_tag_at"], "right_at": a5["right_at"], "right_tag_at": a5["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S1", "S2"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], SW_S, SW_W, "center", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "muted", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema C03 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Anzug/Mantel als Tendenz, Kammgarnflanell als Ausnahme genannt.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Zwei Begriffe vom Etikett, eine Frage nach dem Unterschied.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["'worsted weight' (Strickgarnstärke) ist nicht gemeint; nur im englischen Hook-Kandidaten H2 erwähnt.",
                             "Keine Aussagen zu Super-Zahlen, Faserfeinheit oder Herkunft der Wolle."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
