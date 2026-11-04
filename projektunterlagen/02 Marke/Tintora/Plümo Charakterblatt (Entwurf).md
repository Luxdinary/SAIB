# Plümo – Charakterblatt (Entwurf)

Stand 30.10.2026. Figur der Marke Zonkfruit (`brainrot`). Nur mit Code erzeugt (SVG aus `brands/brainrot/renderer/plumo.py`), kein KI-Bild, kein Higgsfield. **Entwurf, bis Stefan freigibt.**

## Dateien

| Datei | Inhalt |
|---|---|
| `plumo_sheet.png` | Charakterblatt: vorne, Seite, hinten, sechs Posen, Farben, Merkmale |
| `plumo_front.svg`, `plumo_side.svg`, `plumo_back.svg` | Ansichten (neutral) |
| `plumo_pose_<name>.svg` | Posen: neutral, staunen, stolz, zeigen, verwirrt, umgekippt |
| `../logo/zonkfruit-mark.svg` | Logo-Marke (Plümos Kopf) |
| `../../renderer/plumo.py` | Generator; jede Szene baut die Figur daraus, IDs `<uid>-lidL`, `-pupL`, `-m-<mund>`, `-leaf`, `-stem` |

## Name

Vorschlag **Plümo** (EN: Plumo), von „plumps“ (Geräusch beim Umfallen). „Zonk“ als Figurenname scheidet aus: Zonk ist eine Videospielfigur von Hudson Soft (Air Zonk, 1992). Die Marke heißt weiter Zonkfruit (Stefans Entscheidung vom 30.10.2026).

## Feste Farben (Hex)

Körper #B7FF00 · Licht #ECFFA6 · Mittelton #8FD600 · Schatten #4E8C00 · Lid #9BE000 · Kante #2C4F00 · Randlicht #FF43C0 · Blatt #FF43C0 / #C21F8C · Blattader #7A1F5E · Stiel #B04A92 · Auge #FFF7FB · Pupille #101010 · Mund #3B0F31 · Sommersprossen #FF43C0 · Etikett #FFF2C7 mit Schrift #101010.

## Unveränderliche Merkmale (Style-Lock)

1. Gummidrop-Silhouette mit rundem Boden; er kippt um und steht wieder auf (das ist der „Zonk“).
2. Spiralfeder als Stiel mit genau drei Windungen; schwingt elastisch nach.
3. Ein magenta Blatt ist seine einzige Hand: zeigt, winkt, stützt. Keine Arme, keine Beine.
4. Schwere Lider, Grundblick deadpan.
5. Drei magenta Sommersprossen im Dreieck, nur auf seiner rechten Wange (im Bild links), nie gespiegelt.
6. Etikett mit „?“ auf dem Rücken: Seine Sorte ist „nicht ermittelbar“ (Running Gag).
7. Keine Kleidung, keine Schrift am Körper, keine Zähne.
8. Licht von links oben, magenta Randlicht rechts, weicher Bodenschatten.

## Grundposen und Mimik

| Pose | Lider | Mund | Blatt | Einsatz |
|---|---|---|---|---|
| neutral | halb zu | flach | hängt rechts | Grundzustand, deadpan |
| staunen | offen, kleine Pupillen | o | hoch | Pointe trifft ihn |
| stolz | fast zu, Blick nach oben | schiefes Grinsen | an der „Hüfte“ | bevor er scheitert |
| zeigen | leicht offen, Blick zur Seite | spricht | waagrecht | erklärt, zeigt auf Labels |
| verwirrt | links offen, rechts halb | Wellenlinie | kratzt am Kopf | Denkfehler |
| umgekippt | zu | flach | schlaff | nach dem Scheitern, Loop-Start |

## Bewegungsstil

Elastisch: Squash und Stretch bei jedem Hüpfer (Bodenpunkt fest), Feder-Nachschwingen am Stiel, Blatt federt mit `back.out`, Umkippen mit `bounce.out` über die Unterkante, Aufstehen mit `elastic.out`. Atmen alle 0,8 s (Skalierung 0,985–1,025), damit er nie einfriert. Keine Stroboskope, keine Schockbilder.

## Ähnlichkeitsprüfung (Websuche 30.10.2026, Vorprüfung, keine Rechtsauskunft)

| Geprüft | Befund | Abgrenzung Plümo |
|---|---|---|
| Suche „lime green fruit mascot spring stem pink leaf“ | keine Figur mit dieser Kombination gefunden; nur Stock-Grafiken (z. B. Zitronenfigur) | – |
| Suche „roly-poly fruit character tips over“ | keine Fruchtfigur; Treffer: Weebles-Spielzeug (Eiform, „wobble but they don't fall down“), Wackelspielzeuge | Stehauf-Prinzip ist ein allgemeines Spielzeugprinzip; Plümo fällt um (Gegenteil des Weebles-Slogans), Frucht statt Ei-Figur |
| Annoying Orange (YouTube-Serie, Cartoon Network 2012) | fotorealistische Orange mit menschlichem Mund und Augen | Plümo ist stilisiert, lime, Feder-Stiel, deadpan statt laut |
| Barbapapa | rosa, runde Figur mit Gesicht, Erkennung über Farbe und Gesicht | Plümo lime, Blatt als Hand, Sommersprossen, Etikett; keine Formwandlung |
| Fruit of the Loom (Apfel, Blatt, Trauben) | Werbefiguren aus realistischen Früchten | keine Übereinstimmung |
| „Zonk“ | Air Zonk (Hudson Soft, 1992), Cyborg mit Sonnenbrille | deshalb kein Figurenname „Zonk“ |
| „Kippo“ | Manga-Titel von Hiroshi Tanaka | deshalb nicht als Figurenname |
| „Plümo“ / „Plumo“ | keine Figur gefunden | Namensvorschlag |

Nicht geprüft: Markenregister (TMview) für „Plümo“, Bildersuche (Rückwärtssuche ist ohne fertiges Bild im Netz nicht möglich). Vor einer Markenanmeldung oder Merchandise wäre eine anwaltliche Prüfung nötig.

Quellen der Suche: en.wikipedia.org/wiki/Air_Zonk · en.wikipedia.org/wiki/Annoying_Orange · en.wikipedia.org/wiki/Barbapapa · www.fandompost.com (Kippo-Manga) · www.overstreetaccess.com (Weebles).
