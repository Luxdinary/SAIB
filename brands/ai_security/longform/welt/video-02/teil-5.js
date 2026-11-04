// Teil 5 · Der Beispielbetrieb und seine Dokumente (Absätze 26 bis 31).
// Bühnen: der erfundene Betrieb mit seinen sechs Antworten (Kamera durch das Haus, Liste rechts) → D1 Selbstauskunft
// → D5 Antwortschreiben mit Abgleichstabelle → D4 Nachweisliste, ein datiertes Bild für den Kunden.
akt({
  name: 'beispiel',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    const K = { de: '5 · DER BEISPIELBETRIEB', en: '5 · THE EXAMPLE BUSINESS' };
    // ---------- Wortanker ----------
    const Q5 = quelle(); this.tQ5 = Q5.s;
    this.tErf = c('ist erfunden', 'is fictional');
    this.tElektro = c('Elektrotechnikbetrieb', 'electrical contractor');
    this.tBesch = c('Beschäftigten in Österreich', 'staff in Austria');
    this.tKeine = c('Keine Person', 'No person');
    this.tFB = c('einen Fragebogen geschickt', 'sent it a questionnaire');
    this.tMisch = c('Mischbild', 'mixed picture');
    this.tR = [c('bei E-Mail', 'on email'), c('Cloud-Konsole|Cloud Konsole|Cloudkonsole', 'cloud console'), c('tägliche Sicherung', 'daily backup'), c('Wiederherstellungstest', 'restore test'), c('Notfallplan', 'emergency plan'), c('alter Werkstattrechner|Werkstattrechner', 'old workshop computer|workshop computer')];
    const Q6 = quelle(); this.tQ6 = Q6.s;
    this.tNeun = c('Neun Abschnitte', 'Nine sections');
    this.tTab = c('Übersichtstabelle', 'overview table');
    this.tStand = c('Stand und Datum', 'status and its date');
    this.tUnter = c('Unterschriftszeile', 'signature line');
    this.tOrd = c('alles in Ordnung', 'all good');
    this.tHeute = c('heute vorhanden', 'in place today');
    this.tTeilw = c('teilweise da', 'partly there');
    this.tHat = c('einen Termin hat', 'has a date');
    this.tAS = c('Das Antwortschreiben sagt', 'The cover letter says');
    this.tKlein = c('eines kleinen Betriebs', 'a small business');
    this.tLuecken = c('welche Lücken', 'which gaps');
    const Q7 = quelle(); this.tQ7 = Q7.s;
    this.tTyp = c('typische Fragen', 'typical questions');
    this.tZehn = c('die zehn Bereiche', 'the ten areas');
    this.tVerw = c('verwiesen', 'pointed to');
    const Q8 = quelle(); this.tQ8 = Q8.s;
    this.tVorliegt = c('was vorliegt', 'only what exists');
    this.tMFA = c('bei E-Mail', 'on email');
    this.tNichtV = c('Was nicht vorliegt', 'What does not exist');
    this.tFrNr = c('Fragennummer', 'question number');
    this.tSatz = c('einen Termin und einen Satz', 'a date and a sentence');
    this.tOffen = c('Offene Punkte', 'Open points');
    this.tVersteckt = c('nicht versteckt', 'not hidden');
    this.tBild = c('datiertes Bild', 'dated picture');
    this.tVersp = c('kein Versprechen', 'not a promise');
    this.tEnde = cue({ de: 'Was dieses Toolkit nicht', en: 'What this toolkit is' }, { halten: true }).s;

    // ---------- Bühne 1: der erfundene Betrieb und seine Antworten ----------
    const b1 = buehne('beispiel-betrieb', { seed: 73 }); this.b1 = b1;
    const B = bauBetrieb(b1.cam); this.B = B;
    // eigener Rahmen für den Notfallplan an der Wand der Leitung, alter Rechner in der Werkstatt
    this.notfall = g(b1.cam); { el('rect', { x: 640, y: 340, width: 190, height: 150, rx: 8, fill: 'rgba(255,255,255,0.02)', stroke: C.amberLine, 'stroke-width': 4, 'stroke-dasharray': '12 9' }, this.notfall); T(this.notfall, 735, 404, { de: 'NOTFALL-', en: 'EMERGENCY' }, { mono: 1, size: 20, fill: C.amber, anchor: 'middle', ls: '0.08em' }); T(this.notfall, 735, 432, { de: 'PLAN', en: 'PLAN' }, { mono: 1, size: 20, fill: C.amber, anchor: 'middle', ls: '0.08em' }); T(this.notfall, 735, 470, '—', { size: 30, weight: 800, fill: C.amber, anchor: 'middle' }); }
    this.pc = g(b1.cam); { el('rect', { x: 2450, y: 770, width: 130, height: 80, rx: 4, fill: '#16203a' }, this.pc); el('rect', { x: 2455, y: 650, width: 120, height: 100, rx: 8, fill: '#3a3f4a', stroke: '#5a6070', 'stroke-width': 3 }, this.pc); el('rect', { x: 2469, y: 662, width: 92, height: 70, rx: 4, fill: '#20303a' }, this.pc); el('rect', { x: 2495, y: 750, width: 40, height: 20, fill: '#3a3f4a' }, this.pc); }
    this.sicherung = g(b1.cam); { el('rect', { x: 290, y: 800, width: 110, height: 52, rx: 6, fill: '#1f2c47', stroke: C.blue, 'stroke-width': 3 }, this.sicherung); el('circle', { cx: 380, cy: 826, r: 6, fill: C.green }, this.sicherung); }
    this.ziele = [[1194, 610], [1594, 610], [345, 826], [345, 826], [735, 415], [2515, 700]];
    this.ringe = this.ziele.map(() => el('circle', { r: 110, fill: 'none', stroke: C.blue, 'stroke-width': 6 }, b1.cam));
    this.stempel = stempel(b1.cam, { de: 'ERFUNDEN', en: 'FICTIONAL' }, C.amber, 56);
    this.beschP = pille(b1.cam, { de: '10 bis 49 Beschäftigte · Österreich', en: '10 to 49 staff · Austria' }, { icon: 'group', col: C.blue, size: 48 });
    this.echtP = pille(b1.cam, { de: 'niemand darin ist echt', en: 'nobody in it is real' }, { icon: 'person', col: C.amber, gestrichelt: true, size: 48 });
    this.umschlag = g(b1.cam); el('rect', { x: -64, y: -42, width: 128, height: 84, rx: 6, fill: C.paper, filter: 'url(#shadowS)' }, this.umschlag); el('path', { d: 'M -60 -38 L 0 6 L 60 -38', fill: 'none', stroke: C.pMuted, 'stroke-width': 4, 'stroke-linejoin': 'round' }, this.umschlag);
    // Liste der Antworten im Bildraum rechts
    this.liste = g(b1.front);
    karte(this.liste, 1180, 230, 650, 600, { fill: 'rgba(18,27,47,0.97)' });
    T(this.liste, 1214, 276, { de: 'ANTWORTEN DES BEISPIELBETRIEBS', en: 'ANSWERS OF THE EXAMPLE BUSINESS' }, { mono: 1, size: 18, fill: C.blue, ls: '0.1em' });
    const ZEILEN = [[{ de: 'MFA bei E-Mail', en: 'MFA on email' }, 'vorhanden', null], [{ de: 'MFA Cloud-Konsole', en: 'MFA cloud console' }, 'termin', null], [{ de: 'Tägliche Sicherung', en: 'Daily backup' }, 'teilweise', { de: 'keine Kopie außer Reichweite', en: 'no copy out of reach' }],
      [{ de: 'Wiederherstellungstest', en: 'Restore test' }, 'termin', { de: 'nie gemacht', en: 'never done' }], [{ de: 'Notfallplan', en: 'Emergency plan' }, null, { de: 'keiner', en: 'none' }], [{ de: 'Alter Werkstattrechner', en: 'Old workshop computer' }, null, null]];
    this.zeilen = ZEILEN.map(([name, art, zus], i) => {
      const y = 340 + i * 84, gr = g(this.liste);
      T(gr, 1214, y, name, { size: 26, weight: 800 });
      if (zus) T(gr, 1214, y + 30, zus, { mono: 1, size: 18, fill: C.muted });
      let p = null;
      if (art) { p = antwort(gr, art, { size: 20, text: art === 'termin' ? { de: 'Termin', en: 'Date' } : null }); tr(p, 1800 - p.w / 2, y - 8); }
      else if (i === 4) { p = pille(gr, { de: 'keiner', en: 'none' }, { col: C.amber, gestrichelt: true, size: 20, mono: false, weight: 700 }); tr(p, 1800 - p.w / 2, y - 8); }
      return { g: gr, p };
    });
    this.blicke = [{ f: [1560, 560], z: 0.85 }, { f: [1900, 560], z: 0.85 }, { f: [760, 600], z: 0.85 }, { f: [760, 600], z: 0.85 }, { f: [900, 560], z: 0.85 }, { f: [2880, 600], z: 0.85 }];
    shot(b1, this.tQ5 - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne 2: D1 Selbstauskunft ----------
    const b2 = buehne('beispiel-d1', { seed: 79, regalDeckkraft: 0.5 }); this.b2 = b2;
    const k2 = b2.cam;
    this.d1 = g(k2);
    const d1 = blatt(this.d1, { w: 640, h: 700, kicker: { de: 'D1 · SELBSTAUSKUNFT · MUSTER ELEKTROTECHNIK E.U.', en: 'D1 · SELF-DECLARATION · EXAMPLE ELECTRICAL LTD' }, kSize: 13, pad: 34 });
    this.reiter = Array.from({ length: 9 }, (_, i) => { const gr = g(d1.g); el('rect', { x: 320, y: -300 + i * 66, width: 46, height: 54, rx: 6, fill: C.blueSoft, stroke: C.blueBar, 'stroke-width': 2 }, gr); T(gr, 343, -266 + i * 66, String(i + 1), { mono: 1, size: 20, fill: C.blueDeep, anchor: 'middle' }); return gr; });
    T(d1.g, d1.left, d1.y + 24, { de: 'Übersicht', en: 'Overview' }, { size: 28, weight: 800, fill: C.pInk });
    const ST = [['vorhanden', C.green], ['termin', C.amber], ['teilweise', C.amber], ['termin', C.amber], ['termin', C.amber], ['teilweise', C.amber]];
    this.tabelle = ST.map(([art, col], i) => {
      const y = d1.y + 76 + i * 56, zg = g(d1.g);
      el('rect', { x: d1.left - 6, y: y - 24, width: 640 - 2 * d1.pad + 12, height: 46, rx: 6, fill: i % 2 ? '#f2f4f8' : 'none' }, zg);
      el('rect', { x: d1.left + 8, y: y - 6, width: 210 + ((i * 29) % 70), height: 11, rx: 5.5, fill: C.pBar }, zg);
      const st = g(zg); el('circle', { cx: d1.left + 360, cy: y, r: 12, fill: art === 'termin' ? 'none' : col, stroke: col, 'stroke-width': 3.5, 'stroke-dasharray': art === 'termin' ? '6 4' : '' }, st);
      T(st, d1.left + 382, y + 6, art === 'termin' ? { de: 'Termin', en: 'Date' } : ANTWORT[art].t, { size: 18, weight: 700, fill: C.pInk });
      const dat = T(zg, d1.right, y + 6, { de: 'Datum', en: 'date' }, { mono: 1, size: 15, fill: C.pMuted, anchor: 'end' });
      return { g: zg, st, dat };
    });
    el('rect', { x: d1.left, y: d1.y0 + 700 - 86, width: 240, height: 2, fill: C.pMuted }, d1.g);
    T(d1.g, d1.left, d1.y0 + 700 - 60, { de: 'Unterschrift der Leitung', en: 'Signed by the management' }, { mono: 1, size: 14, fill: C.pMuted });
    this.d1Sig = el('path', { d: `M ${d1.left + 10} ${d1.y0 + 700 - 94} c 14 -26 22 -26 26 -2 c 4 20 12 -30 26 -20 c 12 8 4 22 18 10 c 16 -14 26 -8 40 -4 c 12 4 26 -10 44 -6`, fill: 'none', stroke: C.blueDeep, 'stroke-width': 3.5, 'stroke-linecap': 'round' }, d1.g);
    this.d1SigRing = el('rect', { x: d1.left - 14, y: d1.y0 + 700 - 130, width: 280, height: 90, rx: 10, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, d1.g);
    this.ordnungP = g(k2); { const p = pille(this.ordnungP, { de: '„alles in Ordnung“', en: '"all good"' }, { col: C.muted, size: 30, gestrichelt: true, mono: false, weight: 800 }); this.ordnungS = streich(this.ordnungP, p.w, C.red); }
    this.d1Lampen = ['vorhanden', 'teilweise', 'termin'].map((a) => antwort(k2, a, { size: 30 }));
    shot(b2, this.tQ6 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 3: D5 Antwortschreiben, Abgleichstabelle ----------
    const b3 = buehne('beispiel-d5', { seed: 83, regalDeckkraft: 0.5 }); this.b3 = b3;
    const k3 = b3.cam;
    this.d5 = g(k3);
    const d5 = blatt(this.d5, { w: 600, h: 640, kicker: { de: 'D5 · ANTWORTSCHREIBEN', en: 'D5 · COVER LETTER' }, kSize: 14, pad: 34 });
    this.d5Abs = g(d5.g); el('rect', { x: d5.left - 10, y: d5.y - 4, width: 600 - 2 * d5.pad + 20, height: 112, rx: 10, fill: C.blueSoft }, this.d5Abs); T(this.d5Abs, d5.left, d5.y + 30, { de: 'Antworten eines kleinen Betriebs', en: 'The answers of a small business' }, { size: 26, weight: 800, fill: C.blueDeep }); linien(this.d5Abs, d5.left, d5.y + 52, 480, 2, 24, C.blueBar, 10);
    this.d5L = [0, 1, 2].map((i) => { const zg = g(d5.g); const y = d5.y + 160 + i * 58; el('rect', { x: d5.left - 10, y: y - 24, width: 552, height: 46, rx: 8, fill: C.amberSoft }, zg); ikon(zg, 'calendar', d5.left + 12, y, 26, C.amberDeep); T(zg, d5.left + 40, y + 8, [{ de: 'MFA Cloud-Konsole', en: 'MFA cloud console' }, { de: 'Wiederherstellungstest', en: 'Restore test' }, { de: 'Notfallplan', en: 'Emergency plan' }][i], { size: 22, weight: 800, fill: C.amberDeep }); T(zg, d5.right, y + 8, { de: 'bis …', en: 'by …' }, { mono: 1, size: 18, fill: C.amberDeep, anchor: 'end' }); return zg; });
    linien(d5.g, d5.left, d5.y + 370, 480, 4, 30, C.pBar, 10);
    // Abgleich: 18 Fragen, 10 Bereiche, Abschnitte der Selbstauskunft
    this.abg = g(k3);
    karte(this.abg, 840, 230, 990, 610, { fill: C.surface });
    T(this.abg, 880, 280, { de: 'ABGLEICHSTABELLE', en: 'MAPPING TABLE' }, { mono: 1, size: 20, fill: C.blue, ls: '0.1em' });
    T(this.abg, 960, 330, { de: '18 Fragen', en: '18 questions' }, { size: 28, weight: 800, anchor: 'middle' });
    T(this.abg, 1330, 330, { de: '10 Bereiche', en: '10 areas' }, { size: 28, weight: 800, anchor: 'middle' });
    T(this.abg, 1700, 330, { de: 'Abschnitte D1', en: 'D1 sections' }, { size: 28, weight: 800, anchor: 'middle' });
    this.fragen = Array.from({ length: 18 }, (_, i) => { const x = 920 + (i % 2) * 80, y = 380 + Math.floor(i / 2) * 50; const gr = g(this.abg); el('rect', { x: x - 30, y: y - 18, width: 60, height: 36, rx: 8, fill: C.raised, stroke: C.line, 'stroke-width': 2 }, gr); T(gr, x, y + 7, 'F' + (i + 1), { mono: 1, size: 16, fill: C.muted, anchor: 'middle' }); return { g: gr, x, y }; });
    this.bereiche = 'abcdefghij'.split('').map((ch, i) => { const x = 1330, y = 380 + i * 45; const gr = g(this.abg); el('rect', { x: x - 24, y: y - 18, width: 48, height: 36, rx: 8, fill: C.raised, stroke: C.blue, 'stroke-width': 2 }, gr); T(gr, x, y + 8, ch, { mono: 1, size: 20, fill: C.ink, anchor: 'middle' }); return { g: gr, x, y }; });
    this.abschn = Array.from({ length: 9 }, (_, i) => { const x = 1700, y = 380 + i * 50; const gr = g(this.abg); el('rect', { x: x - 26, y: y - 20, width: 52, height: 40, rx: 6, fill: C.blueSoft, stroke: C.blueBar, 'stroke-width': 2 }, gr); T(gr, x, y + 8, String(i + 1), { mono: 1, size: 20, fill: C.blueDeep, anchor: 'middle' }); return { g: gr, x, y }; });
    this.vLinien = this.fragen.map((f, i) => { const z = this.abschn[(i * 5) % 9]; return el('path', { d: `M ${f.x + 32} ${f.y} C ${f.x + 300} ${f.y} ${z.x - 300} ${z.y} ${z.x - 28} ${z.y}`, fill: 'none', stroke: C.blue, 'stroke-width': 2, opacity: 0.55 }, this.abg); });
    this.bLinien = this.bereiche.map((b, i) => { const z = this.abschn[(i * 4 + 1) % 9]; return el('path', { d: `M ${b.x + 26} ${b.y} C ${b.x + 150} ${b.y} ${z.x - 150} ${z.y} ${z.x - 28} ${z.y}`, fill: 'none', stroke: C.purple, 'stroke-width': 2, opacity: 0.6 }, this.abg); });
    [...this.fragen, ...this.bereiche, ...this.abschn].forEach((x) => this.abg.appendChild(x.g)); // Kästchen über den Linien
    shot(b3, this.tAS - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 4: D4 Nachweisliste, ein datiertes Bild ----------
    const b4 = buehne('beispiel-d4', { seed: 89, regalDeckkraft: 0.5 }); this.b4 = b4;
    const k4 = b4.cam;
    this.d4 = g(k4);
    const d4 = blatt(this.d4, { w: 760, h: 560, kicker: { de: 'D4 · NACHWEISLISTE', en: 'D4 · EVIDENCE LIST' }, kSize: 14, pad: 34 });
    const KOPF = [{ de: 'FRAGE', en: 'QUESTION' }, { de: 'BELEG', en: 'EVIDENCE' }, { de: 'ANLAGE · TERMIN', en: 'ATTACHMENT · DATE' }];
    [0, 120, 470].forEach((dx, i) => T(d4.g, d4.left + dx, d4.y + 12, KOPF[i], { mono: 1, size: 15, fill: C.pMuted, ls: '0.08em' }));
    const ZL = [[2, { de: 'MFA E-Mail · Bildschirmfoto', en: 'MFA email · screenshot' }, 1], [5, { de: 'Kontenliste', en: 'Account list' }, 2], [9, { de: 'Sicherung · Einstellung', en: 'Backup · settings' }, 3],
      [14, { de: 'Wiederherstellungstest', en: 'Restore test' }, null], [21, { de: 'Notfallkarte', en: 'Emergency card' }, null], [7, { de: 'MFA Cloud-Konsole', en: 'MFA cloud console' }, null]];
    this.d4Z = ZL.map(([fr, txt, anl], i) => {
      const y = d4.y + 62 + i * 62, zg = g(d4.g);
      const bg0 = el('rect', { x: d4.left - 10, y: y - 28, width: 760 - 2 * d4.pad + 20, height: 52, rx: 8, fill: anl ? 'none' : C.amberSoft, stroke: anl ? 'none' : C.amberLine, 'stroke-width': 2, 'stroke-dasharray': '8 6' }, zg);
      T(zg, d4.left, y + 7, 'F' + fr, { mono: 1, size: 20, fill: C.pMuted });
      T(zg, d4.left + 120, y + 7, txt, { size: 22, weight: 700, fill: C.pInk });
      if (anl) { const a = g(zg); el('rect', { x: d4.left + 466, y: y - 18, width: 140, height: 36, rx: 6, fill: C.blueSoft, stroke: C.blue, 'stroke-width': 2 }, a); T(a, d4.left + 536, y + 7, { de: 'Anlage ' + anl, en: 'Att. ' + anl }, { size: 18, weight: 800, fill: C.blueDeep, anchor: 'middle' }); }
      else { ikon(zg, 'calendar', d4.left + 484, y - 2, 26, C.amberDeep); T(zg, d4.left + 506, y + 7, { de: 'Termin · Satz', en: 'date · sentence' }, { size: 18, weight: 700, fill: C.amberDeep }); }
      return { g: zg, bg0, offen: !anl };
    });
    this.d4Kunde = kundeHaus(k4, 1640, 820, 0.55, { label: null });
    this.d4KundeL = T(k4, 1640, 866, { de: 'KUNDE', en: 'CUSTOMER' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.d4Stempel = stempel(k4, { de: 'DATIERT', en: 'DATED' }, C.blueDeep, 30);
    this.verspP = pille(k4, { de: 'ein datiertes Bild, kein Versprechen', en: 'a dated picture, not a promise' }, { icon: 'calendar', col: C.blue, size: 26 });
    this.offenP = pille(k4, { de: 'aufgeführt, nicht versteckt', en: 'listed, not hidden' }, { icon: 'list', col: C.amber, gestrichelt: true, size: 26 });
    shot(b4, this.tQ8 - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [b1, b2, b3, b4];

    // ---------- Einblendungen ----------
    kopf(this.tQ5, this.tMisch - 0.3, K, { de: 'Muster Elektrotechnik e.U.', en: 'Example Electrical Ltd' });
    kopf(this.tMisch, this.tQ6 - 0.3, K, { de: 'Ein ehrliches Mischbild', en: 'An honest mixed picture' });
    kopf(this.tQ6, this.tAS - 0.3, K, { de: 'D1 Selbstauskunft', en: 'D1 Self-declaration' });
    kopf(this.tAS, this.tQ8 - 0.3, K, { de: 'D5 Antwortschreiben', en: 'D5 Cover letter' });
    kopf(this.tQ8, this.tEnde - 0.3, K, { de: 'D4 Nachweisliste', en: 'D4 Evidence list' });
  },

  zeichnen(t) {
    // ---------- Bühne 1 ----------
    if (this.b1.vis) {
      const B = this.B;
      const shots = [{ t: this.tFB - 0.6, d: 1.4, f: [1500, 560], z: 0.8 }];
      this.tR.forEach((tt, i) => shots.push({ t: tt - 0.5, d: 1.1, f: this.blicke[i].f, z: this.blicke[i].z }));
      const k = fahrt(t, { f: [1680, 470], z: 0.56 }, shots);
      kamera(this.b1, k.f, k.z);
      B.monitore.forEach((m, i) => bildschirm(m, 0.5)); bildschirm(B.monL, 0.3);
      betriebLeben(B, t, { tippen: { figA: [this.tQ5, 99], figB: [this.tQ5 + 0.4, 99] } }); stelle(B.figM1, 2670, 852, 1);
      tr(this.stempel, 1680, 140, Math.max(0.01, P(t, this.tErf, 0.4, E.back)), -4); O(this.stempel, Math.min(P(t, this.tErf, 0.2), 1 - P(t, this.tFB - 0.6, 0.5)));
      tr(this.beschP, 1680, 960, Math.max(0.01, P(t, this.tBesch - 0.4, 0.45, E.back))); O(this.beschP, Math.min(P(t, this.tBesch - 0.4, 0.2), 1 - P(t, this.tFB - 0.6, 0.5)));
      tr(this.echtP, 1680, 1060, Math.max(0.01, P(t, this.tKeine, 0.45, E.back))); O(this.echtP, Math.min(P(t, this.tKeine, 0.2), 1 - P(t, this.tFB - 0.6, 0.5)));
      const fk = P(t, this.tFB - 0.4, 1.3, E.io); const p = bogen([-200, 160], [1150, 690], fk, 160);
      tr(this.umschlag, p[0], p[1], 1, lerp(-14, 0, fk)); O(this.umschlag, Math.min(P(t, this.tFB - 0.4, 0.2), 1 - P(t, this.tFB + 1.4, 0.4)));
      // die sechs Antworten: Ring am Ort im Haus, Zeile in der Liste
      const lk = P(t, this.tMisch - 0.2, 0.6, E.out); O(this.liste, lk); tr(this.liste, (1 - lk) * 40, 0);
      this.zeilen.forEach((z, i) => { const t0 = this.tR[i] - 0.1; O(z.g, P(t, t0, 0.3)); if (z.p) { const kk = P(t, t0 + 0.6, 0.4, E.back); z.p.firstChild.setAttribute('transform', `scale(${Math.max(0.01, kk).toFixed(3)})`); } });
      const farbe = [C.green, C.amber, C.amber, C.amber, C.amber, C.muted];
      this.ringe.forEach((r, i) => { const t0 = this.tR[i] + 0.1, nxt = i < 5 ? this.tR[i + 1] - 0.3 : this.tQ6; r.setAttribute('cx', this.ziele[i][0]); r.setAttribute('cy', this.ziele[i][1]); r.setAttribute('stroke', farbe[i]); r.setAttribute('stroke-dasharray', i === 0 ? '' : '16 10'); O(r, fenster(t, t0, 0.3, nxt, 0.3)); r.setAttribute('r', (110 + 6 * Math.sin(t * 3)).toFixed(1)); });
      O(this.notfall, P(t, this.tR[4] - 0.2, 0.4)); this.notfall.firstChild.setAttribute('stroke-dashoffset', (-t * 14).toFixed(1));
    }
    // ---------- Bühne 2 ----------
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      const dk = P(t, this.tQ6, 0.7, E.out); tr(this.d1, 640, 560 + (1 - dk) * 24, 1, -1); O(this.d1, dk);
      this.reiter.forEach((r, i) => O(r, P(t, this.tNeun + i * 0.1, 0.25)));
      this.tabelle.forEach((z, i) => { O(z.g, 0.25 + 0.75 * P(t, this.tTab + i * 0.12, 0.3)); O(z.st, P(t, this.tStand + i * 0.12, 0.3)); O(z.dat, P(t, this.tStand + 0.4 + i * 0.12, 0.3)); });
      zeichne(this.d1Sig, P(t, this.tUnter - 0.1, 0.9)); zeichne(this.d1SigRing, P(t, this.tUnter, 0.6)); O(this.d1SigRing, 1 - P(t, this.tOrd - 0.3, 0.4));
      tr(this.ordnungP, 1400, 330, Math.max(0.01, P(t, this.tOrd - 0.2, 0.45, E.back))); O(this.ordnungP, P(t, this.tOrd - 0.2, 0.2)); zeichne(this.ordnungS, P(t, this.tOrd + 0.4, 0.4));
      [this.tHeute, this.tTeilw, this.tHat].forEach((tt, i) => { const p = this.d1Lampen[i]; tr(p, 1400, 480 + i * 100, Math.max(0.01, P(t, tt - 0.2, 0.45, E.back))); O(p, P(t, tt - 0.2, 0.2)); });
    }
    // ---------- Bühne 3 ----------
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      const ab = P(t, this.tQ7 - 0.3, 0.8, E.io);
      const dk = P(t, this.tAS, 0.7, E.out); tr(this.d5, lerp(960, 480, ab), 560 + (1 - dk) * 24, lerp(1, 0.86, ab), lerp(1, -1.5, ab)); O(this.d5, dk);
      O(this.d5Abs, 0.2 + 0.8 * P(t, this.tKlein - 0.2, 0.4));
      this.d5L.forEach((z, i) => O(z, 0.15 + 0.85 * P(t, this.tLuecken + i * 0.25, 0.35)));
      O(this.abg, ab); tr(this.abg, (1 - ab) * 60, 0);
      this.fragen.forEach((f, i) => O(f.g, P(t, this.tTyp - 0.3 + i * 0.05, 0.25)));
      this.bereiche.forEach((b, i) => O(b.g, P(t, this.tZehn - 0.2 + i * 0.06, 0.25)));
      this.abschn.forEach((a, i) => O(a.g, P(t, this.tZehn + 0.3 + i * 0.05, 0.25)));
      this.vLinien.forEach((l, i) => zeichne(l, P(t, this.tVerw - 0.4 + i * 0.04, 0.6)));
      this.bLinien.forEach((l, i) => zeichne(l, P(t, this.tVerw - 0.2 + i * 0.05, 0.6)));
    }
    // ---------- Bühne 4 ----------
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      const zum = P(t, this.tBild - 0.3, 1.1, E.io);
      const dk = P(t, this.tQ8, 0.7, E.out); tr(this.d4, lerp(760, 1180, zum), lerp(540, 480, zum) + (1 - dk) * 24, lerp(1, 0.55, zum), lerp(-1, 2, zum)); O(this.d4, dk);
      this.d4Z.forEach((z, i) => { const t0 = z.offen ? (i === 3 ? this.tNichtV : this.tOffen + (i - 4) * 0.3) : this.tVorliegt + i * 0.25; O(z.g, 0.2 + 0.8 * P(t, t0 - 0.1, 0.35)); if (z.offen) z.bg0.setAttribute('stroke-width', t > this.tOffen ? 3.5 : 2); });
      tr(this.offenP, 760, 880, Math.max(0.01, P(t, this.tVersteckt - 0.2, 0.45, E.back))); O(this.offenP, Math.min(P(t, this.tVersteckt - 0.2, 0.2), 1 - zum));
      O(this.d4Kunde.g, zum); O(this.d4KundeL, zum);
      tr(this.d4Stempel, 1180, 640, Math.max(0.01, P(t, this.tBild + 0.6, 0.4, E.back)), -6); O(this.d4Stempel, P(t, this.tBild + 0.6, 0.2));
      tr(this.verspP, 800, 820, Math.max(0.01, P(t, this.tVersp, 0.45, E.back))); O(this.verspP, P(t, this.tVersp, 0.2));
    }
  },
});
