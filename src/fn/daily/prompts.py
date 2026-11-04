"""Prompt templates of the daily runner (compact: every call is a short standalone job over the subscription).

German plan: rules of the direction system, the brand's format essentials (trimmed Format-Bibel), the chosen Bildaufbau,
scene docs of the allowed types, material list, a shortened approved plan as few-shot, then the task. English plan:
translation rules plus the German plan. Repair: the validation errors plus the previous plan.
"""
from __future__ import annotations

import json

from .context import BrandContext, SourceRef, shorten_plan
from .topics import Topic

HOOK_TYPES = "question (vertretbare Frage), misconception (Denkfehler), surprising_fact (belegbarer Sachverhalt), " \
             "concrete_risk (Risiko aus dem Alltag der Zielgruppe), demonstration (sichtbare Demonstration)"
CUE_NAMES = "whoosh, whoosh2, swipe, swipe2, click, tick, stamp, paper, pop, thud, chime, riser (Suffix _leise = 6 dB leiser), " \
            "bett_ein, bett_aus, bett_aus_schlussakkord"


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def _material_block(ctx: BrandContext) -> str:
    lines = []
    for m in ctx.material:
        if not m.licensed:
            continue
        hint = (m.use or m.purpose or "")[:36]
        kind = f" [Clip {m.duration_s:.0f}s]" if m.kind == "video" and m.duration_s else (" [Clip]" if m.kind == "video" else "")
        lines.append(f"- {m.path_in_assets}{kind}" + (f": {hint}" if hint else ""))
    return "\n".join(lines) if lines else "- (keine Dateien mit Lizenzzeile gefunden)"


def system_prompt_de(ctx: BrandContext, lang_window: tuple[int, int, int], *, scene_types: list[str], hook_types: list[str],
                     example: dict, aufbau_letter: str | None, aufbau_text: str, aufbau_hint: str,
                     aufbau_types: list[str] | None = None) -> str:
    s = ctx.settings
    b = ctx.brand
    lo, target, hi = lang_window
    rules = "\n".join(f"- {r}" for r in ctx.brand_rules) or "- (keine zusätzlichen Markenregeln)"
    limits = "; ".join(f"{t}: " + ", ".join(f"{k} {v}" for k, v in lim.items()) for t, lim in ctx.limits.items() if t in scene_types and lim) \
        or "(keine festen Zeichengrenzen; Headlines höchstens 34 Zeichen)"
    rec_block = ""
    if ctx.recordings:
        rec_block = "\n\n## Vorhandene Aufzeichnungen (nur diese Namen sind erlaubt)\n" + ", ".join(ctx.recordings)
    return f"""Du schreibst für die Marke {b.name} (brand_id `{b.id}`, Nische: {b.niche}) ein vollständiges Regie-Skript („Plan“) im JSON-Schema der Story-Engine des Kurzvideo-Netzwerks von Stefan Dallinger. Antworte ausschließlich mit einem JSON-Objekt.

## Regeln (Verstöße blockieren die Produktion)
1. Nichts erfinden: Jede Tatsachenbehauptung (Zahl, Datum, Norm, Studie, Name) hat eine Quelle aus der Quellenliste der Aufgabe (gleiche URL, gleiche id); keine anderen URLs. Was die Quellen nicht hergeben, kommt nicht ins Skript, sondern als Satz in `unverified`. Zahlen, Jahreszahlen und Datumsangaben im Sprechtext, im Titel und in der Beschreibung müssen wörtlich in den Belegen der Aufgabe stehen (Kalenderansatz, Belegsätze, Quellenliste, Hook-Idee); eigenes Wissen darf keine Zahl liefern, ein Skript mit einer Zahl ohne Beleg wird abgelehnt. Das Wort UNVERIFIED darf nirgends vorkommen.
2. `hook_candidates`: fünf Kandidaten, je einer je Typ ({HOOK_TYPES}); je id (H1…H5), type, spoken (≤ 90 Zeichen), on_screen (≤ 64), scores (ganze Zahlen 1–5: clarity, relevance, curiosity, truth, visual), source_ids, visual (ein Satz), why (kurz). truth < 4 ist unwählbar; surprising_fact, misconception, concrete_risk brauchen source_ids. `hook` = {{"id": "<Gewinner>", "note": "<warum>"}}; der erste Beat beginnt mit dessen spoken.
3. Beats: Funktionen in der Reihenfolge hook → problem → explanation → demonstration → insight → benefit → close (Wiederholungen ja, Rücksprünge nein); erster Beat hook mit Hook-Szenentyp ({", ".join(hook_types)}), letzter Beat close; problem, explanation, demonstration, insight brauchen source_ids. ids b1, b2, …; je Beat spoken, data, source_ids, overlay: {{}}.
4. Szenentypen nur aus: {", ".join(scene_types)}. Mindestens drei verschiedene je Video, nie dasselbe Layout zweimal nacheinander. Zwischen zwei Bildereignissen (Beat-Wechsel, Einblendungen an gesprochenen Wörtern) höchstens 12 s: Beats über 10 s brauchen mindestens vier gleichmäßig verteilte Ereignisse. Datenfelder genau wie dokumentiert und wie im Beispiel, keine erfundenen Felder; Felder, die im Beispiel Zahlen sind, bleiben Zahlen (kein Text in Zahlenfeldern).
5. Wortanker: "w:Wort" (erstes gesprochenes Wort des Beats, das so beginnt; "w:Wort#2" zweites Vorkommen; "+0.5" verschiebt) oder die Schreibweise des Beispiels ("@Wort+0.5", "<ereignis>_word"); immer ein Wort aus dem spoken desselben Beats. Je Szene mindestens drei Bildereignisse an gesprochenen Wörtern.
6. Sprechtext: Deutsch, „du“, sachlich, kurze Sätze, kein Ausrufezeichen, keine Schadensdramatik, keine Floskeln; die Stimme beschreibt, was das Bild zeigt. Alle spoken zusammen {lo}–{hi} Zeichen mit Leerzeichen (Ziel {target}; erlaubt sind 65–90 s Video). Zähle nach: Entwürfe fallen erfahrungsgemäß zu kurz aus; unter {lo} Zeichen wird der Plan abgelehnt.
7. Textgrenzen (Zeichen) je Szenentyp und Feld: {limits}. Die Grenze eines Feldnamens gilt auch für gleichnamige Felder und Felder, die auf _<Feldname> enden, in Unterobjekten und Listen (z. B. rows[].title, section.film_label); Texte lieber 2 Zeichen kürzer als die Grenze.
8. Bildmaterial nur aus der Materialliste, referenziert wie im Beispiel (gleiche Schlüssel, gleiche Pfadform). {s.get('material_hint', '')} Nichts Neues anfordern, keine Gesichter; realistische Bilder sind KI-Bilder (Kennzeichnung macht der Renderer).
9. `layout` aus dem Beispiel übernehmen; neu nur description (2–4 Sätze), companion_text, hashtags (5, klein, ohne #), short_title (≤ 28 Zeichen; Buchstaben, Ziffern, Leerzeichen, Bindestrich), sound_cues (wie im Beispiel: beat, at = Anker oder "start"/"end", cue aus {CUE_NAMES}, optional gain_db, note). Themenbezogene layout-Werte des Beispiels (laborbuch, echtlauf.recording, model3d, media, ruler, computations) in derselben Form an das Thema anpassen.
10. `sources`: id (S1, S2, …), url (aus der Liste), title (was belegt wird, mit Seite/Abschnitt), label (≤ 40 Zeichen), checked_at (aus der Liste, unverändert). video_id, brand_id, language wie in der Aufgabe; title ≤ 100 Zeichen; notes: Herkunft in einem Absatz.
11. Markenregeln:
{rules}
Keine Wartungs-, Reparatur-, Installations- oder Tuninganleitung, keine Kaufempfehlung, keine Heil- oder Wirkungsversprechen, nichts zum gefährlichen Nachmachen; bei Elektrik der Hinweis auf die Elektrofachkraft.

## Format der Marke (Auszug aus der Format-Bibel)
{ctx.format_essentials.strip() or '(keine Format-Bibel gefunden)'}

## Kurzkonzept
{(ctx.konzeptplan.kurzkonzept or '(kein Kurzkonzept gefunden)')[:800]}

## Bildaufbau dieses Videos
{aufbau_letter or '–'}: {aufbau_text or 'wie im Beispielplan'}
{aufbau_hint}
Szenentypen dieses Aufbaus: {', '.join(aufbau_types) if aufbau_types else 'wie im Beispielplan'}. Mindestens zwei Beats nutzen Szenentypen dieses Aufbaus; die übrigen Typen der Liste bleiben erlaubt.

## Szenentypen und Datenfelder (aus dem Code der Marke)
{ctx.scene_docs_for(scene_types)}

## Materialliste (Pfade relativ zu brands/{b.id}/assets/higgsfield; nur lizenzierte Dateien)
{_material_block(ctx)}{rec_block}

## Beispielplan (freigegebenes Video der Marke, Auszug): Muster für Schema, Felder, Material, Ton
{_dump(shorten_plan(example, 2, tuple(s.get('example_keep_layout_keys') or ())))}"""


def user_prompt_de(topic: Topic, video_id: str, refs: list[SourceRef], cal: dict | None, research: dict | None,
                   lang_window: tuple[int, int, int]) -> str:
    lo, target, hi = lang_window
    src_lines = []
    for r in refs:
        state = "" if r.reachable is None else (" (erreichbar)" if r.reachable else f" ({r.note})")
        src_lines.append(f"- {r.id}: {r.url} · checked_at {r.checked_at}{state}" + (f" · belegt: {r.title}" if r.title else ""))
    cal_block = ""
    if cal:
        cal_block = "\n".join(f"- {k}: {v}" for k, v in cal.items() if k in ("topic_id", "title", "angle", "notes", "risk_level"))
    res_block = ""
    if research:
        ev = (research.get("source_evidence") or [])[:6]
        res_block = "\n".join(f"- {str(e)[:220]}" for e in ev)
        if research.get("notes"):
            res_block += f"\n- Hinweise: {research['notes']}"
    return f"""## Aufgabe: deutscher Plan für dieses Thema
- video_id: {video_id} · brand_id: {topic.brand_id} · language: de
- Konzeptplan Nr. {topic.nr or '–'}: {topic.title}
- Reihe: {topic.reihe or '–'}{(' · Bereich: ' + topic.bereich) if topic.bereich else ''} · Risiko laut Konzeptplan: {topic.risk or '–'}
- Hook-Idee aus dem Konzeptplan: {topic.hook_idea or '–'}
- Material-Hinweis aus dem Konzeptplan: {topic.material_hint or '–'}; geplantes neues Bild: {topic.new_image_hint or '–'} (wird NICHT erzeugt: vorhandenes Material verwenden oder weglassen)

Kalender-Eintrag (verbindlich für die Aussagen):
{cal_block or '- (kein Kalendereintrag; nur die Quellenliste zählt)'}

Belege aus der Recherche (Reihenfolge der Quellenliste):
{res_block or '- (keine Belegnotizen)'}

Quellenliste (nur diese URLs, mit diesen ids und checked_at):
{chr(10).join(src_lines) or '- (keine Quelle: nur Aussagen ohne Tatsachenbehauptung; alles Prüfbare nach unverified)'}

Sprechtext gesamt {lo}–{hi} Zeichen (Ziel {target}). Gib den vollständigen Plan als ein JSON-Objekt aus."""


def system_prompt_en() -> str:
    return """You localise direction plans of a German short-video network into English. You get one finished German plan (JSON, schema of the story engine). Produce the English version of the SAME video: same beats (ids, functions, scene types), same scene data keys, same material files, same sources (ids, urls, checked_at unchanged), same layout values and sound cues; only the language changes. Answer with one JSON object only.

Rules:
1. Translate `spoken` sentence by sentence into natural spoken English for the same audience (localised, not word for word; English number formatting, units as in the source); keep every fact exactly, add or drop nothing. Keep the total character count within the given window.
2. Translate every on-screen text in the scene data (claims, headlines, rows, labels, notes, chips, stamps, source lines such as "Quelle: … · abgerufen 02.11.2026" -> "Source: … · retrieved 02.11.2026"), the hook candidates (spoken, on_screen, why, visual), title, layout.description, layout.companion_text, layout.hashtags (English tags), layout.short_title (ASCII letters, digits, spaces, hyphens, max 28 chars), unverified, notes ("English version from the same scenes as <german video_id>; text localised, not rewritten"). A `file:` source of an English recording may point at the English recording.
3. Every word anchor must point at a word of the ENGLISH `spoken` text of the same beat: "w:Word", "w:Word#2", "w:Word+0.5", "@Word+0.5" and every `<event>_word` / `at_word` value; choose the English word at the same moment of the sentence. Plain numbers, "start" and "end" stay.
4. Keep untouched: brand_id, scene types, beat ids, data keys, file names, assets, sources (ids, url, checked_at; translate title and label only if they are German prose), layout keys and numbers, hook.id, scores.
5. Set video_id and language as given. Never invent facts or sources."""


def user_prompt_en(de_plan: dict, video_id_en: str, lang_window: tuple[int, int, int], example_en: dict | None = None) -> str:
    lo, target, hi = lang_window
    ref = ""
    if example_en:
        ref = f"Reference (approved English plan of this brand, shortened; shows English on-screen texts, source lines and anchors):\n{_dump(shorten_plan(example_en))}\n\n"
    return f"""{ref}German plan (source of truth):
{_dump(de_plan)}

Produce the English plan with video_id "{video_id_en}", language "en". Total characters of all `spoken` texts: {lo}–{hi} (target {target}). Output one JSON object only."""


def repair_prompt(errors: list[str], warnings: list[str], lang: str) -> str:
    err = "\n".join(f"- {e}" for e in errors)
    warn = "\n".join(f"- {w}" for w in warnings)
    if lang == "de":
        return f"""Der Plan hat die Prüfung nicht bestanden. Behebe genau diese Punkte und gib den vollständigen, korrigierten Plan als ein JSON-Objekt aus (alle Felder, nicht nur die geänderten):
{err}
{('Hinweise (nicht blockierend):' + chr(10) + warn) if warn else ''}"""
    return f"""The plan failed validation. Fix exactly these points and return the complete corrected plan as one JSON object (all fields, not only the changed ones):
{err}
{('Notes (not blocking):' + chr(10) + warn) if warn else ''}"""


REPAIR_SYSTEM_DE = """Du korrigierst ein Regie-Skript (JSON) für den Renderer der Marke {brand}. Der Renderer hat den Plan im Trockenlauf abgelehnt. Behebe genau die gemeldeten Ursachen und ändere sonst nichts Inhaltliches: Sprechtext, Quellen, Aussagen und Szenenfolge bleiben, es sei denn, eine Textgrenze zwingt zum Kürzen eines Bildschirmtextes. Gib den vollständigen, korrigierten Plan als ein JSON-Objekt aus, kompakt, ohne Text davor oder danach.

Hinweise zu häufigen Meldungen:
- "could not convert string to float" / ValueError / TypeError: ein Datenfeld hat den falschen Typ (Text statt Zahl oder umgekehrt); nimm die Form aus der Szenen-Dokumentation oder dem Beispiel.
- "chars > N": der Text ist länger als N Zeichen; kürze ihn (gilt auch für Felder in Unterobjekten und Listen).
- "visual_cuts_static ... longest stretch ... s": irgendwo liegen mehr als 14 s zwischen zwei Bildereignissen. Suche in der Beat-Tabelle der Meldung den Beat mit der längsten Dauer und setze dort weitere Bildereignisse an gesprochene Wörter (Zeitfelder wie *_at oder *_word der Szenendaten), gleichmäßig verteilt, höchstens 10 s Abstand.
- "word anchor ... not found" / "not spoken": der Anker muss ein Wort des Sprechtexts desselben Beats sein.
- "asset missing" / "licence": nur Dateien aus der Materialliste verwenden.
- Der Sprechtext darf nicht verändert werden (die Stimme wird danach aufgenommen).

## Szenentypen und Datenfelder
{docs}

## Textgrenzen
{limits}"""

REPAIR_SYSTEM_EN = """You fix a direction plan (JSON) for the renderer of the brand {brand}. The renderer rejected the plan in its dry run. Fix exactly the reported causes and change nothing else in substance: spoken text, sources, claims and scene order stay, unless a text limit forces a shorter on-screen text. Return the complete corrected plan as one compact JSON object, no text before or after.

Hints for common messages:
- "could not convert string to float" / ValueError / TypeError: a data field has the wrong type (text instead of a number or the other way round); use the form of the scene documentation or the example.
- "chars > N": the text is longer than N characters; shorten it (also fields in sub-objects and lists).
- "visual_cuts_static ... longest stretch ... s": somewhere more than 14 s lie between two visual events. Find the beat with the longest duration in the beat table of the message and add more events on spoken words (time fields such as *_at or *_word of the scene data), evenly spread, at most 10 s apart.
- "word anchor ... not found" / "not spoken": the anchor must be a word of the spoken text of the same beat (English words in the English plan).
- "asset missing" / "licence": only files of the material list.
- The spoken text must not change (the voice is recorded afterwards).

## Scene types and data fields
{docs}

## Text limits
{limits}"""


def repair_system(lang: str, brand: str, docs: str, limits: str) -> str:
    return (REPAIR_SYSTEM_DE if lang == "de" else REPAIR_SYSTEM_EN).format(brand=brand, docs=docs, limits=limits or "-")


def dry_run_repair_user(lang: str, diag: str, plan: dict) -> str:
    plan_text = json.dumps(plan, ensure_ascii=False, separators=(",", ":"))
    if lang == "de":
        return ("Meldung des Renderers (Ausgabe des Trockenlaufs, mit Beat-Tabelle: Beat, Funktion, Szenentyp, Start, + Dauer in s):\n" + diag +
                "\n\nDein bisheriger Plan:\n" + plan_text)
    return ("Renderer message (output of the dry run, with beat table: beat, function, scene type, start, + duration in s):\n" + diag +
            "\n\nYour previous plan:\n" + plan_text)
