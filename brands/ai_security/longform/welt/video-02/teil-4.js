// Teil 4 · Die Quellen hinter „noch nicht, mit Termin“ (Absätze 16 bis 25).
// Bühnen: Kernaussage → Lücke und Korrektur (Art. 21 Abs. 4, NISG § 33) → § 45 NISG (zwei Ausgänge) → Lücke mit Plan als Normalzustand
// → Frist der Selbstdeklaration und Weg der Antworten → acht Vertragsinhalte (DVO, NISV, Muster der Klauseln) → was offen ist.
akt({
  name: 'beleg',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    const K = { de: '3 · DIE QUELLEN', en: '3 · THE SOURCES' };
    // ---------- Wortanker ----------
    this.tJetzt = c('Jetzt die Quellen', 'Now the sources');
    this.tKern = c('Kernaussage', 'core claim');
    this.tNoch = c('noch nicht, mit Termin', 'not yet, with a date');
    this.tVoll = c('vollständige Antwort', 'complete answer');
    const F17 = belegt(); this.tF17 = F17.s;
    this.tFest = c('nicht nachkommt', 'does not comply');
    this.tKorr = c('Korrekturmaßnahmen', 'corrective measures');
    this.tAT = c('erwartet einen Prüfbericht', 'expects an audit report');
    this.tMaengel = c('festgestellter Mängel', 'identified deficiencies');
    this.tPlan = c('Maßnahmenplan', 'action plan');
    const F18 = belegt(); this.tF18 = F18.s;
    this.tStraf = c('Strafbestimmungen', 'penalty provisions');
    this.tNur = c('nur strafbar', 'an offence only');
    this.tSelbstD = c('Selbstdeklaration der Einrichtung', 'own self-declaration');
    this.tFalsch = c('Wissentlich falsche', 'Knowingly false');
    this.tEigens = c('eigens strafbar', 'offence of their own');
    const A19 = belegt(); this.tA19 = A19.s;
    this.tNormal = c('Normalzustand', 'normal state');
    this.tVerschont = c('verschont sogar', 'even spares');
    this.tBestraft = c('bestraft stattdessen', 'punishes the false');
    this.tLief = c('Ein Lieferant, der schreibt', 'A supplier that writes');
    this.tGibt = c('gibt dem Kunden', 'gives the customer');
    this.tSelbstE = c('für sich selbst erzeugen', 'produce for itself');
    this.tBegr = c('ganze Begründung', 'whole reasoning');
    const F20 = belegt(); this.tF20 = F20.s;
    this.tWes = c('wesentliche und wichtige', 'essential and important');
    this.tZwoelf = c('binnen zwölf Monaten', 'within twelve months', { halten: true }); // im Englischen nach der Selbstdeklaration
    this.tStrukt = c('strukturierte Selbstdeklaration', 'structured self-declaration');
    this.tLK = c('Sicherheit ihrer Lieferketten', 'security of their supply chains');
    const A21 = belegt(); this.tA21 = A21.s;
    this.tRoh = c('Rohmaterial', 'raw material');
    this.tFragt = c('Wer Sie', 'Whoever asks you');
    this.tBehoerde = c('an die Behörde', 'to the authority');
    this.tTon = c('Ton und Fristen', 'tone and the deadlines');
    this.tKeineE = c('nicht zu einer Eingabe', 'a filing with the authority');
    const F22 = belegt(); this.tF22 = F22.s;
    this.tDigital = c('digitale Anbieter', 'digital providers');
    this.tDVO = c('Durchführungsverordnung der Kommission', 'Implementing Regulation of');
    this.tV = [c('Cybersicherheitsanforderungen', 'cybersecurity requirements'), c('Ausbildung und', 'training and'), c('Zuverlässigkeitsüberprüfungen', 'background checks'), c('Sicherheitsvorfälle unverzüglich', 'report incidents'),
      c('Recht auf Prüfung', 'right to audit'), c('Schwachstellen zu beheben', 'handle vulnerabilities'), c('Unterauftragsvergabe', 'subcontracting'), c('bei Vertragsende', 'end of the contract')];
    this.tAcht = c('Acht Inhalte', 'Eight contents');
    const F23 = belegt(); this.tF23 = F23.s;
    this.tJede = c('jede wesentliche', 'every essential');
    const A24 = belegt(); this.tA24 = A24.s;
    this.tMuster = c('Muster der Klauseln', 'pattern of the clauses');
    this.tUnion = c('überall in der Union', 'anywhere in the Union');
    this.tInAT = c('in Österreich', 'customer in Austria');
    this.tDeutsch = c('deutscher Kunde', 'German customer');
    this.tNichtGeb = c('nicht von Gesetzes wegen', 'not bound');
    this.tPruefer = c('Prüfer und Juristen', 'auditors and lawyers');
    const L25 = belegt(); this.tL25 = L25.s;
    this.tGesucht = c('Muster-Lieferantenfragebogen|Musterlieferantenfragebogen|Muster Lieferantenfragebogen', 'model supplier questionnaire');
    this.tKeinen = c('keinen gefunden', 'found none');
    this.tFolgen = c('folgen den Quellen', 'follow the sources');
    this.tGericht = c('Gericht', 'court');
    this.tNichtG = c('nicht gesucht', 'not searched');
    this.tAbs6 = c('Abschnitt sechs', 'section six');
    this.tEnde = cue({ de: 'Zwei Fälle zum Mitentscheiden', en: 'Two cases for you' }, { halten: true }).s;

    // ---------- Bühne 1: Kernaussage ----------
    const b1 = buehne('beleg-kern', { seed: 51, regalDeckkraft: 0.55 }); this.b1 = b1;
    this.kNoch = antwort(b1.cam, 'termin', { size: 40 });
    this.kVoll = pille(b1.cam, { de: 'vollständige Antwort', en: 'complete answer' }, { icon: 'check', col: C.blue, size: 34, mono: false, weight: 800 });
    this.kBuecher = [{ de: 'NIS2', en: 'NIS2' }, { de: 'NISG 2026', en: 'NISG 2026' }, { de: 'DVO 2024/2690', en: 'IR 2024/2690' }, { de: 'NISV 2026', en: 'NISV 2026' }].map((b0) => { const gr = g(b1.cam); el('rect', { x: -90, y: -60, width: 180, height: 120, rx: 10, fill: '#1c2a47', stroke: C.edge, 'stroke-width': 3 }, gr); el('rect', { x: -90, y: -60, width: 22, height: 120, rx: 8, fill: '#2a3c62' }, gr); T(gr, 10, 8, b0, { mono: 1, size: 22, fill: C.ink, anchor: 'middle' }); return gr; });
    this.kLinien = [0, 1, 2, 3].map((i) => el('path', { d: `M ${510 + i * 300} 690 C ${510 + i * 300} 580 960 600 960 470`, fill: 'none', stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '8 6' }, b1.cam));
    shot(b1, this.tJetzt - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne 2: Lücke und Korrektur ----------
    const b2 = buehne('beleg-korrektur', { seed: 53, regalDeckkraft: 0.5 }); this.b2 = b2;
    const k2 = b2.cam;
    this.ein = g(k2);
    const eb = blatt(this.ein, { w: 420, h: 470, kicker: { de: 'EINRICHTUNG · MASSNAHMEN', en: 'ENTITY · MEASURES' }, kSize: 14, pad: 30 });
    this.einZ = Array.from({ length: 6 }, (_, i) => { const y = eb.y + 24 + i * 56, zg = g(eb.g); const ok = i !== 3; el('circle', { cx: eb.left + 12, cy: y, r: 12, fill: ok ? C.blue : 'none', stroke: ok ? C.blue : C.amberLine, 'stroke-width': 3, 'stroke-dasharray': ok ? '' : '5 4' }, zg); el('rect', { x: eb.left + 38, y: y - 6, width: 220 + ((i * 37) % 70), height: 12, rx: 6, fill: ok ? C.pBar : '#f0d9a0' }, zg); return { g: zg, y }; });
    this.lueckeKreis = el('circle', { r: 46, fill: 'none', stroke: C.amberLine, 'stroke-width': 5, 'stroke-dasharray': '12 8' }, k2);
    this.lueckeP = pille(k2, { de: 'nicht nachgekommen', en: 'not complied' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 24 });
    this.korrPfeil = el('path', { d: 'M 640 560 C 760 560 780 420 900 420', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round' }, k2);
    this.korrP = pille(k2, { de: 'Korrekturmaßnahmen · unverzüglich', en: 'corrective measures · without undue delay' }, { icon: 'cycle', col: C.blue, size: 26 });
    this.atBlaetter = [[{ de: 'PRÜFBERICHT', en: 'AUDIT REPORT' }, { de: 'festgestellte Mängel', en: 'identified deficiencies' }, 'search'], [{ de: 'MASSNAHMENPLAN', en: 'ACTION PLAN' }, { de: 'zur Beseitigung', en: 'to remedy them' }, 'calendar']].map(([k0, t0, ic]) => {
      const gr = g(k2); const b = blatt(gr, { w: 360, h: 300, kicker: k0, kSize: 14, pad: 28 });
      ikon(b.g, ic, b.left + 22, b.y + 30, 40, C.blueDeep); TB(b.g, b.left + 54, b.y + 40, t0, { size: 28, weight: 800, fill: C.pInk, maxW: 250, lh: 32 });
      linien(b.g, b.left, b.y + 120, 280, 3, 28, C.pBar, 10); return gr;
    });
    this.atP = pille(k2, { de: 'AT · NISG 2026 § 33 Abs. 3', en: 'AT · NISG 2026 § 33(3)' }, { col: C.blue, size: 22 });
    shot(b2, this.tF17 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 3: § 45 NISG, zwei Ausgänge ----------
    const b3 = buehne('beleg-strafe', { seed: 57, regalDeckkraft: 0.5 }); this.b3 = b3;
    const k3 = b3.cam;
    this.sd = g(k3);
    const sdb = blatt(this.sd, { w: 300, h: 380, kicker: { de: 'SELBSTDEKLARATION', en: 'SELF-DECLARATION' }, kSize: 13, pad: 26 });
    linien(sdb.g, sdb.left, sdb.y + 10, 240, 7, 34, C.pBar, 10);
    this.bahn = [el('path', { d: 'M 520 470 C 760 470 820 380 1080 380 H 1560', fill: 'none', stroke: C.blue, 'stroke-width': 6, 'stroke-linecap': 'round' }, k3), el('path', { d: 'M 520 650 C 760 650 820 720 1080 720 H 1300', fill: 'none', stroke: C.red, 'stroke-width': 6, 'stroke-linecap': 'round' }, k3)];
    this.bahnP = [pille(k3, { de: 'Lücke selbst gemeldet', en: 'gap reported by the entity' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 24 }), pille(k3, { de: 'wissentlich falsche Angabe', en: 'knowingly false statement' }, { icon: 'warn', col: C.red, size: 24 })];
    this.tor = g(k3); T(this.tor, 0, 10, '§ 45 NISG 2026', { mono: 1, size: 26, fill: C.muted, anchor: 'middle', ls: '0.06em' });
    this.schranke = g(this.tor);
    this.strafeP = g(k3); { el('circle', { r: 58, fill: 'url(#gRed)' }, this.strafeP); el('circle', { r: 44, fill: C.surface, stroke: C.red, 'stroke-width': 4 }, this.strafeP); iconPara(this.strafeP, 54, C.red); }
    this.strafeL = T(k3, 1440, 820, { de: 'eigens strafbar', en: 'an offence of its own' }, { size: 30, weight: 800, fill: C.red, anchor: 'middle' });
    this.durchP = pille(k3, { de: 'Behörde erfährt es nur daraus: nicht strafbar', en: 'authority learns it only from this: no offence' }, { icon: 'check', col: C.muted, size: 22 });
    shot(b3, this.tF18 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 4: Lücke mit Plan als Normalzustand ----------
    const b4 = buehne('beleg-normal', { seed: 59, regalDeckkraft: 0.5 }); this.b4 = b4;
    const k4 = b4.cam;
    this.nLief = kleinHaus(k4, 330, 800, 0.85, { label: { de: 'LIEFERANT', en: 'SUPPLIER' } });
    this.nKunde = kundeHaus(k4, 1600, 800, 0.72, { label: null });
    T(k4, 1600, 850, { de: 'KUNDE', en: 'CUSTOMER' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.nAntw = g(k4);
    const na = blatt(this.nAntw, { w: 560, h: 200, kicker: { de: 'ANTWORT DES LIEFERANTEN', en: "SUPPLIER'S ANSWER" }, kSize: 14, pad: 28, back: false });
    T(na.g, na.left, na.y + 30, { de: 'Noch nicht · geplant bis Ende des Quartals', en: 'Not yet · planned by the end of the quarter' }, { size: 24, weight: 800, fill: C.pInk });
    T(na.g, na.left, na.y + 72, { de: 'verantwortlich: Büroleitung mit IT-Dienstleister', en: 'responsible: office manager with the IT provider' }, { size: 21, weight: 700, fill: C.pInk });
    this.nPlan = g(k4);
    const np = blatt(this.nPlan, { w: 480, h: 420, kicker: { de: 'MASSNAHMENPLAN DES KUNDEN', en: "CUSTOMER'S ACTION PLAN" }, kSize: 14, pad: 30 });
    linien(np.g, np.left, np.y + 10, 400, 3, 36, C.pBar, 11);
    this.nSlot = el('rect', { x: np.left - 8, y: np.y + 100, width: 480 - 2 * np.pad + 16, height: 124, rx: 8, fill: 'none', stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '10 7' }, np.g);
    this.nSlotY = np.y + 162; linien(np.g, np.left, np.y + 252, 400, 2, 36, C.pBar, 11);
    k4.appendChild(this.nAntw); // die Antwort liegt über dem Plan
    this.normalP = pille(k4, { de: 'Lücke mit Plan: Normalzustand', en: 'gap with a plan: normal state' }, { marke: 'auslegung', col: C.purple, size: 26 });
    this.vierP = pille(k4, { de: 'vier Antworten · Maßnahmenplan', en: 'four answers · action plan' }, { icon: 'list', col: C.blue, size: 24 });
    shot(b4, this.tA19 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 5: Frist und Weg der Antworten ----------
    const b5 = buehne('beleg-frist', { seed: 61, regalDeckkraft: 0.5 }); this.b5 = b5;
    const k5 = b5.cam;
    this.fLinie = el('path', { d: 'M 300 470 H 1620', stroke: C.line, 'stroke-width': 6, 'stroke-linecap': 'round' }, k5);
    this.fBalken = el('rect', { x: 420, y: 452, width: 1060, height: 36, rx: 18, fill: 'rgba(79,140,255,0.18)', stroke: C.blue, 'stroke-width': 3 }, k5);
    this.fStart = g(k5); { el('circle', { cx: 420, cy: 470, r: 18, fill: C.blue }, this.fStart); TB(this.fStart, 300, 560, { de: 'Registrierungspflicht tritt ein', en: 'registration duty arises' }, { size: 26, weight: 800, maxW: 260, lh: 30 }); }
    this.fZwoelf = T(k5, 950, 430, { de: '12 Monate', en: '12 months' }, { size: 40, weight: 800, fill: C.blue, anchor: 'middle' });
    this.fBeh = behoerde(k5, 1560, 410, 0.9, { de: 'BEHÖRDE', en: 'AUTHORITY' });
    this.fSD = g(k5);
    const fsd = blatt(this.fSD, { w: 400, h: 300, kicker: { de: 'SELBSTDEKLARATION · STRUKTURIERT', en: 'SELF-DECLARATION · STRUCTURED' }, kSize: 13, pad: 26 });
    linien(fsd.g, fsd.left, fsd.y + 10, 340, 2, 32, C.pBar, 10);
    this.fLK = g(fsd.g); el('rect', { x: fsd.left - 8, y: fsd.y + 70, width: 400 - 2 * fsd.pad + 16, height: 52, rx: 8, fill: C.blueSoft }, this.fLK); ikon(this.fLK, 'link', fsd.left + 16, fsd.y + 96, 28, C.blueDeep); T(this.fLK, fsd.left + 42, fsd.y + 105, { de: 'Lieferketten', en: 'supply chains' }, { size: 26, weight: 800, fill: C.blueDeep });
    linien(fsd.g, fsd.left, fsd.y + 150, 340, 2, 32, C.pBar, 10);
    this.fWes = pille(k5, { de: 'wesentliche und wichtige Einrichtungen', en: 'essential and important entities' }, { icon: 'building', col: C.blue, size: 22 });
    // Weg der Antworten: Lieferant → Kunde → Behörde
    this.wLief = kleinHaus(k5, 330, 860, 0.6, { label: null });
    this.wKunde = kundeHaus(k5, 960, 860, 0.5, { label: null });
    this.wBeh = behoerde(k5, 1590, 830, 0.8, null);
    this.wLab = [T(k5, 330, 900, { de: 'SIE', en: 'YOU' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' }), T(k5, 960, 900, { de: 'KUNDE', en: 'CUSTOMER' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' }), T(k5, 1590, 900, { de: 'BEHÖRDE', en: 'AUTHORITY' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' })];
    this.wPfeile = [el('path', { d: 'M 430 700 C 560 620 760 620 880 660', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round' }, k5), el('path', { d: 'M 1060 660 C 1180 600 1380 600 1500 680', fill: 'none', stroke: C.blue, 'stroke-width': 5, 'stroke-linecap': 'round' }, k5)];
    this.wJahr = [T(k5, 655, 600, '2026', { mono: 1, size: 34, fill: C.blue, anchor: 'middle' }), T(k5, 1280, 600, '2027', { mono: 1, size: 34, fill: C.blue, anchor: 'middle' })];
    this.wRohP = pille(k5, { de: 'Rohmaterial', en: 'raw material' }, { marke: 'auslegung', col: C.purple, size: 24 });
    this.wDirekt = el('path', { d: 'M 360 600 C 600 380 1300 380 1560 600', fill: 'none', stroke: C.dim, 'stroke-width': 4, 'stroke-dasharray': '12 9' }, k5);
    this.wSchere = g(k5); iconCross(this.wSchere, 80, C.muted);
    this.wKeineP = pille(k5, { de: 'keine Eingabe bei der Behörde', en: 'not a filing with the authority' }, { icon: 'cross', col: C.muted, size: 22 });
    shot(b5, this.tF20 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 6: acht Vertragsinhalte ----------
    const b6 = buehne('beleg-vertrag', { seed: 67, regalDeckkraft: 0.5 }); this.b6 = b6;
    const k6 = b6.cam;
    this.vertrag = g(k6);
    const vb = blatt(this.vertrag, { w: 620, h: 640, kicker: { de: 'VERTRAG · LIEFERANT', en: 'CONTRACT · SUPPLIER' }, kSize: 14, pad: 32 });
    const KL = [['list', { de: 'Cybersicherheitsanforderungen', en: 'Cybersecurity requirements' }], ['group', { de: 'Ausbildung, ggf. Zertifizierungen', en: 'Training, certifications where appropriate' }], ['id', { de: 'Zuverlässigkeitsüberprüfungen', en: 'Background checks' }],
      ['warn', { de: 'Vorfälle unverzüglich melden', en: 'Report incidents without undue delay' }], ['search', { de: 'Prüfung oder Prüfberichte', en: 'Audit or audit reports' }], ['cycle', { de: 'Schwachstellen beheben', en: 'Handle vulnerabilities' }], ['link', { de: 'Unterauftragsvergabe', en: 'Subcontracting' }], ['door', { de: 'Pflichten bei Vertragsende', en: 'Obligations at contract end' }]];
    this.klauseln = KL.map(([ic, txt], i) => { const y = vb.y + 30 + i * 62, zg = g(vb.g); T(zg, vb.left, y + 8, String(i + 1), { mono: 1, size: 20, fill: C.pMuted }); ikon(zg, ic, vb.left + 44, y, 30, C.blueDeep); T(zg, vb.left + 74, y + 9, txt, { size: 24, weight: 700, fill: C.pInk }); return zg; });
    this.acht = g(k6); { el('circle', { r: 70, fill: C.blue }, this.acht); T(this.acht, 0, 24, '8', { size: 72, weight: 800, fill: '#fff', anchor: 'middle' }); }
    this.vDigital = pille(k6, { de: 'digitale Anbieter · EU', en: 'digital providers · EU' }, { icon: 'globe', col: C.blue, size: 24 });
    this.vAT = pille(k6, { de: 'AT · NISV 2026 § 2', en: 'AT · NISV 2026 § 2' }, { col: C.blue, size: 24 });
    this.vWes = pille(k6, { de: 'jede wesentliche und wichtige Einrichtung', en: 'every essential and important entity' }, { icon: 'building', col: C.blue, size: 22 });
    this.kopienV = [0, 1, 2, 3].map(() => { const gr = g(k6); const b = blatt(gr, { w: 160, h: 200, pad: 14, back: false }); linien(b.g, b.left, b.y0 + 30, 120, 8, 19, C.pBar2, 7); return gr; });
    this.deKunde = g(k6); { el('rect', { x: -150, y: -110, width: 300, height: 220, rx: 16, fill: 'none', stroke: C.dim, 'stroke-width': 3, 'stroke-dasharray': '12 9' }, this.deKunde); const kh = kundeHaus(this.deKunde, 0, 70, 0.3, { label: null }); T(this.deKunde, 0, 96, { de: 'KUNDE · DE', en: 'CUSTOMER · DE' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.08em' }); }
    this.deP = pille(k6, { de: 'nicht gebunden', en: 'not bound by law' }, { icon: 'cross', col: C.muted, gestrichelt: true, size: 22 });
    this.deLupe = g(k6); el('circle', { r: 60, fill: 'url(#gBlue)' }, this.deLupe); iconSearch(this.deLupe, 90, C.blue);
    this.deLese = pille(k6, { de: 'Prüfer lesen denselben Text', en: 'auditors read the same text' }, { icon: 'book', col: C.blue, size: 22 });
    shot(b6, this.tF22 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 7: was offen ist ----------
    const b7 = buehne('beleg-offen', { seed: 71, regalDeckkraft: 0.75 }); this.b7 = b7;
    const k7 = b7.cam;
    ordnerRegal(k7, 220, 330, 14);
    ordnerRegal(k7, 220, 520, 14);
    this.oLupe = g(k7); el('circle', { r: 64, fill: 'url(#gBlue)' }, this.oLupe); iconSearch(this.oLupe, 100, C.blue);
    this.oLeer = g(k7); { el('circle', { r: 86, fill: 'none', stroke: C.red, 'stroke-width': 6, 'stroke-dasharray': '16 11' }, this.oLeer); TB(this.oLeer, -70, -6, { de: 'amtliches Muster', en: 'official model' }, { size: 26, weight: 800, fill: C.red, maxW: 150, lh: 30 }); }
    this.oKeinP = pille(k7, { de: 'keinen gefunden', en: 'none found' }, { marke: 'luecke', col: C.red, gestrichelt: true, size: 24 });
    this.oQuellen = pille(k7, { de: 'Fragen folgen den genannten Quellen', en: 'questions follow the sources named' }, { icon: 'book', col: C.blue, size: 22 });
    this.oHammer = g(k7); { el('circle', { r: 66, fill: 'none', stroke: C.muted, 'stroke-width': 4, 'stroke-dasharray': '11 8' }, this.oHammer); iconGavel(this.oHammer, 70, C.muted); }
    this.oHammerT = TB(k7, 1240, 760, { de: '„unverzüglich“ für kleine Lieferanten?', en: '"without undue delay" for small suppliers?' }, { size: 26, weight: 800, maxW: 520, lh: 30, fill: C.muted });
    this.oNichtG = pille(k7, { de: 'nicht gesucht', en: 'not searched' }, { marke: 'luecke', col: C.red, gestrichelt: true, size: 24 });
    this.oHb = g(k7);
    const hb = blatt(this.oHb, { w: 420, h: 300, kicker: { de: 'HANDBUCH · ABSCHNITT 6', en: 'HANDBOOK · SECTION 6' }, kSize: 14, pad: 28 });
    this.oHbZ = [['6.6', { de: 'kein amtliches Muster', en: 'no official model' }], ['6.22', { de: '„unverzüglich“: nicht gesucht', en: '"without undue delay": not searched' }]].map(([n, txt], i) => { const zg = g(hb.g); const y = hb.y + 40 + i * 70; markerShape(g(zg, { transform: `translate(${hb.left + 12} ${y - 8})` }), 'luecke', 22); T(zg, hb.left + 34, y, n, { mono: 1, size: 20, fill: C.pMuted }); T(zg, hb.left + 94, y, txt, { size: 21, weight: 700, fill: C.pInk }); return zg; });
    shot(b7, this.tL25 - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [b1, b2, b3, b4, b5, b6, b7];

    // ---------- Einblendungen ----------
    kopf(this.tJetzt, this.tF17 - 0.3, K, { de: 'Noch nicht, mit Termin', en: 'Not yet, with a date' });
    kopf(this.tF17, this.tF18 - 0.3, K, { de: 'Erst die Lücke, dann der Plan', en: 'First the gap, then the plan' });
    kopf(this.tF18, this.tA19 - 0.3, K, { de: 'Österreich: § 45 NISG 2026', en: 'Austria: § 45 NISG 2026' });
    kopf(this.tA19, this.tF20 - 0.3, K, { de: 'Lücke mit Plan', en: 'A gap with a plan' });
    kopf(this.tF20, this.tF22 - 0.3, K, { de: 'Die Selbstdeklaration des Kunden', en: "The customer's self-declaration" });
    kopf(this.tF22, this.tL25 - 0.3, K, { de: 'Acht Vertragsinhalte', en: 'Eight contract contents' });
    kopf(this.tL25, this.tEnde - 0.3, K, { de: 'Was offen ist', en: 'What is open' });
  },

  zeichnen(t) {
    // ---------- Bühne 1 ----------
    if (this.b1.vis) {
      kamera(this.b1, [960, 540], 1);
      this.kBuecher.forEach((b, i) => { const t0 = this.tKern + i * 0.15, k = P(t, t0, 0.5, E.out); tr(b, 510 + i * 300, 760 + (1 - k) * 30, 1, 0); O(b, k); O(this.kLinien[i], P(t, this.tVoll + 0.2 + i * 0.1, 0.4)); });
      tr(this.kNoch, 960, 400, Math.max(0.01, P(t, this.tNoch, 0.5, E.back))); O(this.kNoch, P(t, this.tNoch, 0.2));
      tr(this.kVoll, 960, 520, Math.max(0.01, P(t, this.tVoll, 0.5, E.back))); O(this.kVoll, P(t, this.tVoll, 0.2));
    }
    // ---------- Bühne 2 ----------
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      const ek = P(t, this.tF17, 0.6, E.out); tr(this.ein, 420, 540 + (1 - ek) * 20, 1, -1.5); O(this.ein, ek);
      const lz = this.einZ[3]; const lp = [420 - 210 + 30 + 12, 540 + lz.y];
      const lk = P(t, this.tFest - 0.1, 0.5, E.back); tr(this.lueckeKreis, lp[0], lp[1], Math.max(0.01, lk)); O(this.lueckeKreis, P(t, this.tFest - 0.1, 0.2)); this.lueckeKreis.setAttribute('stroke-dashoffset', (-t * 16).toFixed(1));
      tr(this.lueckeP, 800, 720, Math.max(0.01, P(t, this.tFest + 0.2, 0.45, E.back))); O(this.lueckeP, P(t, this.tFest + 0.2, 0.2));
      zeichne(this.korrPfeil, P(t, this.tKorr - 0.2, 0.7));
      tr(this.korrP, 1180, 330, Math.max(0.01, P(t, this.tKorr, 0.45, E.back))); O(this.korrP, P(t, this.tKorr, 0.2));
      this.atBlaetter.forEach((b, i) => { const t0 = i === 0 ? this.tMaengel - 0.2 : this.tPlan - 0.2, k = P(t, t0, 0.6, E.out); tr(b, 1080 + i * 400, 640 + (1 - k) * 24, 0.92, i ? 1.5 : -1.5); O(b, k); });
      tr(this.atP, 1280, 440, Math.max(0.01, P(t, this.tAT, 0.45, E.back))); O(this.atP, P(t, this.tAT, 0.2));
    }
    // ---------- Bühne 3 ----------
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      const sk0 = P(t, this.tF18, 0.6, E.out); tr(this.sd, 360, 560 + (1 - sk0) * 20, 1, -2); O(this.sd, sk0);
      tr(this.tor, 1200, 560, 1); O(this.tor, P(t, this.tStraf - 0.2, 0.5));
      // Schranke: offen für die selbst gemeldete Lücke, die falsche Angabe trifft auf den roten Paragrafen
      this.schranke.setAttribute('transform', `rotate(${lerp(-90, 0, P(t, this.tFalsch + 0.2, 0.6)).toFixed(1)})`);
      zeichne(this.bahn[0], P(t, this.tSelbstD - 0.3, 1.2)); zeichne(this.bahn[1], P(t, this.tFalsch, 1.0));
      tr(this.bahnP[0], 860, 330, Math.max(0.01, P(t, this.tSelbstD, 0.45, E.back))); O(this.bahnP[0], P(t, this.tSelbstD, 0.2));
      tr(this.bahnP[1], 860, 790, Math.max(0.01, P(t, this.tFalsch, 0.45, E.back))); O(this.bahnP[1], P(t, this.tFalsch, 0.2));
      tr(this.durchP, 1420, 300, Math.max(0.01, P(t, this.tNur + 0.3, 0.45, E.back))); O(this.durchP, P(t, this.tNur + 0.3, 0.2));
      const st = P(t, this.tEigens, 0.45, E.back); tr(this.strafeP, 1440, 720, Math.max(0.01, st) * (1 + 0.08 * puls(t, this.tEigens + 0.4, 1, 8))); O(this.strafeP, P(t, this.tEigens, 0.2)); O(this.strafeL, P(t, this.tEigens + 0.2, 0.3));
    }
    // ---------- Bühne 4 ----------
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      const ein = P(t, this.tA19, 0.6, E.out); O(this.nLief.g, ein); O(this.nKunde.g, ein);
      tr(this.normalP, 960, 300, Math.max(0.01, P(t, this.tNormal, 0.45, E.back))); O(this.normalP, Math.min(P(t, this.tNormal, 0.2), 1 - P(t, this.tLief - 0.3, 0.4)));
      const pk = P(t, this.tVerschont - 0.3, 0.6, E.out); tr(this.nPlan, 1450, 470 + (1 - pk) * 20, 0.9, 1.5); O(this.nPlan, pk);
      // die Antwort des Lieferanten wandert in eine Zeile des Kundenplans
      const ak = P(t, this.tLief, 0.6, E.out), fk = P(t, this.tGibt, 1.3, E.io);
      const pos = bogen([560, 470], [1450, 470 + this.nSlotY * 0.9], fk, 120);
      tr(this.nAntw, pos[0], pos[1], lerp(1, 0.68, fk), lerp(-1.5, 1.5, fk)); O(this.nAntw, ak);
      this.nSlot.setAttribute('stroke', t > this.tSelbstE ? C.blue : C.line); O(this.nSlot, 1 - P(t, this.tGibt + 1.2, 0.3));
      tr(this.vierP, 960, 300, Math.max(0.01, P(t, this.tBegr, 0.45, E.back))); O(this.vierP, P(t, this.tBegr, 0.2));
    }
    // ---------- Bühne 5 ----------
    if (this.b5.vis) {
      kamera(this.b5, [960, 540], 1);
      const zweit = P(t, this.tA21 - 0.4, 0.8, E.io); // Wechsel zur Auslegung: Weg der Antworten
      const lk = P(t, this.tWes - 0.3, 0.8); zeichne(this.fLinie, lk); O(this.fLinie, 1 - zweit);
      O(this.fStart, P(t, this.tWes, 0.5) * (1 - zweit));
      tr(this.fWes, 700, 300, Math.max(0.01, P(t, this.tWes, 0.45, E.back))); O(this.fWes, P(t, this.tWes, 0.2) * (1 - zweit));
      const zb = P(t, this.tZwoelf - 0.1, 1.0, E.out); this.fBalken.setAttribute('width', (1060 * zb).toFixed(1)); O(this.fBalken, P(t, this.tZwoelf - 0.1, 0.2) * (1 - zweit));
      O(this.fZwoelf, P(t, this.tZwoelf + 0.3, 0.4) * (1 - zweit));
      O(this.fBeh.g, P(t, this.tStrukt - 0.2, 0.5) * (1 - zweit));
      const sk0 = P(t, this.tStrukt, 0.6, E.out); tr(this.fSD, 1180, 720 + (1 - sk0) * 24, 0.85, 1.5); O(this.fSD, sk0 * (1 - zweit));
      O(this.fLK, 0.2 + 0.8 * P(t, this.tLK, 0.4));
      // Auslegung: Lieferant → Kunde 2026 → Behörde 2027; kein direkter Weg zur Behörde
      const w = P(t, this.tA21, 0.6, E.out);
      [this.wLief.g, this.wKunde.g, this.wBeh.g, ...this.wLab].forEach((e) => O(e, w));
      tr(this.wRohP, 655, 520, Math.max(0.01, P(t, this.tRoh, 0.45, E.back))); O(this.wRohP, P(t, this.tRoh, 0.2));
      zeichne(this.wPfeile[0], P(t, this.tFragt - 0.2, 0.7)); zeichne(this.wPfeile[1], P(t, this.tBehoerde - 0.4, 0.7));
      O(this.wJahr[0], P(t, this.tFragt, 0.4)); O(this.wJahr[1], P(t, this.tBehoerde - 0.2, 0.4));
      O(this.wDirekt, P(t, this.tKeineE - 0.6, 0.4) * (1 - 0.6 * P(t, this.tKeineE + 0.4, 0.4)));
      tr(this.wSchere, 960, 438, Math.max(0.01, P(t, this.tKeineE + 0.2, 0.45, E.back))); O(this.wSchere, P(t, this.tKeineE + 0.2, 0.2));
      tr(this.wKeineP, 960, 330, Math.max(0.01, P(t, this.tKeineE + 0.4, 0.45, E.back))); O(this.wKeineP, P(t, this.tKeineE + 0.4, 0.2));
    }
    // ---------- Bühne 6 ----------
    if (this.b6.vis) {
      kamera(this.b6, [960, 540], 1);
      const viele = P(t, this.tA24 - 0.2, 0.8, E.io);
      const vk = P(t, this.tF22, 0.6, E.out); tr(this.vertrag, lerp(960, 820, viele), 560 + (1 - vk) * 24, lerp(1, 0.8, viele), -1); O(this.vertrag, vk);
      this.klauseln.forEach((k, i) => O(k, 0.12 + 0.88 * P(t, this.tV[i] - 0.1, 0.35)));
      const ak = P(t, this.tAcht, 0.5, E.back); tr(this.acht, lerp(1380, 1140, viele), lerp(320, 250, viele), Math.max(0.01, ak) * lerp(1, 0.7, viele)); O(this.acht, P(t, this.tAcht, 0.2));
      tr(this.vDigital, 1500, 470, Math.max(0.01, P(t, this.tDigital, 0.45, E.back))); O(this.vDigital, P(t, this.tDigital, 0.2) * (1 - viele));
      tr(this.vAT, 1500, 560, Math.max(0.01, P(t, this.tF23, 0.45, E.back))); O(this.vAT, P(t, this.tF23, 0.2) * (1 - viele));
      tr(this.vWes, 1500, 640, Math.max(0.01, P(t, this.tJede, 0.45, E.back))); O(this.vWes, P(t, this.tJede, 0.2) * (1 - viele));
      // Muster der Klauseln: Kopien bei digitalen Anbietern in der EU und bei NIS2-Kunden in Österreich
      this.kopienV.forEach((k, i) => { const t0 = (i < 2 ? this.tUnion : this.tInAT) - 0.2 + (i % 2) * 0.2, kk = P(t, t0, 0.7, E.out); tr(k, lerp(820, 200 + (i % 2) * 200, kk), lerp(560, i < 2 ? 330 : 700, kk), lerp(0.4, 1, kk), (i % 2 ? 4 : -4)); O(k, P(t, t0, 0.2)); });
      const dk = P(t, this.tDeutsch - 0.2, 0.6, E.out); tr(this.deKunde, 1480, 420 + (1 - dk) * 20, 1); O(this.deKunde, dk);
      tr(this.deP, 1480, 580, Math.max(0.01, P(t, this.tNichtGeb, 0.45, E.back))); O(this.deP, P(t, this.tNichtGeb, 0.2));
      const lk = P(t, this.tPruefer - 0.3, 1.0, E.io); const lp = lerp2([1480, 420], [800, 520], lk);
      tr(this.deLupe, lp[0] + 8 * Math.sin(t * 2), lp[1], 1); O(this.deLupe, P(t, this.tPruefer - 0.3, 0.3));
      tr(this.deLese, 1480, 760, Math.max(0.01, P(t, this.tPruefer + 0.4, 0.45, E.back))); O(this.deLese, P(t, this.tPruefer + 0.4, 0.2));
    }
    // ---------- Bühne 7 ----------
    if (this.b7.vis) {
      const zweit = P(t, this.tGericht - 0.6, 1.0, E.io), ende = P(t, this.tAbs6 - 0.6, 0.9, E.io);
      kamera(this.b7, [960, 540], 1);
      const lk = clamp((t - this.tL25 - 0.2) / Math.max(1, this.tKeinen - this.tL25 - 0.2));
      tr(this.oLupe, lerp(320, 640, E.sine(lk)) + 20 * Math.sin(t * 1.4), 420 + 60 * Math.sin(lk * Math.PI), 1); O(this.oLupe, Math.min(P(t, this.tL25, 0.4), 1 - P(t, this.tKeinen + 0.4, 0.4)));
      const ek = P(t, this.tKeinen - 0.1, 0.5, E.back); tr(this.oLeer, lerp(820, 1500, ende), lerp(460, 380, ende), Math.max(0.01, ek) * lerp(1, 0.4, ende)); O(this.oLeer, Math.min(P(t, this.tKeinen - 0.1, 0.2), 1 - ende));
      tr(this.oKeinP, 820, 600, Math.max(0.01, P(t, this.tKeinen + 0.2, 0.45, E.back))); O(this.oKeinP, Math.min(P(t, this.tKeinen + 0.2, 0.2), 1 - ende));
      tr(this.oQuellen, 820, 680, Math.max(0.01, P(t, this.tFolgen, 0.45, E.back))); O(this.oQuellen, Math.min(P(t, this.tFolgen, 0.2), 1 - ende));
      const hk = P(t, this.tGericht - 0.2, 0.5, E.back); tr(this.oHammer, lerp(1340, 1500, ende), lerp(560, 380, ende), Math.max(0.01, hk) * lerp(1, 0.4, ende)); O(this.oHammer, Math.min(P(t, this.tGericht - 0.2, 0.2), 1 - ende));
      O(this.oHammerT, P(t, this.tGericht + 0.3, 0.4) * (1 - ende));
      tr(this.oNichtG, 1460, 860, Math.max(0.01, P(t, this.tNichtG, 0.45, E.back))); O(this.oNichtG, Math.min(P(t, this.tNichtG, 0.2), 1 - ende));
      const hb = P(t, this.tAbs6 - 0.4, 0.6, E.out); tr(this.oHb, 1460, 470 + (1 - hb) * 24, 1, 1.5); O(this.oHb, hb);
      this.oHbZ.forEach((z, i) => O(z, P(t, this.tAbs6 + 0.2 + i * 0.3, 0.3)));
    }
  },
});
