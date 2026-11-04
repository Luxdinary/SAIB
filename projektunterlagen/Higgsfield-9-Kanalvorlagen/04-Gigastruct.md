# Gigastruct: Vorlage für Higgsfield und Claude

Entwurf vom 30.10.2026. Grundlage: Markenregister und bestehende Konfiguration `C:\Automation\faceless-network\brands\megaconstruction`. Noch kein Higgsfield-Projekt, keine Generierung und keine Kosten ausgelöst. Bestehende Farben/Schriften übernommen; Szenen und Bewegungsregeln sind Vorschläge zur Verbesserung. Drive-Übersicht nicht erreichbar, daher vor endgültigem Einfrieren abgleichen.

## Direkt in Claude mit aktivem Higgsfield-Connector einfügen

```text
Entwickle mit mir eine wiederverwendbare Kanalvorlage für Gigastruct (Marken-ID megaconstruction).
Ich brauche ein System für viele unterschiedliche Themen, keine bloße Logoanimation und kein einzelnes fertiges Video.

GESTALTUNG
Architekturmodell, Größenvergleich und Bauphasen schaffen nachvollziehbare Größe statt beliebiger Drohnenbilder.
Palette: bg: #20384F; accent: #FF8A2A; text: #E9EDF0; surface: #30465B; muted: #8F9CA8.
Schriften für die spätere Codefassung: Oswald, Inter. Wenn diese im Werkzeug nicht verfügbar sind, Abweichung benennen; keine exakte Schriftwiedergabe versprechen.

FORMAT UND AUFBAU
9:16, Ziel 1080 × 1920, 30 fps. Zunächst ein 15-Sekunden-Designmuster; spätere Episoden 65–90 Sekunden. Nicht mit Logo-Intro beginnen. Marke klein ab dem ersten Bild. Ein großes Hauptmotiv pro Einstellung; die Bildmitte aktiv nutzen. Sinnvolle Bildentwicklung statt gleichförmiger Texttafeln.
Baue folgende austauschbare Szenenmodule: Größen-Hook; Bauphasen; Schnittmodell; nachgerechneter Maßstabsvergleich; Detailzoom; Gesamtansicht.
Untertitel in kurzen sinnvollen Wortgruppen, normale Schreibweise und deutliche Wortabstände. Nicht mit Erklärungstext überlagern. Text, Logo und Untertitel möglichst separat bearbeitbar halten; wenn das nicht möglich ist, eine saubere textfreie Fassung plus exakten Overlay-Zeitplan liefern.
Alle wichtigen Elemente mit Plattform-Bedienelementen im Hochformat prüfen; keine pauschale Safe-Zone-Garantie.

TESTTHEMA
Wie ein Brückenmodell Schritt für Schritt entsteht.
Storyboard: 0–3 s: stilisiertes Brückenmodell wird räumlich enthüllt. 3–7 s: Pfeiler und Überbau separat sichtbar. 7–11 s: abstrahierte Bauphasen bauen aufeinander auf. 11–15 s: Gesamtmodell und Kanalaufruf. Ohne Zahlen und ohne Bezug auf ein reales Projekt.
Gesprochener Hauptaufruf am Ende: „Große Bauwerke verständlich erklärt: Folge Gigastruct.“
Website: Keine bestätigte Website verwenden; keine Domain oder Handles erfinden.
Abschluss mit Markenname und Kanalaufruf, ohne erfundene Kontaktangaben.

INHALTSREGELN
Testmodell als Illustration kennzeichnen. Bei realen Bauwerken Geometrie, Maße, Bauverfahren und Termine mit Projektquellen prüfen. Keine geschätzten Größenvergleiche.
Das Muster dient der Designabnahme, nicht als fachlich freigegebene Veröffentlichung. Fachliche Aussagen vor Vertonung prüfen. DE und EN mit getrennten Text- und Audiofeldern vorsehen. Zunächst DE testen. „KI-generiert“ als einplanbares Overlay führen; Musik nur mit geklärter Lizenz. Beim Vorlagenwechsel Referenzmusik nicht automatisch übernehmen.

ARBEITSWEISE
1. Zeige zuerst zwei passende Designrichtungen oder verfügbare Vorlagen und empfehle eine anhand der Marke. Falls /katana keine passende Vorlage liefert, sage das; wähle keinen beliebigen Effekt als Ersatz.
2. Liefere Storyboard, benötigte Assets und exakte Creditkosten vor Generierung. Keine neun Generierungen auf einmal. Warte vor kostenpflichtiger Ausführung auf meine konkrete Freigabe.
3. Kläre, ob ich nur MP4, einzelne Clips, ein editierbares Projekt oder ausführbaren Quellcode erhalte. Nenne unterstützte Exportformate tatsächlich, statt sie zu erfinden.
4. Ziel ist spätere Produktion nur mit Claude Code und lokalem Renderer. Liste pro Szene auf: direkt in Code nachbaubar, benötigt feste Bild-/Videoassets, benötigt bei neuen Themen erneut Higgsfield. Ein MCP-Aufruf aus Claude Code zählt nicht als unabhängiges lokales Rendern.
5. Nach Freigabe erst das 15-Sekunden-Muster erzeugen und prüfen. Danach die Regeln für 65–90 Sekunden ausarbeiten, mit alternativen Hooks und variabler Szenenfolge.
6. Dokumentiere Palette, Typografie, Layout, Bewegung, Szenendauern, Übergänge, Untertitel und Abschluss sowie alle Abweichungen. Liefere nach Möglichkeit saubere Einzelassets und einen Szenenplan; fehlende Exportmöglichkeiten offen benennen.
```

## Wiederverwendung nach Designabnahme

```text
Nutze die freigegebene Gigastruct-Vorlage in Version {VERSION}.
Thema: {THEMA}
Zielgruppe und Kernfrage: {KERNFRAGE}
Geprüftes Skript und Quellen: {SKRIPT_QUELLEN}
Sprache: {DE_ODER_EN}
Zieldauer: {65_BIS_90_SEKUNDEN}
Verfügbare Aufnahmen und Assets: {ASSETLISTE}
Abschluss: {KANALAUFRUF_UND_BESTAETIGTE_WEBSITE}
Wähle zur Aussage passende Szenenmodule, zeige den Zeitplan und nenne fehlende Assets. Verändere das freigegebene Design nicht stillschweigend. Benenne neue Generierungskosten und externe Abhängigkeiten vor der Ausführung. Keine Quellen oder Aufnahmen erfinden.
```

## Abnahme dieser Vorlage

- Auch ohne Ton verständliche visuelle Entwicklung, keine lange unveränderte Titelkarte.
- Unterscheidbar von den acht anderen Marken, nicht nur über die Akzentfarbe.
- Text austauschbar; keine eingebrannten Tippfehler. DE/EN-Textlängen praktisch prüfen.
- Mindestens Hook, Erklärung/Vergleich und Abschluss im Muster erkennbar.
- Exporte und externe Abhängigkeiten praktisch getestet; MP4 nicht als Codevorlage bezeichnen.
- Wiederverwendung mit einem zweiten Thema testen, bevor Version 1.0 festgelegt wird.
