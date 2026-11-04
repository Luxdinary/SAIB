// Teil 3b · Fünf Schritte, Schritt 3 bis 5 (Absätze 12 bis 15).
// Bühnen: Weg (Rückkehr nach jedem Schritt) → Größe (Verhältnismäßigkeit, Fakt und Auslegung) → Nachweise (neun Belege, Nachweisordner)
// → Senden (Selbstauskunft, Anlagen, Antwortschreiben, eingefrorene Fassung).
akt({
  name: 'loesung-2',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    // ---------- Wortanker ----------
    const F3 = belegt(); this.tS3 = F3.s;
    this.tGroesse = c('Größe der Einrichtung', 'size of the entity');
    this.tRisiko = c('Risikoexposition', 'exposure to risk');
    this.tDVO = c('Durchführungsverordnung wiederholt', 'Implementing Regulation repeats');
    this.tDok = c('dokumentieren, warum', 'document why');
    this.tNichtAng = c('nicht angemessen', 'not appropriate');
    const A3 = belegt(); this.tA3 = A3.s;
    this.tFuer = c('für Ihren Kunden', 'written for your customer');
    this.tMehr = c('mehr zu verlangen', 'asking more of you');
    this.tGrund = c('guten Grund', 'good reason');
    this.tMessen = c('an Ihrer Größe', 'measured by your size');
    this.tErster = c('im ersten Absatz', 'first paragraph');
    this.tNichts = c('Nichts in unserem Toolkit', 'Nothing in our toolkit');
    this.tX = [c('Security Operations Center', 'security operations centre|security operations center'), c('Penetrationstests', 'penetration tests'), c('Zertifizierung', 'certification')];
    const Q4 = quelle(); this.tS4 = Q4.s;
    this.tVorOrt = c('Prüfung vor Ort', 'on-site audit');
    this.tSelten = c('selten', 'is rare');
    this.tDatiert = c('datiertes Dokument', 'dated document');
    this.tGibt = c('gibt es schon', 'exist already');
    this.tStunde = c('in einer Stunde', 'an hour or less');
    this.tB = [c('Die Kontenliste', 'The account list'), c('Bildschirmfotos der', 'Screenshots of the'), c('Die schriftlichen Regeln', 'The written rules'), c('Die Sicherungseinstellungen', 'The backup settings'),
      c('Der Wiederherstellungstest', 'The restore test'), c('Die Notfallkarte', 'The emergency card'), c('Die Update-Prüfung|Die Update Prüfung|Die Updateprüfung', 'The update check'), c('Das Vorfallsprotokoll', 'The incident log'), c('Die Teilnehmerliste', 'The attendance list')];
    this.tNichtZ = c('nicht zeigen können', 'cannot show');
    this.tMitT = c('mit dem Termin', 'with the date');
    this.tSagt = c('Antwortschreiben sagt es', 'cover letter says so');
    this.tS5 = c('Schritt fünf', 'Step five');
    this.tSelbst = c('als Selbstauskunft', 'as a self-declaration');
    this.tForm = c('ausgefülltes Formular', 'filled-in form');
    this.tStand = c('mit Stand und Datum', 'status and date');
    this.tUnter = c('unterschrieben', 'signed by');
    this.tAnl = c('als Anlagen', 'as attachments');
    this.tAS = c('ein Antwortschreiben', 'a cover letter');
    this.tLuecken = c('Lücken mit ihren Terminen', 'gaps with their dates');
    this.tZuord = c('Ihren Abschnitten', 'to your sections');
    this.tFrier = c('einfrieren', 'freeze');
    this.tUeberpr = c('wann Sie sie überprüfen', 'when you will review');
    this.tEnde = cue({ de: 'Jetzt die Quellen', en: 'Now the sources' }, { halten: true }).s;

    // ---------- Bühne W2: der Weg, Rückkehr nach jedem Schritt ----------
    const bW = buehne('loesung-weg-2', { seed: 29, regalDeckkraft: 0.6 }); this.bW = bW;
    this.Wg = bauWeg5(bW.cam);
    shot(bW, this.tS3 - 1.1, { typ: 'kreisRaus', d: 1.0, p: weg5Punkt(1) });

    // ---------- Bühne G: Größe ----------
    const bG = buehne('loesung-groesse', { seed: 41, regalDeckkraft: 0.5 }); this.bG = bG;
    const gc = bG.cam;
    this.grossH = kundeHaus(gc, 330, 770, 0.72, { label: null });
    this.kleinH = kleinHaus(gc, 860, 770, 0.8, { label: null });
    this.grossLab = T(gc, 330, 818, { de: 'GROSSE EINRICHTUNG', en: 'LARGE ENTITY' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.kleinLab = T(gc, 860, 818, { de: 'KLEINER BETRIEB', en: 'SMALL BUSINESS' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    const stapel = (x, n, col) => Array.from({ length: n }, (_, i) => { const gr = g(gc, { transform: `translate(${x} ${760 - i * 44})` }); el('rect', { x: -48, y: -38, width: 96, height: 38, rx: 7, fill: col === C.blue ? '#1d3766' : 'rgba(255,209,102,0.08)', stroke: col, 'stroke-width': 3, 'stroke-dasharray': col === C.blue ? '' : '8 6' }, gr); return gr; });
    this.stGross = stapel(560, 9, C.blue);
    this.stKlein = stapel(1010, 3, C.blue);
    this.stForder = stapel(0, 7, C.amber); // Forderung des Kunden, wandert zum kleinen Betrieb
    this.massP = [pille(gc, { de: 'Größe', en: 'Size' }, { icon: 'building', col: C.blue, size: 26 }), pille(gc, { de: 'Risikoexposition', en: 'Exposure to risk' }, { icon: 'warn', col: C.blue, size: 26 })];
    this.begr = g(gc);
    const bg0 = blatt(this.begr, { w: 520, h: 400, kicker: { de: 'BEGRÜNDUNG · DVO 2024/2690', en: 'REASONING · IR 2024/2690' }, kSize: 14, pad: 32 });
    T(bg0.g, bg0.left, bg0.y + 30, { de: 'Anforderung:', en: 'Requirement:' }, { size: 26, weight: 800, fill: C.pInk });
    this.begrZ = linien(bg0.g, bg0.left, bg0.y + 60, 400, 4, 34, C.pBar2, 11);
    this.begrStempel = stempel(bg0.g, { de: 'NICHT ANGEMESSEN, WEIL …', en: 'NOT APPROPRIATE, BECAUSE …' }, C.blueDeep, 20); tr(this.begrStempel, 0, 140, 1, -3);
    this.stift = g(gc); iconPen(this.stift, 64, C.ink);
    this.verhP = pille(gc, { de: 'Verhältnismäßigkeit: für den Kunden', en: 'Proportionality: for the customer' }, { marke: 'auslegung', col: C.purple, size: 24 });
    this.messP = pille(gc, { de: 'an Ihrer Größe messen', en: 'measured by your size' }, { icon: 'check', col: C.blue, size: 24 });
    this.brief = g(gc);
    const br = blatt(this.brief, { w: 520, h: 440, kicker: { de: 'ANTWORTSCHREIBEN', en: 'COVER LETTER' }, kSize: 14, pad: 32 });
    this.briefHl = el('rect', { x: br.left - 12, y: br.y + 4, width: 520 - 2 * br.pad + 24, height: 132, rx: 10, fill: C.blueSoft }, br.g);
    T(br.g, br.left, br.y + 36, { de: 'Erster Absatz', en: 'First paragraph' }, { size: 26, weight: 800, fill: C.blueDeep });
    linien(br.g, br.left, br.y + 62, 420, 3, 26, C.blueBar, 10); linien(br.g, br.left, br.y + 170, 420, 6, 30, C.pBar, 10);
    this.ohne = [{ de: 'Security Operations Center', en: 'Security operations centre' }, { de: 'Penetrationstests', en: 'Penetration tests' }, { de: 'Zertifizierung', en: 'Certification' }]
      .map((w0) => { const gr = g(gc); const p = pille(gr, w0, { col: C.muted, size: 24, gestrichelt: true }); const s = streich(gr, p.w, C.red); return { g: gr, s, w: p.w }; });
    shot(bG, this.tS3 + 0.8, { typ: 'kreis', d: 1.3, p: weg5Punkt(2) });
    shot(bW, this.tS4 - 1.1, { typ: 'kreisRaus', d: 1.0, p: weg5Punkt(2) });

    // ---------- Bühne N: Nachweise ----------
    const bN = buehne('loesung-nachweise', { seed: 43, regalDeckkraft: 0.5 }); this.bN = bN;
    const nc = bN.cam;
    this.nHaus = kleinHaus(nc, 1120, 800, 0.9, { label: null });
    this.pruefer = stehend(nc, 300, 852, { jacke: '#4a5470', haar: 'bun', blatt: true, kragen: '#cfd6e3', skala: 0.95 });
    this.selten = pille(nc, { de: 'selten', en: 'rare' }, { icon: 'clock', col: C.muted, gestrichelt: true, size: 26 });
    const BELEGE = [['list', { de: 'Kontenliste', en: 'Account list' }, { de: 'eine Tabelle', en: 'one table' }], ['id', { de: 'MFA-Bildschirmfotos', en: 'MFA screenshots' }, { de: 'eines je System', en: 'one per system' }],
      ['pen', { de: 'Schriftliche Regeln', en: 'Written rules' }, { de: 'zwei Seiten, unterschrieben', en: 'two pages, signed' }], ['folder', { de: 'Sicherung und Kopie', en: 'Backup and copy' }, { de: 'ein Foto, ein Satz', en: 'one screenshot, one sentence' }],
      ['cycle', { de: 'Wiederherstellungstest', en: 'Restore test' }, { de: 'Datum, Dauer, Ergebnis', en: 'date, duration, result' }], ['warn', { de: 'Notfallkarte', en: 'Emergency card' }, { de: 'gedruckt, datiert, ausgehängt', en: 'printed, dated, posted' }],
      ['calendar', { de: 'Update-Prüfung', en: 'Update check' }, { de: 'eine Zeile im Monat', en: 'one line per month' }], ['doc', { de: 'Vorfallsprotokoll', en: 'Incident log' }, { de: 'eine Seite, angelegt', en: 'one page, started' }], ['group', { de: 'Teilnehmerliste', en: 'Attendance list' }, { de: 'Datum, Themen, Namen', en: 'date, topics, names' }]];
    this.belege = BELEGE.map(([ic, name, det], i) => {
      const gr = g(nc); const w = 340, h = 100;
      el('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: 8, fill: C.paper, filter: 'url(#shadowS)' }, gr);
      ikon(gr, ic, -w / 2 + 38, 0, 38, C.blueDeep);
      T(gr, -w / 2 + 72, -6, name, { size: 24, weight: 800, fill: C.pInk });
      T(gr, -w / 2 + 72, 26, det, { mono: 1, size: 17, fill: C.pMuted });
      const x = 300 + (i % 3) * 370, y = 330 + Math.floor(i / 3) * 128;
      return { g: gr, x, y };
    });
    this.offen = belegKarte(nc, 'cycle', { de: 'Wiederherstellungstest · Termin', en: 'Restore test · date' }, { offen: true, w: 340, h: 100, size: 24 });
    this.ordner = nachweisOrdner(nc, { w: 380, h: 270 });
    this.ordnerP = pille(nc, { de: 'je Antwort ein datiertes Dokument', en: 'one dated document per answer' }, { icon: 'calendar', col: C.blue, size: 24 });
    this.stundeP = pille(nc, { de: 'eine Stunde oder weniger', en: 'an hour or less' }, { icon: 'clock', col: C.blue, size: 24 });
    this.kopien = this.belege.map(() => { const gr = g(nc); el('rect', { x: -22, y: -28, width: 44, height: 56, rx: 4, fill: C.paper }, gr); return gr; });
    this.nListe = g(nc);
    const nl = blatt(this.nListe, { w: 420, h: 220, kicker: { de: 'NACHWEISLISTE', en: 'EVIDENCE LIST' }, kSize: 14, pad: 28, back: false });
    linien(nl.g, nl.left, nl.y + 8, 300, 3, 30, C.pBar, 10);
    this.nListeT = terminPille(this.nListe, { de: 'Termin aus dem Maßnahmenplan', en: 'date from the action plan' }, 20); tr(this.nListeT, 0, 72);
    this.asP = pille(nc, { de: 'Antwortschreiben sagt es', en: 'the cover letter says so' }, { icon: 'mail', col: C.blue, size: 22 });
    shot(bN, this.tS4 + 0.7, { typ: 'kreis', d: 1.2, p: weg5Punkt(3) });
    shot(bW, this.tS5 - 1.1, { typ: 'kreisRaus', d: 1.0, p: weg5Punkt(3) });

    // ---------- Bühne S: Senden ----------
    const bS = buehne('loesung-senden', { seed: 47, regalDeckkraft: 0.5 }); this.bS = bS;
    const sc = bS.cam;
    this.formGeist = g(sc);
    { const fg = blatt(this.formGeist, { w: 300, h: 380, kicker: { de: 'FORMULAR', en: 'FORM' }, kSize: 13, pad: 24, back: false, schatten: false }); linien(fg.g, fg.left, fg.y + 10, 240, 8, 30, C.pBar, 10); }
    this.formStrich = el('path', { d: 'M -170 -190 L 170 190', stroke: C.red, 'stroke-width': 7, 'stroke-linecap': 'round' }, this.formGeist);
    this.sa = g(sc);
    const sa = blatt(this.sa, { w: 480, h: 600, kicker: { de: 'SELBSTAUSKUNFT', en: 'SELF-DECLARATION' }, kSize: 15, pad: 34 });
    this.saZeilen = [['vorhanden', C.green], ['termin', C.amber], ['teilweise', C.amber], ['termin', C.amber], ['vorhanden', C.green]].map(([art, col], i) => {
      const y = sa.y + 30 + i * 62, zg = g(sa.g);
      const lamp = el('circle', { cx: sa.left + 14, cy: y, r: 13, fill: art === 'termin' ? 'none' : col, stroke: col, 'stroke-width': 3.5, 'stroke-dasharray': art === 'termin' ? '6 4' : '' }, zg);
      el('rect', { x: sa.left + 42, y: y - 6, width: 170 + ((i * 41) % 60), height: 12, rx: 6, fill: C.pBar }, zg);
      const dat = T(zg, sa.right, y + 7, { de: 'Stand · Datum', en: 'status · date' }, { mono: 1, size: 15, fill: C.pMuted, anchor: 'end' });
      return { g: zg, dat };
    });
    el('rect', { x: sa.left, y: sa.y0 + 600 - 96, width: 220, height: 2, fill: C.pMuted }, sa.g);
    T(sa.g, sa.left, sa.y0 + 600 - 70, { de: 'Unterschrift der Leitung', en: 'Signed by the management' }, { mono: 1, size: 14, fill: C.pMuted });
    this.unterschrift = el('path', { d: `M ${sa.left + 8} ${sa.y0 + 600 - 104} c 14 -26 22 -26 26 -2 c 4 20 12 -30 26 -20 c 12 8 4 22 18 10 c 16 -14 26 -8 40 -4 c 12 4 26 -10 44 -6`, fill: 'none', stroke: C.blueDeep, 'stroke-width': 3.5, 'stroke-linecap': 'round' }, sa.g);
    this.anlagen = [1, 2, 3].map((n) => { const gr = g(sc); el('rect', { x: -88, y: -30, width: 176, height: 60, rx: 6, fill: C.paper, stroke: C.blueBar, 'stroke-width': 2 }, gr); T(gr, 0, 9, { de: 'Anlage ' + n, en: 'Attachment ' + n }, { size: 19, weight: 800, fill: C.blueDeep, anchor: 'middle' }); return gr; });
    this.as = g(sc);
    const as = blatt(this.as, { w: 540, h: 520, kicker: { de: 'ANTWORTSCHREIBEN', en: 'COVER LETTER' }, kSize: 15, pad: 34 });
    linien(as.g, as.left, as.y + 8, 440, 2, 26, C.pBar, 10);
    this.asLuecken = [0, 1].map((i) => { const zg = g(as.g); const y = as.y + 74 + i * 52; el('rect', { x: as.left - 10, y: y - 22, width: 492, height: 42, rx: 8, fill: C.amberSoft }, zg); ikon(zg, 'calendar', as.left + 12, y - 1, 24, C.amberDeep); el('rect', { x: as.left + 36, y: y - 6, width: 240 - i * 40, height: 11, rx: 5.5, fill: '#f0d9a0' }, zg); T(zg, as.right, y + 6, { de: 'bis …', en: 'by …' }, { mono: 1, size: 16, fill: C.amberDeep, anchor: 'end' }); return zg; });
    T(as.g, as.left, as.y + 210, { de: 'ZUORDNUNG', en: 'MAPPING' }, { mono: 1, size: 15, fill: C.pMuted, ls: '0.08em' });
    this.zuord = [0, 1, 2].map((i) => { const zg = g(as.g); const y = as.y + 250 + i * 50; T(zg, as.left, y + 6, { de: 'Frage ' + [3, 9, 14][i], en: 'Question ' + [3, 9, 14][i] }, { size: 20, weight: 700, fill: C.pInk }); const pf = el('path', { d: `M ${as.left + 140} ${y} H ${as.left + 300}`, stroke: C.blueDeep, 'stroke-width': 3, 'marker-end': '' }, zg); T(zg, as.left + 316, y + 6, { de: 'Abschnitt ' + [2, 5, 7][i], en: 'Section ' + [2, 5, 7][i] }, { size: 20, weight: 800, fill: C.blueDeep }); return { g: zg, pf }; });
    this.sOrdner = nachweisOrdner(sc, { w: 300, h: 210 });
    this.paket = g(sc); el('rect', { x: -60, y: -76, width: 120, height: 152, rx: 6, fill: C.paper, filter: 'url(#shadowS)' }, this.paket); linien(this.paket, -44, -52, 88, 5, 20, C.pBar2, 8);
    this.frierP = stempel(this.paket, { de: 'DATIERT', en: 'DATED' }, C.blueDeep, 16); tr(this.frierP, 0, 40, 1, -6);
    this.pruefP = pille(sc, { de: 'Überprüfung', en: 'Review' }, { icon: 'calendar', col: C.blue, size: 24 });
    shot(bS, this.tS5 + 0.7, { typ: 'kreis', d: 1.2, p: weg5Punkt(4) });
    this.buehnen = [bW, bG, bN, bS];

    // ---------- Einblendungen ----------
    const K = { de: '2 · FÜNF SCHRITTE', en: '2 · FIVE STEPS' };
    kopf(this.tS3 - 1.0, this.tS3 + 0.6, K, { de: 'Was der Betrieb tut', en: 'What the business does' });
    kopf(this.tS3 + 0.8, this.tA3 - 0.3, { de: 'SCHRITT 3', en: 'STEP 3' }, { de: 'An der eigenen Größe messen', en: 'Measure by your size' });
    kopf(this.tA3, this.tS4 - 1.2, { de: 'SCHRITT 3', en: 'STEP 3' }, { de: 'Was Sie daraus machen', en: 'What you make of it' });
    kopf(this.tS4 - 1.0, this.tS4 + 0.5, K, { de: 'Was der Betrieb tut', en: 'What the business does' });
    kopf(this.tS4 + 0.7, this.tS5 - 1.2, { de: 'SCHRITT 4', en: 'STEP 4' }, { de: 'Nachweise', en: 'Evidence' });
    kopf(this.tS5 - 1.0, this.tS5 + 0.5, K, { de: 'Was der Betrieb tut', en: 'What the business does' });
    kopf(this.tS5 + 0.7, this.tEnde - 0.3, { de: 'SCHRITT 5', en: 'STEP 5' }, { de: 'Als Selbstauskunft senden', en: 'Send a self-declaration' });
  },

  zeichnen(t) {
    // ---------- Bühne W2 ----------
    if (this.bW.vis) {
      kamera(this.bW, WEG5_BLICK.f, WEG5_BLICK.z);
      const schritt = t < this.tS4 - 1.5 ? 2 : t < this.tS5 - 1.5 ? 3 : 4;
      const t0 = [0, 0, this.tS3, this.tS4, this.tS5][schritt];
      weg5Zeichnen(this.Wg, t, { aktiv: schritt, aktivK: P(t, t0 - 0.25, 0.4), erledigt: schritt });
      this.Wg.nodes.forEach((n, i) => O(n.glow, i === schritt ? 0.9 * P(t, t0 - 0.25, 0.4) : 0));
    }
    // ---------- Bühne G ----------
    if (this.bG.vis) {
      kamera(this.bG, [960, 540], 1);
      const gi = P(t, Math.min(this.tS3 + 1.2, this.tGroesse - 0.3), 0.6, E.out);
      O(this.grossH.g, gi); O(this.kleinH.g, gi); O(this.grossLab, gi); O(this.kleinLab, gi);
      this.stGross.forEach((s, i) => { const k = P(t, this.tGroesse + 0.2 + i * 0.08, 0.3, E.back); sk(s, 0, 0, 1); s.setAttribute('transform', `translate(560 ${760 - i * 44}) scale(${Math.max(0.01, k).toFixed(3)})`); O(s, P(t, this.tGroesse + 0.2 + i * 0.08, 0.15)); });
      this.stKlein.forEach((s, i) => { const k = P(t, this.tGroesse + 0.4 + i * 0.08, 0.3, E.back); s.setAttribute('transform', `translate(1010 ${760 - i * 44}) scale(${Math.max(0.01, k).toFixed(3)})`); O(s, P(t, this.tGroesse + 0.4 + i * 0.08, 0.15)); });
      tr(this.massP[0], 800, 260, Math.max(0.01, P(t, this.tGroesse, 0.45, E.back))); O(this.massP[0], Math.min(P(t, this.tGroesse, 0.2), 1 - P(t, this.tA3 - 0.3, 0.4)));
      tr(this.massP[1], 800, 330, Math.max(0.01, P(t, this.tRisiko, 0.45, E.back))); O(this.massP[1], Math.min(P(t, this.tRisiko, 0.2), 1 - P(t, this.tA3 - 0.3, 0.4)));
      // Begründung: die DVO lässt dokumentieren, warum etwas nicht angemessen ist
      const bk = P(t, this.tDVO - 0.2, 0.7, E.out), bAus = P(t, this.tErster - 0.4, 0.5);
      tr(this.begr, lerp(1600, 1480, bk), 560 + (1 - bk) * 20, 1, lerp(4, 1.5, bk)); O(this.begr, Math.min(bk, 1 - bAus));
      this.begrZ.forEach((z, i) => O(z, P(t, this.tDok + i * 0.3, 0.3)));
      const sp = clamp((t - this.tDok) / 1.6); tr(this.stift, 1300 + sp * 300, 560 + Math.floor(sp * 4) * 34 + 6 * Math.sin(t * 25) * (sp > 0 && sp < 1 ? 1 : 0), 1); O(this.stift, fenster(t, this.tDok - 0.3, 0.3, this.tNichtAng + 0.8, 0.4));
      tr(this.begrStempel, 0, 140, Math.max(0.01, P(t, this.tNichtAng, 0.4, E.back)), -3); O(this.begrStempel, P(t, this.tNichtAng, 0.2));
      // Auslegung: für den Kunden geschrieben; mehr verlangen ist erlaubt; an Ihrer Größe messen
      tr(this.verhP, 400, 250, Math.max(0.01, P(t, this.tFuer, 0.45, E.back))); O(this.verhP, P(t, this.tFuer, 0.2));
      const fk = P(t, this.tMehr - 0.2, 1.4, E.io);
      this.stForder.forEach((s, i) => { const x = lerp(470, 1120, fk), y = 760 - i * 44; s.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)})`); O(s, P(t, this.tMehr - 0.2 + i * 0.05, 0.25) * (1 - 0.5 * P(t, this.tMessen, 0.5))); });
      tr(this.messP, 1010, 380, Math.max(0.01, P(t, this.tMessen, 0.45, E.back))); O(this.messP, P(t, this.tMessen, 0.2));
      this.stKlein.forEach((s) => s.firstChild.setAttribute('stroke-width', t > this.tMessen ? 5 : 3));
      const brk = P(t, this.tErster - 0.4, 0.7, E.out); tr(this.brief, lerp(1600, 1480, brk), 540 + (1 - brk) * 20, 1, lerp(3, 1, brk)); O(this.brief, brk);
      O(this.briefHl, P(t, this.tErster + 0.2, 0.4));
      this.ohne.forEach((o, i) => { const t0 = this.tX[i]; tr(o.g, 760 + i * 0 + [0, 380, 700][i], 900, 1); O(o.g, P(t, t0 - 0.1, 0.3)); zeichne(o.s, P(t, t0 + 0.3, 0.35)); });
    }
    // ---------- Bühne N ----------
    if (this.bN.vis) {
      kamera(this.bN, [960, 540], 1);
      const vor = fenster(t, this.tVorOrt - 0.3, 0.5, this.tGibt, 0.6);
      O(this.nHaus.g, vor);
      const gx = lerp(300, 820, P(t, this.tVorOrt - 0.3, 2.4, E.io)); stelle(this.pruefer, gx, 852, 0.95); gehen(this.pruefer, (t - this.tVorOrt) * 2.2, t < this.tVorOrt + 2.1 ? 1 : 0);
      O(this.pruefer.g, vor * (1 - 0.6 * P(t, this.tSelten, 0.5)));
      tr(this.selten, 820, 360, Math.max(0.01, P(t, this.tSelten, 0.45, E.back))); O(this.selten, Math.min(P(t, this.tSelten, 0.2), 1 - P(t, this.tGibt, 0.5)));
      const ok = P(t, this.tDatiert - 0.3, 0.6, E.out); tr(this.ordner.g, 1560, 470 + (1 - ok) * 30, 1); O(this.ordner.g, ok);
      tr(this.ordnerP, 1560, 660, Math.max(0.01, P(t, this.tDatiert + 0.2, 0.45, E.back))); O(this.ordnerP, Math.min(P(t, this.tDatiert + 0.2, 0.2), 1 - P(t, this.tB[0] - 0.2, 0.4)));
      tr(this.stundeP, 1560, 730, Math.max(0.01, P(t, this.tStunde, 0.45, E.back))); O(this.stundeP, Math.min(P(t, this.tStunde, 0.2), 1 - P(t, this.tB[0] - 0.2, 0.4)));
      const umk = P(t, this.tNichtZ - 0.1, 0.5);
      this.belege.forEach((b, i) => {
        const t0 = this.tB[i] - 0.15, k = P(t, t0, 0.45, E.back);
        tr(b.g, b.x, b.y, Math.max(0.01, k)); O(b.g, P(t, t0, 0.2) * (i === 4 ? 1 - umk : 1));
        // eine Kopie fliegt in den Ordner, das Original bleibt
        const ck = P(t, t0 + 0.5, 0.8, E.io); const cp = bogen([b.x, b.y], [1560, 450], ck, 120);
        tr(this.kopien[i], cp[0], cp[1], lerp(1, 0.6, ck), ck * 12); O(this.kopien[i], i === 4 ? 0 : Math.min(P(t, t0 + 0.5, 0.15), 1 - P(t, t0 + 1.2, 0.15)));
      });
      // was fehlt: Wiederherstellungstest wird zur offenen Karte mit Termin und wandert in die Nachweisliste
      const b4 = this.belege[4], wk = P(t, this.tMitT - 0.1, 0.9, E.io);
      tr(this.offen, lerp(b4.x, 1560, wk), lerp(b4.y, 700, wk), lerp(1, 0.9, wk)); O(this.offen, umk);
      const nl = P(t, this.tMitT - 0.3, 0.5, E.out); tr(this.nListe, 1560, 720 + (1 - nl) * 20, 1); O(this.nListe, nl);
      O(this.nListeT, P(t, this.tMitT + 0.6, 0.3));
      tr(this.asP, 1560, 880, Math.max(0.01, P(t, this.tSagt, 0.45, E.back))); O(this.asP, P(t, this.tSagt, 0.2));
    }
    // ---------- Bühne S ----------
    if (this.bS.vis) {
      kamera(this.bS, [960, 540], 1);
      const fg = P(t, this.tSelbst - 0.6, 0.5); tr(this.formGeist, 250, 560, 1, -4); O(this.formGeist, Math.min(fg, 1 - P(t, this.tStand - 0.2, 0.5)) * 0.7);
      zeichne(this.formStrich, P(t, this.tForm, 0.4));
      const sk0 = P(t, this.tSelbst - 0.1, 0.7, E.out); tr(this.sa, lerp(520, 560, sk0), 560 + (1 - sk0) * 30, 1, lerp(-4, -1.5, sk0)); O(this.sa, sk0);
      this.saZeilen.forEach((z, i) => { O(z.g, 0.2 + 0.8 * P(t, this.tStand + i * 0.18, 0.3)); });
      zeichne(this.unterschrift, P(t, this.tUnter - 0.1, 0.9));
      this.anlagen.forEach((a, i) => { const t0 = this.tAnl - 0.1 + i * 0.25, k = P(t, t0, 0.5, E.back); tr(a, 890, 360 + i * 80, Math.max(0.01, k), 4); O(a, P(t, t0, 0.2)); });
      const ak = P(t, this.tAS - 0.2, 0.7, E.out), klein = P(t, this.tFrier - 0.6, 0.8, E.io);
      tr(this.as, lerp(1500, 1380, ak), 520 + (1 - ak) * 20, 1, lerp(3, 1, ak)); O(this.as, ak);
      this.asLuecken.forEach((z, i) => O(z, 0.15 + 0.85 * P(t, this.tLuecken + i * 0.3, 0.35)));
      this.zuord.forEach((z, i) => { O(z.g, P(t, this.tZuord - 0.6 + i * 0.25, 0.3)); zeichne(z.pf, P(t, this.tZuord - 0.4 + i * 0.25, 0.4)); });
      // datierte Fassung einfrieren, Überprüfung notieren
      const ok = P(t, this.tFrier - 0.4, 0.5, E.out); tr(this.sOrdner.g, 960, 830 + (1 - ok) * 20, 0.8); O(this.sOrdner.g, ok);
      const pk = P(t, this.tFrier, 1.0, E.io); const pp = bogen([560, 560], [960, 800], pk, 140);
      tr(this.paket, pp[0], pp[1], lerp(0.9, 0.55, pk), pk * -8); O(this.paket, Math.min(P(t, this.tFrier - 0.1, 0.2), 1 - P(t, this.tFrier + 1.1, 0.3)));
      tr(this.frierP, 0, 40, Math.max(0.01, P(t, this.tFrier + 0.1, 0.4, E.back)), -6);
      tr(this.pruefP, 1260, 850, Math.max(0.01, P(t, this.tUeberpr, 0.45, E.back))); O(this.pruefP, P(t, this.tUeberpr, 0.2));
    }
  },
});
