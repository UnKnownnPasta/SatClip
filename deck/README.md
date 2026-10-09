# SatClip deck (M7)

- `satclip.pptx`: 14-slide pitch and demo deck in claymorphism style (soft extruded cards with paired outer and inner shadows, pastel palette with dark ink text). Speaker notes on every slide name the source of each number.
- Rebuild:
  1. Start the API: `cd backend && uvicorn satclip.api.main:app --port 8000`.
  2. `python tools/screenshots.py` (warms the scene cache; live questions take 20 to 100 s each).
  3. `python deck/capture_assets.py` (element screenshots of the evidence card and map into `deck/assets/`).
  4. `PPTX_SKILL=<path to the pptx skill> node deck/build_deck.js` (needs pptxgenjs, react, react-dom, react-icons, sharp; the skill path is only used to apply the theme colours).
- Story: users and problem, why it lasts, the solution, two live demos (published answer, abstention with follow-ups), UX states, why it is easier, trust (measured calibration and reproducibility), architecture and measured scaling, research landscape (archive chart is read from `archive/index.csv` at build time), limits and roadmap, team.
