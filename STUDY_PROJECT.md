# Patente B — Study Project (handoff & continuation)

This file is the single reference to continue the work from any computer.
Goal: build **one scrollable page listing every official Patente B exam question**,
grouped by the 25 sections, each with **Italian text · English translation · a memory hint · the sign image** (if any).

Last updated: 2026-06-23.

---

## 1. The exam — rules (facts, verified)

- The theory exam is drawn **verbatim from a fixed, public ministerial question bank** (MIT — Motorizzazione Civile). Nothing is improvised; study the whole bank and you've seen every possible question.
- **Format (current, since 20 Dec 2021):**
  - **30 questions**, each a **Vero / Falso** (True/False) statement
  - **20 minutes**
  - **max 3 errors** to pass (≥27 correct)
  - questions sampled across all **25 sections (argomenti)**
- Official bank size: **~7,105 questions** (official listato, 23-04-2025). Many are the same rule reworded.
- Verified against the **official government source**: `ilportaledellautomobilista.it` → "Quiz per le patenti AM, B, Superiori e CQC" → file **"domande AB italiano 23 04 2025.pdf"**.

---

## 2. Files in this project

| File | What it is |
|---|---|
| `patente_quiz_lista.html` | **THE DELIVERABLE** — single-page list of all 7,166 questions, 25 sections, V/F + Italian + inline sign image. English + hints not yet filled. Open from inside this folder so `img_sign/` loads. |
| `scripts/build_list.py` | Generator for the HTML page. Re-run after data changes: `python3 scripts/build_list.py` |
| `quizPatenteB_updated_2026.json` | **Working dataset** (7,166 Q). 2023 community set + 27 newer questions, kept in the 25-section structure with images. The build script reads THIS file. |
| `quizPatenteB2023.json` | Original 2023 community set (7,139 Q) with `img_sign/` images. Untouched. |
| `listato_AB_MIT_2025-04-23.pdf` | **Official Ministry PDF** (authoritative, with figures), 23-04-2025. Ground truth. |
| `listato_ufficiale_MIT_2025_questions.json` | Official 7,106 questions, flat: `{numero, domanda, risposta}` with official IDs. No sections/images, but clean text + correct answers. |
| `NUOVE_DOMANDE_2026.txt` | The 27 questions added after 2023 (two-wheeler safety / road hazards). |
| `img_sign/` | 413 unique sign/diagram PNGs (reused across ~3,983 questions). Referenced by relative path. |

### Data shapes
- `quizPatenteB_updated_2026.json`: `{ "<section-slug>": { "<subtopic>": [ {"q": str, "a": bool, "img": "/img_sign/NN.png"|""} ] } }`
  - `a: true` = Vero, `a: false` = Falso. `img` may be absent on text-only questions.
- `listato_ufficiale_MIT_2025_questions.json`: `[ {"numero": "21810", "domanda": str, "risposta": "VERO"|"FALSO"} ]`

---

## 3. The page format rules (keep consistent)

- **Italian first** (the exam is in Italian; English is a comprehension aid).
- Per question, in order: **V/F chip** → **Italian text** → **English translation** → **memory hint** → **sign image** (if `img`).
- Visual style: **navy section headers, black body text, light background**, minimal — no flashcards, no quiz UI, no animation. A plain scrollable reference + a clickable section index at top.
- Images: relative path `img_sign/NN.png` (NOT inlined), so the file stays small and works offline from this folder.
- English line is already in the HTML as a hidden `<p class="en" data-empty="1">`; filling it (remove `data-empty`, add text) makes it appear. Same pattern will be used for the hint.

### Hint style guide (when writing hints)
A hint must **force memorization by naming the trap**, not restate the sentence. Patterns that work:
- State the underlying **rule**, then the verdict: e.g. *"Safety distance depends on SPEED, reflexes, road/weather, brakes & load → VERO; never on the engine (power, cc, fuel) or road width → FALSO."*
- For signs: name the **shape/colour → meaning** (e.g. *"Octagon = STOP, the only sign meaning a full halt → VERO"*; *"upside-down red triangle = Give Way"*).
- Flag classic **false-friend traps** (words like *sempre / mai / solo / in ogni caso* often signal FALSO).
- Keep it one short line, English.

---

## 4. Next step — fill in English + hints (the big batch)

The remaining work is generating **English translation + hint for all ~7,100 questions**. This is a large batch best run **in parallel, one job per section** (25 sections), then re-assemble.

**Recommended approach (multi-agent workflow):**
1. For each of the 25 section slugs, take its questions from `quizPatenteB_updated_2026.json`.
2. Have one agent per section produce, for every question, structured output: `{q_it, en, hint}` (preserve order/answers; do NOT change Italian text or answers).
3. Write results back into a new field per question, e.g. add `"en"` and `"hint"` keys → save as `quizPatenteB_translated.json`.
4. Update `scripts/build_list.py` to read those keys and render the English line + a hint line (remove the `data-empty` hiding).
5. Re-run `python3 scripts/build_list.py` → regenerates `patente_quiz_lista.html` with everything.

To resume on another computer, just say:
> "Continue the Patente B project from STUDY_PROJECT.md — run the English + hints batch."

**Smaller-first option:** do one section (e.g. `distanza-di-sicurezza` or `segnali-precedenza`) to approve translation + hint quality before the full run.

---

## 5. Quick commands

```bash
# Regenerate the page after any data change
python3 scripts/build_list.py

# Open the page (macOS) — run from this folder so img_sign/ loads
open patente_quiz_lista.html

# Count questions per section
python3 -c "import json;d=json.load(open('quizPatenteB_updated_2026.json'));[print(k, sum(len(v) for v in s.values())) for k,s in d.items()]"
```

---

## 6. Open decisions / notes
- Working dataset is the 2023 community set + 27 additions. For 100% official text/answers you can instead key off `listato_ufficiale_MIT_2025_questions.json` (has official IDs) — but it lacks section grouping and image links, which the community set provides. Current page favors structure + images.
- The official bank gets small periodic updates; re-check `ilportaledellautomobilista.it` before an exam for the latest listato.
