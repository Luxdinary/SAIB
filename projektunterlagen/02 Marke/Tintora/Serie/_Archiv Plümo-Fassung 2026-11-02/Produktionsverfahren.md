# Produktionsverfahren: Plümo und die Insel der verlorenen Farben

Stand 02.11.2026, Entwurf von Claude. Die Angaben zu Werkzeugen, Preisen und Plattformregeln sind am 02.11.2026 geprüft; die Quellen stehen in Abschnitt 8. Was nicht geprüft werden konnte, ist als „nicht geprüft“ oder „nicht ermittelbar“ markiert. Es wurde nichts generiert. Die Higgsfield-Preise sind mit `get_cost` abgefragt; diese Abfrage reicht keinen Auftrag ein. Vor den Abfragen lag das Guthaben bei 182 Credits. Eine Kontrolle danach ergab ebenfalls 182 Credits.

## 1. Werkzeuge

| Aufgabe | Werkzeug | Geprüft am 02.11.2026 |
|---|---|---|
| Modellblätter, Schauplätze, Start- und Endbilder, Standbilder | Higgsfield, **Nano Banana Pro** (`nano_banana_pro`) | nimmt Referenzbilder an (`image_references`); Auflösung 1k, 2k, 4k; Formate u. a. 16:9 und 9:16; 2K kostet 2 Credits, 4K 4 Credits |
| Bewegte Shots | Higgsfield, **Kling 3.0 Omni Frames** (`kling_o3_flf`) | Startbild und Endbild; 3–15 s; Modi std, pro, 4k; Ton an oder aus; Formate 16:9, 9:16, 1:1; mehrere Einstellungen in einem Auftrag möglich (`multi_shots`) |
| Ausweichmodell für schwierige Shots | Higgsfield, **Seedance 2.5** (`seedance_2_5`) | nimmt Referenzbilder für die Identität an, deutlich teurer (Preise in `Kostenschätzung Pilot.md`) |
| Stimmen | **Gemini TTS** über die API (wie bisher, nur Google-Stimmen) | Mehrsprecher-Ausgabe nur mit **höchstens 2 Sprechern je Anfrage**; Deutsch unterstützt; 30 vorgefertigte Stimmen |
| Geräusche | selbst erzeugt wie bisher (`brands\brainrot\assets\sfx\`, eigene Arbeit) | vorhanden |
| Schnitt | per Skript (ffmpeg bzw. der vorhandene Renderer), aus einer Schnittliste | ob der vorhandene Renderer Querformat 16:9 und reine Videospuren ohne HyperFrames-Szenen kann, ist **nicht geprüft** |
| Musik | offen | keine Lizenzquelle gewählt (Regel: nur mit Nachweis in `08 Recht und Verwaltung\Lizenzen`) |

**Warum Kling 3.0 Omni Frames als Hauptmodell:**
- Bei ihm bestimmt man das erste und das letzte Bild selbst. So bleibt die Figur so, wie sie auf dem freigegebenen Startbild aussieht, und Anschlüsse zwischen Shots lassen sich planen (Endbild von 1-07 = Startbild von 1-10).
- Es lief am 30.10.2026 im Starter-Tarif für Scutoria.
- Es kostet in pro ohne Ton 1,25 Credits je Sekunde.

Ein Nachteil: Referenzbilder nimmt das Modell nicht an, die Gleichheit hängt also ganz am Startbild. Seeds gibt Higgsfield nicht heraus (Notiz vom 30.10.2026).

## 2. Figuren und Schauplätze gleich halten

### 2.1 Bibliothek vor der Produktion (Stufe 0)

1. **Stilfindung:** etwa 12 Testbilder in 2K mit Plümo vor einem Schauplatz, in zwei bis drei Stilrichtungen. Stefan wählt eine Richtung.
2. **Modellblätter je Figur**, im gewählten Stil, ohne Schrift im Bild, als 4K-Querformat:
   - Ansichten von vorn, von der Seite und von hinten
   - sechs Ausdrücke
   - für Funzel und Kasimir je eine bunte und eine graue Fassung
   - Plümos Modellblatt entsteht mit dem freigegebenen Charakterblatt `..\Plümo Charakterblatt (Entwurf).png` als Referenzbild
3. **Größenvergleich:** alle vier Figuren nebeneinander in einem Bild.
4. **Schauplatz-Referenzen:**
   - Farbbaum-Hügel am Abend bunt, bei Nacht und am grauen Morgen
   - Insel-Totale bunt und grau
   - Leuchtturm im Nebel
   - Echoberg von fern
   - Pfad
5. **Freigabe durch Stefan.** Erst die freigegebenen Bilder kommen in den Ordner `02 Marke\Tintora\Serie\Referenzen\` (anzulegen nach Freigabe) und gelten als Referenz. Abgelehnte Bilder werden nicht verwendet.

### 2.2 Feste Bausteine in jedem Bild-Prompt

Ein Prompt wird immer in derselben Reihenfolge zusammengesetzt:

1. **Stilblock:** wörtlich gleich in jedem Bild. Vorschlag, wird nach der Stilfindung angepasst:
   ```text
   STYLE: 2D anime-style children's animation still, clean confident line art, flat cel shading with one soft shadow tone, hand-painted watercolour backgrounds with soft edges, warm gentle lighting, rounded friendly shapes, no text, no letters, no logos, no watermark. Not photorealistic. Suitable for children aged 6 to 9: nothing scary, no sharp teeth, no blood.
   ```
   Keine Namen von Studios, Künstlern oder bekannten Figuren im Prompt. Das schützt vor Stilkopie und hält die Serie eigenständig.
2. **Farbzustand**, wörtlich nach dem Staffelzeitpunkt, z. B.:
   - vor dem Farbverlust: `COLOUR STATE: the whole world is fully colourful and saturated.`
   - nach dem Farbverlust: `COLOUR STATE: the whole world is desaturated blue-grey monochrome, EXCEPT Plumo who keeps his full lime-green and magenta colours.`
   - später ergänzt um die zurückgekehrten Farben, z. B. `... and EXCEPT everything yellow, which has its colour back.`
3. **Figurenblöcke** aus `Figuren.md`, wörtlich, nur für die Figuren im Bild; bei mehreren Figuren mit Größenverhältnis.
4. **Schauplatzsatz**, je Ort festgelegt (z. B. „Colour Tree Hill: a round grassy hill in the centre of a small island, a huge old tree with leaves in all rainbow colours …“). Er entsteht mit den Schauplatz-Referenzen.
5. **Bildinhalt** aus dem Storyboard: Einstellung, Handlung, Blickrichtung, Format, Lage der Figur im Bild.
6. **Referenzbilder** (bei Nano Banana Pro): das Modellblatt jeder Figur im Bild und das Schauplatzbild.

Die Bausteine 1–4 liegen als Textdateien neben den Referenzen. Ein kleines Skript setzt den Prompt je Shot aus der Storyboard-Zeile zusammen. So tippt niemand eine Figurbeschreibung neu, und Abweichungen sind ausgeschlossen.

### 2.3 Video-Prompts

Video-Prompts beschreiben **nur die Bewegung**, nicht das Aussehen, z. B. „Plumo hops forward twice with squash and stretch, his spring stem wobbles, camera stays still.“ Das Aussehen kommt aus dem Startbild.

Feste Zusätze:
- `no new characters appear`
- `no text`
- `keep character design exactly as in the first frame`

Zu jedem Shot steht im Storyboard, ob ein Endbild vorgegeben wird.

### 2.3a Erkenntnisse aus Stufe 0 (02.11.2026)

Einzelheiten in `Stufe 0\Ergebnis Stufe 0.md`.

- Im Starter gibt es Nano Banana Pro nur bis 2K (2.752 × 1.536 px). Für das Hochformat gibt es deshalb eigene 2K-Startbilder, kein Ausschnitt aus dem Querformat.
- Bei Videoaufträgen schlägt Higgsfield manchmal eine Vorlage vor. Der Auftrag läuft erst, wenn man sie mit `declined_preset_id` ablehnt.
- Bei mehr als 4 gleichzeitigen Bildaufträgen kam einmal der Fehler 429 (Ratenlimit). Höchstens 4 Aufträge je Stapel.
- Typische Fehler bei Plümo:
  - Stummelfüße
  - Rankenarm mit Fingern
  - Sommersprossen auf beiden oder auf der falschen Wange
  - Kugel statt Gummidrop

  Im Video bleibt er stabiler als in Standbildern, weil das Startbild ihn festhält.
- Im Hochformat setzt das Modell Figuren tiefer als verlangt. Im Prompt deshalb „between 25 and 55 percent of the picture height“ angeben.

### 2.4 Prüfliste je Bild und je Video (vor Übernahme)

- Plümo:
  - genau drei Federwindungen
  - Blatt magenta
  - Sommersprossen nur auf seiner rechten Wange (im Bild links)
  - keine Arme, keine Beine, keine Stummelfüße, kein Rankenarm, keine Finger am Blatt
  - Etikett nur auf dem Rücken
- Funzel: rote Flügeldecken mit genau einem weißen Punkt je Seite (wenn bunt); Licht nur im Hinterleib.
- Kasimir: rechte Schere größer; Teekanne weiß mit blauem Muster und Sprung am Ausguss (wenn bunt).
- Grisel: keine Zähne und keine Krallen; Laterne mit Messingrahmen; ab 2-09 mit Sprung im Glas.
- Farbzustand stimmt mit dem Staffelzeitpunkt überein.
- Keine Schrift, keine fremden Figuren, keine sechsten Finger oder Ähnliches.
- Im Hochformat: Figur zwischen y 300 und y 1300.

Ein Shot, der eine Prüfung nicht besteht, wird neu erzeugt (Kosten: Nachdrehfaktor in `Kostenschätzung Pilot.md`) oder als Standbild gelöst.

## 3. Stimmen

- **Je Satz eine Anfrage, eine Stimme.** Gemini kann in einer Anfrage höchstens zwei Sprecher. In vielen Szenen sprechen drei Figuren, dazu die Erzählerin. Jeden Satz einzeln zu erzeugen hat zwei Vorteile: Ein misslungener Satz lässt sich allein wiederholen, und Pausen und Timing setzt der Schnitt. Die Doku empfiehlt dafür, Rohdaten (PCM) statt WAV mit Kopfteil anzufordern oder den Kopfteil zu entfernen.
- **Feste Stilanweisung je Figur** (aus `Figuren.md`), wörtlich in jeder Anfrage, dazu die Regieanweisung der Zeile aus dem Drehbuch.
- **Stimmenwahl:** vor der Festlegung je Figur zwei bis drei Stimmen mit denselben drei Testsätzen probehören. Offen ist, ob eine Gemini-Stimme für Funzel kindlich genug klingt.
- **Modell:** Für neue Aufnahmen schlage ich `gemini-3.8-flash-tts` vor. Es ist laut Preisseite bis 31.12.2026 günstiger als das bisher genutzte `gemini-2.5-flash-preview-tts` (Preise in `Kostenschätzung Pilot.md`). Die Klangqualität beider Modelle ist nicht verglichen; der Test gehört zum Probehören.
- **Bezahlte Woche-1-Stimmen** der alten Zonkfruit-Videos (Puck, Fakten-Format) passen nicht zur Serie und werden hier nicht verwendet.
- **Englisch:** gleiche Stimmen, eigene Stilanweisung auf Englisch, eigener Text nach Freigabe des deutschen.

## 4. Ein Bild für zwei Sprachen

Damit die englische Fassung kein neues Bild braucht, gelten diese Regeln:

- **Keine Schrift im Bild.** Titel, Etikett-Text, „Ein paar Stunden vorher“ und „Fortsetzung folgt“ sind Einblendungen im Schnitt, je Sprache.
- **Keine Lippensynchronität.** Plümo, Funzel und Kasimir haben kleine Münder. Gesprochen wird in Shots mit allgemeiner Mundbewegung, in Rückansichten, in Reaktionsshots der Zuhörer oder aus dem Off. Bei Standbildern kommt ein Wechsel zwischen offenem und geschlossenem Mund als Zweitbild hinzu. Das ist im Anime-Stil üblich. Ein Higgsfield-Modell, das Lippen nach einer fremden Tonspur bewegt, habe ich nicht gefunden: Die Suche am 02.11. ergab nur Modelle mit eigener Tonerzeugung.
- **Länge:** Englische Sätze werden auf dieselbe Länge geschrieben; ein Shot darf in der englischen Fassung höchstens 1 s länger sein (durch Standbild am Ende).

## 5. Ablauf je Abschnitt und Schnitt

1. **Drehbuch** freigeben (Stefan).
2. **Stimmen** erzeugen, alle Sätze des Abschnitts (Kosten unter 0,05 USD, Abschnitt 3 der Kostenschätzung).
3. **Animatic:** Aus Startbildern und Standbildern plus Stimme entsteht ein Film mit festen Shotlängen.
   - Shots ohne fertiges Bild bekommen eine Platzhalterkarte mit der Shotnummer.
   - Stefan nimmt das Animatic ab. **Erst danach werden KI-Videos erzeugt**, und zwar in genau den Längen des Animatics. Das ist der größte Hebel gegen verschwendete Credits.
4. **Startbilder und Endbilder** erzeugen, prüfen (2.4) und freigeben.
5. **KI-Videos** erzeugen, erst 16:9, dann 9:16.
   - Vor jedem Stapel steht eine Kostenabfrage mit `get_cost`, dazu Stefans Freigabe des Stapels.
   - Höchstens ein Abschnitt je Stapel.
6. **Schnitt per Skript** aus einer Schnittliste (eine JSON-Datei je Abschnitt: Shot, Datei, Ein- und Auspunkt, Format, Markierung `nur_kurzclip`). Das Skript baut:
   - den Kurzclip 9:16: mit Rückblick, „Fortsetzung folgt“, Untertiteln, Logo und „KI-generiert“
   - den Abschnitt 16:9 für die Langfolge: ohne Rückblick und ohne „Fortsetzung folgt“
   - die Langfolge durch Aneinanderhängen der Abschnitte, mit Titel am Anfang und Schlusstafel ohne Endbildschirm-Elemente (Abschnitt 7)
7. **Ton:** Stimme, selbst erzeugte Geräusche, Musik erst nach Lizenzklärung; Lautheit −16 LUFS wie bisher.
8. **Abnahme durch Stefan**, dann Ablage nach `CLAUDE.md` (Ordner `05 Produktion\JJJJ-MM-TT Kurztitel`, Dateinamen mit Kanal und Format).

**Untertitel:** im Kurzclip wie bisher in Sinngruppen. In der Langfolge 16:9 als Untertiteldatei zum Hochladen, nicht ins Bild gebrannt. Sechsjährige lesen noch langsam, Untertitel dienen hier eher den Eltern und dem Ton-aus-Schauen.

## 6. Kennzeichnung

- **YouTube:** Offenlegen muss man laut YouTube „Inhalte, die echt zu sein scheinen“. Für nicht realistische Inhalte nennt die Hilfeseite ausdrücklich keine Offenlegungspflicht, mit dem Beispiel einer KI-animierten Rakete in einem ganz animierten Video. Die Serie ist eindeutig gezeichnet. **Trotzdem bleibt die Regel des Netzwerks: Jedes Video wird als KI-Inhalt gekennzeichnet.** Das heißt:
  - „KI-generiert“ im Bild, im Kurzclip dauerhaft, in der Langfolge im Vorspann und im Abspann
  - ein Satz in der Beschreibung
  - die Angabe beim Hochladen
  - die Metadaten wie bisher (`is_ai_generated`, `containsSyntheticMedia`)

  Laut YouTube erscheint das Label bei animierten Inhalten gegebenenfalls in der erweiterten Beschreibung, nicht im Player.
- **EU-KI-Verordnung Art. 50:** Plümo und seine Freunde sind erkennbar Zeichentrickfiguren und damit kein Deepfake. Grundlage ist die bisherige Einordnung in `02 Marke\Tintora\Vorlage Zonkfruit.md` Abschnitt 6 und die Leitlinien in `08 Recht und Verwaltung`; am 02.11. habe ich sie nicht neu geprüft.
- **Synthetische Stimme:** Die Einstiegszeile der Kurzclips heißt bisher „Synthetische Stimme · Quellen am Bildschirm …“. Für die Serie gibt es keine Quellen am Bildschirm mehr. Vorschlag für die neue Einstiegszeile: „Erfundene Geschichte · KI-Bilder · synthetische Stimmen“.
- **Lizenz der Bilder und Videos:** Higgsfield-Nutzungsbedingungen Abschnitt 4.4. Laut `08 Recht und Verwaltung\Lizenzen\Lizenzübersicht.md` gibt es keine Einschränkung der kommerziellen Nutzung, und die Rechte bleiben nach Kündigung. Je Shot steht eine Zeile in einer `LICENSE.md` mit Job-Nummer, wie bei Scutoria.

## 7. YouTube „speziell für Kinder“: was das bedeutet

**Einstufung:** YouTube nennt als Merkmale unter anderem:
- Kinder sind die beabsichtigte oder tatsächliche Zielgruppe
- kinderaffine Figuren
- kindgerechte Sprache
- Geschichten für Kinder

Kein Merkmal entscheidet allein. Eine Anime-Serie mit Plümo für 6- bis 9-Jährige erfüllt mehrere davon. **Ich halte die Einstufung „speziell für Kinder“ deshalb für zwingend.** Grund dafür sind die Vereinbarung mit der FTC und COPPA in den USA. Außerhalb der USA kann die Altersgrenze anders liegen; YouTube verweist auf die örtlichen Gesetze und gibt selbst keine Rechtsberatung. Bei einer falschen Einstufung drohen Folgen auf der Plattform und rechtliche Folgen.

**Was dann abgeschaltet ist** (YouTube-Hilfe „Funktionen, die bei Inhalten speziell für Kinder deaktiviert sind“, abgerufen 02.11.2026):

| Bereich | Betroffen |
|---|---|
| Einnahmen | **keine personalisierte Werbung**; YouTube schreibt selbst, dass man dadurch weniger Umsatz erzielen kann. Außerdem keine Kanalmitgliedschaft, kein Merchandise- und Ticketregal, keine Spenden-Schaltfläche, kein Super Chat und keine Super Sticker |
| Verlinkung | **keine Infokarten und keine Endbildschirme**. Ein Kurzclip kann also nicht per Endbildschirm auf die Langfolge oder auf Teil 2 verweisen. Auch kein Wasserzeichen im Video und keine Benachrichtigungsglocke |
| Zuschauer | **keine Kommentare**. Kein Speichern in „Später ansehen“ und keine Playlist für die Zuschauer, keine Wiedergabe im Miniplayer, kein Autoplay auf der Startseite |
| Kanal (wenn der ganze Kanal eingestuft wird) | zusätzlich keine Beiträge und kein „Frag Studio“ |

**Folgen für die Planung:**
- **Kurzclip → Langfolge** führt nur noch über den Kanal selbst. Gemeint sind die Kanalseite mit Abschnitten bzw. Playlists, die der Kanal anlegt, der Titel („Teil 2 von 36“), der Satz in der Beschreibung und „Fortsetzung folgt“ im Bild. Ob der Kanal bei Kinderinhalten eigene Playlists anlegen und in Shorts auf ein zugehöriges Video verweisen darf, steht in den gelesenen Seiten nicht. Das muss vor dem Start in YouTube Studio geprüft werden. Das Gleiche gilt für die Frage, ob Links in der Beschreibung klickbar bleiben.
- **Keine Aufforderung an Kinder**, zu abonnieren, zu klicken oder zu kaufen. Die YouTube-Qualitätsgrundsätze werten übermäßig kommerzielle Kinderinhalte als minderwertig. „Fortsetzung folgt“ ist erlaubt, „Abonniere jetzt!“ nicht.
- **Qualitätsgrundsätze für Kinderinhalte:**
  - YouTube empfiehlt hochwertige Kinderinhalte häufiger. Als hochwertig gelten etwa Freundschaft und Respekt, Neugier, Fantasie und Lebenskompetenzen mit klarem Handlungsbogen.
  - Als minderwertig gelten unter anderem schwer verständliche Videos ohne klaren Anfang, Mitte und Ende, die laut YouTube „häufig in großen Mengen“ oder automatisch erstellt werden. Dazu kommen Sensationelles und Irreführendes sowie scheinbar Lehrreiches mit falschem Inhalt.
  - Ein Kanal, der im Wesentlichen aus minderwertigen Kinderinhalten besteht, kann aus dem Partnerprogramm ausgeschlossen werden. Einzelne Videos können eingeschränkte oder keine Werbung bekommen.
  - Für die Serie heißt das: **wenige, sorgfältige Abschnitte statt Masse.**
- **Shorts:** Die gelesene Seite zu den deaktivierten Funktionen erwähnt Shorts nicht. Wie sich die Einstufung auf Shorts-Funktionen und die Shorts-Umsatzbeteiligung auswirkt, ist **nicht ermittelt**.
- **TikTok und Instagram:** Beide setzen laut Nutzungsbedingungen ein Mindestalter von 13 Jahren voraus. Das habe ich nur über Suchergebnisse gefunden, unter anderem klicksafe.de; die Primärquelle ist nicht geöffnet.

## 7a. Plattformen (Entscheidung Stefan, 02.11.2026)

Die Serie erscheint auf **allen drei Plattformen**: YouTube, TikTok und Instagram.

| Plattform | Einstufung und Ansprache | Was das praktisch heißt |
|---|---|---|
| YouTube (Shorts und Langfolgen) | **„Speziell für Kinder“**: einzeln je Video oder für den ganzen Kanal, siehe Abschnitt 7 | Einschränkungen nach Abschnitt 7; Verlinkung nur über Kanalseite, Titel und Beschreibung |
| TikTok, Instagram Reels | **Familien- und Animationsserie.** Es gibt keine direkte Ansprache von Kindern unter 13. | siehe Regeln unten |

Regeln für TikTok und Instagram:
- **Titel, Beschreibung und Hashtags** richten sich an Familien und an Leute, die Animation mögen, nicht an Kinder. Beispiele:
  - erlaubt: „Neue Folge unserer Animationsserie“ oder „Zum gemeinsamen Anschauen“
  - nicht erlaubt: „Hey Kinder!“, „Für dich, wenn du 7 bist“
  - nicht erlaubt: Hashtags, die gezielt Kinder ansprechen, etwa `#fürkinder` oder `#kidsvideo`
- **Kein Aufruf zum Mitmachen, der sich an Kinder richtet.** Also keine Fragen wie „Schreib in die Kommentare, welche Farbe du magst!“ und keine Gewinnspiele. Erlaubt ist eine neutrale Frage an alle, etwa „Welche Farbe kommt als Nächstes zurück?“.
- **Kommentare:**
  - Wenn die Plattformen es zulassen, werden sie gefiltert oder eingeschränkt.
  - Antworten erst ab Phase 3 (Regel vom 29.10.2026).
  - Antworten nie an erkennbar junge Nutzer und nie mit der Bitte um persönliche Angaben.
  - Welche Kommentarfilter TikTok und Instagram dafür bieten, ist **nicht geprüft**.
- **Inhalt gleich, Begleittext anders.** Das Video ist auf allen drei Plattformen derselbe 9:16-Kurzclip. Nur Titel, Beschreibung und Hashtags unterscheiden sich je Plattform. In `Veröffentlichung.md` je Abschnitt gibt es deshalb drei Textblöcke, nicht einen.
- **Kennzeichnung:** wie Abschnitt 6, auf TikTok und Instagram mit den KI-Kennzeichen der Plattformen (`is_aigc` bzw. das KI-Label von Instagram) wie bisher im Netzwerk.
- **Profiltext von @zonkfruit.tv** auf TikTok und Instagram: im selben Ton, an Familien gerichtet. Das bisherige Profilpaket in `03 Kanäle\Zonkfruit\Profilpaket.md` beschreibt noch das Fakten-Format und muss vor dem Start angepasst werden; das ist **noch nicht gemacht**.
- **Offen und nicht geprüft:**
  - Gibt es auf TikTok oder Instagram eigene Einstellungen oder Pflichten für Inhalte, die auch Kinder ansprechen, zum Beispiel ein Altershinweis beim Hochladen?
  - Was sagen die Werberichtlinien für Kinderinhalte bei späteren Kooperationen?
  - Beides vor dem ersten Post klären.
- **Österreich:** Ob ein YouTube-Kanal mit Kinderserie bei der KommAustria als audiovisueller Mediendienst auf Abruf anzuzeigen ist und welche Werberegeln für Kinder dann gelten, ist **nicht geprüft**. Vor dem Start klären, am besten zusammen mit der offenen Frage zu Gewerbe und Steuerberatung.

## 8. Quellen (abgerufen am 02.11.2026)

| Inhalt | Quelle |
|---|---|
| Kriterien „speziell für Kinder“, COPPA und FTC, Altersgrenze außerhalb der USA | support.google.com/youtube/answer/9528076 (deutsch) |
| Deaktivierte Funktionen, weniger Umsatz durch fehlende personalisierte Werbung | support.google.com/youtube/answer/9527654 (deutsch) |
| Qualitätsgrundsätze für Kinder- und Familieninhalte, Folgen für YPP und Werbung | support.google.com/youtube/answer/10774223 (deutsch) |
| Offenlegung veränderter oder synthetischer Inhalte, Ausnahme für nicht realistische Animation, Ort des Labels | support.google.com/youtube/answer/14328491 (deutsch) |
| Gemini TTS: höchstens 2 Sprecher je Anfrage, Modelle, Deutsch, 30 Stimmen, PCM-Hinweis | ai.google.dev/gemini-api/docs/speech-generation |
| Gemini TTS-Preise, 25 Audio-Token je Sekunde | ai.google.dev/gemini-api/docs/pricing |
| Higgsfield-Modelle, Parameter und Creditpreise | Higgsfield-MCP-Server (`models_explore`, `generate_* get_cost`, `balance`), 02.11.2026 |
| Higgsfield-Tarifpreise (Starter, Plus, Ultra) | higgsfield.ai/pricing laut `01 Idee und Strategie\Übergabebericht 2026-10-30.md` (Abruf 29./30.10.2026); am 02.11. lud die Seite ohne Preise (per Skript nachgeladen) und war daher nicht erneut prüfbar |
| Mindestalter TikTok und Instagram 13 Jahre | Suchergebnisse u. a. klicksafe.de/en/mindestalter; Primärquelle nicht geöffnet |
| Lizenz Higgsfield-Ergebnisse | `08 Recht und Verwaltung\Lizenzen\Lizenzübersicht.md` (Nutzungsbedingungen 4.4) |
