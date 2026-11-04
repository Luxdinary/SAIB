// Text-overlap check for rendered direction projects (Stefan, 30.10.2026: "die Texte überschneiden sich").
// Loads storage/direction/<id>-<version>/project/index.html in headless Chrome, seeks the GSAP timeline every
// STEP seconds and reports visible text boxes of different layers that intersect: explainer layer (marker, source,
// head, opening), scene, captions, status bar, outro, and any other element with an id (brand layers such as
// Dewlane's #nhx-stamp). Overlaps between two text elements inside one scene are listed as `warnings` (exit code
// unchanged), because stacked lines of one card are intended. The viewport follows #root data-width/data-height (16:9 too).
// Usage: node scripts/overlap_check.mjs <project_dir> [<project_dir> ...]   (exit 1 when any overlap is found)
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

function findPuppeteer() {                                 // FN_PUPPETEER, else the copy in the npx cache (HyperFrames)
  if (process.env.FN_PUPPETEER) return process.env.FN_PUPPETEER;
  const base = path.join(process.env.LOCALAPPDATA || "", "npm-cache", "_npx");
  for (const d of fs.existsSync(base) ? fs.readdirSync(base) : []) {
    const p = path.join(base, d, "node_modules", "puppeteer-core");
    if (fs.existsSync(p)) return p;
  }
  throw new Error("puppeteer-core not found; set FN_PUPPETEER");
}
const PUPPETEER = findPuppeteer();
const CHROME = process.env.FN_CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const STEP = Number(process.env.FN_OVERLAP_STEP || 0.25);
const require = createRequire(import.meta.url);
const puppeteer = require(PUPPETEER);

function pageCheck(step) {
  const tl = window.__timelines && window.__timelines.main;
  const root = document.getElementById("root");
  const total = Number(root.dataset.duration);
  const layerOf = (el) => {
    if (el.closest(".xlayer, #xtag")) return "explainer";
    if (el.closest(".xhead")) return "head";
    if (el.closest(".scene")) return "scene:" + el.closest(".scene").id;
    if (el.closest("#captions")) return "caption";
    if (el.closest("#status")) return "status";
    if (el.closest("#outro")) return "outro";
    if (el.closest("#art50")) return "art50";
    for (let a = el; a && a !== root; a = a.parentElement) if (a.id) return "brand:" + a.id;   // brand layers
    return null;
  };
  const texts = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    const layer = layerOf(el);
    if (layer) texts.push({ node: n, el, layer });
  }
  const inTime = (el, t) => {
    for (let a = el; a && a !== root; a = a.parentElement) {
      if (a.dataset && a.dataset.start !== undefined && a.classList.contains("clip")) {
        const s = Number(a.dataset.start), d = Number(a.dataset.duration);
        if (t < s || t > s + d) return false;
      }
    }
    return true;
  };
  const opacity = (el) => {
    let o = 1;
    for (let a = el; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.display === "none" || cs.visibility === "hidden") return 0;
      o *= Number(cs.opacity);
    }
    return o;
  };
  const cut = (a, c) => {                                          // intersection of two rects, null when empty
    const left = Math.max(a.left, c.left), right = Math.min(a.right, c.right);
    const top = Math.max(a.top, c.top), bottom = Math.min(a.bottom, c.bottom);
    return right > left && bottom > top ? { left, right, top, bottom, width: right - left, height: bottom - top } : null;
  };
  const clipOf = (el) => {                                         // visible area left by ancestors with overflow != visible
    let c = { left: -1e9, top: -1e9, right: 1e9, bottom: 1e9 };
    for (let a = el.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (/(hidden|clip|scroll|auto)/.test(cs.overflowX + cs.overflowY)) c = cut(c, a.getBoundingClientRect()) || { left: 0, top: 0, right: 0, bottom: 0 };
    }
    return c;
  };
  const found = new Map(), warn = new Map(), small = new Map();
  const MIN_PX = 24, scale = 1080 / Math.min(Number(root.dataset.width || 1080), Number(root.dataset.height || 1920));
  const note = (map, A, B, t) => {
    const key = A.layer + " | " + B.layer + " | " + A.node.textContent.trim().slice(0, 40) + " | " + B.node.textContent.trim().slice(0, 40);
    const f = map.get(key);
    if (f) f.until = t; else map.set(key, { from: t, until: t, y: Math.round(Math.max(A.b.top, B.b.top)) });
  };
  for (let t = 0; t <= total; t += step) {
    tl.seek(t, false);
    const vis = [];
    for (const x of texts) {
      if (!inTime(x.el, t) || opacity(x.el) < 0.35) continue;
      const clip = clipOf(x.el);
      const r = document.createRange(); r.selectNodeContents(x.node);
      for (const raw of r.getClientRects()) {
        const b = cut(raw, clip);                                   // only the part not cut off by overflow:hidden
        if (b && b.width > 2 && b.height > 2) vis.push({ ...x, b });
      }
      const ctm = x.el instanceof SVGElement && x.el.getScreenCTM ? x.el.getScreenCTM() : null;   // SVG text scales with viewBox
      const px = parseFloat(getComputedStyle(x.el).fontSize) * (ctm ? Math.hypot(ctm.a, ctm.b) : 1) * scale;   // R7: ~24 px at 1080 width
      if (px < MIN_PX && x.layer !== "caption") {
        const k = x.layer + " | " + x.node.textContent.trim().slice(0, 40);
        if (!small.has(k)) small.set(k, { text: k, px: Math.round(px), at: +t.toFixed(2) });
      }
    }
    for (let i = 0; i < vis.length; i++) for (let j = i + 1; j < vis.length; j++) {
      const A = vis[i], B = vis[j];
      if (A.layer.startsWith("scene:") && B.layer.startsWith("scene:") && A.layer !== B.layer) continue;   // transition overlap of two scenes is intended
      const w = Math.min(A.b.right, B.b.right) - Math.max(A.b.left, B.b.left);
      const h = Math.min(A.b.bottom, B.b.bottom) - Math.max(A.b.top, B.b.top);
      if (!(w > 4 && h > 4)) continue;
      if (A.layer !== B.layer) note(found, A, B, t);
      else if (A.el !== B.el && !A.el.contains(B.el) && !B.el.contains(A.el)) {         // two texts inside one layer:
        const ink = (b) => ({ top: b.top + 0.22 * b.height, bottom: b.bottom - 0.22 * b.height });  // line box -> approx. glyph height
        const ia = ink(A.b), ib = ink(B.b);
        const hi = Math.min(ia.bottom, ib.bottom) - Math.max(ia.top, ib.top);
        if (hi > 4 && w * hi >= 0.3 * Math.min(A.b.width * (ia.bottom - ia.top), B.b.width * (ib.bottom - ib.top))) note(warn, A, B, t);
      }
    }
  }
  const list = (m) => [...m.entries()].map(([k, v]) => ({ pair: k, from: +v.from.toFixed(2), until: +v.until.toFixed(2), y: v.y }));
  return { overlaps: list(found), warnings: list(warn).filter(x => x.until - x.from >= 2 * step),   // skip one-sample cross-fades
           small_text: [...small.values()] };                                                       // below MIN_PX, exit code unchanged
}

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--allow-file-access-from-files"] });
let bad = 0;
for (const dir of process.argv.slice(2)) {
  const idx = path.join(dir, "index.html");
  if (!fs.existsSync(idx)) { console.log(`${dir}: no index.html`); bad++; continue; }
  const page = await browser.newPage();
  const html = fs.readFileSync(idx, "utf-8");
  const size = (k, d) => Number((html.match(new RegExp(`id="root"[^>]*data-${k}="(\\d+)"`)) || [])[1] || d);
  await page.setViewport({ width: size("width", 1080), height: size("height", 1920) });
  await page.goto(pathToFileURL(idx).href, { waitUntil: "load" });
  for (let k = 0; k < 100 && !(await page.evaluate(() => !!(window.__timelines && window.__timelines.main))); k++) await new Promise(r => setTimeout(r, 200));
  await page.evaluate(() => document.fonts.ready);
  const res = await page.evaluate(pageCheck, STEP);
  console.log(JSON.stringify({ project: dir, ...res }));
  if (res.overlaps.length) bad++;
  await page.close();
}
await browser.close();
process.exit(bad ? 1 : 0);
