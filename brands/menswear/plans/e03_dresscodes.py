"""E03 Smart Casual und Cocktail: dehnbare Dresscodes (14.11.2026, Thema 1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261114-1"
SC = {"kind": "jacket", "variant": "sb2", "fastened": [0], "lapel": "notch", "neck": "open", "strain": False}
SUIT = {**SC, "neck": "tie"}
DJ = {"kind": "jacket", "variant": "sb1", "fastened": [0], "lapel": "peak", "dinner": True, "neck": "bow", "strain": False}
LEGS = {"kind": "legs", "break": "slight", "shoe": "oxford"}
CHECKED = "2026-11-01"
SOURCES = [
    {"id": "S1", "url": "https://debretts.com/deconstructing-dress-codes/", "title": "Debrett's, Deconstructing Dress Codes: Smart Casual ist der häufigste Code, keine Business-Kleidung, ein Sammelbegriff, den man nach Kontext (Stadtabend oder Landpartie) deutet; Cocktail lockert für Herren Dinnerjackett und Fliege zugunsten eines eleganten Anzugs, Samt- oder Nehru-Jacketts; lieber leicht over- als underdressed", "checked_at": CHECKED, "label": "Debrett's, Deconstructing"},
    {"id": "S2", "url": "https://debretts.com/etiquette-category/events-and-dress-codes/", "title": "Debrett's, Events and Dress Codes (Smart Casual): Sakko oder Blazer, Flanell, Cord oder Chino, nicht Jeans, Hemd mit Kragen, keine Turnschuhe oder Sandalen, Krawatte nicht nötig", "checked_at": CHECKED, "label": "Debrett's, Dress Codes"},
    {"id": "S3", "url": "https://suitsupply.com/en-us/journal/cocktail-attire-for-men.html", "title": "Suitsupply (Hersteller), Cocktail attire for men: zwischen Business Casual und Black Tie; am Abend ist ein dunkler einreihiger Anzug in Navy oder Anthrazit die sicherste Wahl; Krawatte für den Abend empfohlen, bei Rooftop-Events verzichtbar", "checked_at": CHECKED, "label": "Suitsupply, Journal"},
]

T = {
    "de": dict(
        title="Smart Casual und Cocktail: dehnbare Dresscodes",
        q="Smart Casual, Cocktail: Was heißt das?",
        b1="Smart Casual oder Cocktail auf der Einladung. Klingt entspannt, ist aber dehnbar. Was ist damit eigentlich gemeint?",
        b1_at=dict(badge_at="w:Cocktail", loupe_at="w:Cocktail", nie_at="w:gemeint"),
        b2="Debrett's, der britische Etikette-Ratgeber, nennt Smart Casual den häufigsten Code. Business-Kleidung ist damit nicht gemeint. Es ist ein Sammelbegriff, den du am Anlass ablesen musst: Ein Abend in der Stadt ist etwas anderes als eine Landpartie.",
        b2_head="Locker oder Business?", b2_l=("Smart Casual", "ein Sammelbegriff", "Stadt oder Land"), b2_r=("Business", "nicht gemeint"),
        b2_at=dict(left_at="w:Debrett", left_tag_at="w:Sammelbegriff", tag2_at="w:Landpartie", right_at="w:Business", right_tag_at="w:nicht", rpulse="w:gemeint"),
        b3="Laut Debrett's heißt Smart Casual: Sakko oder Blazer und ein Hemd mit Kragen, die Krawatte ist nicht nötig. Dazu Flanell, Cord oder Chino, aber keine Jeans. Und keine Turnschuhe oder Sandalen.",
        b3_head="Smart Casual",
        b3_st=[(None, [("lapel", "Sakko oder Blazer", "laut Debrett's", "always", "w:Sakko"),
                       ("neck", "Hemd mit Kragen", "Krawatte nicht nötig", "always", "w:Hemd")]),
               ("Hose, Schuh", [("crease", "Flanell, Cord", "oder Chino", "always", "w:Flanell"),
                                ("break", "keine Jeans", "laut Debrett's", "never", "w:Jeans"),
                                ("shoe", "statt Turnschuh", "keine Sandalen", "always", "w:Turnschuhe")])],
        b3_stage2="w:Dazu",
        b4="Cocktail ist die gelockerte Form von Black Tie. Laut Debrett's weichen Dinnerjackett und Fliege einem eleganten Anzug, auch Samt- oder Nehru-Jacketts gehen. Suitsupply nennt für den Abend den dunklen einreihigen Anzug in Navy oder Anthrazit die sicherste Wahl.",
        b4_head="Und Cocktail?", b4_label="Cocktail: dunkler Anzug",
        b4_at=dict(pointer_at="w:Black", zoom_at="w:Dinnerjackett", flip_at="w:eleganten", label_at="w:dunklen"),
        b4_marker="w:Debrett",
        b5="Und die Krawatte? Laut Suitsupply ist sie für den Abend empfohlen, bei einem Rooftop-Event verzichtbar. Wenn du unsicher bist, rät Debrett's: lieber etwas zu gut als zu leger angezogen.",
        b5_head="Mit oder ohne Krawatte?", b5_l=("Am Abend", "Krawatte empfohlen"), b5_r=("Auf dem Dach", "Krawatte verzichtbar", "im Zweifel: etwas besser"),
        b5_at=dict(left_at="w:Krawatte", left_tag_at="w:empfohlen", right_at="w:Rooftop", right_tag_at="w:verzichtbar", tag2_at="w:lieber", lpulse="w:Abend"),
        b5_marker="w:Suitsupply",
        b6="Kurz gesagt: Smart Casual heißt Sakko und Hemd mit Kragen, ohne Jeans und Turnschuhe. Cocktail heißt am Abend ein dunkler Anzug, die Krawatte je nach Anlass. Und im Zweifel lieber etwas zu gut.",
        b6_head="Kurz gesagt",
        b6_items=[("Smart Casual: Sakko", "Hemd mit Kragen, keine Jeans", "w:Smart", "w:Kragen"),
                  ("Cocktail: dunkler Anzug", "Krawatte je nach Anlass", "w:Cocktail", "w:Anlass"),
                  ("Im Zweifel: etwas besser", "laut Debrett's", "w:Zweifel", "w:gut")],
        b7="Im Zweifel ein Stück besser angezogen. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Lieber etwas zu gut.", b7_at=dict(fix_at="w:besser", ring_at="w:angezogen", statement_at="w:angezogen", chip_at="w:Blick"),
        status="Dresscodes",
        states=["Dresscode: ?", "kein Business", "Sakko, Hemd, Kragen", "Cocktail: dunkler Anzug", "Krawatte: je nachdem", "Sakko, Kragen, Anzug", "lieber etwas zu gut"],
        desc="Smart Casual und Cocktail sind dehnbare Dresscodes. Debrett's (britische Etikette): Sakko, Hemd mit Kragen, keine Jeans, keine Turnschuhe; Cocktail lockert Black Tie zum eleganten Anzug. Suitsupply zur Krawatte am Abend.",
        tags=["herrenmode", "dresscode", "smartcasual", "cocktail", "stilregeln"],
        hooks=[("H1", "question", "Smart Casual, Cocktail: Was heißt das?", []),
               ("H2", "misconception", "Smart Casual heißt nicht Jeans und Turnschuhe", ["S2"]),
               ("H3", "surprising_fact", "Cocktail erlaubt laut Debrett's sogar Samtjacketts", ["S1"]),
               ("H4", "concrete_risk", "Zu leger? Debrett's: lieber etwas zu gut angezogen.", ["S1"]),
               ("H5", "demonstration", "Vom Smoking zum Anzug: So lockert Cocktail", [])],
    ),
    "en": dict(
        title="Smart casual and cocktail: the stretchy dress codes",
        q="Smart casual, cocktail: what's meant?",
        b1="Smart casual or cocktail on the invitation. Sounds relaxed, but both codes stretch. So what do they actually mean?",
        b1_at=dict(badge_at="w:cocktail", loupe_at="w:cocktail", nie_at="w:mean"),
        b2="Debrett's, the British etiquette guide, calls smart casual the most common code. It does not mean business wear. It is a catch-all you read from the occasion: an evening in town differs from a day in the country.",
        b2_head="Relaxed or business?", b2_l=("Smart casual", "a catch-all", "town or country"), b2_r=("Business", "not what is meant"),
        b2_at=dict(left_at="w:Debrett", left_tag_at="w:catch", tag2_at="w:country", right_at="w:business", right_tag_at="w:wear", rpulse="w:wear"),
        b3="For smart casual, Debrett's spells it out: a jacket or blazer and a collared shirt, no tie needed. Then flannel, cords or chinos, but not jeans. And no trainers or sandals.",
        b3_head="Smart casual",
        b3_st=[(None, [("lapel", "jacket or blazer", "says Debrett's", "always", "w:jacket"),
                       ("neck", "collared shirt", "no tie needed", "always", "w:collared")]),
               ("Trousers, shoes", [("crease", "flannel, cords", "or chinos", "always", "w:flannel"),
                                    ("break", "no jeans", "says Debrett's", "never", "w:jeans"),
                                    ("shoe", "proper shoes", "no trainers or sandals", "always", "w:trainers")])],
        b3_stage2="w:Then",
        b4="Cocktail loosens black tie. According to Debrett's, the dinner jacket and bow tie give way to an elegant suit, and velvet or Nehru jackets work too. Suitsupply calls a dark single-breasted suit in navy or charcoal the safest evening choice.",
        b4_head="And cocktail?", b4_label="Cocktail: a dark suit",
        b4_at=dict(pointer_at="w:black", zoom_at="w:dinner", flip_at="w:elegant", label_at="w:dark"),
        b4_marker="w:Debrett",
        b5="And the tie? Suitsupply recommends one for the evening, but at a rooftop event you can skip it. If you are unsure, Debrett's advice: better slightly overdressed than underdressed.",
        b5_head="Tie or no tie?", b5_l=("In the evening", "tie recommended"), b5_r=("On a rooftop", "tie optional", "when unsure: a bit more"),
        b5_at=dict(left_at="w:tie", left_tag_at="w:recommends", right_at="w:rooftop", right_tag_at="w:skip", tag2_at="w:better", lpulse="w:evening"),
        b5_marker="w:Suitsupply",
        b6="In short: smart casual means a jacket and a collared shirt, no jeans, no trainers. Cocktail in the evening means a dark suit, the tie depending on the event. And when in doubt, dress slightly up.",
        b6_head="In short",
        b6_items=[("Smart casual: a jacket", "collared shirt, no jeans", "w:smart", "w:collared"),
                  ("Cocktail: a dark suit", "tie depending on the event", "w:Cocktail", "w:event"),
                  ("In doubt: a bit more", "says Debrett's", "w:doubt", "w:up")],
        b7="When in doubt, a little better dressed. For more eye for detail: follow Suitwerk.",
        b7_stmt="Slightly overdressed.", b7_at=dict(fix_at="w:better", ring_at="w:dressed", statement_at="w:dressed", chip_at="w:eye"),
        status="Dress codes",
        states=["dress code: ?", "not business", "jacket and collar", "cocktail: dark suit", "tie: it depends", "jacket, collar, suit", "a little dressier"],
        desc="Smart casual and cocktail are stretchy dress codes. Debrett's (British etiquette): a jacket, a collared shirt, no jeans, no trainers; cocktail loosens black tie to an elegant suit. Plus Suitsupply on the evening tie.",
        tags=["menswear", "dresscode", "smartcasual", "cocktailattire", "styletips"],
        hooks=[("H1", "question", "Smart casual, cocktail: what's meant?", []),
               ("H2", "misconception", "Smart casual does not mean jeans and trainers", ["S2"]),
               ("H3", "surprising_fact", "Cocktail even allows velvet jackets, says Debrett's", ["S1"]),
               ("H4", "concrete_risk", "Too relaxed? Debrett's: better slightly overdressed.", ["S1"]),
               ("H5", "demonstration", "From dinner suit to suit: how cocktail loosens up", [])],
    ),
}


def _stages(spec, objs, second):
    out = []
    for k, ((title, tags), obj) in enumerate(zip(spec, objs)):
        st = {"object": obj, "at": 0.0 if k == 0 else second,
              "tags": [{"spot": sp, "text": tx, "sub": sub, "tone": tone, "at": at} for sp, tx, sub, tone, at in tags]}
        if title:
            st["title"] = title
        out.append(st)
    return out


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, src, "Sakko mit offenem Kragen, Lupe auf dem Hemdkragen") for h, ty, os, src in t["hooks"]]
    a2, a4, a5 = t["b2_at"], t["b4_at"], t["b5_at"]
    objs = [(SC, None, "neck"), (SUIT, {"neck": "open"}, None), (SC, {"neck": "tie"}, None)]
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
         "data": {"question": t["q"], "object": SC, "target": "neck", "badge": "?", "question_at": 0.3, **t["b1_at"], "hold_end": True},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b2"],
         "data": {"headline": t["b2_head"],
                  "left": {"title": t["b2_l"][0], "object": SC, "target": "neck", "tag": t["b2_l"][1], "tag2": t["b2_l"][2], "tag2_at": a2["tag2_at"]},
                  "right": {"title": t["b2_r"][0], "object": SUIT, "tag": t["b2_r"][1],
                            "pulses": [{"target": "neck", "at": a2["rpulse"], "tone": "red"}]},
                  "left_at": a2["left_at"], "left_tag_at": a2["left_tag_at"], "right_at": a2["right_at"], "right_tag_at": a2["right_tag_at"],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_ladder", "duration_hint": 11, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "stages": _stages(t["b3_st"], (SC, LEGS), t["b3_stage2"]), "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": "w:Debrett"}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_fitting", "duration_hint": 14, "spoken": t["b4"],
         "data": {"headline": t["b4_head"], "from": DJ, "to": SUIT, "target": "neck", "zoom": 1.4, "label": t["b4_label"],
                  "backdrop": True, "hold_end": True, **a4},
         "source_ids": ["S1", "S3"],
         "overlay": {"transition": {"type": "iris", "x": 300, "y": 760, "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": t["b4_marker"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_compare", "duration_hint": 11, "spoken": t["b5"],
         "data": {"headline": t["b5_head"],
                  "left": {"title": t["b5_l"][0], "object": SUIT, "target": "neck", "tag": t["b5_l"][1],
                           "pulses": [{"target": "neck", "at": a5["lpulse"]}]},
                  "right": {"title": t["b5_r"][0], "object": SC, "target": "neck", "tag": t["b5_r"][1], "tag2": t["b5_r"][2], "tag2_at": a5["tag2_at"]},
                  "left_at": a5["left_at"], "left_tag_at": a5["left_tag_at"], "right_at": a5["right_at"], "right_tag_at": a5["right_tag_at"],
                  "backdrop": True},
         "source_ids": ["S3", "S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": t["b5_marker"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 11, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S2", "S3", "S1"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], SC, SUIT, "neck", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "amber", "muted", "muted", "amber", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema E03 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Debrett's als britische Instanz benannt, Lounge Suit nur als Abgrenzung (Business), Suitsupply nur als Quelle.",
                 sources=SOURCES, hooks=hooks, hook_note="Die zwei dehnbaren Begriffe als Frage, die Lupe auf dem offenen Kragen.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["In Deutschland und Österreich werden die Begriffe teils anders benutzt (Hinweis aus der Recherche): im Video nur über 'britisch' angedeutet.",
                             "Samt- und Nehru-Jacketts (S1): nur gesprochen, keine eigene Zeichnung.",
                             "Turnschuhe: keine Zeichnung; das rote Etikett steht am gezeichneten Schnürschuh.",
                             "Stoffe (Flanell, Cord, Chino) und Farben (Navy, Anthrazit): nur gesprochen."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
