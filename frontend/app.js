// SatClip UI shell (M1): ask, show what was understood, stream tile progress, render the evidence card.
const $ = (id) => document.getElementById(id);
const API = location.port === "8080" || location.protocol === "file:" ? "http://localhost:8000" : "";

document.querySelectorAll("[data-q]").forEach((b) =>
  b.addEventListener("click", () => { $("q").value = b.dataset.q; $("q").focus(); }));

function chip(text, cls) {
  const s = document.createElement("span");
  s.className = `chip ev clay-sm ${cls}`;
  s.textContent = text;
  return s;
}

function renderCard(card) {
  const el = $("card");
  el.classList.remove("hidden");
  el.classList.toggle("abstain", card.abstained);
  $("card-title").textContent = card.abstained ? "Not enough evidence" : "Answer";
  $("answer").textContent = card.answer_text;
  const ev = $("evidence");
  ev.replaceChildren();
  (card.scenes || []).slice(0, 4).forEach((s) => {
    ev.append(chip(`Scene ${s.id.slice(0, 28)}`, "scene"), chip(`${s.sensor} ${s.date}`, "date"));
  });
  if (card.confidence != null) ev.append(chip(`Confidence ${card.confidence_band} (${card.confidence.toFixed(2)})`, "conf"));
  if (card.tiles_total) ev.append(chip(`${card.tiles_answered}/${card.tiles_total} tiles measured`, "tiles"));
  if (card.observed_vs_inferred && card.observed_vs_inferred !== "observed") ev.append(chip(card.observed_vs_inferred, "date"));
  const next = $("next");
  next.classList.toggle("hidden", !card.next_step);
  next.textContent = card.next_step ? `What would help: ${card.next_step}` : "";
  $("receipt").href = `${API}/v1/receipts/${card.receipt_id}`;
  el.focus?.();
}

$("ask").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("card").classList.add("hidden");
  const res = await fetch(`${API}/v1/queries`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: $("q").value.trim() }),
  });
  const body = await res.json();
  if (!res.ok) { renderCard({ abstained: true, answer_text: body.detail || "Request failed.", scenes: [] }); return; }
  $("understood").classList.remove("hidden");
  $("understood-text").textContent = body.parsed.understood_as;
  if (body.card) { $("bar").style.width = "0"; $("progress-text").textContent = ""; renderCard(body.card); return; }
  let done = 0;
  const src = new EventSource(`${API}/v1/jobs/${body.job_id}/events`);
  src.addEventListener("tile", () => {
    done += 1;
    $("bar").style.width = `${(100 * done) / body.n_tiles}%`;
    $("progress-text").textContent = `${done} of ${body.n_tiles} tiles measured`;
  });
  src.addEventListener("card", (ev) => { src.close(); renderCard(JSON.parse(ev.data)); });
  src.onerror = () => src.close();
});
