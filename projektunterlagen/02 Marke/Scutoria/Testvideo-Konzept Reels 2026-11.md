# Scutoria Reels – Testvideo-Konzept (November 2026)

Stand 02.11.2026, Claude (Sitzung Scutoria Reels). Grundlage: `01 Idee und Strategie\Neustart Testvideos 2026-11-02.md`, Abschnitt 4 und 5; Codex-Bericht 01.11., Abschnitt 3. Entwurf an die Hauptsitzung, kein Rendern ohne Go. Das Konzept der YouTube-Sitzung liegt daneben in `Testvideo-Konzept 2026-11.md`.

## Thema

**„Die Mail vom Chef, der dringend überweisen lässt“** (Konzeptplan Nr. 32, Kalender `ai_security-20261110-1-de`, Reihe „Was tust du?“). Codex nennt genau diese Situation: die falsche Zahlungsanweisung im kleinen Betrieb. Sprechtext, Quellen (Polizei Berlin, CEO-Fraud; FBI IC3, Warnung vom 11.09.2024) und Kennzeichnung bleiben wie geprüft. Ablauf: Mail kommt an → du prüfst → A/B/C → Wahl B durchgespielt → Rückruf als der eine Schritt → „Schon überwiesen?“ → Abschluss.

**Stimme:** Die Flash-Aufnahme dieses Texts liegt vor (Charon, 71,9 s, `storage\direction\voice_ai_security-20261110-1-de_F2_gemini.wav`). Plan: wiederverwenden, also **0 Gemini-Anfragen**. Nur wenn sich der Text ändert, höchstens 3 Flash.

## Bildkonzept: „Du sitzt am Platz“

Ich-Perspektive aus der Buchhaltung eines kleinen Elektrobetriebs. Bei jedem Bild sitzt der Zuschauer selbst auf dem Stuhl: Hände ja, Gesichter nie. Es ist immer dasselbe Büro: B1a ist die Referenz für alle weiteren Bilder. Licht: später Nachmittag mit natürlichem Fensterlicht, gedämpftes Navy und Grau, Scutoria-Blau nur als kalter Lichtakzent an der Tischkante. Die Mail, die Zahlungsmaske und die Uhrzeit setzt der Renderer als scharfe Ebene auf den leeren Bildschirm im Foto. Im KI-Bild steht keine Schrift.

**Stand 02.11., 23:40: alle Bilder erzeugt und geprüft** (Ordner `C:\Automation\faceless-network\brands\ai_security\assets\higgsfield\test2611\`, Nachweis in `LICENSE.md` derselben Bibliothek, Abschnitt „Testvideo 2026-11 (9:16)“).

| Nr | Datei | Bild | Szene im Video | Bewegung |
|---|---|---|---|---|
| B1 | `B1a.png` | Blick vom Stuhl über den Schreibtisch, Monitor frontal, Bildschirm leer hell, Hände auf der Tastatur, Telefon, Ordner, Becher | Hook: Mail fährt auf den Bildschirm | langsames Heranfahren, Mail gleitet ein |
| B2 | `B2.png` | Nah: Monitor, rechte Hand an der Maus | Prüfen: Lupe auf Absender, Thema, Konto | drei Lupen-Zooms, harte Schnitte |
| B3 | `B3.png` | Flur, Bürotür des Chefs halb offen, leerer Platz, Mantelhaken leer | „Name des Chefs“, der Chef ist nicht da | seitlicher Schwenk |
| B4 | `B4.png` | Analoge Wanduhr ohne Ziffern, kurz vor fünf | Denkpause nach „Entscheide dich jetzt“ | Standbild, Zeiger läuft |
| B5 | `B5b.png` | Zeigefinger auf der Maus kurz vor dem Klick, Bildschirm leer | Wahl A und Zeitleiste „Du überweist“ | Druck-Zoom auf den Klick |
| B6 | `B6c.png` | Montagmorgen: derselbe Tisch, Monitor aus, Kaffee dampft, Autoschlüssel, Jacke über dem Stuhl | Zeitleiste „MO 08:30“ | Weißblitz-Schnitt |
| B7 | `B7.png` | Hand hebt den Hörer des Tischtelefons ab | Der eine Schritt: Rückruf | Hörer-Bewegung, Stempel „Rückruf“ |
| B8 | `B8.png` | Hand hält Smartphone, Bildschirm dunkel, Bankkarte ohne Aufdruck | „Schon überwiesen?“: Bank anrufen | ruhiger Zoom |
| B9 | `B9.png` | Derselbe Platz am Abend, Monitor aus, Schreibtischlampe | Abschluss | Ausblenden, Regelkarte |

Verworfen und liegen gelassen: `B1b` (zweite Variante), `B5` (Herstellerlogo am Monitor, anderer Tisch), `B6` (Spiegelung eines Stativs im Monitor), `B6b` (Pseudo-Schrift auf Ordnerrücken). Hinweis: Tastaturen und das Tastenfeld des Telefons (B7) zeigen normale Tastenbeschriftung, aber keine lesbare Information.

**Credits Bilder: 13 × 2 = 26** (Preis mit `get_cost` geprüft: Nano Banana Pro 9:16 2K 2 Credits).

**Kling-Clips** (erst, wenn die Hauptsitzung meldet, dass Kling läuft; je 8 s, Omni Frames pro, 10 Credits): B1 Heranfahren, B4 Zeiger läuft, B7 Hörer abheben, B6 Licht geht an, B3 Tür schwingt. **5 × 10 = 50 Credits.** **Gesamt dann 76 von 100 Credits**, Rest 24 als Reserve.

## Variation (mindestens drei Szenentypen, eigene Bewegungen)

1. **Foto mit Bildschirm-Einblendung:** Mail, Zahlungsmaske und Uhrzeit sitzen im realen Monitor.
2. **Lupe:** drei kreisrunde Detail-Zooms auf das Foto mit Urteil-Chip („wirkt echt“, „plausibel“, „erklärbar“).
3. **Entscheidung im Standbild:** Das Bild friert ein und wird grau, A/B/C kommen als Karten, die Uhr B4 tickt.
4. **Fotomontage als Zeitleiste:** Wahl B in vier harten Schnitten (B2 → B5 → B4 → B6), Zeitstempel als Stempel.
5. **Handlung:** Hörer abheben (B7) mit Stempel „Rückruf“; A und B werden durchgestrichen.

Wechsel: Wisch nach links bei neuen Fakten, harter Schnitt in der Zeitleiste, Weißblitz beim Montag.

## Was es von den anderen Marken unterscheidet

Keine andere Marke erzählt aus der Ich-Perspektive mit eigener Entscheidung des Zuschauers. Dewlane zeigt Produktnahaufnahmen, Revlore Mechanik, Gigastruct Baustellen und Luftbilder, Suitwerk Stoff, Frontlore Rekonstruktionen, Gritwerk Versuche, Promptwerk echte Bildschirmläufe, Tintora Anime. Scutoria YouTube bleibt in der gezeichneten Welt mit Figuren (Konzept nebenan). Nur die Scutoria-Reels setzen den Zuschauer selbst an einen realen Arbeitsplatz mit echter Uhrzeit und stoppen das Bild, bevor er wählt.

## Ton-Cues (Klangfarbe: Büro, trocken, nah)

Die Namen folgen, wo möglich, denen der YouTube-Sitzung, damit die gemeinsame Tonebene eine Liste hat.

| Stelle | Geräusch |
|---|---|
| Mail erscheint (Hook) | `mail_in` (leiser Eingangston) |
| Jede Lupe | `click` plus `whoosh_soft` |
| Urteil-Chip | `tick` |
| Standbild der Entscheidung | kurzes Bild-Stopp-Geräusch, danach nur `clock_tick`, Musik aus |
| A/B/C-Karten | `pop` je Karte |
| Zeitleisten-Schnitte | `whoosh_soft`, Zeitstempel als `stamp_soft` |
| Montag (Weißblitz) | `thud_low` |
| Rückruf | Hörer abheben, ein Freizeichen |
| Durchstreichen A und B | `pen_strike` |
| Abschluss | Musik kommt zurück und klingt aus |

Musikbett: ruhiges, dunkles Pad ohne Schlagzeug, unter der Stimme abgesenkt, in der Denkpause ganz aus. Quelle nur mit Lizenznachweis in `08 Recht und Verwaltung\Lizenzen`; die Auswahl übernimmt die Hauptsitzung für den Renderer.

## Stand 03.11.2026: Clips, Szenen, Trockenlauf

- **Freigaben der Hauptsitzung vom 02.11. nachts:** Konzept in Ordnung, Menschen ohne Gesicht erlaubt, Kling frei innerhalb der Kappe.
- **Kling-Clips:** 5 × 10 = 50 Credits, alle in unter 15 Minuten fertig und an je fünf Einzelbildern geprüft: `C1_typing` (Hook), `C2_mouse` (zoomt leicht, deshalb nur in der Montage, ohne Einblendung), `C3_corridor` (Tür schwingt auf, leeres Büro), `C4_monday` (Dampf, Morgenlicht; die letzte Sekunde mit grünem Lichtfleck wird nicht gezeigt), `C5_phone` (Hörer abheben). **Higgsfield gesamt: 26 + 50 = 76 von 100 Credits.**
- **Szenen:** neue Szenentypen in `brands\ai_security\buero.py` (`sb_screen`, `sb_lens`, `sb_freeze`, `sb_montage`, `sb_action`), eingebunden über `scenes.py`. Die Fotos und Clips legt die Marken-Ebene (LAYER) unter die Szenen; am gemeinsamen Code ist nichts geändert.
- **Plan:** `data\direction\ai_security-20261110-1-de.T1.json`, gebaut mit `brands\ai_security\build_test2611.py` aus F2. Text und Quellen sind unverändert, die Flash-Stimme ist wiederverwendet: **0 Gemini-Anfragen.**
- **Ton-Cues:** 38 Stellen im Plan (`cues` je Beat). Beim Bauen werden sie aufgelöst nach `storage\direction\ai_security-20261110-1-de-T1\project\sound_cues.json` (Sekunde, Geräuschname, Beat, Wortanker) für die gemeinsame Tonebene.
- **Trockenlauf ohne Rendern (03.11.):** Direction-Checks ok; HyperFrames Lint 0, Layout 0, Gestaltung 0 Hinweise; `overlap_check`: keine Überschneidungen, keine zu kleine Schrift. Sichtbilder: `Testvideo Reels – Trockenlauf T1 (Sichtbilder).jpg` hier im Ordner. Länge wie F2: 74,7 s.
- **Finaler Render 03.11. (Go der Hauptsitzung):** mit Tonebene (Palette tech, Bett prozedural „dark“, 36 Plan-Cues in `layout.sound_cues`, Musik aus/an und Freizeichen gibt es dort nicht und fehlen), Status VALIDATED, Prüfbericht 29 Befunde ohne Fehler, overlap_check sauber, 74,7 s, -16,1 LUFS. Export: `05 Produktion\Scutoria\2026-11\2026-11-10 Testvideo Chef-Mail\`. Wartet auf Stefans Urteil; keine englische Fassung vorher.
- **Freigabe und Neufassung (03.11., nachmittags):** Stefan hat freigegeben („Alle freigeben“), mit der Korrektur „Effekte zu laut“. Die deutsche Neufassung T3 nutzt Sweeps bei -19 dBFS, gleichzeitige Cues sind entzerrt, der Geräusch-Stem liegt bei -16,9 dBFS; sie steht im selben Ordner wie T1. Die englische Fassung T3 hat dieselben Szenen und Cues und brauchte 1 Flash-Anfrage, Ordner `2026-11-10 Testvideo Chef-Mail EN`. Beide sind VALIDATED. Gebaut werden beide mit `brands\ai_security\build_test2611.py de en`.
- **Früher offen:** finaler Render und Export erst nach Go der Hauptsitzung und wenn die Tonebene steht (erledigt). Eine echte Denkpause in der Stimme gibt es weiterhin nicht; Uhr und Hinweis erscheinen deshalb schon bei „Nummer“.
