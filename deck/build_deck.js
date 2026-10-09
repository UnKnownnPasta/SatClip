// Builds deck/satclip.pptx (milestone M7). Run from the repo root: node deck/build_deck.js
// Needs pptxgenjs, react, react-dom, react-icons and sharp (npm). Screenshots come from
// deck/assets/ (crops of docs/screenshots made by deck/prepare_assets.py).
// Every number on the slides comes from docs/QUALITY.md, docs/demo/TRANSCRIPT.md,
// training reports or the archive index; the source is named in the speaker notes.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");

const SKILL = process.env.PPTX_SKILL || "";
const ROOT = path.resolve(__dirname, "..");
const ASSETS = path.join(__dirname, "assets");
const OUT = path.join(__dirname, "satclip.pptx");

// Claymorphism palette: cool pastel base, one dominant water blue, mint for published answers,
// peach for abstentions, lilac for the language layer. Text is always the dark ink (contrast > 9:1 on every pastel).
const THEME = {
  name: "SatClip Clay",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2940", lt1: "FFFFFF", dk2: "2B3467", lt2: "EDF0F8",
    accent1: "2F6FB3", accent2: "BFD8F5", accent3: "C3EBD2", accent4: "FFDCC4",
    accent5: "DDD4F7", accent6: "1E6B45", hlink: "2F6FB3", folHlink: "5B4B9A",
  },
};
const HEX = THEME.colors;
const SHADOW_DARK = "A3ACCB"; // outer clay shadow on the light base
const SHADOW_DEEP = "141A33"; // outer clay shadow on the dark base

const W = 13.333, H = 7.5;

async function icon(Comp, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

// pptxgenjs closes an inner shadow with </a:outerShdw>; repair the tag so the XML is valid.
async function fixInnerShadows(file) {
  const JSZip = require(require.resolve("jszip", { paths: [path.dirname(require.resolve("pptxgenjs"))] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async("string");
    const fixed = xml.replace(/(<a:innerShdw\b[^>]*>(?:(?!<\/a:innerShdw>|<a:outerShdw).)*?)<\/a:outerShdw>/gs, "$1</a:innerShdw>");
    zip.file(name, fixed);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "SatClip: evidence, not guesses";
  pres.author = "Team Stardust";
  pres.subject = "SIH26167 SatQueryAI";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  // Layouts
  pres.defineSlideMaster({
    title: "CLAY_LIGHT",
    background: { color: C.background2 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.9, fontFace: THEME.headFontFace, fontSize: 34, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "" } },
      { text: { text: "SatClip  |  Team Stardust  |  SIH26167", options: { x: 0.6, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: "4A5470", margin: 0 } } },
    ],
    slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: "4A5470", align: "right" },
  });
  pres.defineSlideMaster({
    title: "CLAY_DARK",
    background: { color: C.text2 },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.1, w: 11.7, h: 1.4, fontFace: THEME.headFontFace, fontSize: 48, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "" } },
      { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 3.6, w: 11.7, h: 1.0, fontFace: THEME.bodyFontFace, fontSize: 22, color: "DCE3F7", valign: "top", margin: 0 }, text: "" } },
    ],
  });

  // Clay primitives: an outer shadow (depth) under an inner highlight (soft extrusion).
  let uid = 0;
  function clay(slide, x, y, w, h, fill, o = {}) {
    const r = o.r ?? 0.25;
    const dark = o.dark;
    uid += 1;
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h, rectRadius: r, objectName: `clay-${uid}-base`,
      fill: { color: fill }, line: { color: fill, width: 0.5 },
      shadow: { type: "outer", color: dark ? SHADOW_DEEP : SHADOW_DARK, blur: o.blur ?? 16, offset: o.offset ?? 6, angle: 45, opacity: dark ? 0.6 : 0.55 },
    });
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h, rectRadius: r, objectName: `clay-${uid}-top`,
      fill: { color: fill }, line: { color: fill, width: 0.5 },
      shadow: { type: "inner", color: "FFFFFF", blur: 10, offset: 4, angle: 225, opacity: 0.85 },
    });
  }
  function pill(slide, x, y, w, h, fill, text, o = {}) {
    clay(slide, x, y, w, h, fill, { r: h / 2, blur: 8, offset: 3, dark: o.dark });
    slide.addText(text, { x, y, w, h, isTextBox: true, align: "center", valign: "middle", fontSize: o.fontSize ?? 14, bold: o.bold ?? true, color: o.color ?? HEX.dk1, margin: 0, objectName: `pill-${uid}` });
  }
  async function iconBubble(slide, Comp, x, y, d, fill, color) {
    clay(slide, x, y, d, d, fill, { r: d / 2, blur: 8, offset: 3 });
    slide.addImage({ data: await icon(Comp, color), x: x + d * 0.25, y: y + d * 0.25, w: d * 0.5, h: d * 0.5, altText: "" });
  }
  function shot(slide, file, x, y, w, h, alt) {
    // Screenshot inside a clay frame; the image keeps its aspect ratio and is centred.
    const p = path.join(ASSETS, file);
    const s = pngSize(p);
    clay(slide, x, y, w, h, HEX.lt1, { r: 0.2 });
    const pad = 0.12;
    const bw = w - 2 * pad, bh = h - 2 * pad;
    const k = Math.min(bw / s.w, bh / s.h);
    const iw = s.w * k, ih = s.h * k;
    slide.addImage({ path: p, x: x + pad + (bw - iw) / 2, y: y + pad + (bh - ih) / 2, w: iw, h: ih, altText: alt, rounding: false });
  }
  const body = (slide, text, x, y, w, h, o = {}) =>
    slide.addText(text, { x, y, w, h, isTextBox: true, fontSize: o.fontSize ?? 15, color: o.color ?? HEX.dk1, valign: o.valign ?? "top", margin: o.margin ?? 0, bold: o.bold, align: o.align ?? "left", paraSpaceAfter: o.paraSpaceAfter ?? 4, fit: "none" });

  // ---------- 1. Title ----------
  pres.addSection({ title: "Opening" });
  {
    const s = pres.addSlide({ masterName: "CLAY_DARK", sectionTitle: "Opening" });
    s.addText("SatClip", { placeholder: "title" });
    s.addText("Ask the satellite a plain question. Get evidence, not guesses.", { placeholder: "body" });
    pill(s, 0.8, 1.2, 4.2, 0.55, HEX.accent2, "SIH26167  |  SatQueryAI  |  Space Technology", { fontSize: 13, dark: true });
    pill(s, 0.8, 5.3, 2.9, 0.55, HEX.accent3, "Live Sentinel-1 and 2", { fontSize: 13, dark: true });
    pill(s, 3.95, 5.3, 2.9, 0.55, HEX.accent4, "Abstains when unsure", { fontSize: 13, dark: true });
    pill(s, 7.1, 5.3, 2.9, 0.55, HEX.accent5, "Runs on a CPU", { fontSize: 13, dark: true });
    s.addText("Team Stardust, RVITM Bengaluru", { x: 0.8, y: 6.4, w: 8, h: 0.4, isTextBox: true, fontSize: 14, color: "DCE3F7", margin: 0 });
    s.addNotes("SatClip answers plain-language questions about Indian land, like how much of a district was under water on a date, from live Sentinel data. Each answer is an evidence card: a measured number, a map, scene IDs and dates, a calibrated confidence and a receipt anyone can re-run. When the evidence is weak it says so instead of guessing.");
  }

  // ---------- 2. Who has the problem ----------
  pres.addSection({ title: "Problem" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Problem" });
    s.addText("Three people who need a satellite answer today", { placeholder: "title" });
    const people = [
      [fa.FaHouseDamage, HEX.accent2, "District disaster official", "\"Which parts of my district are under water since Tuesday, and is it spreading?\"", "Waits for central NRSC flood maps: about 300 products for all of India in 2024, delivered same day to two days later."],
      [fa.FaSeedling, HEX.accent3, "Agriculture and crop-insurance officer", "\"Did the crop in these blocks really decline between sowing and harvest?\"", "Relies on slow crop-cutting experiments; satellite yield estimates are disputed without an independent check."],
      [fa.FaSearch, HEX.accent5, "Journalist or fact-checker", "\"Was this village really flooded on the date in the viral post?\"", "Needs GIS skills and hours of data wrangling, or trusts a fluent AI answer that cites no scene."],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.6 + i * 4.15, y = 1.6, w = 3.85, h = 5.0;
      const [Ic, col, who, q, today] = people[i];
      clay(s, x, y, w, h, HEX.lt1);
      await iconBubble(s, Ic, x + 0.35, y + 0.35, 0.9, col, HEX.dk2);
      body(s, who, x + 1.45, y + 0.35, w - 1.7, 0.9, { fontSize: 17, bold: true, valign: "middle" });
      body(s, q, x + 0.35, y + 1.5, w - 0.7, 1.4, { fontSize: 15 });
      clay(s, x + 0.25, y + 3.05, w - 0.5, 1.7, HEX.lt2, { r: 0.18, blur: 6, offset: 2 });
      body(s, [{ text: "Today: ", options: { bold: true } }, { text: today }], x + 0.45, y + 3.2, w - 0.9, 1.45, { fontSize: 13 });
    }
    s.addNotes("Source: SOLUTION.md section 1 and the evidence brief (docs/reference/problem-evidence.md, claims E2, E5, E6, E11, E16). The beachhead is monsoon flood and crop questions at district level.");
  }

  // ---------- 3. Why it lasts ----------
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Problem" });
    s.addText("Why this problem does not go away", { placeholder: "title" });
    const stats = [
      ["735", "districts, each with its own polygon and dates", HEX.accent2, "Questions are local; maps are made centrally"],
      ["~500k", "more geospatial users India needs, against 25k to 50k trained", HEX.accent5, "The skills gap closes slowly"],
      [">60%", "cloud cover over most of India, June to September", HEX.accent4, "Optical fails exactly in the monsoon"],
      ["6 days", "Sentinel-1 radar revisit, free and open", HEX.accent3, "Data is not the bottleneck; trust is"],
    ];
    for (let i = 0; i < 4; i++) {
      const col = i % 2, row = Math.floor(i / 2);
      const x = 0.6 + col * 6.15, y = 1.6 + row * 2.6, w = 5.9, h = 2.3;
      const [n, label, fill, head] = stats[i];
      clay(s, x, y, w, h, fill);
      s.addText(n, { x: x + 0.35, y: y + 0.3, w: 2.4, h: 1.0, isTextBox: true, fontSize: 44, bold: true, color: HEX.dk2, margin: 0, fontFace: THEME.headFontFace });
      body(s, head, x + 2.8, y + 0.35, w - 3.1, 0.9, { fontSize: 17, bold: true, valign: "middle" });
      body(s, label, x + 0.35, y + 1.4, w - 0.7, 0.75, { fontSize: 14 });
    }
    s.addNotes("735 is the number of districts in SatClip's gazetteer (geoBoundaries ADM2). Skills gap: India's geospatial task force (E21, E22). Cloud cover: E30. Sentinel-1C and 1D restore a 6-day revisit (E42, E43). Fluent AI makes this worse: GPT-4V localisation about 0.16 mIoU (A013); 2026 RS hallucination benchmark reports 47 to 61% hallucination rates (A203).");
  }

  // ---------- 4. The solution ----------
  pres.addSection({ title: "Solution" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Solution" });
    s.addText("One question in, one evidence card out", { placeholder: "title" });
    const steps = [
      [fa.FaCommentDots, HEX.accent5, "Ask", "Plain English, Hinglish or Hindi; district and dates"],
      [fa.FaSatellite, HEX.accent2, "Find scenes", "Live STAC search; radar when clouds block optical"],
      [fa.FaRulerCombined, HEX.accent2, "Measure", "Transparent instrument on every map tile"],
      [fa.FaBalanceScale, HEX.accent3, "Calibrate", "Confidence fitted on labelled floods"],
      [fa.FaReceipt, HEX.accent4, "Publish or abstain", "Card with scenes, mask, receipt, or a next step"],
    ];
    for (let i = 0; i < 5; i++) {
      const x = 0.6 + i * 2.48, y = 1.65, w = 2.2, h = 2.75;
      const [Ic, fill, t, d] = steps[i];
      clay(s, x, y, w, h, HEX.lt1);
      await iconBubble(s, Ic, x + 0.65, y + 0.25, 0.9, fill, HEX.dk2);
      body(s, t, x + 0.15, y + 1.3, w - 0.3, 0.45, { fontSize: 17, bold: true, align: "center" });
      body(s, d, x + 0.2, y + 1.75, w - 0.4, 0.95, { fontSize: 13, align: "center" });
    }
    clay(s, 0.6, 4.75, 12.1, 1.95, HEX.accent5);
    body(s, [
      { text: "The core idea: instruments answer, the language model only asks and explains.", options: { bold: true, breakLine: true } },
      { text: "Every number comes from a named, versioned instrument run on an identified Sentinel scene (SAR water threshold, log-ratio change, NDVI difference). A vision-language model never produces the number, because benchmarks show they localise and count poorly." },
    ], 0.95, 4.95, 11.4, 1.6, { fontSize: 16 });
    s.addNotes("This refines the submitted deck: the LoRA-tuned VLM moves from the centre to the language layer (SOLUTION section 8). Evidence: GeoChat, EarthDial and GEOBench-VLM results (A001, A003, A014); RSHBench 2026 (A203).");
  }

  // ---------- 5. Demo: published answer ----------
  pres.addSection({ title: "Demo" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Demo" });
    s.addText("Demo 1: Barpeta flood extent, 11 July 2024", { placeholder: "title" });
    shot(s, "extent.png", 0.6, 1.55, 8.1, 5.2, "SatClip answer card for Barpeta flood extent with map overlay");
    const facts = [
      ["914 sq km", "under water, 39% of the district measured", HEX.accent3],
      ["0.62", "calibrated confidence, just above the 0.60 bar", HEX.accent2],
      ["77 s", "cold, 117 radar tiles on a 2-core CPU; 0.5 s warm", HEX.accent5],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 1.55 + i * 1.78;
      clay(s, 9.05, y, 3.65, 1.5, facts[i][2]);
      s.addText(facts[i][0], { x: 9.3, y: y + 0.15, w: 3.2, h: 0.65, isTextBox: true, fontSize: 30, bold: true, color: HEX.dk2, margin: 0, fontFace: THEME.headFontFace });
      body(s, facts[i][1], 9.3, y + 0.8, 3.2, 0.6, { fontSize: 13 });
    }
    s.addNotes("Live run, docs/demo/TRANSCRIPT.md: scene S1A_IW_GRDH_1SDV_20240711T115715 (Sentinel-1, chosen automatically because of monsoon cloud), receipt 5d27fcc87150f848. Honest caveat: the 914 sq km includes the Brahmaputra channel and permanent wetlands; it has not been checked against an independent flood map.");
  }

  // ---------- 6. Demo: abstention and follow-ups ----------
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Demo" });
    s.addText("Demo 2: when the evidence is weak, SatClip says so", { placeholder: "title" });
    shot(s, "change_abstain_card.png", 0.6, 1.55, 5.95, 4.3, "Abstained flood change card with two follow-up buttons");
    shot(s, "followup_card.png", 6.75, 1.55, 5.95, 4.3, "Published follow-up answer for water before the flood");
    pill(s, 0.6, 6.05, 5.95, 0.65, HEX.accent4, "\"Did the flood spread?\"  Not enough evidence (0.23)", { fontSize: 14 });
    pill(s, 6.75, 6.05, 5.95, 0.65, HEX.accent3, "One click: before 413 sq km (0.73), after 914 sq km (0.62)", { fontSize: 14 });
    s.addNotes("Change areas are the least reliable number SatClip measures (Kuro Siwo calibration: 75% of flood chips undercounted by more than 20%). Instead of a confident wrong number, the card explains why and offers two extent questions, each measured and calibrated on its own. Source: TRANSCRIPT.md, receipts 4b761f62146d6e6d and 3af7eb6ef03ed33a.");
  }

  // ---------- 7. UX states ----------
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Demo" });
    s.addText("Designed for a phone, a hurry and no GIS training", { placeholder: "title" });
    shot(s, "mobile.png", 0.6, 1.55, 2.75, 5.2, "Mobile answer card");
    shot(s, "oos.png", 3.6, 1.55, 2.75, 5.2, "Mobile out of scope refusal");
    const ux = [
      [fa.FaQuestionCircle, HEX.accent4, "Needs one detail", "Ambiguous district names (Aurangabad) ask which one, in 0.01 s, before any data is fetched."],
      [fa.FaBan, HEX.accent5, "Out of scope, by design", "\"How many cars are parked in Mumbai?\" is refused with what SatClip can answer instead."],
      [fa.FaUniversalAccess, HEX.accent2, "Accessible", "Keyboard path tested end to end, ARIA district picker, light and dark themes, plain-language confidence."],
      [fa.FaLanguage, HEX.accent3, "Indian formats", "11/07/2024, \"11th July\", Hindi month names and Hinglish keywords give the same card as English."],
    ];
    for (let i = 0; i < 4; i++) {
      const y = 1.55 + i * 1.33, x = 6.65;
      clay(s, x, y, 6.05, 1.15, HEX.lt1, { r: 0.2 });
      await iconBubble(s, ux[i][0], x + 0.2, y + 0.17, 0.8, ux[i][1], HEX.dk2);
      body(s, [{ text: ux[i][2], options: { bold: true, breakLine: true } }, { text: ux[i][3] }], x + 1.2, y + 0.1, 4.7, 0.95, { fontSize: 13, valign: "middle" });
    }
    s.addNotes("Screenshots are from the prototype (docs/screenshots). Keyboard walkthrough: tools/ui_keyboard_check.py. Parser accuracy on 44 hand-written questions (English, Hinglish, Hindi): 0.68 full match with the rule parser; the LoRA parser (training/) is meant to raise this.");
  }

  // ---------- 8. Why it is easier ----------
  pres.addSection({ title: "Innovation" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Innovation" });
    s.addText("The innovation is ease, not a bigger model", { placeholder: "title" });
    const cols = [
      ["GIS workflow", HEX.lt1, ["Find scenes, check clouds", "Download, calibrate, reproject", "Threshold, map, measure", "Hours to days, needs an analyst"], "Accurate, but out of reach"],
      ["Chat with a VLM", HEX.lt1, ["Upload an image you already have", "Get a fluent paragraph", "No scene ID, date or mask", "47 to 61% hallucination in RS tests"], "Easy, but unverifiable"],
      ["SatClip", HEX.accent3, ["Type the question", "Scenes found, radar if cloudy", "Number, map, confidence, receipt", "About a minute on a CPU"], "Easy and checkable"],
    ];
    for (let i = 0; i < 3; i++) {
      const x = 0.6 + i * 4.15, y = 1.6, w = 3.85, h = 4.15;
      const [t, fill, items, verdict] = cols[i];
      clay(s, x, y, w, h, fill);
      body(s, t, x + 0.35, y + 0.3, w - 0.7, 0.5, { fontSize: 20, bold: true });
      body(s, items.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < items.length - 1 } })), x + 0.35, y + 0.95, w - 0.7, 2.4, { fontSize: 14, paraSpaceAfter: 8 });
      pill(s, x + 0.35, y + 3.35, w - 0.7, 0.55, i === 2 ? HEX.lt1 : HEX.lt2, verdict, { fontSize: 14 });
    }
    clay(s, 0.6, 6.0, 12.1, 0.8, HEX.accent5, { r: 0.2 });
    body(s, "Free-form EO agents pick the right tool parameters only 26 to 35% of the time. SatClip's fixed router to versioned instruments cannot make that error.", 0.9, 6.05, 11.5, 0.7, { fontSize: 14, valign: "middle" });
    s.addNotes("Agent figures: Earth-Agent with GPT-5 (A094) and ThinkGeo with GPT-4o (A092). Hallucination rates: RSHBench 2026 (A203). Day-one value needs no training: instruments are physics-based or pretrained and the data is free (SOLUTION section 4).");
  }

  // ---------- 9. Trust ----------
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Innovation" });
    s.addText("Why the card can be trusted, measured", { placeholder: "title" });
    clay(s, 0.6, 1.55, 7.2, 5.2, HEX.lt1);
    s.addChart(pres.charts.BAR, [
      { name: "Water v1.0 (VV)", labels: ["Answers correct", "Coverage at 0.60", "Median IoU", "Error when published"], values: [44, 11, 15, 33] },
      { name: "Water v1.1 (VV + VH)", labels: ["Answers correct", "Coverage at 0.60", "Median IoU", "Error when published"], values: [55, 43, 31, 26] },
    ], {
      x: 0.8, y: 1.7, w: 6.8, h: 4.9, barDir: "col", barGapWidthPct: 60,
      chartColors: ["9FB4D9", HEX.accent1], showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 11, dataLabelColor: HEX.dk1,
      dataLabelFormatCode: "0\"%\"", showTitle: true, title: "Held-out Sen1Floods11 test, 82 chips (%)", titleFontSize: 13, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
      catAxisLabelColor: HEX.dk1, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
      showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.dk1, valAxisMaxVal: 70, dataLabelFontFace: "+mn-lt",
    });
    const t = [
      [fa.FaBalanceScale, HEX.accent3, "Calibrated", "Water ECE 0.074; change ECE 0.214 to 0.041 with per-regime maps"],
      [fa.FaHandPaper, HEX.accent4, "Abstains", "Below 0.60 no number is published, and the card says what would help"],
      [fa.FaRedo, HEX.accent2, "Reproducible", "8 of 8 demo receipts (713 tiles) re-ran to identical outputs"],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 1.55 + i * 1.78;
      clay(s, 8.1, y, 4.6, 1.5, HEX.lt1, { r: 0.2 });
      await iconBubble(s, t[i][0], 8.3, y + 0.33, 0.85, t[i][1], HEX.dk2);
      body(s, [{ text: t[i][2], options: { bold: true, breakLine: true } }, { text: t[i][3] }], 9.35, y + 0.15, 3.2, 1.2, { fontSize: 13, valign: "middle" });
    }
    s.addNotes("Sources: training/calibration/reports/sar_water_otsu.md (v1.0 vs v1.1), fit_change report (Kuro Siwo, grouped cross-validation by event), docs/quality/reproducibility.json. The reproducibility check caught a real defect in run 8 (GDAL decimation under concurrency) which is fixed. Crop-change confidence is still a labelled placeholder: no open Indian crop-decline labels exist.");
  }

  // ---------- 10. Architecture and scale ----------
  pres.addSection({ title: "Architecture" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Architecture" });
    s.addText("Scales out, or runs offline on state servers", { placeholder: "title" });
    const boxes = [
      ["Web UI", "Phone first, no build step", HEX.accent5],
      ["Stateless API", "FastAPI; parse, route, cache", HEX.accent2],
      ["Tile queue", "Redis lists, one job = many tiles", HEX.accent2],
      ["Workers", "Instruments on COG windows", HEX.accent3],
      ["Public STAC", "Planetary Computer, Earth Search, CDSE", HEX.accent4],
    ];
    for (let i = 0; i < 5; i++) {
      const x = 0.6 + i * 2.48, y = 1.6, w = 2.2, h = 1.55;
      clay(s, x, y, w, h, boxes[i][2]);
      body(s, [{ text: boxes[i][0], options: { bold: true, breakLine: true } }, { text: boxes[i][1] }], x + 0.18, y + 0.15, w - 0.36, h - 0.3, { fontSize: 13, valign: "middle", align: "center" });
      if (i < 4) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + w + 0.04, y: y + 0.6, w: 0.2, h: 0.35, fill: { color: HEX.dk2 }, line: { color: HEX.dk2 }, objectName: `arrow-${i}` });
    }
    clay(s, 0.6, 3.5, 6.6, 3.25, HEX.lt1);
    s.addChart(pres.charts.BAR, [{ name: "Tiles per second", labels: ["1 worker", "2 workers", "4 workers"], values: [2.0, 4.0, 7.8] }], {
      x: 0.8, y: 3.6, w: 6.2, h: 3.05, barDir: "col", barGapWidthPct: 70, chartColors: [HEX.accent1],
      showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 11, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt", dataLabelFormatCode: "0.0",
      showTitle: true, title: "Throughput with real Redis and 400 ms reads (tiles/s)", titleFontSize: 13, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
      catAxisLabelColor: HEX.dk1, catAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, valAxisMaxVal: 9,
    });
    const notes = [
      ["Near-linear scale-out", "Reads dominate; adding workers adds throughput"],
      ["Cheap per worker", "About 86 MB RAM each; Redis 13 MB"],
      ["Fast repeats", "Warm 144-tile job in 0.01 to 0.2 s"],
      ["Offline ready", "Docker compose; point STAC at an on-prem mirror"],
    ];
    for (let i = 0; i < 4; i++) {
      const y = 3.5 + i * 0.83;
      clay(s, 7.5, y, 5.2, 0.7, HEX.lt1, { r: 0.18, blur: 8, offset: 3 });
      body(s, [{ text: notes[i][0] + ": ", options: { bold: true } }, { text: notes[i][1] }], 7.7, y + 0.05, 4.9, 0.6, { fontSize: 13, valign: "middle" });
    }
    s.addNotes("Source: docs/QUALITY.md and docs/quality/loadtest.json (2 vCPU sandbox). Compute is about 0.1 s per tile; with simulated 400 ms reads, 1, 2 and 4 Redis workers gave 2.0, 4.0 and 7.8 tiles/s. Parse-only API: 84 requests/s, p50 14 ms. Architecture: docs/ARCHITECTURE.md.");
  }

  // ---------- 11. Research landscape ----------
  pres.addSection({ title: "Research" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Research" });
    s.addText("225 papers read: nobody combines all of it yet", { placeholder: "title" });
    const idx = fs.readFileSync(path.join(ROOT, "archive", "index.csv"), "utf8");
    const counts = {};
    const nice = { "rs-vlm": "RS vision-language models", "trust-calibration": "Trust and calibration", "rs-benchmark": "RS benchmarks", "eo-foundation": "EO foundation models", "change-detection": "Change detection", "sar-optical-fusion": "SAR and fusion", "indian-context": "Indian context", "eo-agents": "EO agents", "human-factors": "Human factors", "data-infrastructure": "Data infrastructure", "efficient-inference": "Efficient inference", "upcoming": "Upcoming (2026)", "historical": "Historical", "object-detection": "Object detection" };
    for (const line of idx.split("\n").slice(1)) {
      const m = line.match(/,(rs-vlm|trust-calibration|rs-benchmark|eo-foundation|change-detection|sar-optical-fusion|indian-context|eo-agents|human-factors|data-infrastructure|efficient-inference|upcoming|historical|object-detection),/);
      if (m) counts[m[1]] = (counts[m[1]] || 0) + 1;
    }
    const keys = Object.keys(counts).sort((a, b) => counts[a] - counts[b]);
    const total = keys.reduce((a, k) => a + counts[k], 0);
    clay(s, 0.6, 1.55, 6.0, 5.2, HEX.lt1);
    s.addChart(pres.charts.BAR, [{ name: "Papers", labels: keys.map((k) => nice[k]), values: keys.map((k) => counts[k]) }], {
      x: 0.75, y: 1.65, w: 5.7, h: 5.0, barDir: "bar", barGapWidthPct: 40, chartColors: [HEX.accent1],
      showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 10, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
      showTitle: true, title: `Archive by category (${total} papers)`, titleFontSize: 13, titleColor: HEX.dk1, titleFontFace: "+mn-lt",
      catAxisLabelColor: HEX.dk1, catAxisLabelFontSize: 10, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false,
    });
    const rivals = [
      ["VisTA (2024)", "change answers with masks", "no confidence, no live data"],
      ["EO-Gym (2026)", "switches optical to SAR", "no abstention or receipts"],
      ["SHRUG-FM (2026)", "rejects unreliable flood maps", "scores not calibrated, optical"],
      ["UnivEARTH (2026)", "agents fetch live imagery", "best 64.5% accuracy, never abstains"],
      ["TerraScope (2026)", "pixel-grounded area answers", "GPU, no calibration or provenance"],
    ];
    for (let i = 0; i < 5; i++) {
      const y = 1.55 + i * 1.05;
      clay(s, 6.9, y, 5.8, 0.88, HEX.lt1, { r: 0.18, blur: 8, offset: 3 });
      body(s, [{ text: rivals[i][0] + ": ", options: { bold: true } }, { text: "has " + rivals[i][1] + "; " + rivals[i][2] }], 7.1, y + 0.06, 5.4, 0.76, { fontSize: 13, valign: "middle" });
    }
    s.addNotes("Full archive: archive/README.md and archive/index.csv, one entry per paper with what it means for SatClip. Closest prior work: VisTA A179, EO-Gym A176, SHRUG-FM A202, UnivEARTH A204, TerraScope A201. The novelty claim (NOVELTY.md) is the combination: calibrated confidence, threshold abstention with a next step, scene receipts, live Sentinel retrieval with automatic SAR fallback, on CPU, for Indian non-experts.");
  }

  // ---------- 12. Honest limits and roadmap ----------
  pres.addSection({ title: "Roadmap" });
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Roadmap" });
    s.addText("What it does not do yet, and what comes next", { placeholder: "title" });
    clay(s, 0.6, 1.55, 5.6, 5.2, HEX.accent4);
    body(s, "Known limits, stated on the card", 0.9, 1.8, 5.0, 0.5, { fontSize: 18, bold: true });
    const lim = [
      "Flood extent includes rivers, wetlands and paddy (no HAND terrain mask yet)",
      "Urban flooding is missed by radar intensity alone",
      "Crop-change confidence is a placeholder: no open Indian labels",
      "Flood change areas are often undercounted, so they abstain",
    ];
    body(s, lim.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < lim.length - 1 } })), 0.9, 2.45, 5.0, 4.1, { fontSize: 15, paraSpaceAfter: 10 });
    const road = [
      ["Next", "HAND and permanent-water exclusion mask; per-pixel water probability", HEX.accent2],
      ["Then", "LoRA intent parser trained on Colab; Hindi district names", HEX.accent5],
      ["Pilot", "One district disaster office in Assam or Bihar through a monsoon", HEX.accent3],
      ["Scale", "On-prem STAC mirror on state infrastructure; more instruments", HEX.lt1],
    ];
    for (let i = 0; i < 4; i++) {
      const y = 1.55 + i * 1.33;
      clay(s, 6.5, y, 6.2, 1.15, road[i][2], { r: 0.2 });
      pill(s, 6.7, y + 0.3, 1.2, 0.55, HEX.lt1, road[i][0], { fontSize: 14 });
      body(s, road[i][1], 8.1, y + 0.1, 4.45, 0.95, { fontSize: 14, valign: "middle" });
    }
    s.addNotes("Limits: SOLUTION.md section 9 (risks 12 and 17), archive A210 (HAND), A211 (exclusion maps), A212 (probabilistic flood mapping), A214 and A215 (urban flood coherence; Planetary Computer RTC has no phase, so coherence is not available today). Training code is ready to run: training/colab/satclip_lora.ipynb.");
  }

  // ---------- 13. Team ----------
  {
    const s = pres.addSlide({ masterName: "CLAY_LIGHT", sectionTitle: "Roadmap" });
    s.addText("Team Stardust", { placeholder: "title" });
    const team = ["Sai Bhuwan S", "Yashita Mandavilli", "Raj Venkat", "Nikhil S Rao", "Shashwat Mittal", "Sasanuru Anirudh"];
    const fills = [HEX.accent2, HEX.accent3, HEX.accent5, HEX.accent4, HEX.accent2, HEX.accent3];
    for (let i = 0; i < 6; i++) {
      const col = i % 3, row = Math.floor(i / 3);
      const x = 0.6 + col * 4.15, y = 1.7 + row * 2.4, w = 3.85, h = 2.0;
      clay(s, x, y, w, h, HEX.lt1);
      const initials = team[i].split(" ").filter((p) => p.length > 1).slice(0, 2).map((p) => p[0]).join("");
      clay(s, x + 0.35, y + 0.45, 1.1, 1.1, fills[i], { r: 0.55, blur: 8, offset: 3 });
      s.addText(initials, { x: x + 0.35, y: y + 0.45, w: 1.1, h: 1.1, isTextBox: true, align: "center", valign: "middle", fontSize: 24, bold: true, color: HEX.dk2, margin: 0 });
      body(s, team[i], x + 1.7, y + 0.45, w - 1.9, 1.1, { fontSize: 18, bold: true, valign: "middle" });
    }
    s.addNotes("Team Stardust, RVITM Bengaluru, Smart India Hackathon 2026, problem statement SIH26167.");
  }

  // ---------- 14. Close ----------
  {
    const s = pres.addSlide({ masterName: "CLAY_DARK", sectionTitle: "Roadmap" });
    s.addText("Every answer, with its evidence", { placeholder: "title" });
    s.addText("Open source, free data, runs on a CPU. Code, archive and receipts: github.com/UnKnownnPasta/satclip", { placeholder: "body" });
    pill(s, 0.8, 5.2, 3.2, 0.6, HEX.accent3, "Measured number", { dark: true });
    pill(s, 4.25, 5.2, 3.2, 0.6, HEX.accent2, "Scenes, dates, map", { dark: true });
    pill(s, 7.7, 5.2, 3.2, 0.6, HEX.accent4, "Confidence or abstain", { dark: true });
    s.addNotes("Close on the evidence card. Offer to run a live question for the jury's own district.");
  }

  await pres.writeFile({ fileName: OUT });
  await fixInnerShadows(OUT);
  if (SKILL) {
    const { applyTheme } = require(path.join(SKILL, "scripts", "apply_theme.js"));
    await applyTheme(OUT, THEME);
  }
  console.log("wrote", OUT);
}

main().catch((e) => { console.error(e); process.exit(1); });
