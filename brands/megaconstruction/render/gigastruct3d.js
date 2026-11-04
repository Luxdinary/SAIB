// Gigastruct 3D layer: one persistent WebGL canvas under all scenes, drawn as a pure function of time.
//
// Data comes from window.GS_SPEC (written by render_gigastruct.py from plan.layout.model3d):
//   palette  {bg, model, edge, accent, water, seabed, ground, compare, grid}
//   beats    [{id, start, end}]                       absolute seconds, from the timed plan
//   objects  [{id, kind, ...geometry, props:{...}}]   kinds: element, water, seabed, ground, tower, boat, pontoon
//   anchors  {name: [x, y, z]}                         world points; DOM elements with data-anchor follow them
//   shots    {beatId: {cam:{p0,p1,l0,l1,fov}, props:{"obj.prop": value | [[t, v], ...]}}}
//   transitions {beatId: {type: iris|blende, seconds, x, y}}   into that beat (plan beats[].overlay.transition);
//            the outgoing shot keeps running on a second canvas (#gs3dprev) while #gs3d opens as a circle or fades in
// Units are metres. x = along the structure, y = up, z = across. Times inside shots are seconds from the beat start.
// HyperFrames seek protocol: render(t) is called from the hf-seek listener; no clock, no randomness.
import * as THREE from "../vendor/three.module.min.js";

const S = window.GS_SPEC;
const P = S.palette;
const canvas = document.getElementById("gs3d");
const prevCanvas = document.getElementById("gs3dprev");
function makeRenderer(cv) {
  const r = new THREE.WebGLRenderer({ canvas: cv, antialias: true, preserveDrawingBuffer: true });
  r.setPixelRatio(1);
  r.setSize(1080, 1920, false);
  r.shadowMap.enabled = true;
  r.shadowMap.type = THREE.PCFSoftShadowMap;
  r.localClippingEnabled = true;
  r.outputColorSpace = THREE.SRGBColorSpace;
  return r;
}
const renderer = makeRenderer(canvas);
const TR = S.transitions || {};
const prevRenderer = prevCanvas && Object.keys(TR).length ? makeRenderer(prevCanvas) : null;

const scene = new THREE.Scene();
scene.background = new THREE.Color(P.bg);
const FOG = [S.fog?.[0] ?? 600, S.fog?.[1] ?? 2600];
scene.fog = new THREE.Fog(P.haze || P.bg, FOG[0], FOG[1]);
const camera = new THREE.PerspectiveCamera(S.fov ?? 38, 1080 / 1920, 1, 30000);

// sky dome (world space, follows the camera): deep steel blue at the zenith, a light haze band at the horizon,
// darker water below. Gives every shot a lit background with depth instead of a flat colour; no glow, no sun disc.
const dome = new THREE.Mesh(
  new THREE.SphereGeometry(18000, 48, 24),
  new THREE.ShaderMaterial({
    side: THREE.BackSide, depthWrite: false, fog: false,
    uniforms: {
      top: { value: new THREE.Color(P.sky_top || "#10223a") }, mid: { value: new THREE.Color(P.bg) },
      haze: { value: new THREE.Color(P.haze || "#4b6f8f") }, deep: { value: new THREE.Color(P.deep || "#132536") },
    },
    vertexShader: "varying vec3 vDir; void main(){ vDir = normalize(position); gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }",
    fragmentShader: "uniform vec3 top; uniform vec3 mid; uniform vec3 haze; uniform vec3 deep; varying vec3 vDir;" +
      "void main(){ float y = vDir.y; vec3 c;" +
      " if (y > 0.0) { c = mix(haze, mid, smoothstep(0.0, 0.10, y)); c = mix(c, top, smoothstep(0.10, 0.65, y)); }" +
      " else { c = mix(haze, deep, smoothstep(0.0, 0.18, -y)); }" +
      // three.js only expands #include at the start of a line
      " gl_FragColor = vec4(c, 1.0);\n#include <colorspace_fragment>\n}",
  }),
);
dome.renderOrder = -10;
scene.add(dome);

// light: warm key with a contact shadow, cool rim, soft sky fill (architectural model look)
scene.add(new THREE.HemisphereLight("#d6e4f2", P.bg, 0.9));
const key = new THREE.DirectionalLight("#ffe2c4", 2.1);
key.position.set(220, 340, 260);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
Object.assign(key.shadow.camera, { left: -420, right: 420, top: 420, bottom: -420, near: 10, far: 1600 });
key.shadow.bias = -0.0004;
scene.add(key);
const rim = new THREE.DirectionalLight("#9cc3ff", 0.9);
rim.position.set(-300, 160, -280);
scene.add(rim);

const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.82, metalness: 0.0, ...o });
const edgeMat = (color, opacity) => new THREE.LineBasicMaterial({ color, transparent: true, opacity });

const objects = {};   // id -> {group, def, apply(props)}

function shapeWithTubes(w, h, tubes) {
  // cross-section in the z/y plane: outer rectangle, tube holes; extruded along x
  const s = new THREE.Shape();
  s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w / 2, h); s.lineTo(-w / 2, h); s.lineTo(-w / 2, 0);
  for (const t of tubes || []) {
    const hole = new THREE.Path();
    const x0 = -w / 2 + t.x - t.w / 2, y0 = t.y ?? 1, r = Math.min(t.r ?? 0, t.w / 2);
    hole.moveTo(x0, y0); hole.lineTo(x0 + t.w, y0); hole.lineTo(x0 + t.w, y0 + t.h - r);
    if (r > 0) hole.quadraticCurveTo(x0 + t.w, y0 + t.h, x0 + t.w - r, y0 + t.h); else hole.lineTo(x0 + t.w, y0 + t.h);
    hole.lineTo(x0 + r, y0 + t.h);
    if (r > 0) hole.quadraticCurveTo(x0, y0 + t.h, x0, y0 + t.h - r); else hole.lineTo(x0, y0 + t.h);
    hole.lineTo(x0, y0);
    s.holes.push(hole);
  }
  return s;
}

function buildElement(d) {
  const g = new THREE.Group();
  const n = d.segments || 1, gap = d.gap ?? 0.35, L = d.length, segL = (L - gap * (n - 1)) / n;
  const clipTop = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1e6);   // cutaway: removes everything above its constant
  const shape = shapeWithTubes(d.width, d.height, d.tubes);
  const geo = new THREE.ExtrudeGeometry(shape, { depth: segL, bevelEnabled: false });
  geo.rotateY(Math.PI / 2);                       // extrude along +x
  const m = mat(P.model, { side: THREE.DoubleSide, clippingPlanes: [clipTop] });
  const inner = mat(P.model_inner || P.model, { side: THREE.BackSide, clippingPlanes: [clipTop] });
  const em = edgeMat(P.edge, 0.55);
  const segs = [];
  for (let i = 0; i < n; i++) {
    const seg = new THREE.Group();
    const mesh = new THREE.Mesh(geo, m); mesh.castShadow = true; mesh.receiveShadow = true;
    const back = new THREE.Mesh(geo, inner);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 30), em);
    seg.add(mesh, back, edges);
    seg.position.x = -L / 2 + i * (segL + gap);
    g.add(seg); segs.push(seg);
  }
  // bulkheads: thin plates closing both ends (make the element buoyant)
  const bh = new THREE.Group();
  const plate = new THREE.Mesh(new THREE.BoxGeometry(0.8, d.height * 0.96, d.width * 0.96), mat(P.accent, { roughness: 0.6 }));
  const p1 = plate.clone(); p1.position.set(-L / 2 - 0.5, d.height / 2, 0);
  const p2 = plate.clone(); p2.position.set(L / 2 + 0.5, d.height / 2, 0);
  bh.add(p1, p2); g.add(bh);
  // highlight frame: accent edges around the whole block
  const hl = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(L + 1.5, d.height + 1, d.width + 1.5)), edgeMat(P.accent, 1));
  hl.position.y = d.height / 2; g.add(hl);
  return {
    group: g,
    apply(pr) {
      const rev = pr.reveal ?? n;
      segs.forEach((s, i) => {
        const k = Math.max(0, Math.min(1, rev - i));
        s.visible = k > 0.001;
        s.scale.set(1, Math.max(0.001, k < 1 ? 0.15 + 0.85 * easeOut(k) : 1), 1);
      });
      bh.visible = (pr.bulkheads ?? 0) > 0.5;
      hl.visible = (pr.highlight ?? 0) > 0.01;
      hl.material.opacity = pr.highlight ?? 0;
      const cut = pr.cut ?? 0;   // 0 = closed, 1 = roof removed down to 45 % of the height (clip plane per element)
      clipTop.constant = cut > 0.001 ? (g.position.y + d.height * (1 - 0.55 * cut)) : 1e6;
      m.opacity = inner.opacity = pr.opacity ?? 1;
      m.transparent = inner.transparent = (pr.opacity ?? 1) < 0.999;
    },
  };
}

function buildWater(d) {
  const g = new THREE.Group();
  const top = new THREE.Mesh(new THREE.PlaneGeometry(d.size, d.size), mat(P.water, { transparent: true, opacity: 0.5, roughness: 1.0, depthWrite: false }));
  top.rotation.x = -Math.PI / 2;
  const lines = new THREE.GridHelper(d.size, Math.round(d.size / 40), P.water_line || P.edge, P.water_line || P.edge);
  lines.material.transparent = true; lines.material.opacity = 0.18; lines.position.y = 0.05;
  g.add(top, lines);
  const cell = d.size / Math.round(d.size / 40);
  return {
    group: g,
    apply(pr, t) {   // the surface grid drifts slowly (current), a pure function of time
      top.material.opacity = 0.5 * (pr.opacity ?? 1); lines.material.opacity = 0.18 * (pr.opacity ?? 1);
      lines.position.x = ((t || 0) * 2.2) % cell; lines.position.z = ((t || 0) * 0.9) % cell;
    },
  };
}

function buildChain(d) {
  // the whole tunnel as a row of `count` elements along +x (instanced boxes, schematic: all drawn as standard elements).
  // props: reveal (elements shown, float), done (first n in the reached-state green), lead (index drawn in the accent),
  //        pulse (float index of a moving accent light, e.g. a train), pulse_w (its width in elements)
  const n = d.count, L = d.length, gap = d.gap ?? 0.6, step = L + gap;
  const geo = new THREE.BoxGeometry(L, d.height, d.width); geo.translate(0, d.height / 2, 0);
  const mesh = new THREE.InstancedMesh(geo, mat("#ffffff", { roughness: 0.8 }), n);
  mesh.castShadow = true; mesh.receiveShadow = true;
  mesh.frustumCulled = false;   // the bounding sphere would only cover the first instance
  const g = new THREE.Group(); g.add(mesh);
  const cModel = new THREE.Color(P.model), cAcc = new THREE.Color(P.accent), cGreen = new THREE.Color(P.green || "#5CD08A"), tmpC = new THREE.Color();
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < n; i++) { m4.makeTranslation(i * step, 0, 0); mesh.setMatrixAt(i, m4); mesh.setColorAt(i, cModel); }
  return {
    group: g,
    apply(pr) {
      const rev = Math.max(0, Math.min(n, pr.reveal ?? n));
      mesh.count = Math.ceil(rev);
      const last = Math.ceil(rev) - 1, kLast = rev - Math.floor(rev);
      const done = pr.done ?? 0, lead = pr.lead ?? -1, pulse = pr.pulse ?? -999, pw = pr.pulse_w ?? 3;
      for (let i = 0; i < mesh.count; i++) {
        const sy = i === last && kLast > 0.001 ? 0.15 + 0.85 * easeOut(kLast) : 1;
        m4.makeScale(1, sy, 1); m4.setPosition(i * step, 0, 0); mesh.setMatrixAt(i, m4);
        const pk = Math.max(0, 1 - Math.abs(i - pulse) / pw);
        if (i < done) tmpC.copy(cGreen); else if (i === lead) tmpC.copy(cAcc); else tmpC.copy(cModel).lerp(cAcc, pk);
        mesh.setColorAt(i, tmpC);
      }
      mesh.instanceMatrix.needsUpdate = true; mesh.instanceColor.needsUpdate = true;
    },
  };
}

function buildLand(d) {
  // a stylised coast: a flat plateau with a sloped edge towards the water, matte, with a coarse survey grid
  const g = new THREE.Group();
  const lm = mat(P.land || P.ground, { roughness: 1 });
  const body = new THREE.Mesh(new THREE.BoxGeometry(d.size_x, d.height, d.size_z), lm);
  body.position.y = d.height / 2 - d.depth; body.receiveShadow = true; g.add(body);
  const grid = new THREE.GridHelper(Math.max(d.size_x, d.size_z), Math.round(Math.max(d.size_x, d.size_z) / 120), P.grid, P.grid);
  grid.material.transparent = true; grid.material.opacity = 0.35; grid.position.y = d.height - d.depth + 0.2; g.add(grid);
  return { group: g, apply() {} };
}

function buildBox(d) {
  // a plain box in a palette colour (e.g. a vehicle or a marker); size [x, y, z]
  const s = d.size || [10, 10, 10];
  const m = mat(P[d.color] || d.color || P.model, { roughness: 0.6, transparent: true });
  const b = new THREE.Mesh(new THREE.BoxGeometry(s[0], s[1], s[2]), m); b.position.y = s[1] / 2; b.castShadow = true;
  const g = new THREE.Group(); g.add(b);
  return { group: g, apply(pr) { m.opacity = pr.opacity ?? 1; } };
}

function buildSeabed(d) {
  // seabed with an excavated trench (stylised, trench along x)
  const g = new THREE.Group();
  const m = mat(P.seabed, { roughness: 0.95 });
  const side = (d.size - d.trench_w) / 2;
  for (const s of [-1, 1]) {
    const p = new THREE.Mesh(new THREE.BoxGeometry(d.size, 2, side), m);
    p.position.set(0, -1, s * (d.trench_w / 2 + side / 2)); p.receiveShadow = true; g.add(p);
  }
  const floor = new THREE.Mesh(new THREE.BoxGeometry(d.size, 2, d.trench_w), m);
  floor.position.y = -d.trench_d - 1; floor.receiveShadow = true; g.add(floor);
  const grid = new THREE.GridHelper(d.size, Math.round(d.size / 50), P.grid, P.grid);
  grid.material.transparent = true; grid.material.opacity = 0.35; grid.position.y = 0.1; g.add(grid);
  return { group: g, apply() {} };
}

function buildGround(d) {
  const g = new THREE.Group();
  const p = new THREE.Mesh(new THREE.PlaneGeometry(d.size, d.size), mat(P.ground, { roughness: 1 }));
  p.rotation.x = -Math.PI / 2; p.receiveShadow = true; g.add(p);
  const grid = new THREE.GridHelper(d.size, Math.round(d.size / (d.grid ?? 25)), P.grid, P.grid);
  grid.material.transparent = true; grid.material.opacity = 0.5; grid.position.y = 0.05; g.add(grid);
  return { group: g, apply(pr) { p.material.opacity = pr.opacity ?? 1; p.material.transparent = (pr.opacity ?? 1) < 1; } };
}

function buildTower(d) {
  // stylised lattice tower for scale comparisons: four tapered legs, platforms, mast. Not a likeness.
  const H = d.height, B = d.base, n = d.count || 1, gap = d.spacing ?? B * 1.25;
  const g = new THREE.Group();
  const buildPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1e6);   // prop build 0..1: construction rising
  const tm = mat(P[d.color] || P.compare, { roughness: 0.7, clippingPlanes: [buildPlane] });
  const em = edgeMat(P.compare_edge || P.edge, 0.7);
  em.clippingPlanes = [buildPlane];
  const one = new THREE.Group();
  const legTop = H * 0.62, topW = B * 0.12;
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
    const a = new THREE.Vector3(sx * B / 2, 0, sz * B / 2), b = new THREE.Vector3(sx * topW / 2, legTop, sz * topW / 2);
    const len = a.distanceTo(b), leg = new THREE.Mesh(new THREE.BoxGeometry(B * 0.07, len, B * 0.07), tm);
    leg.position.copy(a.clone().add(b).multiplyScalar(0.5)); leg.lookAt(b); leg.rotateX(Math.PI / 2); leg.castShadow = true; one.add(leg);
  }
  for (const [y, w] of (d.platforms || [[0.17, 0.62], [0.35, 0.36]])) {
    const pl = new THREE.Mesh(new THREE.BoxGeometry(B * w, H * 0.012, B * w), tm); pl.position.y = H * y; pl.castShadow = true; one.add(pl);
    const pe = new THREE.LineSegments(new THREE.EdgesGeometry(pl.geometry), em); pe.position.copy(pl.position); one.add(pe);
  }
  const mast = new THREE.Mesh(new THREE.BoxGeometry(topW, H - legTop, topW), tm); mast.position.y = legTop + (H - legTop) / 2; mast.castShadow = true; one.add(mast);
  const copies = [];
  for (let i = 0; i < n; i++) { const c = one.clone(); c.position.x = (i - (n - 1) / 2) * gap; g.add(c); copies.push(c); }
  return {
    group: g,
    apply(pr) {
      const rev = pr.reveal ?? n;
      copies.forEach((c, i) => { const k = Math.max(0, Math.min(1, rev - i)); c.visible = k > 0.001; c.scale.set(1, Math.max(0.001, easeOut(k)), 1); });
      const b = pr.build ?? 1;
      buildPlane.constant = b < 0.999 ? g.position.y + H * b : 1e6;
    },
  };
}

function buildBoat(d) {
  // stylised tug: hull + cabin; `count` boats in a fan
  const g = new THREE.Group();
  const hm = mat(P.boat || P.compare, { roughness: 0.6 }), cm = mat(P.model, { roughness: 0.7 });
  for (let i = 0; i < (d.count || 1); i++) {
    const b = new THREE.Group();
    const hull = new THREE.Mesh(new THREE.BoxGeometry(d.length ?? 30, 4, d.width ?? 11), hm); hull.position.y = 1; hull.castShadow = true;
    const cab = new THREE.Mesh(new THREE.BoxGeometry((d.length ?? 30) * 0.35, 5, (d.width ?? 11) * 0.7), cm); cab.position.set(-(d.length ?? 30) * 0.12, 5.5, 0); cab.castShadow = true;
    b.add(hull, cab);
    const p = (d.positions || [])[i] || [i * 40, 0, 0];
    b.position.set(p[0], p[1], p[2]); b.rotation.y = p[3] ?? 0;
    g.add(b);
  }
  return { group: g, apply() {} };
}

function buildPontoon(d) {
  // stylised immersion pontoon straddling the element: deck plus two legs
  const g = new THREE.Group();
  const pm = mat(P.boat || P.compare, { roughness: 0.6 });
  const deckY = d.deck_y ?? 16, cables = [];
  for (const x of d.xs || [0]) {
    const deck = new THREE.Mesh(new THREE.BoxGeometry(d.length ?? 40, 4, d.width ?? 60), pm); deck.position.set(x, deckY, 0); deck.castShadow = true;
    g.add(deck);
    for (const s of [-1, 1]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry((d.length ?? 40) * 0.8, 8, 4), pm); leg.position.set(x, deckY - 5, s * ((d.width ?? 60) / 2 - 2)); g.add(leg);
    }
    for (const s of [-1, 1]) {
      const cable = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1, 0.8), mat(P.accent));
      cable.position.set(x, deckY, s * 12); g.add(cable); cables.push(cable);
    }
  }
  return {
    group: g,
    apply(pr) {   // cable: hanging length in metres below the deck (follows the element while it is lowered)
      const len = Math.max(0.01, pr.cable ?? 8);
      for (const c of cables) { c.scale.y = len; c.position.y = deckY - len / 2; }
    },
  };
}

// ---------- general structures (Woche 1, 01.11.2026): towers, bridges, dams, ridges with bores, pendulum, flap gates, paths ----------
const col = (k, fb) => P[k] || k || fb || P.model;
function withEdges(mesh, color, opacity = 0.5) {
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry, 30), edgeMat(color || P.edge, opacity));
  e.position.copy(mesh.position); e.rotation.copy(mesh.rotation); e.scale.copy(mesh.scale);
  return e;
}
function tube(a, b, r, m) {   // straight member from a to b (Vector3), radius r
  const len = a.distanceTo(b), mesh = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 8), m);
  mesh.position.copy(a).add(b).multiplyScalar(0.5);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
  mesh.castShadow = true;
  return mesh;
}

function buildPrism(d) {
  // a tower of `levels` slabs (floor lines), cross-section box|cyl|tri|oct, scale profile [[t, s], ...] over the height,
  // twist in degrees bottom->top. props: reveal (levels shown), lean (deg, tilts about the base), fade (opacity)
  const n = d.levels || 40, H = d.height, w = d.width, dp = d.depth ?? d.width, gap = d.gap ?? 0.12;
  const prof = d.profile || [[0, 1], [1, 1]];
  const sAt = (t) => { for (let i = 1; i < prof.length; i++) if (t <= prof[i][0]) { const [t0, a] = prof[i - 1], [t1, b] = prof[i]; return a + (b - a) * (t - t0) / Math.max(1e-6, t1 - t0); } return prof[prof.length - 1][1]; };
  const segs = { box: 4, tri: 3, oct: 8, cyl: 32 }[d.shape || "box"] || 4;
  const m = mat(col(d.color, P.model), { roughness: 0.75, transparent: true });
  const em = edgeMat(P.edge, 0.45);
  const g = new THREE.Group(), lean = new THREE.Group(); g.add(lean);
  const slabs = [], h = H / n;
  for (let i = 0; i < n; i++) {
    const t0 = i / n, t1 = (i + 1) / n, s0 = sAt(t0), s1 = sAt(t1);
    let geo;
    if (segs === 4) { geo = new THREE.BoxGeometry(w * (s0 + s1) / 2, h * (1 - gap), dp * (s0 + s1) / 2); }
    else { geo = new THREE.CylinderGeometry(w / 2 * s1, w / 2 * s0, h * (1 - gap), segs); }
    const mesh = new THREE.Mesh(geo, m); mesh.castShadow = true; mesh.receiveShadow = true;
    mesh.position.y = h * (i + 0.5); mesh.rotation.y = THREE.MathUtils.degToRad((d.twist || 0) * t0 + (d.rot0 || 0));
    lean.add(mesh); slabs.push(mesh);
    if (n <= 80) { const e = withEdges(mesh, P.edge, 0.4); e.material = em; lean.add(e); slabs.push(e); }
  }
  if (d.spire) {   // a thin mast on top: [height, width]
    const sp = new THREE.Mesh(new THREE.CylinderGeometry(d.spire[1] * 0.2, d.spire[1] / 2, d.spire[0], 8), m);
    sp.position.y = H + d.spire[0] / 2; sp.castShadow = true; lean.add(sp); slabs.push(sp);
  }
  return {
    group: g,
    apply(pr) {
      const rev = pr.reveal ?? 1e9, per = n <= 80 ? 2 : 1;
      slabs.forEach((s, i) => { s.visible = Math.floor(i / per) < rev; });
      lean.rotation.z = THREE.MathUtils.degToRad(pr.lean ?? 0);
      m.opacity = pr.fade ?? 1; m.depthWrite = (pr.fade ?? 1) > 0.95;
    },
  };
}

function buildBridge(d) {
  // deck along x from x0 to x1 at deck_y; piers down to ground_y; type suspension | cantilever | beam
  // suspension: towers at d.towers (x), height tower_h above the deck, main cables (sag to the deck), hangers
  // cantilever: diamond trusses around d.towers with arm length d.arm and height tower_h; props: reveal (0..1 deck)
  const g = new THREE.Group();
  const m = mat(col(d.color, P.model), { roughness: 0.7 }), cm = mat(col(d.cable_color, P.accent), { roughness: 0.5 });
  const x0 = d.x0, x1 = d.x1, y = d.deck_y, W = d.deck_w, T = d.deck_t ?? 4, gy = d.ground_y ?? 0;
  const deck = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, T, W), m); deck.position.set((x0 + x1) / 2, y, 0); deck.castShadow = deck.receiveShadow = true;
  g.add(deck, withEdges(deck));
  for (const px of d.piers || []) {
    const ph = y - gy; if (ph <= 0) continue;
    const p = new THREE.Mesh(new THREE.BoxGeometry(d.pier_w ?? 8, ph, W * 0.7), m); p.position.set(px, gy + ph / 2, 0); p.castShadow = true; g.add(p);
  }
  const th = d.tower_h ?? 0, tw = d.tower_w ?? 12;
  if (d.type === "suspension") {
    for (const tx of d.towers) for (const s of [-1, 1]) {
      const leg = new THREE.Mesh(new THREE.BoxGeometry(tw, th + (y - gy), tw * 0.8), m);
      leg.position.set(tx, gy + (th + y - gy) / 2, s * W * 0.45); leg.castShadow = true; g.add(leg);
    }
    for (const tx of d.towers) { const beam = new THREE.Mesh(new THREE.BoxGeometry(tw, tw * 0.6, W * 0.9), m); beam.position.set(tx, y + th * 0.92, 0); g.add(beam); }
    const [ta, tb] = [Math.min(...d.towers), Math.max(...d.towers)], top = y + th, sag = y + (d.sag_min ?? 3);
    for (const s of [-1, 1]) {
      const pts = [];
      pts.push(new THREE.Vector3(x0, y + 2, s * W * 0.45));
      for (let i = 0; i <= 40; i++) { const x = ta + (tb - ta) * i / 40, u = (x - (ta + tb) / 2) / ((tb - ta) / 2); pts.push(new THREE.Vector3(x, sag + (top - sag) * u * u, s * W * 0.45)); }
      pts.push(new THREE.Vector3(x1, y + 2, s * W * 0.45));
      const curve = new THREE.CatmullRomCurve3(pts);
      const cable = new THREE.Mesh(new THREE.TubeGeometry(curve, 160, d.cable_r ?? 1.6, 6, false), cm); cable.castShadow = true; g.add(cable);
      const hp = [];
      for (let i = 1; i < 40; i++) { const x = ta + (tb - ta) * i / 40, u = (x - (ta + tb) / 2) / ((tb - ta) / 2); hp.push(x, y, s * W * 0.45, x, sag + (top - sag) * u * u, s * W * 0.45); }
      const hg = new THREE.BufferGeometry(); hg.setAttribute("position", new THREE.Float32BufferAttribute(hp, 3));
      g.add(new THREE.LineSegments(hg, edgeMat(P.accent, 0.6)));
    }
  }
  if (d.type === "cantilever") {
    const r = d.member_r ?? 2.2, arm = d.arm;
    for (const tx of d.towers) for (const s of [-1, 1]) {
      const z = s * W * 0.5, zt = s * W * 0.25;
      const base = new THREE.Vector3(tx, y - (d.below ?? th * 0.25), z), topP = new THREE.Vector3(tx, y + th, zt);
      const L = new THREE.Vector3(tx - arm, y, z), R = new THREE.Vector3(tx + arm, y, z);
      for (const [a, b] of [[base, topP], [topP, L], [topP, R], [base, L], [base, R]]) g.add(tube(a, b, r, cm));
      for (const f of [0.33, 0.66]) {   // secondary diagonals
        for (const e of [L, R]) { const a = topP.clone().lerp(e, f), b = base.clone().lerp(e, f); g.add(tube(a, b, r * 0.5, cm)); }
      }
    }
  }
  return { group: g, apply() {} };
}

function buildViaduct(d) {
  // a very long viaduct: deck strip from 0 to length along x, instanced piers every `spacing` m; props: reveal (0..1 of the length)
  const g = new THREE.Group(), m = mat(col(d.color, P.model), { roughness: 0.75 });
  const deck = new THREE.Mesh(new THREE.BoxGeometry(1, d.deck_t ?? 3, d.deck_w ?? 13), m); deck.castShadow = deck.receiveShadow = true;
  g.add(deck);
  const n = Math.min(6000, Math.floor(d.length / d.spacing)), ph = d.deck_y;
  const piers = new THREE.InstancedMesh(new THREE.BoxGeometry(3, ph, (d.deck_w ?? 13) * 0.6), m, n); piers.frustumCulled = false; piers.castShadow = true;
  const m4 = new THREE.Matrix4();
  for (let i = 0; i < n; i++) { m4.makeTranslation(i * d.spacing, ph / 2, 0); piers.setMatrixAt(i, m4); }
  g.add(piers);
  return {
    group: g,
    apply(pr) {
      const k = Math.max(0.0001, Math.min(1, pr.reveal ?? 1)), L = d.length * k;
      deck.scale.x = L; deck.position.set(L / 2, ph + (d.deck_t ?? 3) / 2, 0);
      piers.count = Math.max(1, Math.floor(n * k)); piers.instanceMatrix.needsUpdate = true;
    },
  };
}

function buildDam(d) {
  // arch dam (radius R, opening angle deg) or straight dam (type straight, length); height H, thickness t (crest) / tb (base);
  // water behind it as a box at prop level (0..1 of H)
  const g = new THREE.Group(), m = mat(col(d.color, P.model), { roughness: 0.85 });
  const H = d.height, tb = d.tb ?? d.height * 0.3, t = d.t ?? 10;
  let wall;
  if (d.type === "straight") {
    const sh = new THREE.Shape(); sh.moveTo(-tb / 2, 0); sh.lineTo(tb / 2, 0); sh.lineTo(-tb / 2 + t, H); sh.lineTo(-tb / 2, H); sh.lineTo(-tb / 2, 0);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: d.length, bevelEnabled: false }); geo.translate(0, 0, -d.length / 2); geo.rotateY(Math.PI / 2);
    wall = new THREE.Mesh(geo, m);
  } else {
    const a = THREE.MathUtils.degToRad(d.angle ?? 100), R = d.radius, sh = new THREE.Shape();
    sh.absarc(0, 0, R + t, -a / 2, a / 2, false); sh.absarc(0, 0, R, a / 2, -a / 2, true);
    const geo = new THREE.ExtrudeGeometry(sh, { depth: H, bevelEnabled: false, curveSegments: 48 }); geo.rotateX(-Math.PI / 2); geo.translate(-R, 0, 0);
    wall = new THREE.Mesh(geo, m);
  }
  wall.castShadow = wall.receiveShadow = true; g.add(wall, withEdges(wall, P.edge, 0.35));
  const wm = mat(P.water, { transparent: true, opacity: 0.75, roughness: 0.4 });
  const water = new THREE.Mesh(new THREE.BoxGeometry(d.water_l ?? 600, 1, d.water_w ?? 800), wm);
  g.add(water);
  return {
    group: g,
    apply(pr) {
      const lv = Math.max(0.01, pr.level ?? 0.9) * H; water.visible = (pr.water ?? 1) > 0.5;
      water.scale.y = lv; water.position.set(d.water_x ?? -(d.water_l ?? 600) / 2 - 5, lv / 2, 0);
    },
  };
}

function buildRidge(d) {
  // a mountain ridge along x (triangular cross-section, base width W, height H, length L), translucent so bores inside
  // show; d.bores: [{z, y, r, color}] tubes through the whole length; props: fade, bore (0..1 driven length), pulse (0..1)
  const g = new THREE.Group(), L = d.length, W = d.width, H = d.height;
  const sh = new THREE.Shape(); sh.moveTo(-W / 2, 0); sh.lineTo(-W * 0.08, H * 0.96); sh.lineTo(W * 0.06, H); sh.lineTo(W / 2, 0); sh.lineTo(-W / 2, 0);
  const geo = new THREE.ExtrudeGeometry(sh, { depth: L, bevelEnabled: false }); geo.rotateY(Math.PI / 2); geo.translate(-L / 2, 0, 0);
  const rm = mat(col(d.color, P.land || P.ground), { roughness: 1, transparent: true, side: THREE.DoubleSide });
  const rock = new THREE.Mesh(geo, rm); rock.receiveShadow = true; g.add(rock, withEdges(rock, P.grid, 0.4));
  const bores = [];
  for (const b of d.bores || []) {
    const bm = mat(col(b.color, P.accent), { roughness: 0.5 });
    const tb = new THREE.Mesh(new THREE.CylinderGeometry(b.r, b.r, 1, 16), bm); tb.rotation.z = Math.PI / 2; tb.castShadow = true;
    g.add(tb); bores.push({ mesh: tb, def: b });
  }
  const pulse = new THREE.Mesh(new THREE.BoxGeometry(L * 0.04, (d.bores?.[0]?.r ?? 5) * 2.6, (d.bores?.[0]?.r ?? 5) * 2.6), mat("#ffffff", { emissive: new THREE.Color(P.accent), emissiveIntensity: 0.9 }));
  g.add(pulse);
  return {
    group: g,
    apply(pr) {
      rm.opacity = pr.fade ?? 0.55; rm.depthWrite = (pr.fade ?? 0.55) > 0.95;
      const k = Math.max(0.0005, Math.min(1, pr.bore ?? 1));
      for (const { mesh, def } of bores) { mesh.scale.y = L * k; mesh.position.set(-L / 2 + (L * k) / 2, def.y, def.z); }
      const p = pr.pulse ?? -1; pulse.visible = p >= 0 && p <= 1;
      pulse.position.set(-L / 2 + L * Math.max(0, p), d.bores?.[0]?.y ?? H * 0.2, d.bores?.[0]?.z ?? 0);
    },
  };
}

function buildPendulum(d) {
  // tuned mass damper: sphere of radius r hanging on `cables` from a frame at height `hang` above it; prop swing (deg)
  const g = new THREE.Group(), pivot = new THREE.Group(); pivot.position.y = d.hang; g.add(pivot);
  const sm = mat(col(d.color, P.accent), { roughness: 0.35, metalness: 0.3 });
  const ball = new THREE.Mesh(new THREE.SphereGeometry(d.r, 48, 32), sm); ball.position.y = -d.hang; ball.castShadow = true; pivot.add(ball);
  const lp = [];
  for (let i = 0; i < (d.cables ?? 8); i++) { const a = i / (d.cables ?? 8) * Math.PI * 2, x = Math.cos(a) * d.r * 0.7, z = Math.sin(a) * d.r * 0.7; lp.push(x, 0, z, x, -d.hang + d.r * 0.6, z); }
  const lg = new THREE.BufferGeometry(); lg.setAttribute("position", new THREE.Float32BufferAttribute(lp, 3));
  pivot.add(new THREE.LineSegments(lg, edgeMat(P.text || "#E9EDF0", 0.8)));
  const frame = new THREE.Mesh(new THREE.BoxGeometry(d.r * 3, d.r * 0.25, d.r * 3), mat(P.model)); frame.position.y = d.hang; g.add(frame);
  return { group: g, apply(pr) { pivot.rotation.z = THREE.MathUtils.degToRad(pr.swing ?? 0); } };
}

function buildGates(d) {
  // flap gates hinged at the seabed (MOSE type): n gates of width w along x, length l along z, thickness t; prop raise 0..1
  const g = new THREE.Group(), gm = mat(col(d.color, P.accent), { roughness: 0.6 }), hinges = [];
  for (let i = 0; i < d.count; i++) {
    const h = new THREE.Group(); h.position.set((i - (d.count - 1) / 2) * (d.w + (d.gap ?? 0.6)), 0, -d.l / 2);
    const b = new THREE.Mesh(new THREE.BoxGeometry(d.w, d.t, d.l), gm); b.position.set(0, d.t / 2, d.l / 2); b.castShadow = true;
    h.add(b, withEdges(b, P.edge, 0.5)); g.add(h); hinges.push(h);
  }
  const housing = new THREE.Mesh(new THREE.BoxGeometry(d.count * (d.w + (d.gap ?? 0.6)) + 4, 2, d.l + 8), mat(P.model_inner || P.model));
  housing.position.y = -1; g.add(housing);
  return { group: g, apply(pr) { const a = THREE.MathUtils.degToRad(d.angle ?? 45) * (pr.raise ?? 0); hinges.forEach((h, i) => { const k = Math.max(0, Math.min(1, (pr.raise ?? 0) * d.count * 0.25 - i * 0.18 + 1)); h.rotation.x = -a * Math.min(1, k); }); } };
}

function buildPath(d) {
  // a band along a polyline [[x, z] or [x, y, z], ...]: wall, road or canal; width, height; props: reveal (0..1 of the segments)
  const g = new THREE.Group(), m = mat(col(d.color, P.model), { roughness: 0.8 }), segs = [];
  const pts = d.points.map((p) => p.length === 2 ? new THREE.Vector3(p[0], d.y ?? 0, p[1]) : new THREE.Vector3(p[0], p[1], p[2]));
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1], len = a.distanceTo(b);
    const s = new THREE.Mesh(new THREE.BoxGeometry(len + d.width * 0.5, d.height, d.width), m);
    s.position.copy(a).add(b).multiplyScalar(0.5); s.position.y += d.height / 2;
    s.lookAt(b.x, s.position.y + (b.y - a.y), b.z); s.rotateY(Math.PI / 2);
    s.castShadow = s.receiveShadow = true; g.add(s); segs.push(s);
  }
  return { group: g, apply(pr) { const k = (pr.reveal ?? 1) * segs.length; segs.forEach((s, i) => { s.visible = i < k; }); } };
}

function buildPiles(d) {
  // a grid of cylinders (piles, springs): nx x nz, spacing, radius r, length len, hanging down from y=0 (or up with d.up)
  const m = mat(col(d.color, P.model_inner), { roughness: 0.7 }), n = d.nx * d.nz;
  const mesh = new THREE.InstancedMesh(new THREE.CylinderGeometry(d.r, d.r, d.len, 12), m, n); mesh.frustumCulled = false; mesh.castShadow = true;
  const m4 = new THREE.Matrix4();
  let i = 0;
  for (let a = 0; a < d.nx; a++) for (let b = 0; b < d.nz; b++) {
    m4.makeTranslation((a - (d.nx - 1) / 2) * d.spacing, (d.up ? 1 : -1) * d.len / 2, (b - (d.nz - 1) / 2) * d.spacing); mesh.setMatrixAt(i++, m4);
  }
  const g = new THREE.Group(); g.add(mesh);
  return { group: g, apply(pr) { mesh.count = Math.max(0, Math.min(n, Math.round((pr.reveal ?? 1) * n))); } };
}

// ---------- Format "Bauaufgabe" (02.11.2026): an assembled tuned mass damper and wind load arrows ----------
function setTube(mesh, a, b) {   // re-aim a unit cylinder (height 1) from a to b
  const len = a.distanceTo(b);
  mesh.position.copy(a).add(b).multiplyScalar(0.5);
  mesh.scale.set(1, Math.max(0.001, len), 1);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
}
function buildTmd(d) {
  // tuned mass damper as a bill of materials: a sphere of radius r built from `plates` horizontal discs of thickness t
  // (stack centred on the sphere), hanging `hang` metres below a frame on `cables` straight cables (arranged on a circle,
  // schematic), a bumper ring under the ball and `dampers` horizontal dampers from the ring to fixed anchors.
  // props: plates (discs shown, bottom up), cables (count shown), hl (first n cables in the accent), dampers (count),
  //        ring (0/1), swing (horizontal displacement of the ball in metres along `dir` degrees), frame (0/1)
  const g = new THREE.Group(), R = d.r, H = d.hang, n = d.plates ?? 41, t = d.t ?? 0.125, nc = d.cables ?? 92;
  const pm = mat(col(d.color, P.accent), { roughness: 0.45, metalness: 0.25 });
  const pivot = new THREE.Group(); pivot.position.y = H; g.add(pivot);
  const ball = new THREE.Group(); ball.position.y = -H; pivot.add(ball);
  const discs = [], stack = n * t;
  for (let i = 0; i < n; i++) {
    const y = -stack / 2 + (i + 0.5) * t, rr = Math.sqrt(Math.max(0.04, R * R - y * y));
    const m = new THREE.Mesh(new THREE.CylinderGeometry(rr, rr, t * 0.9, 40), pm); m.position.y = y; m.castShadow = true;
    const e = new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry, 30), edgeMat(P.edge, 0.55)); e.position.y = y;
    ball.add(m, e); discs.push([m, e]);
  }
  // cables: from the frame (y = 0 in pivot space) to the upper ball (y = -H + 0.35 R); first `hl` in the accent
  const cg = new THREE.CylinderGeometry(0.045, 0.045, 1, 5), cm = mat(P.cable || P.text || "#E9EDF0", { roughness: 0.5 }), ch = mat(P.accent, { roughness: 0.5 });
  const cables = [];
  for (let i = 0; i < nc; i++) {
    const ring = i % 2, a = (i / nc) * Math.PI * 2 + ring * 0.03, rr = R * (0.55 + 0.17 * ring);
    const top = new THREE.Vector3(Math.cos(a) * rr, 0, Math.sin(a) * rr), bot = new THREE.Vector3(Math.cos(a) * rr, -H + R * 0.35, Math.sin(a) * rr);
    const c = new THREE.Mesh(cg, cm); setTube(c, top, bot); pivot.add(c); cables.push(c);
  }
  const frame = new THREE.Mesh(new THREE.BoxGeometry(R * 3.2, 1.2, R * 3.2), mat(P.model_inner || P.model)); frame.position.y = H + 0.6; frame.castShadow = true;
  const frameE = withEdges(frame, P.edge, 0.6);
  g.add(frame, frameE);
  // bumper ring under the ball (moves with it) and fixed damper anchors on a circle around it
  const ringY = -R - 0.6, ringR = R * 0.45;
  const ringM = new THREE.Mesh(new THREE.TorusGeometry(ringR, 0.22, 10, 48), mat(P.model, { roughness: 0.6 })); ringM.rotation.x = Math.PI / 2; ringM.position.y = ringY; ball.add(ringM);
  const nd = d.dampers ?? 8, anchorR = ringR + (d.reach ?? 4.2), dg = new THREE.CylinderGeometry(0.28, 0.28, 1, 10), dm = mat(P.model_inner || P.model, { roughness: 0.6 });
  const dampers = [], posts = [];
  for (let i = 0; i < nd; i++) {
    const a = (i / nd) * Math.PI * 2 + Math.PI / nd;
    const m = new THREE.Mesh(dg, dm); m.castShadow = true; g.add(m); dampers.push([m, a]);
    const post = new THREE.Mesh(new THREE.BoxGeometry(0.8, 2.4, 0.8), mat(P.model_inner || P.model)); post.position.set(Math.cos(a) * anchorR, ringY, Math.sin(a) * anchorR); g.add(post); posts.push(post);
  }
  const floor = new THREE.Mesh(new THREE.CylinderGeometry(anchorR + 1.5, anchorR + 1.5, 0.4, 48), mat(P.ground || P.model_inner, { roughness: 0.9 })); floor.position.y = ringY - 1.4; floor.receiveShadow = true; g.add(floor);
  const tmp1 = new THREE.Vector3();
  return {
    group: g,
    apply(pr) {
      const sw = pr.swing ?? 0, dir = THREE.MathUtils.degToRad(pr.dir ?? 0);
      const ang = Math.asin(Math.max(-0.99, Math.min(0.99, sw / H)));
      pivot.rotation.set(Math.sin(dir) * ang, 0, -Math.cos(dir) * ang);   // the ball moves +sw along dir (x/z plane)
      const np = Math.round(pr.plates ?? n);
      discs.forEach(([m, e], i) => { m.visible = e.visible = i < np; });
      const ncs = Math.round(pr.cables ?? nc), nh = Math.round(pr.hl ?? 0);
      cables.forEach((c, i) => { c.visible = i < ncs; c.material = i < nh ? ch : cm; });
      ringM.visible = (pr.ring ?? 1) > 0.5;
      frame.visible = frameE.visible = (pr.frame ?? 1) > 0.5;
      floor.visible = (pr.floor ?? 1) > 0.5;
      const ndd = Math.round(pr.dampers ?? nd);
      g.updateMatrixWorld(true);
      const rc = ringM.getWorldPosition(tmp1); g.worldToLocal(rc);
      dampers.forEach(([m, a], i) => {
        m.visible = posts[i].visible = i < ndd;
        const outer = new THREE.Vector3(Math.cos(a) * anchorR, ringY, Math.sin(a) * anchorR);
        const inner = new THREE.Vector3(rc.x + Math.cos(a) * ringR, rc.y, rc.z + Math.sin(a) * ringR);
        setTube(m, inner, outer);
      });
    },
  };
}
function buildWind(d) {
  // wind load: `count` arrows stacked from y0 to y1, pointing +x, starting at x = -dist; arrows drift along x
  // (pure function of time). props: wind (0..1 strength: length and opacity)
  const g = new THREE.Group(), m = new THREE.MeshBasicMaterial({ color: col(d.color, P.water_line || "#9CC3E6"), transparent: true });
  const arrows = [], n = d.count ?? 7, L = d.len ?? 60, w = d.w ?? 1.6;
  for (let i = 0; i < n; i++) {
    const a = new THREE.Group();
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(w, w, 1, 8), m); shaft.rotation.z = -Math.PI / 2;
    const head = new THREE.Mesh(new THREE.ConeGeometry(w * 3, w * 6, 12), m); head.rotation.z = -Math.PI / 2;
    a.add(shaft, head); a.position.set(-(d.dist ?? 120), lerp(d.y0 ?? 0, d.y1 ?? 300, n > 1 ? i / (n - 1) : 0.5), (i % 2 ? 1 : -1) * (d.spread ?? 20));
    g.add(a); arrows.push({ shaft, head, k: 0.75 + 0.25 * (((i * 7) % 5) / 4), ph: (i * 0.37) % 1 });
  }
  return {
    group: g,
    apply(pr, t) {
      const s = Math.max(0, Math.min(1, pr.wind ?? 1));
      m.opacity = 0.85 * s;
      g.visible = s > 0.02;
      for (const o of arrows) {
        const len = Math.max(0.1, L * o.k * (0.4 + 0.6 * s)), drift = (((t || 0) * 0.35 + o.ph) % 1) * (d.drift ?? 30);
        o.shaft.scale.y = len; o.shaft.position.x = len / 2 + drift; o.head.position.x = len + drift + w * 3;
      }
    },
  };
}

const BUILD = { tmd: buildTmd, wind: buildWind, piles: buildPiles, element: buildElement, water: buildWater, seabed: buildSeabed, ground: buildGround, tower: buildTower, boat: buildBoat, pontoon: buildPontoon,
  chain: buildChain, land: buildLand, box: buildBox, prism: buildPrism, bridge: buildBridge, viaduct: buildViaduct, dam: buildDam,
  ridge: buildRidge, pendulum: buildPendulum, gates: buildGates, path: buildPath };
for (const d of S.objects) {
  const o = BUILD[d.kind](d);
  o.def = d;
  o.group.position.set(...(d.pos || [0, 0, 0]));
  scene.add(o.group);
  objects[d.id] = o;
}
// bounding spheres of the full objects (all parts shown) for the automatic camera
const BOUNDS = {};
for (const [id, o] of Object.entries(objects)) {
  o.apply({ ...(o.def.props || {}), reveal: 1e9, bore: 1, build: 1 }, 0);
  o.group.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(o.group);
  BOUNDS[id] = box;
}
function autoCam(c, k) {
  // frame the union of c.target objects: azimuth/elevation in degrees, fit = share of the frame width the object fills,
  // cy = vertical screen position (px) of its centre. Returns {p, l, dy, fog}
  const box = new THREE.Box3();
  for (const id of c.target) if (BOUNDS[id]) box.union(BOUNDS[id]);
  if (c.box) box.set(new THREE.Vector3(...c.box[0]), new THREE.Vector3(...c.box[1]));
  const ctr = box.getCenter(new THREE.Vector3()), size = box.getSize(new THREE.Vector3());
  if (c.center) ctr.set(...c.center);
  const az = THREE.MathUtils.degToRad(lerp(c.az0 ?? 35, c.az1 ?? c.az0 ?? 35, k)), el = THREE.MathUtils.degToRad(lerp(c.el0 ?? 18, c.el1 ?? c.el0 ?? 18, k));
  const fit = lerp(c.fit0 ?? 0.85, c.fit1 ?? c.fit0 ?? 0.85, k);
  const vf = THREE.MathUtils.degToRad(c.fov ?? S.fov ?? 38), hf = 2 * Math.atan(Math.tan(vf / 2) * 1080 / 1920);
  // apparent width: the box seen from this azimuth (projected horizontal extent), height for tall objects
  const wx = Math.abs(Math.sin(az)) * size.x + Math.abs(Math.cos(az)) * size.z, hy = size.y * Math.cos(el) + (Math.abs(Math.cos(az)) * size.x + Math.abs(Math.sin(az)) * size.z) * Math.sin(el);
  const zone = c.zone ?? 760;   // usable height in px for the object
  const dW = (wx / fit) / 2 / Math.tan(hf / 2), dH = (hy / Math.max(0.1, zone / 1920)) / 2 / Math.tan(vf / 2);
  const dist = Math.max(dW, dH) + Math.max(size.x, size.z) * 0.15 * (c.depth ?? 1);
  const p = [ctr.x + dist * Math.cos(el) * Math.cos(az), ctr.y + dist * Math.sin(el), ctr.z + dist * Math.cos(el) * Math.sin(az)];
  return { p, l: [ctr.x, ctr.y, ctr.z], dy: 960 - (c.cy ?? 760), fog: [dist * 1.2, dist * 8 + 4000] };
}

function easeOut(k) { return 1 - Math.pow(1 - k, 3); }
function easeInOut(k) { return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }
function smooth(k) { return k * k * (3 - 2 * k); }
function lerp(a, b, k) { return a + (b - a) * k; }
function lerp3(a, b, k) { return [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)]; }

function valueAt(v, rel) {
  if (!Array.isArray(v)) return v;
  if (rel <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) {
    if (rel <= v[i][0]) {
      const [t0, a] = v[i - 1], [t1, b] = v[i];
      return lerp(a, b, smooth((rel - t0) / Math.max(1e-6, t1 - t0)));
    }
  }
  return v[v.length - 1][1];
}

const anchorEls = Array.from(document.querySelectorAll("[data-anchor]"));
const railEls = Array.from(document.querySelectorAll("#gbrail > div"));
const tmp = new THREE.Vector3();

function draw(beat, t, rend) {
  const shot = S.shots[beat.id] || {};
  const rel = t - beat.start, dur = Math.max(0.1, beat.end - beat.start);
  // object state: defaults, then the shot's props (constant or keyframes in beat-relative seconds)
  for (const [id, o] of Object.entries(objects)) {
    const pr = { ...(o.def.props || {}) };
    for (const [key, v] of Object.entries(shot.props || {})) {
      const [oid, prop] = key.split(".");
      if (oid === id) pr[prop] = valueAt(v, rel);
    }
    o.group.visible = (pr.visible ?? 1) > 0.5;
    const base = o.def.pos || [0, 0, 0];
    o.group.position.set(base[0] + (pr.x ?? 0), base[1] + (pr.y ?? 0), base[2] + (pr.z ?? 0));
    o.group.rotation.set(THREE.MathUtils.degToRad(pr.rx ?? 0), pr.rot ?? 0, THREE.MathUtils.degToRad(pr.rz ?? 0));
    o.group.scale.set(pr.sx ?? 1, pr.sy ?? 1, pr.sz ?? 1);
    o.apply(pr, t);
  }
  // camera: one continuous move per beat (dive or push), eased; dy shifts the image vertically (px, + = content up)
  const c = shot.cam || S.default_cam;
  const k = easeInOut(Math.min(1, rel / (c.seconds ?? dur)));
  let cp, cl, cdy = c.dy, autoFog = null;
  if (c.target) { const a = autoCam(c, k); cp = a.p; cl = a.l; cdy = a.dy; autoFog = a.fog; }
  else { cp = lerp3(c.p0, c.p1 || c.p0, k); cl = lerp3(c.l0, c.l1 || c.l0, k); }
  // fog per shot (long views along the whole tunnel need a far fog), else from the automatic camera, else the default
  const fog = shot.fog || autoFog || FOG;
  scene.fog.near = fog[0]; scene.fog.far = fog[1];
  camera.fov = c.fov ?? S.fov ?? 38;
  if (cdy) camera.setViewOffset(1080, 1920, 0, cdy, 1080, 1920); else camera.clearViewOffset();
  camera.updateProjectionMatrix();
  camera.position.set(...cp);
  const look = cl;
  camera.lookAt(look[0], look[1], look[2]);
  camera.updateMatrixWorld();
  dome.position.copy(camera.position);
  rend.render(scene, camera);
}

function quadInOut(k) { return k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; }

function render(t) {
  const beat = S.beats.find((b) => t >= b.start && t < b.end) || S.beats[S.beats.length - 1];
  // transition into this beat: the previous shot keeps running underneath, this one opens (iris) or fades in (blende)
  const tr = TR[beat.id];
  const idx = S.beats.indexOf(beat);
  const kt = tr && idx > 0 ? (t - beat.start) / Math.max(0.05, tr.seconds) : 1;
  if (prevRenderer && kt < 1) {
    prevCanvas.style.visibility = "visible";
    draw(S.beats[idx - 1], t, prevRenderer);
    if (tr.type === "iris") {
      canvas.style.opacity = "1";
      canvas.style.clipPath = `circle(${(2300 * easeInOut(Math.max(0, kt))).toFixed(1)}px at ${tr.x}px ${tr.y}px)`;
    } else {
      canvas.style.clipPath = "none";
      canvas.style.opacity = quadInOut(Math.max(0, kt)).toFixed(3);
    }
  } else {
    if (prevCanvas) prevCanvas.style.visibility = "hidden";
    canvas.style.clipPath = "none";
    canvas.style.opacity = "1";
  }
  draw(beat, t, renderer);
  // chapter rail (format Bauaufgabe): the chapter of the current beat is "on", earlier chapters are "done"
  if (railEls.length) {
    const ch = (S.chapters?.beats || {})[beat.id];
    railEls.forEach((el, i) => { el.className = ch === undefined ? "" : i === ch ? "on" : i < ch ? "done" : ""; });
  }
  // labels follow their 3D anchors (projected to the 1080 x 1920 frame, camera of the current beat)
  for (const el of anchorEls) {
    const a = S.anchors[el.dataset.anchor];
    if (!a) continue;
    tmp.set(a[0], a[1], a[2]).project(camera);
    const x = (tmp.x + 1) / 2 * 1080, y = (1 - tmp.y) / 2 * 1920;
    el.style.left = `${x.toFixed(1)}px`;
    el.style.top = `${y.toFixed(1)}px`;
  }
}

window.__gsRender = render;
render(window.__gsPending ?? 0);
window.__gsReady && window.__gsReady();
