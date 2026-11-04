# Übergabebericht: KI-Kurzvideo-Netzwerk (Business „Video und Social Media")

Stand: 30.10.2026, 16:05 (Wien). Verfasst von Claude (Claude Code, Desktop-App) für eine nachfolgende KI ohne Zugriff auf den bisherigen Chat. Zeitraum der Arbeit: 29.10.2026 ab etwa 21:30 bis 30.10.2026 nachmittags (Wiener Zeit). Alle Angaben stammen aus dem Chat, aus Dateien auf Stefans Laptop und aus den zitierten Quellen. Wo etwas unsicher ist, steht es ausdrücklich dabei. Es stehen keine Passwörter, Schlüssel oder Tokens in diesem Bericht, nur ihre Ablageorte.

Hinweis zur Zeit: Der Laptop läuft in Beiruter Zeit (Stefan ist im Einsatz). Datei-Zeitstempel im Explorer sind daher eine Stunde später als Wiener Zeit (seit Ende der Sommerzeit am 25.10.2026: Beirut UTC+2, Wien UTC+1). In diesem Bericht ist jede Uhrzeit Wiener Zeit, sofern nicht anders vermerkt.

---

## 1. Ziel und Zweck des Projekts

### 1.1 Was gebaut wird

Ein Netzwerk aus neun getrennten Nischenmarken, die jeweils auf TikTok, Instagram Reels und YouTube Shorts KI-erzeugte Erklärvideos von 65 bis 90 Sekunden veröffentlichen, auf Deutsch und Englisch. Die Produktion soll so weit wie möglich automatisch laufen: Claude Code plant Themen einen Monat im Voraus, recherchiert mit Quellen, schreibt Skripte, lässt sie vertonen, rendert die Videos am Laptop und übergibt sie einem Upload-Dienst, der sie zu festen Uhrzeiten veröffentlicht. Statistik fließt zurück in die Themenplanung.

### 1.2 Hintergrund

- Stefan Dallinger, Wohnsitz Österreich, Angehöriger des Österreichischen Bundesheeres, derzeit im Auslandseinsatz (Zeitzone Beirut). Er hat ein bestehendes Business „Scutoria" (Ratgeber und Toolkits zu Informationssicherheit, Compliance und KI für kleine Betriebe; Website scutoria.com; eigener Ordner `C:\Users\Stefa\OneDrive\scutoria` mit eigener `CLAUDE.md`).
- Auslöser: Ein Kollege von Stefan betreibt mehrere TikTok-Kanäle mit KI-Videos (5 bis 7 Kanäle, je auf TikTok, Instagram, YouTube Shorts; Nischen u. a. Baustellen/Megakonstruktionen und Motorentechnik; 3 Videos pro Tag und Kanal; Themen einen Monat im Voraus; Upload über einen Dienst mit API-Schlüssel). Dessen System ist als HTML-Bauplan „Die Faceless-Maschine" dokumentiert (liegt im Projekt, siehe Abschnitt 5).
- Stefan hat sechs YouTube-Videos zum TikTok Creator Rewards Program als Ausgangspunkt genannt (Tinus Klauser, Maurice KI Experte, German_Tank_, BerkanViral zweimal, Taro Creates Playlist). Deren Volltranskripte konnten in der Grok-Recherche nicht geladen werden (YouTube Bot-Check, HTTP 429); ausgewertet wurden nur Titel und Beschreibungen.

### 1.3 Stefans Motivation (aus seinen Aussagen)

- Zusätzliches Einkommen; ausdrücklich: „Ich will das durchziehen und so automatisiert wie möglich."
- Getrennte Kanäle pro Nische, damit Werbepartner gezielt pro Nische buchen können (Idee des Kollegen, von Stefan übernommen).
- Ursprünglich Ziel TikTok Creator Rewards (Videos über 1 Minute). Dieses Programm ist in Österreich nicht verfügbar (siehe Abschnitt 6); Stefan will alles so aufbauen, dass Rewards aktiviert werden können, sobald sie offiziell verfügbar sind.
- Das Vorhaben läuft neben Scutoria (Stefan, 29.10.2026); Scutoria ist zugleich eine der neun Videomarken.

---

## 2. Stefans Anforderungen, Vorgaben, Regeln und Präferenzen

### 2.1 Globale Regeln (aus `C:\Users\Stefa\.claude\CLAUDE.md` und Google Drive › Claude-Gedächtnis › `00 START.md`)

- Immer auf Deutsch antworten. Stil: menschlich, modern, wissenschaftlich, höflich, präzise, ehrlich. Keine Emojis.
- „Nichts erfinden, auch nichts Kleines. Nicht Belegtes heißt ‚nicht ermittelbar' mit Grund. Rückfragen sind erwünscht."
- Keine Rechts-, Anlage- oder medizinische Beratung; Entscheidungsgrundlagen mit dem stärksten Gegenargument.
- Claude löscht nichts. Was weg soll, kommt nach `C:\Users\Stefa\Documents\_zum_loeschen\<Datum Thema>` (in Google Drive in den Ordner `_zum_loeschen`). Unwiderrufliches klickt Stefan.
- Keine Konto-, Vertrags-, Ausweis- oder Versicherungsnummern und keine Zugangsdaten im Gedächtnis, im Log oder in Dateinamen.
- Das Gedächtnis liegt in Google Drive › Claude-Gedächtnis (Markdown): `00 START.md` (Einstieg), `Übersichten` (gültiger Stand je Projekt), `Hintergrund`, `Vorlagen`, `Claude-System` (Log), `Archiv`. Inhalte (Dateien) liegen nur in OneDrive (`C:\Users\Stefa\OneDrive`), nie in Google Drive; Gedächtnis nie lokal. `OneDrive\Notizen` und `C:\Obsidian` sind aufgelöst, nie lesen oder anlegen.
- Übersicht ändern: Der Google-Drive-Konnektor kann Dateien nicht bearbeiten. Ablauf: aktuelle Fassung lesen; vollständige neue Fassung mit demselben Titel in `Übersichten` anlegen (`create_file`, `contentMimeType` `text/markdown`, `disableConversionToGoogleType` `true`, oben „Stand: TT.MM.JJJJ, HH:MM (Wien)"); alte Fassung mit `update_file` nach `Übersichten › Frühere Fassungen` verschieben und Titel um „ (bis JJJJ-MM-TT HH-MM)" ergänzen. START und Hintergrund-Dateien genauso, alte Fassung nach `Archiv`.
- Am Ende jedes Chats ein Log-Eintrag in Google Drive › Claude-Gedächtnis › Claude-System › Log-Eingang (Ordner-ID `1V22KU5F65VYe2dl4NK27-phR6tSpSHcO`), Titel `JJJJ-MM-TT HH:MM Projekt` (Wien), Inhalt: entschieden/erledigt, offen. Bestehende Logs nie ändern.
- E-Mails nur auf ein ausdrückliches Sendewort; Termine nur auf klaren Auftrag.
- Zeit: im Einsatz Asia/Beirut, zuhause Europe/Vienna; Termine, Dateinamen, Log-Titel in Wiener Zeit.
- Wird eine Aktion vom System abgelehnt: nicht anders erzwingen, Stefan melden.
- Die Ordnerstruktur in OneDrive ist gewollt; Änderungen nur nach Vorschlag und Freigabe.

### 2.2 Regeln für diesen Arbeitsordner (`C:\Users\Stefa\OneDrive\Business\CLAUDE.md`, angelegt 29.10.2026)

Hier liegen nur Inhalte; der gültige Stand steht in der Übersicht in Google Drive. Ordner `00 Eingang` bis `08 Recht und Verwaltung` (siehe Abschnitt 5). Keine Zugangsdaten in Dateien. Musik, Bilder, Clips nur mit geklärter Lizenz, Nachweis in `08 Recht und Verwaltung\Lizenzen`. Entscheidungen sofort in die Übersicht in Google Drive.

### 2.3 Inhaltliche Vorgaben zum Vorhaben (Stefan, möglichst wörtlich)

Aus dem ursprünglichen Brief (von Grok für ChatGPT formuliert, von Stefan bestätigt):
- „Wohnsitz Österreich. Das TikTok Creator Rewards Program ist hier derzeit nicht verfügbar. Keine Umgehung per VPN oder fremdem Wohnsitz; alles so aufbauen, dass Rewards aktivierbar sind, sobald sie offiziell verfügbar werden."
- „Nebenbeschäftigung ist abgeklärt. KI-Inhalte werden auf allen Plattformen gekennzeichnet."
- „5 bis 7 Kanäle mit je eigener Nische, jeweils auf TikTok, Instagram Reels und YouTube Shorts. Alles zweisprachig, Deutsch und Englisch. Pro Kanal eine eigene Gmail-Adresse. 3 Videos pro Tag und Kanal, jeweils über 1 Minute lang, vollständig automatisiert. Themenplanung jeweils 1 Monat im Voraus. Getrennte Kanäle, damit Werbepartner gezielt pro Nische buchen können."
- Nischen: „KI und Sicherheit; Beauty und Schönheitsprodukte; Claude-Workflows und Prompts; Kleidungsstil und Anzugarten; Brainrot; Motivation und Selbsthilfe; Sicherheit und Militär (Taktiken und Techniken, nur öffentlich zugängliche Inhalte). Zum Vergleich: Baustellen und Megakonstruktionen, Motorentechnik."
- Regeln für Antworten: „Nichts erfinden. Jede Zahl mit Quelle und Datum. Nicht Belegbares als ‚nicht ermittelbar' markieren, mit Begründung. Bei jeder Einschätzung das stärkste Gegenargument nennen."

Weitere Aussagen Stefans im Chat:
- Zum VPN (gegenüber Grok): „Gut dann mache es mittels eines VPNs erstmal bis auf Zwischenlösung." Grok lehnte ab. Stefan danach: „Okay du hilfst mir nicht beim VPN verstehe ich. Trotzdem so einrichten und beschreiben, dass man es dann offiziell machen kann." Seitdem gilt: kein VPN, kein fremder Wohnsitz.
- Rechner: „Ich will es hier auf meinem Laptop machen, nicht auf meinem Mac Mini." Später: Claude-Konto „grundsätzlich hätte ich es gern anfangs im bestehenden Claude-Konto, für die Zukunft kann man das auf meinen alten Mac mini M1 2020 verlegen, aber zunächst jetzt hier am PC."
- „Anmerkungen von mir: Ich will das durchziehen und so automatisiert wie möglich. Überprüfe alles gegen. Mache einen Plan bzw. Ablaufplan. Erstelle einen Fragenkatalog, falls du Fragen an mich hast. Ziel sollte es sein, komplett fertige Videos und Produkte für den Upload für TikTok, YouTube und Instagram."
- Zum Vorgehen bei den Videos: „Wir machen jedes Demo-Video für jeden Channel mal fertig, nacheinander pro Abschnitt."
- Zu Higgsfield: „Mein Vorgehen wäre jetzt gewesen, mittels Higgsfield eine Vorlage einmalig zu erstellen bzw. ein Design mit den Animationen und Sonstigem … Also konkret: wir arbeiten jetzt für jeden Channel eine Vorlage aus, einmal nur mit Claude Code. Danach machen wir eine Vorlage mit Higgsfield und das gleichen wir dann ab, und es soll dann nur mit Claude Code funktionieren." Danach: „Machen wir nur mal eine Marke."
- Zu Scutoria: „Zusatz, der nur für Scutoria gilt: Hier gibt es schon Design im Hinblick auf Logos etc."
- Anrede im Scutoria-Video: „Du" (30.10.2026), abweichend vom Scutoria-Markenbuch, das „Sie" vorschreibt.

### 2.4 Antworten auf den Fragenkatalog (Stefan, 29.10.2026, wörtlich in Kurzform)

| Nr. | Frage | Antwort Stefan |
|---|---|---|
| 1 | Startkanäle | „Eigentlich alle Marken fertig auf einmal (wichtig: überprüfe nochmal die Namen und finde bessere Namen bzw. Marken), aber ja, beginne mit Promptpilot und Scutoria" |
| 2 | Sprache zuerst | „Zuerst Deutsch, aber parallel Englisch" |
| 3 | Konten je Sprache | „Konto je Marke" (DE und EN auf demselben Konto) |
| 4 | Takt | „12:00, 14:00, 18:00" |
| 5 | Zeit für Freigaben | „2 h" pro Tag |
| 6 | Freigabe | „Automatisch" |
| 7 | Ohne Netz im Einsatz | „Puffer" |
| 8 | Kommentare beantworten | „Ja" |
| 9 | Budget | „50 € im Monat" |
| 10 | Gewerbe, Steuerberatung | „noch nicht" |
| 11 | Impressum | „Scutoria-Adresse" |
| 12 | Gmail-Struktur | „Je Marke eine Gmail-Adresse, YouTube, TikTok, Instagram Kanal" |
| 13 | Markennamen | „Mache eine Recherche und Analyse dahingehend" |
| 14 | Speicher C: | „C: reicht, ich lösche etwas" |
| 15 | Claude-Konto | bestehendes Konto, später eventuell Mac mini M1 |
| 16 | Projektordner außerhalb OneDrive | „ja" |
| 17 | Laufzeit Laptop | „Laptop kann 24/7 laufen" |
| 18 | Stimme | „Gemini Stimme" |
| 19 | KI-Clips erst ab Phase 3 | „ja genau, perfekt" |
| 20 | Militärkanal nur historisch, nichts Dienstliches | „ja genau" |
| 21 | Beauty | „Noch nicht, aber ich ziele darauf ab, dass man hier Werbung schalten kann für Beauty-Produkte" |
| 22 | Brainrot | „eigener Charakter" |
| 23 | Echte Bildschirmaufnahmen für Claude-Workflows | „ja" |
| 24 | Verhältnis zu Scutoria | „neben" |
| 25 | Täglicher Log, Wochenbericht | „ja" |

Weitere Kurzentscheidungen: Markennamen aus der Namensrecherche übernommen („Namen übernehmen", 30.10.2026). Gemini-Schlüssel, der kurz in `.env.example` stand: „lasse ich so" (Stefan erneuert ihn nicht).

### 2.5 Was Stefan ausdrücklich nicht will oder was ausgeschlossen ist

- Kein VPN, kein vorgetäuschter Wohnsitz für TikTok Rewards.
- Keine unbelegten Zahlen, keine erfundenen Quellen, keine Schätzungen ohne Kennzeichnung.
- Nichts aus Stefans Dienst im Militärkanal, keine Uniform, keine Taktik-Anleitungen (§ 46 BDG Verschwiegenheit).
- Keine Videos, die wie animierte Folien wirken (seine Kritik am ersten Testvideo, bestätigt durch zwei externe Analysen).
- Für Scutoria: das vorhandene Markendesign verwenden, keine eigene Palette.

---

## 3. Chronologischer Verlauf (Wiener Zeit)

### 29.10.2026, abends: Arbeitsumgebung

1. Stefan: neue Business-Idee mit Videoinhalten und Social Media auf mehreren Kanälen; „erstelle schon mal eine passende Umgebung".
2. Claude las Google Drive › `00 START.md`, die Landkarte `OneDrive — Aktenschrank.md` und die archivierte Notiz `Hintergrund › Business.md` (dort steht: am 18.10.2026 „einziges Business ist Scutoria"; Prüfpunkt Nebenbeschäftigung § 56 BDG).
3. Claude legte in `C:\Users\Stefa\OneDrive\Business` die Ordner `00 Eingang` bis `08 Recht und Verwaltung` an, Vorlagen (`Konzept.md`, `Markenstimme.md`, Kanalprofil-Vorlage, Video-Vorlage mit `Skript.md` und `Veröffentlichung.md`, `Ideenspeicher.md`, `Redaktionsplan.csv`) und eine `CLAUDE.md`.
4. Gedächtnis: neue Übersicht `Übersicht — Business (Video und Social Media).md` in Google Drive; Landkarte OneDrive um `Business\` ergänzt (alte Fassung ins Archiv). Auf Stefans Freigabe („Ja, eintragen") wurde das Projekt in die Projekttabelle von `00 START.md` eingetragen (neue Fassung, alte nach Archiv als „00 START (bis 2026-10-29 21-40).md").

### 29.10.2026, spät: Unterlagen, Faktencheck, Konzept

5. Stefan lieferte drei KI-Berichte und den Bauplan des Kollegen: (a) ChatGPT-Masterplan mit Windows-Fassung, neun Kanal-Templates und Markennamen; (b) Grok-Recherche (PDF, 24 Seiten) mit Chatverlauf; (c) Perplexity-Prüfung des Masterplans; (d) HTML „Faceless-Maschine Bauplan". Alles wurde nach `01 Idee und Strategie\Recherche` gelegt (Bauplan kopiert aus `Downloads`, PDF verschoben).
6. Drei parallele Prüfläufe gegen Primärquellen (Plattform-APIs; Monetarisierung und Recht; Werkzeuge und Preise). Ergebnis: `Recherche\Faktencheck 2026-10-29.md`. Wichtigste Befunde siehe Abschnitt 6.
7. Claude schrieb `Konzept.md`, `Ablaufplan.md` (Phasen 0 bis 5) und `Fragenkatalog.md` (25 Fragen mit Annahmen).
8. Laptop geprüft: PCSpecialist Recoil III 16, Intel Core Ultra 9 275HX, NVIDIA RTX 5080 Laptop GPU 16 GB VRAM (Treiber 610.74), 31,5 GB RAM, Windows 11 Pro; Git, Node 24, Python 3.13, FFmpeg mit NVENC, Claude Code 2.1, VS Code bereits installiert. C: hatte 61 GB frei von 3,7 TB.

### 29./30.10.2026, Nacht: Antworten, Namen, Repository

9. Stefan beantwortete alle 25 Fragen (Abschnitt 2.4). Claude trug sie in `Konzept.md` (Fassung 2) und `Fragenkatalog.md` ein.
10. Namensrecherche für neun Marken (37 Namen geprüft gegen TMview, Plattform-Handles, Domains). Befund: PromptPilot (eingetragene EU-Marke von Lemon Inc., ByteDance-Konzern, Kl. 9/42), VelvetGlow (eingetragene EU- und UK-Marke in Klasse 3) und TorqueLab (eingetragene US-Marke Mountz, Kl. 9) sind ausgeschlossen; die anderen ChatGPT-Vorschläge waren auf den Plattformen belegt oder generisch. Stefan übernahm die Empfehlungen (Abschnitt 7.1).
11. Repository `C:\Automation\faceless-network` angelegt (Git initialisiert, eigene `CLAUDE.md` mit Betriebsregeln, `config/brands.yaml` mit allen neun Marken, `.env.example`, `.gitignore`, `README.md`). Markenregister `02 Marke\Marken.md`.
12. Phase 1 wurde in eine eigene Claude-Code-Sitzung ausgelagert („Phase 1: Pipeline in faceless-network bauen", Abschnitt 5.6).

### 30.10.2026, früh: Phase 1 fertig

13. Die Phase-1-Sitzung baute: Designsystem für alle neun Marken, neun 10-Sekunden-Demos, die vollständige Kette Skript → TTS → Wortzeiten (faster-whisper mit CUDA) → HyperFrames-Render → FFmpeg NVENC → Prüfbericht → SQLite-Zustände → Warteschlange, Mock-Publisher im Dry-Run, Kostenlogger, Tests, Aufgabenplanungs-Vorlagen. Ihre erste Meldung brach ab („Nutzungslimit"); auf Stefans „Versuch es noch einmal" lieferte sie: 24 Tests grün, neun Demos und zwölf Testvideos (Promptwerk und Scutoria, je drei Themen DE und EN) als MP4 in `05 Produktion`; alle im Zustand HUMAN_REVIEW, nur weil die Stimme ein stummer Platzhalter war.

### 30.10.2026, Vormittag: echte Stimme

14. Stefan trug den Gemini-Schlüssel ein, aber in `.env.example` statt `.env`. Claude übernahm ihn nach `.env` (von Git ignoriert) und leerte `.env.example`; es gab noch keinen Commit. Stefan: „lasse ich so" (keine Erneuerung).
15. Erstes Testvideo mit Gemini-Stimme (Scutoria DE, 05.11.): 74,1 s, alle Prüfungen bestanden, Zustand APPROVED, Kosten 0,0169 USD, etwa 5 Minuten am Laptop.
16. Hintergrundlauf für die restlichen elf: vier weitere Scutoria-Videos fertig (je 0,0155 bis 0,0172 USD); zwei Läufe brachen mit `WinError 10053` ab (Verbindung zu Google unterbrochen); dann wurde der Lauf von Stefan oder der App gestoppt. Sieben Testvideos sind seither nicht neu vertont (alle sechs Promptwerk, Scutoria 07.11. EN). Sie bleiben bewusst liegen, weil das alte Design inzwischen abgelöst ist.

### 30.10.2026, Mittag: Regie statt Folien

17. Stefan brachte eine ChatGPT-Analyse des ersten Testvideos: technisch brauchbar, aber „animierte Präsentation, kein Reel" (schwacher Einstieg, kaum visuelle Abwechslung, leere Bildfläche, kein Spannungsbogen, Schild-Symbol überall). Abgelegt in `02 Marke\Scutoria\2026-10-30 Reel-Analyse erstes Testvideo (ChatGPT).md`. Vorgabe Stefans: jede Marke nacheinander fertig machen, Abschnitt für Abschnitt.
18. Die Phase-1-Sitzung baute ein Regie-System (Hook-Engine mit fünf Hook-Typen und Bewertung, Story-Engine, fünf Szenentypen Cinematic Hook / UI Demonstration / Data Flow / Comparison / Key Takeaway, neue Prüfungen für Szenenvielfalt, Bildwechsel, Lesbarkeit, Audiopegel). Dokumentiert in `docs/direction-system.md` und `02 Marke\Scutoria\2026-10-30 Regie Szenenplan und Hooks (Claude).md` (mit Quellenprüfung S1 bis S9, vier Aussagen als UNVERIFIED ausgeschlossen).
19. 15-Sekunden-Prototyp mit Vorher-Nachher. Stefan: „Ja passt soweit, aber ich bin nicht zu 100 % zufrieden" und schlug Higgsfield vor (Abschnitt 2.3).
20. Claude bewertete Higgsfield: liefert Filmmaterial (Clips, Bilder), keine Vorlage mit Text und Layout; daher Higgsfield einmalig als Asset-Fabrik je Marke, Claude Code dauerhaft als Regie und Renderer. Vergleich Fassung A (nur Claude Code) gegen Fassung B (Higgsfield-Clips plus Claude Code), danach Einfrieren der Marke.
21. Fassung A Scutoria: Hook H1 („Darfst du vertrauliche Firmendaten einfach in Claude eingeben?"), neue Vertonung 0,0177 USD, 75,5 s. Korrigiert (zu lange Texte, doppeltes Layout, Leerraum) ohne neue Kosten.

### 30.10.2026, Nachmittag: zweite Kritik, Scutoria-Design, Higgsfield

22. Stefan wollte Fassung A „noch ändern" und lieferte eine zweite Kritik (Verfasser nicht genannt; bezog sich auf das erste Testvideo). Abgelegt: `02 Marke\Scutoria\2026-10-30 Überarbeitung KI-Datenschutz-Reel (zweite Kritik).md` mit Abgleich. Umgesetzt als Fassung A2: Kundenliste.xlsx als roter Faden, kein Logo-Intro, Amber nur für Offenes, Rot nur für Sperren, Statusleiste unten, Untertitel normal geschrieben, keine URL-Zeilen im Bild, Training/Speicherung/Freigabe getrennt, Abschluss mit scutoria.com. Abweichung: Länge 65–90 s statt der vorgeschlagenen 45 s (Grund: TikTok Rewards zählt nur Videos über 1 Minute; Konzept).
23. Stefan: Für Scutoria gibt es schon ein Design. Claude fand es in `C:\Users\Stefa\OneDrive\scutoria\design\project\` (Markenbuch `README.md`, `tokens.json`, Scutum-Logo, Manrope-Schrift) und ließ die Marke darauf umstellen. Ergebnis Fassung A3, danach A3.1 (Untertitel in Sinngruppen, Bildmitte gefüllt). Anrede: Stefan „Du".
24. Parallel hat Stefan diesen Chat geforkt („Umgebung für Video- und Social-Media-Projekt (fork)"); daraus entstand die Sitzung „Higgsfield-Clips für Scutoria generieren (Fassung B)". Stefan buchte Higgsfield Starter. Diese Sitzung schrieb das Prompt-Blatt auf das Scutoria-Design um (Fassung 2), holte Creditpreise und erzeugte Clips (Stand Abschnitt 4).
25. Ohne Beteiligung dieses Chats liegt seit 30.10.2026 ein Ordner `02 Marke\_Higgsfield-Briefings (Codex, 2026-10-30)` mit neun Marken-Briefings, laut eigener Angabe von „Codex" erstellt (vermutlich ein anderes KI-Werkzeug, das Stefan benutzt hat; nicht von Claude erstellt, Herkunft nicht weiter geprüft). Er erwähnt eine Datei `OneDrive/Business/AGENTS.md`, die es dort zum Zeitpunkt dieses Berichts nicht gibt.

### Verworfen und warum

| Verworfen | Grund |
|---|---|
| Mac mini M1 (8 GB) als Produktionsrechner | Stefans Wunsch, am Laptop zu arbeiten; Laptop deutlich stärker. Mac mini bleibt mögliche spätere Reserve. |
| VPN oder fremder Wohnsitz für TikTok Rewards | Verstoß gegen TikTok-Bedingungen (Auszahlung wird über Steuer- und Bankdaten geprüft), Risiko Sperre und Einbehalt. |
| Eigene TikTok-Direct-Post-App | TikTok nennt „A utility tool to help upload contents to the account(s) you or your team manages" ausdrücklich als nicht akzeptablen Anwendungsfall; ohne Audit nur private Posts. |
| Ayrshare | Premium hat nur 1 Profil; für mehrere Marken Launch 299 USD/Monat, außerhalb des Budgets. |
| Google Veo über die Gemini-API | eingestellt („The Veo 3.1 Preview in the Gemini API has been shut down."). |
| Automatischer Chartsong (Bauplan des Kollegen) | Musikrechte für kommerzielle Nutzung nicht geklärt. |
| ChatGPT-Markennamen PromptPilot, VelvetGlow, TorqueLab | eingetragene Marken (Abschnitt 6.6). |
| Eigene Cyan-Palette für Scutoria (#0B132B / #00D4FF) | widerspricht dem vorhandenen Scutoria-Markenbuch. |
| 45-Sekunden-Fassung aus der zweiten Kritik | Länge unter 1 Minute schließt TikTok Rewards aus; Dramaturgie wurde übernommen. |
| Schild-Symbol als Motiv, Clip „hero_shield_assemble" | signalisiert Sicherheit, während ein Risiko erklärt wird (zweite Kritik); Markenbuch erlaubt das Schild nur als Logo. |
| Neu-Vertonung der sieben alten Testvideos | altes Design ist abgelöst; Geld für ein verworfenes Design. |

---

## 4. Aktueller Stand im Detail

### 4.1 Fertig

- Arbeitsumgebung `OneDrive\Business` mit Vorlagen und `CLAUDE.md`.
- Gedächtnis: Übersicht in Google Drive (letzte Fassung 30.10.2026, 06:00 Wien), Projekt in `00 START.md`, Landkarte OneDrive, Log-Einträge vom 30.10.2026 00:45 (dieser Chat) und 05:38 (Phase-1-Sitzung). Die Übersicht spiegelt noch nicht den Stand ab Mittag (Regie, A2/A3, Scutoria-Design, Higgsfield, Anrede).
- Planungsdokumente: `Konzept.md` (Fassung 2), `Ablaufplan.md`, `Fragenkatalog.md` (alle Antworten), `Faktencheck 2026-10-29.md`, Namensrecherche, Markenregister.
- Repository mit vollständiger Produktionskette ohne Veröffentlichung; 32 Tests bestehen (Stand 30.10.2026 16:00); Regie-System; Asset-Schicht für Fassung B; Scutoria-Marke auf dem echten Designsystem.
- Neun 10-Sekunden-Demos (altes Phase-1-Design) in `05 Produktion\_Demos\<id>\demo.mp4` mit `index.html`.
- Scutoria Fassung A3.1: 78,4 s, Gemini-Stimme („du"), Scutoria-Design, Prüfbericht bestanden bis auf `schematic_ui` (UI-Szene ist ein Schema, keine echte Bildschirmaufnahme), Zustand HUMAN_REVIEW. Pfad `05 Produktion\_Demos\scutoria-regie\fassung-a3\video.mp4`; Vorgänger als `*_v1` daneben; Übersichtsseite `scutoria-regie\index.html` zeigt Prototyp, A, A2, A3.

### 4.2 Teilweise erledigt

- **Testvideos alt (Phase-1-Design):** 5 Scutoria-Videos mit Gemini-Stimme im Zustand APPROVED (`storage\approved`), 4 in HUMAN_REVIEW, 3 in SCRIPTED (Stand `fn.cli status`). Sie sind Testmaterial, nicht zur Veröffentlichung gedacht.
- **Fassung B Scutoria (Higgsfield):** Vier Clips liegen in `C:\Automation\faceless-network\brands\ai_security\assets\higgsfield\`: `hero_document_to_chat.mp4`, `bg_hook_dataroom.mp4`, `bg_flow_lanes.mp4`, `bg_ui_desk.mp4`, je mit Startbild `.start.png` und Rohdatei `_raw_*.mp4`. Nur `hero_document_to_chat.mp4` ist in `manifest.json` und `LICENSE.md` dokumentiert (12 Credits). Das Guthaben fiel laut Konnektor von 278 (Freigabevorlage, 30.10.2026 vormittags) auf 182 Credits (30.10.2026, 16:00 Wien), also 96 Credits Verbrauch; die Aufschlüsselung der übrigen 84 Credits ist in den Dateien noch nicht eingetragen. Die Higgsfield-Sitzung arbeitete beim letzten Blick noch (Abfrage Guthaben). Laut Prompt-Blatt Fassung 2 fehlen noch `bg_compare_split`, `bg_negate_pulse`, `bg_takeaway_calm`, `bg_outro_orbit` (optional `hero_server_corridor`). Fassung B ist noch nicht gerendert.
- **Codex-Briefings** für alle neun Marken liegen vor, sind aber nicht mit dem Repository abgeglichen und kein beschlossener Stand.
- **Upload-Post-Adapter:** Code vorhanden; Upload-Endpunkt laut Dokumentation verifiziert, Pfade für Status, Profile, Analytics als NOT_VERIFIED markiert (werfen bewusst einen Fehler).
- **Aufgabenplanung:** Vorlagen in `automation\` (FN Render Queue 09:00, FN Publish Sync stündlich :05 von 8 bis 23 Uhr im Dry-Run, FN Costs and Status 19:00, FN Topic Proposals 19:30 mit `claude -p`), nicht registriert. Diese Zeiten stammen aus dem Bauplan-Muster; Stefans Slots 12/14/18 Uhr betreffen die Veröffentlichung über Upload-Post, nicht die Produktion.

### 4.3 Noch nicht begonnen

- Promptwerk und die anderen sieben Marken im neuen Regie-Stil (nur Scutoria ist in Arbeit).
- Konten: keine Gmail-, TikTok-, Instagram-, YouTube-Konten angelegt; keine Domains gesichert; Upload-Post-Konto nicht angelegt.
- Handy-Zentrale (Claude-Artefakt für Themenwahl und Freigabe).
- 30-Tage-Themenkalender für den Echtbetrieb (nur Testkalender ab 05.11.2026 für zwei Marken).
- Musik und Soundeffekte (keine Lizenzquelle gewählt; `music.file` in `audio_style.yaml` leer).
- Kommentar-Beantwortung (Phase 3).
- Gewerbe, Steuerberatung, Impressum-Text.
- Erster Git-Commit (18 Änderungen offen, kein Commit; Stefan hat noch keinen Commit beauftragt).

---

## 5. Technisches Setup

### 5.1 Geräte

| Gerät | Rolle | Daten |
|---|---|---|
| PCSpecialist Recoil III 16 (Windows 11 Pro) | Produktionsrechner, läuft laut Stefan 24/7 | Core Ultra 9 275HX, RTX 5080 Laptop 16.303 MiB VRAM, Treiber 610.74, 31,5 GB RAM; C: 3,7 TB, frei 43,7 GB am 30.10.2026 16:00 (Mindestwert für Renders 30 GB); Energiezustände: Modern Standby (S0) und Ruhezustand, kein S1 |
| Mac mini M1 (2020), 8 GB | Reserve, eventuell später für das Claude-Konto | nicht im Einsatz |
| Handy | Freigaben, Ansicht der Videos | Stefan folgt dem Chat per Remote Control; große Dateien (28 MB) kamen teils nicht an |

### 5.2 Software auf dem Laptop (geprüft 29.10.2026)

Git 2.53, Node v24.22.1, Python 3.13.14, FFmpeg mit `h264_nvenc`, `hevc_nvenc`, `av1_nvenc`, Claude Code 2.1.142, VS Code 1.132, winget 1.29. Im Repository: Python-venv `.venv` (Paket `fn` editierbar installiert, faster-whisper mit CUDA 12/cuDNN 9 über pip-Wheels, Modell large-v3 im Cache), `package.json` mit HyperFrames (`npx hyperframes`). Für die Volltextsuche existiert lokal `C:\Users\Stefa\.od-extract` (nicht projektbezogen).

### 5.3 Konten und Dienste

| Dienst | Stand | Wo Zugang liegt |
|---|---|---|
| Claude Max (Stefans bestehendes Konto) | genutzt für alle Sitzungen | Konto Stefan; keine Datei |
| Google Gemini API (TTS) | Schlüssel gesetzt, Paid Tier genutzt | `C:\Automation\faceless-network\.env`, Variable `GEMINI_API_KEY` (Git ignoriert) |
| Higgsfield | Tarif Starter (von Stefan gebucht, 30.10.2026), 182 Credits (16:00) | Lesender Konnektor in diesem Chat; generierender MCP-Server `higgsfield` (`https://mcp.higgsfield.ai/mcp`) in der Higgsfield-Sitzung, von Stefan per `/mcp` angemeldet; `HIGGSFIELD_API_KEY` in `.env` leer |
| Upload-Post | nicht angelegt | `UPLOADPOST_API_KEY`, `UPLOADPOST_USER` in `.env` leer |
| Runway, ElevenLabs | nicht genutzt | Variablen in `.env` leer |
| TikTok, Instagram, YouTube, Gmail je Marke | nicht angelegt | – |
| Google Drive (Gedächtnis) | verbunden über Konnektor | Ordner Claude-Gedächtnis, ID `1bUdvCrjhipJezYHPlhBM_d5YHl1AA5fp`; Übersichten `1C_0Au5INARUiG1dq_djKtf01o_eLKZ17`; Frühere Fassungen `1lqhMDs_wWQuy9tO6iY98xinBzbLHK-PP`; Archiv `1OckzHysYbJTdRcZi3rdgzUtex6BPBZeJ`; Log-Eingang `1V22KU5F65VYe2dl4NK27-phR6tSpSHcO` |

### 5.4 Ordner in OneDrive (`C:\Users\Stefa\OneDrive\Business`)

```
CLAUDE.md                          Regeln des Arbeitsordners
00 Eingang\                        leer
01 Idee und Strategie\
   Konzept.md                      Fassung 2, gültiges Zielbild
   Ablaufplan.md                   Phasen 0–5 mit Abnahme
   Fragenkatalog.md                25 Fragen, Antworten oben
   Übergabebericht 2026-10-30.md   dieser Bericht
   Recherche\
      2026-10-29 Masterplan (ChatGPT).md
      2026-10-29 Chatverlauf Recherche (Grok).md
      2026-10-29 TikTok KI-Videos und Creator Rewards – Recherche (Grok).pdf
      2026-10-29 Prüfung des Masterplans (Perplexity).md
      2026-10-29 Faceless-Maschine Bauplan (System des Kollegen).html
      Faktencheck 2026-10-29.md
   Wettbewerb und Vorbilder\       leer
02 Marke\
   Marken.md                       Markenregister (Namen, Handles, Domains, Gmail-Vorschläge)
   Namensrecherche 2026-10-29.md
   Markenstimme.md                 Gerüst
   Logo\, Farben und Schriften\, Designvorlagen\   leer
   Scutoria\
      2026-10-30 Reel-Analyse erstes Testvideo (ChatGPT).md
      2026-10-30 Regie Szenenplan und Hooks (Claude).md
      2026-10-30 Überarbeitung KI-Datenschutz-Reel (zweite Kritik).md
      2026-10-30 Higgsfield Asset-Paket (Prompt-Blatt).md          Fassung 1, Farben ungültig
      2026-10-30 Higgsfield Asset-Paket (Prompt-Blatt, Fassung 2).md  gültig
      2026-10-30 Higgsfield Designrichtungen und Freigabe.md       Modelle, Creditpreise
   _Higgsfield-Briefings (Codex, 2026-10-30)\   00-START.md, 01-Scutoria.md … 09-Zonkfruit.md
03 Kanäle\_Vorlage Kanal\Kanalprofil.md
04 Redaktionsplan\Redaktionsplan.csv (nur Kopfzeile), Ideenspeicher.md
05 Produktion\
   _Vorlage Video\                 Ordnervorlage je Video
   _Demos\<brand_id>\demo.mp4      neun 10-s-Demos, index.html
   _Demos\scutoria-regie\          Prototyp, vorher/nachher, fassung-a, fassung-a2, fassung-a3, index.html
   _Test\<video_id>\               zwölf Testvideos (Phase-1-Design), index.html
06 Bibliothek\, 07 Auswertung\     leer
08 Recht und Verwaltung\
   2026-07-20 EU-Kommission Leitlinien Art. 50 AI Act (Transparenz, C(2026) 5054).pdf
   Gewerbe und Nebenbeschäftigung\, Lizenzen\, Verträge und Kooperationen\, Rechnungen\   leer
```

### 5.5 Repository `C:\Automation\faceless-network` (Git, Branch `main`, kein Commit)

| Pfad | Inhalt |
|---|---|
| `CLAUDE.md` | Betriebsregeln für Claude (verbindlich, lesen) |
| `README.md` | Installation, Startbefehle, Phase-2-Checkliste |
| `.env` / `.env.example` | Schlüssel (nur `.env` befüllt, Git ignoriert) |
| `config/brands.yaml` | neun Marken: IDs, Namen, Phase, `enabled`, Stil, Palette, Regeln, Risiko; Defaults (Sprachen de/en, primär de, Slots 12:00/14:00/18:00 Europe/Vienna, 3 Themen/Tag, 1080×1920, 65–90 s, harte Untergrenze 61 s, Freigabe automatisch, erste 20 manuell, Risiko high manuell, KI-Label immer, Puffer 7 Tage) |
| `config/platforms.yaml`, `policies.yaml`, `voices.yaml` | Plattform-, Richtlinien-, Stimmeinstellungen |
| `brands/<id>/` | Designsystem je Marke (`brand.yaml`, `visual_style.md`, `script_prompt.md`, `image_prompt.md`, `subtitle_style.json`, `intro_config.json`, `outro_config.json`, `audio_style.yaml`, `assets/`, `references/`); `brands/ai_security/tokens.json` = Kopie der Scutoria-Tokens; `brands/ai_security/assets/` mit Logo (Scutum-Marke), Schriften (Manrope, IBM Plex Mono mit Lizenzen), `higgsfield/` (Clips, `manifest.json`, `LICENSE.md`) |
| `docs/design-system.md`, `docs/direction-system.md` | gemeinsames 9:16-Layout; Regie-System, Prüfungen, Ablauf |
| `prompts/` | `calendar_planner.md`, `research_factcheck.md`, `script_writer.md`, `localizer.md`, `compliance_review.md` |
| `.claude/skills/` | zehn Skills: calendar-planner, research-factcheck, script-writer, localizer, voice-generator, video-producer, video-editor, compliance-check, social-publisher, analytics-review |
| `src/fn/` | Python-Paket: `config`, `brands`, `calendar`, `scripting`, `tts/` (gemini, edge, sapi, mock), `transcribe`, `render/` (hyperframes, ffmpeg, compose, templates, director, assets), `direction/` (hooks, story, checks), `compliance`, `state`, `queue`, `publishing/` (base, mock, uploadpost), `costs`, `disk`, `pipeline`, `cli` |
| `scripts/` | `scaffold_brands.py`, `scaffold_skills.py`, `render_demos.py` |
| `tests/` | pytest, 32 Tests bestehen |
| `automation/` | `register_tasks.ps1`, `run_render.ps1`, `run_publish.ps1`, `run_status.ps1`, `run_claude_calendar.ps1`, README (nicht registriert) |
| `data/` | `state.db` (SQLite), `calendars/`, `scripts/`, `direction/` (Szenenpläne A, A2, B, Prototyp), `costs/costs.jsonl` |
| `storage/` | `drafts/`, `approved/`, `published/`, `failed/`, `demos/`, `direction/` (Renders), Spiegel nach `OneDrive\Business\05 Produktion` |

Wichtige Befehle (PowerShell, im Repository, vorher `$env:PYTHONIOENCODING = "utf-8"`):
`.\.venv\Scripts\python.exe -m fn.cli status` · `… -m fn.cli costs` · `… -m fn.cli produce data\scripts\<id>.md --tts gemini` · `… -m fn.cli publish --dry-run` · `… -m pytest -q`.

Bekannte Eigenheiten (aus der Gedächtnisnotiz `C:\Users\Stefa\.claude\projects\C--Users-Stefa-OneDrive-Business\memory\faceless-network-phase1.md`): Python immer über `.venv\Scripts\python.exe`; ohne Gemini-Schlüssel ist die Stimme stumm (`--tts sapi` gibt eine hörbare Windows-Entwurfsstimme, nie veröffentlichbar); Bash-Heredocs mit Apostrophen scheitern auf diesem Rechner, Dateien mit dem Write-Werkzeug schreiben; `hyperframes snapshot -o` braucht einen absoluten Pfad; PyAV ist inkompatibel, `fn.transcribe` dekodiert über FFmpeg.

### 5.6 Claude-Code-Sitzungen (Desktop-App)

| Sitzung | ID | Rolle | Stand |
|---|---|---|---|
| Umgebung für Video- und Social-Media-Projekt (diese) | – | Planung, Gedächtnis, Steuerung | aktiv |
| Phase 1: Pipeline in faceless-network bauen | `local_61a9137e-6cf2-4cdd-9477-409ebe6d996a` | baut und rendert im Repository (Regie, A/A2/A3) | zuletzt untätig nach A3.1 |
| Umgebung … (fork) | `local_77b166ea-e260-4722-b8fb-dc98d4a88a21` | Stefans Abzweig dieses Chats | untätig |
| Higgsfield-Clips für Scutoria generieren (Fassung B) | `local_fca3ee1c-8c1a-47f6-901f-8b18981d4392` | erzeugt Higgsfield-Clips, gestartet aus dem Fork | arbeitete zuletzt |

### 5.7 Scutoria-Designsystem (nur lesen, dort gilt eine eigene `CLAUDE.md`)

Quelle `C:\Users\Stefa\OneDrive\scutoria\design\project\`: `README.md` (Markenbuch), `tokens.json`, `assets\Logos\scutum-mark.svg` (dunkel), `scutum-mark-ink.svg` (Papier), `favicon.svg`, `fonts\manrope-*.woff2`, `licenses\manrope.txt`. Kernwerte Thema dunkel: ground #0b1120, surface #121b2f, surface-raised #19243b, ink #e9eef8, ink-muted #a1adc4, accent #4f8cff (einziger Akzent), button #2f6be6, signal-amber #ffd166, signal-red #ff6b6b, signal-green #2ec4b6, on-signal #0a0c10; Marker Fakt (Quadrat, #4f8cff), Auslegung (Raute, #b07cff), Unsicher (halber Kreis, #ffd166), Lücke (gestrichelter Kreis, #ff6b6b). Schrift Manrope 200–800, Belegschrift IBM Plex Mono. Kein Neon, Glow, Glas, keine Lichtkegel, flacher Grund; Bewegung kurz und einmalig. Logo: Scutum-Marke, nie umfärben/füllen/drehen; Wortzeichen SCUTORIA als Text Manrope 700, Versalien, Laufweite 0,18em. Claim „Belegt. Datiert. Vorzeigbar." / „Sourced. Dated. Ready to show."; Pflichtzeile „Quellenbasiert. Keine Rechtsberatung." Markenbuch sieht „Sie" vor; im Video gilt „du" (Stefan).

### 5.8 Zeitpläne

- Veröffentlichung (geplant, Stefan): je Marke 12:00, 14:00, 18:00 Europe/Vienna. Annahme (nicht bestätigt): je Slot eine Sprachfassung, also 3 Posts je Konto und Tag.
- Produktion (Vorlagen, nicht registriert): siehe 4.2.
- Gedächtnis: Tageslog-Aufgabe täglich 21:51 Wien, Monatslog am 1. um 06:50 Wien (in START beschrieben, nicht Teil dieses Projekts).

---

## 6. Zahlen, Daten, Preise, Fakten (mit Quelle und Abrufdatum)

Alle Abrufe am 29. oder 30.10.2026, sofern nicht anders angegeben. Ausführlich mit URLs in `01 Idee und Strategie\Recherche\Faktencheck 2026-10-29.md`.

### 6.1 Plattformen und Programme

| Fakt | Wert | Quelle |
|---|---|---|
| TikTok Creator Rewards, Länder | USA, UK, Deutschland, Japan, Südkorea, Frankreich, Mexiko, Brasilien; Österreich nicht | TikTok Creator Academy, „Who is eligible…", zuletzt aktualisiert 18.08.2026 |
| Rewards-Voraussetzungen | 18+, 10.000 Follower, 100.000 Views in 30 Tagen, nur Personal Account, Videos über 1 Minute, mind. 1.000 For-You-Views je Video, kein Photo Mode, 5 Verstöße in 30 Tagen schließen aus | ebd. und „What videos are eligible…" |
| TikTok Shop | in Österreich nicht verfügbar (EU-Liste: DE, FR, ES, IE, IT, PL, NL, BE, UK) | seller.tiktok.com |
| TikTok LIVE-Geschenke, TikTok One in Österreich | nicht ermittelbar (offizielle Seiten ohne Länderliste) | TikTok Support, ads.tiktok.com |
| YouTube-Partnerprogramm | Österreich verfügbar; 1.000 Abonnenten + 4.000 Stunden/12 Monate oder 10 Mio. Shorts-Views/90 Tage | support.google.com/youtube/answer/7101720, /72851 |
| YouTube Fan-Funding-Stufe | 500 Abonnenten, 3 Uploads/90 Tage, 3.000 Stunden oder 3 Mio. Shorts-Views | support.google.com/youtube/answer/13429240 |
| YouTube ab 01.02.2027 | Neuantragsteller: 8.000 Stunden/365 Tage oder 20 Mio. Shorts-Views/90 Tage; keine Shorts-Werbeerlöse mehr für Kanäle unter 10 Mio. Shorts-Views/90 Tage; bestehende YPP-Mitglieder nicht von der Anhebung betroffen | YouTube-Blog, 10.08.2026 |
| YouTube „inauthentic content" | seit 15.07.2025; nicht monetarisierbar u. a. „AI-generated content made with generic or unoriginal templates" | support.google.com/youtube/answer/1311392 |
| Instagram-Geschenke | Österreich auf Länderliste; professionelles Konto, 18+, 500 Follower; 0,01 USD je Stern | help.instagram.com/738469380549477 |
| Instagram-Abos | Österreich laut Creators-Blog vom 20.09.2023; aktuelle Liste nicht ermittelbar | creators.instagram.com |
| Instagram Bonus-Programme | nur auf Zufallseinladung; Österreich nicht ermittelbar | help.instagram.com/331274061770840 |

### 6.2 APIs und Limits

| Fakt | Wert | Quelle |
|---|---|---|
| TikTok Content Posting API, nicht auditiert | nur SELF_ONLY (privat), höchstens 5 Nutzer je 24 h | developers.tiktok.com/doc/content-sharing-guidelines |
| TikTok Posting-Cap | „typically around 15 posts per day/creator account", kontoweit über alle Clients | ebd. |
| TikTok Felder | `privacy_level` Pflicht; `brand_content_toggle`, `brand_organic_toggle`; `is_aigc` optional | Direct-Post-Referenz |
| TikTok Tokens | Access 24 h, Refresh 365 Tage, Refresh rotiert; 6 Requests/Minute je Token | oauth-user-access-token-management |
| YouTube videos.insert | eigener Topf 100 Aufrufe/Tag/Projekt, 1 Einheit je Aufruf (seit 01.06.2026; Kostenkorrektur 04.12.2025); Erhöhung nur nach Audit | developers.google.com/youtube/v3/determine_quota_cost (Stand 15.10.2026), revision_history |
| YouTube unverifizierte Projekte | Referenz 15.10.2026: „not restricted to private viewing mode"; Hilfeseite nennt Sperre weiterhin; widersprüchlich, vor Betrieb testen | API-Referenz videos; support.google.com/youtube/answer/7300965 |
| YouTube KI-Offenlegung | Pflicht bei realistischen Inhalten; API-Feld `status.containsSyntheticMedia` (seit 30.10.2024) | support.google.com/youtube/answer/14328491 |
| Instagram API-Limit | Endpunkt `content_publishing_limit` liefert 50/24 h, Guide nennt 100; Reels nicht ausdrücklich; konservativ 50 | developers.facebook.com |
| Instagram KI-Label | Pflicht bei fotorealistischem Video/realistischem Audio; API-Parameter `is_ai_generated` | meta.com Help; Content-Publishing-Guide |
| Instagram API | Business- oder Creator-Konto; Medien müssen öffentlich gehostet sein; Container verfallen nach 24 h | developers.facebook.com |

### 6.3 Werkzeuge und Preise

| Dienst | Preis / Wert | Quelle |
|---|---|---|
| Upload-Post | Free 0 (2 Profile, 10 Uploads/Monat, ohne TikTok); Basic 24 USD monatlich / 16 USD jährlich (5 Profile); Professional 50 / 33 (25); Advanced 147 / 118 (75); Business 438 / 350 (225); Add-ons Basic +5 für 15 USD, +10 für 25 USD | upload-post.com/llms-full.txt |
| Upload-Post Tagesgrenzen je Konto | TikTok 15, Instagram 50, YouTube 30 | docs.upload-post.com/guides/rate-limits |
| Upload-Post API | `POST https://api.upload-post.com/api/upload`, `scheduled_date` (bis 365 Tage), `Idempotency-Key`, Status je `request_id`/`job_id`, Analytics; KI-Labels `is_aigc`, `is_ai_generated`, `containsSyntheticMedia`; offizieller MCP-Server `https://mcp.upload-post.com/mcp` (MIT) | docs.upload-post.com |
| Ob Upload-Posts TikTok-App auditiert ist | nicht ermittelbar (nicht öffentlich dokumentiert); Test mit erstem Post | – |
| Ayrshare | Premium 149 USD (1 Profil), Launch 299 USD (10), Business 599 USD (30) | ayrshare.com/pricing |
| Blotato | Starter 29 USD (20 Konten), Creator 97 USD (40), Agency 499 USD | blotato.com/pricing |
| Gemini TTS | 2.5 Flash Preview TTS: Output 10 USD/1 Mio. Audio-Token; 3.8 Flash TTS 9 USD; Free-Tier-Limits nicht ermittelbar (nur hinter Login) | ai.google.dev/gemini-api/docs/pricing |
| ElevenLabs | Starter 6 USD, Creator 22 USD (121 Minuten), Pro 99 USD; kommerziell ab Starter | elevenlabs.io/pricing |
| Google Veo (Gemini API) | eingestellt; Nachfolger Gemini Omni Flash ca. 0,10 USD/s 720p | ai.google.dev/gemini-api/docs/video |
| Runway API | gen4_turbo 5 Credits/s (0,40 USD je 8 s), gen4.5 0,96 USD je 8 s | docs.dev.runwayml.com |
| Kling API | 3.0 720p ohne Ton ca. 0,74 USD je 8 s | kling.ai/dev/pricing |
| Higgsfield Tarife | Starter 19 €/Monat (270 Credits), Plus 59 € / 47 € jährlich (1.200), Ultra 129 € / 99 €; Free ohne kommerzielle Nutzung | higgsfield.ai/pricing (Abruf 29./30.10.2026) |
| Higgsfield Creditpreise laut Server (30.10.2026) | Nano Banana Pro Standbild 2k: 2; Kling 3.0 Omni Frames pro 8 s ohne Ton: 10 (std 8, 6 s std 6, 4k 48); Seedance 1.5 Pro 1080p 8 s: 24; Kling 3.0 Turbo 1080p 8 s: 16 | `02 Marke\Scutoria\2026-10-30 Higgsfield Designrichtungen und Freigabe.md` (Vorabfrage `get_cost`) |
| Higgsfield Lizenz | Nutzungsbedingungen 4.4: keine Beschränkung der kommerziellen Nutzung von Outputs; Rechte bleiben nach Kündigung | zitiert in `brands\ai_security\assets\higgsfield\LICENSE.md` |
| HyperFrames | Open Source von HeyGen, Apache-2.0, Version 0.8.217 (29.10.2026), Node ≥ 22, FFmpeg | github.com/heygen-com/hyperframes |
| faster-whisper | CUDA 12, cuDNN 9 | github.com/SYSTRAN/faster-whisper |
| Claude Max | ab 100 USD/Monat; 5-Stunden-Fenster und Wochenlimit, geteilt zwischen Claude und Claude Code; Limits gelten für „ordinary, individual usage"; Desktop-Scheduled-Tasks laufen nur bei wachem Rechner und offener App | claude.com/pricing; code.claude.com/docs |

### 6.4 Recht Österreich und EU

| Fakt | Wert | Quelle |
|---|---|---|
| Gewerbe für Creator | Werbung/Kooperationen: in der Regel Gewerbe „Werbeagentur" (frei) bzw. Ankündigungsunternehmen; Affiliate mit Provision: Handelsgewerbe; SVS-Pflicht | WKO 20.03.2026 und 12.03.2026 |
| Kleinunternehmergrenze USt | 55.000 € brutto (seit 01.01.2025), Toleranz 10 % | USP, Stand 01.01.2026 |
| Impressum Social Media | erforderlich, mit höchstens zwei Klicks erreichbar; Verweis auf Website-Impressum genügt nicht; Werbung nach § 6 ECG kennzeichnen | WKO NÖ, 14.01.2026 |
| EU AI Act Art. 50 | gilt seit 02.08.2026; Deployer müssen Deepfakes offenlegen; monetarisierte Kanäle gelten laut Leitlinien als professionell (Deployer); stilisierte, physikalisch unmögliche, cartoonhafte Darstellungen und KI-Stimmen ohne Identitätstäuschung sind keine Deepfakes; realistische Szenen historischer Ereignisse schon | EU-Kommission, Leitlinien C(2026) 5054 vom 20.07.2026 (PDF in `08`); Code of Practice 10.06.2026 (freiwillig) |
| Nebenbeschäftigung | § 56 BDG Meldepflicht; laut Stefan abgeklärt (29.10.2026); nicht von Claude geprüft | RIS; Aussage Stefan |
| Verschwiegenheit | § 46 BDG | RIS NOR40183036 (aus Grok-PDF) |

### 6.5 Kosten dieses Projekts bisher

| Posten | Betrag | Quelle |
|---|---|---|
| Gemini TTS, sieben Vertonungen (fünf Testvideos alt, Fassung A, A2/A3) | 0,1183 USD (0,0169 + 0,0177 + 0,0188 + 0,0161 + 0,0155 + 0,0172 + 0,0161) | `fn.cli costs`, 30.10.2026 16:00 |
| Higgsfield Starter | Tarifpreis laut Preisseite 19 €/Monat; ob monatlich oder jährlich gebucht: nicht ermittelbar | Stefan hat gebucht; Konnektor zeigt „starter" |
| Higgsfield Credits | 96 Credits verbraucht (278 → 182); davon 12 im Manifest belegt | Konnektor; `manifest.json` |
| Upload-Post, Konten, Domains | 0 (nicht angelegt) | – |
| Claude | im bestehenden Max-Abo, kein Zusatzbetrag | – |

Gemessene Kosten je fertigem 75-Sekunden-Video (Stimme): 0,0155 bis 0,0188 USD. Renderzeit je Video am Laptop: 1,5 bis 8 Minuten (`fn.cli costs`).

### 6.6 Markennamen (Prüfung 29./30.10.2026)

Ausgeschlossen: PromptPilot (EU-Marke 019235961, eingetragen, Kl. 9/42, Lemon Inc.), VelvetGlow (EU-Marke 019139965, eingetragen 2025, Kl. 3; UK 00003535497, Kl. 3), TorqueLab (US-Marke 77750022, Kl. 9, Mountz Inc.; TikTok-Konto gleicher Nische). TitanWorks generisch und belegt; TailoredCode, RiseTheory, IronArchive, GlitchMango auf den Plattformen belegt. Details: `02 Marke\Namensrecherche 2026-10-29.md`. Die Prüfung ist eine Vorprüfung, keine anwaltliche Markenrecherche.

### 6.7 Nicht ermittelbar (mit Grund)

- Vergütung je 1.000 Views bei TikTok oder YouTube: nicht veröffentlicht; Creator-Angaben in YouTube-Videos sind Marketing.
- Tatsächliche Nachfrage je Nische: keine Marktdaten erhoben.
- Gemini-TTS-Free-Tier-Limits: nur hinter Google-Login sichtbar.
- Ob Upload-Post einen auditierten TikTok-Client hat: nicht dokumentiert.
- Ob Instagram-Reels auf das API-Tageslimit zählen: nicht dokumentiert.
- YouTube: ab wann die „unverifiziert = privat"-Regel aufgehoben wurde: kein Changelog-Eintrag gefunden.
- Rendergeschwindigkeit HyperFrames auf der RTX 5080 allgemein: nur eigene Messwerte (siehe 6.5), keine Herstellerangabe.
- Ob die drei Higgsfield-Hintergrundclips (`bg_*`) abgenommen sind: nicht im Manifest eingetragen.

---

## 7. Entscheidungen

### 7.1 Getroffen

| Entscheidung | Datum | Pro | Contra |
|---|---|---|---|
| Windows-Laptop statt Mac mini | 29.10. | stark (RTX 5080, 32 GB), Bauplan des Kollegen ist Windows | Dauerbetrieb, Hitze, Speicher C: knapp |
| Kein VPN, Rewards nicht einplanen, System Rewards-fähig bauen | 29.10. | regelkonform, kein Sperrrisiko | TikTok bringt aus Österreich vorerst kein Plattformgeld |
| Publisher Upload-Post, austauschbar | 29.10. | einziger geprüfter Weg zu öffentlichen TikTok-API-Posts, setzt KI-Labels aller drei Plattformen, MCP, günstig | Abhängigkeit von einem Drittanbieter; Audit-Status von TikTok nicht belegt |
| Neun Marken in Phase 1 gestalten, Veröffentlichung zuerst Promptwerk und Scutoria | 29.10. | Architektur einmal, Fachnischen zuerst | viel Gestaltungsarbeit vor dem ersten Post |
| Markennamen: Promptwerk (Claude-Workflows), Scutoria (KI und Sicherheit), Revlore (Motorentechnik, Handles nur als Variante frei), Gigastruct (Megakonstruktionen), Suitwerk (Herrenstil, Reserve Lapelore), Gritwerk (Motivation), Frontlore (Militärgeschichte, Reserve Armorlore), Dewlane (Beauty), Zonkfruit (Brainrot) | 30.10. | markenrechtlich unauffällig in TMview, Domains teils frei | drei „-werk"-Namen machen Herkunft erkennbar; Handles teils nur als Variante |
| DE zuerst, EN parallel, ein Konto je Marke | 29.10. | halbe Kontenzahl | gemischte Zielgruppe je Konto |
| Slots 12:00, 14:00, 18:00 | 29.10. | – | Annahme zur Sprachverteilung unbestätigt |
| Freigabe automatisch, Risiko „hoch" manuell | 29.10. | Automatisierung | Fehler gehen ohne Blick hinaus; Claude empfiehlt erste 20 je Marke manuell (nicht beschlossen) |
| Gemini TTS | 29.10. | Cent-Beträge je Video | Qualität gegen ElevenLabs nicht verglichen |
| KI-Clips erst ab Phase 3 | 29.10. | Budget | inzwischen durch Higgsfield-Test für Scutoria vorgezogen |
| Budget 50 €/Monat | 29.10. | – | Upload-Post Professional plus Higgsfield würden es sprengen |
| Laptop 24/7, C: ohne externe SSD | 29.10. | – | C: sank von 61 auf 43,7 GB |
| Regie-System statt Folien-Template | 30.10. | adressiert beide Kritiken | mehr Komplexität im Renderer |
| Scutoria nutzt das bestehende Scutoria-Designsystem | 30.10. | Markenkonsistenz mit Website und Produkten | einige Markenbuchregeln (Größen, Anrede) für Video angepasst |
| Anrede im Scutoria-Video „du" | 30.10. | Kurzvideo-üblich | weicht vom Markenbuch („Sie") ab |
| Länge bleibt 65–90 s | 29./30.10. | Rewards-Fähigkeit | Kritik empfahl 45 s für Kurzvideo-Tempo |
| Higgsfield einmalig als Asset-Fabrik, Claude Code als Renderer | 30.10. | filmischer Look, danach keine laufenden Kosten | KI-Look, Konsistenz zwischen Clips; Credits |

### 7.2 Offen

| Frage | Pro | Contra |
|---|---|---|
| Fassung A3.1 (nur Claude Code) einfrieren oder Fassung B (mit Higgsfield) abwarten | A3.1 ist fertig, ohne Folgekosten | Mitte und unteres Drittel wirken in ruhigen Momenten noch leer |
| Slot-Annahme: 3 Posts je Konto und Tag (Sprachen wechseln) oder 6 (3 DE + 3 EN) | 3: weniger Produktion, Cap weit unterschritten | 6: beide Sprachen täglich, doppelte Produktion |
| Erste 20 Videos je Marke manuell freigeben | Kalibrierung der Prüfregeln | widerspricht „automatisch" |
| Restliche Higgsfield-Clips (4 offen) erzeugen | vollständige Fassung B | Credits (Kernpaket laut Freigabevorlage 96 Credits bei 8 Clips) |
| Codex-Briefings übernehmen oder verwerfen | vollständige Szenensysteme für alle neun Marken | nicht mit Repository und Markenbuch abgeglichen; teils andere Annahmen |
| Bildschirmaufnahme der Claude-Einstellungen liefern | macht UI-Szene echt, hebt `schematic_ui` auf | Stefans Aufwand; Demo-Konto ohne persönliche Daten nötig |
| Gewerbe neu oder Scutoria-Gewerbe erweitern | – | nicht ermittelt, welches Gewerbe für Scutoria besteht |
| Erster Commit | Sicherung des Stands | Stefan hat ihn noch nicht beauftragt |

---

## 8. Probleme, Fehler, Risiken

| Problem / Risiko | Stand |
|---|---|
| Erste Phase-1-Meldung brach ab („Nutzungslimit") | gelöst durch Neustart der Runde; Ursache Claude-Nutzungslimit, Wiederholung möglich |
| Gemini-Schlüssel in `.env.example` | nach `.env` verschoben, Vorlage geleert, vor jedem Commit; Stefan erneuert nicht |
| Netzabbrüche: `WinError 10053` bei Gemini; `ECONNREFUSED` in der Phase-1-Sitzung; Dateiübertragung ans Handy brach bei 28 MB ab | jeweils wiederholt bzw. nur in der Desktop-App sichtbar; Ursache vermutlich Netz im Einsatz, nicht geprüft |
| Hintergrundlauf der Testvideos gestoppt | sieben Videos ohne Stimme, bewusst liegen gelassen |
| Erstes Video wirkte wie Folien | gelöst durch Regie-System, A/A2/A3 |
| Falsche Palette für Scutoria | gelöst (A3); Prompt-Blatt Fassung 1 ungültig, Fassung 2 gültig |
| UI-Szene nur schematisch | offen, braucht Stefans Bildschirmaufnahme |
| Higgsfield-Manifest unvollständig (96 Credits verbraucht, 12 belegt) | offen; Higgsfield-Sitzung muss nachtragen |
| Speicher C: fällt (61 → 43,7 GB in einem Tag) | Mindestwert 30 GB im Code; Stefan wollte selbst aufräumen |
| YouTube-Regeländerung ab 01.02.2027 | strategisches Risiko für Werbeerlöse aus Shorts |
| „Inauthentic content" / Unoriginalität | Gegenmaßnahme: Quellen, eigener Blickwinkel, Regie, Fachnischen |
| TikTok-API-Audit | über Upload-Post; Test beim ersten Post |
| Claude-Max-Limits bei Vollausbau (bis 54 Renders/Tag) | messen; API-Schlüssel als Ausweichweg |
| Budget 50 €/Monat gegen Upload-Post Professional (50 USD) plus Higgsfield (19 €) | bei mehr als 5 Marken nicht haltbar; je Phase neu vorlegen |
| Musikrechte | keine Musik im Video bisher; Lizenzquelle fehlt |
| Codex-Ordner verweist auf `AGENTS.md`, die nicht existiert | unklar, ob Stefan sie woanders hat |
| Übersicht in Google Drive hinkt hinterher (Stand 06:00) | nach diesem Bericht nachziehen |

---

## 9. Offene Aufgaben und nächste Schritte (Reihenfolge, Abhängigkeiten)

1. **Übersicht in Google Drive aktualisieren** (Regie, A3.1, Scutoria-Design, Anrede du, Higgsfield Starter, Codex-Briefings, Verweis auf diesen Bericht) und Log-Eintrag schreiben. Keine Abhängigkeit.
2. **Higgsfield-Sitzung abschließen lassen:** Manifest und `LICENSE.md` für alle erzeugten Clips nachtragen (Modelle, Job-IDs, Credits, Abnahme), Clips abnehmen (keine Schrift/Logos, Palette, Loop), restliche Clips nur nach Stefans Freigabe. Abhängig von Stefans Freigabe der Credits.
3. **Fassung B Scutoria rendern** (gleiche Regie wie A3.1, Higgsfield-Clips als Hintergründe und Hero), Vorher-Nachher A3.1 gegen B. Abhängig von 2.
4. **Stefan entscheidet** A oder B (oder Mischung) und friert Scutoria als `brand_version 1.0` ein. Abhängig von 3.
5. **Bildschirmaufnahme** der Claude-Einstellungen (Anleitung im Szenenplan: claude.ai › Settings › Privacy, Schalter „Help Improve our AI models", Demo-Konto, Datei `brands\ai_security\assets\ui\claude-privacy-settings.mp4` plus `.png`), dann UI-Szene echt einbauen. Abhängig von Stefan.
6. **Promptwerk** nach demselben Ablauf (Fassung A nur Claude Code, dann gegebenenfalls Higgsfield). Braucht echte Bildschirmaufnahmen aus einem Demo-Projekt (Stefan: „ja"). Danach die übrigen sieben Marken nacheinander.
7. **Konten und Namen sichern** (Stefan): Handles laut `Marken.md`, Domains .at/.io, je Marke Gmail, YouTube, Instagram Creator, TikTok Personal; gestaffelt (YouTube: höchstens 2 Kanäle je Telefonnummer und Jahr; Instagram: höchstens 5 Konten je E-Mail; TikTok: eine E-Mail je Konto). Impressum mit Scutoria-Adresse. Zuerst Promptwerk und Scutoria.
8. **Upload-Post** (Stefan): Konto, Basic, zwei Profile, OAuth zu den drei Plattformen, `UPLOADPOST_API_KEY` in `.env`. Dann Claude: NOT_VERIFIED-Endpunkte gegen die Dokumentation prüfen, Dry-Run, erster echter Post je Plattform mit Freigabe; prüfen, ob TikTok-Post öffentlich ist und Labels sichtbar sind. Abhängig von 7.
9. **Handy-Zentrale** (Claude-Artefakt mit Datenbank: Themenwahl, Vorschau, Freigabe, Stopp bis zur Slot-Zeit). Abhängig von 8 für echte Posts, kann vorher gebaut werden.
10. **Aufgabenplanung registrieren** (`automation\register_tasks.ps1`, mit Administratorrechten durch Stefan), Energieeinstellungen prüfen. Abhängig von 8.
11. **30-Tage-Kalender** je aktiver Marke füllen, Puffer 7 Tage vorproduzieren. Abhängig von 4 und 6.
12. **Gewerbe und Steuerberatung** (Stefan), spätestens vor dem ersten bezahlten Werbepartner.
13. **Musik:** lizenzfreie oder lizenzierte Quelle wählen, Nachweise in `08 Recht und Verwaltung\Lizenzen`.
14. **Erster Commit** im Repository, wenn Stefan es sagt (vorher prüfen, dass `.env` ignoriert ist und keine Schlüssel in Dateien stehen).
15. Phase 3 laut Ablaufplan: Kommentar-Beantwortung, Media-Kit je Marke, Affiliate.

---

## 10. Offene Fragen an Stefan

1. Fassung A3.1 so einfrieren, oder erst Fassung B mit Higgsfield abwarten und vergleichen?
2. Wie viele Higgsfield-Credits darf die Clip-Sitzung noch für Scutoria ausgeben (182 übrig)? Sollen danach auch für andere Marken Clips entstehen?
3. Slots: 3 Posts je Konto und Tag mit wechselnder Sprache, oder 6 (3 DE + 3 EN)?
4. Gilt die Empfehlung, die ersten 20 Videos je Marke von Hand freizugeben, oder sofort automatisch?
5. Was sind die „Codex"-Briefings in `02 Marke\_Higgsfield-Briefings (Codex, 2026-10-30)`, und sollen sie übernommen, abgeglichen oder verworfen werden? Gibt es die dort erwähnte `AGENTS.md` an einem anderen Ort?
6. Wann kommt die Bildschirmaufnahme der Claude-Einstellungen (und die Demo-Aufnahmen für Promptwerk)?
7. Ist der Higgsfield-Starter monatlich oder jährlich gebucht, und soll er nach der Asset-Erzeugung gekündigt werden?
8. Besteht für Scutoria bereits ein Gewerbe, und welches? Gibt es eine Steuerberatung?
9. Darf der Stand im Repository jetzt committet werden?
10. Wie soll Speicher auf C: frei werden (Stefan wollte selbst löschen; aktuell 43,7 GB)?
11. Budget: Bleibt es bei 50 €/Monat, auch wenn ab etwa sechs Marken Upload-Post Professional nötig wird?

---

## 11. Begriffe und Abkürzungen

| Begriff | Bedeutung |
|---|---|
| Faceless | Kanäle ohne sichtbare Person; Stimme und Bild KI-erzeugt |
| Creator Rewards (CRP) | TikToks Vergütungsprogramm für Videos über 1 Minute; nicht in Österreich |
| YPP | YouTube-Partnerprogramm |
| Upload-Post | Multi-Plattform-Upload-Dienst mit API und MCP-Server |
| MCP | Model Context Protocol; Schnittstelle, über die Claude Werkzeuge externer Dienste nutzt |
| Konnektor | in claude.ai bzw. Claude Code eingebundene MCP-Verbindung |
| TTS | Text-to-Speech, Sprachausgabe (hier Gemini) |
| HyperFrames | Open-Source-Renderer (HeyGen), der HTML/Three.js-Szenen zu MP4 rendert |
| NVENC | Videoencoder der NVIDIA-Grafikkarte |
| faster-whisper | Spracherkennung für Wortzeiten der Untertitel |
| Regie-System (direction) | Hook-Engine, Story-Engine, fünf Szenentypen, Prüfungen im Repository |
| Hook | erste Sekunden eines Videos, die zum Weiterschauen bringen |
| Beat | ein Abschnitt der Dramaturgie mit einer Funktion (Hook, Problem, Erklärung …) |
| Fassung A / A2 / A3 / A3.1 | Scutoria-Video nur mit Claude Code: A erste Regie-Fassung, A2 nach zweiter Kritik, A3 im Scutoria-Design, A3.1 Feinschliff |
| Fassung B | Scutoria-Video mit Higgsfield-Clips als Hintergründe, Text und Grafik weiter aus dem Renderer |
| Asset-Fabrik | Higgsfield einmalig für wiederverwendbare Clips je Marke |
| Style-Lock, `brand_version` | eingefrorenes Design einer Marke |
| Zustände | PLANNED, RESEARCHED, SCRIPTED, RENDERED, VALIDATED, APPROVED, SCHEDULED, PUBLISHED, VERIFIED; daneben NEEDS_RESEARCH, BLOCKED, HUMAN_REVIEW, REJECTED, FAILED |
| HUMAN_REVIEW | Video wartet auf Stefan (z. B. schematische UI, Risiko hoch) |
| `schematic_ui` | Prüfvermerk: UI-Szene ist ein Schema statt einer echten Aufnahme |
| NOT_VERIFIED / UNVERIFIED | Endpunkt bzw. Aussage nicht gegen Primärquelle bestätigt; wird nicht verwendet |
| Dry-Run | Probelauf ohne echte Veröffentlichung |
| KI-Label | `is_aigc` (TikTok), `is_ai_generated` (Instagram), `containsSyntheticMedia` (YouTube) |
| Art. 50 AI Act | EU-Transparenzpflicht für KI-Inhalte, seit 02.08.2026 |
| Deployer | Betreiber eines KI-Systems im Sinne des AI Act |
| Scutum-Marke | Scutoria-Logo (Schildkontur) |
| Marker | Scutoria-Kennzeichen Fakt, Auslegung, Unsicher, Lücke |
| § 46 / § 56 BDG | Beamten-Dienstrechtsgesetz: Verschwiegenheit / Nebenbeschäftigung |
| WKO, USP, SVS | Wirtschaftskammer Österreich, Unternehmensserviceportal, Sozialversicherung der Selbständigen |
| TMview, EUIPO | Markenregister-Suche; Amt der EU für geistiges Eigentum |
| Credits | Higgsfield-Verrechnungseinheit |
| Codex | vermutlich ein anderes KI-Werkzeug, mit dem die Briefings im Ordner `_Higgsfield-Briefings` erstellt wurden (nicht geprüft) |
