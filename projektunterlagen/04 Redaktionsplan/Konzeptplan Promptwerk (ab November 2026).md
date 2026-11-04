# Konzeptplan Promptwerk (ab November 2026)

Stand 02.11.2026, Claude. Marke Promptwerk, Marken-ID `claude_workflows`. Entwurf zur Freigabe durch Stefan, ändert keinen Kalender und keinen Redaktionsplan.
Grundlagen: `02 Marke\Promptwerk\Format-Bibel.md` (Format „Echtlauf“, freigegeben 02.11.2026), Kalender `C:\Automation\faceless-network\data\calendars\claude_workflows_2026-11.json` (84 Themen, 168 Zeilen, Quellen: Claude-Code- und Plattform-Doku, abgerufen 01.11.2026), `04 Redaktionsplan\Themen- und Kalenderplan Promptwerk (09.11.–06.12.2026).md`, Aufzeichnungen und Spezifikationen in `C:\Automation\faceless-network\brands\claude_workflows\echtlauf\` (Stand 02.11.2026).

## Kurzkonzept

- **Versprechen:** Echte Aufgabe, echter Ablauf, echtes Ergebnis, mit Fehlern und Grenzen. Claude Code läuft in einem Testordner mit Beispieldaten; das Terminal im Bild ist die Aufzeichnung dieses Laufs, mit Datum, Version und Modell-ID im Stempel.
- **Zielgruppe (Annahme, in den Unterlagen nicht ausdrücklich festgelegt):** Leute, die Claude Code im Alltag nutzen oder ausprobieren wollen und wissen möchten, was eine Funktion wirklich tut; DE und EN.
- **Format:** nur Reels, „Echtlauf“ 65–90 s (Zielwert 70 s): Auftrag, Ausgangslage, Regel, zwei bis drei Läufe mit Zeitstempeln, Ergebnis mit Wiederholungszahl, Protokollkarte. Kein YouTube-Langformat geplant.
- **Reihen:** Hält das? (Schutzfunktion bis zur Grenze) · Eine Aufgabe, ein Lauf (Vorher-nachher einer Datei) · Doku gegen Wirklichkeit (Behauptung mit zwei Läufen geprüft, ersetzt Mythos-Check) · Gleicher Auftrag, anderer Schalter (zwei Einstellungen nebeneinander).
- **Takt:** je Tag 3 DE (12:00, 14:00, 18:00) und 3 EN (15:00, 20:00, 23:00). Jede EN-Fassung braucht eine eigene englische Aufzeichnung (`<id>-en`), nie eine deutsche Aufzeichnung englisch vertont.
- **Grenzen:** jeder Lauf mindestens zweimal (`--repeat 2`), alle Läufe zählen, nur Testordner unter `C:\Automation\promptwerk-sandbox\`, abgeschottete Läufe, Standardmodell Haiku; nur behaupten, was gezeigt wurde; Hinweis „Verhalten kann sich mit Version und Modell ändern“.

## Neustart ab 04.11.2026: Bildaufbauten und Takt

Stand 03.11.2026. Stefan hat das Testvideo „Dubletten“ (Nr. 52) am 03.11. freigegeben, mit der Korrektur „Geräusche zu laut“. Format, Bildwelt und Tonebene des Testvideos sind die Vorlage. Stefans Kritik war „die Videos sind alle gleich“. Deshalb hat jede Reihe einen eigenen Bildaufbau, und an einem Tag laufen nie zwei Themen mit demselben Aufbau. Allen Aufbauten gemeinsam:
- die echte Aufzeichnung;
- KI-Bilder nur vom Arbeitsplatz rund um die Aufgabe, nie vom Bildschirm, ohne Gesichter, markiert als „KI-Bild“;
- Tonebene `tech` mit leisem Bett.

| Aufbau | Reihe | Ablauf im Bild | Einstieg |
|---|---|---|---|
| **A Vorher-nachher** (wie Testvideo) | Eine Aufgabe, ein Lauf | Foto → Ausgangsdatei (rec_setup „before“, bei einer CSV als Liste mit markierten Zeilen rec_table) → Lauf (rec_replay) → Ergebnisdatei (rec_setup „after“, bei einer CSV Zeilenstreifen und Zähler rec_diff) → Antwortkarte (rec_answer) → Schlussfoto | KI-Foto oder Kling-Clip vom Arbeitsplatz, Frage darüber |
| **B Duell mit Stempel** | Hält das? | Regeldatei mit Doku-Zitat (rec_rule) → Läufe nacheinander, je mit rotem oder grünem Stempel (rec_replay) → Ergebnistafel (rec_result) → Protokollkarte (rec_protokoll) | Terminal-Einstieg: Befehl tippt sich (rec_auftrag), kein Foto am Anfang |
| **C Doku gegen Protokoll** | Doku gegen Wirklichkeit | Regeldatei mit Zitat und Quelle (rec_rule, ein reines Zitat-Bild gibt es nicht) → Lauf (rec_replay) → Antwortkarte mit markierter Stelle (rec_answer) → Ergebnistafel (rec_result) → Foto als Schluss | Zitat und Regeldatei, Foto erst am Schluss |
| **D Zwei Schalter** | Gleicher Auftrag, anderer Schalter | Beide Läufe nacheinander (rec_replay) → Ergebnistafel mit Messwert je Lauf (Tokens oder Sekunden, rec_result) → Antwortkarte des auffälligeren Laufs (rec_answer); das geteilte Bild (rec_split) nur bei einer CSV-Aufzeichnung wie dem Testvideo | Foto mit zwei markierten Schaltern oder Notizzetteln |

Die gebauten Aufbauten und die Aufzeichnung je Thema stehen in `brands\claude_workflows\aufbauten.yaml` (Stand 03.11. abends, geprüft). `rec_table`, `rec_diff` und `rec_split` lesen eine CSV-Datei samt Zeilenzahl und laufen darum nur mit der Aufzeichnung `kunden-dubletten`.

**Wechselregel:** An einem Tag haben die zwei Themen verschiedene Aufbauten. Derselbe Aufbau kommt höchstens jeden zweiten Tag an derselben Tagesstelle. Die Fotos kommen in dieser Reihenfolge:
1. aus der Realbild-Bibliothek `brands\claude_workflows\assets\higgsfield\library\` (29 Bilder, 1 Clip, Tabelle „Realbilder (03.11.2026)“ in `02 Marke\Promptwerk\Vorlage Bibliothek.md`; im Plan als `"src": "library/<datei>"`);
2. danach aus dem Testvideo-Material `assets\higgsfield\tv_*`. Ein neues Bild höchstens je Thema (Nano Banana Pro, 2 Credits).

**Higgsfield-Budget (Stefan, 03.11.2026, „Vorschlag so“):**
- Tagesproduktion 33 Credits für Promptwerk bis 30.11., höchstens 2 Credits je Thema.
- Mehr nur mit Begründung über die Hauptsitzung (Reserve 152).
- Die Realbild-Bibliothek (etwa 70 Credits) baut die Bibliotheken-Sitzung; bis dahin dient das Testvideo-Material.
- Eigenes Material nie in `library\`, sondern daneben mit eigener `LICENSE.md`.
- Der Verbrauch steht je Thema im Prüfbericht (`Veröffentlichung.md` › Produktion) und in der Tabelle hier.

| Datum | Thema | Credits | Stand |
|---|---|---|---|
| 03.11. | Testvideo Dubletten (DE und EN), 4 Bilder und 2 Kling-Clips | 28 | aus dem Testvideo-Budget, vor der Verteilung |

**Takt ab 04.11.:** 2 Themen je Tag, jedes DE und EN, also 4 Videos.
- **Reihenfolge je Thema:** Aufzeichnung DE und EN → Skript DE → Stimme DE → Render DE → EN aus denselben Szenen.
- **Stimmen:** Flash, höchstens 4 Anfragen je Tag; dieselbe Stimme Kore in DE und EN.
  - Deutsche Stimme über `brands\claude_workflows\echtlauf\voice_tts.py --say Claude=Klohd`. Die Schreibweise gilt nur im TTS-Text, die Untertitel behalten „Claude“. Whisper-Gegenprobe: Claude 4, Cloud 0 am 03.11.
  - Englische Aufträge enden mit „Reply in English.“, sonst antwortet Claude bei deutschen Testdaten auf Deutsch (Aufzeichnung 03.11.).
- **Render und Export:** Render über `scripts\render_queue.py`; Export wie beim Testvideo mit Sprachkennung; nichts veröffentlichen.

**Erste Tage** (Themen mit Aufzeichnung DE und EN vom 02.11.; vor dem Export `record_run.py --check`, die Aufzeichnungen bekommen neue Szenen nach Aufbau):

| Tag | Thema 1 (Aufbau) | Thema 2 (Aufbau) |
|---|---|---|
| 04.11. | Nr. 3 CLAUDE.md gegen Hook (B) | Nr. 4 Eine Aufgabe von Anfang bis Ende (A) |
| 05.11. | Nr. 6 Ganze Datei lesen oder gezielt suchen (D) | Nr. 1 Kurze gegen lange CLAUDE.md (C) |
| 06.11. | Nr. 8 Formatieren nach jeder Änderung (B) | Nr. 2 Was Claude zu Beginn liest (D) |
| 07.11. | Nr. 9 Ein Subagent mit eigenen Werkzeugen (B) | Nr. 7 Ein MCP-Server, echt verbunden (D) |
| 08.11. | Nr. 10 Welche Werkzeuge eine Freigabe brauchen (B) | Nr. 11 Berechtigungsregel gegen Hook (D) |

Ab 09.11. folgen die Themen ohne Aufzeichnung in der Reihenfolge der Tabelle unten, je Thema zuerst die Aufzeichnung (DE und EN). Die Zeilen „Takt“ im Kurzkonzept oben (3 + 3 je Tag) gelten nicht mehr.

## Vorschläge

Reihenfolge: zuerst die 11 Kalenderthemen mit vorhandener Aufzeichnung (alle Läufe 2 von 2 gleich, `outcome.json`), dann weitere Kalenderthemen mit einem Lauf-Entwurf, dann neue Vorschläge. Die Hook-Idee ist nach Format-Bibel die Frage des Laufs, nicht sein Ergebnis. Risiko: Kalenderwert (`low` = niedrig, `medium` = mittel), bei zwei Themen von Claude auf „hoch“ gesetzt, weil der Lauf selbst Schutzschalter abschaltet.

| Nr | Thema/Titel | Reihe | Format | Hook-Idee in einem Satz | Quellenstand | Risiko |
|---|---|---|---|---|---|---|
| 1 | Kurze gegen lange CLAUDE.md (Mythos: Je länger die CLAUDE.md, desto besser) | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Findet Claude eine bestimmte Regel in einer CLAUDE.md mit 240 Regeln genauso wie in einer mit 4? | belegt im Kalender claude_workflows-20261109-1-de; Aufzeichnung `claude-md-lang` (DE und EN); Export in `05 Produktion\Promptwerk\2026-11` vorhanden | niedrig |
| 2 | Was Claude zu Beginn liest (CLAUDE.md – die Datei, die Claude Code zuerst liest) | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Kennt Claude ein Codewort, das nur in der CLAUDE.md steht, ohne danach zu suchen? | belegt im Kalender claude_workflows-20261109-2-de; Aufzeichnung `claude-md-laden` (DE und EN) | niedrig |
| 3 | CLAUDE.md gegen Hook (Hooks – Regeln, die Claude Code nicht umgehen kann) | Hält das? | Reel Echtlauf 65–90 s | Hält eine Regel in der CLAUDE.md Claude davon ab, die .env zu ändern, oder braucht es einen Hook? | belegt im Kalender claude_workflows-20261109-3-de; Aufzeichnung `hook-env` (4 Läufe, DE und EN); Export vorhanden | niedrig |
| 4 | Eine Aufgabe von Anfang bis Ende (Wie Claude Code eine Aufgabe abarbeitet) | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Ein Beispielskript rechnet falsch: Wie geht Claude vor, einmal mit Bash, einmal ohne? | belegt im Kalender claude_workflows-20261110-1-de; Aufzeichnung `aufgabe-ablauf` (DE und EN) | niedrig |
| 5 | Deny-Regel gegen das Lesen der .env (Pilot) | Hält das? | Reel Echtlauf 65–90 s | Hält die Deny-Regel auch, wenn Claude die Datei über Bash oder ein Skript lesen will? | belegt im Kalender claude_workflows-20261110-2-de; Aufzeichnung `deny-env` (4 Läufe); Pilot-Export DE und EN vorhanden | mittel |
| 6 | Ganze Datei lesen oder gezielt suchen (Mythos: Mehr Kontext ist immer besser) | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Findet Claude einen Ortsnamen in einer langen Datei mit weniger Aufwand, wenn es suchen darf? | belegt im Kalender claude_workflows-20261111-1-de; Aufzeichnung `kontext-suche` (DE und EN) | niedrig |
| 7 | Ein MCP-Server, echt verbunden | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Beantwortet Claude eine Doku-Frage anders, wenn ein MCP-Server verbunden ist? | belegt im Kalender claude_workflows-20261113-1-de; Aufzeichnung `mcp-docs` (DE und EN) | niedrig |
| 8 | Formatieren nach jeder Änderung | Hält das? | Reel Echtlauf 65–90 s | Ist die Datei nach Claudes Änderung formatiert, einmal ohne und einmal mit PostToolUse-Hook? | belegt im Kalender claude_workflows-20261114-3-de; Aufzeichnung `format-hook` (DE und EN) | niedrig |
| 9 | Ein Subagent mit eigenen Werkzeugen | Hält das? | Reel Echtlauf 65–90 s | Kann ein Subagent, der nur Read bekommen hat, trotzdem eine Datei ändern? | belegt im Kalender claude_workflows-20261115-1-de; Aufzeichnung `subagent-werkzeuge` (DE und EN, Fassung v1 verworfen) | niedrig |
| 10 | Welche Werkzeuge eine Freigabe brauchen (Die Werkzeuge von Claude Code) | Hält das? | Reel Echtlauf 65–90 s | Read, Write, Bash: Was darf Claude ohne Freigabe, und wo hält es an? | belegt im Kalender claude_workflows-20261115-2-de; Aufzeichnung `werkzeuge-freigabe` (3 Läufe, Fassung v1 verworfen) | niedrig |
| 11 | Berechtigungsregel gegen Hook | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Port ändern, Debug einschalten: Was stoppt eine Berechtigungsregel, was ein Hook? | belegt im Kalender claude_workflows-20261115-3-de; Aufzeichnung `regel-oder-hook` (3 Läufe) | mittel |
| 12 | Mythos: Checkpoints ersetzen Git | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Kommt eine Datei zurück, wenn ein Bash-Befehl sie gelöscht hat und man zum Checkpoint zurückgeht? | belegt im Kalender claude_workflows-20261112-3-de; Lauf noch nicht aufgezeichnet; Zurückspringen ist interaktiv, Umsetzbarkeit im Recorder prüfen | niedrig |
| 13 | CLAUDE.md oder Skill? | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Dieselbe Anweisung einmal in der CLAUDE.md, einmal als Skill: Wann greift sie im Lauf? | belegt im Kalender claude_workflows-20261110-3-de; Lauf offen; Skills brauchen Slash-Befehle, Abschottung gegen Stefans eigene Skills vorher klären | niedrig |
| 14 | Deinen ersten Skill anlegen | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Legt Claude aus einer kurzen Beschreibung einen Skill an, der im nächsten Lauf auch geladen wird? | belegt im Kalender claude_workflows-20261111-3-de; Lauf offen; Abschottung wie Nr. 13 | niedrig |
| 15 | Skill oder Subagent? | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Dieselbe Rechercheaufgabe als Skill und als Subagent: Was landet im Hauptkontext? | belegt im Kalender claude_workflows-20261114-1-de; Lauf offen (Messwert `input_tokens`) | niedrig |
| 16 | Mythos: Viele Skills verstopfen den Kontext | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Steigen die Eingabe-Tokens, wenn im Testordner viele Skills liegen statt keiner? | belegt im Kalender claude_workflows-20261114-2-de; Lauf offen | niedrig |
| 17 | Mythos: WICHTIG in Großbuchstaben wirkt besser | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Hält sich Claude besser an eine Regel, wenn WICHTIG in Großbuchstaben davorsteht? | belegt im Kalender claude_workflows-20261116-1-de; Beispiel in Format-Bibel 4.3; Lauf offen | niedrig |
| 18 | Benachrichtigung, wenn Claude auf dich wartet | Hält das? | Reel Echtlauf 65–90 s | Meldet sich ein Notification-Hook, sobald Claude auf eine Freigabe wartet? | belegt im Kalender claude_workflows-20261116-3-de; Lauf offen; ob das Ereignis im Modus `-p` auslöst, vorher prüfen | niedrig |
| 19 | Einen eigenen Subagenten bauen | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Ruft Claude einen selbst angelegten Subagenten auf, wenn die Aufgabe zu seiner Beschreibung passt? | belegt im Kalender claude_workflows-20261117-2-de; Lauf offen (Kalendernotiz: `/agents` legt laut Doku nichts an) | niedrig |
| 20 | Opus, Sonnet oder Haiku? | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Dieselbe kleine Aufgabe mit drei Modellen: Was unterscheidet sich an Ergebnis, Dauer und Werkzeugaufrufen? | belegt im Kalender claude_workflows-20261117-3-de; Lauf offen; einziges Thema mit Sonnet und Opus (Format-Bibel 6.10) | niedrig |
| 21 | Mythos: /clear löscht Claudes Gedächtnis | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Weiß Claude in einer frischen Sitzung noch, was in der CLAUDE.md steht? | belegt im Kalender claude_workflows-20261118-1-de; Lauf offen; `/clear` läuft im Modus `-p` nicht, Ersatz (neue Sitzung) im Video offen benennen | niedrig |
| 22 | 4 Hook-Ereignisse, die du kennen solltest | Hält das? | Reel Echtlauf 65–90 s | Welche Hook-Ereignisse feuern in einem kurzen Lauf, und in welcher Reihenfolge? | belegt im Kalender claude_workflows-20261118-2-de; Lauf offen (Hooks schreiben je Ereignis eine Zeile in eine Protokolldatei) | niedrig |
| 23 | Regeln nur für bestimmte Ordner: .claude/rules/ | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Greift eine Regel für den Ordner `tests` auch, wenn Claude im Ordner `src` arbeitet? | belegt im Kalender claude_workflows-20261118-3-de; Lauf offen | niedrig |
| 24 | Mythos: bypassPermissions ist auf dem eigenen Rechner harmlos | Hält das? | Reel Echtlauf 65–90 s | Was führt Claude im Testordner aus, wenn gar keine Freigabe mehr gefragt wird? | belegt im Kalender claude_workflows-20261119-3-de (Sicherheitsthema); Lauf offen | hoch |
| 25 | CLAUDE.md aufteilen mit @-Importen | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Kennt Claude eine Regel, die nur in einer per @ importierten Datei steht? | belegt im Kalender claude_workflows-20261120-1-de; Lauf offen | niedrig |
| 26 | MCP-Server: lokal, Projekt oder Benutzer | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Welcher Server ist im Lauf verfügbar, wenn er einmal im Projekt und einmal lokal eingetragen ist? | belegt im Kalender claude_workflows-20261120-2-de; Lauf offen; nur Projekt- und lokale Ebene im Testordner, keine Benutzerebene | niedrig |
| 27 | 4 Schalter für Claude Code in Skripten | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Dieselbe Frage im Modus `-p` einmal als Text, einmal als JSON: Was kommt heraus? | belegt im Kalender claude_workflows-20261120-3-de; Beispiel in Format-Bibel 4.4; Lauf offen | niedrig |
| 28 | Mythos: Subagenten sind gratis | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Braucht dieselbe Aufgabe mit Subagent mehr oder weniger Tokens als ohne? | belegt im Kalender claude_workflows-20261121-2-de; Lauf offen | niedrig |
| 29 | Planmodus – erst lesen, dann ändern | Hält das? | Reel Echtlauf 65–90 s | Ändert Claude im Planmodus eine Datei, wenn der Auftrag es ausdrücklich verlangt? | belegt im Kalender claude_workflows-20261122-1-de; Beispiel in Format-Bibel 4.1; Lauf offen | niedrig |
| 30 | Projekt oder lokal: welche settings.json gilt? | Hält das? | Reel Echtlauf 65–90 s | Das Projekt erlaubt einen Befehl, die lokale Einstellung verbietet ihn: Was gewinnt? | belegt im Kalender claude_workflows-20261122-3-de; Lauf offen; Benutzerebene bleibt wegen Abschottung außen vor, das im Video sagen | niedrig |
| 31 | Mythos: Eine geänderte CLAUDE.md wirkt sofort | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Bemerkt Claude in einer fortgesetzten Sitzung, dass die CLAUDE.md inzwischen geändert wurde? | belegt im Kalender claude_workflows-20261123-1-de; Lauf offen (mit `--continue`) | niedrig |
| 32 | Was Claude Code in großen Projekten nicht liest | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Findet Claude eine Angabe, die nur in einem tief verschachtelten Unterordner steht? | belegt im Kalender claude_workflows-20261123-2-de; Lauf offen | niedrig |
| 33 | Geprüftes JSON aus Claude Code holen (zusammen mit „Structured Outputs oder JSON per Prompt?“) | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Liefert Claude in zwei von zwei Läufen ein JSON, das das vorgegebene Schema besteht? | belegt im Kalender claude_workflows-20261123-3-de und -20261203-2-de; Lauf offen | niedrig |
| 34 | Standardmodus oder dontAsk? | Hält das? | Reel Echtlauf 65–90 s | Was passiert im Modus dontAsk mit einem Befehl, der nicht freigegeben ist? | belegt im Kalender claude_workflows-20261124-3-de (Sicherheitsthema); Beispiel in Format-Bibel 4.1; Lauf offen | mittel |
| 35 | Mythos: Claude Code ist nur für Code | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Aus drei Textnotizen soll eine Tabelle werden: Schafft Claude Code das ohne eine Zeile Programmcode? | belegt im Kalender claude_workflows-20261125-1-de; Aufgabe aus Format-Bibel 4.2; Lauf offen | niedrig |
| 36 | Zwei Aufgaben gleichzeitig mit --worktree (zusammen mit „Git-Worktrees“) | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Zwei Läufe ändern dieselbe Datei in zwei Worktrees: Kommen sie sich in die Quere? | belegt im Kalender claude_workflows-20261125-3-de und -20261201-1-de; Lauf offen; Testordner muss ein Git-Repo sein | niedrig |
| 37 | Mythos: Eine Read-Sperre blockiert jeden Zugriff | Hält das? | Reel Echtlauf 65–90 s | Die Read-Sperre steht, und Claude versucht es über `cat` und über ein Skript. | belegt im Kalender claude_workflows-20261126-3-de; die Aufzeichnung `deny-env` (Läufe L3 und L4) deckt genau diese Frage ab; eigener Lauf oder Wiederverwendung klären | mittel |
| 38 | Bash-Befehle in die Sandbox schicken | Hält das? | Reel Echtlauf 65–90 s | Kommt ein Bash-Befehl aus der Sandbox an eine Beispieldatei im Nachbarordner? | belegt im Kalender claude_workflows-20261127-1-de (Sicherheitshinweis: Grenzen laut Doku nennen); Lauf offen; beide Ordner unter `promptwerk-sandbox` | mittel |
| 39 | Effort – wie viel Claude nachdenkt (zusammen mit „Thinking oder Effort?“) | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Dieselbe Knobelaufgabe mit niedrigem und hohem Effort: Was ändert sich an Dauer und Ergebnis? | belegt im Kalender claude_workflows-20261127-2-de und -20261128-1-de; Standardwerte je Modell vor dem Skript erneut prüfen (Kalendernotiz); Lauf offen | niedrig |
| 40 | Die eingebauten Subagenten | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Welchen eingebauten Subagenten wählt Claude für eine reine Suchaufgabe? | belegt im Kalender claude_workflows-20261127-3-de (Liste vor dem Skript vollständig aus der Doku); Lauf offen | niedrig |
| 41 | Mythos: ultrathink ist ein Zauberwort | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Ändert das Wort „ultrathink“ im Prompt etwas an Dauer oder Ergebnis? | belegt im Kalender claude_workflows-20261128-2-de (Changelog 2.1.316); Lauf offen | niedrig |
| 42 | Tests erzwingen mit einem Stop-Hook | Hält das? | Reel Echtlauf 65–90 s | Hört Claude auf, solange der Test noch rot ist, wenn ein Stop-Hook das verbietet? | belegt im Kalender claude_workflows-20261128-3-de (Blockgrenze für Stop-Hooks erwähnen); Lauf offen | niedrig |
| 43 | Claude liest PDFs mit Diagrammen und Tabellen | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Liest Claude Code einen Wert aus der Tabelle einer Beispiel-PDF richtig ab? | belegt im Kalender claude_workflows-20261129-1-de (Plattform-Doku; Gültigkeit für Claude Code prüfen); Lauf offen | niedrig |
| 44 | Mythos: Jeder MCP-Server ist geprüft | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Folgt Claude einer Anweisung, die ein selbst gebauter Beispiel-Server in seine Antwort schreibt? | belegt im Kalender claude_workflows-20261130-1-de (Sicherheitsthema); Lauf offen; Server nur lokal und selbst geschrieben, Ausgang aus Sicht des Nutzers zeigen, keine Bauanleitung | hoch |
| 45 | Mythos: Auto Mode heißt alles erlauben | Hält das? | Reel Echtlauf 65–90 s | Was lässt der Auto Mode im Testordner durch, und wo hält er an? | belegt im Kalender claude_workflows-20261202-1-de (Sicherheitsthema); Lauf offen | mittel |
| 46 | Wenn Claude Code deine Einstellung ignoriert | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Dieselbe Einstellung in drei Fassungen (andere Datei, anderer Schlüssel, anderer Ort): In welchem Lauf greift sie? | belegt im Kalender claude_workflows-20261202-2-de; Lauf offen; Ergebnis erst nach der Aufzeichnung festhalten | niedrig |
| 47 | Screenshots direkt an Claude Code geben | Eine Aufgabe, ein Lauf | Reel Echtlauf 65–90 s | Liest Claude aus einem Beispiel-Screenshot die Fehlermeldung richtig ab? | belegt im Kalender claude_workflows-20261202-3-de; Lauf offen | niedrig |
| 48 | Mythos: Claude weiß schon, was du meinst | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Ein vager Auftrag gegen einen genauen: Was steht danach jeweils in der Ergebnisdatei? | belegt im Kalender claude_workflows-20261203-3-de; Lauf offen | niedrig |
| 49 | Mythos: Prompt-Caching muss man selbst einschalten (zusammen mit „Prompt-Caching in Claude Code“) | Doku gegen Wirklichkeit | Reel Echtlauf 65–90 s | Zeigt der zweite gleiche Lauf Cache-Treffer, ohne dass jemand etwas eingeschaltet hat? | belegt im Kalender claude_workflows-20261205-2-de und -20261126-1-de; Lauf offen (Messwert aus der JSON-Ausgabe) | niedrig |
| 50 | Bessere Antworten mit Beispielen im Prompt | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Schreibt Claude eine Liste Beispieladressen einheitlicher, wenn der Prompt ein Beispiel enthält? | belegt im Kalender claude_workflows-20261205-3-de; Lauf offen | niedrig |
| 51 | 3 Umgebungsvariablen für Claude Code | Gleicher Auftrag, anderer Schalter | Reel Echtlauf 65–90 s | Derselbe Lauf, einmal mit gesetzter Umgebungsvariable: Was ändert sich im Protokoll? | belegt im Kalender claude_workflows-20261206-2-de; Lauf offen | niedrig |
| 52 | Kundenliste mit Dubletten bereinigen | Eine Aufgabe, ein Lauf (neu) | Reel Echtlauf 65–90 s | Eine Beispiel-Kundenliste mit doppelten Einträgen: Wie viele bleiben übrig, und stimmt das? | Quelle zu prüfen (Aufgabe aus Format-Bibel 4.2, nicht im Kalender) | niedrig |
| 53 | Dateinamen nach Datum umbenennen | Eine Aufgabe, ein Lauf (neu) | Reel Echtlauf 65–90 s | Ein Ordner voller Beispielrechnungen soll einheitlich nach Datum heißen: Wie viele Werkzeugaufrufe braucht das? | Quelle zu prüfen (Aufgabe aus Format-Bibel 4.2) | niedrig |
| 54 | Den Fehler finden, der Test wird grün | Eine Aufgabe, ein Lauf (neu) | Reel Echtlauf 65–90 s | Ein Test ist rot: Findet Claude den Fehler, ohne den Test selbst zu ändern? | Quelle zu prüfen (Aufgabe aus Format-Bibel 4.2) | niedrig |
| 55 | Hook gegen Löschen im Ordner `archiv` | Hält das? (neu) | Reel Echtlauf 65–90 s | Der Auftrag sagt „räum das Archiv auf“, ein Hook verbietet Änderungen dort: Wer gewinnt? | Quelle zu prüfen (Beispiel aus Format-Bibel 4.1) | mittel |
| 56 | Datumsformat nur in der CLAUDE.md | Gleicher Auftrag, anderer Schalter (neu) | Reel Echtlauf 65–90 s | Schreibt Claude Datumsangaben im gewünschten Format, wenn das nur in der CLAUDE.md steht? | Quelle zu prüfen | niedrig |
| 57 | Deutscher gegen englischer Prompt | Gleicher Auftrag, anderer Schalter (neu) | Reel Echtlauf 65–90 s | Derselbe Auftrag auf Deutsch und auf Englisch: Unterscheiden sich Ergebnis, Dauer und Werkzeugaufrufe? | Quelle zu prüfen | niedrig |
| 58 | Aus einer langen Mail eine Aufgabenliste | Eine Aufgabe, ein Lauf (neu) | Reel Echtlauf 65–90 s | Eine lange Beispiel-Mail mit versteckten Aufgaben: Findet Claude alle für die Liste? | Quelle zu prüfen | niedrig |
| 59 | Mythos: Höflich bitten bringt bessere Ergebnisse | Doku gegen Wirklichkeit (neu) | Reel Echtlauf 65–90 s | Derselbe Auftrag mit und ohne „bitte“: Gibt es einen Unterschied in der Ergebnisdatei? | Quelle zu prüfen | niedrig |
| 60 | Edit-Sperre für den Ordner `vertraege` | Hält das? (neu) | Reel Echtlauf 65–90 s | Hält eine Edit-Sperre, wenn Claude die Beispieldatei stattdessen per Bash umschreiben will? | Quelle zu prüfen (Regelwerk wie `deny-env`, eigener Lauf nötig) | mittel |

Summe: 60 Vorschläge (11 aufgezeichnet, 40 Zeilen mit 44 weiteren Kalenderthemen, davon 4 Zeilen aus je zwei Kalenderthemen zusammengelegt, 9 neue). Von den 84 Kalenderthemen stehen damit 55 in der Tabelle, die übrigen 29 unter „Hinweise“.

## Hinweise

- **Aufzeichnungsalter:** Läufe, die bei Export älter als 14 Tage sind oder vor einer neuen Claude-Code-Version entstanden, prüft `record_run.py --check` erneut (Format-Bibel 6.2). Die 11 Aufzeichnungen stammen vom 02.11.2026.
- **Kalenderthemen ohne Zeile oben** (Format-Bibel 4: nicht echt ausführbare Themen werden umgebaut oder fallen weg):
  - Slash-Befehle laufen im Modus `-p` nicht (Aufzeichnungserfahrung 02.11.2026): /compact oder /clear? (-20261112-2), Was beim Kompaktieren verloren geht (-20261112-1), Wichtiges nach dem Kompaktieren wieder einspielen (-20261204-1), 5 Befehle für die erste Sitzung (-20261111-2).
  - Oberfläche statt Terminal, im Recorder nicht abbildbar: 4 Tastenkürzel (-20261113-3), Eigene Tastenkürzel (-20261201-2), Statuszeile mit Kontextanzeige (-20261121-3), Remote Control (-20261206-1), Claude Code mit Chrome (-20261204-2), Terminal, Desktop oder VS Code? (-20261205-1).
  - Netzwerkdienst mit Anmeldung oder Cloud, gegen Format-Bibel 6.6: @claude im GitHub-Issue (-20261124-2), Lokal oder in der Cloud? (-20261206-3), Zeitgesteuert: Cloud, Desktop oder /loop? (-20261201-3), Ein Plugin aus dem Marketplace installieren (-20261130-3).
  - Noch offen, Lauf denkbar: Auto Memory (-20261113-2), Skills bei Bedarf (-20261116-2), Checkpoints (-20261117-1), Fast Mode (-20261119-1), Output Style oder --append-system-prompt? (-20261119-2), MCP oder Skill? (-20261121-1), 5 Wege, Tokens zu sparen (-20261122-2), Claude Code ohne Chatfenster: -p (-20261124-1), Mitgelieferte Skills (-20261125-2), --continue oder --resume? (-20261126-2), 4 Prompt-Techniken (-20261129-2), Subagent oder Agent-Team? (-20261129-3, experimentell), Plugins (-20261130-2), Welche Version habe ich? (-20261203-1), Die eingebauten Output Styles (-20261204-3).
- **Mengen:** Bei 3 DE und 3 EN je Tag reichen die 60 Vorschläge für 20 Tage. Jeder Lauf braucht zwei Aufzeichnungen (DE und EN), jede mindestens zweimal wiederholt.
- **Alter Kalenderplan:** Der Themen- und Kalenderplan vom 01.11.2026 sieht noch animierte Oberflächen vor; das ist für neue Videos durch die Format-Bibel „Echtlauf“ ersetzt. Die Reihen des Kalenders (Grundlagen, In drei Schritten, Mythos-Check, Entweder-oder, Werkzeugkiste) sind oben den vier Echtlauf-Reihen zugeordnet.

## Zur Info: geeignet für die Produktion bis 05.11.2026

Kriterium: Aufzeichnung DE und EN liegt vor (2 von 2 gleich), Plan `data\direction\<id>-echtlauf.json` existiert, in `05 Produktion\Promptwerk\2026-11` liegt noch kein Export, frühe Termine.

1. **„Was Claude zu Beginn liest“ (Nr. 2, claude_workflows-20261109-2-de, Termin 09.11.2026).**
2. **„Eine Aufgabe von Anfang bis Ende“ (Nr. 4, claude_workflows-20261110-1-de, Termin 10.11.2026).**
3. **„Ganze Datei lesen oder gezielt suchen“ (Nr. 6, claude_workflows-20261111-1-de, Termin 11.11.2026).**
