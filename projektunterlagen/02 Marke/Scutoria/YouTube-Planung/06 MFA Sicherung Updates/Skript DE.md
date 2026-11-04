# MFA, Sicherung, Updates: was Fragebogen und Versicherer zuerst fragen

Fassung 3 (Langvideo, Planung), Entwurf 2026-11-02. Freigegebener Wortlaut aus SKRIPTE/06-mfa-backup-updates.de.md Fassung 2 (Stefan, 29.10. und 01.11.2026) unverändert; neu und zur Freigabe: Kaltstart (c0s0), Überblick (c0s2), Kapitel 4 (c4) und der letzte Satz (Verweis auf Video 07 statt auf Video 02), im Feld new=true markiert.

Neue, noch nicht freigegebene Stellen sind mit „(neu, zur Freigabe)“ markiert.

## 0 Dieselben ersten Fragen

[c0s0 · case · yt/shot02_questionnaire_desk.start.png] (neu, zur Freigabe)
[MARKER: Beispiel]
Mittwoch, sechzehn Uhr. Auf dem Schreibtisch liegen zwei Formulare nebeneinander: der Fragebogen eines Kunden und der Antrag einer Cyberversicherung. Die ersten Fragen sind fast dieselben.

[c0s1 · statement]
Wonach fragen ein Sicherheitsfragebogen vom Kunden und ein Antragsformular vom Versicherer zuerst? Nach denselben Dingen: Multi-Faktor-Authentifizierung, Sicherung, Updates.
[QUELLE: Mannheimer, Fragebogen Cyber-Risiken (HF_060 0424); Markel, Pro Cyber v2; Allianz, IT-Haftpflicht 9.25; Beazley, Sicherheitsanforderungen; Funk mit Beazley, Juli 2022; Donau, AVB Cyber 2025 · Abruf 2026-10-19 und 2026-10-23]

Dieses Video nennt fünf Maßnahmen, sagt, welcher Beleg zu jeder genügt, und zeigt, wo die Quellen sich widersprechen.

[c0s2 · chapters] (neu, zur Freigabe)
Wir gehen so vor: sechs Formulare und ihre kurze Liste, fünf Maßnahmen mit fünf Belegen, wo die Quellen sich widersprechen, zwei Fälle, in denen Sie entscheiden, der Beispielbetrieb, was das Toolkit nicht ist, und am Ende das freie Memo.

## 1 Sechs Versichererformulare, eine kurze Liste

[c1s0 · statement · yt/lib_envelopes_desk.start.png]
Anfragen dieser Art erreichen einen kleinen Betrieb von einem größeren Kunden, über einen Vertrag mit Sicherheitsklauseln oder von einer Cyberversicherung. Warum der Fragebogen kommt, erklärt Video zwei. Hier geht es darum, was die Formulare fragen, und die Versicherer sind der klarste Fall, weil sie es mit Zahlen aufschreiben.

[c1s1 · paper · yt/lib_documents_desk.start.png]
[MARKER: Fakt]
Wir haben sechs öffentliche Unterlagen von Versicherern ganz gelesen: vier Anträge für Cyberversicherungen, einen Fragebogen zur IT-Haftpflicht, ein Bedingungswerk. Die meisten fragen dasselbe: Sicherung auf getrennte Systeme mit geprüfter Wiederherstellung; Multi-Faktor-Authentifizierung für Cloud-Dienste, E-Mail, Fernzugriff und Administratoren; Patches zeitnah und keine Software ohne Hersteller-Updates; Schutzsoftware auf allen Geräten mit automatischen Updates; jährliche Schulung mit Anti-Phishing; ein schriftliches Notfallkonzept; Administratorrechte nur für die Administration. Einer davon, Beazley, nennt vier dieser Punkte eine zwingende Voraussetzung für den Abschluss einer Cyberdeckung.
[QUELLE: Mannheimer, Fragebogen Cyber-Risiken (HF_060 0424); Markel, Pro Cyber v2; Allianz, IT-Haftpflicht 9.25; Beazley, Sicherheitsanforderungen; Funk mit Beazley, Juli 2022; Donau, AVB Cyber 2025 · Abruf 2026-10-19 und 2026-10-23]

[c1s2 · statement]
[MARKER: Auslegung]
Die Versicherer fragen weitgehend dasselbe, was das Gesetz die Kunden fragen lässt, in einfacheren Worten und mit Zahlen. Unsere Auslegung: Für einen Betrieb ohne IT-Abteilung ist das eine gute Nachricht. Die Liste ist kurz, und ein Beleg dient beiden.

[c1s3 · paper · yt/lib_network_cupboard.start.png]
Die typische Lage: Die E-Mail hat einen zweiten Faktor, weil der Anbieter darauf gedrängt hat; die Cloud-Konsole hat keinen. Jede Nacht läuft eine Sicherung auf eine Platte im Büro, und niemand hat je eine Datei daraus zurückgespielt. Ein alter Rechner in der Werkstatt bekommt keine Updates mehr. Das ist keine Nachlässigkeit; so wächst es, wenn IT nebenbei läuft. Die Formulare fragen, was vorhanden ist, was teilweise da ist, und bis wann der Rest kommt.

## 2 Fünf Maßnahmen, fünf Belege

[c2s0 · steps]
Fünf Maßnahmen, in der Reihenfolge, in der die Formulare fragen, jede mit dem Beleg, der genügt.

[c2s1 · compare]
Eins: Multi-Faktor-Authentifizierung auf jedem E-Mail-Konto.

[MARKER: Fakt]
Beazleys kritische Anforderung zwei und Funks Frage zwei verlangen MFA für cloudbasierte Dienste, mit dem E-Mail-Konto in der Cloud als Beispiel, und für alle Fernzugriffe. Die Frage B sechs des österreichischen Labels verlangt MFA zumindest bei kritischen Systemen. Die NIS-zwei-Richtlinie nennt Multi-Faktor-Authentifizierung in Artikel einundzwanzig, Absatz zwei, Buchstabe j.
[QUELLE: Beazley, Anforderung 2; Funk, Frage 2; Cyber Trust Austria, Schema Policy 2026, B6; Durchführungsverordnung (EU) 2024/2690, Anhang Nr. 11.7.1; Richtlinie (EU) 2022/2555, Art. 21 Abs. 2 Buchst. j; ENISA, 12 steps, Schritt 5; Bundeskriminalamt, CEO Fraud, Stand 29.6.2026 · abgerufen 19.10.2026]

[c2s2 · statement]
[MARKER: Auslegung]
Dass jedes Postfach kritisch ist, ist unser Schluss, nicht der Wortlaut des Labels: Ein gekapertes Postfach ist der Beginn des Zahlungsbetrugs, und das Erste, was ein Angreifer damit tut, ist, anderswo Passwörter zurückzusetzen. Der Beleg: ein datiertes Bildschirmfoto der MFA-Einstellungen je System.

[c2s3 · compare · yt/lib_key_board.start.png]
Zwei: MFA für Fernzugriff, Administratorkonten und Cloud-Konsolen.

[MARKER: Fakt]
Mannheimer fragt, ob Administratoren zwingend MFA für die internen Server und Cloud-Strukturen brauchen und ob der Zugriff aus dem Homeoffice nur mit MFA möglich ist. Markel fragt nach MFA für alle Fernzugriffe und für Administratoren. Beazley: kein Fernzugriff ohne VPN und MFA.
[QUELLE: Mannheimer, 7.7.1, 7.7.3, 8.1; Markel, Abschnitt 4 Nr. 6 und 6.2; Allianz, 2.5.5; Beazley, 2 und 3; Cyber Trust Austria, Schema Policy 2026, A6; DVO (EU) 2024/2690, Anhang Nr. 11.3.2 Buchst. a und 6.7.2 Buchst. d; Donau Versicherung, AVB Cyber 2025, Teil E · abgerufen 19.10.2026]

[c2s4 · steps]
[MARKER: Fakt]
Welcher zweite Faktor? Die CISA reiht Authenticator-Apps und Sicherheitsschlüssel über Codes per SMS; SMS steht unter den MFA-Verfahren zuletzt, aber noch über dem Passwort allein.
[QUELLE: CISA, Implementing Phishing-Resistant MFA, Oktober 2022 · Abruf 2026-10-19; NIST SP 800-63B-4, Juli 2025, Abschnitt 3.2.5 · Abruf 2026-10-23]

[MARKER: Auslegung]
Also: zuerst App oder Sicherheitsschlüssel auf E-Mail- und Administratorkonten, SMS als Rückfallweg. Der Beleg ist dasselbe Bildschirmfoto oder der Administratorbericht des Anbieters.

[c2s5 · compare · yt/lib_backup_shelf.start.png]
Drei: eine tägliche Sicherung mit einer Kopie außerhalb der Reichweite eines Angreifers.

[MARKER: Fakt]
Die meisten Versichererformulare fragen, wie oft gesichert wird und ob die Speichermedien von den aktiven Systemen getrennt sind. Markel verlangt Sicherungen auf separierten Systemen, unter einer Million Euro Umsatz mindestens wöchentlich, darüber täglich. Beazleys erste kritische Anforderung sind getestete Offline-Backups. Die Durchführungsverordnung zu NIS zwei verlangt Sicherungskopien an einem Ort, der nicht im selben Netz liegt wie das System. Und die DSGVO, die jeden Betrieb bindet, der personenbezogene Daten verarbeitet, verlangt die Fähigkeit, diese Daten nach einem Zwischenfall rasch wiederherzustellen.
[QUELLE: Mannheimer, 4.1, 4.5, 4.6, 4.7, 4.9; Markel, Abschn. 4 Nr. 5; Beazley, 1; Funk, 1; DVO (EU) 2024/2690, Anh. Nr. 4.2.2 Buchst. c; ENISA, 12 steps, Schritt 9; RL (EU) 2022/2555, Art. 21 Abs. 2 Buchst. c · Abruf 19.10.2026; VO (EU) 2016/679, Art. 32 Abs. 1 Buchst. a, c und d · Abruf 23.10.2026]

[c2s6 · statement]
[MARKER: Auslegung]
Außer Reichweite ist der ganze Sinn: Eine Sicherung auf einer immer angeschlossenen Platte oder in einem Cloud-Ordner, den das Bürokonto löschen kann, ist die nächste verschlüsselte Sicherung. Täglich ist der strengste Rhythmus der Formulare, deshalb fragt das Toolkit täglich. Der Beleg: ein Bildschirmfoto der Sicherungseinstellungen und ein Satz, wo die Kopie außer Reichweite liegt.

[c2s7 · paper · yt/shot02_backup_drive.start.png]
Vier: eine Wiederherstellung, in den letzten zwölf Monaten geprobt, mit notierter Dauer.

[MARKER: Fakt]
Mannheimer fragt nach dem Datum des letzten erfolgreichen Rücksicherungstests. Markel fragt, ob mindestens einmal im Jahr ein Wiederherstellungstest für alle Sicherungen erfolgt. Die Durchführungsverordnung verlangt regelmäßige Tests der Wiederherstellung von Sicherungskopien.
[QUELLE: Mannheimer, 4.2; Markel, 7.2; Beazley, 1; Funk, 1; Durchführungsverordnung (EU) 2024/2690, Anhang Nr. 4.2.6 · abgerufen 19.10.2026; Verordnung (EU) 2016/679, Art. 32 Abs. 1 Buchst. a, c und d · abgerufen 23.10.2026]

[MARKER: Auslegung]
Die notierte Dauer ist unser Zusatz: Sie zeigt, ob die IT innerhalb der Zeit wieder läuft, die der Betrieb überbrücken kann. Ein Ordner zurückgespielt, die Zeit gestoppt, Datum und Ergebnis in einer Zeile. Diese Zeile ist der Beleg.

[c2s8 · compare · yt/lib_laptop_side.start.png]
Fünf: Updates automatisch innerhalb von Tagen, und Schutzsoftware auf jedem Gerät.

[MARKER: Fakt]
Die Frage B neun des österreichischen Labels sagt: Kein Sicherheitsupdate darf länger als ein Quartal überfällig sein. Markel fragt, ob Sicherheitspatches innerhalb von vier Wochen eingespielt werden und kritische ab einem CVSS-Wert von acht Komma null unverzüglich.
[QUELLE: Cyber Trust Austria, Schema Policy 2026, B9; Markel, 7.3; Mannheimer, 7.1; Allianz, 2.5.3; Beazley; Funk, 5; Durchführungsverordnung (EU) 2024/2690, Anhang Nr. 6.6.1 Buchst. a bis c; ENISA, 12 steps, Schritt 6 · abgerufen 19.10.2026]

[MARKER: Fakt]
Zum Schutz: Mannheimer fragt, ob alle Systeme einen Schutz gegen Schadsoftware mit automatischen Updates haben; Beazley und Funk fragen nach Virenschutz auf allen Geräten und dem Scannen eingehender E-Mails.
[QUELLE: Mannheimer, 7.2; Markel, Abschn. 4 Nr. 5, 7.3; Beazley; Funk, 6, 7; Cyber Trust Austria 2026, B11, B12; DVO (EU) 2024/2690, Anh. 6.9.1, 9; ENISA, 12 steps, Schr. 6; RL (EU) 2022/2555, Art. 21 Abs. 2 lit. h · Abruf 19.10.2026; VO (EU) 2016/679, Art. 32 Abs. 1 lit. a, c, d · Abruf 23.10.2026]

[c2s9 · paper]
[MARKER: Auslegung]
Innerhalb von Tagen ist strenger als das Quartal des Labels und die vier Wochen von Markel; es ist das, was automatische Updates von selbst tun, und automatisch ist der einzige Weg, auf dem ein Betrieb ohne IT-Abteilung mithält. Der eingebaute Schutz genügt jedem Formular, das wir gelesen haben. Der Beleg: eine Zeile im Monat, dass die Updates gelaufen sind, und eine Geräteliste mit der Spalte „unterstützt bis“ und einer Spalte Verschlüsselung. Die Verschlüsselung zählt: Ein verlorenes Notebook mit personenbezogenen Daten und ohne Verschlüsselung ist meist eine Datenpanne, die binnen zweiundsiebzig Stunden zu melden ist; mit Verschlüsselung ist es meist ein verlorenes Notebook im Vorfallsprotokoll.
[QUELLE: Verordnung (EU) 2016/679, Art. 4 Nr. 12, Art. 33 Abs. 1 und 5, Art. 34 Abs. 1 · EUR-Lex · Abruf 2026-10-23]

[c2s10 · statement]
Fünf Maßnahmen, fünf Belege. Wo sie vorliegen, stellen Sie sie in einer Stunde oder weniger zusammen, wie das Handbuch es zeigt. Was noch nicht da ist, bekommt einen Termin, und der Termin steht im Dokument.

## 3 Wo die Quellen sich widersprechen

[c3s0 · statement · yt/lib_law_books.start.png]
Die Marker: Das Quadrat ist ein Fakt, am Original gelesen, mit Abrufdatum. Die Raute ist unsere Auslegung, über die sich streiten lässt. Der halbe Kreis: Die Quellen widersprechen sich, oder die Rechtslage ist offen. Der gestrichelte Kreis: Keine Quelle beantwortet die Frage, und Ihr Betrieb entscheidet.

[c3s1 · compare]
Erstens die Passwortregel. Das ist offen.

[MARKER: Unsicher]
Die Digital Identity Guidelines der NIST vom Juli 2025 verlangen mindestens fünfzehn Zeichen, wo das Passwort der einzige Faktor ist, und acht, wo ein zweiter Faktor dazukommt. Sie verbieten Kompositionsregeln und den regelmäßigen Wechsel ohne Hinweis auf eine Kompromittierung. Das BSI hat sich am 31. Januar 2025 und noch einmal am 30. Januar 2026 öffentlich gegen erzwungene Wechsel ausgesprochen. Die Durchführungsverordnung zu NIS zwei weist in die andere Richtung: Sie verlangt die Änderung von Authentifizierungsdaten in vorab festgelegten Zeitabständen.
[QUELLE: NIST SP 800-63B-4, Juli 2025, Abschnitte 3.1.1.1 und 3.1.1.2 · Abruf 2026-10-19; BSI-Pressemitteilungen vom 31. Januar 2025 und 30. Januar 2026 · Abruf 2026-10-19; Durchführungsverordnung (EU) 2024/2690, Anhang 11.6.2 · Abruf 2026-10-19]

[c3s2 · steps]
Das Toolkit folgt NIST und BSI: lang, einmalig, im Passwort-Manager, bei Verdacht geändert, durch einen zweiten Faktor geschützt. Besteht ein Kunde oder ein Versicherer auf Intervallen und beruft sich auf die Verordnung, ist die ehrliche Antwort, ein Intervall für die Konten ohne zweiten Faktor zu vereinbaren und MFA überall sonst zu behalten. Die Selbstauskunft sagt, welche Regel gilt. Die Umsetzungsleitlinie der ENISA liest die Verordnung wie das Toolkit: Passwörter wechseln, wenn nötig, zum Beispiel nach einem Sicherheitsvorfall. Ob ein Gericht oder eine Behörde über den Widerspruch entschieden hat, haben wir nicht gesucht.
[QUELLE: ENISA, NIS2 Technical Implementation Guidance, Juni 2025, S. 142, abgerufen 23.10.2026]

[c3s3 · compare · yt/lib_archive_shelf.start.png]
Zweitens eine Lücke.

[MARKER: Lücke]
Wir haben keine Quelle gefunden, die ein gesetzliches Mindestmaß für die Anmeldesicherheit eines Betriebs außerhalb von NIS zwei nennt. Die Maßstäbe oben sind das, was die Behörden empfehlen und wonach Fragebögen fragen. Ein Vertrag mit einem Kunden oder Versicherer kann mehr verlangen.

Drittens der Rhythmus.

[MARKER: Auslegung]
Wo die Formulare sich unterscheiden, nimmt das Toolkit das strengste: tägliche Sicherung, Wiederherstellungstest einmal im Jahr, Updates innerhalb von Tagen. Unsere Auslegung: Die Selbstauskunft muss vor allen bestehen. Markels vier Wochen und Beazleys vier zwingende Voraussetzungen sind die Worte der Formulare, nicht des Gesetzes.
[QUELLE: Mannheimer, Fragebogen Cyber-Risiken (HF_060 0424); Markel, Pro Cyber v2; Allianz, IT-Haftpflicht 9.25; Beazley, Sicherheitsanforderungen; Funk mit Beazley, Juli 2022; Donau, AVB Cyber 2025 · Abruf 2026-10-19 und 2026-10-23]

## 4 Was tun Sie? Zwei Fälle

[c4s0 · case · yt/lib_key_board.start.png] (neu, zur Freigabe)
[MARKER: Beispiel]
Zwei Fälle zum Mitentscheiden. Beide sind erfunden, die Quellen dahinter nicht. Fall eins. Dienstag, zehn Uhr. Im Fragebogen eines Kunden steht: Werden Passwörter in festen Abständen geändert? Im Betrieb gilt: lange, einmalige Passwörter im Passwort-Manager, ein zweiter Faktor, ein Wechsel bei Verdacht.

[c4s1 · choice] (neu, zur Freigabe)
Was tun Sie? A: Ja ankreuzen, das will der Kunde hören. B: Ab sofort alle Passwörter in festen Abständen wechseln lassen, auch dort, wo ein zweiter Faktor schützt. C: Die eigene Regel ehrlich angeben und anbieten, für Konten ohne zweiten Faktor ein Intervall zu vereinbaren. Überlegen Sie kurz.

[c4s2 · timeline] (neu, zur Freigabe)
[MARKER: Beispiel]
A ist schnell. Im Beispiel geht der Fragebogen mit Ja zurück. In der Selbstauskunft steht aber die eigene Regel: lang, einmalig, Wechsel bei Verdacht. Zwei Dokumente sagen jetzt Verschiedenes.

[c4s3 · step] (neu, zur Freigabe)
[MARKER: Auslegung]
Richtig ist C, nach unserer Auslegung. Die Quellen widersprechen sich hier: NIST und BSI raten von erzwungenen Wechseln ab, die Durchführungsverordnung verlangt feste Abstände. Die ehrliche Antwort nennt Ihre Regel und bietet ein Intervall für Konten ohne zweiten Faktor an. A widerspricht Ihrer eigenen Selbstauskunft, und B gibt ohne Not die Empfehlung von NIST und BSI auf.
[QUELLE: NIST SP 800-63B-4, Juli 2025, Abschnitte 3.1.1.1 und 3.1.1.2 · Abruf 2026-10-19; BSI-Pressemitteilungen vom 31. Januar 2025 und 30. Januar 2026 · Abruf 2026-10-19; Durchführungsverordnung (EU) 2024/2690, Anhang 11.6.2 · Abruf 2026-10-19]

[c4s4 · case · yt/lib_laptop_side.start.png] (neu, zur Freigabe)
[MARKER: Beispiel]
Fall zwei. Montag, halb acht. Ein Monteur meldet, dass sein Notebook aus dem Wagen verschwunden ist. Darauf liegen Angebote mit Namen und Anschriften von Kunden. Ob es verschlüsselt war, weiß er nicht.

[c4s5 · choice] (neu, zur Freigabe)
Was tun Sie? A: Ein neues Notebook bestellen, sonst nichts. B: Ein paar Tage abwarten, vielleicht taucht es wieder auf. C: In der Geräteliste nachsehen, ob es verschlüsselt war, den Fall ins Vorfallsprotokoll schreiben und, wenn es nicht verschlüsselt war, sofort klären, ob eine Meldung nötig ist. Überlegen Sie kurz.

[c4s6 · timeline] (neu, zur Freigabe)
[MARKER: Beispiel]
B klingt gelassen. Im Beispiel wartet der Betrieb bis Donnerstag. Dann zeigt die Geräteliste: Das Notebook war nicht verschlüsselt.

[MARKER: Fakt]
Eine Verletzung des Schutzes personenbezogener Daten meldet der Verantwortliche unverzüglich und möglichst binnen zweiundsiebzig Stunden, nachdem sie ihm bekannt wurde, es sei denn, sie führt voraussichtlich nicht zu einem Risiko. Jede Verletzung wird dokumentiert.
[QUELLE: Verordnung (EU) 2016/679, Art. 4 Nr. 12, Art. 33 Abs. 1 und 5, Art. 34 Abs. 1 · EUR-Lex · Abruf 2026-10-23]

[c4s7 · step] (neu, zur Freigabe)
[MARKER: Auslegung]
Richtig ist C, nach unserer Auslegung. Die Geräteliste mit der Spalte Verschlüsselung beantwortet die erste Frage sofort. Mit Verschlüsselung ist es meist ein verlorenes Notebook im Vorfallsprotokoll; ohne ist es meist eine Datenpanne, die binnen zweiundsiebzig Stunden zu melden ist. A hat nichts dokumentiert, und B lässt die Uhr laufen.
[QUELLE: Verordnung (EU) 2016/679, Art. 4 Nr. 12, Art. 33 Abs. 1 und 5, Art. 34 Abs. 1 · EUR-Lex · Abruf 2026-10-23]

## 5 Der Beispielbetrieb

[c5s0 · statement · yt/lib_cables_toolbox.start.png]
Der Generator ist mit einem erfundenen Betrieb vorbelegt: ein Elektrotechnikbetrieb in Österreich mit zehn bis neunundvierzig Beschäftigten, die IT teils von einem externen Dienstleister, teils vom Büro betreut. Keine Person und kein Betrieb darin ist echt. Ein Kunde hat einen Fragebogen geschickt.

[c5s1 · paper]
Seine Antworten zeigen ein realistisches Mischbild. MFA bei E-Mail: vorhanden, eine Authenticator-App auf jedem Postfach. MFA bei der Cloud-Konsole: VPN ja, die Konsole noch nicht: teilweise, erste Welle. Sicherung: täglich auf einen Speicher im Büro, keine Kopie außer Reichweite: teilweise, erste Welle. Wiederherstellungstest: nie gemacht: noch nicht, erste Welle. Updates und Schutzsoftware: vorhanden. Ein Passwort-Manager fürs Büro, aber nicht für den Außendienst: teilweise. Ein alter Werkstattrechner, keine schriftliche Geräteliste: teilweise, zweite Welle.

[c5s2 · steps · yt/lib_documents_desk.start.png]
Was herauskommt: der Maßnahmenplan, D2. Jedes „teilweise“ und jedes „noch nicht“ wird eine Maßnahme mit Priorität, verantwortlicher Person, Termin in einer von drei Wellen und dem Nachweis, der danach vorliegt. Die erste Welle dieses Betriebs enthält die Cloud-Konsole, die Kopie außer Reichweite, den Wiederherstellungstest und den Notfallplan, das Thema von Video acht.

[c5s3 · paper · yt/shot02_evidence_folder.start.png]
Die Nachweisliste, D4, nennt je Frage einen Beleg. Was vorliegt, bekommt eine Anlagennummer; was fehlt, behält seine Fragennummer und seinen Termin. Die Selbstauskunft trägt dieselben Stände in ihrer Übersichtstabelle, und das Antwortschreiben nennt die Lücken mit ihren Terminen. Wer prüft, liest: nicht überall Ja, sondern was heute vorhanden ist und was datiert ist.

## 6 Was das Toolkit nicht ist

[c6s0 · statement · yt/lib_archive_shelf.start.png]
Was das Toolkit nicht ist: Es ist keine Rechtsberatung, kein Audit und kein Zertifikat. Kein Dokument behauptet, dass Ihr Betrieb sicher ist oder ein Gesetz erfüllt. Die Dokumente zeigen, was Sie an einem Datum vorweisen können, was Sie bis wann tun werden und wer dafür einsteht.

[c6s1 · compare]
Die fünf Maßnahmen sind die ersten Fragen der Formulare, kein Urteil über Ihren Betrieb. Die Selbstauskunft hat neun Bereiche; diese fünf liegen in dreien davon.

Die offenen Punkte dieses Themas stehen im Handbuch: Der Passwort-Widerspruch ist der offene Punkt sechs Punkt siebzehn; ob ein Gericht darüber entschieden hat, ist Punkt sechs Punkt zweiundzwanzig, nicht gesucht. Ihr Betrieb entscheidet. Die Dokumente halten die Entscheidung fest, mit Datum.

## 7 Freies Memo und Toolkit

[c7s0 · paper]
Wenn Sie heute anfangen wollen, fangen Sie mit dem freien Memo an: Wo steht unsere Anmeldung? Acht Fragen zu Multi-Faktor-Authentifizierung, Passwörtern, geteilten Konten, Austritten und Wiederherstellung. Sie lesen das Memo auf der Seite, das PDF kommt per E-Mail, und für ein Memo, das Sie nur lesen, wird nichts gespeichert. Es nennt die drei Schritte, die zuerst kommen: ein zweiter Faktor auf jedem Konto, das zählt; ein langes Passwort je Konto, verwaltet von einem Passwort-Manager; ein Konto je Person, Austritte am selben Tag, Wiederherstellung geprobt. Das Memo ist frei auf scutoria.com; der Link steht in der Beschreibung.

[c7s1 · statement]
Das Sicherheitsnachweis-Toolkit macht aus diesen Schritten und den weiteren Maßnahmen, nach denen Kunden oder Versicherer fragen, sieben datierte Dokumente: darunter die Selbstauskunft, den Maßnahmenplan D2 mit seinen drei Wellen und die Nachweisliste D4. Das Handbuch steht vor dem Kauf vollständig online, mit jedem offenen Punkt. Das Toolkit kostet 199 Euro im Jahr. Die ersten zehn Käufer zahlen 99.

[c7s2 · close] (neu, zur Freigabe)
Hier ist Scutoria. Die Stimme, die Sie hören, ist synthetisch. Das Skript wurde mit einem KI-Tool entworfen und von uns Satz für Satz geprüft. Jede Zahl und jede Rechtsaussage trägt ihre Quelle am Bildschirm. Quellenbasiert, keine Rechtsberatung.

Als Nächstes auf diesem Kanal: Müssen Sie kennzeichnen, was Ihre KI erzeugt? Artikel fünfzig der KI-Verordnung.
