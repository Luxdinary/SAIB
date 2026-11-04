# Fragenkatalog an Stefan

Stand: 30.10.2026, 00:30 (Wien). Alle 25 Fragen am 29.10.2026 beantwortet. Die Antworten stehen hier oben, die ursprünglichen Fragen mit den damaligen Annahmen darunter als Verlauf. Gültig ist, was in `Konzept.md` steht.

## Antworten (29.10.2026)

| Nr. | Antwort Stefan | Folge für den Bau |
|---|---|---|
| 1 | Alle Marken auf einmal fertig bauen; Namen nochmals prüfen und bessere finden; Veröffentlichung beginnt mit **PromptPilot** (Arbeitsname) und **Scutoria** | Scutoria ersetzt „NeuralShield" als Marke für KI und Sicherheit. Designsystem und Konfiguration für alle 9 Marken in Phase 1; Namensrecherche läuft (`02 Marke\Namensrecherche 2026-10-29.md`) |
| 2 | Zuerst Deutsch, parallel Englisch | Jedes Thema wird in DE und EN produziert, von Anfang an |
| 3 | Ein Konto je Marke | DE und EN laufen auf demselben TikTok-, Instagram-, YouTube-Konto. Annahme dazu: je Slot ein Video, Sprachen wechseln sich ab (siehe Nr. 4); YouTube zusätzlich mehrsprachige Audiospur prüfen |
| 4 | Slots 12:00, 14:00, 18:00 | 3 Veröffentlichungen je Marke und Tag ab Phase 2 (Wiener Zeit). Annahme: 3 Themen je Tag, jedes in DE und EN gerendert; je Slot wird eine Sprachfassung gepostet, die andere am Folgetag oder im nächsten Slot, so dass je Konto 3 Posts/Tag bleiben (TikTok-Cap 15 weit unterschritten). Wenn Stefan 6 Posts/Tag will (3 DE + 3 EN), bitte sagen |
| 5 | 2 Stunden pro Tag | Zeit für Themenwahl, Freigaben, Gegenlesen; mehr als nötig, erlaubt Kalibrierung |
| 6 | Automatisch | Veröffentlichung ohne manuelle Freigabe, sobald technische und Compliance-Prüfung bestanden; Claude-Empfehlung: die ersten 20 Videos je Marke von Hand freigeben (Kalibrierung), danach automatisch; sensible Themen (Risiko „hoch") bleiben manuell |
| 7 | Puffer | 7–14 Tage vorproduzierter, geprüfter Videos; läuft ohne Netz weiter |
| 8 | Ja, Kommentare beantworten | eigener Baustein ab Phase 3; nur über offizielle APIs bzw. Upload-Post, eigene Regeln (keine Streitgespräche, keine Beratung, Kennzeichnung) |
| 9 | 50 € im Monat | Phase 2 passt (Upload-Post Basic ca. 22 €, TTS unter 5 €). Ab 3 Marken (9 Profile) Basic + Add-on 39 USD ≈ 36 €; ab 6 Marken Professional 50 USD ≈ 46 € bei Monatszahlung, KI-Clips dann nicht im Budget. Budget wird je Phase neu vorgelegt |
| 10 | Gewerbe und Steuerberatung noch nicht | Phase 0: Werbeagentur (freies Gewerbe) prüfen bzw. bestehendes Scutoria-Gewerbe erweitern; vor dem ersten bezahlten Werbepartner zwingend |
| 11 | Scutoria-Adresse | Impressum je Profil mit Name und Scutoria-Anschrift |
| 12 | Je Marke eine Gmail-Adresse mit YouTube-, TikTok-, Instagram-Kanal | 9 Google-Konten, gestaffelt angelegt (Telefonnummern: YouTube höchstens 2 Kanäle je Nummer und Jahr). **Überholt 02.11.2026:** Google Workspace `admin@scutoria.com` als Zentrale, je Marke ein Alias, YouTube als Markenkonten (siehe `Konzept.md`) |
| 13 | Recherche und Analyse zu den Namen | läuft, Ergebnis in `02 Marke` |
| 14 | C: reicht, Stefan löscht etwas | kein externer Datenträger; Claude überwacht freien Platz und warnt unter 30 GB |
| 15 | Bestehendes Claude-Konto, später eventuell Mac mini M1 | kein zweites Abo; Produktion läuft über Stefans Max-Konto; Verbrauch gegen 5-Stunden- und Wochenlimit messen; API-Key als Ausweichweg |
| 16 | Ja | Code und Produktion in `C:\Automation\faceless-network`, Spiegel nach `OneDrive\Business\05 Produktion` |
| 17 | Laptop läuft 24/7 | Produktion kann rund um die Uhr geplant werden; Energieeinstellungen: kein Standby am Netz |
| 18 | Gemini-Stimme | Gemini Flash TTS, Paid Tier; ElevenLabs nur als Vergleich |
| 19 | Ja | Phase 1–2 Animation und KI-Bilder; KI-Clips ab Phase 3 für die ersten 5 Sekunden |
| 20 | Ja | Militärkanal nur historisch, keine Taktik, nichts Dienstliches, keine Uniform, Phase 4 oder später |
| 21 | Noch keine Produkte; Ziel: Werbung für Beauty-Produkte schalten lassen | Beauty-Kanal auf Inhaltsstoffwissen und Routinen ohne Produktversprechen; Media-Kit für Werbepartner; keine Affiliate-Links ohne Produktkenntnis |
| 22 | Eigene Figur | Brainrot mit eigenem Charakter: Charakter-Sheet (Ansichten, Farben, feste Merkmale), Style-Lock |
| 23 | Ja | echte Bildschirmaufnahmen aus einem Demo-Projekt für Claude-Workflows |
| 24 | Neben Scutoria | beide laufen; Scutoria wird zusätzlich eine der Videomarken |
| 25 | Ja | täglicher Log-Eintrag, Wochenbericht in `07 Auswertung` |

---

## Ursprüngliche Fragen (29.10.2026, mit damaligen Annahmen)

## A. Umfang des Starts (am wichtigsten)

1. **Mit welchen zwei Kanälen starten wir?** Mein Vorschlag: PromptPilot (Claude-Workflows) und NeuralShield (KI und Sicherheit), weil du dort Fachwissen einbringst, die Quellenlage gut ist und das Richtlinienrisiko niedrig. Annahme ohne Antwort: diese zwei.
2. **Welche Sprache zuerst?** Englisch hat die größere Reichweite und das YouTube-Partnerprogramm ist von Österreich aus für beide Sprachen offen; Deutsch hat weniger Konkurrenz und deine natürliche Stimme in den Skripten. Annahme: Englisch zuerst, Deutsch als zweite Fassung ab Phase 3.
3. **Getrennte DE- und EN-Konten oder ein Konto je Marke?** Getrennt = doppelte Konten und Profile, saubere Zielgruppen. Ein Konto = halber Aufwand, aber gemischte Zielgruppe (Plattformen zeigen Videos nach Sprache der Zuschauer). Annahme: getrennte Konten, aber erst anlegen, wenn die zweite Sprache startet.
4. **Wie viele Videos pro Kanal und Tag in Phase 2?** Das Ziel 3/Tag bleibt für die Architektur; für den Start empfehle ich 1/Tag je Kanal (das ist bereits 1 Video alle 24 h, 60–90 s, zweisprachig später). Annahme: 1/Tag, Steigerung auf 3/Tag nach den ersten 100 Videos, wenn Verwurfquote unter 20 % liegt.
5. **Wie viel Zeit pro Tag hast du für Themenwahl und Freigabe am Handy?** Das System des Kollegen braucht etwa 10–15 Minuten abends (Themen antippen) und tagsüber kurze Freigaben. Annahme: 15 Minuten pro Tag.

## B. Freigabe und Automatisierungsgrad

6. **Soll jedes Video von dir freigegeben werden, oder dürfen Videos mit niedrigem Risiko nach einer Einlaufphase automatisch veröffentlicht werden?** Vorschlag: die ersten 100 Videos je Kanal alle von Hand freigeben; danach automatische Freigabe für Formate, die du als „sicher" markiert hast; Beauty, Militär und alles mit Produktversprechen bleiben dauerhaft manuell. Annahme: so.
7. **Was passiert, wenn du im Einsatz keinen Netzzugang hast?** Option a: Pipeline hält an und holt nach. Option b: vorproduzierter Puffer von 7–14 Tagen, der ohne dich läuft (nur freigegebene Videos). Annahme: b, mit Puffer von 7 Tagen.
8. **Darf Claude Kommentare beantworten?** Das ist ein eigener Automatisierungsbaustein mit eigenem Risiko. Annahme: nein, nur Statistik lesen.

## C. Geld und Konten

9. **Monatliches Budget für Dienste in Phase 1–2?** Fixkosten laut Prüfung: Upload-Post Professional 50 USD/Monat monatlich (oder 33 USD/Monat bei Jahreszahlung), TTS je nach Anbieter, KI-Videoclips sind der größte Kostentreiber. Ohne Zahl plane ich mit 150 EUR/Monat ohne KI-Videoclips und baue Clips erst ein, wenn du die Kosten freigibst.
10. **Gibt es schon ein Gewerbe (aus Scutoria) und eine Steuerberatung?** Das bestimmt Impressum, Rechnungen an Werbepartner, Umsatzsteuer. Annahme: Gewerbe aus Scutoria vorhanden, Details zu klären.
11. **Impressum und Offenlegung:** Welcher Name und welche Anschrift stehen in den Profilen (Pflicht in Österreich)? Ein Postfach oder die Scutoria-Adresse? Annahme: wie bei Scutoria.
12. **Gmail-Konten:** Eine Adresse je Marke (9 neue Google-Konten, davon zunächst 2) oder ein zentrales Google-Konto mit Brand-Kanälen auf YouTube plus je Marke nur die TikTok- und Instagram-Konten? Instagram erlaubt laut Hilfe höchstens 5 Konten je E-Mail-Adresse, TikTok eine E-Mail je Konto, YouTube verifiziert eine Telefonnummer mit höchstens 2 Kanälen pro Jahr. Annahme: je Marke ein Google-Konto, Telefonnummern vorab zählen.
13. **Markennamen:** ChatGPT schlägt NeuralShield, VelvetGlow, PromptPilot, TailoredCode, GlitchMango, RiseTheory, IronArchive, TitanWorks, TorqueLab vor. Soll ich die Verfügbarkeit (Handles, Domains, Markenregister TMview) für die ersten zwei prüfen, bevor du Konten anlegst? Annahme: ja, Prüfung vor Kontoanlage; „PromptPilot" ist vermutlich belegt.

## D. Technik

14. **Laufwerk C: hat nur 61 GB frei (von 3,7 TB).** Soll ich suchen, was den Platz belegt, oder arbeiten wir mit einer externen SSD für Rohmaterial und Renders? Annahme: zuerst Analyse der Belegung, Vorschlag an dich, nichts löschen.
15. **Eigener Windows-Benutzer „Automations" mit eigenem Claude-Konto wie beim Kollegen, oder dein bestehendes Konto?** Ein zweites Konto kostet ein zweites Abo. Mit deinem Max-Konto geht es auch; dann konkurrieren Produktion und deine eigene Arbeit um dieselben Nutzungslimits. Annahme: zunächst dein Konto, Trennung über einen eigenen Projektordner; zweites Konto erst bei Bedarf.
16. **Projektordner:** `C:\Automation\faceless-network` (außerhalb von OneDrive, wegen Rohmaterial und Git) oder innerhalb von `OneDrive\Business`? Vorschlag: Code und Produktion außerhalb von OneDrive, fertige Videos und Skripte werden nach `OneDrive\Business\05 Produktion` gespiegelt. Annahme: so.
17. **Laptop-Betrieb:** Der Laptop kennt nur Modern Standby (S0) und Ruhezustand. Für die geplanten Aufgaben muss er zu den Zeiten wach und am Netz sein. Zu welchen Uhrzeiten läuft er sicher? Annahme: Produktion nachts zwischen 02:00 und 06:00 Wiener Zeit, Veröffentlichung über Upload-Post serverseitig zu den Slot-Zeiten (Laptop darf dann aus sein).
18. **TTS-Stimme:** Gemini-TTS (günstig, Limits), ElevenLabs (teurer, beste Qualität) oder lokal (Kokoro, Piper; gratis, Qualität zu testen)? Annahme: Phase 1 Gemini-TTS Paid Tier oder lokal, Hörprobe an dich, dann Entscheidung.
19. **KI-Videoclips (Veo, Kling, Runway) oder nur programmatische Animation (HyperFrames/Three.js, FFmpeg) plus KI-Bilder?** Clips sind der größte Kostenfaktor und der größte Qualitätssprung. Annahme: Phase 1–2 ohne Clips, nur Animation und Bilder; Clips ab Phase 3 für den Hook (erste 5 Sekunden).

## E. Inhalt

20. **Militärkanal:** Ausschließlich historische Technik und öffentlich dokumentierte Systeme, keine Taktik-Anleitungen, nichts aus deinem Dienst, keine Uniform? Das ist meine Empfehlung wegen Monetarisierung und § 46 BDG. Annahme: ja, und der Kanal kommt erst in Phase 4.
21. **Beauty:** Hast du Zugang zu Produkten oder Affiliate-Programmen, oder bleibt es bei Wissen über Inhaltsstoffe? Ohne echte Produkte sind Empfehlungen angreifbar. Annahme: nur Wissen, keine Produkttests, Kanal erst in Phase 4.
22. **Brainrot:** Eigene wiederkehrende Figur (Charakter-Sheet) oder Formate ohne Figur (Simulationen, Battles wie beim Kollegen)? Annahme: Simulation ohne Figur, Kanal erst in Phase 4.
23. **Quellen für Claude-Workflows:** Darf ich echte Bildschirmaufnahmen deines Claude-Setups verwenden (ohne private Daten)? Das ist glaubwürdiger als KI-Oberflächen. Annahme: ja, aus einem eigenen Demo-Projekt.

## F. Gedächtnis und Zusammenarbeit

24. **Scutoria:** Läuft das neue Vorhaben neben Scutoria oder ersetzt es Scutoria? Es betrifft die Zeitplanung und die Übersicht. Annahme: daneben, Scutoria ruht.
25. **Soll der Fortschritt täglich im Log stehen** (Skill system-log, wie in START geregelt) und zusätzlich eine Wochenübersicht in `07 Auswertung`? Annahme: ja.
