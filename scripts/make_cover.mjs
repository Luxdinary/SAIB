// Cover image for a rendered direction project (Prüfrunde 03.11.2026, R2: covers were video frames with half a
// caption, the AI label and the progress bar). Loads the project in headless Chrome, seeks the GSAP timeline (and every
// <video> clip) to <seconds>, hides captions, progress bar and AI label, puts the hook title large into the upper middle
// (inside the 1:1 and 3:4 grid crops) and writes a JPEG.
// Usage: node scripts/make_cover.mjs <project_dir> <seconds> <out.jpg> "<title>"
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

function findPuppeteer() {                                 // same lookup as overlap_check.mjs
  if (process.env.FN_PUPPETEER) return process.env.FN_PUPPETEER;
  const base = path.join(process.env.LOCALAPPDATA || "", "npm-cache", "_npx");
  for (const d of fs.existsSync(base) ? fs.readdirSync(base) : []) {
    const p = path.join(base, d, "node_modules", "puppeteer-core");
    if (fs.existsSync(p)) return p;
  }
  throw new Error("puppeteer-core not found; set FN_PUPPETEER");
}
const require = createRequire(import.meta.url);
const puppeteer = require(findPuppeteer());
const CHROME = process.env.FN_CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const [dir, secArg, out, title = ""] = process.argv.slice(2);
const idx = path.join(dir, "index.html");
const html = fs.readFileSync(idx, "utf-8");
const size = (k, d) => Number((html.match(new RegExp(`id="root"[^>]*data-${k}="(\\d+)"`)) || [])[1] || d);
const W = size("width", 1080), H = size("height", 1920);

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--allow-file-access-from-files", "--autoplay-policy=no-user-gesture-required"] });
const page = await browser.newPage();
await page.setViewport({ width: W, height: H });
await page.goto(pathToFileURL(idx).href, { waitUntil: "load" });
for (let k = 0; k < 100 && !(await page.evaluate(() => !!(window.__timelines && window.__timelines.main))); k++) await new Promise(r => setTimeout(r, 200));
await page.evaluate(() => document.fonts.ready);
await page.evaluate(async (t, title, W, H) => {
  window.__timelines.main.seek(t, false);
  const waits = [];
  for (const v of document.querySelectorAll("video")) {            // background and hero clips
    const clip = v.closest("[data-start]");
    const local = Math.max(0, t - Number(clip ? clip.dataset.start : 0));
    v.pause();
    waits.push(new Promise(res => { v.addEventListener("seeked", res, { once: true }); setTimeout(res, 3000); }));
    v.currentTime = v.duration ? local % v.duration : local;
  }
  await Promise.all(waits);
  for (const sel of ["#captions", "#progress", "#ailabel"]) { const e = document.querySelector(sel); if (e) e.style.visibility = "hidden"; }
  // HyperFrames shows a clip only inside [data-start, data-start + data-duration]; a bare timeline seek does not, so
  // later scenes would leak into the cover (Gritwerk 02.11.2026: empty page-turn sheet on top)
  for (const c of document.querySelectorAll(".clip[data-start]")) {
    const s = Number(c.dataset.start), d = Number(c.dataset.duration);
    if (t < s || t > s + d) c.style.visibility = "hidden";
  }
  if (title) {
    const box = document.createElement("div");
    const portrait = H > W;
    box.textContent = title;
    box.style.cssText = `position:absolute;left:${Math.round(W * 0.08)}px;right:${Math.round(W * 0.08)}px;` +
      `top:${portrait ? Math.round(H * 0.58) : Math.round(H * 0.62)}px;z-index:99;text-align:center;` +
      `font-weight:800;font-size:${portrait ? 84 : 72}px;line-height:1.08;color:var(--text,#fff);` +
      `background:var(--bg,#000);padding:28px 32px;border-radius:24px;` +
      `border:3px solid var(--accent,#4f8cff);`;
    document.getElementById("root").appendChild(box);
  }
}, Number(secArg), title, W, H);
await new Promise(r => setTimeout(r, 300));
await page.screenshot({ path: out, type: "jpeg", quality: 90 });
await browser.close();
console.log(out);
