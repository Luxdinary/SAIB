// Teil 7 · Freies Memo, Handbuch, Toolkit, Scutoria und KI-Hinweis, 20 Sekunden Endbild (Absätze 35 bis 38, Fassung 2).
// Bühnen: Memo „Sind wir von NIS2 betroffen?“ → Handbuch und Toolkit (47 Fragen, sieben Dokumente, Preis)
// → Offenlegung (Fassung 2: „Hier ist Scutoria …“ vom Anfang hierher verschoben, statt des bisherigen Schlusssatzes) → Ausblick und Endbild.
akt({
  name: 'verweis',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    const K = { de: '7 · FREI UND IM TOOLKIT', en: '7 · FREE AND IN THE TOOLKIT' };
    // ---------- Wortanker ----------
    const Q10 = quelle(); this.tQ10 = Q10.s;
    this.tMemo = c('Das freie Memo', 'the free memo');
    this.tFuenf = c('fünf Fragen', 'five questions');
    this.tS = [c('Sektor', 'sector'), c('Größe', 'size'), c('Sonderfällen', 'special cases')];
    this.tDatiert = c('datiertes Memo', 'dated memo');
    this.tQuelle = c('jede Aussage mit Quelle', 'every statement sourced');
    this.tSeite = c('auf der Seite', 'on the page');
    this.tPDF = c('per E-Mail', 'by email');
    this.tFrei = c('frei auf', 'free on');
    this.tLink = c('Beschreibung', 'description');
    const Q11 = quelle(); this.tQ11 = Q11.s;
    this.tVorKauf = c('vor dem Kauf', 'before you buy');
    this.t47 = c('siebenundvierzig Fragen', 'forty-seven questions|forty seven questions');
    this.tVorbel = c('vorbelegtem Beispielbetrieb', 'example business prefilled');
    this.t7 = c('sieben datierte Dokumente', 'seven dated documents');
    this.tD = [c('die Selbstauskunft', 'the self-declaration'), c('den Maßnahmenplan', 'the action plan'), c('die Notfallkarte', 'the emergency card'), c('die Nachweisliste', 'the evidence list'),
      c('das Antwortschreiben', 'the cover letter'), c('Klausel-Prüfliste|Klausel Prüfliste|Klauselprüfliste', 'clause checklist'), c('die Nachweisseite', 'the evidence summary')];
    this.tPreis = c('Das Toolkit kostet', 'The toolkit costs');
    this.tErste = c('Die ersten zehn', 'The first ten');
    this.z = { scut: c('Hier ist Scutoria|Hier ist', 'This is Scutoria|This is'), stimme: c('Die Stimme, die Sie hören', 'The voice you hear'), synth: c('synthetisch', 'synthetic'),
      skript: c('Das Skript', 'The script'), entw: c('entworfen', 'drafted'), pruef: c('von uns Satz', 'checked by us'), zahl: c('Jede Zahl', 'Every number'),
      recht: c('Rechtsaussage', 'legal statement'), quelle: c('ihre Quelle', 'its source'), qb: c('Quellenbasiert', 'Source-based|Source based'), keine: c('keine Rechtsberatung', 'no legal advice') };
    this.tNaechst = c('Als Nächstes', 'Next on this channel');
    this.tRund = c('was nie in ein', 'what never goes into');   // Ausblick der Langfassung: Video 04 statt „Rundgang“
    this.tGen = c('fünf Datenarten', 'five kinds of data');
    this.tMarker = c('Zweifelsregel', 'rule of doubt');
    this.tOrdner = this.tMarker;   // letzter Anker des Ausblicks
    const letzt = WORT.length ? WORT[WORT.length - 1].e : DAUER;
    this.tEndbild = Math.max(this.tOrdner + 1.6, letzt + 0.8);
    NACHLAUF = Math.max(0, this.tEndbild + 20 - DAUER); // 20 Sekunden ruhiges Endbild nach dem letzten Wort

    // ---------- Bühne 1: freies Memo ----------
    const b1 = buehne('verweis-memo', { seed: 109, regalDeckkraft: 0.55 }); this.b1 = b1;
    const k1 = b1.cam;
    this.memo = g(k1);
    { const m = blatt(this.memo, { w: 500, h: 640, kicker: { de: 'MEMO · SCUTORIA', en: 'MEMO · SCUTORIA' }, kSize: 15, pad: 36, titel: { de: 'Sind wir von NIS2 betroffen?', en: 'Does NIS2 apply to us?' }, tSize: 36 });
      this.mZeilen = [0, 1, 2, 3, 4].map((i) => { const y = m.y + 20 + i * 52, zg = g(m.g); T(zg, m.left, y + 6, String(i + 1), { mono: 1, size: 18, fill: C.pMuted }); el('rect', { x: m.left + 30, y: y - 5, width: 190 + ((i * 41) % 80), height: 11, rx: 5.5, fill: C.pBar }, zg); for (let j = 0; j < 2; j++) el('circle', { cx: m.right - 50 + j * 34, cy: y, r: 9, fill: 'none', stroke: '#aab3c2', 'stroke-width': 2 }, zg); el('circle', { cx: m.right - 50 + (i % 2) * 34, cy: y, r: 9.5, fill: C.pInk }, zg); return zg; });
      this.mQuellen = [0, 1, 2].map((i) => { const zg = g(m.g); const y = m.y + 300 + i * 40; el('rect', { x: m.left, y: y - 9, width: 14, height: 14, fill: C.blue }, zg); el('rect', { x: m.left + 26, y: y - 6, width: 280 - i * 40, height: 9, rx: 4.5, fill: C.pBar2 }, zg); return zg; });
      this.mDatum = T(m.g, m.right, m.y0 + 46, { de: 'DATIERT', en: 'DATED' }, { mono: 1, size: 15, fill: C.blueDeep, anchor: 'end', ls: '0.08em' }); }
    this.mThemen = [{ de: 'Sektor', en: 'Sector' }, { de: 'Größe', en: 'Size' }, { de: 'Sonderfälle', en: 'Special cases' }].map((w0) => pille(k1, w0, { col: C.blue, size: 26 }));
    this.mSeite = pille(k1, { de: 'auf der Seite lesen', en: 'read on the page' }, { icon: 'globe', col: C.blue, size: 26 });
    this.mMail = g(k1); { el('circle', { r: 64, fill: 'url(#gBlue)' }, this.mMail); iconMail(this.mMail, 90, C.ink); T(this.mMail, 0, 74, 'PDF', { mono: 1, size: 22, fill: C.muted, anchor: 'middle' }); }
    this.mFrei = pille(k1, { de: 'frei · scutoria.com/de/memos/nis2', en: 'free · scutoria.com/memos/nis2' }, { icon: 'link', col: C.blue, size: 26 });
    this.mLink = pille(k1, { de: 'Link in der Beschreibung', en: 'link in the description' }, { col: C.muted, size: 22 });
    shot(b1, this.tQ10 - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne 2: Handbuch und Toolkit ----------
    const b2 = buehne('verweis-toolkit', { seed: 113, regalDeckkraft: 0.5 }); this.b2 = b2;
    const k2 = b2.cam;
    this.hb = g(k2); { el('circle', { r: 120, fill: 'url(#gPaper)' }, this.hb); const bb = blatt(this.hb, { w: 240, h: 320, kicker: { de: 'HANDBUCH', en: 'HANDBOOK' }, kSize: 13, pad: 22 }); linien(bb.g, bb.left, bb.y + 8, 190, 8, 28, C.pBar, 9); }
    this.hbP = pille(k2, { de: 'vor dem Kauf lesbar', en: 'readable before you buy' }, { icon: 'book', col: C.blue, size: 24 });
    this.gen = g(k2);
    karte(this.gen, -170, -120, 340, 240, { fill: C.surface });
    T(this.gen, 0, -60, { de: 'GENERATOR', en: 'GENERATOR' }, { mono: 1, size: 18, fill: C.blue, anchor: 'middle', ls: '0.12em' });
    this.gen47 = T(this.gen, 0, 10, { de: '47 Fragen', en: '47 questions' }, { size: 44, weight: 800, anchor: 'middle' });
    this.genBalken = el('rect', { x: -130, y: 40, width: 260, height: 12, rx: 6, fill: C.blue }, this.gen);
    el('rect', { x: -130, y: 40, width: 260, height: 12, rx: 6, fill: 'none', stroke: C.line, 'stroke-width': 2 }, this.gen);
    this.genVor = T(this.gen, 0, 92, { de: 'Beispielbetrieb vorbelegt', en: 'example business prefilled' }, { mono: 1, size: 17, fill: C.muted, anchor: 'middle' });
    const DOKS = [{ de: 'Selbstauskunft', en: 'Self-declaration' }, { de: 'Maßnahmenplan', en: 'Action plan' }, { de: 'Notfallkarte', en: 'Emergency card' }, { de: 'Nachweisliste', en: 'Evidence list' },
      { de: 'Antwortschreiben mit Abgleich', en: 'Cover letter with mapping' }, { de: 'Klausel-Prüfliste', en: 'Clause checklist' }, { de: 'Nachweisseite', en: 'Evidence summary' }];
    this.doks = DOKS.map((n, i) => { const gr = g(k2); const b = blatt(gr, { w: 200, h: 250, pad: 18, back: false }); T(b.g, b.left, b.y0 + 40, 'D' + (i + 1), { mono: 1, size: 22, fill: C.blueDeep }); TB(b.g, b.left, b.y0 + 84, n, { size: 21, weight: 800, fill: C.pInk, maxW: 164, lh: 25 }); linien(b.g, b.left, b.y0 + 160, 150, 3, 22, C.pBar, 8); return gr; });
    this.preis = g(k2); { el('rect', { x: -420, y: -34, width: 840, height: 68, rx: 34, fill: C.surface, stroke: C.edge, 'stroke-width': 2 }, this.preis); this.preisT = T(this.preis, 0, 9, '', { mono: 1, size: 26, fill: C.ink, anchor: 'middle', ls: '0.04em' }); }
    shot(b2, this.tQ11 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 3: Scutoria und KI-Hinweis (Fassung 2) ----------
    this.off = offenlegungsBuehne('verweis-offenlegung', this.z, { kicker: { de: 'SKRIPT · VIDEO 02', en: 'SCRIPT · VIDEO 02' }, aussage: {
      zeile: { de: 'Art. 32 Abs. 1 Buchst. c', en: 'Art. 32(1)(‌c) GDPR' }, wert: { de: 'rasch wiederherstellen', en: 'timely restore' }, rahmen: { de: 'Art. 32', en: 'Art. 32(1)(‌c)' }, // ‌: Manrope setzt „(c)“ sonst als ©
      quelle: { de: 'Verordnung (EU) 2016/679, Art. 32 Abs. 1 Buchst. a bis d · EUR-Lex · abgerufen 23.10.2026', en: 'Regulation (EU) 2016/679, Art. 32(1)(a) to (d) · EUR-Lex · retrieved 2026-10-23' } } });
    this.b3 = this.off.b;
    shot(this.b3, this.z.scut - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 4: Ausblick und Endbild ----------
    const b4 = buehne('verweis-ende', { seed: 7, regalDeckkraft: 0.4, licht: 0.6 }); this.b4 = b4;
    const k4 = b4.cam;
    this.next = g(k4);
    karte(this.next, -380, -200, 760, 400, { fill: C.surface });
    T(this.next, -340, -140, { de: 'ALS NÄCHSTES · VIDEO 04', en: 'NEXT · VIDEO 04' }, { mono: 1, size: 22, fill: C.blue, ls: '0.12em' });
    TB(this.next, -340, -80, { de: 'Was nie in ein KI-Tool darf', en: 'What never goes into an AI tool' }, { size: 44, weight: 800, maxW: 680, lh: 52 });
    this.nextIc = [['key', { de: 'was nie hinein darf', en: 'never goes in' }], ['id', { de: 'fünf Datenarten', en: 'five kinds of data' }], ['question', { de: 'Zweifelsregel', en: 'rule of doubt' }]].map(([ic, w0], i) => {
      const gr = g(this.next, { transform: `translate(${-240 + i * 240} 110)` });
      if (ic) ikon(gr, ic, 0, -14, 56, C.blue); else ['fakt', 'auslegung', 'unsicher', 'luecke'].forEach((m, j) => markerShape(g(gr, { transform: `translate(${-42 + j * 28} -14)` }), m, 22));
      T(gr, 0, 46, w0, { size: 24, weight: 700, anchor: 'middle', fill: C.muted }); return gr;
    });
    this.endG = g(k4);
    { const z = g(this.endG, { transform: 'translate(960 300)' }); zeichen(z, 72, C.blue, 1.6); T(this.endG, 960, 392, 'Scutoria', { size: 48, weight: 800, anchor: 'middle' });
      el('rect', { x: 340, y: 470, width: 560, height: 315, rx: 14, fill: 'none', stroke: 'rgba(226,232,246,0.10)', 'stroke-width': 2 }, this.endG);
      el('circle', { cx: 1300, cy: 628, r: 120, fill: 'none', stroke: 'rgba(226,232,246,0.10)', 'stroke-width': 2 }, this.endG); }
    shot(b4, this.tNaechst - 0.4, { typ: 'blende', d: 0.8 });
    this.buehnen = [b1, b2, this.b3, b4];

    // ---------- Einblendungen ----------
    kopf(this.tQ10, this.tQ11 - 0.3, K, { de: 'Das freie Memo', en: 'The free memo' });
    kopf(this.tQ11, this.z.scut - 0.3, K, { de: 'Handbuch und Toolkit', en: 'Handbook and toolkit' });
    kopf(this.tNaechst, this.tEndbild - 0.4, { de: 'ALS NÄCHSTES', en: 'NEXT' }, '');
  },

  zeichnen(t) {
    // ---------- Bühne 1 ----------
    if (this.b1.vis) {
      kamera(this.b1, [960, 540], 1);
      const mk = P(t, this.tMemo - 0.2, 0.7, E.out); tr(this.memo, 620, 560 + (1 - mk) * 24, 1, -1.5); O(this.memo, mk);
      this.mZeilen.forEach((z, i) => O(z, 0.2 + 0.8 * P(t, this.tFuenf + i * 0.15, 0.3)));
      this.mThemen.forEach((p, i) => { tr(p, 1200, 320 + i * 80, Math.max(0.01, P(t, this.tS[i] - 0.1, 0.45, E.back))); O(p, P(t, this.tS[i] - 0.1, 0.2) * (1 - P(t, this.tSeite - 0.3, 0.4))); });
      O(this.mDatum, P(t, this.tDatiert, 0.4)); this.mQuellen.forEach((q, i) => O(q, 0.15 + 0.85 * P(t, this.tQuelle + i * 0.2, 0.3)));
      tr(this.mSeite, 1300, 360, Math.max(0.01, P(t, this.tSeite, 0.45, E.back))); O(this.mSeite, P(t, this.tSeite, 0.2));
      const fk = P(t, this.tPDF - 0.3, 1.1, E.io); const fp = bogen([700, 520], [1300, 520], fk, 120);
      tr(this.mMail, fp[0], fp[1], 1); O(this.mMail, P(t, this.tPDF - 0.3, 0.2));
      tr(this.mFrei, 1300, 700, Math.max(0.01, P(t, this.tFrei, 0.45, E.back))); O(this.mFrei, P(t, this.tFrei, 0.2));
      tr(this.mLink, 1300, 790, Math.max(0.01, P(t, this.tLink, 0.45, E.back))); O(this.mLink, P(t, this.tLink, 0.2));
    }
    // ---------- Bühne 2 ----------
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      const doks = P(t, this.t7 - 0.3, 0.8, E.io);
      const hk = P(t, this.tQ11, 0.6, E.out); tr(this.hb, lerp(560, 300, doks), lerp(500, 380, doks), lerp(1, 0.7, doks), -3); O(this.hb, hk);
      tr(this.hbP, lerp(560, 300, doks), lerp(720, 560, doks), Math.max(0.01, P(t, this.tVorKauf - 0.2, 0.45, E.back))); O(this.hbP, P(t, this.tVorKauf - 0.2, 0.2));
      const gk = P(t, this.t47 - 0.3, 0.6, E.out); tr(this.gen, lerp(1300, 960, doks), lerp(500, 330, doks), lerp(1, 0.8, doks)); O(this.gen, gk);
      this.genBalken.setAttribute('width', (260 * P(t, this.t47, 1.6, E.out)).toFixed(1)); O(this.genVor, P(t, this.tVorbel, 0.4));
      this.doks.forEach((d, i) => { const t0 = this.tD[i] - 0.15, k = P(t, t0, 0.5, E.out); const x = 240 + i * 240, y = 700; tr(d, lerp(960, x, k), lerp(380, y, k), lerp(0.3, 0.92, k), (i - 3) * 1.6 * k); O(d, P(t, t0, 0.2)); });
      const pk = P(t, this.tPreis, 0.5, E.out); tr(this.preis, 960, 860 + (1 - pk) * 10, 1); O(this.preis, pk);
      setText(this.preisT, t < this.tErste ? { de: '199 Euro im Jahr', en: '199 euros per year' } : { de: '199 Euro im Jahr · die ersten zehn Käufer: 99 Euro', en: '199 euros per year · the first ten buyers: 99 euros' });
    }
    // ---------- Bühne 3 ----------
    if (this.b3.vis) this.off.zeichnen(t);
    // ---------- Bühne 4 ----------
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      const ende = P(t, this.tEndbild, 1.0, E.io);
      const nk = P(t, this.tNaechst, 0.6, E.out); tr(this.next, 960, 560 + (1 - nk) * 24 - ende * 30, 1); O(this.next, nk * (1 - ende));
      [this.tRund, this.tGen, this.tMarker].forEach((tt, i) => { const kk = P(t, tt - 0.1, 0.45, E.back); this.nextIc[i].setAttribute('transform', `translate(${-240 + i * 240} 110) scale(${Math.max(0.01, kk).toFixed(3)})`); O(this.nextIc[i], P(t, tt - 0.1, 0.2)); });
      O(this.endG, P(t, this.tEndbild + 0.4, 1.0));
    }
  },
});
