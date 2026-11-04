# Anleitung: Google Workspace fertigstellen (Gmail-Filter, Absicherung, Markenkonten, Zustelltest)

Stand: 04.11.2026 (Wien). Verfasst von Claude für Stefan. Du klickst, ich führe dich Schritt für Schritt. Keine Zugangsdaten in dieser Datei. Menüpfade nennen die Bezeichnungen, die Google zuletzt verwendet hat; ändert Google die Namen, folge der Bezeichnung. Was ich nicht geprüft habe, steht dabei.

Reihenfolge: 1 Absicherung, 2 Gmail-Filter, 3 Zustelltest, 4 Admin-Konsole, 5 zweiter Inhaber. Dauer insgesamt etwa 30 bis 40 Minuten, am Laptop.

---

## 1. admin@scutoria.com absichern

admin@ ist die Zentrale für alle neun Marken; wer es übernimmt, hat alle Kanäle. Darum zuerst.

1. Mit admin@scutoria.com anmelden, Google-Konto öffnen (myaccount.google.com), Bereich „Sicherheit“.
2. **Passkey** anlegen (Windows Hello am Laptop genügt) oder einen **Sicherheitsschlüssel** registrieren, wenn du einen hast. Besser beides: Passkey am Laptop, Schlüssel oder zweites Gerät als Ersatz.
3. **Bestätigung in zwei Schritten** aktiv lassen oder einschalten.
4. **Wiederherstellungs-E-Mail** eintragen, die **nicht** auf scutoria.com liegt (zum Beispiel deine private Gmail-Adresse). Grund: Fällt die Domain aus, kommst du sonst nicht mehr an die Wiederherstellung.
5. **Wiederherstellungs-Telefonnummer:** optional. Ob eine hier hinterlegte Nummer auf die YouTube-Grenze (zwei Kanäle je Nummer und Jahr) angerechnet wird, ist nicht ermittelbar (keine Quelle geprüft). Im Zweifel keine Nummer eintragen; Wiederherstellung läuft dann über die Adresse außerhalb der Domain und die Backup-Codes.
6. **Backup-Codes** erzeugen und **ausdrucken oder offline** ablegen, nicht in OneDrive und nicht im Chat.
7. In der Admin-Konsole (admin.google.com) für Super-Admins prüfen, dass die Zwei-Schritt-Bestätigung nicht ausgeschaltet ist. Nicht geprüft, wo genau Google das für deine Edition zeigt.

Sag mir danach „Absicherung fertig“; ich trage es in `Stand Konten.md` ein.

---

## 2. Gmail-Filter je Marke

Ziel: Mails an die Alias-Adresse einer Marke bekommen das Label dieser Marke. Scutoria ist erledigt (02.11.2026); acht fehlen: Promptwerk, Tintora, Dewlane, Revlore, Gigastruct, Suitwerk, Frontlore, Gritwerk.

Je Marke (am Laptop, in Gmail von admin@):

1. Gmail › Zahnrad › „Alle Einstellungen aufrufen“ › Reiter „Filter und blockierte Adressen“ › „Neuen Filter erstellen“.
2. Feld **An** ausfüllen mit dem Alias, zum Beispiel `promptwerk@scutoria.com`. Weiter mit „Filter erstellen“.
3. Haken bei **„Label anwenden“**, „Neues Label“ wählen, Name der Marke (zum Beispiel `Promptwerk`). Optional „Posteingang überspringen (Archivieren)“ nicht anhaken, damit du Verifizierungsmails nicht übersiehst.
4. „Filter erstellen“.

Tipp: Lege zuerst alle acht Labels an (Seitenleiste › „Neues Label erstellen“), dann gehen die Filter schneller. Namensschema: genau der Markenname, ohne Zusatz.

Nicht geprüft: ob Gmail bei Mails an Aliase das Feld „An“ so füllt, dass der Filter greift. Genau das prüft der Zustelltest in Abschnitt 3.

---

## 3. Zustellung der Aliase testen

1. Von deinem privaten Konto (stefan.dallinger.me@gmail.com) **eine** Mail senden, im Feld „An“ alle neun Adressen: `social@`, `promptwerk@`, `tintora@`, `dewlane@`, `revlore@`, `gigastruct@`, `suitwerk@`, `frontlore@`, `gritwerk@` (jeweils `@scutoria.com`). Betreff: „Alias-Test 04.11.“.
2. In admin@ die Mail öffnen: Erwartung (nicht geprüft): Sie kommt nur einmal an, weil alle neun Adressen auf dasselbe Postfach zeigen, und **alle neun Labels** hängen an der Mail.
3. Fehlt ein Label, ist entweder der Filter falsch (Tippfehler im Alias) oder der Alias fehlt. Dann sende ich dir die Prüfschritte für genau diese Marke.
4. Zweiter Test, **ausgehend**: Nicht nötig. Anmeldungen laufen mit dem Alias nur zum Empfang; bei TikTok und Instagram kommen Codes an die Alias-Adresse, du antwortest nicht.

Wenn du möchtest, schicke ich die Testmail nicht selbst; Mails in deinem Namen sende ich nur auf dein ausdrückliches Wort.

---

## 4. Admin-Konsole: Markenkonten und YouTube einschalten

1. admin.google.com › Apps › „Weitere Google-Dienste“ (Bezeichnung laut `Anleitung Kanäle anlegen`, nicht neu geprüft).
2. Dienst **YouTube** auf „Für alle aktiviert“ oder für die Organisation einschalten.
3. Dienst für **Markenkonten** (englisch „Brand Account“; die genaue deutsche Bezeichnung ist nicht geprüft): einschalten. Falls es keinen eigenen Schalter gibt, steht die Möglichkeit, Kanäle als Markenkonto zu führen, in den YouTube-Einstellungen; dann sage mir, was du siehst, und wir klären es am Bildschirm.
4. Speichern. Änderungen können einige Minuten bis Stunden brauchen.

---

## 5. Zweiter Inhaber der YouTube-Markenkonten (Notfallzugang)

Wer? Eine Person, der du vertraust und deren Google-Konto **außerhalb** von scutoria.com liegt, damit es bei einem Domainproblem noch geht. Das entscheidest du; ich nenne niemanden. Ohne zweiten Inhaber bleibt admin@ der einzige Zugang.

Eintragung später je Kanal in YouTube (Einstellungen › Berechtigungen, Rolle „Inhaber“). Bis du die Person festgelegt hast, legen wir die Kanäle an und tragen den zweiten Inhaber nach; das ist ein Nachtrag, kein Hindernis für den Start.
