# Reel-Analyse: erstes Scutoria-Testvideo (ChatGPT)

Quelle: von Stefan am 30.10.2026 eingefügt. ChatGPT hat das erste Testvideo mit Gemini-Stimme (`05 Produktion\_Test\ai_security-20261105-1-de\video.mp4`, 74,17 s, 1080 × 1920, 30 fps) bewertet. Stefans Auftrag dazu: jedes Demo-Video je Kanal nacheinander, Abschnitt für Abschnitt, fertig machen; Beginn mit Scutoria. Hinweis: Der im Prompt genannte Projektpfad `C:\AI-Faceless-Network` ist falsch; das Repository liegt in `C:\Automation\faceless-network`. Aussagen zu Claude, KI-Training und Datenschutz sind vor jeder Produktion gegen aktuelle Primärquellen zu prüfen.

## Kernurteil

Technisch brauchbar, aber visuell eine animierte Präsentation, kein Reel: schwacher Einstieg („Heute: Einstellungen prüfen"), kaum visuelle Abwechslung (gleicher Hintergrund, gleiches Schildsymbol, ähnliche Textanordnung), schlecht genutzter Bildschirmraum (Information oben, viel Leere, Quellen zu klein), kein Spannungsbogen, Design auf eine Vorlage fixiert. Das Problem ist die visuelle Regie, nicht die Technik. Claude braucht Regeln für Hook, Szenenwechsel, Bewegung und Dramaturgie, nicht nur ein Design-Template.

## Fünf Befunde mit Verbesserung

1. **Einstieg:** statt Checklistenformulierung eine Frage, die eine Wissenslücke öffnet, z. B. „Kannst du Claude mit Firmendaten nutzen, ohne dass sie zum KI-Training verwendet werden?"
2. **Visuelle Abwechslung:** zwischen Bildschirmaufnahmen, animierten Datenflüssen, großen Aussagen, Vergleichskarten und Grafiken wechseln.
3. **Bildschirmraum:** ein dominantes Motiv je Szene, Fokus in der Bildmitte, gut lesbare Einblendungen.
4. **Dramaturgie:** eine Leitfrage, drei überprüfbare Erkenntnisse, eine eindeutige Schlussfolgerung.
5. **Vorlage:** Logo, Farben, Typografie konstant; drei bis fünf verschiedene Szenenlayouts innerhalb derselben Identität.

## Vorgeschlagener Schnittplan (70–80 s)

| Zeit | Funktion | Bild | Sprecher |
|---|---|---|---|
| 0–3 s | Hook | große Frage, Dokument wandert in eine KI-Chatoberfläche, Warnsymbol | „Darfst du vertrauliche Firmendaten einfach in Claude eingeben?" |
| 3–10 s | Problem | animierte Trennung Mitarbeiter → KI-Dienst → Datenverarbeitungsweg | „Die Antwort hängt nicht nur von einer Einstellung ab." |
| 10–23 s | Erkenntnis | Vergleich zweier Kontokonfigurationen (nur geprüfte Produktinformation) | „Entscheidend sind Kontotyp, Vertragsbedingungen und die konkrete Datenverarbeitung." |
| 23–39 s | Demonstration | echte Bildschirmaufnahme, Cursorzoom, hervorgehobener Schalter | „Hier prüfst du, welche Optionen für dein Konto tatsächlich gelten." |
| 39–55 s | Denkfehler | großes NEIN über „Kein Training = keine weiteren Datenschutzfragen" | „Eine deaktivierte Trainingsnutzung ersetzt keine Datenschutzprüfung." |
| 55–69 s | Drei-Punkte-Check | drei Checkkarten: Vertrag, Kontokonfiguration, Freigabe | „Prüfe diese drei Punkte, bevor du sensible Inhalte hochlädst." |
| 69–76 s | Abschluss | Scutoria-Endscreen, animierte Zusammenfassung, dezente Handlungsaufforderung | „Speichere die Checkliste für deinen nächsten KI-Einsatz im Unternehmen." |

## Neue Gestaltungsregeln für Scutoria

Farben bleiben (Marineblau, Türkis, Weiß); geändert wird ihr Einsatz.

| Element | Vorgabe |
|---|---|
| Einstieg | in den ersten 2 Sekunden eine konkrete Frage, ein überraschender Fakt oder ein sichtbares Problem |
| Szenen | unterschiedliche Kompositionen, keine identischen Folien |
| Bewegung | animierte Objekte, Kamerabewegung, UI-Demonstrationen, wechselnde Perspektiven |
| Untertitel | lesbar, sprechersynchron, gezielte Hervorhebung |
| Bildmaterial | mindestens zwei verschiedene Darstellungsformen je Video |
| Logo | klein und konstant, nicht Hauptmotiv |
| Quellen | lesbare Kurzbelege oder Quellen im Begleittext |
| Sound | Übergangseffekte, bewusst eingesetzte Musik, Sprachpausen |
| Rhythmus | keine willkürliche Hektik; Schnitt dort, wo sich die Aussage entwickelt; Abstände aus Tests, keine starre Regel |

## Prompt-Kern für die Pipeline (von ChatGPT, auf das echte Repository anzuwenden)

- **Hook-Engine:** je Video mindestens fünf Hook-Ideen (provokante, vertretbare Frage · häufiger Denkfehler · überraschender belegbarer Sachverhalt · konkretes Risiko · sichtbare Demonstration), bewertet nach Klarheit, Relevanz, Neugier, Wahrheitsgehalt, visueller Umsetzbarkeit; die stärkste sachlich vertretbare gewinnt, nicht die dramatischste.
- **Story-Engine:** Hook → Problem → Erklärung → Demonstration → Erkenntnis → Nutzen → Abschluss; jede Szene mit Funktion, Wiederholungen streichen.
- **Motion-Design-Engine:** mindestens fünf wiederverwendbare Szenentypen: Cinematic Hook · UI Demonstration · Data Flow · Comparison · Key Takeaway; gleiche Identität, unterscheidbare Optik.
- **Brand-Design:** Typografie, Titelgrößen, Untertitelpositionen, sichere Zonen, Animationen, Übergänge, Icon-Stil, Kamerabewegungen, Szenenlayouts, Audio, Intro-/Outro-Varianten definieren; Logo konstant, kein Folien-Look.
- **Mediengenerierung:** je Szene passende Form (Bildschirmaufnahme, animiertes Diagramm, KI-Hintergrund, kurzer KI-Clip, programmatische Grafik, Textanimation); Text, Logo, Untertitel in der Render-Engine, nicht im KI-Bild.
- **Audio:** visuelle Ereignisse mit der Stimme synchronisieren; Musik, Effekte, Pausen gezielt; verständliche Lautstärke.
- **Fakten und Compliance:** Aussagen zu Claude, Training, Datenschutz, Unternehmenskonten gegen aktuelle Primärquellen prüfen; Kontotyp, Vertrag, Trainingsnutzung, Speicherung, weitere Verarbeitung, Unternehmensrichtlinien unterscheiden; keine unbelegten Versprechen; synthetische Darstellungen kennzeichnen.
- **Technik:** bestehende Pipeline untersuchen, Motion-Templates, datengetriebene Szenenbeschreibung, automatische Prüfungen für Auflösung, Dauer, Lesbarkeit, Untertitelposition, Audiopegel, Szenenvielfalt, Bildwechsel, Quellenmanifest.
- **Testproduktion:** 1. Analyse des Renderers · 2. neuer Szenenplan für das vorhandene Video · 3. drei Hook-Konzepte · 4. 15-Sekunden-Prototyp im neuen Design · 5. Vorher-Nachher · 6. Liste geänderter Dateien; volles Video erst nach Freigabe.
- Kein Clickbait ohne Einlösung, keine Viralitätsversprechen, keine unautorisierten API-Kosten, keine Veröffentlichung ohne Freigabe.

## Prioritäten (subjektiv, laut ChatGPT)

Hook und Leitfrage 10 · Szenenvielfalt 10 · Bewegung und Schnitt 9 · Storytelling 9 · Mobile Lesbarkeit 8 · Sounddesign 7.

Einschränkung der Analyse: Bild und Technik wurden geprüft, die Tonspur nicht transkribiert; die sprachliche Dramaturgie ist nur anhand der sichtbaren Inhalte bewertet.
