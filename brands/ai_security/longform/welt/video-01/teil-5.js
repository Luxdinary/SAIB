// Teil 5 · Der Beispielbetrieb, erfunden. Absätze 37 bis 42 des Skripts.
// Bühnen: Generator (Frage 3 von 34, vorbelegt) → Haus mit Besetzung → Memo mit roter Lampe → § 1 als Weggabelung →
// § 2 und § 3 → die eine Seite aus der Richtlinie → Nachweisseite (Geregelt, Geplant, Offen).
akt({
  name: 'beispiel',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    const K = { de: '5 · DER BEISPIELBETRIEB, ERFUNDEN', en: '5 · THE EXAMPLE BUSINESS, FICTIONAL' };
    this.tGen = c('Der Generator ist', 'The generator is');
    this.tErf = c('erfundenen Betrieb', 'fictional business');
    this.tKeine = c('keine echte Person', 'no real person');
    this.tMuster = c('Muster Elektrotechnik', 'Example Electrical');
    this.tAT = c('in Österreich', 'in Austria');
    this.tZehn = c('zehn bis|10 bis', 'ten to|10 to');
    this.tInh = c('Eine Inhaberin', 'An owner');
    { const m = cue({ de: 'Montagepersonal', en: 'field staff' }); this.tMont = m.s; // „Büro“ davor verschluckt Whisper manchmal
      const b = cue({ de: 'Büro', en: 'office staff' }, { ab: Math.max(0, m.i - 3), halten: true, leise: true, weit: 3 }); this.tBuero = b ? b.s : m.s - 0.7; }
    this.tLehr = c('ein Lehrling', 'one apprentice');
    this.tDreiP = c('Drei Personen im Büro', 'Three people in the office');
    this.tVerw = [c('für Angebote', 'for quotes'), c('Zusammenfassungen', 'summaries'), c('Übersetzungen', 'translations')];
    this.tZwei = c('Zwei Monteure', 'Two field staff');
    this.tPrivat = c('privat auf dem Telefon', 'privately on their phones');
    this.tNiemand = c('Niemand hier ist echt', 'Nobody here is real');
    this.tMemo = c('Geben Sie diese Lage', 'Put that situation');
    this.tRot = c('auf Rot', 'is red');
    this.tWeil = c('weil die Konten privat', 'because the accounts are private');
    this.tErster = c('Der erste Schritt lautet', 'The first step reads');
    this.tKonten = c('betriebliche Konten ein', 'set up business accounts');
    this.tTraining = c('abgeschaltet', 'switched off');
    this.tSeite = c('hängen Sie die eine Seite', 'post the one page');
    this.tP1 = c('Paragraf eins|Paragraf 1', 'section one|section 1');
    this.tFuer2 = c('Für die zwei Monteure', 'For the two field staff');
    this.tEntweder = c('Entweder bekommen', 'either they get');
    this.tOder = c('oder die dienstliche Nutzung', 'or their work use');
    this.tGelt = c('mit dem Geltungsbeginn', 'on the effective date');
    this.tWie = c('Wie bisher', 'As before');
    this.tP2 = c('Paragraf zwei|Paragraf 2', 'Section two|Section 2');
    this.tU = [c('Entwürfe für Angebote', 'quote drafts'), c('Herstellertexten', 'manufacturer texts'), c('Übersetzungen für', 'translations for'), c('Mängelrügen', 'complaints')];
    this.tBew = c('Bewerbungen', 'applications');
    this.tAus = c('ausgeschlossen', 'is excluded');
    this.tP3 = c('Paragraf drei|Paragraf 3', 'Section three|Section 3');
    this.tKalk = c('Kalkulationsblätter', 'calculation sheets');
    this.tCodes = c('Zutrittscodes', 'access codes');
    this.tD2 = c('Die eine Seite nimmt', 'The one page takes');
    this.tWider = c('nicht widersprechen', 'cannot contradict');
    this.tNie = c('was nie hinein darf', 'what never goes in');
    this.tAnkreuz = c('Ankreuzfeldern', 'boxes to tick');
    this.tGepr = c('vor der Verwendung geprüft', 'checked before use');
    this.tGefragt = c('wer gefragt wird', 'who is asked');
    this.tVorf = c('Vorfälle gemeldet', 'incidents are reported');
    this.tD7 = c('Und die Nachweisseite', 'And the evidence summary');
    this.tDatiert = c('datiert', 'dated');
    this.tDokNr = c('Dokumentnummer', 'document number');
    this.tZeile = c('je Nachweis eine Zeile', 'one line per piece');
    this.tStatus = c('Geregelt, Geplant', 'regulated, planned');
    this.tWv = c('Wiedervorlage', 'review after');
    this.tAnlass = c('jedem Anlass', 'every occasion');
    this.tOffen = c('Offene Punkte', 'Open items');
    this.tEnde = cue({ de: 'Es ist keine Rechtsberatung', en: 'It is not legal advice' }, { halten: true }).s;

    // ---------- 1 Generator ----------
    const bG = buehne('beispiel-generator', { seed: 73, regalDeckkraft: 0.6 }); this.bG = bG;
    const gc = bG.cam;
    this.form = g(gc);
    karte(this.form, 260, 230, 900, 640, { fill: C.surface, stroke: C.edge });
    T(this.form, 310, 300, { de: 'KI-RICHTLINIEN-TOOLKIT · GENERATOR', en: 'AI POLICY TOOLKIT · GENERATOR' }, { mono: 1, size: 20, fill: C.muted, ls: '0.1em' });
    T(this.form, 1110, 300, { de: 'FRAGE 3 VON 34', en: 'QUESTION 3 OF 34' }, { mono: 1, size: 20, fill: C.blue, anchor: 'end', ls: '0.1em' });
    el('rect', { x: 310, y: 322, width: 800, height: 8, rx: 4, fill: C.lane }, this.form);
    el('rect', { x: 310, y: 322, width: 800 * 3 / 34, height: 8, rx: 4, fill: C.blue }, this.form);
    const FELD = [[{ de: 'Name des Betriebs', en: 'Name of the business' }, { de: 'Muster Elektrotechnik e.U.', en: 'Example Electrical Ltd' }],
      [{ de: 'Land', en: 'Country' }, { de: 'Österreich', en: 'Austria' }], [{ de: 'Beschäftigte', en: 'Staff' }, { de: '10 bis 49', en: '10 to 49' }]];
    this.felder = FELD.map(([lab, wert], i) => {
      const y = 400 + i * 150; const gr = g(this.form);
      T(gr, 310, y, lab, { size: 24, weight: 700, fill: C.muted });
      el('rect', { x: 310, y: y + 20, width: 800, height: 76, rx: 12, fill: C.raised, stroke: C.line, 'stroke-width': 2 }, gr);
      const tx = T(gr, 336, y + 70, '', { size: 34, weight: 800 });
      return { tx, wert, y };
    });
    this.vorbelegt = pille(gc, { de: 'vorbelegt', en: 'prefilled' }, { icon: 'check', col: C.blue, size: 22 });
    this.stempelG = stempel(gc, { de: 'ERFUNDEN · KEINE ECHTE PERSON', en: 'FICTIONAL · NO REAL PERSON' }, C.amber, 26);
    shot(bG, this.tGen - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- 2 Haus mit Besetzung ----------
    const bB = buehne('beispiel-haus', { seed: 3 }); this.bB = bB;
    this.B = bauBetrieb(bB.cam);
    const rolle = (txt, icon, col = C.blue) => pille(bB.cam, txt, { icon, col, size: 30 });
    this.rInh = rolle({ de: 'Inhaberin · Leitung', en: 'Owner · management' }, 'person');
    this.rBuero = rolle({ de: 'Büro · drei Personen', en: 'Office · three people' }, 'group');
    this.rMont = rolle({ de: 'Montage · zwei Monteure', en: 'Field staff · two' }, 'truck');
    this.rLehr = rolle({ de: 'Lehrling', en: 'Apprentice' }, 'person');
    this.verwP = [['doc', { de: 'Angebote', en: 'Quotes' }], ['list', { de: 'Zusammenfassungen', en: 'Summaries' }], ['translate', { de: 'Übersetzungen', en: 'Translations' }]].map(([ic, t0]) => pille(bB.cam, t0, { icon: ic, col: C.blue, size: 24 }));
    this.privP = [0, 1].map(() => pille(bB.cam, { de: 'privat', en: 'private' }, { icon: 'person', col: C.amber, gestrichelt: true, size: 26 }));
    this.stempelB = stempel(bB.cam, { de: 'ERFUNDEN', en: 'FICTIONAL' }, C.amber, 64);
    shot(bB, this.tInh - 0.7, { typ: 'kreis', d: 1.2, p: [710, 470] });

    // ---------- 3 Memo, rote Lampe ----------
    const bM = buehne('beispiel-memo', { seed: 1 }); this.bM = bM;
    this.memo = bauMemo(bM.cam);
    this.lampRing = el('circle', { cx: -180, cy: 250, r: 26, fill: 'none', stroke: C.red, 'stroke-width': 4 }, this.memo.band);
    this.kontenP = pille(bM.cam, { de: 'Konten: privat', en: 'Accounts: private' }, { icon: 'person', col: C.red, size: 26 });
    this.erster = g(bM.cam);
    karte(this.erster, 1100, 300, 680, 480, { fill: C.surface, stroke: C.blue });
    T(this.erster, 1140, 362, { de: 'ERSTER SCHRITT', en: 'FIRST STEP' }, { mono: 1, size: 22, fill: C.blue, ls: '0.12em' });
    this.e1 = g(this.erster); { const ic = g(this.e1, { transform: 'translate(1180 470)' }); iconBuilding(ic, 60, C.blue); TB(this.e1, 1240, 460, { de: 'Betriebliche Konten einrichten', en: 'Set up business accounts' }, { size: 32, weight: 800, maxW: 500, lh: 38 }); }
    this.tgl = g(this.erster, { transform: 'translate(1290 565)' });
    T(this.tgl, -50, 8, 'TRAINING', { mono: 1, size: 18, fill: C.muted, anchor: 'end', ls: '0.08em' });
    this.tglTrack = el('rect', { x: -30, y: -15, width: 60, height: 30, rx: 15, fill: C.blue }, this.tgl);
    this.tglKnob = el('circle', { cx: 15, cy: 0, r: 11, fill: '#fff' }, this.tgl);
    this.tglTxt = T(this.tgl, 44, 8, { de: 'AN', en: 'ON' }, { mono: 1, size: 18, fill: C.ink, ls: '0.08em' });
    this.e2 = g(this.erster); { const ic = g(this.e2, { transform: 'translate(1180 680)' }); iconDoc(ic, 60, C.blue); TB(this.e2, 1240, 670, { de: 'Die eine Seite aushängen', en: 'Post the one page' }, { size: 32, weight: 800, maxW: 500, lh: 38 }); }
    shot(bM, this.tMemo - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 4 § 1 als Weggabelung ----------
    const b1 = buehne('beispiel-p1', { seed: 79, regalDeckkraft: 0.6 }); this.b1 = b1;
    const pc = b1.cam;
    this.d1 = g(pc);
    const db = blatt(this.d1, { w: 420, h: 520, kicker: { de: 'D1 · KI-NUTZUNGSRICHTLINIE', en: 'D1 · AI USAGE POLICY' }, titel: { de: '§ 1 Tools und Zugang', en: '§ 1 Tools and access' }, tSize: 30 });
    linien(db.g, db.left, db.y + 10, 320, 8, 30, C.pBar2, 10);
    this.mont = stehend(pc, 820, 900, { ...BESETZUNG.monteur1, skala: 0.95 });
    this.gab = [
      { d: 'M 900 600 C 1080 600 1120 380 1300 380', col: C.blue, ziel: [1500, 380] },
      { d: 'M 900 600 L 1200 600', col: C.red, ziel: [1290, 600] },
      { d: 'M 900 600 C 1080 600 1120 820 1300 820', col: C.muted, ziel: [1500, 820] },
    ].map((w) => ({ ...w, p: el('path', { d: w.d, fill: 'none', stroke: w.col, 'stroke-width': 10, 'stroke-linecap': 'round', 'stroke-dasharray': w.col === C.muted ? '16 12' : '' }, pc) }));
    this.zielA = g(pc); karte(this.zielA, 1310, 320, 520, 120, { fill: C.surface, stroke: C.blue }); { const ic = g(this.zielA, { transform: 'translate(1365 380)' }); iconBuilding(ic, 54, C.blue); } T(this.zielA, 1410, 392, { de: 'Zugang über Betriebskonto', en: 'Access via business account' }, { size: 26, weight: 800 });
    this.zielB = g(pc); karte(this.zielB, 1310, 760, 460, 120, { fill: C.surface, stroke: C.edge, gestrichelt: true }); { const ic = g(this.zielB, { transform: 'translate(1365 820)' }); iconPhone(ic, 54, C.muted); const x = g(this.zielB, { transform: 'translate(1365 820)' }); iconCross(x, 40, C.muted); } TB(this.zielB, 1410, 810, { de: 'private Nutzung endet mit Geltungsbeginn', en: 'private use ends on the effective date' }, { size: 26, weight: 800, maxW: 340, lh: 30 });
    this.sperre = g(pc); el('rect', { x: 1206, y: 540, width: 14, height: 120, rx: 7, fill: C.red }, this.sperre); el('circle', { cx: 1213, cy: 600, r: 70, fill: 'url(#gRed)' }, this.sperre);
    this.wieBisher = pille(pc, { de: '„wie bisher“: keine Antwort', en: '"as before": not an option' }, { icon: 'cross', col: C.red, size: 24 });
    shot(b1, this.tP1 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 5 § 2 und § 3 ----------
    const b2 = buehne('beispiel-p2', { seed: 83, regalDeckkraft: 0.6 }); this.b2 = b2;
    const qc = b2.cam;
    this.p2 = g(qc);
    const p2b = blatt(this.p2, { w: 700, h: 640, kicker: { de: 'D1 · § 2', en: 'D1 · § 2' }, titel: { de: 'Verwendungen, die vorkommen', en: 'Uses that actually occur' }, tSize: 32 });
    const VW = [['doc', { de: 'Entwürfe für Angebote', en: 'Quote drafts' }], ['list', { de: 'Zusammenfassungen von Herstellertexten', en: 'Summaries of manufacturer texts' }], ['translate', { de: 'Übersetzungen für die Monteure', en: 'Translations for the field staff' }], ['pen', { de: 'Formulierungshilfe bei Mängelrügen', en: 'Wording help for complaints' }]];
    this.vw = VW.map(([ic, txt], i) => { const gr = g(p2b.g); const y = p2b.y + 30 + i * 62; const h = g(gr, { transform: `translate(${p2b.left + 14} ${y - 8})` }); iconCheck(h, 28, C.blueDeep); ikon(gr, ic, p2b.left + 56, y - 8, 28, C.pInk); T(gr, p2b.left + 90, y, txt, { size: 24, weight: 700, fill: C.pInk }); return gr; });
    const ay = p2b.y + 30 + 4 * 62 + 20;
    el('rect', { x: p2b.left, y: ay - 26, width: p2b.w - 2 * p2b.pad, height: 1.5, fill: C.pLine }, p2b.g);
    this.ausg = [{ de: 'Bewerbungen', en: 'Applications' }, { de: 'Beurteilung einzelner Beschäftigter', en: 'Assessment of individual employees' }].map((txt, i) => { const gr = g(p2b.g); const y = ay + 24 + i * 56; const x = g(gr, { transform: `translate(${p2b.left + 14} ${y - 8})` }); iconCross(x, 28, C.redDeep); const tx = T(gr, p2b.left + 56, y, txt, { size: 24, weight: 700, fill: C.pMuted }); const st = el('rect', { x: p2b.left + 54, y: y - 10, width: 0, height: 3, fill: C.redDeep }, gr); return { g: gr, st, w: breite(tx) }; });
    T(p2b.g, p2b.right, ay - 2, { de: 'AUSGESCHLOSSEN', en: 'EXCLUDED' }, { mono: 1, size: 15, fill: C.redDeep, anchor: 'end', ls: '0.1em' });
    this.p3 = g(qc);
    const p3b = blatt(this.p3, { w: 560, h: 640, kicker: { de: 'D1 · § 3', en: 'D1 · § 3' }, titel: { de: 'Was nie hinein darf', en: 'What never goes in' }, tSize: 32 });
    ['id', 'key', 'calc', 'pulse', 'sealed'].forEach((ic, i) => { const y = p3b.y + 30 + i * 52; ikon(p3b.g, ic, p3b.left + 16, y - 8, 26, C.pMuted); el('rect', { x: p3b.left + 46, y: y - 14, width: 260 - (i * 23) % 70, height: 12, rx: 6, fill: C.pBar2 }, p3b.g); });
    this.neu = [['calc', { de: 'Kalkulationsblätter je Auftrag', en: 'Calculation sheets per job' }], ['key', { de: 'Zutrittscodes zu Kundenobjekten', en: 'Access codes to customer sites' }]].map(([ic, txt], i) => {
      const gr = g(p3b.g); const y = p3b.y + 30 + 5 * 52 + 20 + i * 70;
      el('rect', { x: p3b.left - 12, y: y - 40, width: p3b.w - 2 * p3b.pad + 24, height: 60, rx: 10, fill: C.blueSoft, stroke: C.blue, 'stroke-width': 2 }, gr);
      ikon(gr, ic, p3b.left + 16, y - 10, 28, C.blueDeep); T(gr, p3b.left + 48, y - 2, txt, { size: 22, weight: 800, fill: C.pInk });
      const plus = g(gr, { transform: `translate(${p3b.right + 4} ${y - 40})` }); el('circle', { r: 16, fill: C.blue }, plus); T(plus, 0, 7, '+', { size: 24, weight: 800, fill: '#fff', anchor: 'middle' });
      return gr;
    });
    shot(b2, this.tP2 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 6 die eine Seite aus der Richtlinie ----------
    const b3 = buehne('beispiel-d2', { seed: 89, regalDeckkraft: 0.6 }); this.b3 = b3;
    const rc = b3.cam;
    this.d1b = g(rc);
    const d1b = blatt(this.d1b, { w: 440, h: 580, kicker: { de: 'D1 · RICHTLINIE', en: 'D1 · POLICY' }, titel: { de: 'Richtlinie', en: 'Policy' }, tSize: 32 });
    this.d1Bl = [0, 1, 2].map((i) => { const gr = g(d1b.g); el('rect', { x: d1b.left - 8, y: d1b.y + 20 + i * 120, width: 360, height: 96, rx: 10, fill: '#eef2f8' }, gr); linien(gr, d1b.left + 8, d1b.y + 44 + i * 120, 300, 3, 22, C.pBar2, 9); return gr; });
    this.d2 = g(rc);
    const d2b = blatt(this.d2, { w: 600, h: 620, kicker: { de: 'D2 · EINE SEITE · AUSHANG', en: 'D2 · ONE PAGE · TO POST' } });
    const D2Z = [['cross', { de: 'Was nie hinein darf', en: 'What never goes in' }], ['search', { de: 'Vor der Verwendung prüfen', en: 'Check before use' }], ['question', { de: 'Wen fragen · wohin melden', en: 'Whom to ask · where to report' }]];
    this.d2z = D2Z.map(([ic, txt], i) => { const gr = g(d2b.g); const y = d2b.y + 30 + i * 150; el('rect', { x: d2b.left - 10, y: y - 10, width: d2b.w - 2 * d2b.pad + 20, height: 130, rx: 12, fill: '#eef2f8' }, gr); ikon(gr, ic, d2b.left + 20, y + 24, 30, C.pInk); T(gr, d2b.left + 54, y + 34, txt, { size: 26, weight: 800, fill: C.pInk }); return { g: gr, y }; });
    this.kreuz = [0, 1, 2, 3].map((k) => kaestchen(d2b.g, d2b.left + 70 + k * 56, d2b.y + 30 + 84, 30));
    this.d2P = [linien(d2b.g, d2b.left + 54, d2b.y + 30 + 150 + 62, 380, 2, 24, C.pBar2, 10), linien(d2b.g, d2b.left + 54, d2b.y + 30 + 300 + 62, 380, 2, 24, C.pBar2, 10)];
    this.pfeile = [0, 1, 2].map((i) => el('path', { d: `M 640 ${330 + i * 120} C 820 ${330 + i * 120} 860 ${300 + i * 150} 1030 ${300 + i * 150}`, fill: 'none', stroke: C.blue, 'stroke-width': 4, 'stroke-dasharray': '10 8', 'stroke-linecap': 'round' }, rc));
    this.uebern = pille(rc, { de: 'aus der Richtlinie übernommen', en: 'taken from the policy' }, { icon: 'link', col: C.blue, size: 22 });
    shot(b3, this.tD2 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 7 Nachweisseite ----------
    const b4 = buehne('beispiel-d7', { seed: 97, regalDeckkraft: 0.6 }); this.b4 = b4;
    const nc = b4.cam;
    this.d7 = g(nc);
    const d7b = blatt(this.d7, { w: 820, h: 660, kicker: { de: 'D7 · NACHWEISSEITE · MUSTER ELEKTROTECHNIK', en: 'D7 · EVIDENCE SUMMARY · EXAMPLE ELECTRICAL' } });
    this.d7b = d7b;
    this.datumT = T(d7b.g, d7b.left, d7b.y + 30, { de: 'STAND 30.10.2026', en: 'AS OF 30 OCT 2026' }, { mono: 1, size: 22, fill: C.pInk, ls: '0.06em' });
    this.dokNr = g(d7b.g); T(this.dokNr, d7b.right - 180, d7b.y + 30, { de: 'DOK.-NR.', en: 'DOC NO.' }, { mono: 1, size: 18, fill: C.pMuted, ls: '0.06em', anchor: 'end' }); el('rect', { x: d7b.right - 168, y: d7b.y + 14, width: 168, height: 22, rx: 6, fill: C.pBar2 }, this.dokNr);
    const ST = [['g', { de: 'Geregelt', en: 'Regulated' }, C.greenDeep, 'check'], ['p', { de: 'Geplant', en: 'Planned' }, C.blueDeep, 'clock'], ['o', { de: 'Offen', en: 'Open' }, C.amberDeep, 'unknown']];
    const REIHE = ['g', 'g', 'p', 'o', 'g', 'p', 'o'];
    this.d7z = REIHE.map((k, i) => {
      const s = ST.find((x) => x[0] === k); const gr = g(d7b.g); const y = d7b.y + 88 + i * 62;
      el('rect', { x: d7b.left, y: y - 12, width: 360 - (i * 41) % 120, height: 12, rx: 6, fill: C.pBar2 }, gr);
      const pl = g(gr, { transform: `translate(${d7b.right - 110} ${y - 6})` });
      const r = el('rect', { x: -96, y: -22, width: 192, height: 44, rx: 22, fill: k === 'o' ? C.amberSoft : k === 'g' ? C.greenSoft : C.blueSoft, stroke: s[2], 'stroke-width': 2 }, pl);
      if (k === 'o') r.setAttribute('stroke-dasharray', '8 6');
      ikon(pl, s[3], -66, 0, 24, s[2]); T(pl, -44, 8, s[1], { size: 22, weight: 800, fill: s[2] });
      return { g: gr, pl, k };
    });
    this.d7Over = pille(nc, { de: 'Geregelt · Geplant · Offen', en: 'Regulated · Planned · Open' }, { size: 26, col: C.muted });
    this.wv = pille(nc, { de: 'Wiedervorlage: 12 Monate und bei jedem Anlass', en: 'Review: after 12 months and on every occasion' }, { icon: 'cycle', col: C.blue, size: 24 });
    shot(b4, this.tD7 - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [bG, bB, bM, b1, b2, b3, b4];

    // ---------- Einblendungen ----------
    kopf(this.tGen, this.tInh - 0.6, K, '');
    kopf(this.tInh - 0.3, this.tMemo - 0.3, K, { de: 'Muster Elektrotechnik e.U.', en: 'Example Electrical Ltd' });
    kopf(this.tMemo, this.tP1 - 0.3, K, { de: 'Das Memo: Lampe Rot', en: 'The memo: red lamp' });
    kopf(this.tP1, this.tP2 - 0.3, K, { de: '§ 1 Tools und Zugang', en: '§ 1 Tools and access' });
    kopf(this.tP2, this.tD2 - 0.3, K, { de: '§ 2 und § 3', en: '§ 2 and § 3' });
    kopf(this.tD2, this.tD7 - 0.3, K, { de: 'Die eine Seite', en: 'The one page' });
    kopf(this.tD7, this.tEnde - 0.3, K, { de: 'Die Nachweisseite', en: 'The evidence summary' });
  },

  zeichnen(t) {
    if (this.bG.vis) {
      kamera(this.bG, [960, 540], 1);
      const fi = P(t, this.tGen - 0.3, 0.7, E.out); tr(this.form, 0, (1 - fi) * 40); O(this.form, fi);
      const tz = [this.tMuster, this.tAT, this.tZehn];
      this.felder.forEach((f, i) => typeText(f.tx, f.wert, t, tz[i] - 0.1, 0.6));
      rein(this.vorbelegt, 1300, 400, t, this.tErf, 0.45);
      const sk0 = P(t, this.tKeine, 0.35, E.back); tr(this.stempelG, 1500, 640, lerp(1.6, 1, sk0), -8); O(this.stempelG, P(t, this.tKeine, 0.15));
    }
    if (this.bB.vis) {
      const B = this.B;
      const k = fahrt(t, { f: [1680, 470], z: 0.6 }, [
        { t: this.tDreiP - 0.3, d: 1.0, f: [1540, 520], z: 1.0 },
        { t: this.tZwei - 0.3, d: 1.0, f: [2740, 520], z: 1.05 },
        { t: this.tNiemand - 0.4, d: 0.9, f: [1680, 470], z: 0.6 },
      ]);
      kamera(this.bB, k.f, k.z);
      const an = P(t, this.tDreiP + 0.2, 0.4);
      B.monitore.forEach((m, i) => bildschirm(m, P(t, this.tDreiP + 0.2 + i * 0.15, 0.35)));
      bildschirm(B.monL, 0);
      B.telefone.forEach((f, i) => { const kk = P(t, this.tZwei + i * 0.2, 0.35); O(f.dim, 0.78 * (1 - kk)); O(f.glow, 0.12 + 0.88 * kk); });
      betriebLeben(B, t, { tippen: { figA: [this.tDreiP + 0.3, 1e9], figB: [this.tDreiP + 0.4, 1e9], figC: [this.tDreiP + 0.5, 1e9] } });
      const groesse = 1 / k.z;
      const rolle = (p, x, y, t0, bis) => { tr(p, x, y - (1 - P(t, t0, 0.45, E.out)) * 30, groesse); O(p, fenster(t, t0, 0.4, bis, 0.4)); };
      rolle(this.rInh, 680, 220, this.tInh, this.tDreiP - 0.3);
      rolle(this.rBuero, 1540, 220, this.tBuero, this.tDreiP - 0.3);
      rolle(this.rMont, 2620, 220, this.tMont, this.tDreiP - 0.3);
      rolle(this.rLehr, 2840, 380, this.tLehr, this.tDreiP - 0.3);
      this.verwP.forEach((p, i) => { const m = B.monitore[i]; rolle(p, m.x + 86, m.y - 60, this.tVerw[i], this.tZwei - 0.3); });
      this.privP.forEach((p, i) => { const f = B.telefone[i]; rolle(p, f.x - 60, 420, this.tPrivat + i * 0.2, this.tNiemand - 0.3); });
      const st = P(t, this.tNiemand + 0.3, 0.4, E.back); tr(this.stempelB, 1680, 560, lerp(1.8, 1, st) / k.z * 1.3, -6); O(this.stempelB, P(t, this.tNiemand + 0.3, 0.15));
    }
    if (this.bM.vis) {
      kamera(this.bM, [960, 540], 1);
      const M = this.memo; const mi = P(t, this.tMemo - 0.3, 0.7, E.out);
      tr(M.g, 620, 560 + (1 - mi) * 40, 1, -2); O(M.g, mi);
      M.qRows.forEach((q, i) => { const k = P(t, this.tMemo + 0.3 + i * 0.12, 0.2); O(q.sel, k); });
      O(M.band, P(t, this.tRot - 0.3, 0.3));
      M.lampe.setAttribute('r', (13 + 3 * puls(t, this.tRot, 1.2, 9)).toFixed(1)); O(this.lampRing, P(t, this.tRot, 0.3) * (0.6 + 0.4 * Math.sin(t * 5)));
      rein(this.kontenP, 620, 958, t, this.tWeil, 0.45);
      const ei = P(t, this.tErster - 0.2, 0.6, E.out); O(this.erster, ei); tr(this.erster, (1 - ei) * 40, 0);
      O(this.e1, P(t, this.tKonten - 0.1, 0.4)); O(this.tgl, P(t, this.tKonten + 0.4, 0.4));
      const tk = P(t, this.tTraining - 0.2, 0.4); this.tglKnob.setAttribute('cx', lerp(15, -15, tk).toFixed(1)); this.tglTrack.setAttribute('fill', tk > 0.5 ? '#3a4660' : C.blue); setText(this.tglTxt, tk > 0.5 ? { de: 'AUS', en: 'OFF' } : { de: 'AN', en: 'ON' });
      O(this.e2, P(t, this.tSeite - 0.1, 0.4));
    }
    if (this.b1.vis) {
      kamera(this.b1, [960, 540], 1);
      const di = P(t, this.tP1 - 0.2, 0.6, E.out); tr(this.d1, 330, 560 + (1 - di) * 40, 1, -1.5); O(this.d1, di);
      O(this.mont.g, P(t, this.tFuer2 - 0.3, 0.5)); arme(this.mont, 18, 131, -6, 0, 3 * Math.sin(t)); O(this.mont.dim, 0); O(this.mont.glow, 0.7);
      const zt = [this.tEntweder, this.tWie, this.tOder];
      this.gab.forEach((w, i) => { zeichne(w.p, i === 1 ? 0.92 * P(t, this.tWie - 0.1, 0.6) : P(t, zt[i] - 0.1, 0.8), null); w.p.setAttribute('stroke-dasharray', i === 2 && P(t, zt[i] + 0.8, 0.01) > 0 ? '16 12' : w.p.getAttribute('stroke-dasharray')); });
      const za = P(t, this.tEntweder + 0.5, 0.45, E.out); O(this.zielA, za); tr(this.zielA, (1 - za) * 30, 0);
      const zb = P(t, this.tOder + 0.6, 0.45, E.out); O(this.zielB, zb); tr(this.zielB, (1 - zb) * 30, 0);
      const sp = P(t, this.tWie + 0.4, 0.4, E.back); sk(this.sperre, 1213, 600, Math.max(0.01, sp)); O(this.sperre, P(t, this.tWie + 0.4, 0.15));
      rein(this.wieBisher, 1450, 600, t, this.tWie + 0.5, 0.45);
    }
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      const p2 = P(t, this.tP2 - 0.2, 0.6, E.out); tr(this.p2, 560, 570 + (1 - p2) * 40, 1, -1); O(this.p2, p2);
      this.vw.forEach((v, i) => O(v, P(t, this.tU[i] - 0.1, 0.35)));
      this.ausg.forEach((a, i) => { O(a.g, P(t, this.tBew - 0.1 + i * 0.5, 0.35)); a.st.setAttribute('width', (a.w * P(t, this.tAus, 0.5)).toFixed(1)); });
      const p3 = P(t, this.tP3 - 0.2, 0.7, E.out); tr(this.p3, lerp(1700, 1430, p3), 570, 1, lerp(5, 1.5, p3)); O(this.p3, p3);
      this.neu.forEach((n, i) => { const t0 = i ? this.tCodes : this.tKalk; const k = P(t, t0 - 0.1, 0.5, E.out); tr(n, (1 - k) * 60, 0); O(n, k); });
    }
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      const di = P(t, this.tD2 - 0.2, 0.6, E.out); tr(this.d1b, 400, 560 + (1 - di) * 40, 1, -1.5); O(this.d1b, di);
      const d2 = P(t, this.tD2 + 0.4, 0.7, E.out); tr(this.d2, 1340, 560 + (1 - d2) * 40, 1, 1.2); O(this.d2, d2);
      const zt = [this.tNie, this.tGepr, this.tGefragt];
      this.pfeile.forEach((p, i) => { zeichne(p, P(t, zt[i] - 0.2, 0.6), null); if (P(t, zt[i] + 0.5, 0.01) > 0) { p.setAttribute('stroke-dasharray', '10 8'); p.setAttribute('stroke-dashoffset', (-t * 30).toFixed(1)); } });
      this.d1Bl.forEach((b, i) => O(b, 0.45 + 0.55 * fenster(t, zt[i] - 0.3, 0.3, zt[i] + 2.5, 0.5)));
      this.d2z.forEach((z, i) => O(z.g, 0.25 + 0.75 * P(t, zt[i], 0.4)));
      this.kreuz.forEach((kk, i) => { const hk = P(t, this.tAnkreuz + 0.2 + i * 0.2, 0.3, E.back); kk.haken.setAttribute('transform', `scale(${Math.max(0.01, hk).toFixed(3)})`); O(kk.haken, P(t, this.tAnkreuz + 0.2 + i * 0.2, 0.15)); });
      this.d2P.forEach((ls, i) => ls.forEach((l) => O(l, P(t, (i ? this.tVorf : this.tGepr) + 0.2, 0.4))));
      rein(this.uebern, 900, 210, t, this.tWider - 0.4, 0.45);
    }
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      const di = P(t, this.tD7 - 0.2, 0.7, E.out); tr(this.d7, 960, 560 + (1 - di) * 40, 1, -1); O(this.d7, di);
      O(this.datumT, P(t, this.tDatiert, 0.4)); O(this.dokNr, P(t, this.tDokNr, 0.4));
      this.d7z.forEach((z, i) => { O(z.g, P(t, this.tZeile + i * 0.15, 0.3)); const sp = P(t, this.tStatus - 0.2 + i * 0.12, 0.35, E.back); z.pl.setAttribute('transform', `translate(${this.d7b.right - 110} ${this.d7b.y + 82 + i * 62}) scale(${Math.max(0.01, sp * (z.k === 'o' ? 1 + 0.06 * Math.sin(t * 5) * P(t, this.tOffen, 0.4) : 1)).toFixed(3)})`); });
      rein(this.d7Over, 960, 940, t, this.tStatus, 0.45, this.tWv - 0.3);
      rein(this.wv, 960, 940, t, this.tWv, 0.45);
    }
  },
});
