// Teil 3a · Womit Sie anfangen: Memo und Reihenfolge, Schritt 1 Bestand, Schritt 2 Konten (aus der Probe 01, Note 1),
// dann die eine Seite zum Aushängen und die Zweifelsregel. Absätze 9 bis 16 des Skripts.
// Die Probe war in Sekunden ab ihrem Ausschnitt getaktet. w(x) bildet diese Probezeit über Wortanker auf die Tonspur ab
// (stückweise linear zwischen den Ankern), damit das abgenommene Timing auch mit einer anderen Stimme stimmt.
akt({
  name: 'anfangen',
  bauen() {
    const K = { de: '2 · WOMIT SIE ANFANGEN', en: '2 · WHERE YOU START' };
    // ---------- Wortanker und Zeitabbildung ----------
    const paare = [];
    const A = (pt, de, en) => { const s = cue({ de, en }).s; paare.push([pt, s]); return s; };
    const AB = (pt) => { const b = belegt(); paare.push([pt, b.s]); return b; };
    A(0.0, 'Das freie Memo stellt', 'The free memo asks');
    A(1.64, 'sieben Fragen', 'seven questions');
    A(3.24, 'den einen Schritt', 'the one step');
    A(4.16, 'zuerst kommt', 'comes first');
    A(5.06, 'Wir gehen', 'We walk');
    A(7.24, 'die Reihenfolge kommt', 'the order is the point');
    A(9.16, 'Schritt eins|Schritt 1', 'Step one|Step 1');
    A(11.14, 'Welche Tools', 'Which tools');
    A(13.2, 'Mit welchen Konten', 'with which accounts');
    A(14.36, 'Eine Zeile je', 'One row per');
    A(16.24, 'Unklar ist', 'Unclear is a');
    A(18.02, 'ein Befund', 'a finding');
    A(20.46, 'Schritt zwei|Schritt 2', 'Step two|Step 2');
    A(22.08, 'privaten oder unbekannten', 'private or unknown');
    A(24.78, 'die erste Stelle', 'puts it first');
    A(26.52, 'Konten für die freigegebenen', 'business accounts for the approved'); // Whisper hört „Betriebliche“ hier falsch, deshalb ab „Konten“
    A(28.66, 'abgeschaltetem Training', 'switched off');
    A(31.2, 'Funktionsadresse', 'functional address');
    A(32.88, 'ohne Personennamen', 'without personal names');
    A(34.06, 'Keine privaten Konten', 'No private accounts');
    const F1 = AB(36.8);
    A(39.4, 'dass Beschäftigte', 'that employees');
    A(43.36, 'Profile', 'profiles');
    A(46.12, 'dass Accounts so', 'accounts should be set');
    A(49.18, 'Trainingszwecken', 'used for training');
    const A1 = AB(51.18);
    A(53.38, 'nur das Tool', 'only names the tool');
    A(54.54, 'erlaubt', 'permits');
    A(56.46, 'privaten Zugang', 'private account');
    A(57.38, 'Die Regel muss', 'The rule must');
    A(58.44, 'Tool und', 'the tool and');
    A(59.18, 'Zugangsweg', 'access path');
    this.tSeite = cue({ de: 'Und hängen Sie die eine Seite|hängen Sie die eine Seite', en: 'And post the one page' }).s;
    paare.push([61.0, this.tSeite]);
    paare.sort((a, b) => a[0] - b[0]);
    this.w = (x) => { if (x <= paare[0][0]) return paare[0][1] + (x - paare[0][0]); for (let i = 1; i < paare.length; i++) if (x <= paare[i][0]) { const [a0, b0] = paare[i - 1], [a1, b1] = paare[i]; return b0 + (x - a0) * (b1 - b0) / Math.max(1e-6, a1 - a0); } const [a, b] = paare[paare.length - 1]; return b + (x - a); };
    const w = this.w;
    this.tStart = w(0); this.tF1 = F1.s; this.tA1 = A1.s;
    // eine Seite und Zweifelsregel
    const c = (de, en) => cue({ de, en }).s;
    this.tNie = c('was nie in ein Tool', 'what never goes into');
    this.tZugang = c('über welchen Zugang', 'whatever the access');
    this.tR = [c('Angaben, mit denen', 'data by which'), c('Zugangsdaten und Passwörter', 'access data and passwords'), c('Kalkulationen, Preise', 'calculations, prices'), c('Gesundheitsangaben', 'health data'), c('Unterlagen Dritter', 'documents of third parties')];
    this.tZweifel = c('mit der Zweifelsregel', 'the rule of doubt');
    this.tImZw = c('Zweifel wird nichts', 'in case of doubt');
    this.tPerson = c('benannte Person', 'named person');
    const A2 = belegt(); this.tA2 = A2.s;
    this.tUnvoll = c('unvollständig', 'incomplete');
    this.tKatalog = c('kein Katalog', 'no catalogue');
    this.tEnde = cue({ de: 'Schritt drei|Schritt 3', en: 'Step three|Step 3' }, { halten: true }).s;
    // Ton (Langfassung 03.11.2026)
    klang(this.tSeite, 'paper_slide'); klang(this.tNie, 'strike', { laut: 0.6 }); (this.tR || []).forEach((t) => klang(t, 'pop', { laut: 0.5 }));
    klang(this.tImZw, 'tick'); klang(this.tPerson, 'click_soft');

    // ---------- Bühne 1: Memo und Weg ----------
    const bM = buehne('anfangen-weg', { seed: 1 }); this.bM = bM;
    this.memo = bauMemo(bM.cam);
    this.lab7 = T(bM.cam, 880, 300, { de: '7 Fragen', en: '7 questions' }, { size: 48, weight: 800 });
    this.lab1 = T(bM.cam, 880, 830, { de: '1 Schritt zuerst', en: '1 step first' }, { size: 48, weight: 800 });
    this.lab7sub = T(bM.cam, 882, 340, { de: 'ZU IHRER LAGE', en: 'ABOUT YOUR SITUATION' }, { mono: 1, size: 20, fill: C.muted, ls: '0.1em' });
    this.lab1sub = T(bM.cam, 882, 870, { de: 'DANN DIE REIHENFOLGE', en: 'THEN THE ORDER' }, { mono: 1, size: 20, fill: C.muted, ls: '0.1em' });
    this.weg = bauWeg(bM.cam);
    this.badges = g(this.weg.nodes[0].g);
    this.badgeP = g(this.badges); this.badgeU = g(this.badges);
    [[this.badgeP, 'privat', -100], [this.badgeU, 'unklar', 100]].forEach(([gr, kind, dx]) => {
      const col = kind === 'privat' ? C.muted : C.amber;
      const r = el('rect', { x: -84, y: -26, width: 168, height: 52, rx: 26, fill: C.raised, stroke: col, 'stroke-width': 2.5 }, gr);
      if (kind === 'unklar') r.setAttribute('stroke-dasharray', '9 6');
      const ic = g(gr, { transform: 'translate(-50 0)' }); ICON[kind](ic, 26, col);
      T(gr, -28, 8, kind === 'privat' ? { de: 'privat', en: 'private' } : { de: 'unklar', en: 'unclear' }, { mono: 1, size: 21, fill: C.ink });
      gr.dx = dx;
    });
    this.tile = g(bM.cam); kachel(this.tile, '1', C.blue, 72);
    shot(bM, this.tStart - 0.4, { typ: 'blende', d: 0.7 });
    const P0 = wegPunkt(0);

    // ---------- Bühne 2: der Betrieb und das Tool-Register ----------
    const bO = buehne('anfangen-betrieb', { seed: 2 }); this.bO = bO;
    const oc = bO.cam;
    el('rect', { x: 96, y: 246, width: 1170, height: 610, rx: 22, fill: C.wall }, oc);
    el('rect', { x: 96, y: 846, width: 1170, height: 14, rx: 5, fill: C.floor }, oc);
    T(oc, 126, 290, { de: 'MUSTER ELEKTROTECHNIK E.U. · ERFUNDEN', en: 'EXAMPLE ELECTRICAL LTD · FICTIONAL' }, { mono: 1, size: 18, fill: C.dim, ls: '0.1em' });
    ordnerRegal(oc, 150, 324, 11); fenster2(oc, 700, 318); tuer(oc, 1062, 470);
    this.figA = seated(oc, 300, 772, BESETZUNG.a);
    this.figB = seated(oc, 718, 772, BESETZUNG.b);
    tisch(oc, 236, 566); tisch(oc, 654, 984);
    el('rect', { x: 386, y: 690, width: 70, height: 10, rx: 3, fill: '#2a3858' }, oc);
    el('rect', { x: 804, y: 690, width: 70, height: 10, rx: 3, fill: '#2a3858' }, oc);
    this.monA = monitor(oc, 384, 566, 172, 108, iconSpark);
    this.monB = monitor(oc, 802, 566, 172, 108, iconTranslate);
    this.figC = stehend(oc, 1150, 846, BESETZUNG.monteur1);
    const TAGS = [['betrieb', 470, 438], ['privat', 888, 438], ['unklar', 1150, 372]];
    const tagWort = { betrieb: { de: 'Betrieb', en: 'business' }, privat: { de: 'privat', en: 'private' }, unklar: { de: 'unklar', en: 'unclear' } };
    this.tags = TAGS.map(([kind, x, y]) => {
      const gr = g(oc);
      el('line', { x1: 0, y1: 0, x2: 0, y2: 22, stroke: C.line, 'stroke-width': 2 }, gr);
      const col = kind === 'betrieb' ? C.blue : kind === 'privat' ? C.muted : C.amber;
      const r = el('rect', { x: -98, y: 22, width: 196, height: 52, rx: 12, fill: C.raised, stroke: col, 'stroke-width': 2.5 }, gr);
      if (kind === 'unklar') r.setAttribute('stroke-dasharray', '9 6');
      const ic = g(gr, { transform: 'translate(-66 48)' }); ICON[kind](ic, 28, col);
      T(gr, -42, 56, tagWort[kind], { mono: 1, size: 22, fill: C.ink });
      return { g: gr, x, y };
    });
    this.REG = { x: 1588, y: 572, r: 1.4 };
    this.reg = g(oc);
    const reg = this.reg;
    el('rect', { x: -240 + 14, y: -262 + 10, width: 480, height: 524, rx: 6, fill: C.paperBack }, reg);
    el('rect', { x: -240, y: -262, width: 480, height: 524, rx: 6, fill: C.paper, filter: 'url(#shadow)' }, reg);
    T(reg, -204, -210, { de: 'TOOL-REGISTER', en: 'TOOL REGISTER' }, { mono: 1, size: 17, fill: C.pInk, ls: '0.1em' });
    T(reg, 204, -210, { de: 'STAND 30.10.2026', en: 'AS OF 30 OCT 2026' }, { mono: 1, size: 14, fill: C.pMuted, anchor: 'end' });
    el('rect', { x: -204, y: -192, width: 408, height: 1.5, fill: C.pLine }, reg);
    T(reg, -204, -160, 'TOOL', { mono: 1, size: 14, fill: C.pMuted, ls: '0.1em' });
    T(reg, 40, -160, { de: 'KONTO', en: 'ACCOUNT' }, { mono: 1, size: 14, fill: C.pMuted, ls: '0.1em' });
    this.ROWY = [-92, -4, 84];
    const ROWS = [
      { name: { de: 'Textassistent', en: 'Text assistant' }, glyph: iconSpark, kind: 'betrieb', col: C.blueDeep },
      { name: { de: 'Übersetzer', en: 'Translator' }, glyph: iconTranslate, kind: 'privat', col: C.pMuted },
      { name: { de: 'Chat-App', en: 'Chat app' }, glyph: iconChat, kind: 'unklar', col: C.amberDeep },
    ];
    this.rows = ROWS.map((r, i) => {
      const y = this.ROWY[i];
      el('rect', { x: -204, y: y + 40, width: 408, height: 1, fill: '#e3e7ee' }, reg);
      const gr = g(reg);
      const gg = g(gr, { transform: `translate(-184 ${y})` }); r.glyph(gg, 30, C.pInk);
      T(gr, -156, y + 9, r.name, { size: 25, weight: 700, fill: C.pInk });
      const ic = g(gr, { transform: `translate(66 ${y})` }); ICON[r.kind](ic, 28, r.col);
      T(gr, 92, y + 8, tagWort[r.kind], { mono: 1, size: 21, fill: r.col });
      return { g: gr, y };
    });
    this.frame3 = el('rect', { x: 40, y: this.ROWY[2] - 30, width: 180, height: 60, rx: 12, fill: 'none', stroke: C.amberLine, 'stroke-width': 3, 'stroke-dasharray': '10 7' }, reg);
    this.underline3 = el('rect', { x: -204, y: this.ROWY[2] + 30, width: 0, height: 4, rx: 2, fill: C.blue }, reg);
    this.befund = g(reg);
    const bft = T(this.befund, 115, this.ROWY[2] + 71, { de: 'BEFUND', en: 'FINDING' }, { mono: 1, size: 19, fill: '#0a0c10', anchor: 'middle', ls: '0.1em' });
    const bw = Math.max(150, breite(bft) + 40);
    this.befund.insertBefore(el('rect', { x: 115 - bw / 2, y: this.ROWY[2] + 44, width: bw, height: 40, rx: 20, fill: C.amber }), bft);
    this.tokens = ROWS.map((r) => {
      const gr = g(oc);
      el('rect', { x: -60, y: -26, width: 120, height: 52, rx: 14, fill: C.paper, filter: 'url(#shadowS)' }, gr);
      const a = g(gr, { transform: 'translate(-28 0)' }); r.glyph(a, 26, C.pInk);
      const b = g(gr, { transform: 'translate(24 0)' }); ICON[r.kind](b, 26, r.kind === 'unklar' ? C.amberLine : r.col);
      return gr;
    });
    shot(bO, w(9.55), { typ: 'kreis', d: 1.3, p: P0 });
    shot(bM, w(20.25), { typ: 'kreisRaus', d: 1.2, p: P0 });

    // ---------- Bühne 3: Zugangswege, Anbieter, Regel ----------
    const bA = buehne('anfangen-zugang', { seed: 3, regalDeckkraft: 0.8 }); this.bA = bA;
    const ac = bA.cam;
    el('rect', { x: 60, y: 868, width: 1800, height: 6, rx: 3, fill: '#16213a' }, ac);
    this.figB2 = seated(ac, 252, 792, BESETZUNG.b);
    el('rect', { x: 180, y: 720, width: 350, height: 22, rx: 6, fill: C.desk }, ac);
    el('rect', { x: 196, y: 742, width: 14, height: 126, fill: '#16203a' }, ac); el('rect', { x: 500, y: 742, width: 14, height: 126, fill: '#16203a' }, ac);
    el('rect', { x: 338, y: 710, width: 70, height: 10, rx: 3, fill: '#2a3858' }, ac);
    this.monB2 = monitor(ac, 330, 586, 172, 108, iconSpark);
    const LT = 'M 502 640 L 600 640 C 690 640 680 470 770 470 L 1482 470';
    const LB = 'M 502 640 L 600 640 C 690 640 680 790 770 790 L 1482 790';
    this.laneTop = el('path', { d: LT, fill: 'none', stroke: C.lane, 'stroke-width': 16, 'stroke-linecap': 'round' }, ac);
    this.laneBot = el('path', { d: LB, fill: 'none', stroke: C.lane, 'stroke-width': 16, 'stroke-linecap': 'round' }, ac);
    this.laneTopHi = el('path', { d: LT, fill: 'none', stroke: C.amber, 'stroke-width': 16, 'stroke-linecap': 'round' }, ac);
    this.laneBotHi = el('path', { d: LB, fill: 'none', stroke: C.blue, 'stroke-width': 16, 'stroke-linecap': 'round' }, ac);
    this.lenT = this.laneTop.getTotalLength(); this.lenB = this.laneBot.getTotalLength();
    const dotLayer = g(ac);
    const pool = (n, fill) => Array.from({ length: n }, () => el('rect', { x: -7, y: -9, width: 14, height: 18, rx: 2.5, fill }, dotLayer));
    this.dotsT = pool(30, C.paper); this.dotsB = pool(40, C.paper); this.dotsA = pool(12, C.blue);
    this.gate = g(ac);
    el('rect', { x: 806, y: 380, width: 6, height: 130, rx: 3, fill: C.line }, this.gate);
    el('rect', { x: 850, y: 380, width: 6, height: 130, rx: 3, fill: C.line }, this.gate);
    el('rect', { x: 800, y: 372, width: 62, height: 12, rx: 4, fill: C.line }, this.gate);
    this.gateBar = g(this.gate);
    el('rect', { x: 814, y: 0, width: 34, height: 84, rx: 6, fill: C.muted }, this.gateBar);
    for (let i = 0; i < 3; i++) el('rect', { x: 818, y: 12 + i * 24, width: 26, height: 7, rx: 3, fill: C.dim }, this.gateBar);
    this.gateLab = T(ac, 790, 558, { de: 'NICHT FÜR DIE ARBEIT', en: 'NOT FOR WORK' }, { mono: 1, size: 19, fill: C.muted, ls: '0.06em' });
    const card = (cx, cy, wd, ht, stroke) => { const gr = g(ac); el('rect', { x: cx - wd / 2, y: cy - ht / 2, width: wd, height: ht, rx: 18, fill: C.raised, stroke, 'stroke-width': 3, filter: 'url(#shadowS)' }, gr); return gr; };
    this.cardP = card(1180, 470, 340, 124, '#4a5878');
    { const ic = g(this.cardP, { transform: 'translate(1046 458)' }); iconPerson(ic, 36, C.muted);
      T(this.cardP, 1078, 468, { de: 'Privates Konto', en: 'Private account' }, { size: 28, weight: 800 });
      T(this.cardP, 1046, 512, { de: 'anna.k@privat.example', en: 'anna.k@private.example' }, { mono: 1, size: 18, fill: C.muted }); }
    this.cardB = card(1180, 790, 340, 200, C.blue);
    this.bizCardHi = el('rect', { x: 1004, y: 684, width: 352, height: 212, rx: 22, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, ac);
    { const ic = g(this.cardB, { transform: 'translate(1046 734)' }); iconBuilding(ic, 36, C.blue);
      T(this.cardB, 1078, 744, { de: 'Betriebskonto', en: 'Business account' }, { size: 28, weight: 800 }); }
    this.nameG = g(this.cardB);
    this.nameT = T(this.nameG, 1046, 790, 'Anna K.', { size: 24, weight: 600 });
    this.nameStrike = el('rect', { x: 1044, y: 780, width: 0, height: 3, fill: C.red }, this.nameG);
    this.addrT = T(this.cardB, 1046, 824, '', { mono: 1, size: 19, fill: C.ink });
    el('rect', { x: 1030, y: 842, width: 300, height: 1, fill: 'rgba(226,232,246,0.14)' }, this.cardB);
    T(this.cardB, 1046, 870, 'TRAINING', { mono: 1, size: 16, fill: C.muted, ls: '0.08em' });
    this.trState = T(this.cardB, 1146, 870, { de: 'AN', en: 'ON' }, { mono: 1, size: 16, fill: C.ink, ls: '0.08em' });
    const tgl = g(this.cardB, { transform: 'translate(1300 864)' });
    this.tglTrack = el('rect', { x: -30, y: -15, width: 60, height: 30, rx: 15, fill: C.blue }, tgl);
    this.tglKnob = el('circle', { cx: 15, cy: 0, r: 11, fill: '#fff' }, tgl);
    this.tglRing = el('rect', { x: -40, y: -25, width: 80, height: 50, rx: 25, fill: 'none', stroke: C.blue, 'stroke-width': 3 }, tgl);
    this.tower = g(ac);
    const tw = this.tower;
    T(tw, 1620, 286, { de: 'ANBIETER', en: 'PROVIDER' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.12em' });
    el('rect', { x: 1482, y: 304, width: 276, height: 592, rx: 22, fill: C.surface, stroke: C.edge, 'stroke-width': 3 }, tw);
    this.lights = [];
    for (let r = 0; r < 2; r++) for (let i = 0; i < 9; i++) this.lights.push(el('circle', { cx: 1514 + i * 26, cy: 336 + r * 26, r: 4, fill: C.blue }, tw));
    el('rect', { x: 1500, y: 404, width: 240, height: 140, rx: 12, fill: C.dark }, tw);
    T(tw, 1516, 430, { de: 'VERLAUF', en: 'HISTORY' }, { mono: 1, size: 14, fill: C.dim, ls: '0.1em' });
    el('rect', { x: 1500, y: 730, width: 240, height: 70, rx: 12, fill: C.dark }, tw);
    this.trainBox = el('rect', { x: 1500, y: 822, width: 240, height: 60, rx: 12, fill: C.dark, stroke: '#2a3858', 'stroke-width': 2 }, tw);
    T(tw, 1518, 858, 'TRAINING', { mono: 1, size: 16, fill: C.muted, ls: '0.08em' });
    this.trainState = T(tw, 1722, 858, { de: 'AUS', en: 'OFF' }, { mono: 1, size: 16, fill: C.ink, anchor: 'end', ls: '0.08em' });
    el('rect', { x: 1616, y: 800, width: 8, height: 22, fill: '#2a3858' }, tw);
    const valve = g(tw, { transform: 'translate(1620 811)' });
    el('circle', { r: 13, fill: C.surface, stroke: C.muted, 'stroke-width': 3 }, valve);
    this.valveBar = el('rect', { x: -10, y: -2.5, width: 20, height: 5, rx: 2.5, fill: C.muted }, valve);
    this.valveRing = el('circle', { cx: 1620, cy: 811, r: 26, fill: 'none', stroke: C.blue, 'stroke-width': 3 }, tw);
    this.pile = Array.from({ length: 7 }, () => { const gr = g(tw); el('rect', { x: -22, y: -28, width: 44, height: 56, rx: 4, fill: C.paper, filter: 'url(#shadowS)' }, gr); for (let k = 0; k < 3; k++) el('rect', { x: -14, y: -16 + k * 11, width: 28 - k * 6, height: 5, rx: 2.5, fill: C.pBar2 }, gr); return gr; });
    this.profile = g(tw);
    el('circle', { cx: 0, cy: 0, r: 120, fill: 'url(#gRed)' }, this.profile);
    el('rect', { x: -104, y: -56, width: 208, height: 112, rx: 14, fill: C.raised, stroke: C.red, 'stroke-width': 3 }, this.profile);
    { const ic = g(this.profile, { transform: 'translate(-62 6)' }); iconPerson(ic, 54, C.red); }
    T(this.profile, -26, -20, { de: 'PROFIL', en: 'PROFILE' }, { mono: 1, size: 17, fill: C.red, ls: '0.1em' });
    [0, 1, 2].forEach((k) => el('rect', { x: -26, y: -4 + k * 16, width: 104 - k * 22, height: 7, rx: 3.5, fill: '#7a5266' }, this.profile));
    this.appr = g(ac);
    { const at = T(this.appr, 372, 555, { de: 'FREIGEGEBEN', en: 'APPROVED' }, { mono: 1, size: 16, fill: C.ink, ls: '0.06em' });
      const wd = breite(at) + 66; this.appr.insertBefore(el('rect', { x: 330, y: 528, width: wd, height: 40, rx: 20, fill: C.raised, stroke: C.green, 'stroke-width': 2.5 }), at);
      const ic = g(this.appr, { transform: 'translate(354 548)' }); iconCheck(ic, 22, C.green); this.apprW = wd; }
    this.inst = g(ac);
    el('circle', { cx: 1000, cy: 140, r: 110, fill: 'url(#gPaper)' }, this.inst);
    { const ic = g(this.inst, { transform: 'translate(1000 140)' }); iconInstitution(ic, 96, C.ink); }
    T(this.inst, 1000, 226, { de: 'DATENSCHUTZAUFSICHT · DE', en: 'DATA PROTECTION AUTHORITIES · DE' }, { mono: 1, size: 20, fill: C.muted, anchor: 'middle', ls: '0.08em' });
    this.rec = g(ac);
    el('rect', { x: -32, y: -42, width: 64, height: 84, rx: 4, fill: C.paper, filter: 'url(#shadowS)' }, this.rec);
    el('rect', { x: -20, y: -28, width: 12, height: 12, fill: C.blue }, this.rec);
    [0, 1, 2].forEach((k) => el('rect', { x: -20, y: -6 + k * 12, width: 40 - k * 8, height: 5, rx: 2.5, fill: C.pBar2 }, this.rec));
    el('circle', { cx: 0, cy: -42, r: 6, fill: C.blue }, this.rec);
    this.rule = g(ac);
    el('line', { x1: 0, y1: -260, x2: 0, y2: -118, stroke: C.line, 'stroke-width': 2 }, this.rule);
    el('rect', { x: -230 + 12, y: -118 + 8, width: 460, height: 236, rx: 6, fill: C.paperBack }, this.rule);
    el('rect', { x: -230, y: -118, width: 460, height: 236, rx: 6, fill: C.paper, filter: 'url(#shadow)' }, this.rule);
    T(this.rule, -196, -76, { de: 'REGEL · KI-NUTZUNG', en: 'RULE · AI USE' }, { mono: 1, size: 16, fill: C.pMuted, ls: '0.1em' });
    el('rect', { x: -196, y: -60, width: 392, height: 1.5, fill: C.pLine }, this.rule);
    this.r1 = T(this.rule, -196, -10, '', { size: 30, weight: 800, fill: C.pInk });
    this.r1u = el('rect', { x: -196, y: 4, width: 0, height: 5, rx: 2.5, fill: C.blue }, this.rule);
    this.r2 = T(this.rule, -196, 54, '', { size: 30, weight: 800, fill: C.blueDeep });
    this.r1full = T(this.rule, -2000, -2000, { de: 'Erlaubt: Textassistent', en: 'Permitted: text assistant' }, { size: 30, weight: 800 }); this.r1W = breite(this.r1full);
    this.conn1 = el('path', { d: 'M 752 185 C 600 185 562 420 562 626', fill: 'none', stroke: C.amber, 'stroke-width': 4, 'stroke-dasharray': '12 10', 'stroke-linecap': 'round' }, ac);
    this.conn1dot = el('circle', { cx: 562, cy: 640, r: 9, fill: C.amber }, ac);
    this.conn2 = el('path', { d: 'M 1208 247 L 1386 247 Q 1414 247 1414 275 L 1414 776', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round' }, ac);
    this.conn2dot = el('circle', { cx: 1414, cy: 790, r: 10, fill: C.blue }, ac);
    this.c2len = this.conn2.getTotalLength();
    shot(bA, w(25.25), { typ: 'kreis', d: 1.2, p: P0 });
    // Datenströme (Probezeiten, abgebildet)
    this.EM_T = emits([[w(23.0), w(33.2)], [w(55.0), w(58.2)]], 0.46);
    this.EM_B = emits([[w(34.5), w(60.6)]], 0.44);
    this.EM_A = emits([[w(48.6), w(50.4)]], 0.5);

    // ---------- Bühne 4: die eine Seite ----------
    const bS = buehne('anfangen-seite', { seed: 31, regalDeckkraft: 0.7 }); this.bS = bS;
    this.seite = g(bS.cam);
    const sb = blatt(this.seite, { w: 620, h: 700, kicker: { de: 'EINE SEITE · ZUM AUSHÄNGEN', en: 'ONE PAGE · TO POST' }, titel: { de: 'Was nie in ein Tool kommt', en: 'What never goes into a tool' }, tSize: 32 });
    el('circle', { cx: 0, cy: sb.y0 + 2, r: 9, fill: C.blue }, this.seite);
    const ZEILEN = [
      ['id', { de: 'Angaben, mit denen eine Person erkennbar ist', en: 'Data that identify a person' }],
      ['key', { de: 'Zugangsdaten und Passwörter', en: 'Access data and passwords' }],
      ['calc', { de: 'Kalkulationen, Preise, Verträge, Kundenlisten', en: 'Calculations, prices, contracts, customer lists' }],
      ['pulse', { de: 'Gesundheitsangaben', en: 'Health data' }],
      ['sealed', { de: 'Unterlagen Dritter, vertraulich übergeben', en: 'Third-party documents given in confidence' }],
    ];
    this.SY = ZEILEN.map((_, i) => sb.y + 20 + i * 78);
    this.szeilen = ZEILEN.map(([ic, txt], i) => {
      const y = this.SY[i], gr = g(sb.g);
      const hi = el('rect', { x: sb.left - 14, y: y - 4, width: sb.w - 2 * sb.pad + 28, height: 70, rx: 12, fill: C.blueSoft }, gr);
      const kreis = el('circle', { cx: sb.left + 26, cy: y + 31, r: 26, fill: C.pInk }, gr);
      ikon(gr, ic, sb.left + 26, y + 31, 30, C.paper);
      const tx = TB(gr, sb.left + 72, y + 26, txt, { size: 23, weight: 700, fill: C.pInk, maxW: sb.w - 2 * sb.pad - 80, lh: 27 });
      if (tx.zeilen === 1) tx.setAttribute('y', y + 39);
      return { g: gr, hi, y };
    });
    this.zband = g(sb.g);
    const zy = this.SY[4] + 94;
    this.zbandR = el('rect', { x: sb.left - 14, y: zy, width: sb.w - 2 * sb.pad + 28, height: 112, rx: 12, fill: C.blue }, this.zband);
    T(this.zband, sb.left + 6, zy + 34, { de: 'IM ZWEIFEL', en: 'IN CASE OF DOUBT' }, { mono: 1, size: 18, fill: '#dfe8ff', ls: '0.1em' });
    TB(this.zband, sb.left + 6, zy + 64, { de: 'nichts eingeben, die benannte Person fragen', en: 'enter nothing, ask the named person' }, { size: 24, weight: 800, fill: '#fff', maxW: sb.w - 2 * sb.pad - 20, lh: 28 });
    this.zbandY = zy; this.sb = sb;
    // rechts: Tool mit Sperre, zwei Zugangswege
    const sc = bS.cam;
    this.sTool = g(sc);
    el('circle', { cx: 1660, cy: 560, r: 190, fill: 'url(#gBlue)' }, this.sTool);
    el('rect', { x: 1560, y: 470, width: 200, height: 180, rx: 16, fill: '#0f1626', stroke: C.edge, 'stroke-width': 4 }, this.sTool);
    el('rect', { x: 1574, y: 484, width: 172, height: 152, rx: 10, fill: '#e3e9f5' }, this.sTool);
    ikon(this.sTool, 'spark', 1660, 560, 64, C.blueDeep);
    T(this.sTool, 1660, 700, { de: 'KI-TOOL', en: 'AI TOOL' }, { mono: 1, size: 20, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    const SLT = 'M 1000 400 C 1200 400 1300 500 1500 500', SLB = 'M 1000 610 C 1200 610 1300 590 1500 590';
    this.sLaneT = el('path', { d: SLT, fill: 'none', stroke: C.amber, 'stroke-width': 10, 'stroke-dasharray': '14 10', 'stroke-linecap': 'round' }, sc);
    this.sLaneB = el('path', { d: SLB, fill: 'none', stroke: C.blue, 'stroke-width': 10, 'stroke-linecap': 'round' }, sc);
    this.sLenT = this.sLaneT.getTotalLength(); this.sLenB = this.sLaneB.getTotalLength();
    this.sLabT = pille(sc, { de: 'privat', en: 'private' }, { icon: 'person', col: C.amber, gestrichelt: true, size: 22 });
    this.sLabB = pille(sc, { de: 'Betrieb', en: 'business' }, { icon: 'building', col: C.blue, size: 22 });
    this.sperre = g(sc);
    this.sperreL = el('rect', { x: 1518, y: 430, width: 12, height: 260, rx: 6, fill: C.red }, this.sperre);
    el('rect', { x: 1500, y: 430, width: 48, height: 260, rx: 12, fill: 'url(#gRed)' }, this.sperre);
    this.sTok = ZEILEN.map(([ic]) => { const gr = g(sc); el('rect', { x: -38, y: -30, width: 76, height: 60, rx: 10, fill: C.paper, filter: 'url(#shadowS)' }, gr); ikon(gr, ic, 0, 0, 38, C.pInk); return gr; });
    this.sBlitz = ZEILEN.map(() => { const gr = g(sc); iconCross(gr, 44, C.red); return gr; });
    // Zweifel: Figur mit unbekanntem Fall, benannte Person
    this.sFig = stehend(sc, 1000, 945, { jacke: BESETZUNG.b.shirt, haar: 'bun', skala: 0.72 });
    this.sUnb = g(sc); el('rect', { x: -38, y: -30, width: 76, height: 60, rx: 10, fill: C.paper }, this.sUnb); iconUnknown(this.sUnb, 40, C.amberDeep);
    this.sPerson = stehend(sc, 1420, 945, { jacke: BESETZUNG.inhaberin.shirt, haar: 'long', skala: 0.72, kragen: '#b9c3d8' });
    this.sPersonP = pille(sc, { de: 'benannte Person', en: 'named person' }, { icon: 'person', col: C.blue, size: 22 });
    this.sFrage = el('path', { d: 'M 1050 720 Q 1210 640 1380 720', fill: 'none', stroke: C.amber, 'stroke-width': 4, 'stroke-dasharray': '10 8', 'stroke-linecap': 'round' }, sc);
    this.sBlase = g(sc); iconQuestion(this.sBlase, 46, C.amber);
    // Auslegung: Fall rutscht durch die Liste
    this.sFall = g(this.seite); el('rect', { x: -30, y: -24, width: 60, height: 48, rx: 8, fill: C.paper, stroke: C.amberLine, 'stroke-width': 2.5 }, this.sFall); iconUnknown(this.sFall, 32, C.amberDeep);
    this.sUnvoll = pille(bS.cam, { de: 'unvollständig', en: 'incomplete' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 24 });
    this.sKatalog = pille(bS.cam, { de: 'kein Katalog trifft alle Fälle', en: 'no catalogue meets every case' }, { col: C.purple, size: 24, marke: 'auslegung' });
    shot(bS, this.tSeite - 0.4, { typ: 'blende', d: 0.8 });
    this.buehnen = [bM, bO, bA, bS];

    // ---------- Einblendungen ----------
    freiesAngebot(this.tStart + 0.3, { de: '/de/memos/wo-anfangen', en: '/memos/where-to-start' });
    kopf(w(0.2), w(8.7), K, '');
    kopf(w(9.16), w(20.2), { de: 'SCHRITT 1', en: 'STEP 1' }, { de: 'Bestand aufnehmen', en: 'Take stock' });
    kopf(w(20.5), this.tSeite - 0.3, { de: 'SCHRITT 2', en: 'STEP 2' }, { de: 'Betriebliche Konten', en: 'Business accounts' });
    kopf(this.tSeite, this.tA2 - 0.3, { de: 'SCHRITT 2 · DAZU', en: 'STEP 2 · AND' }, { de: 'Die eine Seite', en: 'The one page' });
  },

  zeichnen(t) {
    const w = this.w;
    // ---------- Memo und Weg ----------
    if (this.bM.vis) {
      const panK = P(t, w(4.6), w(6.4) - w(4.6));
      kamera(this.bM, lerp2([960, 540], WEG_BLICK.f, panK), 1);
      const M = this.memo;
      const mi = P(t, w(0) - 0.3, 0.7, E.out);
      tr(M.g, 560, 560 + (1 - mi) * 50, 1, -2 - (1 - mi) * 2); O(M.g, mi);
      M.qRows.forEach((q, i) => { const k = P(t, w(1.55) + i * 0.13, 0.22, E.out); O(q.sel, k); q.bar.setAttribute('fill', k > 0.5 ? '#cdd5e3' : C.pBar); });
      O(M.band, P(t, w(3.2), 0.35, E.out));
      const fade7 = Math.min(P(t, w(1.7), 0.4, E.out), 1 - P(t, w(4.9), 0.5));
      tr(this.lab7, 0, (1 - P(t, w(1.7), 0.4, E.out)) * 16); O(this.lab7, fade7); O(this.lab7sub, fade7 * 0.9);
      const fade1 = Math.min(P(t, w(3.35), 0.4, E.out), 1 - P(t, w(4.9), 0.5));
      tr(this.lab1, 0, (1 - P(t, w(3.35), 0.4, E.out)) * 16); O(this.lab1, fade1); O(this.lab1sub, fade1 * 0.9);
      const tk = P(t, w(4.2), 1.1);
      const pos = qb([569, 810], [880, 470], WEG_SLOTS[0], tk);
      tr(this.tile, pos[0], pos[1], lerp(1, 0.62, tk) * (1 + 0.15 * Math.sin(Math.PI * tk)), lerp(-2, 0, tk));
      O(this.tile, Math.min(P(t, w(4.05), 0.2), 1 - P(t, w(5.25), 0.2)));
      const pk = (t > w(7.3) && t < w(8.7)) ? P(t, w(7.3), w(8.7) - w(7.3), E.sine) : -1;
      const head = wegStrecke(this.weg, P(t, w(5.2), 1.7, E.io), pk);
      const swapK = P(t, w(23.85), 1.2, E.io);
      const S = WEG_SLOTS;
      const ueberg = UEBERGANG && (UEBERGANG.von === this.bM || UEBERGANG.nach === this.bM) ? UEBERGANG.k : 0;
      this.weg.nodes.forEach((n, i) => {
        let p = S[i];
        if (i === 0 && swapK > 0) p = qb(S[0], [(S[0][0] + S[1][0]) / 2, 790], S[1], swapK);
        if (i === 1 && swapK > 0) p = qb(S[1], [(S[0][0] + S[1][0]) / 2, 430], S[0], swapK);
        const act0 = i === 0 ? Math.min(P(t, w(5.25), 0.3), 1 - P(t, w(21.45), 0.4)) : 0;
        const act1 = i === 1 ? P(t, w(21.6), 0.4) : 0;
        const near = Math.exp(-Math.pow((head - this.weg.slotAt[i]) / 90, 2));
        const nummer = (i === 0 && swapK > 0.5) ? 2 : (i === 1 && swapK > 0.5) ? 1 : i + 1;
        wegKnoten(n, {
          da: P(t, w(5.25) + i * 0.26, 0.4, E.back), aktiv: Math.max(act0, act1), erledigt: i === 0 ? P(t, w(21.45), 0.4) : 0,
          gross: i === 0 ? P(t, w(9.16), 0.35, E.back) * (1 - P(t, w(21.45), 0.4)) : 0, nah: near, pos: p, nummer,
          nummerDeck: swapK > 0 && swapK < 1 && i < 2 ? Math.abs(swapK - 0.5) * 2 : 1, labAus: clamp(ueberg * 2.5),
        });
      });
      [[this.badgeP, w(22.08)], [this.badgeU, w(22.86)]].forEach(([gr, t0]) => {
        const k = P(t, t0, 0.45, E.back);
        tr(gr, gr.dx, -112 - (1 - k) * 20 + Math.sin((t - t0) * 6) * 3 * (t > t0 && t < t0 + 1.2 ? 1 : 0), Math.max(0.01, k), 0); O(gr, Math.min(P(t, t0, 0.25), 1 - P(t, w(23.55), 0.35)));
      });
    }
    // ---------- Betrieb und Register ----------
    if (this.bO.vis) {
      const zk = Math.min(P(t, w(15.95), 0.85), 1 - P(t, w(19.45), 0.8));
      kamera(this.bO, [lerp(960, 1560, zk), lerp(540, 578, zk)], lerp(1, 1.6, zk));
      O(this.bO.spot, zk); dimmen(zk);
      [[this.monA, w(11.62)], [this.monB, w(11.85)]].forEach(([m, t0]) => bildschirm(m, P(t, t0, 0.35, E.out)));
      const kc = P(t, w(12.1), 0.35, E.out); O(this.figC.dim, 0.78 * (1 - kc)); O(this.figC.glow, 0.2 + 0.8 * kc);
      arme(this.figC, 18, 131, -6, 0, 3 * Math.sin(t * 0.9));
      const pA = Math.min(P(t, w(14.4), 0.3), 1 - P(t, w(15.1), 0.35)), pB = Math.min(P(t, w(14.7), 0.3), 1 - P(t, w(15.4), 0.35));
      pose(this.figA, -112 * pA, tippen(t, w(12.5), w(14.3), 0) + tippen(t, w(15.5), w(21), 0) - 20 * pA, 2 * Math.sin(t * 1.3) - 8 * pA);
      pose(this.figB, -112 * pB, tippen(t, w(12.6), w(14.6), 1.7) + tippen(t, w(15.8), w(21), 1.7) - 20 * pB, 2 * Math.sin(t * 1.1 + 1) - 8 * pB);
      this.tags.forEach((tg, i) => { const t0 = w(13.25) + i * 0.27, k = P(t, t0, 0.4, E.out); tr(tg.g, tg.x, tg.y - (1 - k) * 60, 1, 22 * swing(t, t0 + 0.1) * (k > 0 ? 1 : 0)); O(tg.g, k); });
      const R = this.REG, rk = P(t, w(14.1), 0.7, E.out);
      tr(this.reg, R.x + (1 - rk) * 520, R.y, 1, R.r + (1 - rk) * 6); O(this.reg, rk);
      this.tokens.forEach((gr, i) => {
        const t0 = w(14.45) + i * 0.3, k = P(t, t0, 0.8, E.io);
        const a = [this.tags[i].x, this.tags[i].y + 48], b = [R.x - 40, R.y + this.ROWY[i]];
        const p = qb(a, [(a[0] + b[0]) / 2, Math.min(a[1], b[1]) - 230], b, k);
        tr(gr, p[0], p[1], lerp(1, 0.8, k), lerp(0, 8, Math.sin(Math.PI * k)));
        O(gr, Math.min(P(t, t0, 0.15), 1 - P(t, t0 + 0.78, 0.15)));
        O(this.rows[i].g, P(t, t0 + 0.72, 0.25, E.out));
      });
      const u0 = w(16.24);
      O(this.frame3, P(t, w(15.8), 0.3) * (0.75 + 0.25 * Math.sin(Math.max(0, t - u0) * 7) * (t > u0 && t < u0 + 1.16 ? 1 : 0)));
      this.frame3.setAttribute('stroke-dashoffset', (-(t * 14)).toFixed(1));
      this.underline3.setAttribute('width', (408 * P(t, w(17.5), 0.6, E.io)).toFixed(1));
      sk(this.befund, 115, this.ROWY[2] + 64, Math.max(0.01, P(t, w(18.42), 0.45, E.back))); O(this.befund, P(t, w(18.42), 0.2));
    }
    // ---------- Zugangswege ----------
    if (this.bA.vis) {
      const k = fahrt(t, { f: [960, 540], z: 1 }, [
        { t: w(42.85), d: 0.75, f: [1580, 500], z: 1.5 }, { t: w(45.85), d: 0.75, f: [1190, 790], z: 1.4 },
        { t: w(47.8), d: 0.7, f: [1350, 760], z: 1.25 }, { t: w(50.65), d: 0.7, f: [960, 540], z: 1 },
      ]);
      kamera(this.bA, k.f, k.z);
      const zoomB = Math.min(P(t, w(42.85), 0.75), 1 - P(t, w(50.65), 0.7));
      O(this.bA.spot, zoomB); dimmen(zoomB);
      pose(this.figB2, 0, 5 * Math.sin(t * 2 * Math.PI * 4.2) * (t < w(36.6) || t > w(41) ? 1 : 0.2), 2 * Math.sin(t * 1.2));
      bildschirm(this.monB2, 1);
      zeichne(this.laneBot, P(t, w(25.9), 0.9, E.io), this.lenB);
      sk(this.cardB, 1180, 790, Math.max(0.01, P(t, w(26.45), 0.5, E.back))); O(this.cardB, P(t, w(26.45), 0.25));
      O(this.laneTopHi, 0.55 * Math.min(P(t, w(56.4), 0.4), 1 - P(t, w(59.5), 0.5)));
      O(this.laneBotHi, 0.3 * P(t, w(34.5), 0.6) + 0.4 * P(t, w(59.3), 0.4));
      O(this.bizCardHi, P(t, w(59.3), 0.35) * (0.7 + 0.3 * Math.sin(t * 5)) + Math.min(P(t, w(46.3), 0.3), 1 - P(t, w(47.8), 0.4)) * 0.8);
      sk(this.appr, 330 + this.apprW / 2, 548, Math.max(0.01, P(t, w(27.3), 0.45, E.back))); O(this.appr, P(t, w(27.3), 0.2));
      const tk = P(t, w(28.75), 0.4, E.io);
      this.tglKnob.setAttribute('cx', lerp(15, -15, tk).toFixed(2));
      this.tglTrack.setAttribute('fill', tk > 0.5 ? '#3a4660' : C.blue);
      setText(this.trState, tk > 0.5 ? { de: 'AUS', en: 'OFF' } : { de: 'AN', en: 'ON' });
      O(this.tglRing, Math.min(P(t, w(28.6), 0.2), 1 - P(t, w(29.7), 0.4)) + Math.min(P(t, w(46.4), 0.3), 1 - P(t, w(47.7), 0.4)));
      typeText(this.addrT, { de: 'ki@muster-elektro.example', en: 'ai@sample-electric.example' }, t, w(31.2), 1.35);
      this.nameStrike.setAttribute('width', (breite(this.nameT) * P(t, w(32.95), 0.35)).toFixed(1));
      const no = P(t, w(33.3), 0.45, E.in); tr(this.nameG, no * 40, 0); O(this.nameG, 1 - no);
      this.addrT.setAttribute('y', lerp(824, 792, P(t, w(33.45), 0.4, E.io)).toFixed(1));
      const closed = Math.min(P(t, w(34.15), 0.6, E.io), 1 - P(t, w(54.7), 0.8, E.sine)) + P(t, w(59.5), 0.55, E.io);
      tr(this.gateBar, 0, lerp(282, 428, clamp(closed)));
      O(this.gateLab, Math.min(P(t, w(34.5), 0.4), 1 - P(t, w(54.7), 0.4)) + P(t, w(59.8), 0.4));
      placeDots(this.dotsT, this.laneTop, this.lenT, this.EM_T, t);
      placeDots(this.dotsB, this.laneBot, this.lenB, this.EM_B, t);
      placeDots(this.dotsA, this.laneBot, this.lenB, this.EM_A, t, 360, true);
      this.lights.forEach((l, i) => O(l, 0.25 + 0.5 * (0.5 + 0.5 * Math.sin(t * 2.3 + i * 1.7))));
      const arrived = this.EM_T.filter((e) => e + this.lenT / 360 <= t && e < w(40)).length;
      const morph = P(t, w(43.4), 1.0, E.io);
      this.pile.forEach((gr, i) => {
        const vis = arrived > i * 2 ? 1 : 0, bx = 1572 + i * 7, by = 512 - i * 9;
        tr(gr, lerp(bx, 1620, morph), lerp(by, 476, morph), lerp(1, 0.4, morph), (i % 2 ? 3 : -3) * (1 - morph)); O(gr, vis * (1 - morph));
      });
      const arrivedLate = this.EM_T.filter((e) => e > w(50) && e + this.lenT / 360 <= t).length;
      tr(this.profile, 1620, 476, Math.max(0.01, P(t, w(43.75), 0.6, E.back)) * (1 + 0.04 * arrivedLate), 0); O(this.profile, P(t, w(43.75), 0.3));
      const vk = P(t, w(28.75), 0.4, E.io);
      this.valveBar.setAttribute('transform', `rotate(${lerp(90, 0, vk).toFixed(1)})`); this.valveBar.setAttribute('fill', vk > 0.5 ? C.muted : C.blue);
      O(this.valveRing, Math.min(P(t, w(48.3), 0.3), 1 - P(t, w(50.4), 0.5)) * (0.6 + 0.4 * Math.sin(t * 6)));
      O(this.trainState, P(t, w(28.9), 0.3));
      this.trainBox.setAttribute('stroke', t > w(48.3) && t < w(50.6) ? C.blue : '#2a3858');
      const ik = Math.min(P(t, w(37.3), 0.6, E.out), 1 - P(t, w(42.6), 0.5));
      tr(this.inst, 0, (1 - P(t, w(37.3), 0.6, E.out)) * -30); O(this.inst, ik);
      const rk2 = P(t, w(39.45), 1.0, E.io), rp = qb([1000, 170], [900, 160], [831, 318], rk2);
      tr(this.rec, rp[0], rp[1], lerp(0.6, 1, rk2), lerp(-8, 4, rk2)); O(this.rec, Math.min(P(t, w(39.4), 0.25), 1 - P(t, w(50.9), 0.5)));
      const ruleIn = P(t, w(52.45), 0.8, E.out);
      tr(this.rule, 980, lerp(-120, 205, ruleIn), 1, -1 + 2 * swing(t, w(53.2)) * (t > w(53.2) ? 1 : 0)); O(this.rule, P(t, w(52.45), 0.2));
      typeText(this.r1, { de: 'Erlaubt: Textassistent', en: 'Permitted: text assistant' }, t, w(53.05), 0.75);
      this.r1u.setAttribute('width', (this.r1W * P(t, w(58.4), 0.45)).toFixed(1));
      typeText(this.r2, { de: 'Zugang: Betriebskonto', en: 'Access: business account' }, t, w(59.12), 0.7);
      const c1 = P(t, w(54.45), 0.6, E.io);
      this.conn1.setAttribute('stroke-dashoffset', (-t * 30).toFixed(1));
      O(this.conn1, c1 * (1 - P(t, w(59.4), 0.5))); O(this.conn1dot, c1 * (1 - P(t, w(59.4), 0.5)));
      zeichne(this.conn2, P(t, w(59.35), 0.6, E.io), this.c2len); O(this.conn2, P(t, w(59.35), 0.01)); O(this.conn2dot, P(t, w(59.9), 0.25));
    }
    // ---------- die eine Seite ----------
    if (this.bS.vis) {
      const zoom = Math.min(P(t, this.tA2 - 0.2, 0.9), 1 - P(t, this.tEnde - 1.0, 0.8));
      kamera(this.bS, lerp2([960, 540], [700, 560], zoom), lerp(1, 1.32, zoom)); dimmen(zoom * 0.8);
      const si = P(t, this.tSeite - 0.3, 0.8, E.out);
      tr(this.seite, 560, 560 + (1 - si) * -60 + swing(t, this.tSeite + 0.4) * 6, 1, lerp(-4, -1.2, si) + 1.5 * swing(t, this.tSeite + 0.4)); O(this.seite, si);
      this.szeilen.forEach((z, i) => { O(z.g, P(t, this.tNie + i * 0.12, 0.3)); O(z.hi, fenster(t, this.tR[i] - 0.1, 0.25, (this.tR[i + 1] || this.tZweifel) - 0.15, 0.3)); });
      const zb = P(t, this.tZweifel - 0.1, 0.5, E.out);
      const ausl = Math.min(P(t, this.tA2, 0.4), 1 - P(t, this.tKatalog, 0.4));
      O(this.zband, zb * (1 - 0.85 * ausl)); this.zbandR.setAttribute('fill', P(t, this.tKatalog + 0.6, 0.3) > 0.5 && t > this.tKatalog ? C.blue : C.blue);
      // Wege und Sperre
      const wk = P(t, this.tNie, 0.8);
      zeichne(this.sLaneB, wk, this.sLenB); O(this.sLaneT, wk); this.sLaneT.setAttribute('stroke-dashoffset', (-t * 26).toFixed(1));
      rein(this.sLabT, 1080, 345, t, this.tNie + 0.3, 0.4, this.tZweifel); rein(this.sLabB, 1080, 668, t, this.tNie + 0.5, 0.4, this.tZweifel);
      O(this.sTool, P(t, this.tSeite + 0.4, 0.6));
      const sp = P(t, this.tZugang, 0.5, E.back); this.sperreL.setAttribute('height', (260 * Math.min(1, sp)).toFixed(1)); O(this.sperre, P(t, this.tZugang, 0.2) * (1 - 0.6 * ausl));
      this.sTok.forEach((gr, i) => {
        const t0 = this.tR[i], lane = i % 2 ? this.sLaneB : this.sLaneT, len = i % 2 ? this.sLenB : this.sLenT;
        const flug = P(t, t0, 0.55, E.io), lauf = P(t, t0 + 0.5, 0.75, E.in), zurueck = P(t, t0 + 1.25, 0.45, E.out);
        const zp = [860, 560 + this.SY[i] + 31];
        const start = lane.getPointAtLength(0), ende = lane.getPointAtLength(len);
        let p = bogen([860, zp[1]], [start.x, start.y], flug, 80);
        if (lauf > 0) { const q = lane.getPointAtLength(lauf * len); p = [q.x, q.y]; }
        if (zurueck > 0) p = [ende.x - 70 * zurueck, ende.y + 40 * zurueck];
        tr(gr, p[0], p[1], 1 - 0.3 * zurueck, 14 * zurueck); O(gr, Math.min(P(t, t0, 0.15), 1 - P(t, t0 + 1.4, 0.35)));
        const bz = P(t, t0 + 1.2, 0.3, E.back); tr(this.sBlitz[i], ende.x + 6, ende.y - 46, Math.max(0.01, bz)); O(this.sBlitz[i], Math.min(P(t, t0 + 1.2, 0.1), 1 - P(t, t0 + 1.7, 0.3)));
      });
      // Zweifelsregel: Figur hält einen unbekannten Fall, fragt die benannte Person
      const zf = fenster(t, this.tZweifel, 0.5, this.tA2 - 0.3, 0.4);
      O(this.sFig.g, zf); O(this.sPerson.g, zf);
      arme(this.sFig, -6, 0, -40 * zf, -70 * zf, 0); arme(this.sPerson, -6 + 10 * P(t, this.tPerson + 0.3, 0.4), 0, -6, 0, 0);
      const uk = P(t, this.tImZw, 0.6, E.out);
      tr(this.sUnb, lerp(1060, 1110, uk), 760 - 10 * Math.sin(t * 3), 1); O(this.sUnb, zf * P(t, this.tZweifel + 0.2, 0.3));
      zeichne(this.sFrage, P(t, this.tPerson - 0.6, 0.6)); O(this.sFrage, zf);
      pop(this.sBlase, 1215, 640, t, this.tPerson - 0.2, 0.45, this.tA2 - 0.3); tr(this.sBlase, 1215, 640, Math.max(0.01, P(t, this.tPerson - 0.2, 0.45, E.back)));
      rein(this.sPersonP, 1420, 642, t, this.tPerson, 0.4, this.tA2 - 0.3);
      // Auslegung: ohne Zweifelsregel fällt der Fall durch, mit Zweifelsregel wird er gefangen
      const yTop = this.SY[0] - 10, yBand = this.zbandY + 46, yAus = this.sb.y0 + this.sb.h + 120;
      const f1 = P(t, this.tA2 + 0.6, 2.2, E.in), f2 = P(t, this.tKatalog + 0.3, 1.6, E.out);
      let fy, fo;
      if (t < this.tKatalog + 0.3) { fy = lerp(yTop, yAus, f1); fo = Math.min(P(t, this.tA2 + 0.5, 0.2), 1 - P(t, this.tA2 + 2.6, 0.3)); }
      else { fy = lerp(yTop, yBand, f2); fo = P(t, this.tKatalog + 0.3, 0.2); }
      tr(this.sFall, this.sb.right - 6 + 4 * Math.sin(fy / 30), fy, 1, 8 * Math.sin(fy / 40)); O(this.sFall, fo);
      pop(this.sUnvoll, 0, 0, t, this.tUnvoll, 0.45, this.tKatalog); tr(this.sUnvoll, 1020, 860, Math.max(0.01, P(t, this.tUnvoll, 0.45, E.back)));
      rein(this.sKatalog, 1020, 330, t, this.tKatalog, 0.5);
      if (t > this.tKatalog) O(this.zband, 1);
    }
  },
});
