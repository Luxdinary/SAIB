// Teil 3b · Schritt 3 Richtlinie und Schritt 4 Einweisung. Absätze 17 bis 22 des Skripts.
// Bühnen: Weg (Drehscheibe) → Richtlinie mit neun Regelbereichen, Unterschrift, vier Angaben (Auslegung) → Weg →
// Einweisung mit Nachweis → Artikel 4 und Kommission (Fakten) → Rhythmus (Lücke).
akt({
  name: 'richtlinie-einweisung',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    // ---------- Wortanker ----------
    this.tS3 = c('Schritt drei|Schritt 3', 'Step three|Step 3');
    this.tNeun = c('Neun Regelbereiche', 'Nine areas');
    this.tB = [c('zugelassene Tools', 'permitted tools and access'), c('zulässige und unzulässige', 'permitted and prohibited'), c('was nie hinein', 'what never goes in'),
      c('unvermeidbarem Personenbezug', 'unavoidable personal data'), c('Prüfung vor Verwendung', 'review before use'), c('Freigabe von Schriftstücken', 'release of documents'),
      c('Kennzeichnung', 'labelling'), c('Meldung von Vorfällen', 'reporting incidents'), c('Zuständigkeit für Zweifelsfälle', 'responsibility in case')];
    this.tUnter = c('Von der Leitung', 'Signed by the management');
    const A = belegt(); this.tA = A.s;
    this.tVier = c('machen aus einem Text', 'make a text');
    this.tV = [c('Ein Datum', 'A date'), c('verantwortliche Person', 'responsible person'), c('Weg der Bekanntgabe', 'way in which it was announced'), c('eine Bestätigung', 'a confirmation')];
    this.tKeine = c('Keine Quelle nennt', 'No source lists');
    this.tAufsicht = c('Formulierung der Aufsicht', 'supervisory wording');
    this.tErteilt = c('erteilt und dokumentiert', 'issued and documented');
    this.tNach = c('nach der Einweisung', 'after the briefing');
    this.tNiemand = c('die niemand kennt', 'nobody knows');
    this.tS4 = c('Schritt vier|Schritt 4', 'Step four|Step 4');
    this.tNachweis = c('der Nachweis dazu', 'the record of it');
    { const di = cue({ de: 'Datum, Inhalte', en: 'date, contents' }); this.tDatum = di.s; this.tInhalte = Math.max(di.s + 0.5, di.e - 0.4); }
    this.tDabei = c('wer dabei war', 'who attended');
    const F4 = belegt(); this.tF4 = F4.s;
    this.tAnb = c('Anbietern und Betreibern', 'providers and deployers');
    this.tMass = c('Maßnahmen', 'measures');
    this.tKomp = c('KI-Kompetenz', 'AI literacy');
    this.tNiveau = c('bestimmtes Niveau', 'specific level');
    this.tSeit = c('gilt seit', 'has applied since');
    this.tWort = c('heutiger Wortlaut', 'current wording');
    const FK = belegt(); this.tFK = FK.s;
    this.tZert = c('Zertifikat', 'certificate');
    this.tVerz = c('internes Verzeichnis', 'internal record');
    this.tLeit = c('Leitfaden, kein Gesetz', 'guidance, not law');
    const LU = belegt(); this.tLU = LU.s;
    this.tAufb = c('wie lange', 'how long');
    this.tKeineQ = c('keine Quelle gefunden', 'found no source');
    this.tRhythmus = c('Den Rhythmus', 'sets the rhythm');
    this.tEnde = cue({ de: 'Schritt fünf|Schritt 5', en: 'Step five|Step 5' }, { halten: true }).s;
    // Ton (Langfassung 03.11.2026)
    (this.tB || []).forEach((t) => klang(t, 'tick', { laut: 0.5 })); klang(this.tUnter, 'paper_slide'); (this.tV || []).forEach((t) => klang(t, 'pop', { laut: 0.5 }));
    klang(this.tNachweis, 'stamp_soft'); klang(this.tZert, 'strike', { laut: 0.5 }); klang(this.tRhythmus, 'clock_tick');
    const K = { de: '2 · WOMIT SIE ANFANGEN', en: '2 · WHERE YOU START' };

    // ---------- Bühne 1: Weg als Drehscheibe ----------
    const bW = buehne('schritte-weg', { seed: 1 }); this.bW = bW;
    this.weg = bauWeg(bW.cam);
    this.plus = pille(bW.cam, { de: '+ eine Seite', en: '+ one page' }, { col: C.blue, size: 20 });
    shot(bW, this.tS3 - 0.5, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 2: Richtlinie ----------
    const bR = buehne('schritte-richtlinie', { seed: 37, regalDeckkraft: 0.7 }); this.bR = bR;
    this.doc = g(bR.cam);
    const db = blatt(this.doc, { w: 760, h: 760, kicker: { de: 'KI-NUTZUNGSRICHTLINIE · MUSTER ELEKTROTECHNIK', en: 'AI USAGE POLICY · EXAMPLE ELECTRICAL' }, titel: { de: 'Neun Regelbereiche', en: 'Nine areas' }, tSize: 34 });
    this.db = db;
    const BER = [
      ['spark', { de: 'Tools und Zugänge', en: 'Tools and access' }], ['list', { de: 'Verwendungen', en: 'Uses' }], ['cross', { de: 'Was nie hinein darf', en: 'What never goes in' }],
      ['id', { de: 'Personenbezug', en: 'Personal data' }], ['search', { de: 'Prüfung vor Verwendung', en: 'Review before use' }], ['mail', { de: 'Freigabe nach außen', en: 'Release outside' }],
      ['doc', { de: 'Kennzeichnung', en: 'Labelling' }], ['warn', { de: 'Vorfälle melden', en: 'Report incidents' }], ['question', { de: 'Zweifelsfälle', en: 'Cases of doubt' }],
    ];
    this.TW = 212; this.TH = 150;
    this.kacheln = BER.map(([ic, lab], i) => {
      const gr = g(bR.cam);
      el('rect', { x: -this.TW / 2, y: -this.TH / 2, width: this.TW, height: this.TH, rx: 12, fill: '#eef2f8', stroke: '#d3dae6', 'stroke-width': 2 }, gr);
      T(gr, -this.TW / 2 + 16, -this.TH / 2 + 30, '§ ' + (i + 1), { mono: 1, size: 18, fill: C.blueDeep });
      ikon(gr, ic, this.TW / 2 - 34, -this.TH / 2 + 32, 34, C.pInk);
      const tx = TB(gr, -this.TW / 2 + 16, 18, lab, { size: 23, weight: 800, fill: C.pInk, maxW: this.TW - 30, lh: 27 });
      if (tx.zeilen === 1) tx.setAttribute('y', 30);
      const zx = (i % 3) * (this.TW + 20) - (this.TW + 20), zy = Math.floor(i / 3) * (this.TH + 18);
      return { g: gr, ziel: [zx, db.y + this.TH / 2 + 10 + zy] };
    });
    this.sigY = db.y + 3 * (this.TH + 18) + 50;
    el('rect', { x: db.left, y: this.sigY + 40, width: 300, height: 2, fill: C.pMuted }, db.g);
    T(db.g, db.left, this.sigY + 66, { de: 'LEITUNG · UNTERSCHRIFT', en: 'MANAGEMENT · SIGNATURE' }, { mono: 1, size: 15, fill: C.pMuted, ls: '0.08em' });
    this.sig = el('path', { d: `M ${db.left + 10} ${this.sigY + 30} c 20 -40 30 -40 36 -4 s 14 20 26 -14 s 16 -30 22 6 s 20 18 34 -8 s 22 -12 40 4 s 30 6 60 -10`, fill: 'none', stroke: C.blueDeep, 'stroke-width': 4, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, db.g);
    this.stift = g(db.g); iconPen(this.stift, 46, C.pInk);
    this.geltend = pille(db.g, { de: 'gilt', en: 'in force' }, { icon: 'check', col: C.green, size: 24 });
    // vier Angaben
    this.vier = g(bR.cam);
    karte(this.vier, 1180, 230, 600, 470, { fill: C.surface });
    T(this.vier, 1214, 286, { de: 'VIER ANGABEN', en: 'FOUR THINGS' }, { mono: 1, size: 20, fill: C.purple, ls: '0.12em' });
    const VIER = [['calendar', { de: 'Datum, ab dem sie gilt', en: 'Date it applies from' }], ['person', { de: 'verantwortliche Person', en: 'responsible person' }],
      ['megaphone', { de: 'Weg der Bekanntgabe', en: 'way it was announced' }], ['group', { de: 'Bestätigung je Person', en: 'confirmation by each person' }]];
    this.vzeilen = VIER.map(([ic, lab], i) => { const gr = g(this.vier); const y = 340 + i * 88; el('circle', { cx: 1240, cy: y, r: 30, fill: C.raised, stroke: C.purple, 'stroke-width': 2.5 }, gr); ikon(gr, ic, 1240, y, 34, C.ink); T(gr, 1290, y + 10, lab, { size: 28, weight: 700 }); const hk = g(gr, { transform: `translate(1740 ${y})` }); iconCheck(hk, 30, C.green); return { g: gr, hk }; });
    this.keineQ = pille(bR.cam, { de: 'keine Quelle nennt diese vier', en: 'no source lists these four' }, { icon: 'book', col: C.muted, gestrichelt: true, size: 22 });
    this.aufsicht = g(bR.cam);
    { const ic = g(this.aufsicht, { transform: 'translate(1270 790)' }); iconInstitution(ic, 54, C.ink); }
    this.wE = pille(this.aufsicht, { de: 'erteilt', en: 'issued' }, { col: C.blue, size: 22 });
    this.wD = pille(this.aufsicht, { de: 'dokumentiert', en: 'documented' }, { col: C.blue, size: 22 });
    tr(this.wE, 1430, 790); tr(this.wD, 1640, 790);
    // Zeitachse: Einweisung vor Geltungsbeginn
    this.achse = g(bR.cam);
    el('rect', { x: 1200, y: 806, width: 560, height: 4, rx: 2, fill: C.line }, this.achse);
    this.mEinw = g(this.achse); el('circle', { r: 30, fill: C.raised, stroke: C.blue, 'stroke-width': 3 }, this.mEinw); iconGroup(this.mEinw, 38, C.ink); T(this.mEinw, 0, 62, { de: 'Einweisung', en: 'Briefing' }, { size: 22, weight: 700, anchor: 'middle' });
    this.mGelt = g(this.achse); el('circle', { r: 30, fill: C.raised, stroke: C.green, 'stroke-width': 3 }, this.mGelt); iconCalendar(this.mGelt, 34, C.ink); T(this.mGelt, 0, 62, { de: 'gilt ab', en: 'in force' }, { size: 22, weight: 700, anchor: 'middle' });
    this.pfeil = el('path', { d: 'M 1420 808 L 1560 808', fill: 'none', stroke: C.blue, 'stroke-width': 4, 'marker-end': '' }, this.achse);
    this.niemand = pille(bR.cam, { de: 'Regel, die niemand kennt', en: 'a rule nobody knows' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 22 });
    shot(bR, this.tS3 + 1.1, { typ: 'kreis', d: 1.3, p: wegPunkt(2) });
    shot(bW, this.tS4 - 1.0, { typ: 'kreisRaus', d: 1.1, p: wegPunkt(2) });

    // ---------- Bühne 3: Einweisung ----------
    const bE = buehne('schritte-einweisung', { seed: 41 }); this.bE = bE;
    const ec = bE.cam;
    raum(ec, 100, 280, 1720, 590, { de: 'BESPRECHUNG · MUSTER ELEKTROTECHNIK E.U.', en: 'MEETING ROOM · EXAMPLE ELECTRICAL LTD' });
    this.zuh = [seated(ec, 240, 790, BESETZUNG.a), seated(ec, 470, 790, BESETZUNG.b), seated(ec, 700, 790, BESETZUNG.c)];
    this.lehr = stehend(ec, 860, 862, { ...BESETZUNG.lehrling, skala: 0.8 });
    this.flip = g(ec);
    el('rect', { x: 980, y: 400, width: 230, height: 300, rx: 6, fill: C.paper }, this.flip);
    el('path', { d: 'M 1095 700 V 860 M 1095 740 L 1010 860 M 1095 740 L 1180 860', stroke: '#2a3858', 'stroke-width': 8, 'stroke-linecap': 'round' }, this.flip);
    T(this.flip, 1000, 440, { de: 'KI-REGELN', en: 'AI RULES' }, { mono: 1, size: 20, fill: C.blueDeep, ls: '0.08em' });
    this.flipZ = linien(this.flip, 1000, 466, 180, 6, 34, C.pBar2, 12);
    this.trainer = stehend(ec, 1290, 862, { jacke: BESETZUNG.inhaberin.shirt, haar: 'long', kragen: '#b9c3d8', skala: 0.95 });
    this.nw = g(ec);
    const nb = blatt(this.nw, { w: 440, h: 500, kicker: { de: 'NACHWEIS · EINWEISUNG', en: 'RECORD · BRIEFING' } });
    const NZ = [['calendar', { de: 'Datum', en: 'Date' }], ['list', { de: 'Inhalte', en: 'Contents' }], ['group', { de: 'Anwesend', en: 'Attended' }]];
    this.nzeilen = NZ.map(([ic, lab], i) => { const gr = g(nb.g); const y = nb.y + 24 + i * 100; ikon(gr, ic, nb.left + 18, y + 8, 32, C.pInk); T(gr, nb.left + 50, y + 18, lab, { size: 26, weight: 800, fill: C.pInk }); return { g: gr, y }; });
    this.nwBar = [linien(nb.g, nb.left + 50, nb.y + 54, 220, 1, 20, C.blueBar, 12), linien(nb.g, nb.left + 50, nb.y + 154, 280, 2, 22, C.blueBar, 12)];
    this.nwHaken = [0, 1, 2, 3].map((k) => { const kk = kaestchen(nb.g, nb.left + 64 + k * 62, nb.y + 266, 30); iconPerson(g(nb.g, { transform: `translate(${nb.left + 64 + k * 62} ${nb.y + 306})` }), 28, C.pMuted); return kk; });
    tr(this.nw, 1590, 560, 1, 1.5);
    shot(bE, this.tS4 + 0.25, { typ: 'kreis', d: 1.2, p: wegPunkt(3) });

    // ---------- Bühne 4: Artikel 4 und Kommission ----------
    const bK = buehne('schritte-art4', { seed: 43, regalDeckkraft: 0.6 }); this.bK = bK;
    const kc = bK.cam;
    this.art = g(kc);
    { const ic = g(this.art, { transform: 'translate(240 330)' }); iconBook(ic, 96, C.ink); }
    T(this.art, 310, 316, { de: 'VO (EU) 2024/1689', en: 'Regulation (EU) 2024/1689' }, { mono: 1, size: 22, fill: C.muted, ls: '0.06em' });
    T(this.art, 308, 368, { de: 'Artikel 4', en: 'Article 4' }, { size: 50, weight: 800 });
    this.anb = pille(kc, { de: 'Anbieter', en: 'Providers' }, { icon: 'spark', col: C.blue, size: 24 });
    this.bet = pille(kc, { de: 'Betreiber', en: 'Deployers' }, { icon: 'building', col: C.blue, size: 24 });
    this.stufen = [0, 1, 2].map((i) => { const gr = g(kc); el('rect', { x: 560 + i * 110, y: 700 - (i + 1) * 70, width: 104, height: (i + 1) * 70, rx: 8, fill: C.raised, stroke: C.blue, 'stroke-width': 2.5 }, gr); return gr; });
    this.massLab = T(kc, 560, 735, { de: 'Maßnahmen', en: 'measures' }, { size: 26, weight: 700 });
    this.balkenRahmen = el('rect', { x: 930, y: 400, width: 70, height: 300, rx: 10, fill: 'none', stroke: C.line, 'stroke-width': 3 }, kc);
    this.balken = el('rect', { x: 936, y: 694, width: 58, height: 0, rx: 7, fill: C.blue }, kc);
    this.kompLab = T(kc, 965, 735, { de: 'KI-Kompetenz', en: 'AI literacy' }, { size: 26, weight: 700, anchor: 'middle' });
    this.niveau = el('line', { x1: 880, y1: 430, x2: 1060, y2: 430, stroke: C.muted, 'stroke-width': 3, 'stroke-dasharray': '10 8' }, kc);
    this.niveauP = pille(kc, { de: 'kein garantiertes Niveau', en: 'no guaranteed level' }, { col: C.muted, gestrichelt: true, size: 22 });
    this.zeit = g(kc);
    el('rect', { x: 200, y: 820, width: 900, height: 4, rx: 2, fill: C.line }, this.zeit);
    this.d1 = g(this.zeit); el('circle', { cx: 330, cy: 822, r: 12, fill: C.blue }, this.d1); T(this.d1, 330, 806, { de: '2. Februar 2025', en: '2 February 2025' }, { size: 26, weight: 800, anchor: 'middle' }); T(this.d1, 330, 860, { de: 'GILT', en: 'APPLIES' }, { mono: 1, size: 18, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.d2 = g(this.zeit); el('circle', { cx: 800, cy: 822, r: 12, fill: C.blue }, this.d2); T(this.d2, 800, 806, { de: '27. Juli 2026', en: '27 July 2026' }, { size: 26, weight: 800, anchor: 'middle' }); T(this.d2, 800, 860, { de: 'HEUTIGER WORTLAUT', en: 'CURRENT WORDING' }, { mono: 1, size: 18, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.kom = g(kc);
    { const ic = g(this.kom, { transform: 'translate(1500 300)' }); el('circle', { r: 100, fill: 'url(#gPaper)' }, ic); iconInstitution(ic, 84, C.ink); }
    T(this.kom, 1500, 388, { de: 'EUROPÄISCHE KOMMISSION', en: 'EUROPEAN COMMISSION' }, { mono: 1, size: 20, fill: C.muted, anchor: 'middle', ls: '0.08em' });
    this.zert = g(kc); { const z = g(this.zert); el('rect', { x: -110, y: -80, width: 220, height: 160, rx: 6, fill: C.paper }, z); iconCert(z, 120, C.pMuted); }
    this.zertX = g(kc); iconCross(this.zertX, 120, C.red);
    this.zertLab = T(kc, 1330, 650, { de: 'Zertifikat: nicht nötig', en: 'certificate: not needed' }, { size: 24, weight: 700, anchor: 'middle' });
    this.verz = g(kc);
    const vb = blatt(this.verz, { w: 300, h: 300, kicker: { de: 'VERZEICHNIS DER SCHULUNGEN', en: 'RECORD OF TRAININGS' }, pad: 24, kSize: 12 });
    for (let r = 0; r < 4; r++) { el('rect', { x: vb.left, y: vb.y + 8 + r * 44, width: 60, height: 10, rx: 5, fill: C.blueBar }, vb.g); el('rect', { x: vb.left + 74, y: vb.y + 8 + r * 44, width: 150, height: 10, rx: 5, fill: C.pBar2 }, vb.g); }
    this.leit = pille(kc, { de: 'Leitfaden, kein Gesetz', en: 'guidance, not law' }, { icon: 'book', col: C.muted, size: 24 });
    shot(bK, this.tF4 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 5: Rhythmus offen ----------
    const bL = buehne('schritte-rhythmus', { seed: 47, regalDeckkraft: 0.6 }); this.bL = bL;
    const lc = bL.cam;
    this.monate = Array.from({ length: 12 }, (_, i) => { const gr = g(lc); el('rect', { x: 300 + i * 112, y: 500, width: 96, height: 110, rx: 10, fill: C.surface, stroke: C.edge, 'stroke-width': 2.5 }, gr); T(gr, 348 + i * 112, 570, String(i + 1), { mono: 1, size: 26, fill: C.dim, anchor: 'middle' }); return gr; });
    this.fragen = [1, 4, 6, 9, 11].map((i) => { const gr = g(lc, { transform: `translate(${348 + i * 112} 450)` }); iconUnknown(gr, 52, C.red); return gr; });
    this.wieOft = T(lc, 300, 400, { de: 'Wie oft wiederholen?', en: 'How often to repeat?' }, { size: 34, weight: 800 });
    this.aufb = g(lc, { transform: 'translate(1100 720)' });
    { const ic = g(this.aufb); iconDoc(ic, 70, C.ink); const k2 = g(this.aufb, { transform: 'translate(70 -20)' }); iconClock(k2, 50, C.red); T(this.aufb, 120, 14, { de: 'Wie lange aufbewahren?', en: 'How long to keep?' }, { size: 30, weight: 800 }); }
    this.keineQP = pille(lc, { de: 'keine Quelle gefunden', en: 'no source found' }, { marke: 'luecke', col: C.red, gestrichelt: true, size: 26 });
    this.betr = g(lc, { transform: 'translate(500 760)' }); iconBuilding(this.betr, 70, C.blue); T(this.betr, 60, 14, { de: 'Der Betrieb setzt den Rhythmus', en: 'The business sets the rhythm' }, { size: 30, weight: 800 });
    this.takt = [2, 8].map((i) => { const gr = g(lc, { transform: `translate(${348 + i * 112} 555)` }); el('rect', { x: -48, y: -55, width: 96, height: 110, rx: 10, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, gr); return gr; });
    shot(bL, this.tLU - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [bW, bR, bE, bK, bL];

    // ---------- Einblendungen ----------
    kopf(this.tS3, this.tA - 0.3, { de: 'SCHRITT 3', en: 'STEP 3' }, { de: 'Die Richtlinie', en: 'The policy' });
    kopf(this.tA, this.tS4 - 1.2, { de: 'SCHRITT 3', en: 'STEP 3' }, { de: 'Was eine Regel geltend macht', en: 'What puts a rule in force' });
    kopf(this.tS4, this.tF4 - 0.3, { de: 'SCHRITT 4', en: 'STEP 4' }, { de: 'Einweisung mit Nachweis', en: 'Briefing with a record' });
    kopf(this.tF4, this.tFK - 0.3, { de: 'SCHRITT 4', en: 'STEP 4' }, { de: 'Artikel 4 der KI-Verordnung', en: 'Article 4 of the AI Act' });
    kopf(this.tFK, this.tLU - 0.3, { de: 'SCHRITT 4', en: 'STEP 4' }, { de: 'Kein Zertifikat nötig', en: 'No certificate needed' });
    kopf(this.tLU, this.tEnde - 0.3, { de: 'SCHRITT 4', en: 'STEP 4' }, { de: 'Der Rhythmus ist offen', en: 'The rhythm is open' });
  },

  zeichnen(t) {
    // ---------- Weg ----------
    if (this.bW.vis) {
      kamera(this.bW, WEG_BLICK.f, WEG_BLICK.z);
      wegStrecke(this.weg, 1, -1);
      const ueb = UEBERGANG && (UEBERGANG.von === this.bW || UEBERGANG.nach === this.bW) ? (UEBERGANG.typ === 'kreisRaus' ? 1 - UEBERGANG.k : UEBERGANG.k) : 0;
      this.weg.nodes.forEach((n, i) => {
        const fertig3 = P(t, this.tS4 - 0.6, 0.4);
        const aktiv = i === 2 ? Math.min(P(t, this.tS3 - 0.2, 0.4), 1 - fertig3) : i === 3 ? P(t, this.tS4 - 0.4, 0.4) : 0;
        const erledigt = i < 2 ? 1 : i === 2 ? fertig3 : 0;
        wegKnoten(n, { aktiv, erledigt, haken: erledigt, gross: (i === 2 ? P(t, this.tS3 + 0.2, 0.4, E.back) * (1 - fertig3) : 0) + (i === 3 ? P(t, this.tS4 - 0.2, 0.4, E.back) : 0), labAus: clamp(ueb * 2.5) });
      });
      tr(this.plus, WEG_SLOTS[1][0], WEG_SLOTS[1][1] + 140); O(this.plus, 0.9 * (1 - clamp(ueb * 2.5)));
    }
    // ---------- Richtlinie ----------
    if (this.bR.vis) {
      const links = P(t, this.tA - 0.2, 0.9);
      kamera(this.bR, [960, 540], 1);
      tr(this.doc, lerp(800, 560, links), 570, lerp(1, 0.86, links), -1);
      this.kacheln.forEach((k, i) => {
        const t0 = this.tB[i] - 0.2, kk = P(t, t0, 0.7, E.io);
        const ziel = [lerp(800, 560, links) + k.ziel[0] * lerp(1, 0.86, links), 570 + k.ziel[1] * lerp(1, 0.86, links)];
        const p = bogen([1700, 220 + (i % 3) * 60], ziel, kk, 120);
        tr(k.g, p[0], p[1], lerp(0.7, lerp(1, 0.86, links), kk), lerp(8, -1, kk)); O(k.g, P(t, t0, 0.2));
      });
      const sg = P(t, this.tUnter + 0.2, 1.2, E.io); zeichne(this.sig, sg);
      if (sg > 0 && sg < 1) { const pt = this.sig.getPointAtLength(sg * this.sig.__len); tr(this.stift, pt.x + 14, pt.y - 20); O(this.stift, 1); } else O(this.stift, 0);
      const alle = P(t, this.tV[3] + 0.8, 0.4);
      sk(this.geltend, 0, 0, 1); tr(this.geltend, this.db.right - 70, this.sigY + 30, Math.max(0.01, P(t, this.tV[3] + 0.8, 0.45, E.back))); O(this.geltend, alle);
      const vi = P(t, this.tVier - 0.2, 0.6, E.out); O(this.vier, vi); tr(this.vier, (1 - vi) * 40, 0);
      this.vzeilen.forEach((z, i) => { O(z.g, 0.25 + 0.75 * P(t, this.tV[i], 0.35)); const hk = P(t, this.tV[i] + 0.3, 0.4, E.back); z.hk.setAttribute('transform', `translate(1740 ${340 + i * 88}) scale(${Math.max(0.01, hk).toFixed(3)})`); O(z.hk, P(t, this.tV[i] + 0.3, 0.2)); });
      rein(this.keineQ, 1480, 205, t, this.tKeine, 0.45, this.tNach - 0.3);
      const au = fenster(t, this.tAufsicht - 0.1, 0.5, this.tNach - 0.3, 0.4); O(this.aufsicht, au);
      [this.wE, this.wD].forEach((p, i) => tr(p, 1430 + i * 210, 790, 1 + 0.12 * puls(t, this.tErteilt + i * 0.5, 0.8, 9)));
      // Zeitachse: zuerst steht „gilt ab“ vorn, bei „nach der Einweisung“ wandert sie hinter die Einweisung
      const ach = P(t, this.tNach - 0.3, 0.5); O(this.achse, ach);
      const tausch = P(t, this.tNach + 0.3, 0.9, E.io);
      tr(this.mGelt, lerp(1300, 1660, tausch), 808 + Math.sin(Math.PI * tausch) * -50); tr(this.mEinw, lerp(1660, 1300, tausch), 808 + Math.sin(Math.PI * tausch) * 50);
      zeichne(this.pfeil, P(t, this.tNach + 1.2, 0.5));
      rein(this.niemand, 1480, 915, t, this.tNiemand, 0.45);
    }
    // ---------- Einweisung ----------
    if (this.bE.vis) {
      kamera(this.bE, [960, 560], 1);
      this.zuh.forEach((f, i) => pose(f, i === 1 ? -20 * P(t, this.tDabei, 0.3) : 0, 0, 3 * Math.sin(t * 1.1 + i) + 6));
      arme(this.lehr, -6, 0, -6, 0, 3 * Math.sin(t * 0.9 + 2) + 4);
      const zeig = 0.5 + 0.5 * Math.sin(t * 1.4);
      arme(this.trainer, -6, 0, -(40 + 30 * zeig), -50, -4);
      stelle(this.trainer, 1290, 862, 0.95, true);
      this.flipZ.forEach((z, i) => O(z, P(t, this.tS4 + 0.6 + i * 0.25, 0.3)));
      const ni = P(t, this.tNachweis - 0.2, 0.7, E.out); tr(this.nw, 1590, 560 + (1 - ni) * 40, 1, 1.5); O(this.nw, ni);
      this.nwBar[0].forEach((b) => b.setAttribute('width', (220 * P(t, this.tDatum, 0.5)).toFixed(1)));
      this.nwBar[1].forEach((b, i) => b.setAttribute('width', ((i ? 180 : 280) * P(t, this.tInhalte + 0.1 + i * 0.2, 0.5)).toFixed(1)));
      this.nwHaken.forEach((kk, i) => { const hk = P(t, this.tDabei + 0.1 + i * 0.18, 0.3, E.back); kk.haken.setAttribute('transform', `scale(${Math.max(0.01, hk).toFixed(3)})`); O(kk.haken, P(t, this.tDabei + 0.1 + i * 0.18, 0.15)); });
    }
    // ---------- Artikel 4 und Kommission ----------
    if (this.bK.vis) {
      kamera(this.bK, [960, 540], 1);
      const linksAus = P(t, this.tFK - 0.2, 0.6);
      const lo = 1 - 0.65 * linksAus;
      O(this.art, P(t, this.tF4, 0.5) * lo); tr(this.art, 0, (1 - P(t, this.tF4, 0.5, E.out)) * 20);
      rein(this.anb, 330, 470, t, this.tAnb, 0.4); rein(this.bet, 330, 545, t, this.tAnb + 0.4, 0.4);
      O(this.anb, P(t, this.tAnb, 0.4) * lo); O(this.bet, P(t, this.tAnb + 0.4, 0.4) * lo);
      this.stufen.forEach((s, i) => { const k = P(t, this.tMass + i * 0.2, 0.4, E.back); sk(s, 612 + i * 110, 700, Math.max(0.01, k)); O(s, P(t, this.tMass + i * 0.2, 0.2) * lo); });
      O(this.massLab, P(t, this.tMass + 0.3, 0.4) * lo);
      const hb = 170 * P(t, this.tKomp, 1.6, E.out);
      this.balken.setAttribute('height', hb.toFixed(1)); this.balken.setAttribute('y', (694 - hb).toFixed(1));
      O(this.balken, lo); O(this.balkenRahmen, P(t, this.tKomp - 0.3, 0.3) * lo); O(this.kompLab, P(t, this.tKomp, 0.4) * lo);
      O(this.niveau, P(t, this.tNiveau, 0.4) * lo); this.niveau.setAttribute('stroke-dashoffset', (-t * 14).toFixed(1));
      rein(this.niveauP, 970, 384, t, this.tNiveau + 0.2, 0.45); O(this.niveauP, P(t, this.tNiveau + 0.2, 0.45) * lo);
      O(this.zeit, P(t, this.tSeit - 0.3, 0.4) * lo); O(this.d1, P(t, this.tSeit, 0.4)); O(this.d2, P(t, this.tWort - 0.6, 0.4));
      O(this.kom, P(t, this.tFK, 0.5)); tr(this.kom, 0, (1 - P(t, this.tFK, 0.5, E.out)) * 20);
      const zi = P(t, this.tZert - 0.2, 0.5, E.out); tr(this.zert, 1330, 540, 1, -3); O(this.zert, zi * (1 - 0.5 * P(t, this.tZert + 0.6, 0.4)));
      pop(this.zertX, 1330, 540, t, this.tZert + 0.5); tr(this.zertX, 1330, 540, Math.max(0.01, P(t, this.tZert + 0.5, 0.45, E.back)));
      O(this.zertLab, P(t, this.tZert + 0.6, 0.4));
      const vi = P(t, this.tVerz - 0.2, 0.7, E.out); tr(this.verz, 1660, 560 + (1 - vi) * 40, 1, 2); O(this.verz, vi);
      rein(this.leit, 1500, 790, t, this.tLeit, 0.5);
    }
    // ---------- Rhythmus ----------
    if (this.bL.vis) {
      kamera(this.bL, [960, 540], 1);
      this.monate.forEach((m, i) => O(m, P(t, this.tLU + i * 0.05, 0.3)));
      O(this.wieOft, P(t, this.tLU, 0.4));
      const fr = 1 - P(t, this.tRhythmus + 0.6, 0.5);
      this.fragen.forEach((f, i) => { const k = P(t, this.tLU + 0.5 + i * 0.15, 0.4, E.back); f.setAttribute('transform', `translate(${348 + [1, 4, 6, 9, 11][i] * 112} ${450 + Math.sin(t * 2 + i) * 5}) scale(${Math.max(0.01, k).toFixed(3)})`); O(f, P(t, this.tLU + 0.5 + i * 0.15, 0.2) * fr); });
      O(this.aufb, P(t, this.tAufb, 0.5) * (1 - 0.6 * P(t, this.tRhythmus, 0.5)));
      rein(this.keineQP, 1460, 330, t, this.tKeineQ, 0.45);
      rein(this.betr, 500, 760, t, this.tRhythmus, 0.5); tr(this.betr, 500, 780 + (1 - P(t, this.tRhythmus, 0.5, E.out)) * 20);
      this.takt.forEach((k, i) => { const kk = P(t, this.tRhythmus + 0.7 + i * 0.3, 0.4, E.back); k.setAttribute('transform', `translate(${348 + [2, 8][i] * 112} 555) scale(${Math.max(0.01, kk).toFixed(3)})`); O(k, P(t, this.tRhythmus + 0.7 + i * 0.3, 0.2)); });
    }
  },
});
