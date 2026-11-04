# Scutoria – Format-Bibel „Was tust du?“

Stand 02.11.2026, Fassung 1.0. **Gültig: von Stefan am 02.11.2026 mit dem Piloten „Neue Bankverbindung“ freigegeben.** Grundlage: `01 Idee und Strategie\Neuausrichtung 2026-11-02.md` (Stefans Entscheidung: jede Marke ein eigenes Format). Ersetzt für neue Videos die `Vorlage Scutoria (Fassung B).md`; die alte Vorlage bleibt als Nachweis liegen.

Umsetzung: `C:\Automation\faceless-network\brands\ai_security\scenes.py` (Szenentypen `sc_*`), Pilotplan `data\direction\ai_security-20261115-3-de.P1.json`.

## 1. Versprechen an den Zuschauer

**„Du erlebst in 75 Sekunden einen echten Moment aus einem kleinen Betrieb, triffst eine Entscheidung und weißt danach den einen Schritt, der dich schützt. Belegt, ruhig, ohne Panik.“**

- Ein Fall, keine Vorlesung. Der Zuschauer sitzt am Schreibtisch der Buchhaltung, im Büro, am Firmenhandy.
- Er entscheidet selbst (A, B oder C), bevor er die Lösung sieht.
- Er sieht die Folge einer falschen Wahl an der Uhr ablaufen, nicht als Drohung, sondern als nüchterne Abfolge.
- Am Ende steht genau **ein** Schritt, den er heute umsetzen kann, mit Beleg im Bild.

Zielgruppe unverändert: Inhaber und Büroteams kleiner Betriebe in DACH (EN-Fassung: englischsprachige Kleinbetriebe), die KI und Mail nutzen, aber keine IT-Sicherheitsabteilung haben.

## 2. Bildsprache

| Element | Regel |
|---|---|
| Grund | Scutoria-Designsystem (`OneDrive\scutoria\design\project\`, Tokens in `brand.yaml`): dunkler Grund `#0b1120`, flach, kein Glow, kein Verlauf. Higgsfield-Clips als ruhiger Hintergrund unter einem Schleier (scrim 0,62), je Szenentyp ein Clip. |
| Leitbild des Falls | **Das Objekt des Falls** (Mail, Rechnung, Chatfenster, QR-Code, Anrufanzeige) als Papierkarte (`paper #fbfbfd`), das einzige Helle im Bild. |
| Uhr | Große Uhrzeit in IBM Plex Mono („DI 09:12“). Die Uhr trägt die Dramaturgie: Eröffnung, Folge mit Zeitstempeln, „Wochen später“. Ersetzt Statusleiste und Leitdatei. |
| Entscheidung | Drei Karten A/B/C mit blauem Buchstabenfeld, darunter ein ablaufender Bernstein-Balken (2–3 s Denkpause). |
| Folge | Senkrechte Zeitleiste mit Punkten; neutral grau, Bernstein für das Verdächtige, Rot nur für den Endpunkt der Folge. |
| Der eine Schritt | Große Karte mit grünem Buchstaben (Grün nur für den richtigen Schritt), falsche Optionen werden rot durchgestrichen. Notfallschritt in Bernstein mit „!“. |
| Belege | Marker-Chips direkt in der Szene: Quadrat blau = **Fakt**, violett = **Auslegung**, grau = **Beispiel**, Halbkreis Bernstein = **Unsicher**. Quelle mit Herausgeber und Datum. |
| Schluss | Scutum-Marke, Regel in einem Satz (≤ 34 Zeichen), Frage an den Zuschauer („Was hättest du gewählt?“), scutoria.com, Claim, „Quellenbasiert. Keine Rechtsberatung.“ |
| Entfällt | Statusleiste, Erklärschicht (Kicker oben, Stimmen-Tag, Quellenleiste), Datei als roter Faden, Logo-Intro, Endkarte. KI-Kennzeichnung bleibt als Zeile „KI-generiert“ unten. |

Schrift: Manrope (Anzeige 800, Text 400), IBM Plex Mono für Uhrzeiten, Kicker und Belege. Untertitel in Phrasen zu höchstens vier Wörtern, 800 px breit. Alle Inhalte zwischen y 290 und y 1100.

## 3. Dramaturgie (Ablauf in Sekunden, gemessen am Piloten)

| Zeit | Beat | Szenentyp | Inhalt |
|---|---|---|---|
| 0–7,7 | Fall öffnet (Hook) | `sc_case` | Kicker „Beispielfall · nachgestellt“, Uhrzeit, Ort, das Objekt kommt herein, die verdächtige Zeile wird markiert. Erster gesprochener Satz ist Situation, keine Behauptung. |
| 7,7–22,6 | Du prüfst | `sc_inspect` | Was ein sorgfältiger Mensch prüfen würde, Zeile für Zeile, jeweils „unauffällig“. Pointe: „Nichts fällt auf.“ Dann der belegte Mechanismus als Fakt-Karte. |
| 22,6–34,3 | Entscheidung | `sc_choice` | „Was tust du?“, drei realistische Optionen, Denkpause mit Balken. |
| 34,3–46,1 | Folge | `sc_timeline` | Eine falsche Option wird an der Uhr durchgespielt, gekennzeichnet als „Beispiel“; Mechanik mit Quelle. |
| 46,1–57,2 | Der eine Schritt | `sc_step` (rule) | Richtige Option, Beleg-Chips, die falschen Optionen durchgestrichen mit kurzem Grund. |
| 57,2–65,3 | Wenn es schon passiert ist | `sc_step` (fallback) | Notfallschritte aus der Quelle (Bank, Polizei, Meldestelle). Entfällt, wenn die Quelle keine nennt. |
| 65,3–74,7 | Schluss | `sc_close` | Regel, Frage an den Zuschauer, Absender. |

Länge 65–90 s (Ziel 72–78 s). Gemessenes Sprechtempo Gemini Charon im Fallformat: DE 15,5, EN 15,3 Zeichen/s (20 Renders, 02.11.2026). Der Planbauer rechnet mit 15 Zeichen/s, also etwa 1.050–1.140 Zeichen Sprechtext. Längste Strecke ohne Bildereignis höchstens 13 s; jede Szene hat 3–5 wortgenaue Ereignisse (`"@Wort"`-Anker). Nach dem letzten Ereignis einer Szene bleiben mindestens 1,8 s Standzeit (setzt der Renderer). Die Fallkarte ist spätestens nach 1 s im Bild.

Werkzeuge: Spec je Video in `brands\ai_security\specs\<datum>-<n>-<de|en>.yaml`, Plan mit `build_plan.py` (prüft Textgrenzen, Länge, „ein Schritt“), Produktion mit `run_specs.py` (Trockenlauf, Gemini-Render über die Warteschlange, Überschneidungsprüfung, Export, Kalender und Redaktionsplan).

## 4. Wiederkehrende Reihen

| Reihe | Kern | Szenenfolge | Herkunft im Kalender |
|---|---|---|---|
| **Was tust du?** (Hauptreihe) | Ein Betrugsversuch oder eine Täuschung kommt herein: Mail, Anruf, QR-Code, Rechnung. A/B/C, Folge, ein Schritt. Mythen tauchen als falsche Option auf. | case → inspect → choice → timeline → step → (step fallback) → close | So läuft die Masche (16), Mythos-Check (16) |
| **Vor dem Upload** | Jemand will Kundendaten, Verträge oder Protokolle in ein KI-Tool geben. Optionen: so hochladen / vorher kürzen / anderes Tool. Folge: was laut Anbieterdokumentation mit den Daten passiert. | case (Chatfenster mit Datei) → inspect → choice → timeline → step → close | KI im Büro (20) |
| **Fünf Minuten, die gefehlt haben** | Rückwärts erzählt: Der Fall beginnt beim Schaden („Montag, 07:40, kein Zugriff aufs Postfach“), die Uhr läuft zurück zu der Einstellung, die es gestoppt hätte (2FA, Updates, Backup, Postfachregeln). | timeline (rückwärts) → case → step (Einstellung) → close | Fünf-Minuten-Schutz (20) |
| **Gilt das für uns?** | Regelthemen (AI Act, NIS2, DSGVO, CRA) als Fall eines Betriebs: zwei bis drei Prüffragen als Entscheidung, Antwort mit Fakt/Auslegung/Unsicher, ein Schritt (z. B. Liste anlegen, Behörde fragen). Nie ein Urteil „ihr seid betroffen“. | case → choice (Prüffragen) → step → close | Was gilt wirklich (12) |

Die 80 geplanten Themen bleiben; beim Neuschreiben wird jede Kalenderzeile einer der vier Reihen zugeordnet (Reihe im Feld `notes`). Für „Fünf Minuten“ und „Gilt das für uns?“ fehlen noch ein Rückwärts-Modus in `sc_timeline` und eine Prüffragen-Variante von `sc_choice` (siehe 7).

## 5. Was Scutoria von den anderen acht Marken unterscheidet

| Marke | Format | Scutoria dagegen |
|---|---|---|
| Promptwerk | echte Aufgabe, echter Terminal-Ablauf, echtes Ergebnis | Scutoria zeigt keinen Werkzeugablauf, sondern eine **menschliche Entscheidung** unter Zeitdruck. |
| Zonkfruit | Anime-Serie mit Figur Plümo | keine Figur, keine Fiktion als Unterhaltung; der Fall ist nur Träger für belegte Mechanik. |
| Dewlane | KI-animierte Beauty-Anwendung | dunkel, flach, Papier und Uhr statt Produkt und Textur. |
| Gigastruct | 3D-Modell als Leitmotiv, gerechnete Vergleiche | kein Modell, keine Zahlenshow; Zahlen nur, wenn sie die Entscheidung ändern. |
| Revlore, Suitwerk, Frontlore, Gritwerk | Wissen, Stil, Geschichte, Motivation | nur Scutoria fordert den Zuschauer zur **eigenen Wahl** auf und spielt die **Folge** durch. |

Erkennungsmerkmale, die keine andere Marke nutzt: die Uhrzeit als Einstieg, die A/B/C-Wahl mit Denkpause, die Zeitleiste der Folge, die Marker Fakt/Auslegung/Beispiel/Unsicher im Bild und die Schlussfrage „Was hättest du gewählt?“.

## 6. Prüfregeln (vor jedem Render, zusätzlich zu den gemeinsamen Prüfungen)

Inhalt:
1. **Beispielfall kennzeichnen.** Erste Szene trägt „Beispielfall · nachgestellt“; Betriebe, Personen und Absender sind erkennbar erfunden („Holzhandel Beispiel GmbH“, Domains auf `.example`). Keine echten Firmen, Marken oder Personen als Täter oder Opfer.
2. **Mechanik nur aus Quellen.** Wie die Masche funktioniert und was dagegen hilft, steht in einer Quelle mit URL und Abrufdatum. Erfunden sein darf nur die Situation (Uhrzeit, Branche, Wortlaut der Mail). Erfundene Abläufe stehen in `unverified` und tragen im Bild den Marker „Beispiel“.
3. **Keine erfundenen Zahlen.** Beträge, Schadenssummen, Häufigkeiten nur mit Quelle; im Beispielfall lieber gar keinen Betrag.
4. **Genau ein richtiger Schritt**, heute umsetzbar, ohne Kauf. Keine zusätzliche To-do-Szene. Daneben höchstens ein Notfallblock („Schon passiert?“) mit höchstens zwei Schritten, nur wenn eine Quelle sie nennt. Listen, die Inhalt des einen Schritts sind (Farben einer Ampel, Schulungsfragen), tragen Farbmarken statt Nummern. (Prüfrunde 03.11.2026)
5. **Faire Optionen.** Die falschen Antworten sind das, was vernünftige Menschen tatsächlich tun würden. Kein Spott, kein „wer darauf reinfällt …“.
6. **Auslegung markieren.** Was Scutoria aus einer Quelle folgert, ist im Bild „Auslegung“, nicht „Fakt“.
7. **Keine Angstmache.** Keine Kapuzenhacker, keine Sirenen, kein rotes Vollbild, keine Totenköpfe. Rot nur für den Endpunkt der Folge und Durchstreichungen.
8. **Keine Rechtsberatung, keine Anleitung zum Angriff.** Die Masche wird aus Sicht des Betriebs gezeigt, nie als Bauanleitung. Regelthemen enden mit Auslegung oder offener Frage und dem Hinweis auf die zuständige Stelle.
9. Anrede „du“, der Betrieb ist „ihr/euer“. Ruhiger Ton, kurze Sätze. Entscheidung auf Deutsch mit „Entscheide dich jetzt.“ („Merk dir“ versteht die Spracherkennung als „Merkt ihr“).
10. **EN lokal denken.** Deutsche Behörden im EN-Text als solche benennen („German police“, „Germany's BSI“), nie „Berlin police“.

Lesbarkeit: Etiketten, Beleg-Chips und Uhrzeiten mindestens 28 px; Schritt-, Notfall- und Folgeszenen füllen die Zone bis y 1100.

Technik (gemeinsam, unverändert): Gemini-Stimme (nie SAPI/Edge), 65–90 s, `story.validate` und Trockenlauf ohne Fehler, Textgrenzen der `sc_*`-Typen (`LIMITS` in `scenes.py`), `node scripts\overlap_check.mjs` ohne Befund am Render, KI-Kennzeichnung im Bild und in `post.json`, Clips nur mit Lizenzzeile in `assets\higgsfield\LICENSE.md`.

## 7. Offene Punkte

- Echte Denkpause in der Entscheidung (die Stimme spricht derzeit über den Balken); bräuchte eine Pause in der Vertonung.
- Für die Reihen „Fünf Minuten“ (rückwärts laufende Uhr) und „Gilt das für uns?“ (Prüffragen) je eine Variante der Szenentypen bauen.
- Optional: ein eigener Higgsfield-Clip „Schreibtisch Buchhaltung, Nacht, ruhig“ für `sc_case`, falls Stefan Credits freigibt.
