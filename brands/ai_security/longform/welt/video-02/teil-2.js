// Teil 2 · Was meistens schiefgeht (Absätze 3 bis 6).
// Bühnen: ein Fragebogen kommt vom größeren Kunden (Themen, Termin, keine IT-Abteilung) → im Betrieb: Büroleitung, IT-Betreuung auf der Baustelle,
// fremde Wörter → zwei typische Fehler (Rest leer, überall „Ja“) → Zitat aus dem Handbuch (das „Ja“ zerfällt) → vier Arten von Anfragen.
akt({
  name: 'problem',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    const K = { de: '1 · WAS MEISTENS SCHIEFGEHT', en: '1 · WHAT USUALLY GOES WRONG' };
    // ---------- Wortanker ----------
    this.tLage = c('Die Lage ist', 'The situation is');
    this.tKunde = c('größerer Kunde', 'larger customer');
    this.tDok = c('ein Dokument', 'a document');
    this.tFragen = c('zur Informationssicherheit', 'about information security');
    this.tT = [c('Multi-Faktor-Authentifizierung|Multifaktor-Authentifizierung|Multi-Faktor', 'multi-factor authentication|multifactor authentication|multi-factor'),
      c('Sicherung', 'backups'), c('Updates', 'updates'), c('Vorfälle', 'incidents'), c('Schulung', 'training'), c('Dienstleister', 'providers')];
    this.tTermin = c('einen Termin', 'a date');
    this.tKeineIT = c('keine IT-Abteilung|keine IT Abteilung', 'no IT department');
    this.tBuero = c('Die Büroleitung', 'The office manager');
    this.tExtern = c('externe IT-Betreuung|externe IT Betreuung', 'external IT provider');
    this.tBaustelle = c('einer Baustelle', 'on a job');
    this.tWoerter = c('Wörter', 'words');
    this.tNiemand = c('niemand täglich', 'every day');
    this.tZwei = c('Zwei Dinge', 'Two things');
    this.tErstens = c('Erstens', 'The first');
    this.tTechn = c('technischen Fragen', 'technical questions');
    this.tLeer = c('Rest leer', 'rest blank');
    this.tWer = c('Wer verantwortlich', 'Who is responsible');
    this.tNotfall = c('Notfallplan', 'emergency plan');
    this.tEingew = c('eingewiesen', 'briefed');
    this.tNiemandB = c('niemand beantwortet', 'nobody answers');
    this.tZweitens = c('Zweitens', 'The second');
    this.tJa = c('überall Ja', 'yes everywhere');
    this.tHoeren = c('hören will', 'customer wants');
    const Q1 = quelle(); this.tQ1 = Q1.s;
    this.tEhrlich = c('ehrliches', 'honest');
    this.tErf = c('erfährt mehr', 'learns more');
    this.tNach = c('ersten Nachfrage', 'first follow-up', { halten: true }); // im Englischen steht „falls apart“ davor
    this.tZerf = c('zerfällt', 'falls apart'); this.tNach = Math.min(this.tNach, this.tZerf - 0.9);
    this.tProt = c('Protokoll', 'restore test');
    this.tKeines = c('keines bekommt', 'gets none');
    this.tJedes = c('jedes andere', 'every other');
    const Q2 = quelle(); this.tQ2 = Q2.s;
    this.tA = [c('ein Fragebogen eines|Fragebogen eines', 'a questionnaire from'), c('ein Vertrag', 'a contract'), c('Cyberversicherers|Cyber-Versicherers|Versicherers', 'cyber insurer|insurer'), c('Gütesiegel', 'a label')];
    this.tVideo = c('Dieses Video handelt', 'This video is about');
    this.tVertrag = c('dem Vertrag', 'the contract');
    this.tEnde = cue({ de: 'Was der Betrieb tut', en: 'What the business does' }, { halten: true }).s;

    // ---------- Bühne A: der Fragebogen kommt ----------
    const bA = buehne('problem-lage', { seed: 11, regalDeckkraft: 0.55 }); this.bA = bA;
    this.kunde = kundeHaus(bA.cam, 260, 860, 1);
    this.klein = kleinHaus(bA.cam, 1660, 860, 1.1);
    this.fbA = fragebogen(bA.cam, [['key', { de: 'Multi-Faktor-Authentifizierung', en: 'Multi-factor authentication' }], ['folder', { de: 'Sicherung', en: 'Backups' }], ['cycle', { de: 'Updates', en: 'Updates' }],
      ['warn', { de: 'Vorfälle', en: 'Incidents' }], ['group', { de: 'Schulung', en: 'Training' }], ['briefcase', { de: 'Eigene Dienstleister', en: 'Your own providers' }]], { w: 620, feldW: 100, size: 26 });
    this.itGeist = g(bA.cam);
    this.itGeistR = el('rect', { x: 1510, y: 380, width: 300, height: 130, rx: 14, fill: 'rgba(255,209,102,0.03)', stroke: C.amberLine, 'stroke-width': 4, 'stroke-dasharray': '14 10' }, this.itGeist);
    T(this.itGeist, 1660, 432, { de: 'IT-ABTEILUNG', en: 'IT DEPARTMENT' }, { mono: 1, size: 24, fill: C.amber, anchor: 'middle', ls: '0.1em' });
    T(this.itGeist, 1660, 482, { de: 'keine', en: 'none' }, { size: 34, weight: 800, fill: C.amber, anchor: 'middle' });
    shot(bA, this.tLage - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne B: im Betrieb ----------
    const bB = buehne('problem-buero', { seed: 13 }); this.bB = bB;
    const B = bauBetrieb(bB.cam); this.B = B;
    el('rect', { x: 3330, y: 852, width: 900, height: 10, rx: 5, fill: '#1c2943' }, bB.cam);
    baustelle(bB.cam, 3900, 856);
    this.itFig = itBetreuung(bB.cam, 3640, 852, 1);
    this.itLab = pille(bB.cam, { de: 'IT-Betreuung · extern', en: 'IT provider · external' }, { icon: 'briefcase', col: C.muted, size: 24 });
    this.bBlatt = g(bB.cam);
    const bb = blatt(this.bBlatt, { w: 420, h: 520, kicker: { de: 'FRAGEBOGEN', en: 'QUESTIONNAIRE' }, kSize: 15, pad: 30 });
    linien(bb.g, bb.left, bb.y + 10, 340, 9, 40, C.pBar2, 12);
    this.bueroLab = pille(bB.cam, { de: 'Büroleitung', en: 'Office manager' }, { icon: 'person', col: C.blue, size: 22 });
    this.woerter = [[{ de: 'Multi-Faktor-Authentifizierung', en: 'multi-factor authentication' }, [880, 430]], [{ de: 'Wiederherstellungstest', en: 'restore test' }, [820, 345]], [{ de: 'Lieferkette', en: 'supply chain' }, [1290, 330]]]
      .map(([w0, pos]) => ({ g: pille(bB.cam, w0, { col: C.muted, size: 21, gestrichelt: true }), pos }));
    this.frageZ = g(bB.cam); iconUnknown(this.frageZ, 74, C.amber);
    shot(bB, this.tBuero - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne C: zwei typische Fehler ----------
    const bC = buehne('problem-fehler', { seed: 17, regalDeckkraft: 0.55 }); this.bC = bC;
    const ZEILEN = [['key', { de: 'MFA', en: 'MFA' }], ['folder', { de: 'Sicherung', en: 'Backups' }], ['cycle', { de: 'Updates', en: 'Updates' }],
      ['person', { de: 'Verantwortlich', en: 'Responsible' }], ['warn', { de: 'Notfallplan', en: 'Emergency plan' }], ['group', { de: 'Einweisung', en: 'Staff briefing' }]];
    this.f1 = fragebogen(bC.cam, ZEILEN, { termin: false, w: 540, feldW: 130 });
    this.f2 = fragebogen(bC.cam, ZEILEN, { termin: false, w: 540, feldW: 130 });
    this.f1Antw = this.f1.zeilen.map((z, i) => { const gr = g(z.ein); if (i < 3) el('rect', { x: -50, y: -6, width: 100, height: 12, rx: 6, fill: C.blue }, gr); else { el('rect', { x: -63, y: -18, width: 126, height: 36, rx: 6, fill: C.amberSoft, stroke: C.amberLine, 'stroke-width': 2.5, 'stroke-dasharray': '7 5' }, gr); T(gr, 0, 10, '?', { size: 28, weight: 800, fill: C.amberDeep, anchor: 'middle' }); } return gr; });
    this.f2Ja = this.f2.zeilen.map((z) => jaFeld(z));
    this.itKlein = itBetreuung(bC.cam, 150, 880, 0.72);
    this.stift = g(bC.cam); iconPen(this.stift, 64, C.ink);
    this.k1 = kachel(bC.cam, '1', C.blue, 64); this.k2 = kachel(bC.cam, '2', C.blue, 64);
    this.p1 = pille(bC.cam, { de: 'Rest leer', en: 'Rest left blank' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 26 });
    this.p2 = pille(bC.cam, { de: 'Überall „Ja“', en: '"Yes" everywhere' }, { icon: 'check', col: C.amber, gestrichelt: true, size: 26 });
    shot(bC, this.tZwei - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne D: Zitat aus dem Handbuch ----------
    const bD = buehne('problem-zitat', { seed: 19, regalDeckkraft: 0.45, licht: 0.7 }); this.bD = bD;
    const dc = bD.cam;
    this.dKunde = kundeHaus(dc, 960, 430, 0.42, { label: null });
    this.dLinie = el('path', { d: 'M 560 540 C 600 420 760 380 900 360', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round' }, dc);
    this.dErf = pille(dc, { de: 'erfährt mehr', en: 'learns more' }, { icon: 'search', col: C.blue, size: 24 });
    this.dNoch = antwort(dc, 'termin', { text: { de: 'noch nicht', en: 'not yet' }, size: 34 });
    // „Ja“-Karte aus drei Stücken, die bei „zerfällt“ auseinanderfallen
    this.ja = g(dc);
    const STUECK = [[[-130, -64], [12, -64], [-12, -4], [22, 64], [-130, 64]], [[12, -64], [130, -64], [130, 8], [44, 20], [-12, -4]], [[-12, -4], [44, 20], [130, 8], [130, 64], [22, 64]]];
    this.stuecke = STUECK.map((pts) => { const gr = g(this.ja); el('path', { d: 'M ' + pts.map((p) => p.join(' ')).join(' L ') + ' Z', fill: C.raised, stroke: C.edge, 'stroke-width': 3, 'stroke-linejoin': 'round' }, gr); const cx = pts.reduce((s, p) => s + p[0], 0) / pts.length, cy = pts.reduce((s, p) => s + p[1], 0) / pts.length; return { g: gr, c: [cx, cy] }; });
    { const h = g(this.stuecke[0].g, { transform: 'translate(-82 0)' }); el('rect', { x: -20, y: -20, width: 40, height: 40, rx: 6, fill: 'none', stroke: C.ink, 'stroke-width': 3 }, h); iconCheck(h, 44, C.ink);
      T(this.stuecke[0].g, -40, 18, { de: 'J', en: 'Y' }, { size: 52, weight: 800 }); T(this.stuecke[1].g, -6, 18, { de: 'a', en: 'es' }, { size: 52, weight: 800 }); }
    this.frageB = g(dc); el('circle', { r: 46, fill: C.surface, stroke: C.blue, 'stroke-width': 3 }, this.frageB); iconQuestion(this.frageB, 54, C.blue);
    this.nachP = pille(dc, { de: 'Nachfrage', en: 'Follow-up' }, { col: C.blue, size: 22 });
    this.dForm = fragebogen(dc, [['key', { de: 'MFA', en: 'MFA' }], ['folder', { de: 'Sicherung', en: 'Backups' }], ['cycle', { de: 'Updates', en: 'Updates' }], ['warn', { de: 'Notfallplan', en: 'Emergency plan' }], ['group', { de: 'Schulung', en: 'Training' }]], { termin: false, w: 500, feldW: 130 });
    this.dJa = this.dForm.zeilen.map((z) => jaFeld(z));
    this.dZweifel = this.dForm.zeilen.map((z) => { const gr = g(z.g, { transform: `translate(${z.fx + 112} ${z.y - 8})` }); el('circle', { r: 17, fill: C.amber }, gr); T(gr, 0, 8, '?', { size: 24, weight: 800, fill: C.ground, anchor: 'middle' }); return gr; });
    this.slot = g(dc);
    el('rect', { x: -170, y: -170, width: 340, height: 340, rx: 10, fill: 'rgba(255,255,255,0.02)', stroke: C.amberLine, 'stroke-width': 4, 'stroke-dasharray': '14 10' }, this.slot);
    TB(this.slot, -140, -110, { de: 'Protokoll Wiederherstellungstest', en: 'Restore test record' }, { size: 26, weight: 800, fill: C.amber, maxW: 290, lh: 32 });
    this.slotLeer = T(this.slot, 0, 110, { de: 'keines', en: 'none' }, { mono: 1, size: 30, fill: C.amber, anchor: 'middle', ls: '0.1em' });
    shot(bD, this.tQ1 - 0.4, { typ: 'blende', d: 0.8 });

    // ---------- Bühne E: vier Arten von Anfragen ----------
    const bE = buehne('problem-arten', { seed: 23, regalDeckkraft: 0.55 }); this.bE = bE;
    this.eHaus = kleinHaus(bE.cam, 960, 840, 1);
    const ARTEN = [['doc', { de: 'Fragebogen eines Kunden', en: 'Questionnaire from a customer' }], ['contract', { de: 'Vertrag mit Sicherheitsklauseln', en: 'Contract with security clauses' }],
      ['briefcase', { de: 'Antrag eines Cyberversicherers', en: 'Cyber insurer application' }], ['cert', { de: 'Gütesiegel oder Zertifikat', en: 'Label or certificate' }]];
    this.ePos = [[390, 470], [770, 330], [1150, 330], [1530, 470]];
    this.eVon = [[-200, 300], [600, -120], [1320, -120], [2120, 300]];
    this.eLinien = this.ePos.map(([x, y]) => el('path', { d: `M ${x} ${y + 44} Q ${(x + 960) / 2} ${y + 200} 960 590`, fill: 'none', stroke: C.line, 'stroke-width': 3, 'stroke-dasharray': '9 7' }, bE.cam));
    this.eKarten = ARTEN.map(([ic, txt]) => belegKarte(bE.cam, ic, txt, { w: 340, h: 88, size: 23 }));
    this.eRahmen = this.eKarten.map((k) => el('rect', { x: -178, y: -52, width: 356, height: 104, rx: 12, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, k));
    shot(bE, this.tQ2 - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [bA, bB, bC, bD, bE];

    // ---------- Einblendungen ----------
    kopf(this.tLage, this.tBuero - 0.3, K, { de: 'Ein Fragebogen kommt an', en: 'A questionnaire arrives' });
    kopf(this.tBuero, this.tZwei - 0.3, K, { de: 'Wer davor sitzt', en: 'Who opens it' });
    kopf(this.tZwei, this.tQ1 - 0.3, K, { de: 'Zwei typische Fehler', en: 'Two typical mistakes' });
    kopf(this.tQ1, this.tQ2 - 0.3, K, { de: 'Das ehrliche „noch nicht“', en: 'The honest "not yet"' });
    kopf(this.tQ2, this.tEnde - 0.3, K, { de: 'Vier Arten von Anfragen', en: 'Four kinds of requests' });
    freiesAngebot(this.tQ1 - 0.1, { de: '/de/toolkits/sicherheitsnachweis/handbuch', en: '/toolkits/security-evidence/handbook' }, { icon: 'book' }); // aus welt.js, wie in Video 01
  },

  zeichnen(t) {
    // ---------- Bühne A ----------
    if (this.bA.vis) {
      kamera(this.bA, [960, 540], 1);
      const ki = P(t, this.tKunde - 0.3, 0.6, E.out); O(this.kunde.g, ki); tr(this.kunde.g, 260 - (1 - ki) * 60, 860, 1);
      this.kunde.fenster.forEach((f, i) => f.setAttribute('fill', (i * 7 + Math.floor(t * 0.7)) % 9 === 0 ? '#3a5584' : (i % 4 === 1 ? '#2a3d62' : '#1a2742')));
      const fk = P(t, this.tDok - 0.2, 1.2, E.io), hoch = P(t, this.tFragen - 0.2, 1.0, E.io);
      const flug = bogen([300, 520], [1640, 660], fk, 170);
      const pos = lerp2(flug, [960, 545], hoch);
      tr(this.fbA.g, pos[0], pos[1], lerp(0.12, 0.95, hoch), lerp(lerp(-14, 6, fk), -1.5, hoch)); O(this.fbA.g, P(t, this.tDok - 0.2, 0.25));
      this.fbA.zeilen.forEach((z, i) => { const k = P(t, this.tT[i] - 0.05, 0.35, E.out); O(z.label, 0.15 + 0.85 * k); O(z.feld, 0.3 + 0.7 * k); z.icon.setAttribute('opacity', (0.15 + 0.85 * k).toFixed(3)); });
      { const k = P(t, this.tTermin, 0.4, E.out); O(this.fbA.termin, 0.2 + 0.8 * k); }
      const gk = P(t, this.tKeineIT + 0.1, 0.6, E.out); O(this.itGeist, gk); tr(this.itGeist, 0, (1 - gk) * -24); this.itGeistR.setAttribute('stroke-dashoffset', (-t * 14).toFixed(1));
      O(this.klein.g, P(t, this.tLage, 0.6)); this.klein.fenster[0].setAttribute('fill', P(t, this.tDok + 1.0, 0.3) > 0.5 ? '#5d7fc0' : '#2a3d62');
    }
    // ---------- Bühne B ----------
    if (this.bB.vis) {
      const B = this.B;
      const k = fahrt(t, { f: [1180, 620], z: 1.25 }, [{ t: this.tExtern - 0.3, d: 1.5, f: [3600, 600], z: 1.0 }, { t: Math.max(this.tExtern + 1.4, this.tWoerter - 1.0), d: 1.3, f: [1120, 580], z: 1.32 }]);
      kamera(this.bB, k.f, k.z);
      B.monitore.forEach((m, i) => bildschirm(m, i === 0 ? 1 : 0.35));
      const zeig = fenster(t, this.tBuero + 0.4, 0.4, this.tExtern - 0.2, 0.4);
      betriebLeben(B, t, { zeigen: { figA: zeig * 0.4 }, tippen: { figB: [this.tBuero, 99], figC: [this.tBuero + 0.3, 99] } });
      const bk = P(t, this.tBuero + 0.1, 0.7, E.back); tr(this.bBlatt, 1196, 455, Math.max(0.01, 0.34 * bk), -3); O(this.bBlatt, P(t, this.tBuero + 0.1, 0.25));
      tr(this.bueroLab, 1024, 880, 1); O(this.bueroLab, fenster(t, this.tBuero + 0.3, 0.4, this.tExtern - 0.3, 0.3));
      // IT-Betreuung tippt auf dem Laptop
      arme(this.itFig, -6, 0, 30 + 2 * Math.sin(t * 9), 72 + tippen(t, this.tExtern, this.tWoerter, 0, 4), 6 + 3 * Math.sin(t * 0.8));
      tr(this.itLab, 3640, 930, 1); O(this.itLab, P(t, this.tBaustelle - 0.2, 0.4));
      this.woerter.forEach((w, i) => { const t0 = this.tWoerter + 0.15 + i * 0.35; const kk = P(t, t0, 0.45, E.back); tr(w.g, w.pos[0], w.pos[1] + 5 * Math.sin(t * 1.3 + i * 2), Math.max(0.01, kk)); O(w.g, P(t, t0, 0.2)); });
      { const kk = P(t, this.tNiemand, 0.45, E.back); tr(this.frageZ, 1024, 470 + 4 * Math.sin(t * 2), Math.max(0.01, kk), 8 * Math.sin(t * 1.5)); O(this.frageZ, P(t, this.tNiemand, 0.2)); }
    }
    // ---------- Bühne C ----------
    if (this.bC.vis) {
      kamera(this.bC, [960, 540], 1);
      const a1 = P(t, this.tErstens - 0.2, 0.6, E.out), a2 = P(t, this.tZweitens - 0.3, 0.6, E.out);
      tr(this.f1.g, 600, 570 + (1 - a1) * 30, 0.92, -1.2); O(this.f1.g, 0.25 + 0.75 * a1);
      tr(this.f2.g, 1360, 570 + (1 - a2) * 30, 0.92, 1.2); O(this.f2.g, 0.25 + 0.75 * a2);
      tr(this.k1, 600, 238, Math.max(0.01, P(t, this.tErstens, 0.45, E.back))); O(this.k1, P(t, this.tErstens, 0.2));
      tr(this.k2, 1360, 238, Math.max(0.01, P(t, this.tZweitens, 0.45, E.back))); O(this.k2, P(t, this.tZweitens, 0.2));
      // IT-Betreuung füllt die technischen Zeilen, der Rest bleibt leer
      const itK = fenster(t, this.tErstens, 0.5, this.tZweitens, 0.5); stelle(this.itKlein, lerp(60, 170, P(t, this.tErstens, 0.8, E.out)), 880, 0.72); O(this.itKlein.g, itK);
      arme(this.itKlein, -6, 0, 30, 72 + tippen(t, this.tTechn - 0.3, this.tLeer, 0, 4), 4);
      this.f1Antw.forEach((a, i) => { if (i < 3) { const k = P(t, this.tTechn + i * 0.3, 0.35, E.out); O(a, k); tr(a, 0, 0, 1); a.firstChild.setAttribute('width', (100 * k).toFixed(1)); a.firstChild.setAttribute('x', (-50).toFixed(1)); } else { const tt = [this.tWer, this.tNotfall, this.tEingew][i - 3]; O(a, P(t, this.tLeer + 0.1, 0.4)); sk(a, 0, 0, 1 + 0.18 * puls(t, tt, 0.9, 9)); } });
      tr(this.p1, 600, 905, Math.max(0.01, P(t, this.tNiemandB, 0.45, E.back))); O(this.p1, P(t, this.tNiemandB, 0.2));
      // Zweitens: überall „Ja“
      const n = this.f2Ja.length;
      this.f2Ja.forEach((j, i) => { const t0 = this.tJa - 0.4 + i * 0.22; O(j.g, P(t, t0, 0.12)); O(j.haken, P(t, t0 + 0.05, 0.12)); });
      const sp = clamp((t - (this.tJa - 0.5)) / (n * 0.22 + 0.2)); const zi = Math.min(n - 1, Math.floor(sp * n));
      const z = this.f2.zeilen[zi]; const sy = 570 + (z.y - 8) * 0.92, sx = 1360 + (z.fx + 30) * 0.92;
      tr(this.stift, sx + 30, sy - 30 + 8 * Math.sin(t * 30) * (sp > 0 && sp < 1 ? 1 : 0), 1, 0); O(this.stift, fenster(t, this.tJa - 0.7, 0.3, this.tJa + n * 0.22 + 0.2, 0.4));
      tr(this.p2, 1360, 905, Math.max(0.01, P(t, this.tHoeren, 0.45, E.back))); O(this.p2, P(t, this.tHoeren, 0.2));
    }
    // ---------- Bühne D ----------
    if (this.bD.vis) {
      kamera(this.bD, [960, 540], 1);
      const zweit = P(t, this.tProt - 0.3, 0.7, E.io); // zweiter Satz: Formular und leeres Fach
      O(this.dKunde.g, P(t, this.tQ1, 0.6));
      const nIn = P(t, this.tEhrlich - 0.1, 0.5, E.back); tr(this.dNoch, lerp(560, 360, zweit), 600, Math.max(0.01, nIn)); O(this.dNoch, Math.min(P(t, this.tEhrlich - 0.1, 0.2), 1 - zweit));
      zeichne(this.dLinie, P(t, this.tErf - 0.1, 0.7)); O(this.dLinie, 1 - zweit);
      tr(this.dErf, 700, 400, Math.max(0.01, P(t, this.tErf + 0.3, 0.45, E.back))); O(this.dErf, Math.min(P(t, this.tErf + 0.3, 0.2), 1 - zweit));
      // „Ja“ steht, die Nachfrage kommt, das „Ja“ zerfällt
      const jIn = P(t, this.tErf + 0.6, 0.5, E.out); tr(this.ja, 1360, 600 + (1 - jIn) * 24); O(this.ja, jIn);
      const br = clamp((t - this.tZerf) / 1.6);
      this.stuecke.forEach((s, i) => { const v = [[-160, -60, -40], [170, -120, 50], [120, 40, 70]][i]; const dx = v[0] * br, dy = v[1] * br + 520 * br * br, r = v[2] * br; s.g.setAttribute('transform', `translate(${(dx + s.c[0]).toFixed(1)} ${(dy + s.c[1]).toFixed(1)}) rotate(${r.toFixed(1)}) translate(${(-s.c[0]).toFixed(1)} ${(-s.c[1]).toFixed(1)})`); O(s.g, 1 - P(t, this.tZerf + 0.5, 0.9)); });
      const fq = P(t, this.tNach - 0.6, 0.9, E.io); const fp = bogen([960, 330], [1290, 500], fq, 80);
      tr(this.frageB, fp[0], fp[1], Math.max(0.01, P(t, this.tNach - 0.6, 0.4, E.back))); O(this.frageB, Math.min(P(t, this.tNach - 0.6, 0.2), 1 - P(t, this.tZerf + 0.8, 0.5)));
      tr(this.nachP, fp[0], fp[1] - 70, 1); O(this.nachP, Math.min(P(t, this.tNach - 0.2, 0.3), 1 - P(t, this.tZerf + 0.8, 0.5)));
      // Zweiter Satz: Formular voller „Ja“, das Protokoll fehlt, jedes „Ja“ wird fraglich
      tr(this.dForm.g, 760, 620 + (1 - zweit) * 30, 0.86, -1); O(this.dForm.g, zweit);
      this.dJa.forEach((j) => O(j.haken, 1));
      const sl = P(t, this.tProt + 0.1, 0.5, E.out); tr(this.slot, 1400, 600 + (1 - sl) * 20, 1); O(this.slot, sl);
      O(this.slotLeer, P(t, this.tKeines, 0.3)); tr(this.slotLeer, 4 * puls(t, this.tKeines, 0.8, 22), 0);
      this.dZweifel.forEach((d, i) => { const t0 = this.tJedes + 0.1 + i * 0.18; O(d, P(t, t0, 0.15)); });
    }
    // ---------- Bühne E ----------
    if (this.bE.vis) {
      kamera(this.bE, [960, 540], 1);
      O(this.eHaus.g, P(t, this.tQ2 - 0.2, 0.6));
      const fokus = P(t, this.tVideo, 0.6);
      this.eKarten.forEach((k, i) => {
        const a = P(t, this.tA[i] - 0.3, 0.9, E.out); const p = lerp2(this.eVon[i], this.ePos[i], a);
        const naeher = i < 2 ? fokus * 30 : 0;
        tr(k, p[0] + (i === 0 ? naeher : i === 1 ? naeher * 0.5 : 0), p[1] + naeher, 1 + (i < 2 ? 0.06 * fokus : -0.06 * fokus), lerp(i % 2 ? 6 : -6, 0, a));
        O(k, Math.min(a, i < 2 ? 1 : 1 - 0.65 * fokus));
        O(this.eRahmen[i], i === 0 ? fokus : i === 1 ? P(t, this.tVertrag, 0.5) : 0);
        O(this.eLinien[i], P(t, this.tA[i] + 0.4, 0.6) * (i < 2 ? 1 : 1 - 0.7 * fokus));
        this.eLinien[i].setAttribute('stroke', i < 2 && fokus > 0.5 ? C.blue : C.line);
      });
    }
  },
});
