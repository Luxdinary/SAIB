// Teil 7 · Freies Memo und Toolkit, Scutoria und KI-Hinweis (Fassung 2: vom Anfang hierher verschoben), Endbild. Danach 20 Sekunden ruhiges Endbild.
// Preise wie im freigegebenen Skript (199 Euro im Jahr, die ersten zehn Käufer 99). Rechts im Endbild bleibt Platz für zwei
// Endscreen-Elemente, die YouTube im Studio setzt (wie ASSETS/endscreen-de.html).
NACHLAUF = 20;
akt({
  name: 'schluss',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    const K = { de: '7 · FREIES MEMO UND TOOLKIT', en: '7 · FREE MEMO AND TOOLKIT' };
    this.tErst = c('Für den ersten Schritt', 'For the first step');
    this.tFrei = c('Das Memo ist frei', 'the memo is free');
    this.tLink = c('der Link steht', 'the link is');
    this.tSieben = c('Sieben Fragen|7 Fragen', 'Seven questions|7 questions');
    this.tDat = c('datiertes Memo', 'dated memo');
    this.tL = [c('Ihre Lage', 'your situation'), c('der eine Schritt', 'the one step'), c('der Plan in Reihenfolge', 'the plan in order'), c('jede Aussage mit Quelle', 'every statement with its source')];
    this.tHier = c('Sie lesen es hier', 'You read it here');
    this.tPDF = c('das PDF kommt', 'the PDF comes');
    this.tGesp = c('nichts gespeichert', 'nothing is stored');
    this.tAdr = c('in der Adresse', 'in the address');
    this.tDok = c('Wenn Sie die Dokumente', 'If you want the documents');
    this.t34 = c('vierunddreißig Fragen|34 Fragen', 'thirty-four questions|34 questions|thirty four questions');
    this.tVorb = c('mit dem Beispielbetrieb', 'with the example business');
    this.t7 = c('sieben datierte Dokumente|7 datierte Dokumente', 'seven dated documents|7 dated documents');
    this.tNutz = c('Nutzungsrichtlinie', 'usage policy');
    this.tEine = c('einen Seite zum Aushängen', 'one page to post');
    this.tPlan = c('Plan der Inkraftsetzung', 'enactment plan');
    this.tNw = c('der Nachweisseite', 'evidence summary');
    this.tFmt = c('als PDF', 'as PDF');
    this.tHB = c('Das Handbuch mit jeder Quelle', 'The handbook with every source');
    this.tVorKauf = c('vor dem Kauf', 'before you buy');
    this.tPreis = c('Das Toolkit kostet', 'The toolkit costs');
    this.tZehn = c('Die ersten zehn|Die ersten 10', 'The first ten|The first 10');
    this.z = { scut: c('Hier ist Scutoria|Hier ist', 'This is Scutoria|This is'), stimme: c('Die Stimme, die Sie hören', 'The voice you hear'), synth: c('synthetisch', 'synthetic'),
      skript: c('Das Skript', 'The script'), entw: c('entworfen', 'drafted'), pruef: c('von uns Satz', 'checked by us'), zahl: c('Jede Zahl', 'Every number'),
      recht: c('Rechtsaussage', 'legal statement'), quelle: c('ihre Quelle', 'its source'), qb: c('Quellenbasiert', 'Source-based|Source based'), keine: c('keine Rechtsberatung', 'no legal advice') };
    this.tNaechst = c('Als Nächstes', 'Next');
    this.tEhrlich = c('ehrlich antworten', 'answer it honestly');
    this.tStill = stilleVor(DAUER + 1);

    // ---------- 1 freies Memo ----------
    const b1 = buehne('schluss-memo', { seed: 1 }); this.b1 = b1;
    const c1 = b1.cam;
    this.memo = bauMemo(c1);
    this.frei = pille(c1, { de: 'Frei · PDF per E-Mail', en: 'Free · PDF by email' }, { icon: 'mail', col: C.blue, size: 26 });
    this.web = g(c1);
    { const z = g(this.web, { transform: 'translate(1040 300)' }); zeichen(z, 56, C.blue, 1.8); }
    T(this.web, 1084, 316, 'scutoria.com', { size: 44, weight: 800 });
    this.link = pille(c1, { de: 'Link in der Beschreibung', en: 'Link in the description' }, { icon: 'link', col: C.muted, size: 22 });
    this.inhalt = g(c1);
    T(this.inhalt, 1010, 436, { de: 'Sieben Fragen, dann ein datiertes Memo', en: 'Seven questions, then a dated memo' }, { size: 28, weight: 800 });
    const IN = [['building', { de: 'Ihre Lage', en: 'your situation' }], ['spark', { de: 'der eine Schritt zuerst', en: 'the one step first' }], ['list', { de: 'der Plan in Reihenfolge', en: 'the plan in order' }], ['book', { de: 'jede Aussage mit Quelle', en: 'every statement with its source' }]];
    this.inz = IN.map(([ic, txt], i) => { const gr = g(this.inhalt); const y = 500 + i * 62; el('circle', { cx: 1036, cy: y, r: 24, fill: C.raised, stroke: C.blue, 'stroke-width': 2 }, gr); ikon(gr, ic, 1036, y, 28, C.ink); T(gr, 1076, y + 9, txt, { size: 26, weight: 700 }); return gr; });
    this.adr = g(c1);
    karte(this.adr, 1000, 780, 820, 72, { fill: C.surface, stroke: C.edge, rx: 36 });
    { const ic = g(this.adr, { transform: 'translate(1042 816)' }); iconGlobe(ic, 30, C.muted); }
    const at = T(this.adr, 1072, 826, { de: 'scutoria.com/de/memos/wo-anfangen', en: 'scutoria.com/memos/where-to-start' }, { mono: 1, size: 22, fill: C.ink });
    this.adrQ = g(this.adr); const qx = 1072 + breite(at) + 8;
    el('rect', { x: qx - 4, y: 798, width: 120, height: 38, rx: 8, fill: 'rgba(79,140,255,0.18)', stroke: C.blue, 'stroke-width': 2 }, this.adrQ);
    T(this.adrQ, qx + 56, 826, '?…', { mono: 1, size: 22, fill: C.blue, anchor: 'middle' });
    this.adrLab = pille(c1, { de: 'Antworten nur in der Adresse · nichts gespeichert', en: 'answers only in the address · nothing stored' }, { col: C.blue, size: 20 });
    shot(b1, this.tErst - 0.6, { typ: 'schwarz', d: 1.0 });

    // ---------- 2 Toolkit ----------
    const b2 = buehne('schluss-toolkit', { seed: 127, regalDeckkraft: 0.6 }); this.b2 = b2;
    const c2 = b2.cam;
    this.form = g(c2);
    karte(this.form, 120, 300, 440, 280, { fill: C.surface, stroke: C.edge });
    T(this.form, 156, 352, { de: 'GENERATOR', en: 'GENERATOR' }, { mono: 1, size: 18, fill: C.muted, ls: '0.1em' });
    this.f34 = T(this.form, 156, 440, '34', { size: 84, weight: 800, fill: C.blue });
    T(this.form, 300, 440, { de: 'Fragen', en: 'questions' }, { size: 34, weight: 800 });
    this.vorb = pille(this.form, { de: 'Beispielbetrieb vorbelegt', en: 'example business prefilled' }, { icon: 'check', col: C.blue, size: 20 }); tr(this.vorb, 340, 520);
    this.pfeil = el('path', { d: 'M 580 440 C 640 440 650 450 700 450', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round' }, c2);
    this.docs = Array.from({ length: 7 }, (_, i) => { const gr = g(c2); el('rect', { x: -70, y: -95, width: 140, height: 190, rx: 5, fill: C.paper, filter: 'url(#shadowS)' }, gr); T(gr, -50, -64, 'D' + (i + 1), { mono: 1, size: 18, fill: C.blueDeep }); linien(gr, -50, -40, 100, 6, 20, C.pBar2, 7); return gr; });
    this.dLab = [[{ de: 'Nutzungsrichtlinie', en: 'Usage policy' }, 0], [{ de: 'eine Seite zum Aushängen', en: 'one page to post' }, 1], [{ de: 'Plan der Inkraftsetzung · 15 Schritte', en: 'Enactment plan · 15 steps' }, 2], [{ de: 'Nachweisseite', en: 'Evidence summary' }, 3]].map(([txt]) => pille(c2, txt, { icon: 'doc', col: C.blue, size: 22 }));
    { const w = this.dLab.map((p) => p.w); const r1 = w[0] + w[1] + 24, r2 = w[2] + w[3] + 24; this.dPos = [[880 - r1 / 2 + w[0] / 2, 690], [880 + r1 / 2 - w[1] / 2, 690], [880 - r2 / 2 + w[2] / 2, 752], [880 + r2 / 2 - w[3] / 2, 752]]; }
    this.fmt = ['PDF', 'DOCX', 'XLSX'].map((f) => pille(c2, f, { col: C.muted, size: 22 }));
    this.hb = g(c2, { transform: 'translate(1600 330)' }); el('circle', { r: 90, fill: 'url(#gPaper)' }, this.hb); iconBook(this.hb, 90, C.ink);
    this.hbLab = pille(c2, { de: 'Handbuch vor dem Kauf lesbar', en: 'Handbook readable before you buy' }, { icon: 'search', col: C.blue, size: 22 });
    this.preis = g(c2);
    karte(this.preis, 1380, 600, 440, 250, { fill: C.surface, stroke: C.blue });
    T(this.preis, 1414, 650, { de: 'KI-RICHTLINIEN-TOOLKIT', en: 'AI POLICY TOOLKIT' }, { mono: 1, size: 18, fill: C.muted, ls: '0.1em' });
    T(this.preis, 1412, 740, '199 €', { size: 76, weight: 800 });
    T(this.preis, 1640, 740, { de: 'im Jahr', en: 'per year' }, { mono: 1, size: 22, fill: C.muted });
    this.gruender = g(this.preis);
    el('rect', { x: 1412, y: 770, width: 370, height: 52, rx: 26, fill: C.blueSoft }, this.gruender);
    T(this.gruender, 1436, 805, { de: 'die ersten zehn Käufer: 99 €', en: 'the first ten buyers: 99 €' }, { mono: 1, size: 20, fill: C.blueDeep });
    shot(b2, this.tDok - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 3 Scutoria und KI-Hinweis (Fassung 2) ----------
    this.off = offenlegungsBuehne('schluss-offenlegung', this.z, { kicker: { de: 'SKRIPT · VIDEO 01', en: 'SCRIPT · VIDEO 01' }, aussage: {
      zeile: { de: 'Artikel 4 gilt seit', en: 'Article 4 has applied since' }, wert: { de: '2. Februar 2025', en: '2 February 2025' }, rahmen: { de: 'Artikel 4', en: 'Article 4' },
      quelle: { de: 'VO (EU) 2024/1689, Art. 4, Art. 113 Buchst. a · Abruf 2026-10-23', en: 'Regulation (EU) 2024/1689, Art. 4, Art. 113(a) · retrieved 2026-10-23' } } });
    this.b3 = this.off.b;
    shot(this.b3, this.z.scut - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 4 Ausblick und Endbild ----------
    const b4 = buehne('schluss-ende', { seed: 137, regalDeckkraft: 0.35 }); this.b4 = b4;
    const c4 = b4.cam;
    this.mark = g(c4); { const z = g(this.mark, { transform: 'translate(116 108)' }); zeichen(z, 40, C.blue, 1.8); } T(this.mark, 150, 118, 'SCUTORIA', { size: 26, weight: 700, ls: '0.18em' });
    this.links = g(c4);
    TB(this.links, 96, 470, { de: 'Belegt. Datiert. Vorzeigbar.', en: 'Sourced. Dated. Ready to show.' }, { size: 44, weight: 800, maxW: 560, lh: 50 });
    TB(this.links, 96, 600, { de: 'Die Memos und Tools auf scutoria.com sind frei. Die Handbücher sind vor dem Kauf lesbar.', en: 'The memos and tools on scutoria.com are free. The handbooks can be read before you buy.' }, { size: 22, weight: 600, fill: C.muted, maxW: 560, lh: 33 });
    T(this.links, 96, 720, { de: 'scutoria.com · Quellenbasiert. Keine Rechtsberatung.', en: 'scutoria.com · Source-based. No legal advice.' }, { mono: 1, size: 16, fill: C.muted });
    this.naechst = g(c4);
    T(this.naechst, 1000, 330, { de: 'ALS NÄCHSTES', en: 'NEXT' }, { mono: 1, size: 22, fill: C.blue, ls: '0.14em' });
    TB(this.naechst, 1000, 392, { de: 'Ihr Kunde schickt einen Sicherheitsfragebogen. So antworten Sie ehrlich.', en: 'Your customer sent a security questionnaire. How to answer honestly.' }, { size: 38, weight: 800, maxW: 780, lh: 46 });
    this.fb = g(this.naechst);
    const fbb = blatt(this.fb, { w: 360, h: 300, kicker: { de: 'FRAGEBOGEN', en: 'QUESTIONNAIRE' }, pad: 24, kSize: 13 });
    this.fbK = [0, 1, 2, 3].map((k) => { const y = fbb.y + 24 + k * 50; el('rect', { x: fbb.left + 44, y: y - 10, width: 200, height: 10, rx: 5, fill: C.pBar2 }, fbb.g); return kaestchen(fbb.g, fbb.left + 14, y - 5, 24); });
    tr(this.fb, 1200, 680, 1, 2);
    shot(b4, this.tNaechst - 0.5, { typ: 'blende', d: 0.8 });
    this.buehnen = [b1, b2, this.b3, b4];

    // ---------- Einblendungen ----------
    kopf(this.tErst, this.tDok - 0.3, K, { de: 'Das Memo ist frei', en: 'The memo is free' });
    kopf(this.tDok, this.z.scut - 0.3, K, { de: 'Das KI-Richtlinien-Toolkit', en: 'The AI Policy Toolkit' });
  },

  zeichnen(t) {
    if (this.b1.vis) {
      kamera(this.b1, [960, 540], 1);
      const M = this.memo; const mi = P(t, this.tErst - 0.3, 0.7, E.out);
      tr(M.g, 520, 560 + (1 - mi) * 40, 1, -2); O(M.g, mi);
      M.qRows.forEach((q, i) => O(q.sel, P(t, this.tSieben + i * 0.12, 0.2)));
      O(M.band, P(t, this.tDat, 0.4));
      rein(this.frei, 520, 950, t, this.tFrei, 0.45);
      O(this.web, P(t, this.tFrei + 0.4, 0.5)); rein(this.link, 1180, 372, t, this.tLink, 0.45, this.tSieben + 0.2);
      O(this.inhalt.firstChild, P(t, this.tSieben, 0.4));
      this.inz.forEach((z, i) => O(z, P(t, this.tL[i] - 0.1, 0.35)));
      const ai = P(t, this.tGesp - 0.4, 0.5, E.out); O(this.adr, ai); tr(this.adr, 0, (1 - ai) * 20);
      sk(this.adrQ, 0, 0, 1); O(this.adrQ, 0.5 + 0.5 * P(t, this.tAdr, 0.4));
      rein(this.adrLab, 1410, 900, t, this.tAdr + 0.2, 0.45);
    }
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      const fi = P(t, this.tDok - 0.2, 0.6, E.out); O(this.form, fi); tr(this.form, 0, (1 - fi) * 30);
      // Marke: Zahlen werden nie hochgezählt, die 34 erscheint als Ganzes
      O(this.f34, P(t, this.t34 - 0.2, 0.4));
      O(this.vorb, P(t, this.tVorb, 0.4));
      zeichne(this.pfeil, P(t, this.t7 - 0.4, 0.5));
      this.docs.forEach((d, i) => { const k = P(t, this.t7 + i * 0.1, 0.6, E.out); const a = (i - 3) * 9; const x = lerp(700, 920 + (i - 3) * 64, k), y = lerp(450, 470 + Math.abs(i - 3) * 8, k); tr(d, x, y, lerp(0.5, 1, k), a * k); O(d, P(t, this.t7 + i * 0.1, 0.2)); });
      const lz = [this.tNutz, this.tEine, this.tPlan, this.tNw];
      this.dLab.forEach((p, i) => rein(p, this.dPos[i][0], this.dPos[i][1], t, lz[i] - 0.1, 0.4));
      this.fmt.forEach((f, i) => rein(f, 750 + i * 130, 840, t, this.tFmt + i * 0.25, 0.4));
      O(this.hb, P(t, this.tHB - 0.1, 0.5)); rein(this.hbLab, 1600, 450, t, this.tVorKauf - 0.2, 0.45);
      const pi = P(t, this.tPreis - 0.2, 0.6, E.out); O(this.preis, pi); tr(this.preis, (1 - pi) * 40, 0);
      O(this.gruender, P(t, this.tZehn - 0.1, 0.4));
    }
    if (this.b3.vis) this.off.zeichnen(t);
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      O(this.mark, P(t, this.tNaechst - 0.3, 0.6)); O(this.links, P(t, this.tNaechst, 0.8));
      const ni = fenster(t, this.tNaechst + 0.2, 0.6, this.tStill + 1.2, 0.8); O(this.naechst, ni); tr(this.naechst, (1 - P(t, this.tNaechst + 0.2, 0.6, E.out)) * 30, 0);
      this.fbK.forEach((kk, i) => { const hk = P(t, this.tEhrlich + i * 0.25, 0.3, E.back); kk.haken.setAttribute('transform', `scale(${Math.max(0.01, hk).toFixed(3)})`); O(kk.haken, P(t, this.tEhrlich + i * 0.25, 0.15)); });
    }
  },
});
