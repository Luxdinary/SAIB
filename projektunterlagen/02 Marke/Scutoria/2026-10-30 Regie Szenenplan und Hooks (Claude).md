# Scutoria – Regie: neuer Szenenplan, Hook-Konzepte, Quellenprüfung

Von Claude, 30.10.2026, Antwort auf die Reel-Analyse vom selben Tag. Bezugsvideo: `05 Produktion\_Test\ai_security-20261105-1-de\video.mp4` (74 s, Gemini-Stimme). Technik und Regeln: `C:\Automation\faceless-network\docs\direction-system.md`. Prototyp und Vorher-Nachher: `05 Produktion\_Demos\scutoria-regie\index.html`.

## Quellenprüfung (alle am 30.10.2026 abgerufen)

| ID | Quelle | Stand | Was belegt ist |
|---|---|---|---|
| S1 | privacy.claude.com „Is my data used for model training?" (Privatkonten) | 16.03.2026 | Free/Pro/Max: Chats und Coding-Sitzungen werden zum Verbessern genutzt, wenn man es in den Privatsphäre-Einstellungen erlaubt, wenn ein Chat zur Sicherheitsprüfung markiert wird, oder bei ausdrücklicher Zustimmung; Incognito-Chats nie. |
| S4 | privacy.claude.com „How do I change my model improvement privacy settings?" | 03.08.2026 | Weg: Name → Settings → Privacy (claude.ai/settings/data-privacy-controls) → Schalter **„Help Improve our AI models"**. Aus = neue Chats nicht mehr fürs Training; was schon in laufenden Trainingsläufen oder trainierten Modellen ist, bleibt. |
| S5 | privacy.claude.com „How long do you store my data?" (Privatkonten) | 01.07.2026 | Mit Training an: de-identifiziert bis zu 5 Jahre in Trainings-Pipelines. Gelöschte Unterhaltungen: innerhalb 30 Tagen aus dem Backend. |
| S6 | privacy.claude.com „Is my data used for model training?" (Firmenkunden) | 18.08.2026 | „By default, we will not use your inputs or outputs from our commercial products" (Claude for Work, API), außer Feedback/Opt-in. |
| S7 | Anthropic Commercial Terms | gültig seit 17.06.2025 | „Anthropic may not train models on Customer Content from Services"; Kunde behält Rechte an Eingaben, besitzt Ausgaben; Customer Content ist vertraulich; Kunde sichert zu, die Rechte zum Einreichen der Eingaben zu haben; DPA. |
| S2 | privacy.claude.com „Can you delete data that I sent via API?" | 16.03.2026 | Kein Ad-hoc-Löschen für zahlende API-Kunden; API-Daten nicht fürs Training (außer Vereinbarung). |
| S9 | privacy.claude.com „How long do you store my organization's data?" | 01.07.2026 | API-Ein-/Ausgaben werden standardmäßig innerhalb 30 Tagen gelöscht; Zero-Data-Retention-Vereinbarung möglich. |
| S8 | privacy.claude.com „Who owns and manages the data of my team?" | 16.03.2026 | Primary Owner der Organisation verwaltet das Work-Konto und alle Daten (Export, Zugriff entziehen). |
| S3 | BSI, „Generative KI-Modelle – Chancen und Risiken" | 21.01.2025 | Risiken und Gegenmaßnahmen für Industrie und Behörden. |
| – | Anthropic Privacy Policy | 10.09.2026 | Eingaben/Ausgaben können zum Training genutzt werden, außer man widerspricht in den Kontoeinstellungen; markierte Chats trotzdem. |

**UNVERIFIED (nicht im Video verwendet):** Standardzustand des Schalters bei neuen Konten (offiziell nicht genannt, Drittquellen widersprechen sich) · angebliches Opt-in-Programm für Team/Enterprise (nur inoffiziell) · Serverstandort/EU-Hosting · Wortlaut der Consumer Terms zur Verantwortung für Eingaben.

## Hook-Konzepte (fünf Kandidaten, drei zur Wahl)

Bewertung 1–5: Klarheit · Relevanz · Neugier · Wahrheit · Bild; Wahrheit unter 4 scheidet aus.

| ID | Typ | Gesprochen | Bild | Score |
|---|---|---|---|---|
| **H1** | Frage | „Darfst du vertrauliche Firmendaten einfach in Claude eingeben?" | Dokument fliegt in Chatfenster, Warnmarke | 5·5·4·5·5 → **90** |
| **H5** | konkretes Risiko | „Dein Mitarbeiter tippt die Kundenliste in einen KI-Chat. Wo landet sie?" (Hook des Bezugsvideos, Stimme vorhanden) | dasselbe Bild, Frage „Wo landet die Kundenliste?" | 5·5·4·5·5 → **90** |
| **H2** | Denkfehler | „Training aus, Datenschutz erledigt? Das ist der Denkfehler." | Schalter kippt, NEIN-Stempel | 4·5·5·4·4 → 86 |
| H3 | Fakt | „Mit Training an bleiben deine Chats bis zu fünf Jahre in Anthropics Trainings-Pipeline." (nur mit „de-identifiziert") | Kalender blättert | 3·4·5·4·4 → 78 |
| H4 | Demonstration | „Dieser eine Schalter entscheidet, ob Claude aus deinem Chat lernt." | Zoom auf den Schalter | 5·5·3·4·5 → 84 |

Empfehlung: **H1** für die Vollfassung (Frage aus der Analyse), **H5** wenn die vorhandene Stimme weiterverwendet werden soll. H2 als Alternative, wenn der Denkfehler den Einstieg tragen soll.

## Szenenplan Vollfassung (ca. 75 s, 171 Wörter, Plan-Datei `data/direction/ai_security-20261105-1-de.json`)

| Beat | Funktion | Szenentyp | Bild | Gesprochen | Quellen |
|---|---|---|---|---|---|
| 1 · 0–5 s | Hook | Cinematic Hook | „Firmendaten in Claude eingeben: erlaubt?", Kundenliste.xlsx fliegt in den Chat, Warnmarke | Darfst du vertrauliche Firmendaten einfach in Claude eingeben? | – |
| 2 · 5–14 s | Problem | Data Flow | Mitarbeiter → KI-Dienst → Verarbeitung; Chip „Kontotyp? Vertrag?" | Die Antwort hängt nicht nur von einer Einstellung ab. Sie hängt davon ab, welches Konto du nutzt und was im Vertrag steht. | S1, S6 |
| 3 · 14–30 s | Erklärung | Comparison (versus) | Karte Privatkonto (Training wenn erlaubt · Sicherheitsprüfung · bis zu 5 Jahre de-identifiziert) vs. Karte Firmenzugang (Standard kein Training · Eingaben bleiben dein Eigentum · API: kein Löschen auf Zuruf) | Bei privaten Konten, also Free, Pro und Max, dürfen Chats zum Verbessern der Modelle genutzt werden, wenn du das erlaubst, oder wenn ein Chat zur Sicherheitsprüfung markiert wird. Bei Firmenzugängen wie Claude for Work oder der API werden Eingaben standardmäßig nicht zum Training genutzt. | S1, S5, S6, S7, S2 |
| 4 · 30–42 s | Demonstration | UI Demonstration | Settings › Privacy, Cursor zum Schalter „Help Improve our AI models", Zoom, Schalter kippt | Für dein privates Konto prüfst du das hier: Einstellungen, Datenschutz, und der Schalter Help Improve our AI models. Aus heißt: neue Chats werden nicht mehr fürs Training verwendet. | S4 |
| 5 · 42–55 s | Erkenntnis (Denkfehler) | Comparison (negate) | „Training aus = Datenschutz erledigt" → Stempel NEIN; Unterzeile | Aber Vorsicht vor dem Denkfehler: Training aus heißt nicht Datenschutz erledigt. Was schon in einem Trainingslauf steckt, bleibt drin. Und ob du die Daten überhaupt eingeben darfst, regelt kein Schalter, sondern dein Vertrag und das Datenschutzrecht. | S4, S7, S3 |
| 6 · 55–68 s | Nutzen | Key Takeaway | drei Check-Karten: Vertrag und Kontotyp · Einstellung im Konto · Freigabe der Daten | Prüfe drei Punkte, bevor du sensible Inhalte hochlädst: erstens den Vertrag und Kontotyp, zweitens die Einstellung im Konto, drittens ob diese Daten überhaupt hinein dürfen. | – |
| 7 · 68–75 s | Abschluss | Key Takeaway (Aussage) + Outro | „Checkliste speichern. Beim nächsten KI-Einsatz: erst prüfen." · Scutoria-Endscreen | Speichere dir die Checkliste für den nächsten KI-Einsatz im Betrieb. Mehr Schutz für kleine Betriebe: folgen. | – |

Fünf Darstellungsformen, Schnitt an jedem Satzwechsel plus innere Bildereignisse (Paket, Stempel, Karten). Unterschied zum alten Skript: BSI-Szene gestrichen (nur noch als Beleg), API-Löschung in die Vergleichskarte verschoben, Denkfehler neu, Drei-Punkte-Check neu.

## UI-Demonstration: Was Stefan aufnehmen soll

Claude meldet sich in kein Konto an; der Prototyp zeigt eine **schematische** Darstellung (im Bild gekennzeichnet, Prüfbericht setzt HUMAN_REVIEW). Für die Vollfassung bitte aus einem Demo-Konto aufnehmen:

1. Browser am Desktop, 100 % Zoom, Fenster mindestens 1600 × 1000, dunkles oder helles Theme (bitte durchgehend eines).
2. claude.ai → Name unten links → **Settings** → **Privacy** (direkt: claude.ai/settings/data-privacy-controls).
3. Aufnahme 10–15 s: Seite ruhig stehen lassen (2 s), Maus zum Schalter **„Help Improve our AI models"**, 1 s warten, Schalter **aus**schalten, 2 s halten (zurückschalten ist egal, wird geschnitten).
4. Keine persönlichen Daten im Bild: Name, E-Mail, Abo-Stufe, Chat-Titel in der Seitenleiste ausblenden oder ein Demo-Konto ohne Chats nutzen.
5. Dateien: `brands\ai_security\assets\ui\claude-privacy-settings.mp4` (MP4 oder MOV, 60 fps gern) und ein Standbild `claude-privacy-settings.png` der Privacy-Seite.

Optional für den Vergleich Firmenzugang: ein Standbild der Admin-Ansicht eines Team-Plans (Primary Owner, Datenverwaltung) – nur wenn ein solches Konto vorhanden ist; sonst bleibt es bei der Karte.

## Prototyp (15 s, gerendert)

Hook H5 mit der vorhandenen Gemini-Stimme (keine neuen TTS-Kosten) + erste Problem-Szene als Data Flow. Dateien in `05 Produktion\_Demos\scutoria-regie\`: `vorher.mp4` (Bezugsvideo, erste 15 s), `nachher.mp4`, `vorher-nachher_5s.jpg`, `vorher-nachher_11s.jpg`, `report.json`, `index.html`.

## Entscheidungen für Stefan

1. Optik des Prototyps freigeben oder Änderungen nennen (Tempo, Farben der Warnmarke, Untertitelposition).
2. Hook für die Vollfassung: H1 oder H5 (oder H2).
3. Freigabe für eine neue Vertonung (Gemini Flash TTS, ca. 0,02 USD) – ohne sie bleibt es beim alten Text.
4. Bildschirmaufnahme der Claude-Einstellungen liefern (oben) oder die schematische Darstellung vorerst akzeptieren (dann HUMAN_REVIEW statt automatischer Freigabe).
