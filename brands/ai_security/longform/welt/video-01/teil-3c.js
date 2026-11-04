// Teil 3c · Schritt 5 Kennzeichnungs-Check, Schritt 6 datieren, Rückblick auf die Reihenfolge. Absätze 23 bis 27.
// Bühnen: Weg (Drehscheibe) → Kennzeichnung (Fakt Art. 50) → Weg → datierte Seite (Fakt DSGVO, Lücke Frist) → Weg mit Rückblick.
akt({
  name: 'kennzeichnung-datum',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    const F5 = belegt(); this.tS5 = F5.s;
    this.tArt50 = c('Artikel fünfzig|Artikel 50', 'Article fifty|Article 50');
    this.tSeit = c('seit', 'since');
    this.tKommt = c('Kommt nichts', 'If nothing');
    this.tVeroeff = c('veröffentlichen', 'publish');
    this.tKunden = c('für Kunden betreiben', 'run for customers');
    this.tKISys = c('aus einem KI-System', 'from an AI system');
    this.tVermerk = c('datierter Vermerk', 'dated note');
    this.tKeinFall = c('derzeit kein Fall', 'no case at present');
    this.tDrei = c('drei Betreiberfälle', 'three deployer cases');
    this.tVideo = c('eigenes Video', 'own video');
    this.tS6 = c('Schritt sechs|Schritt 6', 'Step six|Step 6');
    this.tZ = [c('was geregelt ist', 'what is regulated'), c('was offen ist', 'what is open'), c('wer verantwortlich', 'who is responsible'), c('nächste Überprüfung', 'reviewed next')];
    const F6 = belegt(); this.tF6 = F6.s;
    this.tTOM = c('technischen und organisatorischen', 'technical and organisational');
    this.tAkt = c('überprüft und aktualisiert', 'reviewed and updated');
    const LF = belegt(); this.tLF = LF.s;
    this.tKeineQ = c('keine Quelle gefunden', 'found no source');
    this.tToolkit = c('Das Toolkit bietet', 'The toolkit offers');
    this.tSechs = c('sechs oder zwölf', 'six or twelve');
    this.tKeines = c('keines von beiden', 'recommends neither');
    this.tRueck = c('Das ist die Reihenfolge', 'That is the order');
    this.tR = [c('Bestand', 'stock'), c('Konten und die eine Seite', 'accounts and the one page'), c('die Richtlinie', 'the policy'), c('die Einweisung', 'the briefing'), c('Kennzeichnungs-Check', 'labelling check'), c('datierte Seite', 'dated page')];
    this.tEnde = cue({ de: 'Jetzt die Frage', en: 'Now the question' }, { halten: true }).s;
    // Ton (Langfassung 03.11.2026)
    klang(this.tVermerk, 'paper_slide'); (this.tZ || []).forEach((t) => klang(t, 'pop', { laut: 0.5 })); klang(this.tSechs, 'clock_tick');
    (this.tR || []).forEach((t) => klang(t, 'tick', { laut: 0.5 }));

    // ---------- Weg ----------
    const bW = buehne('drei-c-weg', { seed: 1 }); this.bW = bW;
    this.weg = bauWeg(bW.cam);
    this.plus = pille(bW.cam, { de: '+ eine Seite', en: '+ one page' }, { col: C.blue, size: 20 });
    shot(bW, this.tS5 - 0.5, { typ: 'blende', d: 0.7 });

    // ---------- Kennzeichnung ----------
    const bK = buehne('drei-c-kennzeichnung', { seed: 53, regalDeckkraft: 0.6 }); this.bK = bK;
    const kc = bK.cam;
    this.buch = g(kc);
    { const ic = g(this.buch, { transform: 'translate(230 330)' }); iconBook(ic, 90, C.ink); }
    T(this.buch, 296, 316, { de: 'VO (EU) 2024/1689', en: 'Regulation (EU) 2024/1689' }, { mono: 1, size: 22, fill: C.muted });
    T(this.buch, 294, 366, { de: 'Artikel 50', en: 'Article 50' }, { size: 48, weight: 800 });
    this.seitP = pille(kc, { de: 'gilt seit 2. August 2026', en: 'applies since 2 August 2026' }, { icon: 'calendar', col: C.blue, size: 22 });
    this.haus = g(kc, { transform: 'translate(260 640)' }); el('circle', { r: 120, fill: 'url(#gPaper)' }, this.haus); iconBuilding(this.haus, 130, C.ink);
    T(this.haus, 0, 110, { de: 'Muster Elektrotechnik', en: 'Example Electrical' }, { mono: 1, size: 18, fill: C.muted, anchor: 'middle' });
    this.pfad = el('path', { d: 'M 360 640 L 1240 640', fill: 'none', stroke: C.lane, 'stroke-width': 14, 'stroke-linecap': 'round' }, kc);
    this.pruef = g(kc, { transform: 'translate(800 640)' });
    el('rect', { x: -70, y: -120, width: 140, height: 240, rx: 18, fill: C.surface, stroke: C.blue, 'stroke-width': 3 }, this.pruef);
    ikon(this.pruef, 'search', 0, -60, 56, C.blue);
    T(this.pruef, 0, 30, { de: 'KI?', en: 'AI?' }, { size: 34, weight: 800, anchor: 'middle', fill: C.ink });
    T(this.pruef, 0, 92, 'CHECK', { mono: 1, size: 18, fill: C.muted, anchor: 'middle', ls: '0.12em' });
    this.aus = [['globe', { de: 'Website', en: 'Website' }], ['doc', { de: 'Flyer', en: 'Flyer' }], ['chat', { de: 'Kundendienst', en: 'Customer service' }]].map(([ic, lab]) => {
      const gr = g(kc); el('rect', { x: -66, y: -50, width: 132, height: 100, rx: 12, fill: C.paper, filter: 'url(#shadowS)' }, gr); ikon(gr, ic, 0, -10, 40, C.pInk); T(gr, 0, 36, lab, { size: 18, weight: 700, fill: C.pInk, anchor: 'middle' });
      const nein = g(gr, { transform: 'translate(52 -42)' }); el('circle', { r: 16, fill: C.green }, nein); T(nein, 0, 6, { de: 'nein', en: 'no' }, { mono: 1, size: 12, fill: '#fff', anchor: 'middle' });
      return { g: gr, nein };
    });
    this.vermerk = g(kc);
    const vb = blatt(this.vermerk, { w: 540, h: 330, kicker: { de: 'VERMERK · KENNZEICHNUNG', en: 'NOTE · LABELLING' }, datum: { de: 'STAND 30.10.2026', en: 'AS OF 30 OCT 2026' } });
    T(vb.g, vb.left, vb.y + 50, { de: 'derzeit kein Fall', en: 'no case at present' }, { size: 40, weight: 800, fill: C.pInk });
    linien(vb.g, vb.left, vb.y + 90, 300, 3, 26, C.pBar2, 10);
    this.faelle = [1, 2, 3].map((i) => { const gr = g(kc); karte(gr, -90, -60, 180, 120, { fill: C.surface, stroke: C.edge, gestrichelt: true }); T(gr, 0, -10, { de: 'Fall ' + i, en: 'Case ' + i }, { size: 26, weight: 800, anchor: 'middle' }); T(gr, 0, 26, { de: 'BETREIBER', en: 'DEPLOYER' }, { mono: 1, size: 15, fill: C.muted, anchor: 'middle', ls: '0.1em' }); return gr; });
    this.eigenesVideo = pille(kc, { de: 'eigenes Video', en: 'own video' }, { icon: 'wave', col: C.blue, size: 22 });
    shot(bK, this.tS5 + 0.9, { typ: 'kreis', d: 1.2, p: wegPunkt(4) });
    shot(bW, this.tS6 - 1.0, { typ: 'kreisRaus', d: 1.0, p: wegPunkt(4) });

    // ---------- datierte Seite ----------
    const bD = buehne('drei-c-datiert', { seed: 59, regalDeckkraft: 0.6 }); this.bD = bD;
    const dc = bD.cam;
    this.ring = el('circle', { cx: 700, cy: 560, r: 360, fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-dasharray': '18 14' }, dc);
    this.ringPfeile = [0, 1, 2].map((i) => { const gr = g(dc); el('path', { d: 'M -14 -12 L 10 0 L -14 12', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, gr); return gr; });
    this.ringLab = pille(dc, { de: 'überprüfen und aktualisieren', en: 'review and update' }, { icon: 'cycle', col: C.blue, size: 22 });
    this.seite = g(dc);
    const sb = blatt(this.seite, { w: 560, h: 560, kicker: { de: 'STAND · DATIERT', en: 'STATUS · DATED' }, datum: { de: 'FASSUNG 1', en: 'VERSION 1' }, titel: { de: 'Eine Seite', en: 'One page' }, tSize: 34 });
    this.fassung = T(sb.g, sb.right, sb.y0 + sb.pad + 8, { de: 'FASSUNG 2', en: 'VERSION 2' }, { mono: 1, size: 15, fill: C.blueDeep, anchor: 'end', ls: '0.06em' });
    this.fassungAlt = sb.g.querySelectorAll('text')[1];
    const ZE = [['check', { de: 'Geregelt', en: 'Regulated' }, C.greenDeep], ['unknown', { de: 'Offen', en: 'Open' }, C.amberDeep], ['person', { de: 'Verantwortlich', en: 'Responsible' }, C.pInk], ['calendar', { de: 'Nächste Überprüfung', en: 'Next review' }, C.blueDeep]];
    this.dz = ZE.map(([ic, lab, col], i) => { const gr = g(sb.g); const y = sb.y + 34 + i * 82; el('circle', { cx: sb.left + 24, cy: y, r: 26, fill: '#eef2f8' }, gr); ikon(gr, ic, sb.left + 24, y, 30, col); T(gr, sb.left + 66, y + 9, lab, { size: 27, weight: 800, fill: C.pInk }); el('rect', { x: sb.left + 400, y: y - 6, width: 80, height: 12, rx: 6, fill: C.pBar2 }, gr); return gr; });
    this.dsgvo = g(dc);
    { const ic = g(this.dsgvo, { transform: 'translate(1330 330)' }); iconBook(ic, 80, C.ink); }
    T(this.dsgvo, 1390, 318, { de: 'VO (EU) 2016/679 · DSGVO', en: 'Regulation (EU) 2016/679 · GDPR' }, { mono: 1, size: 20, fill: C.muted });
    T(this.dsgvo, 1388, 364, { de: 'Art. 24 Abs. 1', en: 'Art. 24(1)' }, { size: 42, weight: 800 });
    this.tom = pille(dc, { de: 'technische und organisatorische Maßnahmen', en: 'technical and organisational measures' }, { icon: 'list', col: C.blue, size: 20 });
    this.frist = g(dc);
    T(this.frist, 1250, 560, { de: 'Frist?', en: 'Interval?' }, { size: 44, weight: 800 });
    this.fristQ = pille(this.frist, { de: 'keine Quelle gefunden', en: 'no source found' }, { marke: 'luecke', col: C.red, gestrichelt: true, size: 22 });
    tr(this.fristQ, 1420, 630);
    this.opt = [{ de: '6 Monate', en: '6 months' }, { de: '12 Monate', en: '12 months' }].map((s) => pille(dc, s, { icon: 'calendar', col: C.muted, size: 26 }));
    this.toolkitLab = T(dc, 1250, 720, { de: 'Toolkit bietet beide an', en: 'Toolkit offers both' }, { mono: 1, size: 20, fill: C.muted, ls: '0.06em' });
    this.keineEmpf = pille(dc, { de: 'keine Empfehlung', en: 'no recommendation' }, { col: C.muted, gestrichelt: true, size: 22 });
    shot(bD, this.tS6 + 0.3, { typ: 'kreis', d: 1.2, p: wegPunkt(5) });
    shot(bW, this.tRueck - 0.9, { typ: 'kreisRaus', d: 1.0, p: wegPunkt(5) });
    this.buehnen = [bW, bK, bD];

    // ---------- Einblendungen ----------
    kopf(this.tS5, this.tS6 - 1.2, { de: 'SCHRITT 5', en: 'STEP 5' }, { de: 'Kennzeichnungs-Check', en: 'Labelling check' });
    kopf(this.tS6, this.tF6 - 0.3, { de: 'SCHRITT 6', en: 'STEP 6' }, { de: 'Datieren', en: 'Date it' });
    kopf(this.tF6, this.tLF - 0.3, { de: 'SCHRITT 6', en: 'STEP 6' }, { de: 'Überprüfen steht in der DSGVO', en: 'Review is in the GDPR' });
    kopf(this.tLF, this.tRueck - 0.9, { de: 'SCHRITT 6', en: 'STEP 6' }, { de: 'Die Frist ist offen', en: 'The interval is open' });
    kopf(this.tRueck, this.tEnde - 0.3, { de: '2 · WOMIT SIE ANFANGEN', en: '2 · WHERE YOU START' }, { de: 'Die Reihenfolge', en: 'The order' });
  },

  zeichnen(t) {
    if (this.bW.vis) {
      kamera(this.bW, WEG_BLICK.f, WEG_BLICK.z);
      const rueck = t > this.tRueck - 1;
      const head = rueck ? wegStrecke(this.weg, 1, t > this.tR[0] - 0.3 && t < this.tR[5] + 0.9 ? clamp((t - this.tR[0] + 0.3) / (this.tR[5] + 0.9 - this.tR[0] + 0.3)) : -1) : wegStrecke(this.weg, 1, -1);
      const ueb = UEBERGANG && (UEBERGANG.von === this.bW || UEBERGANG.nach === this.bW) ? (UEBERGANG.typ === 'kreisRaus' ? 1 - UEBERGANG.k : UEBERGANG.k) : 0;
      this.weg.nodes.forEach((n, i) => {
        let aktiv = 0, erledigt = i < 4 ? 1 : 0, gross = 0;
        if (i === 4) { aktiv = Math.min(P(t, this.tS5 - 0.2, 0.4), 1 - P(t, this.tS6 - 0.6, 0.4)); erledigt = P(t, this.tS6 - 0.6, 0.4); gross = P(t, this.tS5, 0.4, E.back) * (1 - erledigt); }
        if (i === 5) { aktiv = P(t, this.tS6 - 0.4, 0.4) * (rueck ? 0 : 1); erledigt = rueck ? 1 : 0; gross = P(t, this.tS6 - 0.2, 0.4, E.back) * (rueck ? 0 : 1); }
        if (rueck) { aktiv = fenster(t, this.tR[i] - 0.1, 0.25, (this.tR[i + 1] || this.tR[5] + 1.2) - 0.1, 0.3); erledigt = 1; }
        wegKnoten(n, { aktiv, erledigt, haken: erledigt * (1 - aktiv), gross, labAus: clamp(ueb * 2.5), nah: rueck ? Math.exp(-Math.pow((head - this.weg.slotAt[i]) / 90, 2)) : 0 });
      });
      tr(this.plus, WEG_SLOTS[1][0], WEG_SLOTS[1][1] + 140, 1 + 0.1 * (rueck ? fenster(t, this.tR[1], 0.25, this.tR[2], 0.3) : 0)); O(this.plus, 0.9 * (1 - clamp(ueb * 2.5)));
    }
    if (this.bK.vis) {
      kamera(this.bK, [960, 540], 1);
      O(this.buch, P(t, this.tArt50 - 0.3, 0.5)); rein(this.seitP, 360, 430, t, this.tSeit, 0.45);
      O(this.haus, P(t, this.tKommt - 0.3, 0.5)); zeichne(this.pfad, P(t, this.tKommt, 0.8)); O(this.pruef, P(t, this.tKommt + 0.3, 0.4));
      const starts = [this.tVeroeff - 0.4, this.tVeroeff + 0.3, this.tKunden + 0.5];
      this.aus.forEach((a, i) => {
        const t0 = starts[i], k = P(t, t0, 1.6, E.io);
        const x = k < 0.5 ? lerp(360, 800, E.out(k * 2)) : lerp(800, 1180, E.in(k * 2 - 1));
        tr(a.g, x, 640, 1.2, 0);
        O(a.g, Math.min(P(t, t0, 0.2), 1 - P(t, t0 + 1.5, 0.3)));
        const n = P(t, t0 + 0.75, 0.35, E.back); a.nein.setAttribute('transform', `translate(52 -42) scale(${Math.max(0.01, n).toFixed(3)})`); O(a.nein, P(t, t0 + 0.75, 0.2));
      });
      const vi = P(t, this.tVermerk - 0.2, 0.7, E.out); tr(this.vermerk, 1460, 560 + (1 - vi) * 40, 1, 1.5); O(this.vermerk, vi);
      sk(this.vermerk, 1460, 560, 1 + 0.04 * puls(t, this.tKeinFall, 0.8, 8));
      tr(this.vermerk, 1460, 560 + (1 - vi) * 40, 1 + 0.04 * puls(t, this.tKeinFall, 0.8, 8), 1.5);
      this.faelle.forEach((f, i) => { const k = P(t, this.tDrei + i * 0.2, 0.45, E.back); tr(f, 1150 + i * 210, 790, Math.max(0.01, k)); O(f, P(t, this.tDrei + i * 0.2, 0.2)); });
      rein(this.eigenesVideo, 1360, 880, t, this.tVideo, 0.45);
      O(this.vermerk, vi * (1 - 0.0));
    }
    if (this.bD.vis) {
      kamera(this.bD, [960, 540], 1);
      const si = P(t, this.tS6 + 0.6, 0.7, E.out); tr(this.seite, 700, 560 + (1 - si) * 40, 1, -1); O(this.seite, si);
      this.dz.forEach((z, i) => O(z, 0.2 + 0.8 * P(t, this.tZ[i], 0.35)));
      const rg = P(t, this.tF6, 1.0);
      O(this.ring, rg); this.ring.setAttribute('stroke-dashoffset', (-t * 40 * P(t, this.tAkt, 0.4)).toFixed(1));
      const rot = (t - this.tAkt) * 50 * P(t, this.tAkt, 0.4);
      this.ringPfeile.forEach((p, i) => { const a = (i * 120 + rot - 90) * Math.PI / 180; tr(p, 700 + 360 * Math.cos(a), 560 + 360 * Math.sin(a), 1, i * 120 + rot); O(p, rg); });
      rein(this.ringLab, 1500, 560, t, this.tAkt, 0.45, this.tLF - 0.2);
      const fw = P(t, this.tAkt + 0.6, 0.4); O(this.fassung, fw); O(this.fassungAlt, 1 - fw);
      const di = fenster(t, this.tF6 + 0.2, 0.5, this.tLF - 0.2, 0.4); O(this.dsgvo, di);
      rein(this.tom, 1500, 450, t, this.tTOM, 0.45, this.tLF - 0.2);
      const fi = P(t, this.tLF, 0.5); O(this.frist, fi);
      O(this.fristQ, P(t, this.tKeineQ, 0.4));
      this.opt.forEach((o, i) => rein(o, 1340 + i * 260, 790, t, this.tSechs + i * 0.3, 0.45));
      O(this.toolkitLab, P(t, this.tToolkit, 0.4));
      rein(this.keineEmpf, 1470, 880, t, this.tKeines, 0.45);
      if (this.bD.vis && t > this.tLF) this.ring.setAttribute('stroke', C.blue);
    }
  },
});
