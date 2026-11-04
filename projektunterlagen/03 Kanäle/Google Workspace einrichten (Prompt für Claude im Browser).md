# Google Workspace einrichten: Prompt für Claude im Browser

Stand: 02.11.2026, 16:07 (Wien). Grundlage: Entscheidung „1+8“ (Stefan, 02.11.2026), `02 Marke\Marken.md`. Keine Zugangsdaten in dieser Datei.

## Ergebnis des Laufs am 02.11.2026

Ausgeführt von Claude Code über Claude in Chrome, auf Stefans Anweisung „Ja, hier ausführen“.

- Bestandsaufnahme: Business Standard, 1 Nutzer (admin@), keine Gruppen, keine Aliase, keine Konflikte. Domain bestätigt, MX und DKIM in Ordnung, SPF mit Hinweis „Achtung“ (betrifft nur ausgehende Post).
- Teil 2 entfiel: YouTube war schon für alle eingeschaltet; die Berechtigung „Strikt eingeschränkt“ wird für angemeldete Nutzer nicht angewendet. Einen Schalter „Brand Account“ gibt es laut Google-Hilfe nur in Education-Versionen; „Zugriff auf zusätzliche Dienste ohne eigene Steuerung“ steht auf AN.
- Teil 3: alle neun Aliase angelegt und nach dem Neuladen geprüft. Die Konsole zeigte sie erst nach etwa einer Minute vollständig an.
- Teil 4: neun Filter per Filter-Import angelegt, die neun Labels entstanden dabei mit. Vorher den Gmail-Dialog „Smarte Funktionen“ in allen drei Stufen auf „deaktiviert“ gesetzt (datensparsame Wahl, in den Einstellungen änderbar).
- Absicherung, nur gelesen: Bestätigung in zwei Schritten bei admin@ AUS; Wiederherstellungs-E-Mail gesetzt; keine Wiederherstellungs-Telefonnummer.

## So benutzt du ihn

1. In Chrome selbst bei admin.google.com und Gmail als admin@scutoria.com anmelden.
2. Claude in Chrome öffnen und den Prompt unten vollständig einfügen.
3. Claude hält bei jeder Anmeldung, Passwort- oder Handy-Bestätigung an; das machst du, dann sagst du „weiter“.

Was Claude dabei **nicht** tut und bei dir bleibt: admin@ absichern (Passkey oder Sicherheitsschlüssel, Wiederherstellungsadresse), YouTube-Kanäle anlegen, TikTok und Instagram registrieren. Das sind Sicherheitseinstellungen und Kontoanlagen.

Vorschläge von Claude im Prompt: die Adresse `social@scutoria.com` für Scutoria und „Nie als Spam einstufen“ in den Filtern, damit Bestätigungscodes von TikTok und Instagram nicht im Spam landen.

## Prompt

```text
Du arbeitest in meinem Chrome. Ich bin Stefan. Ich habe mich selbst als admin@scutoria.com (Super-Admin, Google Workspace, Domain scutoria.com) bei admin.google.com und Gmail angemeldet. Antworte auf Deutsch, kurz und ohne Emojis.

ZIEL
admin@scutoria.com ist die Zentrale für meine neun Videomarken („1+8“: Scutoria als Hauptmarke, acht Marken darunter). Du bereitest das Konto vor: zwei Dienste einschalten, neun E-Mail-Aliase anlegen, je Marke ein Gmail-Label mit Filter. Mit den Aliasen registriere ich später TikTok und Instagram. Die YouTube-Kanäle lege ich danach selbst als Markenkonten (Brand Accounts) an.

GRUNDREGELN
- Gib keine Passwörter, Codes oder Sicherheitsschlüssel ein. Kommt eine Anmeldung, Passwortabfrage oder Bestätigung am Handy: anhalten und mir Bescheid geben. Ich erledige das, dann geht es weiter.
- Sicherheitseinstellungen nur lesen, nie ändern: Bestätigung in zwei Schritten, Passkeys, Wiederherstellung, Passwortrichtlinien, Admin-Rollen.
- Lege keine Nutzer, Gruppen oder Konten an. Lösche nichts, kaufe nichts, ändere keine Lizenz oder Abrechnung, sende keine E-Mail.
- Erlaubt sind nur die Änderungen in Teil 2 bis 4, mit genau den Werten aus der Tabelle. Hiermit erlaube ich sie ausdrücklich.
- Weicht etwas ab, halte an und frag mich. Das gilt, wenn eine Adresse schon vergeben ist, ein Menü fehlt oder eine Einstellung mehr Nutzer betrifft als admin@.
- Die Menünamen hier sind nur Orientierung. Die Oberfläche kann deutsch oder englisch sein und anders heißen. Richte dich nach dem Bildschirm.
- Sag vor jedem Speichern in einem Satz, was du speicherst.

DIE NEUN MARKEN
Marke       | Alias von admin@scutoria.com | Gmail-Label
Scutoria    | social@scutoria.com          | Scutoria
Promptwerk  | promptwerk@scutoria.com      | Promptwerk
Tintora     | tintora@scutoria.com         | Tintora
Dewlane     | dewlane@scutoria.com         | Dewlane
Revlore     | revlore@scutoria.com         | Revlore
Gigastruct  | gigastruct@scutoria.com      | Gigastruct
Suitwerk    | suitwerk@scutoria.com        | Suitwerk
Frontlore   | frontlore@scutoria.com       | Frontlore
Gritwerk    | gritwerk@scutoria.com        | Gritwerk
Nicht anlegen: zonkfruit@scutoria.com (die Marke heißt jetzt Tintora).

TEIL 1: BESTANDSAUFNAHME (nur lesen)
1. Welche Workspace-Edition, wie viele Lizenzen? Ist die Domain scutoria.com bestätigt?
2. Verzeichnis › Nutzer: alle Nutzer auflisten. Bei admin@scutoria.com die vorhandenen Aliase (alternative E-Mail-Adressen) und die Organisationseinheit notieren.
3. Prüfen, ob einer der neun Aliase schon als Nutzer, Gruppe oder Alias existiert. Wenn ja, markiere ihn als „Konflikt“ und lege ihn nicht an.
4. Sicherheit, nur lesen: Ist für admin@ die Bestätigung in zwei Schritten aktiv, und mit welcher Methode? Zeigt die Konsole eine Wiederherstellungs-E-Mail oder -Telefonnummer?
5. Apps › Weitere Google-Dienste: Status von „Brand Account“ bzw. „Markenkonto“ und von „YouTube“ für die Organisationseinheit von admin@. Prüfe auch, ob es bei Brand Accounts eine Einstellung gibt, wer Inhaber sein darf, z. B. nur Nutzer der Organisation. Nur berichten.
Zeig mir das Ergebnis als kurze Tabelle. Warte auf mein „weiter“, bevor du Teil 2 beginnst.

TEIL 2: DIENSTE EINSCHALTEN
1. Apps › Weitere Google-Dienste › Brand Account: Dienststatus für die Organisationseinheit von admin@ auf AN.
2. Apps › Weitere Google-Dienste › YouTube: Dienststatus AN. Unter Berechtigungen die Stufe wählen, mit der angemeldete Nutzer Kanäle anlegen und Videos hochladen können. Wenn dafür eine Altersangabe oder eine Einstellung für die ganze Organisation nötig ist, frag mich vorher.
Hinweis an mich, falls zutreffend: Änderungen können bis zu 24 Stunden brauchen.

TEIL 3: ALIASE ANLEGEN
Verzeichnis › Nutzer › admin@scutoria.com › Nutzerinformationen › Alternative E-Mail-Adressen (E-Mail-Aliase): die neun Adressen aus der Tabelle eintragen, außer denen mit Konflikt. Danach die Seite neu laden und prüfen, ob alle da sind.

TEIL 4: GMAIL-LABELS UND FILTER (mail.google.com, angemeldet als admin@scutoria.com)
1. Je Marke ein Label mit dem Namen aus der Tabelle anlegen.
2. Je Marke einen Filter anlegen: Feld „An“ = Alias der Marke. Aktion: Label der Marke anwenden und „Nie als Spam einstufen“. Nicht archivieren, nicht weiterleiten, nichts löschen.
3. Prüfen: Unter Einstellungen › Filter und blockierte Adressen stehen neun Filter.

TEIL 5: BERICHT
Zum Schluss eine Tabelle mit den Spalten Schritt, Ergebnis (erledigt / Konflikt / übersprungen / wartet auf Stefan) und Hinweis. Danach die Liste, was ich selbst tun muss:
- admin@ mit Passkey oder Sicherheitsschlüssel absichern und eine Wiederherstellungsadresse außerhalb von scutoria.com hinterlegen, falls das noch fehlt.
- Von meiner privaten Adresse an jeden Alias eine Testmail schicken und prüfen, ob das Label greift.
- Die YouTube-Kanäle als Markenkonten unter admin@ anlegen, je mit einem zweiten Inhaber.
```

## Quellen

- E-Mail-Aliase, bis zu 30 je Nutzer: [support.google.com/a/answer/33327](https://support.google.com/a/answer/33327)
- Weitere Google-Dienste ein- und ausschalten: [knowledge.workspace.google.com › turn-on-or-off-additional-google-services](https://knowledge.workspace.google.com/admin/users/advanced/turn-on-or-off-additional-google-services)
- Markenkonten ein- und ausschalten: [support.google.com/accounts/answer/9377793](https://support.google.com/accounts/answer/9377793). Ohne aktiven Inhaber wird ein Markenkonto 21 Tage gesperrt und dann gelöscht.
- YouTube-Einstellungen der Organisation: [knowledge.workspace.google.com/admin/youtube](https://knowledge.workspace.google.com/admin/youtube)
