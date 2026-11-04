# Themen- und Kalenderplan Scutoria (09.11.–06.12.2026)

**Freigegeben von Stefan am 01.11.2026.** Themen im Status `planned` gehen in die Produktion; Themen im Status `idea` erst nach Quellenprüfung; Risiko „high“ vor jeder Veröffentlichung einzeln an Stefan.

Stand: 01.11.2026 (Wien). **Entwurf, wartet auf Stefans Freigabe.** Marke Scutoria (`ai_security`): KI und Sicherheit für kleine Betriebe, ruhig, belegt, ohne Angstmache, Anrede „du“, keine Rechtsberatung.

- Maschinenlesbarer Kalender: `C:\Automation\faceless-network\data\calendars\ai_security_2026-11.json` (168 Zeilen, `calendar check`: ok: 168 rows).
- Grundlage: `Planungsrahmen Themen- und Kalenderplan.md`, `prompts\calendar_planner.md`, `brands\ai_security\script_prompt.md`, `config\brands.yaml`.
- Alter Entwurf `Themenplan November 2026 – Scutoria.md` und der alte Kalender vom 30.10. liegen in `C:\Users\Stefa\Documents\_zum_loeschen\2026-11-01 Kalender alt`. Die drei recherchierten Themen daraus sind übernommen (KI-Chat, KI-Kennzeichnung, Passkeys).
- Quellen: je Thema mindestens zwei Primärquellen, alle am 01.11.2026 geöffnet und auf die Kernaussage geprüft (Stichwortsuche im Text). eur-lex und die DPF-Liste blocken Skriptabrufe; sie wurden im Browser geöffnet und gelesen.

## Zahlen

- Themen: 84 (je ein DE/EN-Paar), Posts: 168.
- Themen nach Status: geplant 80, Idee 1, weiter fortgeschritten 3 (KI-Chat: Skripte DE und EN; KI-Kennzeichnung und Passkeys: Video DE fertig, EN nur Skript).
- Zeilen nach Status: geplant 160, Idee 2, Skript 4, fertig 2.
- Risiko: kein Thema „high“; 4 Themen „low“ (Mythos: Das Schloss heißt, die Seite ist echt, Das NIST-Rahmenwerk in der Kurzfassung für Kleinbetriebe, Phishing melden in 30 Sekunden, Mythos: Inkognito macht anonym), alle übrigen „medium“.

## Takt

Je Tag drei Themen, jedes als DE/EN-Paar am selben Tag. Die EN-Fassung ist sprachlich angepasst, keine wörtliche Übersetzung.

| Thema des Tages | Deutsch | Englisch |
|---|---|---|
| 1 | 12:00 | 15:00 |
| 2 | 14:00 | 20:00 |
| 3 | 18:00 | 23:00 |

Die englischen Uhrzeiten sind eine Annahme (Großbritannien und US-Ostküste), änderbar in `config/brands.yaml` › `slots_by_language`.

## Themenreihen

| Reihe | EN-Name | Ziel | Format | Rhythmus (Wochentag, Thema des Tages) | Themen |
|---|---|---|---|---|---|
| Was gilt wirklich | What the rules say | Recht und Standards in klaren Worten: was AI Act, DSGVO, NIS2, Cyber Resilience Act, Data Act und Einstiegs-Checks für einen Kleinbetrieb bedeuten. Nur zitieren, was die Quelle sagt; keine Rechtsberatung. | Erklärung, Vergleich, Liste | Di 2, Do 1, Sa 2 | 12 |
| Fünf-Minuten-Schutz | Five-minute fix | Eine Einstellung oder Gewohnheit, die in fünf Minuten erledigt ist: Zwei-Faktor, Updates, Backup, Router, Freigaben. Endet mit genau einem Handgriff. | Anleitung, Liste, Erklärung | Mo 3, Di 3, Mi 3, Fr 1, Sa 3 | 20 |
| Mythos-Check | Myth check | Ein verbreiteter Irrtum, aufgelöst mit dem, was BSI, NCSC, NIST oder Hersteller wirklich sagen. Eröffnet die Woche am Montag. | Mythos | Mo 1, Mi 2, Fr 3, So 2 | 16 |
| So läuft die Masche | How the scam works | Wie eine Betrugsmasche abläuft und woran man sie erkennt, ohne Anleitung, ohne erfundene Fälle, ohne Opfernamen. Endet mit einer Prüfregel (Rückruf, Codewort, Lesezeichen). | Fallmuster | Di 1, Do 2, Sa 1, So 3 | 16 |
| KI im Büro | AI at work | KI-Werkzeuge im Büro sicher nutzen: Training und Datenschutz-Einstellungen, Copilot, Prompt Injection, Agenten, Erweiterungen, API-Schlüssel. | Erklärung, Anleitung, Liste, Vergleich | Mo 2, Mi 1, Do 3, Fr 2, So 1 | 20 |

Beispielthemen:

- **Was gilt wirklich:** KI-Kennzeichnung – was seit August 2026 in der EU gilt; KI-Kompetenz: die Pflicht, die schon gilt; NIS2: Ist mein Betrieb betroffen?; Datenpanne: Warum die Uhr 72 Stunden läuft.
- **Fünf-Minuten-Schutz:** Passkeys – das Login, das man nicht phishen kann; Zwei-Faktor zuerst fürs E-Mail-Konto; Automatische Updates: einmal einschalten; Backup: eine Kopie gehört offline.
- **Mythos-Check:** Mythos: Wir sind zu klein für Angreifer; Mythos: Passwörter regelmäßig ändern; Mythos: Phishing erkennt man an Fehlern; Mythos: Das Schloss heißt, die Seite ist echt.
- **So läuft die Masche:** Die Mail vom Chef, der dringend überweisen lässt; Quishing: der falsche QR-Code; Der falsche Microsoft-Anruf; Neue Bankverbindung per Mail? Erst anrufen.
- **KI im Büro:** Was ein KI-Chat über deinen Betrieb speichert; Prompt Injection: versteckte Befehle für deine KI; Die Daten-Ampel für KI-Tools; Geteilter KI-Chat heißt öffentlicher Link.

Wochenraster (gleich in allen vier Wochen):

| | Mo | Di | Mi | Do | Fr | Sa | So |
|---|---|---|---|---|---|---|---|
| Thema 1 (12:00 / 15:00) | Mythos-Check | So läuft die Masche | KI im Büro | Was gilt wirklich | Fünf-Minuten-Schutz | So läuft die Masche | KI im Büro |
| Thema 2 (14:00 / 20:00) | KI im Büro | Was gilt wirklich | Mythos-Check | So läuft die Masche | KI im Büro | Was gilt wirklich | Mythos-Check |
| Thema 3 (18:00 / 23:00) | Fünf-Minuten-Schutz | Fünf-Minuten-Schutz | Fünf-Minuten-Schutz | KI im Büro | Mythos-Check | Fünf-Minuten-Schutz | So läuft die Masche |

## Kalender

| Datum | Uhrzeit DE / EN | Reihe | Titel DE | Titel EN | Format | Risiko | Quellen | Status |
|---|---|---|---|---|---|---|---|---|
| Mo 09.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Wir sind zu klein für Angreifer | Myth: we're too small to be a target | Mythos | medium | 3 | geplant |
| Mo 09.11. | 14:00 / 20:00 | KI im Büro | Was ein KI-Chat über deinen Betrieb speichert | What an AI chat keeps from your business | Erklärung | medium | 3 | Skript |
| Mo 09.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Passkeys – das Login, das man nicht phishen kann | Passkeys – the login that cannot be phished | Anleitung | medium | 3 | DE fertig, EN Skript |
| Di 10.11. | 12:00 / 15:00 | So läuft die Masche | Die Mail vom Chef, der dringend überweisen lässt | The urgent payment request from 'the boss' | Fallmuster | medium | 2 | geplant |
| Di 10.11. | 14:00 / 20:00 | Was gilt wirklich | KI-Kennzeichnung – was seit August 2026 in der EU gilt | AI labelling – what applies in the EU since August 2026 | Erklärung | medium | 3 | DE fertig, EN Skript |
| Di 10.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Zwei-Faktor zuerst fürs E-Mail-Konto | Two-step login: start with your email | Anleitung | medium | 3 | geplant |
| Mi 11.11. | 12:00 / 15:00 | KI im Büro | Prompt Injection: versteckte Befehle für deine KI | Prompt injection: hidden instructions for your AI | Erklärung | medium | 2 | geplant |
| Mi 11.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Passwörter regelmäßig ändern | Myth: change your passwords every 90 days | Mythos | medium | 3 | geplant |
| Mi 11.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Automatische Updates: einmal einschalten | Automatic updates: switch them on once | Anleitung | medium | 2 | geplant |
| Do 12.11. | 12:00 / 15:00 | Was gilt wirklich | KI-Kompetenz: die Pflicht, die schon gilt | AI literacy: the duty that already applies | Erklärung | medium | 2 | geplant |
| Do 12.11. | 14:00 / 20:00 | So läuft die Masche | Quishing: der falsche QR-Code | Quishing: the fake QR code | Fallmuster | medium | 2 | geplant |
| Do 12.11. | 18:00 / 23:00 | KI im Büro | Die Daten-Ampel für KI-Tools | A traffic light for what goes into AI tools | Liste | medium | 2 | geplant |
| Fr 13.11. | 12:00 / 15:00 | Fünf-Minuten-Schutz | Backup: eine Kopie gehört offline | Backups: keep one copy offline | Anleitung | medium | 2 | geplant |
| Fr 13.11. | 14:00 / 20:00 | KI im Büro | Geteilter KI-Chat heißt öffentlicher Link | A shared AI chat is a public link | Anleitung | medium | 2 | geplant |
| Fr 13.11. | 18:00 / 23:00 | Mythos-Check | Mythos: Phishing erkennt man an Fehlern | Myth: phishing emails are full of typos | Mythos | medium | 3 | geplant |
| Sa 14.11. | 12:00 / 15:00 | So läuft die Masche | Der falsche Microsoft-Anruf | The fake Microsoft support call | Fallmuster | medium | 2 | geplant |
| Sa 14.11. | 14:00 / 20:00 | Was gilt wirklich | NIS2: Ist mein Betrieb betroffen? | NIS2: does it apply to my business? | Erklärung | medium | 3 | geplant |
| Sa 14.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Ein Passwortmanager fürs Team | A password manager for the team | Anleitung | medium | 2 | geplant |
| So 15.11. | 12:00 / 15:00 | KI im Büro | Copilot im Firmenkonto: Was mit deinen Eingaben passiert | Copilot on a business plan: what happens to your prompts | Erklärung | medium | 2 | geplant |
| So 15.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Das Schloss heißt, die Seite ist echt | Myth: the padlock means the site is legit | Mythos | low | 2 | geplant |
| So 15.11. | 18:00 / 23:00 | So läuft die Masche | Neue Bankverbindung per Mail? Erst anrufen | New bank details by email? Call first | Fallmuster | medium | 2 | geplant |
| Mo 16.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Der Absender stimmt, also ist die Mail echt | Myth: the sender looks right, so the email is real | Mythos | medium | 2 | geplant |
| Mo 16.11. | 14:00 / 20:00 | KI im Büro | Schatten-KI: private KI-Konten im Betrieb | Shadow AI: personal AI accounts at work | Erklärung | medium | 2 | geplant |
| Mo 16.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Ein Backup zählt erst, wenn es zurückkommt | A backup only counts once you have restored it | Anleitung | medium | 3 | geplant |
| Di 17.11. | 12:00 / 15:00 | So läuft die Masche | Die Stimme klingt wie der Chef und ist es nicht | It sounds like your boss, but it isn't | Fallmuster | medium | 2 | geplant |
| Di 17.11. | 14:00 / 20:00 | Was gilt wirklich | Datenpanne: Warum die Uhr 72 Stunden läuft | Data breach: why the clock runs for 72 hours | Erklärung | medium | 3 | geplant |
| Di 17.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Steht eure Firmenadresse in einem Datenleck? | Is your work email in a data leak? | Anleitung | medium | 2 | geplant |
| Mi 18.11. | 12:00 / 15:00 | KI im Büro | Was sich die KI über dich merkt | What your AI assistant remembers | Anleitung | medium | 3 | geplant |
| Mi 18.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Die Cloud ist mein Backup | Myth: the cloud is my backup | Mythos | medium | 3 | geplant |
| Mi 18.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Microsoft 365: Sicherheitsstandards einschalten | Microsoft 365: turn on security defaults | Anleitung | medium | 2 | geplant |
| Do 19.11. | 12:00 / 15:00 | Was gilt wirklich | Was der AI Act bei KI ganz verbietet | What the AI Act bans outright | Liste | medium | 3 | geplant |
| Do 19.11. | 14:00 / 20:00 | So läuft die Masche | Die Paket-SMS mit Link | The parcel text with a link | Fallmuster | medium | 3 | geplant |
| Do 19.11. | 18:00 / 23:00 | KI im Büro | KI-Agenten: so wenig Rechte wie möglich | AI agents: as few permissions as possible | Erklärung | medium | 2 | geplant |
| Fr 20.11. | 12:00 / 15:00 | Fünf-Minuten-Schutz | Google Workspace: Bestätigung in zwei Schritten erzwingen | Google Workspace: enforce 2-Step Verification | Anleitung | medium | 2 | geplant |
| Fr 20.11. | 14:00 / 20:00 | KI im Büro | Datenstandort EU: gebucht oder nur gehofft? | EU data residency: booked or just assumed? | Vergleich | medium | 2 | geplant |
| Fr 20.11. | 18:00 / 23:00 | Mythos-Check | Mythos: Was die KI sagt, ist geprüft | Myth: what the AI says has been checked | Mythos | medium | 2 | geplant |
| Sa 21.11. | 12:00 / 15:00 | So läuft die Masche | Der angebliche IT-Support im Teams-Chat | The fake IT helpdesk in a Teams chat | Fallmuster | medium | 2 | geplant |
| Sa 21.11. | 14:00 / 20:00 | Was gilt wirklich | KI-Tool im Betrieb: der Vertrag zur Auftragsverarbeitung | AI tools at work: the data processing agreement | Erklärung | medium | 3 | geplant |
| Sa 21.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Postfachregeln prüfen: die stille Weiterleitung | Check your mailbox rules for silent forwarding | Anleitung | medium | 2 | geplant |
| So 22.11. | 12:00 / 15:00 | KI im Büro | KI-Browsererweiterungen lesen mit | AI browser extensions can read along | Anleitung | medium | 2 | geplant |
| So 22.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Sonderzeichen machen Passwörter sicher | Myth: special characters make a password strong | Mythos | medium | 3 | geplant |
| So 22.11. | 18:00 / 23:00 | So läuft die Masche | Die richtige Nummer im Display und trotzdem Betrug | The right number on screen, and still a scam | Fallmuster | medium | 2 | geplant |
| Mo 23.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Die DSGVO verbietet KI | Myth: GDPR bans AI | Mythos | medium | 2 | geplant |
| Mo 23.11. | 14:00 / 20:00 | KI im Büro | KI-Protokoll im Meeting: erst fragen, dann aufnehmen | AI meeting notes: ask before you record | Erklärung | medium | 2 | geplant |
| Mo 23.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Router: eigenes Admin-Passwort, aktuelle Firmware | Your router: own admin password, current firmware | Anleitung | medium | 2 | geplant |
| Di 24.11. | 12:00 / 15:00 | So läuft die Masche | Die Erpressermail mit deinem alten Passwort | The extortion email that quotes your old password | Fallmuster | medium | 2 | geplant |
| Di 24.11. | 14:00 / 20:00 | Was gilt wirklich | CyberRisikoCheck und Cyber Essentials im Vergleich | CyberRisikoCheck vs Cyber Essentials | Vergleich | medium | 3 | geplant |
| Di 24.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Gäste gehören ins Gast-WLAN | Guests belong on the guest Wi-Fi | Anleitung | medium | 2 | geplant |
| Mi 25.11. | 12:00 / 15:00 | KI im Büro | Copilot findet alles, was du sehen darfst | Copilot finds everything you're allowed to see | Erklärung | medium | 2 | geplant |
| Mi 25.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Deepfakes erkennt man immer | Myth: you can always spot a deepfake | Mythos | medium | 2 | geplant |
| Mi 25.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Im Alltag ohne Admin-Rechte arbeiten | Work without admin rights day to day | Anleitung | medium | 2 | geplant |
| Do 26.11. | 12:00 / 15:00 | Was gilt wirklich | Cyber Resilience Act: Sicherheitsupdates werden Pflicht | Cyber Resilience Act: security updates become mandatory | Erklärung | medium | 3 | geplant |
| Do 26.11. | 14:00 / 20:00 | So läuft die Masche | Die gefälschte Seite ganz oben in der Suche | The fake site at the top of the search results | Fallmuster | medium | 2 | geplant |
| Do 26.11. | 18:00 / 23:00 | KI im Büro | KI-Inventar: Welche Tools laufen bei euch? | AI inventory: which tools are you running? | Anleitung | medium | 2 | geplant |
| Fr 27.11. | 12:00 / 15:00 | Fünf-Minuten-Schutz | SPF, DKIM, DMARC: Wer darf in deinem Namen mailen? | SPF, DKIM, DMARC: who may send email as you? | Erklärung | medium | 3 | geplant |
| Fr 27.11. | 14:00 / 20:00 | KI im Büro | Content Credentials: der Herkunftsnachweis für Bilder | Content Credentials: a provenance label for images | Erklärung | medium | 2 | geplant |
| Fr 27.11. | 18:00 / 23:00 | Mythos-Check | Mythos: KI-Detektoren erkennen KI-Texte | Myth: AI detectors can spot AI-written text | Mythos | medium | 2 | geplant |
| Sa 28.11. | 12:00 / 15:00 | So läuft die Masche | Anmeldeanfragen im Minutentakt | Login prompts every minute | Fallmuster | medium | 2 | geplant |
| Sa 28.11. | 14:00 / 20:00 | Was gilt wirklich | Wenn die Software entscheidet: Art. 22 DSGVO | When software decides: GDPR Article 22 | Erklärung | medium | 2 | geplant |
| Sa 28.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Firmenhandy: drei Einstellungen gegen Verlust | Work phone: three settings for when it goes missing | Liste | medium | 2 | geplant |
| So 29.11. | 12:00 / 15:00 | KI im Büro | Gefälschte KI-Apps | Fake AI apps | Erklärung | medium | 1 | Idee |
| So 29.11. | 14:00 / 20:00 | Mythos-Check | Mythos: Gelöscht ist gelöscht | Myth: deleted means gone | Mythos | medium | 2 | geplant |
| So 29.11. | 18:00 / 23:00 | So läuft die Masche | Die Mail vom angeblichen Finanzamt | The fake tax office email | Fallmuster | medium | 2 | geplant |
| Mo 30.11. | 12:00 / 15:00 | Mythos-Check | Mythos: Ein Mac braucht keinen Schutz | Myth: Macs don't need protecting | Mythos | medium | 2 | geplant |
| Mo 30.11. | 14:00 / 20:00 | KI im Büro | US-KI-Anbieter: Steht er auf der DPF-Liste? | US AI vendor: is it on the DPF list? | Anleitung | medium | 2 | geplant |
| Mo 30.11. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Laptop verschlüsseln: aus Datenpanne wird Sachschaden | Encrypt your laptop: a theft stays a hardware loss | Anleitung | medium | 3 | geplant |
| Di 01.12. | 12:00 / 15:00 | So läuft die Masche | Die Rechnung, die amtlich aussieht | The invoice that only looks official | Fallmuster | medium | 3 | geplant |
| Di 01.12. | 14:00 / 20:00 | Was gilt wirklich | Das NIST-Rahmenwerk in der Kurzfassung für Kleinbetriebe | The NIST framework, small business edition | Erklärung | low | 3 | geplant |
| Di 01.12. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Cloud-Freigaben: Wer hat noch den Link? | Cloud sharing: who still has the link? | Anleitung | medium | 2 | geplant |
| Mi 02.12. | 12:00 / 15:00 | KI im Büro | Die OWASP-Liste der KI-Risiken | The OWASP list of AI risks | Liste | medium | 2 | geplant |
| Mi 02.12. | 14:00 / 20:00 | Mythos-Check | Mythos: Wer zahlt, bekommt seine Daten zurück | Myth: paying the ransom gets your data back | Mythos | medium | 2 | geplant |
| Mi 02.12. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Wenn jemand geht: Zugänge am letzten Tag sperren | When someone leaves: revoke access on the last day | Liste | medium | 2 | geplant |
| Do 03.12. | 12:00 / 15:00 | Was gilt wirklich | Ist das schon KI? Wie der AI Act KI-Systeme abgrenzt | Is it AI? How the AI Act defines an AI system | Erklärung | medium | 2 | geplant |
| Do 03.12. | 14:00 / 20:00 | So läuft die Masche | Zahl, oder es hagelt Ein-Stern-Bewertungen | Pay up, or the one-star reviews start | Fallmuster | medium | 2 | geplant |
| Do 03.12. | 18:00 / 23:00 | KI im Büro | KI-Skripte: erst verstehen, dann ausführen | AI-written scripts: understand before you run | Erklärung | medium | 2 | geplant |
| Fr 04.12. | 12:00 / 15:00 | Fünf-Minuten-Schutz | E-Mail-Konto gehackt: die ersten Schritte | Email account hacked: the first steps | Anleitung | medium | 2 | geplant |
| Fr 04.12. | 14:00 / 20:00 | KI im Büro | Fünf Fragen an jeden KI-Anbieter | Five questions for any AI vendor | Liste | medium | 2 | geplant |
| Fr 04.12. | 18:00 / 23:00 | Mythos-Check | Mythos: Der AI Act betrifft nur KI-Hersteller | Myth: the AI Act only concerns AI developers | Mythos | medium | 3 | geplant |
| Sa 05.12. | 12:00 / 15:00 | So läuft die Masche | SIM-Swap: Wenn deine Nummer plötzlich tot ist | SIM swap: when your number suddenly stops working | Fallmuster | medium | 2 | geplant |
| Sa 05.12. | 14:00 / 20:00 | Was gilt wirklich | Data Act: Der Cloud-Wechsel wird leichter | Data Act: switching cloud providers gets easier | Erklärung | medium | 3 | geplant |
| Sa 05.12. | 18:00 / 23:00 | Fünf-Minuten-Schutz | Phishing melden in 30 Sekunden | Report a phishing email in 30 seconds | Anleitung | low | 2 | geplant |
| So 06.12. | 12:00 / 15:00 | KI im Büro | KI-API-Schlüssel wie eine Kreditkarte behandeln | Treat AI API keys like a credit card | Anleitung | medium | 2 | geplant |
| So 06.12. | 14:00 / 20:00 | Mythos-Check | Mythos: Inkognito macht anonym | Myth: incognito mode makes you anonymous | Mythos | low | 3 | geplant |
| So 06.12. | 18:00 / 23:00 | So läuft die Masche | Die Mail, die deine Firmenseite sperren will | The email threatening to shut down your business page | Fallmuster | medium | 2 | geplant |

## Ansatz und Quellen je Thema

Abrufdatum aller Quellen: 01.11.2026. Reihenfolge wie im Kalender.

**Mo 09.11. · Thema 1 · Mythos: Wir sind zu klein für Angreifer** (C01, geplant)  
Ansatz: Kleinsein schützt nicht, weil viele Angriffe automatisiert und breit gestreut laufen; das zeigen die amtlichen Lagebilder aus Deutschland und Großbritannien  
Quellen: <https://www.gov.uk/government/statistics/cyber-security-breaches-survey-2025/cyber-security-breaches-survey-2025> · <https://www.bsi.bund.de/DE/Service-Navi/Publikationen/Lagebericht/lagebericht_node.html> · <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/KMU/KMU_node.html>

**Mo 09.11. · Thema 2 · Was ein KI-Chat über deinen Betrieb speichert** (E01, Skript)  
Ansatz: Ob ein KI-Chat Firmendaten zum Training nutzt, entscheiden eine Einstellung und der Vertrag  
Quellen: <https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training> · <https://privacy.claude.com/en/articles/7996875-can-you-delete-data-that-i-sent-via-api> · <https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html>

**Mo 09.11. · Thema 3 · Passkeys – das Login, das man nicht phishen kann** (B01, fertig)  
Ansatz: Passkeys widerstehen Phishing, weil es kein geteiltes Geheimnis gibt; MFA bleibt die Pflicht dahinter  
Quellen: <https://fidoalliance.org/passkeys/> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Accountschutz/Passkeys/passkeys-anmelden-ohne-passwort_node.html> · <https://www.ncsc.gov.uk/guidance/multi-factor-authentication-online-services>

**Di 10.11. · Thema 1 · Die Mail vom Chef, der dringend überweisen lässt** (D01, geplant)  
Ansatz: Beim CEO-Betrug wirken Zeitdruck und Autorität, nicht Technik; eine feste Rückruf-Regel für Zahlungen bricht das Muster  
Quellen: <https://www.ic3.gov/PSA/2024/PSA240911> · <https://www.berlin.de/polizei/aufgaben/praevention/betrug/artikel.693958.php>

**Di 10.11. · Thema 2 · KI-Kennzeichnung – was seit August 2026 in der EU gilt** (A01, fertig)  
Ansatz: Seit 2. August 2026 gelten die Transparenzregeln des AI Act: Chatbots und KI-Inhalte kennzeichnen  
Hinweis: und Leitlinien zur Transparenz prüfen.  
Quellen: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50> · <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai> · <https://digital-strategy.ec.europa.eu/en/faqs/guidelines-and-code-practice-transparent-ai-systems>

**Di 10.11. · Thema 3 · Zwei-Faktor zuerst fürs E-Mail-Konto** (B02, geplant)  
Ansatz: Das E-Mail-Konto ist der Generalschlüssel für alle Passwort-Resets, darum bekommt es als erstes die Zwei-Faktor-Anmeldung  
Quellen: <https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/use-a-strong-and-separate-password-for-email> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Accountschutz/Zwei-Faktor-Authentisierung/zwei-faktor-authentisierung_node.html> · <https://www.ncsc.gov.uk/guidance/multi-factor-authentication-online-services>

**Mi 11.11. · Thema 1 · Prompt Injection: versteckte Befehle für deine KI** (E03, geplant)  
Ansatz: Liest eine KI Mails oder Webseiten, können darin versteckte Anweisungen stecken; deshalb darf sie ohne Freigabe nichts Folgenreiches tun  
Quellen: <https://genai.owasp.org/llmrisk/llm01-prompt-injection/> · <https://www.ncsc.gov.uk/blog-post/thinking-about-security-ai-systems>

**Mi 11.11. · Thema 2 · Mythos: Passwörter regelmäßig ändern** (C02, geplant)  
Ansatz: Erzwungener regelmäßiger Passwortwechsel macht Passwörter eher schwächer; NIST und NCSC raten zum Wechsel nur bei Verdacht  
Quellen: <https://pages.nist.gov/800-63-4/sp800-63b.html> · <https://www.ncsc.gov.uk/blog-post/problems-forcing-regular-password-expiry> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Accountschutz/Sichere-Passwoerter-erstellen/sichere-passwoerter-erstellen_node.html>

**Mi 11.11. · Thema 3 · Automatische Updates: einmal einschalten** (B03, geplant)  
Ansatz: Updates schließen bekannte Lücken; automatisch eingeschaltet, passieren sie, ohne dass jemand daran denken muss  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Updates-Browser-Open-Source-Software/Wichtige-Softwareupdates/wichtige-softwareupdates_node.html> · <https://www.ncsc.gov.uk/collection/small-business-guide>

**Do 12.11. · Thema 1 · KI-Kompetenz: die Pflicht, die schon gilt** (A02, geplant)  
Ansatz: KI-Kompetenz ist seit Februar 2025 Pflicht für Betriebe, die KI einsetzen; seit dem AI Omnibus ohne vorgeschriebenes Niveau und ohne Zertifikat, geprüft wird ab August 2026  
Hinweis: laut KI-Kompetenz-FAQ der Kommission, Seite aktualisiert 20.10.2026.  
Quellen: <https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers> · <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4>

**Do 12.11. · Thema 2 · Quishing: der falsche QR-Code** (D04, geplant)  
Ansatz: QR-Codes verstecken die Zieladresse; Betrüger kleben falsche Codes über echte oder verschicken sie per Mail und Brief  
Quellen: <https://www.verbraucherzentrale.de/wissen/digitale-welt/phishingradar/quishing-falsche-qrcodes-in-mails-briefen-oepnv-und-strassenverkehr-98612> · <https://www.ic3.gov/PSA/2022/PSA220118>

**Do 12.11. · Thema 3 · Die Daten-Ampel für KI-Tools** (E06, geplant)  
Ansatz: Eine einfache Ampel aus öffentlich, intern und personenbezogen entscheidet in Sekunden, welche Daten in welches KI-Tool dürfen  
Quellen: <https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf> · <https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html>

**Fr 13.11. · Thema 1 · Backup: eine Kopie gehört offline** (B04, geplant)  
Ansatz: Ein Backup schützt vor Erpressersoftware nur, wenn eine Kopie vom Netz getrennt aufbewahrt wird  
Quellen: <https://www.ncsc.gov.uk/blog-post/offline-backups-in-an-online-world> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Daten-sichern-verschluesseln-und-loeschen/Datensicherung-und-Datenverlust/datensicherung-und-datenverlust_node.html>

**Fr 13.11. · Thema 2 · Geteilter KI-Chat heißt öffentlicher Link** (E10, geplant)  
Ansatz: Wer einen KI-Chat per Link teilt, macht ihn für jeden mit dem Link lesbar; geteilte Links lassen sich in den Einstellungen prüfen und löschen  
Quellen: <https://help.openai.com/en/articles/7925741-chatgpt-shared-links-faq> · <https://privacy.claude.com/en/articles/10593882-share-and-unshare-chats>

**Fr 13.11. · Thema 3 · Mythos: Phishing erkennt man an Fehlern** (C11, geplant)  
Ansatz: Mit KI geschriebene Phishing-Mails sind sprachlich sauber; die Behörden erwarten, dass sie dadurch schwerer zu erkennen sind  
Quellen: <https://www.ncsc.gov.uk/report/impact-of-ai-on-cyber-threat> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Leistungen-und-Kooperationen/Digitaler-Verbraucherschutz/Digitalbarometer/Online-Betrug2026/cymon2026_online-betrug_node.html> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Spam-Phishing-Co/Passwortdiebstahl-durch-Phishing/Wie-erkenne-ich-Phishing-in-E-Mails-und-auf-Webseiten/wie-erkenne-ich-phishing-in-e-mails-und-auf-webseiten_node.html>

**Sa 14.11. · Thema 1 · Der falsche Microsoft-Anruf** (D06, geplant)  
Ansatz: Microsoft ruft nicht unaufgefordert an; Fernwartung gibt es nur über einen selbst gewählten, bekannten Kontakt  
Quellen: <https://support.microsoft.com/en-us/windows/protect-yourself-from-tech-support-scams-2ebf91bd-f94c-2a8a-e541-f5c800d18435> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Social-Engineering/social-engineering_node.html>

**Sa 14.11. · Thema 2 · NIS2: Ist mein Betrieb betroffen?** (A04, geplant)  
Ansatz: Ob NIS2 gilt, hängt an Branche und Größe; die meisten Kleinbetriebe fallen nicht direkt darunter, spüren die Pflichten aber als Zulieferer  
Quellen: <https://digital-strategy.ec.europa.eu/en/policies/nis2-directive> · <https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/BSI-Portal/NIS-2-Betroffenheitspruefung/nis-2-betroffenheitspruefung_node.html> · <https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/NIS-2-Infopakete/NIS-2-Lieferkette/NIS-2-Lieferkette_node.html>

**Sa 14.11. · Thema 3 · Ein Passwortmanager fürs Team** (B06, geplant)  
Ansatz: Ein Passwortmanager macht für jedes Konto ein eigenes starkes Passwort möglich, ohne dass sich jemand eines merken muss  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Accountschutz/Sichere-Passwoerter-erstellen/Passwort-Manager/passwort-manager_node.html> · <https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/password-managers>

**So 15.11. · Thema 1 · Copilot im Firmenkonto: Was mit deinen Eingaben passiert** (E02, geplant)  
Ansatz: Im Microsoft-365-Geschäftsangebot gelten für Copilot-Eingaben dieselben Vertragszusagen wie für E-Mails und Dateien, und sie trainieren keine Basismodelle  
Quellen: <https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection> · <https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy>

**So 15.11. · Thema 2 · Mythos: Das Schloss heißt, die Seite ist echt** (C04, geplant)  
Ansatz: Das Schloss zeigt nur eine verschlüsselte Verbindung, nicht ob die Seite vertrauenswürdig ist; Chrome hat das Symbol deshalb ersetzt  
Quellen: <https://blog.chromium.org/2023/05/an-update-on-lock-icon.html> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Spam-Phishing-Co/Passwortdiebstahl-durch-Phishing/Wie-erkenne-ich-Phishing-in-E-Mails-und-auf-Webseiten/wie-erkenne-ich-phishing-in-e-mails-und-auf-webseiten_node.html>

**So 15.11. · Thema 3 · Neue Bankverbindung per Mail? Erst anrufen** (D02, geplant)  
Ansatz: Meldet ein Lieferant per Mail eine neue Bankverbindung, ist ein Rückruf unter der bekannten Nummer die wirksamste Prüfung  
Quellen: <https://www.ic3.gov/PSA/2024/PSA240911> · <https://www.berlin.de/polizei/aufgaben/praevention/betrug/artikel.693958.php>

**Mo 16.11. · Thema 1 · Mythos: Der Absender stimmt, also ist die Mail echt** (C15, geplant)  
Ansatz: Absenderadressen lassen sich fälschen; ob eine Mail echt ist, zeigt erst eine Rückfrage über einen bekannten Weg  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Spam-Phishing-Co/Gefaelschte-Absenderadressen/Schutzmassnahmen/schutzmassnahmen_node.html> · <https://www.ncsc.gov.uk/collection/email-security-and-anti-spoofing>

**Mo 16.11. · Thema 2 · Schatten-KI: private KI-Konten im Betrieb** (E05, geplant)  
Ansatz: Nutzen Mitarbeitende private KI-Konten für Firmendaten, fehlt jede Vertragskontrolle; eine einseitige KI-Regel mit freigegebenen Tools schafft Klarheit  
Quellen: <https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf> · <https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html>

**Mo 16.11. · Thema 3 · Ein Backup zählt erst, wenn es zurückkommt** (B05, geplant)  
Ansatz: Ein Backup ist erst verlässlich, wenn die Wiederherstellung einmal geprobt wurde; ein Testlauf im Quartal deckt Lücken auf  
Quellen: <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Analysen-und-Prognosen/Ransomware-Angriffe/Top-10-Ransomware-Massnahmen/top-10-ransomware-massnahmen_node.html> · <https://www.ncsc.gov.uk/blog-post/offline-backups-in-an-online-world> · <https://www.ncsc.gov.uk/collection/small-business-guide>

**Di 17.11. · Thema 1 · Die Stimme klingt wie der Chef und ist es nicht** (D03, geplant)  
Ansatz: KI kann Stimmen nachahmen; ein vereinbartes Codewort oder ein Rückruf schützt besser als das Ohr  
Quellen: <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Kuenstliche-Intelligenz/Deepfakes/deepfakes_node.html> · <https://www.ic3.gov/PSA/2025/PSA250515>

**Di 17.11. · Thema 2 · Datenpanne: Warum die Uhr 72 Stunden läuft** (A06, geplant)  
Ansatz: Die DSGVO gibt nach einer Datenpanne 72 Stunden für die Meldung an die Aufsicht; wer vorher weiß, wen er anruft, verliert keine davon  
Quellen: <https://eur-lex.europa.eu/eli/reg/2016/679/oj> · <https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en> · <https://www.edpb.europa.eu/sme-data-protection-guide/home_en>

**Di 17.11. · Thema 3 · Steht eure Firmenadresse in einem Datenleck?** (B07, geplant)  
Ansatz: Mit dem Identity Leak Checker des Hasso-Plattner-Instituts prüfst du in einer Minute, ob eine Firmenadresse in bekannten Datenlecks auftaucht  
Quellen: <https://sec.hpi.de/ilc/> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Identitaetsdiebstahl/identitaetsdiebstahl_node.html>

**Mi 18.11. · Thema 1 · Was sich die KI über dich merkt** (E18, geplant)  
Ansatz: KI-Assistenten speichern Erinnerungen über Gespräche hinweg; in den Einstellungen lässt sich prüfen und löschen, was sie über Betrieb und Kunden wissen  
Quellen: <https://openai.com/index/memory-and-new-controls-for-chatgpt/> · <https://support.claude.com/en/articles/11817273-use-claudes-chat-search-and-memory-to-build-on-previous-context> · <https://help.openai.com/en/articles/8590148-memory-faq>

**Mi 18.11. · Thema 2 · Mythos: Die Cloud ist mein Backup** (C09, geplant)  
Ansatz: Synchronisieren ist kein Backup: Gelöschte oder verschlüsselte Dateien wandern in die Cloud mit, und die Wiederherstellung hat Fristen  
Quellen: <https://support.microsoft.com/en-us/office/restore-your-onedrive-fa231298-759d-41cf-bcd0-25ac53eb8a15> · <https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cloud-Computing-Sicherheitstipps/Cloud-Risiken-und-Sicherheitstipps/cloud-risiken-und-sicherheitstipps_node.html>

**Mi 18.11. · Thema 3 · Microsoft 365: Sicherheitsstandards einschalten** (B11, geplant)  
Ansatz: Für kleine Microsoft-365-Umgebungen schaltet ein einziger Schalter, die Sicherheitsstandards, die Mehrfaktor-Anmeldung für alle ein  
Quellen: <https://learn.microsoft.com/en-us/entra/fundamentals/security-defaults> · <https://learn.microsoft.com/en-us/microsoft-365/admin/security-and-compliance/set-up-multi-factor-authentication>

**Do 19.11. · Thema 1 · Was der AI Act bei KI ganz verbietet** (A03, geplant)  
Ansatz: Der AI Act verbietet neun KI-Praktiken, darunter Emotionserkennung am Arbeitsplatz; das neunte Verbot gegen sogenannte Nacktbild-Apps gilt ab Dezember 2026  
Hinweis: gilt laut Kommission ab Dezember 2026; genaues Datum vor dem Skript im Omnibus-Text nachsehen.  
Quellen: <https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-prohibited-artificial-intelligence-ai-practices-defined-ai-act> · <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-5> · <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai>

**Do 19.11. · Thema 2 · Die Paket-SMS mit Link** (D08, geplant)  
Ansatz: Smishing nutzt die Erwartung einer Lieferung; den Paketstatus prüft man in der App oder auf der Seite des Zustellers, nie über den Link  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Spam-Phishing-Co/spam-phishing-co_node.html> · <https://www.verbraucherzentrale.de/wissen/digitale-welt/phishingradar> · <https://www.ncsc.gov.uk/collection/phishing-scams/report-scam-email>

**Do 19.11. · Thema 3 · KI-Agenten: so wenig Rechte wie möglich** (E04, geplant)  
Ansatz: Ein KI-Agent, der Mails senden oder Zahlungen auslösen kann, braucht enge Rechte und eine menschliche Freigabe für folgenreiche Schritte  
Quellen: <https://genai.owasp.org/llmrisk/llm062025-excessive-agency/> · <https://media.defense.gov/2024/Apr/15/2003439257/-1/-1/0/CSI-DEPLOYING-AI-SYSTEMS-SECURELY.PDF>

**Fr 20.11. · Thema 1 · Google Workspace: Bestätigung in zwei Schritten erzwingen** (B12, geplant)  
Ansatz: In Google Workspace kann die Verwaltung die Bestätigung in zwei Schritten für alle erzwingen, statt auf Freiwilligkeit zu hoffen  
Quellen: <https://support.google.com/a/answer/9176657> · <https://support.google.com/a/answer/175197>

**Fr 20.11. · Thema 2 · Datenstandort EU: gebucht oder nur gehofft?** (E14, geplant)  
Ansatz: Ob KI-Daten in der EU bleiben, hängt vom gebuchten Angebot ab; EU-Datenresidenz muss man aktiv prüfen statt sie anzunehmen  
Quellen: <https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn> · <https://openai.com/index/introducing-data-residency-in-europe/>

**Fr 20.11. · Thema 3 · Mythos: Was die KI sagt, ist geprüft** (C07, geplant)  
Ansatz: Sprachmodelle erfinden plausible Antworten, wenn ihnen Wissen fehlt; das ist eine Eigenschaft der Technik und kein seltener Ausrutscher  
Quellen: <https://openai.com/index/why-language-models-hallucinate/> · <https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html>

**Sa 21.11. · Thema 1 · Der angebliche IT-Support im Teams-Chat** (D13, geplant)  
Ansatz: Angreifer geben sich im Chat als interner IT-Support aus und bitten um Fernzugriff; externe Chats lassen sich begrenzen  
Quellen: <https://www.microsoft.com/en-us/security/blog/2024/05/15/threat-actors-misusing-quick-assist-in-social-engineering-attacks-leading-to-ransomware/> · <https://learn.microsoft.com/en-us/microsoftteams/manage-external-access>

**Sa 21.11. · Thema 2 · KI-Tool im Betrieb: der Vertrag zur Auftragsverarbeitung** (A07, geplant)  
Ansatz: Wer Kundendaten in ein KI-Tool gibt, braucht nach Art. 28 DSGVO einen Auftragsverarbeitungsvertrag mit dem Anbieter  
Quellen: <https://eur-lex.europa.eu/eli/reg/2016/679/oj> · <https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-072020-concepts-controller-and-processor-gdpr_en> · <https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf>

**Sa 21.11. · Thema 3 · Postfachregeln prüfen: die stille Weiterleitung** (B13, geplant)  
Ansatz: Wer ein Postfach übernimmt, richtet oft unauffällige Weiterleitungs- und Löschregeln ein; ein Blick in die Regeln deckt das auf  
Quellen: <https://learn.microsoft.com/en-us/defender-office-365/detect-and-remediate-outlook-rules-forms-attack> · <https://learn.microsoft.com/en-us/defender-office-365/outbound-spam-policies-external-email-forwarding>

**So 22.11. · Thema 1 · KI-Browsererweiterungen lesen mit** (E08, geplant)  
Ansatz: Eine Erweiterung mit dem Recht, alle Websites zu lesen, sieht auch Banking und Kundendaten; im Betrieb lassen sich Erweiterungen zentral freigeben  
Quellen: <https://support.google.com/chrome_webstore/answer/186213> · <https://learn.microsoft.com/en-us/deployedge/microsoft-edge-manage-extensions-policies>

**So 22.11. · Thema 2 · Mythos: Sonderzeichen machen Passwörter sicher** (C03, geplant)  
Ansatz: Länge schlägt Komplexität: drei zufällige Wörter sind stärker und leichter zu merken als ein kurzes Passwort voller Sonderzeichen  
Quellen: <https://www.ncsc.gov.uk/blog-post/three-random-words-or-thinkrandom-0> · <https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online/use-a-strong-and-separate-password-for-email> · <https://pages.nist.gov/800-63-4/sp800-63b.html>

**So 22.11. · Thema 3 · Die richtige Nummer im Display und trotzdem Betrug** (D15, geplant)  
Ansatz: Die angezeigte Rufnummer lässt sich fälschen; geht es um Geld oder Zugangsdaten, auflegen und selbst zurückrufen  
Quellen: <https://www.bundesnetzagentur.de/DE/Vportal/TK/Aerger/Faelle/Manipulation/artikel.html> · <https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2022/20221129_TK-Aktueller-Hinweis.html>

**Mo 23.11. · Thema 1 · Mythos: Die DSGVO verbietet KI** (C13, geplant)  
Ansatz: Die DSGVO verbietet KI nicht; sie verlangt eine Rechtsgrundlage, Transparenz und einen passenden Vertrag mit dem Anbieter  
Quellen: <https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en> · <https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf>

**Mo 23.11. · Thema 2 · KI-Protokoll im Meeting: erst fragen, dann aufnehmen** (E07, geplant)  
Ansatz: Ein KI-Notizdienst nimmt das gesprochene Wort auf; in Deutschland ist heimliches Aufnehmen nach § 201 StGB strafbar, darum vorher alle informieren  
Quellen: <https://www.gesetze-im-internet.de/stgb/__201.html> · <https://support.microsoft.com/en-us/office/record-a-meeting-in-microsoft-teams-34dfbe7f-b07d-4a27-b4c6-de62f1348c24>

**Mo 23.11. · Thema 3 · Router: eigenes Admin-Passwort, aktuelle Firmware** (B08, geplant)  
Ansatz: Der Router ist die Haustür des Firmennetzes; ein eigenes Admin-Passwort und aktuelle Firmware sind die zwei wichtigsten Einstellungen  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Router-WLAN-VPN/router-wlan-vpn_node.html> · <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03148/tr03148_node.html>

**Di 24.11. · Thema 1 · Die Erpressermail mit deinem alten Passwort** (D10, geplant)  
Ansatz: Erpressermails mit einem echten alten Passwort stammen meist aus Datenlecks und nicht aus einem Hack; nicht zahlen, Passwort ändern  
Quellen: <https://www.ncsc.gov.uk/guidance/sextortion-scams-how-to-protect-yourself> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Identitaetsdiebstahl/identitaetsdiebstahl_node.html>

**Di 24.11. · Thema 2 · CyberRisikoCheck und Cyber Essentials im Vergleich** (A10, geplant)  
Ansatz: Deutschland und Großbritannien haben je einen Einstiegs-Check für Kleinbetriebe; beide zeigen, dass Grundschutz mit wenigen Kontrollen beginnt  
Quellen: <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/KMU/CyberRisikoCheck/CyberRisikoCheck_node.html> · <https://www.ncsc.gov.uk/cyberessentials/overview> · <https://www.dinmedia.de/de/technische-regel/din-spec-27076/365252629>

**Di 24.11. · Thema 3 · Gäste gehören ins Gast-WLAN** (B09, geplant)  
Ansatz: Ein eigenes Gast-WLAN hält fremde Geräte vom Firmennetz fern, ohne dass jemand das Hauptpasswort kennen muss  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Router-WLAN-VPN/WLAN-LAN-was-man-wissen-sollte/wlan-lan-was-man-wissen-sollte_node.html> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Router-WLAN-VPN/router-wlan-vpn_node.html>

**Mi 25.11. · Thema 1 · Copilot findet alles, was du sehen darfst** (E17, geplant)  
Ansatz: Copilot hält sich an bestehende Berechtigungen; zu weit gefasste Freigaben werden dadurch plötzlich auffindbar, darum vorher aufräumen  
Quellen: <https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy> · <https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-blueprint-oversharing>

**Mi 25.11. · Thema 2 · Mythos: Deepfakes erkennt man immer** (C10, geplant)  
Ansatz: Deepfakes werden schwerer zu erkennen; verlässlicher als das Bauchgefühl ist eine Rückfrage über einen zweiten Kanal  
Quellen: <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Kuenstliche-Intelligenz/Deepfakes/deepfakes_node.html> · <https://www.europol.europa.eu/cms/sites/default/files/documents/Europol_Innovation_Lab_Facing_Reality_Law_Enforcement_And_The_Challenge_Of_Deepfakes.pdf>

**Mi 25.11. · Thema 3 · Im Alltag ohne Admin-Rechte arbeiten** (B10, geplant)  
Ansatz: Wer im Alltag ohne Administratorrechte arbeitet, begrenzt, was eine Schadsoftware auf dem Rechner anrichten kann  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Basisschutz-fuer-Computer-Mobilgeraete/Basisschutz-fuer-Computer/Benutzerkonten/benutzerkonten_node.html> · <https://www.ncsc.gov.uk/collection/small-business-guide>

**Do 26.11. · Thema 1 · Cyber Resilience Act: Sicherheitsupdates werden Pflicht** (A05, geplant)  
Ansatz: Ab Dezember 2027 dürfen vernetzte Produkte in der EU nur mit Sicherheitsupdates verkauft werden; beim Kauf lohnt die Frage nach dem Update-Zeitraum schon heute  
Quellen: <https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act> · <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Cyber_Resilience_Act/cyber_resilience_act_node.html> · <https://eur-lex.europa.eu/eli/reg/2024/2847/oj>

**Do 26.11. · Thema 2 · Die gefälschte Seite ganz oben in der Suche** (D09, geplant)  
Ansatz: Betrüger kaufen Suchanzeigen oder schieben gefälschte Seiten nach oben; Lesezeichen für wichtige Logins umgehen das  
Quellen: <https://www.ic3.gov/PSA/2022/PSA221221> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/SEO-Poisoning/SEO-Poisoning_node.html>

**Do 26.11. · Thema 3 · KI-Inventar: Welche Tools laufen bei euch?** (E13, geplant)  
Ansatz: Eine Liste aller genutzten KI-Tools ist der erste Schritt zu Regeln, Verträgen und KI-Kompetenz  
Quellen: <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf> · <https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers>

**Fr 27.11. · Thema 1 · SPF, DKIM, DMARC: Wer darf in deinem Namen mailen?** (B14, geplant)  
Ansatz: Drei DNS-Einträge legen fest, wer im Namen deiner Domain mailen darf; das schützt Kunden vor gefälschten Mails mit deinem Absender  
Quellen: <https://www.ncsc.gov.uk/collection/email-security-and-anti-spoofing> · <https://support.google.com/a/answer/81126> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Spam-Phishing-Co/Gefaelschte-Absenderadressen/Schutzmassnahmen/schutzmassnahmen_node.html>

**Fr 27.11. · Thema 2 · Content Credentials: der Herkunftsnachweis für Bilder** (E12, geplant)  
Ansatz: Herkunftsnachweise wie C2PA zeigen, wie ein Bild entstanden ist; fehlen sie, beweist das allein noch keine Fälschung  
Quellen: <https://deepmind.google/models/synthid/> · <https://contentcredentials.org/>

**Fr 27.11. · Thema 3 · Mythos: KI-Detektoren erkennen KI-Texte** (C06, geplant)  
Ansatz: KI-Text-Detektoren sind unzuverlässig; OpenAI hat sein eigenes Erkennungswerkzeug wegen zu geringer Genauigkeit zurückgezogen  
Quellen: <https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/> · <https://arxiv.org/abs/2304.02819>

**Sa 28.11. · Thema 1 · Anmeldeanfragen im Minutentakt** (D05, geplant)  
Ansatz: Wer Anmeldeanfragen bekommt, die er nicht ausgelöst hat, lehnt ab und ändert das Passwort; der Zahlenabgleich verhindert Zustimmung aus Versehen  
Quellen: <https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-mfa-number-match> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Accountschutz/Zwei-Faktor-Authentisierung/Bewertung-2FA-Verfahren/bewertung-2fa-verfahren_node.html>

**Sa 28.11. · Thema 2 · Wenn die Software entscheidet: Art. 22 DSGVO** (A08, geplant)  
Ansatz: Entscheidet allein eine Software über Menschen, etwa über Bewerbungen, gibt die DSGVO den Betroffenen das Recht auf eine menschliche Prüfung  
Quellen: <https://eur-lex.europa.eu/eli/reg/2016/679/oj> · <https://ec.europa.eu/newsroom/article29/items/612053>

**Sa 28.11. · Thema 3 · Firmenhandy: drei Einstellungen gegen Verlust** (B16, geplant)  
Ansatz: Bildschirmsperre, Updates und Fernlöschung machen aus einem verlorenen Firmenhandy einen Ärger statt einer Datenpanne  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Basisschutz-fuer-Computer-Mobilgeraete/Schutz-fuer-Mobilgeraete/schutz-fuer-mobilgeraete_node.html> · <https://www.ncsc.gov.uk/collection/small-business-guide>

**So 29.11. · Thema 1 · Gefälschte KI-Apps** (E09, Idee)  
Ansatz: Betrüger tarnen Schadsoftware als bekannte KI-Apps; KI-Werkzeuge nur über die Seite des Herstellers oder den offiziellen Store installieren  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Schadprogramme/schadprogramme_node.html>

**So 29.11. · Thema 2 · Mythos: Gelöscht ist gelöscht** (C12, geplant)  
Ansatz: Papierkorb leeren entfernt nur den Verweis; bevor alte Geräte den Betrieb verlassen, braucht es sicheres Löschen  
Quellen: <https://www.ncsc.gov.uk/guidance/secure-sanitisation-storage-media> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Daten-sichern-verschluesseln-und-loeschen/daten-sichern-verschluesseln-und-loeschen_node.html>

**So 29.11. · Thema 3 · Die Mail vom angeblichen Finanzamt** (D11, geplant)  
Ansatz: Steuerbehörden schicken keine Erstattung per Link; gefälschte Mails im Namen von Finanzverwaltung oder HMRC zielen auf Bank- und Zugangsdaten  
Quellen: <https://www.gov.uk/government/organisations/hm-revenue-customs/contact/reporting-fraudulent-emails> · <https://www.berlin.de/sen/finanzen/steuern/informationen-fuer-steuerzahler-/artikel.1663337.php>

**Mo 30.11. · Thema 1 · Mythos: Ein Mac braucht keinen Schutz** (C05, geplant)  
Ansatz: macOS bringt eigenen Malware-Schutz mit, aber gegen Phishing und gestohlene Passwörter hilft das Betriebssystem nicht  
Quellen: <https://support.apple.com/guide/security/protecting-against-malware-sec469d47bd8/web> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Schadprogramme/schadprogramme_node.html>

**Mo 30.11. · Thema 2 · US-KI-Anbieter: Steht er auf der DPF-Liste?** (E15, geplant)  
Ansatz: Für Datenübermittlungen an US-Anbieter ist die Zertifizierung nach dem EU-US Data Privacy Framework eine öffentliche, prüfbare Grundlage  
Quellen: <https://www.dataprivacyframework.gov/list> · <https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en>

**Mo 30.11. · Thema 3 · Laptop verschlüsseln: aus Datenpanne wird Sachschaden** (B18, geplant)  
Ansatz: Mit eingeschalteter Geräteverschlüsselung ist ein gestohlener Laptop ein Sachschaden und keine Datenpanne  
Quellen: <https://support.microsoft.com/en-us/windows/device-encryption-in-windows-cf7e2b6f-3e70-4882-9532-18633605b7df> · <https://support.apple.com/guide/mac-help/protect-data-on-your-mac-with-filevault-mh11785/mac> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Daten-sichern-verschluesseln-und-loeschen/daten-sichern-verschluesseln-und-loeschen_node.html>

**Di 01.12. · Thema 1 · Die Rechnung, die amtlich aussieht** (D07, geplant)  
Ansatz: Nach einer Firmeneintragung kommen oft amtlich wirkende Angebote und Rechnungen; echte Gebühren kommen nur vom Register selbst  
Quellen: <https://www.ihk.de/osnabrueck/recht-und-fair-play/recht/adressbuchschwindel-1074078> · <https://www.gov.uk/guidance/reporting-scams-pretending-to-be-from-companies-house> · <https://www.gov.uk/government/news/companies-house-and-intellectual-property-office-ipo-join-forces-to-warn-about-unsolicited-payment-requests>

**Di 01.12. · Thema 2 · Das NIST-Rahmenwerk in der Kurzfassung für Kleinbetriebe** (A11, geplant)  
Ansatz: Das NIST Cybersecurity Framework 2.0 hat eine Kurzanleitung für Kleinbetriebe mit sechs Funktionen, vom Regeln-Festlegen bis zum Wiederherstellen  
Quellen: <https://www.nist.gov/cyberframework> · <https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1300.pdf> · <https://www.nist.gov/itl/smallbusinesscyber>

**Di 01.12. · Thema 3 · Cloud-Freigaben: Wer hat noch den Link?** (B19, geplant)  
Ansatz: Freigaben für alle mit dem Link bleiben offen, bis jemand sie schließt; ein regelmäßiger Blick in die Freigaben reicht  
Quellen: <https://learn.microsoft.com/en-us/sharepoint/turn-external-sharing-on-or-off> · <https://support.google.com/drive/answer/2494822>

**Mi 02.12. · Thema 1 · Die OWASP-Liste der KI-Risiken** (E11, geplant)  
Ansatz: Die OWASP Top 10 für LLM-Anwendungen sind eine freie Checkliste, mit der auch Kleinbetriebe ihre KI-Einbindung prüfen können  
Quellen: <https://genai.owasp.org/llm-top-10/> · <https://genai.owasp.org/llmrisk/llm01-prompt-injection/>

**Mi 02.12. · Thema 2 · Mythos: Wer zahlt, bekommt seine Daten zurück** (C16, geplant)  
Ansatz: Eine Lösegeldzahlung garantiert keine Wiederherstellung; Behörden raten davon ab, der verlässliche Ausweg ist das geprüfte Backup  
Quellen: <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Cyber-Sicherheitslage/Analysen-und-Prognosen/Ransomware-Angriffe/ransomware-angriffe_node.html> · <https://www.ncsc.gov.uk/guidance/mitigating-malware-and-ransomware-attacks>

**Mi 02.12. · Thema 3 · Wenn jemand geht: Zugänge am letzten Tag sperren** (B15, geplant)  
Ansatz: Beim Ausscheiden von Mitarbeitenden gehören Konten, Geräte und geteilte Passwörter auf eine Checkliste für den letzten Arbeitstag  
Quellen: <https://www.ncsc.gov.uk/collection/10-steps/identity-and-access-management> · <https://learn.microsoft.com/en-us/microsoft-365/admin/add-users/remove-former-employee>

**Do 03.12. · Thema 1 · Ist das schon KI? Wie der AI Act KI-Systeme abgrenzt** (A09, geplant)  
Ansatz: Nicht jede Software ist ein KI-System im Sinn des AI Act; die Leitlinien der Kommission helfen, die eigenen Werkzeuge einzuordnen  
Quellen: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-3> · <https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-ai-system-definition-facilitate-first-ai-acts-rules-application>

**Do 03.12. · Thema 2 · Zahl, oder es hagelt Ein-Stern-Bewertungen** (D14, geplant)  
Ansatz: Bewertungs-Erpressung ist eine eigene Masche; Google hat dafür ein Meldeformular, und zahlen beendet sie nicht  
Quellen: <https://support.google.com/business/answer/16404809> · <https://support.google.com/contributionpolicy/answer/7400114>

**Do 03.12. · Thema 3 · KI-Skripte: erst verstehen, dann ausführen** (E16, geplant)  
Ansatz: Was eine KI an Makros oder Skripten liefert, läuft mit deinen Rechten; ungeprüft ausgeführt kann es Daten löschen oder preisgeben  
Quellen: <https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/> · <https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/KI/Generative_KI-Modelle.html>

**Fr 04.12. · Thema 1 · E-Mail-Konto gehackt: die ersten Schritte** (B17, geplant)  
Ansatz: Wer ein gehacktes E-Mail-Konto in der richtigen Reihenfolge zurückholt, schließt auch die Tür, durch die der Angreifer kam  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Cyber-Sicherheitslage/Methoden-der-Cyber-Kriminalitaet/Identitaetsdiebstahl/Hilfe-fuer-Betroffene/hilfe-fuer-betroffene_node.html> · <https://www.ncsc.gov.uk/guidance/recovering-a-hacked-account>

**Fr 04.12. · Thema 2 · Fünf Fragen an jeden KI-Anbieter** (E19, geplant)  
Ansatz: Vor dem Einsatz eines KI-Tools klären fünf Fragen das Wesentliche: Training, Speicherort, Vertrag, Löschung und Zugriff  
Quellen: <https://www.datenschutzkonferenz-online.de/media/oh/20240506_DSK_Orientierungshilfe_KI_und_Datenschutz.pdf> · <https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Kuenstliche-Intelligenz/AIC4/aic4_node.html>

**Fr 04.12. · Thema 3 · Mythos: Der AI Act betrifft nur KI-Hersteller** (C14, geplant)  
Ansatz: Der AI Act kennt auch Pflichten für Betreiber, also für Betriebe, die KI nur einsetzen: KI-Kompetenz, Transparenz und bei Hochrisiko-Systemen ab Dezember 2027 menschliche Aufsicht  
Quellen: <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-26> · <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai> · <https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act>

**Sa 05.12. · Thema 1 · SIM-Swap: Wenn deine Nummer plötzlich tot ist** (D12, geplant)  
Ansatz: Beim SIM-Swap übernehmen Betrüger die Handynummer und damit SMS-Codes; App- oder Passkey-Anmeldungen sind deshalb besser als SMS  
Quellen: <https://www.ic3.gov/PSA/2022/PSA220208> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Cyber-Sicherheitsempfehlungen/Accountschutz/Zwei-Faktor-Authentisierung/Bewertung-2FA-Verfahren/bewertung-2fa-verfahren_node.html>

**Sa 05.12. · Thema 2 · Data Act: Der Cloud-Wechsel wird leichter** (A12, geplant)  
Ansatz: Seit September 2025 müssen Cloud-Anbieter in der EU den Wechsel zu einem anderen Anbieter ermöglichen; das senkt die Abhängigkeit kleiner Betriebe  
Quellen: <https://digital-strategy.ec.europa.eu/en/policies/data-act> · <https://digital-strategy.ec.europa.eu/en/library/data-act-explained> · <https://eur-lex.europa.eu/eli/reg/2023/2854/oj>

**Sa 05.12. · Thema 3 · Phishing melden in 30 Sekunden** (B20, geplant)  
Ansatz: Eine verdächtige Mail weiterzuleiten dauert Sekunden und hilft, gefälschte Seiten für alle abzuschalten  
Quellen: <https://www.ncsc.gov.uk/collection/phishing-scams/report-scam-email> · <https://www.verbraucherzentrale.de/wissen/digitale-welt/phishingradar>

**So 06.12. · Thema 1 · KI-API-Schlüssel wie eine Kreditkarte behandeln** (E20, geplant)  
Ansatz: Ein KI-API-Schlüssel erlaubt Zugriff auf Kosten deines Kontos; er gehört nie in Code, Mails oder geteilte Dateien  
Quellen: <https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety> · <https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning>

**So 06.12. · Thema 2 · Mythos: Inkognito macht anonym** (C08, geplant)  
Ansatz: Der private Modus löscht nur den Verlauf auf dem eigenen Gerät; Arbeitgeber, Provider und Websites sehen weiter mit  
Quellen: <https://support.google.com/chrome/answer/95464> · <https://support.microsoft.com/en-us/microsoft-edge/browse-inprivate-in-microsoft-edge-cd2c9a48-0bc4-b98e-5e46-ac40c84e27e2> · <https://support.apple.com/guide/safari/browse-privately-ibrw1069/mac>

**So 06.12. · Thema 3 · Die Mail, die deine Firmenseite sperren will** (D16, geplant)  
Ansatz: Gefälschte Mails im Namen sozialer Netzwerke sollen Zugangsdaten abgreifen; wird die Firmenseite trotzdem gekapert, zählen Passwort ändern, Sitzungen beenden und Kontakte warnen  
Quellen: <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Wie-geht-Internet/Identitaetsdiebstahl-Social-Media/identitaetsdiebstahl-social-media_node.html> · <https://www.bsi.bund.de/DE/Themen/Verbraucherinnen-und-Verbraucher/Informationen-und-Empfehlungen/Onlinekommunikation/Soziale-Netzwerke/soziale-netzwerke_node.html>

## Offene Punkte

1. **Freigabe:** Der Plan ist ein Entwurf. Stefan gibt Reihen, Rhythmus und Themen frei oder streicht einzelne.
2. **Fertige Videos in den ersten Tagen:** Passkeys (Mo 09.11., 18:00 / 23:00) und KI-Kennzeichnung (Di 10.11., 14:00 / 20:00) liegen nur als DE-Export vor; die EN-Fassungen haben ein Skript, aber kein Video. Die Skripte tragen noch die alten Themen-IDs (05.–07.11.); vor der Produktion auf die neuen IDs umstellen oder neu erzeugen. Gleiches gilt für das KI-Chat-Skript (Mo 09.11., 14:00 / 20:00).
3. **AI Omnibus:** Laut Kommission seit 27.07.2026 in Kraft (KI-Kompetenz ohne vorgeschriebenes Niveau, neuntes Verbot ab Dezember 2026, Hochrisiko ab 02.12.2027). Das fertige Video KI-Kennzeichnung vor dem Posten gegen die aktuelle Kommissionsseite und die Transparenz-Leitlinien prüfen.
4. **Ein Thema bleibt Idee:** „Gefälschte KI-Apps“ (So 29.11., 12:00 / 15:00) hat nur eine geöffnete Primärquelle; der Meta-Bericht vom Mai 2023 war nicht abrufbar. Zweite Quelle finden oder Thema tauschen.
5. **EN-Belege für deutsche Themen:** „Die richtige Nummer im Display“ (So 22.11., 18:00 / 23:00) stützt sich nur auf die Bundesnetzagentur; Ofcom blockte den Abruf. Für die EN-Fassung vor dem Skript eine britische oder US-Quelle ergänzen. Beim Thema KI-Protokoll im Meeting (§ 201 StGB) die EN-Fassung als deutsches Beispiel kennzeichnen.
6. **Risikostufe:** Kein Thema ist „high“. Stefan kann die Reihe „Was gilt wirklich“ und das § 201-Thema auf „high“ setzen, damit Rechtsthemen immer auf ihn warten.
7. **Quellen veralten:** Alle Quellen am 01.11.2026 geprüft. Themen ab Dezember vor dem Skript neu öffnen, besonders AI Act, NIS2 und Produktseiten (Microsoft, Google, OpenAI, Anthropic).
8. **Puffer:** Der Fragenkatalog sieht 7 bis 14 Tage fertige Videos im Voraus vor. Für den Start am 09.11. müsste die erste Woche bis etwa 02.11. produziert sein; sonst Start verschieben.
