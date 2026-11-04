"""D02 Schulter: die Schulter muss zuerst passen (11.11.2026, menswear-20261111-1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build, closing_beat, hook, write  # noqa: E402

TID = "menswear-20261111-1"
JK = {"kind": "jacket", "variant": "sb2", "fastened": [0]}
SHIRT = {"kind": "torso", "hold": "none", "tie_tip": 520}
CHECKED = "2026-11-01"
SOURCES = {
    "de": [
        {"id": "S1", "url": "https://suitsupply.com/en-us/journal/how-it-should-fit-jacket.html", "title": "Suitsupply, How it should fit: Schulternaht auf der natürlichen Schulterlinie ohne Überstand; zu weit rutscht die Naht ab, zu eng gibt Spannung, Falten, wenig Bewegung", "checked_at": CHECKED, "label": "Suitsupply, Jacket Fit"},
        {"id": "S2", "url": "https://tmlewin.co.uk/blogs/the-fitting-room/how-a-suit-should-fit", "title": "T.M. Lewin, How a suit should fit: Schultern am schwersten und deshalb am teuersten zu ändern, zuerst nach den Schultern wählen", "checked_at": CHECKED, "label": "T.M. Lewin, Fitting Room"},
        {"id": "S3", "url": "https://propercloth.com/reference/how-much-can-alter-a-jacket-how-much-can-a-tailor-do/", "title": "Proper Cloth, How much can a tailor alter a jacket: Schulterbreite ändern nicht empfohlen, besser andere Grundgröße oder Neuanfertigung", "checked_at": CHECKED, "label": "Proper Cloth, Reference"},
    ],
}
SOURCES["en"] = SOURCES["de"]

T = {
    "de": dict(
        title="Sakko: Warum die Schulter zuerst passen muss",
        q="Was prüfst du zuerst?",
        b1="Du probierst ein Sakko an. Worauf achtest du zuerst? Nicht auf die Ärmel, nicht auf die Länge. Zuerst auf die Schulter.",
        b1_at=dict(badge_at="w:Worauf", loupe_at="w:zuerst", nie_at="w:zuerst#2", cut_at="w:Länge"),
        b2="Der Grund steht beim britischen Herrenausstatter T.M. Lewin: Von allen Stellen am Sakko ist die Schulter am schwersten zu ändern. Und deshalb ist sie auch am teuersten.",
        b2_head="Die schwierigste Stelle", b2_stage="Die Schulter",
        b2_tags=[("am schwersten", "zu ändern", "never", "w:schwersten"),
                 ("am teuersten", "deshalb", "never", "w:teuersten")],
        b2_mark="w:tm", b2_focus="w:deshalb",
        b3="Wo genau gehört die Naht hin? Suitsupply beschreibt es so: Die Schulternaht sitzt auf deiner natürlichen Schulterlinie, ohne Überstand. Zieh das Sakko in Gedanken aus: Wo deine Schulter endet, gehört die Naht hin.",
        b3_head="Wo sitzt die Naht?", b3_label="Naht auf der Schulterlinie",
        b3_at=dict(pointer_at="w:Naht", zoom_at="w:Suitsupply", flip_at="w:Zieh", label_at="w:endet"),
        b4="Sieh dir zwei Fehler an. Links ist die Schulter zu weit: Die Naht rutscht über die Schulter hinaus nach unten. Rechts ist sie zu eng: Der Stoff spannt, es entstehen Falten, und du bewegst dich schwerer.",
        b4_head="Zu weit oder zu eng?", b4_l=("Zu weit", "Naht rutscht nach unten"), b4_r=("Zu eng", "spannt, wirft Falten"),
        b4_at=dict(left_at="w:Links", left_pulse="w:Naht", left_tag_at="w:rutscht", right_at="w:Rechts", right_pulse="w:Stoff",
                   right_tag_at="w:spannt", sleeve_pulse="w:bewegst"),
        b5="Und wenn die Schulter nicht passt? Proper Cloth, ein Hersteller von Maßkleidung, rät davon ab, die Schulterbreite ändern zu lassen. Besser ist eine andere Grundgröße oder eine Neuanfertigung.",
        b5_head="Ändern lassen?", b5_s1="Passt sie nicht?", b5_s2="Besser:",
        b5_t1=[("nicht ändern", "rät Proper Cloth", "never", "w:rät")],
        b5_t2=[("andere Größe", "neue Grundgröße", "always", "w:andere"), ("Neuanfertigung", "nach Maß", "always", "w:oder")],
        b5_at=dict(s2="w:Besser", mark="w:Proper"),
        b6="Kurz gesagt: Prüf beim Anprobieren zuerst die Schulter. Die Naht liegt auf deiner Schulterlinie, ohne Überstand und ohne Spannung. Passt sie nicht, nimm eine andere Größe statt einer Änderung.",
        b6_head="Kurz gesagt",
        b6_items=[("Zuerst: die Schulter", "beim Anprobieren", "w:Prüf", "w:Schulter"),
                  ("Naht auf der Schulterlinie", "ohne Überstand, ohne Spannung", "w:Naht", "w:liegt", "w:Überstand"),
                  ("Passt nicht: tauschen", "andere Größe statt Änderung", "w:Passt", "w:Größe")],
        b7="Erst die Schulter, dann der Rest. Mehr Blick fürs Detail: Folge Suitwerk.",
        b7_stmt="Erst die Schulter.", b7_at=dict(fix_at="w:Erst", ring_at="w:Schulter", statement_at="w:dann", chip_at="w:Blick"),
        status="Sakko, Anprobe",
        states=["Schulter: ?", "schwer zu ändern", "Naht: Schulterlinie", "zu weit, zu eng", "sonst: andere Größe", "Schulter zuerst", "Schulter: passt"],
        desc="Warum prüfst du beim Sakko zuerst die Schulter? Sie ist laut T.M. Lewin am schwersten zu ändern. Wo die Naht sitzt (Suitsupply) und was tun, wenn sie nicht passt (Proper Cloth).",
        tags=["herrenmode", "sakko", "passform", "anprobe", "anzug"],
        hooks=[("H1", "question", "Was prüfst du zuerst?"), ("H2", "misconception", "Erst Länge und Ärmel? Erst die Schulter."),
               ("H3", "surprising_fact", "Die teuerste Änderung am Sakko"), ("H4", "concrete_risk", "Die Schulter ist am schwersten zu ändern"),
               ("H5", "demonstration", "Hier entscheidet sich die Größe")],
    ),
    "en": dict(
        title="Jacket fit: why the shoulders come first",
        q="What do you check first?",
        b1="You try on a jacket. What do you check first? Not the sleeves, not the length. First of all, the shoulders.",
        b1_at=dict(badge_at="w:What", loupe_at="w:first", nie_at="w:first#2", cut_at="w:length"),
        b2="The reason comes from the British outfitter T.M. Lewin: of every part of a jacket, the shoulders are the hardest to alter. And that makes them the most expensive to alter, too.",
        b2_head="The hardest part", b2_stage="The shoulders",
        b2_tags=[("hardest", "to alter", "never", "w:hardest"),
                 ("costliest", "and so", "never", "w:expensive")],
        b2_mark="w:tm", b2_focus="w:And",
        b3="So where should the seam sit? Suitsupply puts it simply: the shoulder seam sits on your natural shoulder line, with nothing hanging over. Picture the jacket off: where your shoulder ends, that is where the seam belongs.",
        b3_head="Where does the seam sit?", b3_label="Seam on the shoulder line",
        b3_at=dict(pointer_at="w:seam", zoom_at="w:Suitsupply", flip_at="w:Picture", label_at="w:ends"),
        b4="Now look at two faults. On the left, the shoulders are too wide: the seam slips down past your shoulder. On the right, they are too narrow: the cloth pulls, creases appear, and you move less freely.",
        b4_head="Too wide or too narrow?", b4_l=("Too wide", "the seam slips down"), b4_r=("Too narrow", "pulls and creases"),
        b4_at=dict(left_at="w:left", left_pulse="w:seam", left_tag_at="w:slips", right_at="w:right", right_pulse="w:cloth",
                   right_tag_at="w:pulls", sleeve_pulse="w:move"),
        b5="And if the shoulders don't fit? Proper Cloth, a made-to-measure clothier, advises against having a tailor change the shoulder width. Better to go for a different base size, or have one made from scratch.",
        b5_head="Have it altered?", b5_s1="Doesn't fit?", b5_s2="Better:",
        b5_t1=[("don't alter", "says Proper Cloth", "never", "w:advises")],
        b5_t2=[("another size", "new base size", "always", "w:different"), ("made new", "made to measure", "always", "w:have")],
        b5_at=dict(s2="w:Better", mark="w:Proper"),
        b6="In short: when you try on a jacket, check the shoulders first. The seam sits on your shoulder line, with no overhang and no pull. If they don't fit, choose another size instead of an alteration.",
        b6_head="In short",
        b6_items=[("First: the shoulders", "when you try a jacket on", "w:check", "w:first"),
                  ("Seam on the shoulder line", "no overhang, no pull", "w:seam", "w:sits", "w:overhang"),
                  ("No fit: change size", "another size, not an alteration", "w:If", "w:size")],
        b7="Shoulders first, then everything else. For more eye for detail: follow Suitwerk.",
        b7_stmt="Shoulders first.", b7_at=dict(fix_at="w:Shoulders", ring_at="w:first", statement_at="w:then", chip_at="w:eye"),
        status="Jacket, fitting",
        states=["shoulders: ?", "hard to alter", "seam: shoulder line", "too wide, too narrow", "else: another size", "shoulders first", "shoulders: fit"],
        desc="Why check the shoulders first when you try on a jacket? T.M. Lewin calls them the hardest part to alter. Where the seam sits (Suitsupply) and what to do if it doesn't fit (Proper Cloth).",
        tags=["menswear", "jacket", "suitfit", "tailoring", "suit"],
        hooks=[("H1", "question", "What do you check first?"), ("H2", "misconception", "Length and sleeves first? Shoulders first."),
               ("H3", "surprising_fact", "The most expensive alteration on a jacket"), ("H4", "concrete_risk", "Shoulders are the hardest part to alter"),
               ("H5", "demonstration", "This is where your size is decided")],
    ),
}


def _tags(rows, spot="shoulder"):
    return [{"spot": spot, "text": tx, "sub": sub, "tone": tone, "at": at} for tx, sub, tone, at in rows]


def make(lang: str) -> dict:
    t = T[lang]
    hooks = [hook(h, ty, os, os, ["S2", "S1"], "Sakko, Lupe auf der Schulter") for h, ty, os in t["hooks"]]
    a3, a4, a5 = t["b3_at"], t["b4_at"], t["b5_at"]
    it1, it2, it3 = t["b6_items"]
    items = [
        {"title": it1[0], "sub": it1[1], "object": JK, "at": it1[2], "ring": "shoulder", "ring_at": it1[3]},
        {"title": it2[0], "sub": it2[1], "object": SHIRT, "at": it2[2], "then": JK, "then_at": it2[3], "ring": "shoulder", "ring_at": it2[4]},
        {"title": it3[0], "sub": it3[1], "object": JK, "at": it3[2], "ring": "shoulder", "ring_at": it3[3]},
    ]
    beats = [
        {"id": "b1", "function": "hook", "scene_type": "suitwerk_hook", "duration_hint": 6, "spoken": t["b1"],
         "data": {"question": t["q"], "object": JK, "target": "shoulder", "badge": "?", "question_at": 0.3, "hold_end": True, **t["b1_at"]},
         "source_ids": [], "overlay": {}},
        {"id": "b2", "function": "problem", "scene_type": "suitwerk_ladder", "duration_hint": 10, "spoken": t["b2"],
         "data": {"headline": t["b2_head"], "stages": [{"object": JK, "at": 0.0, "tags": _tags(t["b2_tags"]),
                                                        "focus_at": t["b2_focus"]}],
                  "backdrop": True, "hold_end": True},
         "source_ids": ["S2"],
         "overlay": {"transition": {"type": "iris", "x": 742, "y": 872, "seconds": 0.7}, "marker": "fakt", "marker_at": t["b2_mark"]}},
        {"id": "b3", "function": "explanation", "scene_type": "suitwerk_fitting", "duration_hint": 13, "spoken": t["b3"],
         "data": {"headline": t["b3_head"], "object": JK, "from": JK, "to": SHIRT, "target": "shoulder", "zoom": 1.5,
                  "label": t["b3_label"], "strain": False, "backdrop": True, "hold_end": True, **a3},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "vignette": True, "marker": "fakt", "marker_at": a3["zoom_at"]}},
        {"id": "b4", "function": "demonstration", "scene_type": "suitwerk_compare", "duration_hint": 13, "spoken": t["b4"],
         "data": {"headline": t["b4_head"],
                  "left": {"title": t["b4_l"][0], "object": JK, "target": "shoulder", "tag": t["b4_l"][1],
                           "pulses": [{"target": "shoulder", "at": a4["left_pulse"], "tone": "red"}]},
                  "right": {"title": t["b4_r"][0], "object": JK, "target": "shoulder", "tag": t["b4_r"][1],
                            "pulses": [{"target": "shoulder", "at": a4["right_pulse"], "tone": "red"},
                                       {"target": "sleeve", "at": a4["sleeve_pulse"], "tone": "red"}]},
                  "left_at": a4["left_at"], "left_tag_at": a4["left_tag_at"], "right_at": a4["right_at"], "right_tag_at": a4["right_tag_at"],
                  "backdrop": True},
         "source_ids": ["S1"],
         "overlay": {"transition": {"type": "blende", "seconds": 0.7}, "marker": "fakt", "marker_at": a4["left_at"]}},
        {"id": "b5", "function": "insight", "scene_type": "suitwerk_ladder", "duration_hint": 11, "spoken": t["b5"],
         "data": {"headline": t["b5_head"], "stages": [
             {"object": JK, "at": 0.0, "tags": _tags(t["b5_t1"])},
             {"object": JK, "at": a5["s2"], "tags": _tags(t["b5_t2"])}], "hold_end": True},
         "source_ids": ["S3"], "overlay": {"marker": "fakt", "marker_at": a5["mark"]}},
        {"id": "b6", "function": "benefit", "scene_type": "suitwerk_takeaway", "duration_hint": 12, "spoken": t["b6"],
         "data": {"headline": t["b6_head"], "items": items, "hold_end": True},
         "source_ids": ["S2", "S1", "S3"], "overlay": {"marker": "auslegung", "marker_at": "w:" + ("gesagt" if lang == "de" else "short")}},
        closing_beat(lang, t["b7"], SHIRT, JK, "shoulder", t["b7_stmt"], **t["b7_at"]),
    ]
    states = [{"beat": f"b{i + 1}", "text": tx, "tone": tone} for i, (tx, tone) in
              enumerate(zip(t["states"], ["amber", "red", "muted", "muted", "muted", "muted", "green"]))]
    return build(TID, lang, title=t["title"], notes="Suitwerk Woche 1 (Vorlage 1.0). Thema D02 aus menswear_2026-11.research.json. Nur Aussagen aus S1-S3; Schulter 'schwer, teuer, nicht empfohlen', nie 'unmöglich'. Keine Zeichnung für überstehende oder zu enge Schulter: Fehler als rote Ringe an Schulter und Ärmel.",
                 sources=SOURCES[lang], hooks=hooks, hook_note="Frage nach der Reihenfolge der Anprobe, Antwort: die Schulter.", beats=beats,
                 status_file=t["status"], states=states, description=t["desc"], hashtags=t["tags"],
                 unverified=["Welche anderen Stellen ein Schneider leicht ändern kann (Ärmel, Länge): in den Quellen nicht einzeln belegt, nicht im Video.",
                             "'Unmöglich zu ändern': nicht belegt, Quellen sagen schwer, teuer, nicht empfohlen."])


if __name__ == "__main__":
    for lang in ("de", "en"):
        write(make(lang))
