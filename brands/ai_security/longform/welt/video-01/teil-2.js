// Teil 2 · Die Lage im kleinen Betrieb. Absätze 2 bis 8 des Skripts.
// Bühnen: Stadt bei Nacht → Büro (ein Tool breitet sich aus, niemand entscheidet) → Memo-Frage mit drei Antworten →
// drei Folgen → Geschäftsgeheimnis (Fakt) → Personenbezug aus dem Zusammenhang (Fakt) → Papier in der Schublade (Auslegung) → womit anfangen.
akt({
  name: 'lage',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o);
    const K = { de: '1 · DIE LAGE IM KLEINEN BETRIEB', en: '1 · THE SITUATION IN A SMALL BUSINESS' };
    // ---------- Wortanker in Sprechreihenfolge ----------
    this.tLage = c('Nehmen Sie eine typische', 'Take a typical').s;
    this.tOhneIT = c('ohne IT-Abteilung', 'without an IT department').s;
    this.tEU = c('irgendwo in der EU', 'somewhere in the EU').s;
    this.tJemand = c('Jemand im Büro', 'Somebody in the office').s;
    this.tText = c('Textassistenten', 'text assistant').s;
    this.tAngebot = c('ein Angebot', 'a quote').s;
    this.tFunkt = c('Es funktioniert', 'It works').s;
    this.tNaechste = c('die nächste Person', 'the next person').s;
    this.tNiemand = c('Entschieden hat das niemand', 'Nobody decided it').s;
    this.tMemo = c('Das freie Start-Memo|Das freie Startmemo', 'The free start memo').s;
    this.tDrei = c('drei Antworten', 'three answers').s;
    this.tA1 = c('Ja, mit betrieblichen', 'Yes, with business').s;
    this.tA2 = c('Ja, mit privaten', 'Yes, with private').s;
    this.tA3 = c('Nein, soweit', 'No, as far').s;
    this.tMitte = c('mittlere Antwort', 'middle answer').s;
    this.tRegeln = c('Schriftliche Regeln', 'Written rules').s;
    this.tMail = c('eine E-Mail', 'an email').s;
    this.tEinw = c('Einweisung', 'A briefing').s;
    this.tOhneN = c('ohne Nachweis', 'without a record').s;
    this.tFolgen = c('Daraus folgen drei', 'Three things follow').s;
    this.tTast = c('an der Tastatur', 'at the keyboard').s;
    this.tNichtB = c('nicht vom Betrieb', 'not by the business').s;
    this.tSchief = c('Wenn etwas schiefgeht', 'If something goes wrong').s;
    this.tRegelWar = c('was die Regel war', 'what the rule was').s;
    this.tKunde = c('ein Kunde', 'a customer').s;
    this.tVers = c('ein Versicherer', 'an insurer').s;
    this.tBeleg = c('die eigene Belegschaft', 'your own staff').s;
    this.tNichts = c('nichts zu zeigen', 'nothing to show').s;
    const G = belegt(); this.tG = G.s; this.tGe = G.e;
    this.tRL = c('Geschäftsgeheimnis-Richtlinie|Geschäftsgeheimnisrichtlinie', 'Trade Secrets Directive').s;
    this.tBed = c('drei Bedingungen', 'three conditions').s;
    this.tDritte = c('die dritte', 'the third').s;
    this.tAngem = c('angemessener', 'reasonable steps').s;
    this.tAT = c('Österreich und Deutschland', 'Austria and Germany').s;
    const D = belegt(); this.tD = D.s; this.tDe = D.e;
    this.tNamen = c('Namen und Anschriften', 'removing names').s;
    this.tReicht = c('reicht regelmäßig nicht', 'regularly not enough').s;
    this.tZus = c('aus dem Zusammenhang', 'from the context').s;
    const A = belegt(); this.tA = A.s; this.tAe = A.e;
    this.tAusl = c('Unsere Auslegung', 'Our interpretation').s;
    this.tDok = c('dokumentiert', 'documented').s;
    this.tErteilt = c('nie erteilt', 'never issued').s;
    this.tZurueck = c('Darauf kommen wir', 'We come back').s;
    this.tWomit = c('Womit also anfangen', 'So where do you start').s;
    this.tLaengst = c('längsten Dokument', 'longest document').s;
    this.tEnde = cue({ de: 'Das freie Memo stellt', en: 'The free memo asks' }, { halten: true }).s;
    // Ton (Langfassung 03.11.2026)
    klang(this.tText, 'keys_typing', { dauer: 1.6, laut: 0.5 }); klang(this.tFunkt, 'click_soft'); klang(this.tNiemand, 'tick');
    [this.tA1, this.tA2, this.tA3].forEach((t) => klang(t, 'pop', { laut: 0.6 })); klang(this.tMail, 'paper_slide');
    [this.tKunde, this.tVers, this.tBeleg].forEach((t) => klang(t, 'pop', { laut: 0.5 })); klang(this.tNichts, 'thud_low', { laut: 0.6 });
    klang(this.tDok, 'paper_slide', { laut: 0.6 }); klang(this.tErteilt, 'stamp_soft'); klang(this.tLaengst, 'paper_slide', { laut: 0.6 });

    // ---------- 1 Stadt ----------
    const b1 = buehne('lage-stadt', { seed: 11, regalDeckkraft: 0.35 }); this.b1 = b1;
    this.S = bauStadt(b1.cam);
    this.fensterAn = this.S.haeuser.map((h, i) => h.fs.map((f, j) => ((i * 7 + j * 13) % 10) / 10));
    const u = this.S.haeuser[this.S.unser]; this.unserMitte = [u.x + u.w / 2, u.y + u.h / 2];
    this.itPille = pille(b1.cam, { de: 'ohne IT-Abteilung', en: 'no IT department' }, { icon: 'door', col: C.muted, gestrichelt: true, size: 26 });
    this.pins = [0, 2, 3, 6, 7, 9, 1].map((i) => { const h = this.S.haeuser[i]; const p = g(b1.cam); el('line', { x1: 0, y1: 0, x2: 0, y2: 34, stroke: C.blue, 'stroke-width': 3 }, p); el('circle', { cx: 0, cy: 0, r: 11, fill: C.blue }, p); return { g: p, x: h.x + h.w / 2, y: h.y - 46 - (i % 2) * 20 }; });
    this.euPille = pille(b1.cam, { de: 'irgendwo in der EU', en: 'somewhere in the EU' }, { col: C.blue, size: 26 });
    shot(b1, this.tLage - 0.5, { typ: 'schwarz', d: 0.8 });
    // Kamera der Stadt: Mitte des Hauses „unser“ liegt bei Kamera (1000, 600), z 0.9
    this.stadtCam = { f: [1000, 520], z: 0.9 };
    this.portal1 = [(this.unserMitte[0] - 1000) * 0.9 + 960, (this.unserMitte[1] - 520) * 0.9 + 540];

    // ---------- 2 Büro ----------
    const b2 = buehne('lage-buero', { seed: 3 }); this.b2 = b2;
    this.B = bauBetrieb(b2.cam);
    this.angebot = g(b2.cam);
    const ab = blatt(this.angebot, { w: 260, h: 300, kicker: { de: 'ANGEBOT', en: 'QUOTE' }, pad: 26, kSize: 14 });
    this.angebotZeilen = linien(ab.g, ab.left, ab.y + 4, 190, 6, 28, C.pBar2, 10);
    this.okPos = [ab.right - 24, ab.y0 + ab.h - 40]; this.angebotOk = g(ab.g, { transform: `translate(${this.okPos[0]} ${this.okPos[1]})` }); el('circle', { r: 26, fill: C.green }, this.angebotOk); iconCheck(this.angebotOk, 30, '#fff');
    this.boegen = [[this.B.monA, this.B.monB], [this.B.monB, this.B.monC], [this.B.monC, null], [null, null]].slice(0, 2).map(([a, b]) => {
      const p0 = [a.x + a.w / 2, a.y - 10], p1 = [b.x + b.w / 2, b.y - 10];
      return el('path', { d: `M ${p0[0]} ${p0[1]} Q ${(p0[0] + p1[0]) / 2} ${p0[1] - 190} ${p1[0]} ${p1[1]}`, fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-dasharray': '10 10', 'stroke-linecap': 'round' }, b2.cam);
    });
    this.bogenM = el('path', { d: `M ${this.B.monC.x + 86} ${this.B.monC.y - 10} Q 2300 360 2522 470`, fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-dasharray': '10 10', 'stroke-linecap': 'round' }, b2.cam);
    this.keineEnt = pille(b2.cam, { de: 'keine Entscheidung', en: 'no decision' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 26 });
    shot(b2, this.tJemand - 0.6, { typ: 'kreis', d: 1.3, p: this.portal1 });

    // ---------- 3 Memo-Frage ----------
    const b3 = buehne('lage-memo', { seed: 13 }); this.b3 = b3;
    this.memo = g(b3.cam);
    const mb = blatt(this.memo, { w: 640, h: 610, kicker: { de: 'MEMO · SCUTORIA · FRAGE 1', en: 'MEMO · SCUTORIA · QUESTION 1' }, titel: { de: 'Nutzt Ihre Belegschaft heute KI-Tools bei der Arbeit?', en: 'Do your staff use AI tools at work today?' }, tSize: 36 });
    const ANTW = [
      { de: 'Ja, mit betrieblichen Konten', en: 'Yes, with business accounts', icon: 'building' },
      { de: 'Ja, mit privaten Konten, oder wir wissen es nicht', en: 'Yes, with private accounts, or we do not know', icon: 'person' },
      { de: 'Nein, soweit wir wissen', en: 'No, as far as we know', icon: 'cross' },
    ];
    this.antw = ANTW.map((a, i) => {
      const gr = g(mb.g); const y = mb.y + 30 + i * 118;
      const r = el('rect', { x: mb.left - 12, y, width: mb.w - 2 * mb.pad + 24, height: 100, rx: 14, fill: '#f1f4f9', stroke: '#d5dbe6', 'stroke-width': 2 }, gr);
      const ring = el('circle', { cx: mb.left + 22, cy: y + 50, r: 13, fill: 'none', stroke: C.pMuted, 'stroke-width': 2.5 }, gr);
      const dot = el('circle', { cx: mb.left + 22, cy: y + 50, r: 7.5, fill: C.blueDeep }, gr);
      const tx = TB(gr, mb.left + 56, y + 42, { de: a.de, en: a.en }, { size: 25, weight: 700, fill: C.pInk, maxW: mb.w - 2 * mb.pad - 70, lh: 30 });
      if (tx.zeilen === 1) tx.setAttribute('y', y + 58);
      return { g: gr, r, dot, y };
    });
    this.rechts = g(b3.cam);
    const rx = 1180;
    this.regelnG = g(this.rechts);
    T(this.regelnG, rx, 330, { de: 'Schriftliche Regeln', en: 'Written rules' }, { size: 34, weight: 800 });
    const mailG = g(this.regelnG, { transform: `translate(${rx + 60} 450)` }); iconMail(mailG, 110, C.paper);
    this.mailZettel = g(this.regelnG, { transform: `translate(${rx + 300} 450) rotate(3)` });
    el('rect', { x: -110, y: -64, width: 220, height: 128, rx: 6, fill: C.paper }, this.mailZettel);
    linien(this.mailZettel, -86, -36, 160, 3, 26, C.pBar2, 10);
    T(this.regelnG, rx, 560, { de: 'ein paar Sätze oder eine E-Mail', en: 'a few sentences or an email' }, { mono: 1, size: 22, fill: C.muted });
    this.einwG = g(this.rechts);
    T(this.einwG, rx, 650, { de: 'Einweisung', en: 'Briefing' }, { size: 34, weight: 800 });
    this.blasen = [0, 1].map((i) => { const b = g(this.einwG, { transform: `translate(${rx + 50 + i * 120} ${730 + i * 14})` }); iconChat(b, 78, i ? C.muted : C.ink); return b; });
    this.nachweis = g(this.einwG, { transform: `translate(${rx + 430} 742)` });
    el('rect', { x: -110, y: -58, width: 220, height: 116, rx: 10, fill: 'none', stroke: C.amber, 'stroke-width': 3, 'stroke-dasharray': '10 7' }, this.nachweis);
    T(this.nachweis, 0, -8, { de: 'NACHWEIS', en: 'RECORD' }, { mono: 1, size: 20, fill: C.amber, anchor: 'middle', ls: '0.1em' });
    T(this.nachweis, 0, 26, '—', { size: 30, weight: 800, fill: C.amber, anchor: 'middle' });
    T(this.einwG, rx, 840, { de: 'informell, ohne Nachweis', en: 'informally, without a record' }, { mono: 1, size: 22, fill: C.muted });
    shot(b3, this.tMemo - 0.4, { typ: 'blende', d: 0.8 });

    // ---------- 4 Drei Folgen ----------
    const b4 = buehne('lage-folgen', { seed: 17, regalDeckkraft: 0.6 }); this.b4 = b4;
    const PX = [400, 960, 1520], PY = 590;
    this.panels = PX.map((x, i) => {
      const gr = g(b4.cam);
      karte(gr, x - 250, PY - 250, 500, 500, { stroke: C.edge, fill: C.surface });
      const k = g(gr, { transform: `translate(${x} ${PY - 250})` }); const kin = g(k); kachel(kin, String(i + 1), C.blue, 70);
      return { g: gr, k, kin, x };
    });
    // Folge 1: Tastatur, Tool, Angaben fliegen hinein
    { const x = PX[0], gr = this.panels[0].g;
      this.tool1 = g(gr); el('rect', { x: x - 120, y: PY - 170, width: 240, height: 150, rx: 12, fill: '#0f1626', stroke: C.edge, 'stroke-width': 4 }, this.tool1); el('rect', { x: x - 108, y: PY - 158, width: 216, height: 126, rx: 8, fill: '#e3e9f5' }, this.tool1); ikon(this.tool1, 'spark', x, PY - 95, 56, C.blueDeep);
      this.toolGlow = el('circle', { cx: x, cy: PY - 95, r: 160, fill: 'url(#gBlue)' }, gr); gr.insertBefore(this.toolGlow, this.tool1);
      const kb = g(gr); el('rect', { x: x - 170, y: PY + 70, width: 340, height: 96, rx: 12, fill: '#16213a', stroke: C.line, 'stroke-width': 3 }, kb);
      this.tasten = []; for (let r = 0; r < 3; r++) for (let k = 0; k < 10; k++) this.tasten.push(el('rect', { x: x - 154 + k * 31, y: PY + 82 + r * 26, width: 25, height: 20, rx: 4, fill: '#24324f' }, kb));
      this.daten = ['id', 'euro', 'contract'].map((n) => { const d = g(gr); el('rect', { x: -42, y: -32, width: 84, height: 64, rx: 9, fill: C.paper }, d); ikon(d, n, 0, 0, 46, C.pInk); return d; });
      this.bet1 = g(gr, { transform: `translate(${x + 170} ${PY - 190})` }); iconBuilding(this.bet1, 44, C.dim); el('circle', { r: 36, fill: 'none', stroke: C.dim, 'stroke-width': 2.5, 'stroke-dasharray': '7 6' }, this.bet1);
      this.lab1 = T(gr, x, PY + 222, { de: 'an der Tastatur entschieden', en: 'decided at the keyboard' }, { size: 26, weight: 700, anchor: 'middle' }); }
    // Folge 2: Warnung, Regel unbekannt
    { const x = PX[1], gr = this.panels[1].g;
      this.regel2 = g(gr, { transform: `translate(${x} ${PY - 40})` });
      el('rect', { x: -130, y: -110, width: 260, height: 190, rx: 8, fill: 'none', stroke: C.amber, 'stroke-width': 3, 'stroke-dasharray': '11 8' }, this.regel2);
      T(this.regel2, 0, -60, { de: 'REGEL', en: 'RULE' }, { mono: 1, size: 20, fill: C.amber, anchor: 'middle', ls: '0.12em' });
      T(this.regel2, 0, 22, '?', { size: 84, weight: 800, fill: C.amber, anchor: 'middle' });
      this.warn2 = g(gr, { transform: `translate(${x - 150} ${PY - 170})` }); el('circle', { r: 60, fill: 'url(#gRed)' }, this.warn2); iconWarn(this.warn2, 80, C.red);
      this.fragen2 = [-90, 0, 90].map((dx, i) => { const q = g(gr, { transform: `translate(${x + dx} ${PY + 128})` }); iconPerson(q, 70, C.muted); const b = g(q, { transform: 'translate(32 -54)' }); iconQuestion(b, 42, C.ink); return q; });
      this.lab2 = T(gr, x, PY + 222, { de: 'Regel unbekannt', en: 'rule unknown' }, { size: 26, weight: 700, anchor: 'middle' }); }
    // Folge 3: Kunde, Versicherer, Belegschaft fragen; nichts zu zeigen
    { const x = PX[2], gr = this.panels[2].g;
      this.frager = [['building', { de: 'Kunde', en: 'customer' }], ['briefcase', { de: 'Versicherer', en: 'insurer' }], ['group', { de: 'Belegschaft', en: 'staff' }]].map(([n, lab], i) => {
        const q = g(gr, { transform: `translate(${x - 140 + i * 140} ${PY - 140})` }); ikon(q, n, 0, 0, 76, C.ink); const b = g(q, { transform: 'translate(38 -50)' }); iconQuestion(b, 42, C.blue); T(q, 0, 74, lab, { mono: 1, size: 20, fill: C.muted, anchor: 'middle' }); return q; });
      this.ordner3 = g(gr, { transform: `translate(${x} ${PY + 90})` });
      el('path', { d: 'M -90 -50 H -30 L -14 -32 H 90 V 60 H -90 Z', fill: 'none', stroke: C.amber, 'stroke-width': 4, 'stroke-dasharray': '11 8', 'stroke-linejoin': 'round' }, this.ordner3);
      T(this.ordner3, 0, 22, { de: 'leer', en: 'empty' }, { mono: 1, size: 22, fill: C.amber, anchor: 'middle', ls: '0.1em' });
      this.lab3 = T(gr, x, PY + 222, { de: 'nichts zu zeigen', en: 'nothing to show' }, { size: 26, weight: 700, anchor: 'middle' }); }
    shot(b4, this.tFolgen - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 5 Geschäftsgeheimnis ----------
    const b5 = buehne('lage-geheimnis', { seed: 19, regalDeckkraft: 0.6 }); this.b5 = b5;
    this.buch = g(b5.cam, { transform: 'translate(960 300)' }); iconBook(this.buch, 74, C.ink);
    T(this.buch, 0, 74, { de: 'RICHTLINIE (EU) 2016/943', en: 'DIRECTIVE (EU) 2016/943' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.08em' });
    this.TOR = [760, 1060, 1360];
    this.tore = this.TOR.map((x, i) => {
      const gr = g(b5.cam, { transform: `translate(${x} 0)` });
      const col = i === 2 ? C.blue : C.line;
      const ps = [el('rect', { x: -100, y: 470, width: 10, height: 250, rx: 4, fill: col }, gr), el('rect', { x: 90, y: 470, width: 10, height: 250, rx: 4, fill: col }, gr), el('rect', { x: -106, y: 460, width: 212, height: 14, rx: 6, fill: col }, gr)];
      const nr = T(gr, 0, 440, String(i + 1), { mono: 1, size: 30, fill: i === 2 ? C.blue : C.muted, anchor: 'middle' });
      const ok = g(gr, { transform: 'translate(0 400)' }); el('circle', { r: 0, fill: 'none' }, ok); iconCheck(ok, 34, C.blue);
      return { g: gr, ps, nr, ok };
    });
    this.kalk = g(b5.cam);
    const kb5 = blatt(this.kalk, { w: 220, h: 270, kicker: { de: 'KALKULATION', en: 'CALCULATION' }, pad: 22, kSize: 13 });
    for (let r = 0; r < 4; r++) { el('rect', { x: kb5.left, y: kb5.y + 6 + r * 34, width: 96, height: 9, rx: 4.5, fill: C.pBar2 }, kb5.g); T(kb5.g, kb5.right, kb5.y + 16 + r * 34, ['1.240 €', '86 €', '312 €', '1.638 €'][r], { mono: 1, size: 16, fill: C.pInk, anchor: 'end' }); }
    this.tor3Lab = TB(b5.cam, 1360 - 150, 772, { de: 'angemessene Geheimhaltungsmaßnahmen', en: 'reasonable steps to keep it secret' }, { size: 28, weight: 800, maxW: 320, lh: 34, fill: C.blue });
    this.tor3Lab.setAttribute('text-anchor', 'start');
    this.recht = [{ de: 'AT · § 26b UWG', en: 'AT · § 26b UWG' }, { de: 'DE · § 2 GeschGehG', en: 'DE · § 2 GeschGehG' }].map((s, i) => { const p = pille(b5.cam, s, { col: C.blue, size: 24, icon: 'para' }); return p; });
    this.rechtLinien = [0, 1].map((i) => el('path', { d: `M 1440 ${560 + i * 0} C 1520 560 1540 ${470 + i * 170} 1600 ${470 + i * 170}`, fill: 'none', stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '8 7' }, b5.cam));
    shot(b5, this.tG - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 6 Personenbezug ----------
    const b6 = buehne('lage-personenbezug', { seed: 23, regalDeckkraft: 0.6 }); this.b6 = b6;
    this.inst6 = g(b6.cam, { transform: 'translate(1380 300)' }); el('circle', { r: 110, fill: 'url(#gPaper)' }, this.inst6); iconInstitution(this.inst6, 84, C.ink);
    T(this.inst6, 0, 82, { de: 'DATENSCHUTZAUFSICHT · DE', en: 'DATA PROTECTION AUTHORITIES · DE' }, { mono: 1, size: 20, fill: C.muted, anchor: 'middle', ls: '0.08em' });
    this.eingabe = g(b6.cam);
    const eb = blatt(this.eingabe, { w: 600, h: 470, kicker: { de: 'EINGABE IN EIN TOOL · BEISPIEL', en: 'INPUT INTO A TOOL · EXAMPLE' } });
    const ZEILEN = [
      { de: 'Name: M. Beispiel', en: 'Name: M. Example', weg: 1 },
      { de: 'Anschrift: Musterweg 4', en: 'Address: 4 Sample Lane', weg: 1 },
      { de: 'Wärmepumpe, Baujahr 2019', en: 'Heat pump, built 2019' },
      { de: 'einziges Haus am Ortsende', en: 'only house at the end of the village' },
      { de: 'Termin Montag, 7 Uhr', en: 'Appointment Monday, 7 am' },
    ];
    this.ezeilen = ZEILEN.map((z, i) => {
      const y = eb.y + 34 + i * 62; const gr = g(eb.g);
      const tx = T(gr, eb.left, y, z, { size: 28, weight: 700, fill: C.pInk });
      const bar = el('rect', { x: eb.left - 8, y: y - 30, width: 0, height: 40, rx: 6, fill: C.pInk }, gr);
      const hi = el('rect', { x: eb.left - 10, y: y - 32, width: breite(tx) + 20, height: 44, rx: 8, fill: 'none', stroke: C.red, 'stroke-width': 3 }, gr);
      return { g: gr, tx, bar, hi, w: breite(tx), y, weg: !!z.weg };
    });
    this.person6 = g(b6.cam, { transform: 'translate(1420 640)' }); el('circle', { r: 120, fill: 'url(#gRed)' }, this.person6); iconPerson(this.person6, 130, C.red);
    this.person6Lab = T(b6.cam, 1420, 760, { de: 'Person erkennbar', en: 'person identifiable' }, { size: 28, weight: 800, anchor: 'middle', fill: C.red });
    this.faeden = [2, 3, 4].map((i) => el('path', { d: '', fill: 'none', stroke: C.red, 'stroke-width': 3, 'stroke-dasharray': '9 7' }, b6.cam));
    shot(b6, this.tD - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 7 Schublade ----------
    const b7 = buehne('lage-schublade', { seed: 3 }); this.b7 = b7;
    this.B7 = bauBetrieb(b7.cam);
    this.lade = this.B7.schrank.laden[1];
    this.papier = g(b7.cam);
    const pb = blatt(this.papier, { w: 200, h: 250, kicker: { de: 'RICHTLINIE', en: 'POLICY' }, pad: 20, kSize: 13 });
    linien(pb.g, pb.left, pb.y + 4, 140, 6, 24, C.pBar2, 8);
    this.dokP = pille(b7.cam, { de: 'dokumentiert', en: 'documented' }, { icon: 'check', col: C.blue, size: 26 });
    this.ertP = pille(b7.cam, { de: 'nie erteilt', en: 'never issued' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 26 });
    this.weg7 = el('path', { d: 'M 260 470 C 300 400 340 430 390 445', fill: 'none', stroke: C.amber, 'stroke-width': 4, 'stroke-dasharray': '10 8', 'stroke-linecap': 'round' }, b7.cam);
    this.lesez = g(b7.cam); el('path', { d: 'M -14 -40 H 14 V 18 L 0 6 L -14 18 Z', fill: C.amber }, this.lesez);
    shot(b7, this.tA - 0.4, { typ: 'blende', d: 0.8 });

    // ---------- 8 Womit anfangen ----------
    const b8 = buehne('lage-anfang', { seed: 29, regalDeckkraft: 0.6 }); this.b8 = b8;
    this.stapel = g(b8.cam);
    for (let i = 0; i < 18; i++) { el('rect', { x: -170 + (i % 3) * 3, y: -i * 16, width: 340, height: 230, rx: 5, fill: i % 2 ? C.paperBack : C.paper, filter: i === 17 ? 'url(#shadowS)' : '' }, this.stapel); }
    this.stapelLab = T(b8.cam, 1240, 962, { de: 'das längste Dokument', en: 'the longest document' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle' });
    this.eins = g(b8.cam); kachel(this.eins, '1', C.blue, 120); el('circle', { r: 160, fill: 'url(#gBlue)' }, this.eins); this.eins.appendChild(this.eins.firstChild);
    shot(b8, this.tWomit - 0.4, { typ: 'blende', d: 0.7 });

    this.buehnen = [b1, b2, b3, b4, b5, b6, b7, b8];

    // ---------- Einblendungen ----------
    kopf(this.tLage, this.tMemo - 0.3, K, '');
    kopf(this.tMemo, this.tFolgen - 0.3, K, { de: 'Die Frage im Memo', en: 'The question in the memo' });
    kopf(this.tFolgen, this.tG - 0.3, K, { de: 'Drei Folgen', en: 'Three consequences' });
    kopf(this.tG, this.tD - 0.3, K, { de: 'Geschäftsgeheimnis', en: 'Trade secrets' });
    kopf(this.tD, this.tA - 0.3, K, { de: 'Name entfernt reicht nicht', en: 'Removing the name is not enough' });
    kopf(this.tA, this.tWomit - 0.3, K, { de: 'Ein Papier in der Schublade', en: 'A paper in a drawer' });
    kopf(this.tWomit, this.tEnde - 0.3, K, { de: 'Womit anfangen?', en: 'Where to start?' });
  },

  zeichnen(t) {
    // ---------- 1 Stadt ----------
    if (this.b1.vis) {
      kamera(this.b1, [lerp(1040, 1000, P(t, this.tLage - 0.5, 4, E.out)), 520], lerp(0.84, 0.9, P(t, this.tLage - 0.5, 4, E.out)));
      this.S.haeuser.forEach((h, i) => {
        const unser = i === this.S.unser;
        h.fs.forEach((f, j) => {
          const t0 = this.tLage + this.fensterAn[i][j] * 1.6 + (unser ? 0 : 0.3) + (unser ? 0 : (i % 3) * 0.2);
          let k = P(t, t0, 0.3) * (unser ? 1 : (this.fensterAn[i][j] > 0.45 ? 0.55 : 0.12));
          if (!unser) k = Math.max(k, P(t, this.tEU + 0.2 + this.fensterAn[i][j] * 0.8, 0.3) * 0.75);
          if (unser) k = Math.max(k, 0.2);
          f.setAttribute('fill', unser ? (k > 0.5 ? '#cfe0ff' : '#1f2c47') : '#d9e0ee'); O(f, unser ? 0.35 + 0.65 * k : 0.15 + 0.6 * k);
        });
      });
      const [ux, uy] = this.unserMitte;
      pop(this.itPille, 0, 0, t, this.tOhneIT, 0.45, this.tJemand - 0.6); tr(this.itPille, ux, uy - 230, Math.max(0.01, P(t, this.tOhneIT, 0.45, E.back)));
      this.pins.forEach((p, i) => { const k = P(t, this.tEU + 0.1 + i * 0.12, 0.4, E.back); tr(p.g, p.x, p.y - (1 - k) * 30, Math.max(0.01, k)); O(p.g, Math.min(P(t, this.tEU + 0.1 + i * 0.12, 0.2), 1 - P(t, this.tJemand - 0.6, 0.3))); });
      rein(this.euPille, 1000, 330, t, this.tEU, 0.5, this.tJemand - 0.6);
    }
    // ---------- 2 Büro ----------
    if (this.b2.vis) {
      const B = this.B;
      const k = fahrt(t, { f: [1300, 520], z: 1.2 }, [
        { t: this.tNaechste - 0.2, d: 0.9, f: [1420, 520], z: 1.0 },
        { t: this.tNaechste + 1.1, d: 1.0, f: [1740, 480], z: 0.62 },
        { t: this.tNiemand - 0.3, d: 1.2, f: [470, 470], z: 1.3 },
      ]);
      kamera(this.b2, k.f, k.z);
      bildschirm(B.monA, P(t, this.tText, 0.4, E.out));
      const ausbreitung = [this.tNaechste + 0.55, this.tNaechste + 1.25, this.tNaechste + 1.6, this.tNaechste + 1.9];
      bildschirm(B.monB, P(t, ausbreitung[0], 0.35, E.out));
      bildschirm(B.monC, P(t, ausbreitung[1], 0.35, E.out));
      B.telefone.forEach((f, i) => { const kk = P(t, ausbreitung[2 + i], 0.35, E.out); O(f.dim, 0.78 * (1 - kk)); O(f.glow, 0.12 + 0.88 * kk); });
      zeichne(this.boegen[0], P(t, this.tNaechste, 0.6)); O(this.boegen[0], 1 - P(t, this.tNiemand, 0.5));
      zeichne(this.boegen[1], P(t, this.tNaechste + 0.8, 0.45)); O(this.boegen[1], 1 - P(t, this.tNiemand, 0.5));
      zeichne(this.bogenM, P(t, this.tNaechste + 1.2, 0.5)); O(this.bogenM, 1 - P(t, this.tNiemand, 0.5));
      [this.boegen[0], this.boegen[1], this.bogenM].forEach((p) => { if (P(t, this.tNaechste + 2.2, 0.01) > 0) { p.setAttribute('stroke-dasharray', '10 10'); p.setAttribute('stroke-dashoffset', (-t * 30).toFixed(1)); } });
      betriebLeben(B, t, { tippen: { figA: [this.tText + 0.3, 999], figB: [ausbreitung[0] + 0.2, 999], figC: [ausbreitung[1] + 0.2, 999] } });
      // Angebot entsteht über dem Bildschirm
      const ak = P(t, this.tAngebot - 0.1, 0.6, E.out);
      tr(this.angebot, 1330, lerp(430, 380, ak), 0.75, lerp(-6, -2, ak)); O(this.angebot, Math.min(ak, 1 - P(t, this.tNaechste + 0.3, 0.4)));
      this.angebotZeilen.forEach((z, i) => O(z, P(t, this.tAngebot + 0.15 + i * 0.12, 0.15)));
      { const kk = P(t, this.tFunkt + 0.1, 0.45, E.back); this.angebotOk.setAttribute('transform', `translate(${this.okPos[0]} ${this.okPos[1]}) scale(${Math.max(0.01, kk).toFixed(3)})`); O(this.angebotOk, P(t, this.tFunkt + 0.1, 0.2)); }
      // niemand hat entschieden
      const rk = P(t, this.tNiemand + 0.3, 0.5);
      B.rahmenRect.setAttribute('stroke', rk > 0.5 ? C.amberLine : C.line); B.rahmenRect.setAttribute('stroke-width', (3 + 2 * rk).toFixed(1)); B.rahmenRect.setAttribute('stroke-dashoffset', (-t * 18).toFixed(1));
      pop(this.keineEnt, 0, 0, t, this.tNiemand + 0.5); tr(this.keineEnt, 445, 292, Math.max(0.01, P(t, this.tNiemand + 0.5, 0.45, E.back)));
    }
    // ---------- 3 Memo-Frage ----------
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      const mi = P(t, this.tMemo - 0.3, 0.8, E.out);
      tr(this.memo, lerp(960, 620, P(t, this.tRegeln - 0.7, 0.8)), 590 + (1 - mi) * 40, 1, lerp(-4, -1.5, mi));
      const zeit = [this.tA1, this.tA2, this.tA3];
      this.antw.forEach((a, i) => {
        const auf = P(t, this.tDrei - 0.1 + i * 0.15, 0.35, E.out);
        const spricht0 = fenster(t, zeit[i], 0.25, i < 2 ? zeit[i + 1] : this.tMitte, 0.3);
        const gewaehlt = i === 1 ? P(t, this.tMitte, 0.4) : 0;
        const dunkel = i !== 1 ? P(t, this.tMitte, 0.4) : 0;
        O(a.g, auf * (1 - 0.55 * dunkel));
        a.r.setAttribute('stroke', gewaehlt > 0.5 || spricht0 > 0.5 ? C.blue : '#d5dbe6');
        a.r.setAttribute('stroke-width', (2 + 2 * Math.max(gewaehlt, spricht0)).toFixed(1));
        a.r.setAttribute('fill', gewaehlt > 0.5 ? C.blueSoft : '#f1f4f9');
        O(a.dot, gewaehlt);
        sk(a.g, 0, a.y + 50, 1 + 0.03 * gewaehlt);
      });
      const r1 = P(t, this.tRegeln - 0.1, 0.5, E.out); O(this.regelnG, r1); tr(this.regelnG, (1 - r1) * 30, 0);
      tr(this.mailZettel, 1180 + 300, 450 - 16 * P(t, this.tMail, 0.5, E.out), 1, 3 - 3 * P(t, this.tMail, 0.5));
      const r2 = P(t, this.tEinw - 0.1, 0.5, E.out); O(this.einwG, r2); tr(this.einwG, (1 - r2) * 30, 0);
      this.blasen.forEach((b, i) => { const kk = P(t, this.tEinw + 0.2 + i * 0.3, 0.4, E.back); b.setAttribute('transform', `translate(${1180 + 50 + i * 120} ${730 + i * 14 + Math.sin(t * 3 + i) * 4}) scale(${Math.max(0.01, kk).toFixed(3)})`); });
      pop(this.nachweis, 1180 + 430, 742, t, this.tOhneN); this.nachweis.setAttribute('transform', `translate(1610 742) scale(${Math.max(0.01, P(t, this.tOhneN, 0.45, E.back)).toFixed(3)})`);
    }
    // ---------- 4 Drei Folgen ----------
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      const PX = [400, 960, 1520], PY = 590;
      const panelT = [this.tFolgen + 0.2, this.tSchief - 0.2, this.tKunde - 0.5];
      const aktiv = [[this.tTast - 1.4, this.tSchief - 0.2], [this.tSchief - 0.2, this.tKunde - 0.5], [this.tKunde - 0.5, 1e9]];
      this.panels.forEach((p, i) => {
        const auf = P(t, this.tFolgen + 0.1 + i * 0.18, 0.5, E.out);
        const an = fenster(t, aktiv[i][0], 0.4, aktiv[i][1], 0.4);
        const war = P(t, aktiv[i][1], 0.4);
        tr(p.g, 0, (1 - auf) * 40); O(p.g, auf * (0.5 + 0.5 * Math.max(an, i === 2 ? 0 : war * 0.6, P(t, this.tNichts + 0.6, 0.5))));
        sk(p.kin, 0, 0, 1 + 0.12 * an);
      });
      // Folge 1
      const x1 = PX[0];
      const tasten = t > this.tTast - 1.2 && t < this.tSchief;
      this.tasten.forEach((k, i) => k.setAttribute('fill', tasten && Math.sin(t * 23 + i * 2.7) > 0.86 ? C.blue : '#24324f'));
      O(this.toolGlow, 0.3 + 0.7 * P(t, this.tTast - 1.2, 0.4));
      this.daten.forEach((d, i) => {
        const t0 = this.tTast - 0.9 + i * 0.55, kk = P(t, t0, 0.9, E.io);
        const pos = bogen([x1 - 80 + i * 80, PY + 90], [x1, PY - 95], kk, 60);
        tr(d, pos[0], pos[1], lerp(1, 0.4, kk), 0); O(d, Math.min(P(t, t0, 0.15), 1 - P(t, t0 + 0.8, 0.12)) * (t < this.tSchief + 2 ? 1 : 0));
      });
      const nb = P(t, this.tNichtB, 0.4); O(this.bet1, 0.4 + 0.6 * nb); this.bet1.setAttribute('transform', `translate(${x1 + 170} ${PY - 190}) scale(${(1 + 0.15 * puls(t, this.tNichtB, 0.9, 8)).toFixed(3)})`);
      O(this.lab1, P(t, this.tTast, 0.4));
      // Folge 2
      const x2 = PX[1];
      this.regel2.setAttribute('transform', `translate(${x2} ${PY - 40})`); O(this.regel2, P(t, this.tSchief, 0.4));
      this.regel2.firstChild.setAttribute('stroke-dashoffset', (-t * 16).toFixed(1));
      pop(this.warn2, 0, 0, t, this.tSchief + 0.2); this.warn2.setAttribute('transform', `translate(${x2 - 150} ${PY - 170}) scale(${Math.max(0.01, P(t, this.tSchief + 0.2, 0.45, E.back)).toFixed(3)})`);
      this.fragen2.forEach((q, i) => { const kk = P(t, this.tRegelWar - 0.4 + i * 0.15, 0.4, E.back); q.setAttribute('transform', `translate(${x2 - 90 + i * 90} ${PY + 128}) scale(${Math.max(0.01, kk).toFixed(3)})`); O(q, P(t, this.tRegelWar - 0.4 + i * 0.15, 0.2)); });
      O(this.lab2, P(t, this.tRegelWar, 0.4));
      // Folge 3
      const x3 = PX[2], ft = [this.tKunde, this.tVers, this.tBeleg];
      this.frager.forEach((q, i) => { const kk = P(t, ft[i], 0.45, E.back); q.setAttribute('transform', `translate(${x3 - 140 + i * 140} ${PY - 140 + Math.sin(t * 2 + i) * 3}) scale(${Math.max(0.01, kk).toFixed(3)})`); O(q, P(t, ft[i], 0.2)); });
      const ok3 = P(t, this.tNichts - 0.2, 0.5, E.back); this.ordner3.setAttribute('transform', `translate(${x3} ${PY + 90}) scale(${Math.max(0.01, ok3).toFixed(3)})`); O(this.ordner3, P(t, this.tNichts - 0.2, 0.2));
      this.ordner3.firstChild.setAttribute('stroke-dashoffset', (-t * 16).toFixed(1));
      O(this.lab3, P(t, this.tNichts, 0.4));
    }
    // ---------- 5 Geschäftsgeheimnis ----------
    if (this.b5.vis) {
      kamera(this.b5, [960, 540], 1);
      O(this.buch, P(t, this.tRL - 0.2, 0.5)); tr(this.buch, 960, 300 + (1 - P(t, this.tRL - 0.2, 0.5, E.out)) * -20);
      this.tore.forEach((tor, i) => { const kk = P(t, this.tBed + i * 0.15, 0.45, E.out); tr(tor.g, this.TOR[i], (1 - kk) * 30); O(tor.g, kk); });
      // Kalkulation läuft durch die Tore
      const s1 = this.tBed + 0.6, s2 = s1 + 1.0, s3 = this.tDritte;
      const links = P(t, this.tBed - 0.5, 0.6);
      let x = lerp(960, 450, links), sc = lerp(1.35, 0.7, links);
      x = lerp(x, 760, P(t, s1, 0.7)); x = lerp(x, 1060, P(t, s2, 0.7)); x = lerp(x, 1360, P(t, s3, 0.7));
      tr(this.kalk, x, 600 + Math.sin(t * 2) * 4, sc, lerp(-3, 0, links));
      O(this.kalk, P(t, this.tG - 0.2, 0.5));
      [s1 + 0.55, s2 + 0.55].forEach((t0, i) => { const ok = this.tore[i].ok; ok.setAttribute('transform', `translate(0 400) scale(${Math.max(0.01, P(t, t0, 0.4, E.back)).toFixed(3)})`); O(ok, P(t, t0, 0.2)); });
      O(this.tore[2].ok, 0);
      const hi = P(t, this.tAngem, 0.5);
      this.tore[2].ps.forEach((p) => p.setAttribute('fill', hi > 0.5 ? C.blue : C.line)); this.tore[2].nr.setAttribute('fill', hi > 0.2 || P(t, this.tDritte, 0.3) > 0.5 ? C.blue : C.muted);
      O(this.tor3Lab, hi); tr(this.tor3Lab, 0, (1 - hi) * 14);
      this.recht.forEach((p, i) => { rein(p, 1700, 470 + i * 170, t, this.tAT + 0.2 + i * 0.3, 0.5); });
      this.rechtLinien.forEach((l, i) => zeichne(l, P(t, this.tAT + 0.1 + i * 0.3, 0.6)));
    }
    // ---------- 6 Personenbezug ----------
    if (this.b6.vis) {
      kamera(this.b6, [960, 540], 1);
      const ii = P(t, this.tD, 0.6, E.out); O(this.inst6, ii); tr(this.inst6, 1380, 300 - (1 - ii) * 24);
      const ei = P(t, this.tD + 0.3, 0.7, E.out); tr(this.eingabe, 640, 600 + (1 - ei) * 40, 1, -1.5); O(this.eingabe, ei);
      let n = 0;
      this.ezeilen.forEach((z, i) => {
        O(z.g, P(t, this.tD + 0.5 + i * 0.12, 0.3));
        if (z.weg) { const kk = P(t, this.tNamen + 0.2 + n * 0.35, 0.5); z.bar.setAttribute('width', ((z.w + 16) * kk).toFixed(1)); n++; O(z.hi, 0); }
        else { O(z.hi, P(t, this.tReicht + 0.2, 0.4) * (0.7 + 0.3 * Math.sin(t * 5))); }
      });
      // Fäden aus dem Zusammenhang zur Person
      const ctx = this.ezeilen.filter((z) => !z.weg);
      this.faeden.forEach((f, i) => { const z = ctx[i]; const a = [640 - 300 + 40 + z.w + 18, 600 - 235 + z.y + 235 - 12]; const b = [1340, 640]; f.setAttribute('d', `M ${a[0].toFixed(0)} ${a[1].toFixed(0)} C ${(a[0] + 200).toFixed(0)} ${a[1].toFixed(0)} ${(b[0] - 160).toFixed(0)} ${b[1]} ${b[0]} ${b[1]}`); f.__len = null; zeichne(f, P(t, this.tZus - 0.2 + i * 0.2, 0.7)); });
      const pk = P(t, this.tZus + 0.5, 0.6, E.back); this.person6.setAttribute('transform', `translate(1420 640) scale(${Math.max(0.01, pk).toFixed(3)})`); O(this.person6, P(t, this.tZus + 0.5, 0.3));
      O(this.person6Lab, P(t, this.tZus + 0.9, 0.4));
    }
    // ---------- 7 Schublade ----------
    if (this.b7.vis) {
      const B = this.B7;
      kamera(this.b7, [410, 540], 1.32);
      betriebLeben(B, t, {});
      const auf = Math.min(P(t, this.tA + 0.3, 0.7), 1 - P(t, this.tZurueck + 0.3, 0.7));
      tr(this.lade, 90 * auf, 0);
      const hoch = Math.min(P(t, this.tA + 0.7, 0.8, E.out), 1 - P(t, this.tZurueck, 0.7, E.in));
      tr(this.papier, 185 + 90 * auf, lerp(660, 470, hoch), lerp(0.4, 0.9, hoch), lerp(0, -3, hoch)); O(this.papier, Math.min(1, hoch * 3));
      pop(this.dokP, 0, 0, t, this.tDok, 0.45, this.tZurueck); tr(this.dokP, 130, 335, Math.max(0.01, P(t, this.tDok, 0.45, E.back)));
      pop(this.ertP, 0, 0, t, this.tErteilt, 0.45); tr(this.ertP, 530, 335, Math.max(0.01, P(t, this.tErteilt, 0.45, E.back)));
      zeichne(this.weg7, 0.55 * P(t, this.tErteilt + 0.2, 0.6)); O(this.weg7, 1 - P(t, this.tZurueck, 0.5));
      B.rahmenRect.setAttribute('stroke', P(t, this.tErteilt, 0.4) > 0.5 ? C.amberLine : C.line); B.rahmenRect.setAttribute('stroke-dashoffset', (-t * 18).toFixed(1));
      const lz = P(t, this.tZurueck + 0.8, 0.4, E.back); tr(this.lesez, 260 + 90 * auf - 60, 600, Math.max(0.01, lz)); O(this.lesez, P(t, this.tZurueck + 0.8, 0.2));
    }
    // ---------- 8 Womit anfangen ----------
    if (this.b8.vis) {
      kamera(this.b8, [960, 540], 1);
      const si = P(t, this.tWomit - 0.2, 0.7, E.out), weg = P(t, this.tLaengst - 0.3, 0.9, E.io);
      tr(this.stapel, lerp(960, 1240, weg), 740 + (1 - si) * 40, lerp(1, 0.78, weg), lerp(-2, 4, weg)); O(this.stapel, si * (1 - 0.65 * weg));
      O(this.stapelLab, Math.min(P(t, this.tLaengst, 0.4), 1));
      const ek = P(t, this.tLaengst + 0.3, 0.6, E.back); tr(this.eins, 640, 560, Math.max(0.01, ek)); O(this.eins, P(t, this.tLaengst + 0.3, 0.3));
    }
  },
});
