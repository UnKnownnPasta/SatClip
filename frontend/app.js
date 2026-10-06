// SatClip web UI (M4). Plain JavaScript, no build step, so it runs from any static server or offline.
// Flow: ask -> show what was understood -> stream tile progress -> evidence card + map overlay.
"use strict";
const $ = (id) => document.getElementById(id);
const API = location.port === "8080" || location.protocol === "file:" ? "http://localhost:8000" : "";
const ui = { abstain_below: 0.6, bands: [], window_half_days: 6, basemap: {}, examples: [] };
const state = { region: null, regionLayer: null, overlays: null, lastCard: null, source: null };

const NEEDS_INPUT = new Set(["out_of_scope", "missing_area", "invalid_area", "missing_dates", "need_two_dates", "ambiguous_area"]);
const REASONS = {
  out_of_scope: "This is not one of the four questions SatClip can measure.",
  missing_area: "I could not tell which place you mean.",
  invalid_area: "The area is not valid.",
  missing_dates: "The question has no date.",
  need_two_dates: "A change question needs two dates.",
  ambiguous_area: "More than one district has this name.",
  low_confidence: "The measurement is below the confidence needed to publish it.",
};

function el(tag, attrs = {}, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") n.className = v; else if (k === "text") n.textContent = v; else n.setAttribute(k, v);
  }
  kids.forEach((k) => n.append(k));
  return n;
}
const fmtKm = (x) => (x >= 100 ? Math.round(x).toLocaleString("en-IN") : x >= 1 ? x.toFixed(1) : x.toFixed(2));
const iso = (d) => d.toISOString().slice(0, 10);
function windowFor(day) {
  const d = new Date(`${day}T00:00:00Z`), h = ui.window_half_days * 864e5;
  return { start: iso(new Date(d - h)), end: iso(new Date(+d + h)) };
}

// ---------- map ----------
const map = L.map("map", { zoomControl: true, attributionControl: true }).setView([22.5, 82], 5);
map.attributionControl.setPrefix("Leaflet");
function initBasemap() {
  const b = ui.basemap || {};
  if (!b.url) { $("map-note").textContent += " No base map is configured (offline mode)."; return; }
  L.tileLayer(b.url, { maxZoom: b.max_zoom || 18, attribution: b.attribution || "" }).addTo(map);
}
async function showRegion(key) {
  if (!key || (state.region && state.region.key === key && state.regionLayer)) return;
  try {
    const f = await (await fetch(`${API}/v1/regions/${encodeURIComponent(key)}`)).json();
    if (state.regionLayer) state.regionLayer.remove();
    state.regionLayer = L.geoJSON(f, { style: { color: "#5b4bd6", weight: 3, fillOpacity: 0.04, dashArray: "6 4" } }).addTo(map);
    map.fitBounds(state.regionLayer.getBounds(), { padding: [16, 16] });
    state.region = { key, name: f.properties.name, state: f.properties.state };
  } catch { /* the map is a convenience; the card carries every number */ }
}
function showOverlays(masks) {
  if (state.overlays) state.overlays.remove();
  state.overlays = L.layerGroup();
  const legend = {};
  (masks || []).forEach((m) => {
    const [w, s, e, n] = m.bounds;
    L.imageOverlay(`${API}${m.href}`, [[s, w], [n, e]], { opacity: 0.85, alt: "Measured overlay tile" }).addTo(state.overlays);
    Object.entries(m.legend || {}).forEach(([k, label]) => { legend[label] = (m.colors || {})[k] || "#6c5ce7"; });
  });
  if ($("show-overlay").checked) state.overlays.addTo(map);
  const ul = $("legend");
  ul.replaceChildren(...Object.entries(legend).map(([label, c]) => el("li", {}, el("i", { style: `background:${c}` }), label)));
  if (state.regionLayer) ul.prepend(el("li", {}, el("i", { style: "background:transparent;border:2px dashed #5b4bd6" }), "district boundary"));
}
$("show-overlay").addEventListener("change", (e) => {
  if (!state.overlays) return;
  e.target.checked ? state.overlays.addTo(map) : state.overlays.remove();
});

// ---------- district combobox (ARIA 1.2 pattern) ----------
const place = $("place"), list = $("place-list");
let hits = [], active = -1, timer = null;
function closeList() { list.classList.add("hidden"); place.setAttribute("aria-expanded", "false"); place.removeAttribute("aria-activedescendant"); active = -1; }
function renderList() {
  list.replaceChildren(...hits.map((h, i) => el("li", { id: `opt-${i}`, role: "option", "aria-selected": String(i === active) },
    el("span", { text: h.name }), el("span", { class: "st", text: h.state }))));
  list.classList.toggle("hidden", !hits.length);
  place.setAttribute("aria-expanded", String(!!hits.length));
  if (active >= 0) place.setAttribute("aria-activedescendant", `opt-${active}`);
  [...list.children].forEach((li, i) => li.addEventListener("mousedown", (e) => { e.preventDefault(); pick(hits[i]); }));
}
function pick(h) {
  closeList();
  place.value = "";
  state.picked = h;
  const box = $("place-picked");
  const rm = el("button", { type: "button", class: "chip clay-sm", "aria-label": `Remove ${h.name}, ${h.state}` }, `${h.name}, ${h.state}  ✕`);
  rm.addEventListener("click", () => { state.picked = null; box.classList.add("hidden"); box.replaceChildren(); place.focus(); });
  box.replaceChildren(rm);
  box.classList.remove("hidden");
  showRegion(h.key);
}
place.addEventListener("input", () => {
  clearTimeout(timer);
  const q = place.value.trim();
  if (q.length < 2) { hits = []; closeList(); return; }
  timer = setTimeout(async () => {
    try { hits = (await (await fetch(`${API}/v1/regions?q=${encodeURIComponent(q)}&limit=8`)).json()).regions; }
    catch { hits = []; }
    active = -1; renderList();
  }, 150);
});
place.addEventListener("keydown", (e) => {
  if (e.key === "ArrowDown" && hits.length) { active = (active + 1) % hits.length; renderList(); e.preventDefault(); }
  else if (e.key === "ArrowUp" && hits.length) { active = (active - 1 + hits.length) % hits.length; renderList(); e.preventDefault(); }
  else if (e.key === "Enter" && active >= 0) { pick(hits[active]); e.preventDefault(); }
  else if (e.key === "Escape") closeList();
});
place.addEventListener("blur", () => setTimeout(closeList, 120));

// ---------- dates ----------
document.querySelectorAll("input[name=mode]").forEach((r) => r.addEventListener("change", () => {
  const two = document.querySelector("input[name=mode]:checked").value === "two";
  $("d2-wrap").classList.toggle("hidden", !two);
  $("d1-label").textContent = two ? "Before date" : "Date";
}));
$("d1").max = $("d2").max = iso(new Date());

// ---------- progress ----------
function step(name) {
  document.querySelectorAll("#steps li").forEach((li) => li.classList.remove("skipped"));
  const order = ["parse", "scenes", "measure", "check"];
  const at = order.indexOf(name);
  document.querySelectorAll("#steps li").forEach((li, i) => {
    li.classList.toggle("done", i < at || name === "done");
    li.classList.toggle("active", i === at);
    if (i === at) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
  });
}
function progress(done, total) {
  const pct = total ? Math.round((100 * done) / total) : 0;
  $("bar").style.width = `${pct}%`;
  $("progress").setAttribute("aria-valuenow", String(pct));
  $("progress").classList.toggle("indeterminate", !total);
  $("progress-text").textContent = total ? `${done} of ${total} map tiles measured` : "Looking for satellite passes";
}

// ---------- evidence card ----------
function headline(card) {
  if (card.abstained || card.value == null) return "";
  if (card.unit === "km2") return `${fmtKm(card.value)} <small>sq km</small>`;
  if (card.breakdown) { const [k, v] = Object.entries(card.breakdown)[0]; return `${Math.round(v * 100)}% <small>${k}</small>`; }
  return `${card.value}`;
}
function evidenceChips(card) {
  const items = [];
  // Group scenes by sensor and date: one district often needs several adjacent granules from the same pass.
  const groups = new Map();
  (card.scenes || []).forEach((s) => {
    const s1 = /S1|sentinel-1/i.test(s.sensor), k = `${s1 ? "S1" : "S2"}|${s.date}`;
    if (!groups.has(k)) groups.set(k, { s1, date: s.date, ids: [] });
    groups.get(k).ids.push(s.id);
  });
  [...groups.values()].sort((a, b) => a.date.localeCompare(b.date)).forEach((g) => {
    const n = g.ids.length;
    items.push(el("li", { class: g.s1 ? "s1" : "s2", title: g.ids.join("\n") },
      el("span", { class: "sensor", text: g.s1 ? "Radar S1" : "Optical S2" }), g.date + (n > 1 ? ` (${n} scenes)` : "")));
  });
  if (card.tiles_total) items.push(el("li", { class: "meta", text: `${card.tiles_answered} of ${card.tiles_total} tiles measured` }));
  if (card.region_name) items.push(el("li", { class: "meta", text: card.region_name }));
  if (card.calibration) {
    const fitted = /^fitted/.test(card.calibration);
    items.push(el("li", { class: fitted ? "meta" : "warnchip", text: fitted ? "Confidence calibrated" : "Confidence not yet calibrated" }));
  }
  if (card.observed_vs_inferred && card.observed_vs_inferred !== "observed") items.push(el("li", { class: "warnchip", text: card.observed_vs_inferred }));
  return items;
}
function drawer(card) {
  const body = [];
  if (card.method) body.push(el("h4", { text: "Method" }), el("p", { text: card.method }));
  if (card.instrument) body.push(el("p", { class: "muted small", text: `Instrument: ${card.instrument}` }));
  if (card.selection_notes?.length) body.push(el("h4", { text: "Why these satellite passes" }), el("ul", {}, ...card.selection_notes.map((t) => el("li", { text: t }))));
  const d = card.details || {};
  const nums = [["measured_km2", "area measured"], ["water_before_km2", "water before"], ["water_after_km2", "water after"],
    ["receded_km2", "water receded"], ["vegetated_before_km2", "green before"], ["gain_km2", "greenness rose"]]
    .filter(([k]) => d[k] != null).map(([k, label]) => el("div", {}, el("b", { text: `${fmtKm(d[k])} sq km` }), el("span", { text: label })));
  if (nums.length) body.push(el("h4", { text: "Numbers" }), el("div", { class: "numbers" }, ...nums));
  if (card.breakdown) {
    body.push(el("h4", { text: "Breakdown" }), el("ul", { class: "bars" }, ...Object.entries(card.breakdown).map(([k, v]) =>
      el("li", {}, el("span", { text: k }), el("span", { class: "bar", role: "img", "aria-label": `${k} ${Math.round(v * 100)} percent` },
        el("span", { style: `width:${(v * 100).toFixed(1)}%` })), el("span", { text: `${Math.round(v * 100)}%` })))));
  }
  if (card.caveats?.length) body.push(el("h4", { text: "What this cannot tell you" }), el("ul", {}, ...card.caveats.map((t) => el("li", { text: t }))));
  if (card.calibration) body.push(el("h4", { text: "Calibration" }), el("p", { text: card.calibration }));
  if (!body.length) body.push(el("p", { text: "No measurement was run for this question." }));
  $("drawer-body").replaceChildren(...body);
}
function renderCard(card, parsed) {
  state.lastCard = card;
  const c = $("card");
  c.classList.remove("hidden");
  c.classList.toggle("abstain", card.abstained);
  // Two kinds of "no": SatClip needs a detail from you, or the satellite evidence was not good enough.
  const needsInput = card.abstained && NEEDS_INPUT.has(card.reason);
  $("badge").className = `badge ${!card.abstained ? "ok" : needsInput ? "input" : "abstain"}`;
  $("badge").textContent = !card.abstained ? "Answer" : needsInput ? "Needs one detail" : "Not enough evidence";
  $("card-title").textContent = !card.abstained ? "Measured answer" : needsInput ? "Nothing measured yet" : "SatClip did not publish a number";
  $("headline").innerHTML = headline(card);
  $("headline").classList.toggle("hidden", !$("headline").innerHTML);
  $("answer").textContent = card.answer_text;

  const hasConf = card.confidence != null;
  $("meter-wrap").classList.toggle("hidden", !hasConf);
  if (hasConf) {
    $("meter-fill").style.width = `${Math.max(2, card.confidence * 100)}%`;
    $("meter-threshold").style.left = `calc(${ui.abstain_below * 100}% - 1px)`;
    $("meter-text").textContent = `Confidence ${card.confidence.toFixed(2)} (${card.confidence_band || "unrated"}). ` +
      `SatClip publishes a number only at or above ${ui.abstain_below.toFixed(2)} (the marker).`;
  }

  const box = $("abstain-box");
  box.classList.toggle("hidden", !card.abstained);
  if (card.abstained) {
    $("reason").textContent = REASONS[card.reason] || (card.reason ? `Why: ${card.reason}` : "Not enough evidence.");
    $("next").textContent = card.next_step ? `What would help: ${card.next_step}` : "";
    const keys = parsed?.candidate_keys || [], labels = parsed?.candidates || [];
    $("choices").replaceChildren(...keys.map((k, i) => {
      const b = el("button", { type: "button", class: "chip clay-sm", text: `Use ${labels[i]}` });
      b.addEventListener("click", () => { const [name, st] = labels[i].split(", "); pick({ key: k, name, state: st }); submit(); });
      return b;
    }));
  }
  $("evidence").replaceChildren(...evidenceChips(card));
  drawer(card);
  $("drawer").classList.toggle("hidden", !card.method && !card.caveats?.length);
  const rid = card.receipt_id;
  $("receipt").classList.toggle("hidden", !rid);
  $("copy").classList.toggle("hidden", !rid);
  $("receipt").href = rid ? `${API}/v1/receipts/${rid}` : "#";
  showOverlays(card.masks);
  if (card.tiles_total) step("done");
  else document.querySelectorAll("#steps li").forEach((li, i) => { li.classList.toggle("done", i === 0); li.classList.toggle("skipped", i > 0); li.classList.remove("active"); });
  progress(card.tiles_total || 0, card.tiles_total || 0);
  $("progress").classList.remove("indeterminate");
  $("abstain-box").classList.toggle("input", needsInput);
  $("progress-text").textContent = card.tiles_total ? `${card.tiles_answered} of ${card.tiles_total} map tiles measured` : "No measurement needed";
  c.focus({ preventScroll: false });
  setBusy(false);
}
$("copy").addEventListener("click", async () => {
  const rid = state.lastCard?.receipt_id; if (!rid) return;
  try { await navigator.clipboard.writeText(rid); $("copy").textContent = "Copied"; } catch { $("copy").textContent = rid; }
  setTimeout(() => { $("copy").textContent = "Copy receipt ID"; }, 2000);
});
$("again").addEventListener("click", () => { $("q").focus(); $("q").select(); });

// ---------- ask ----------
function setBusy(b) { $("go").disabled = b; $("go").querySelector(".go-label").textContent = b ? "Measuring..." : "Ask"; $("ask").setAttribute("aria-busy", String(b)); }
function buildRequest() {
  const text = $("q").value.trim();
  const body = { text };
  if (state.picked) body.region = state.picked.key;
  const two = document.querySelector("input[name=mode]:checked").value === "two";
  const d1 = $("d1").value, d2 = $("d2").value;
  if (two && d1 && d2) body.windows = [windowFor(d1), windowFor(d2)];
  else if (!two && d1) body.windows = [windowFor(d1)];
  return body;
}
async function submit() {
  const err = $("q-err");
  const body = buildRequest();
  if (body.text.length < 3) { err.textContent = "Type a question first, or tap an example."; err.classList.remove("hidden"); $("q").focus(); return; }
  err.classList.add("hidden");
  if (state.source) state.source.close();
  setBusy(true);
  $("card").classList.add("hidden");
  $("understood").classList.remove("hidden");
  $("understood-text").textContent = "Reading your question";
  step("parse"); progress(0, 0);
  let res, out;
  try {
    res = await fetch(`${API}/v1/queries`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    out = await res.json();
  } catch {
    setBusy(false);
    renderCard({ abstained: true, answer_text: "SatClip's server could not be reached.", next_step: "Check your connection and try again." });
    return;
  }
  if (!res.ok) { setBusy(false); renderCard({ abstained: true, answer_text: typeof out.detail === "string" ? out.detail : "The request was not valid." }); return; }
  $("understood-text").textContent = out.parsed.understood_as;
  if (out.parsed.region) showRegion(out.parsed.region);
  if (out.card) { renderCard(out.card, out.parsed); return; }
  step("scenes");
  let done = 0;
  const src = new EventSource(`${API}/v1/jobs/${out.job_id}/events`);
  state.source = src;
  src.addEventListener("tile", () => { done += 1; step("measure"); progress(done, out.n_tiles); if (done === out.n_tiles) step("check"); });
  src.addEventListener("card", (ev) => { src.close(); renderCard(JSON.parse(ev.data), out.parsed); });
  src.onerror = async () => {
    src.close();
    try { const j = await (await fetch(`${API}/v1/jobs/${out.job_id}`)).json(); if (j.card) { renderCard(j.card, out.parsed); return; } } catch { /* fall through */ }
    setBusy(false);
    $("progress-text").textContent = "Lost the live progress stream. The job may still finish; ask again to see it.";
  };
}
$("ask").addEventListener("submit", (e) => { e.preventDefault(); submit(); });
$("q").addEventListener("keydown", (e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); submit(); } });

// ---------- boot ----------
function renderExamples() {
  const ex = ui.examples.length ? ui.examples : [{ label: "Flood extent", text: "How much of Barpeta was under water on 2024-07-11?" }];
  $("examples").replaceChildren(...ex.map((x) => {
    const b = el("button", { type: "button", class: "chip clay-sm", text: x.label, title: x.text, "aria-label": `Example: ${x.text}` });
    b.addEventListener("click", () => { $("q").value = x.text; $("q").focus(); });
    return b;
  }));
}
(async function boot() {
  try {
    const [h, cfg] = await Promise.all([fetch(`${API}/health`).then((r) => r.json()), fetch(`${API}/v1/ui-config`).then((r) => r.json())]);
    Object.assign(ui, cfg);
    $("status").textContent = `Online, v${h.version}`;
    $("status").classList.add("ok");
  } catch {
    $("status").textContent = "Server offline";
    $("status").classList.add("bad");
  }
  $("half").textContent = ui.window_half_days;
  initBasemap();
  renderExamples();
  const q = new URLSearchParams(location.search).get("q");
  if (q) { $("q").value = q; submit(); }
})();
