# From "concern → test list" to "condition → path to Dx"

**A plan for making the blood-tests dashboard show ripple effects, missing-signal tests, a diagnostic path, and a provisional miniDx.**

Prepared for the *What is your blood telling you?* prototype (`blood-tests-dashboard/index.html`).
Companion reference build: `condition-lens.html` (iron-deficiency anemia, working end-to-end).

---

## 1. What the prototype does today, and why it can't reach the goal

The current dashboard is a **concern-in, test-list-out** engine. The user picks concerns (`fatigue`, `hair loss`, …); `relevance()` keyword-scores all 6,192 tests against those concerns via each test's `k` (concern-index) array; `compute()` ranks and de-duplicates them; and four panels render the result — a rollup stat strip, callouts, "worth asking your doctor about," and annual-panel coverage.

It is a good **discovery** tool. But the goal you described is a different shape of problem, and four things the goal needs simply do not exist in the data model or the UI:

| Goal you described | What's missing today |
|---|---|
| "the connections, the ripple effects of a **condition**" | There is no *condition* entity at all. The graph only knows `concern ↔ test`. A condition (a named diagnosis like iron-deficiency anemia) that radiates out to *symptoms*, *systems*, and *markers* is not modeled. |
| "what bloodwork I **haven't had** that would show a signal" | There is no notion of *tests the user has already had*. Every test is treated as un-done. The app can't tell you what's missing because it doesn't know what you have. |
| "show a **path toward Dx**" | Tests are ranked by keyword relevance, not sequenced. There is no "screen first, then confirm" ordering, and no link from a screening hint to its confirmatory follow-up. |
| "have that **miniDx** there if you had that blood work done" | There is no interpretation layer. The app never says "this *pattern* of results points to X." It stops at "here are topically related tests." |

The good news: the existing test catalogue, the annual-panel coverage logic, and the source-quoting/`ai-generated` badge system are exactly the primitives the new model needs. This is an **additive** change, not a rewrite.

---

## 2. The one idea that ties all four goals together

Add a **Condition** as a first-class object that sits *above* the test catalogue and *below* the concern chips:

```
concern (symptom)  →  CONDITION (diagnosis)  →  markers (tests)  →  miniDx (interpretation)
   "I'm tired"          "iron-deficiency          ferritin,           "low Hgb + low MCV +
                          anemia"                  hemoglobin, MCV…     low ferritin →
                                                                       consistent with IDA"
```

Everything the goal asks for falls out of this one addition:

- **Ripple map** = drawing the condition's edges outward to its symptoms *and* its markers.
- **Missing-signal tests** = the condition's marker set, minus the tests the user marks as "already had."
- **Path to Dx** = the condition's markers ordered into `screen → confirm` steps.
- **MiniDx** = a rule that fires once the path's tests exist, reading their pattern against sourced thresholds.

---

## 3. Data model to add

### 3.1 New `conditions` array

Add a `conditions` array to the JSON payload, parallel to `concerns`. Each condition:

```json
{
  "id": "ida",
  "label": "Iron-deficiency anemia",
  "cgrp": "Energy & blood",
  "oneLiner": "Not enough iron to build healthy red blood cells — the most common anemia.",
  "concerns": ["fatigue", "cold-intolerance", "hair-nails", "shortness-of-breath"],
  "ripple": {
    "symptoms": ["Fatigue", "Dizziness or lightheadedness", "Cold hands and feet", "Pale skin", "Shortness of breath", "Restless legs"],
    "systems": ["Energy & blood", "Heart & circulation", "Brain & mood"],
    "untreated": "fatigue, headaches, restless legs syndrome, heart problems, pregnancy complications, and developmental delays in children"
  },
  "path": [
    { "step": 1, "role": "screen",  "testKeys": ["hemoglobin","hematocrit","mcv"], "inPanel": true,
      "signal": "Low hemoglobin/hematocrit with a low MCV (small red cells) is the first hint." },
    { "step": 2, "role": "confirm", "testKeys": ["ferritin","iron","tibc"],        "inPanel": false,
      "signal": "Low ferritin is the most specific confirmation of depleted iron stores." }
  ],
  "minidx": {
    "rule": "hemoglobin=low AND mcv=low AND ferritin=low",
    "reads": {
      "consistent": "This pattern — low hemoglobin, small red cells, and low iron stores — is the classic picture of iron-deficiency anemia.",
      "partial": "Some signals point toward iron deficiency, but the confirming test (ferritin) is still missing.",
      "against": "These results do not fit an iron-deficiency pattern; the tiredness likely has another cause worth exploring."
    }
  },
  "src": [ /* array of {quote, source, url, kind:"quoted"|"inference"} — see §5 */ ]
}
```

### 3.2 Link markers to real catalogue rows

`testKeys` are stable analyte slugs (`ferritin`, `mcv`, …). At load, resolve each to its catalogue index by matching the analyte prefix already computed in `compute()` (the text before the first `[` in the LOINC name). This reuses existing de-duplication logic — no new matching engine.

### 3.3 New user state: "tests I've had"

Extend `state` with one set and one map:

```js
state.had   = new Set();              // analyte slugs the user has had done
state.result= {};                     // slug -> 'low' | 'normal' | 'high' | 'unknown'
```

Persist both to `localStorage` (the table view already uses `localStorage`, so the pattern exists). Seed `state.had` from the annual panel by default — a one-click "I had a standard annual checkup" pre-checks CBC/CMP/lipid components, which is what makes the *"you've had the CBC but not the ferritin"* insight land immediately.

---

## 4. UI changes (each maps to one goal)

**A. Condition lens (new mode).** Add a third view toggle beside *Guided / All tests*: **Conditions**. Picking a condition opens the lens. This keeps the discovery tool intact and adds the diagnostic tool alongside it.

**B. Ripple diagram (goal 1).** Condition at the centre; edges to symptom nodes on one side and marker nodes on the other. Marker nodes are colour-coded by whether you've had them (done / not done). This is the "connections and ripple effects" picture, and it doubles as the missing-signal view.

**C. "Have you had this?" checklist (goal 2).** Each marker row has a *had it / haven't* toggle and an optional result chip (low / normal / high). Markers you haven't had are visually pulled forward with a "signal you haven't tested for" label. Because ferritin sits *outside* the annual panel, it surfaces here automatically for anyone who's only had routine bloodwork.

**D. Path to Dx (goal 3).** A numbered `screen → confirm` track. Step 1 (CBC components, in-panel) and Step 2 (ferritin/iron studies, out-of-panel) each show their signal, source, and your status. The step you're missing is highlighted as the next action.

**E. MiniDx card (goal 4).** Locked until the path's tests are marked "had." Locked state shows exactly what's needed to unlock it ("Add a ferritin result"). Unlocked, it reads your pattern against the rule and shows *consistent / partial / against*, every clause quoted and cited, wrapped in a "not a diagnosis" disclaimer.

---

## 5. Sourcing and honesty (per project rule: no hallucination, quote don't rephrase)

Every condition carries a `src` array. Two `kind`s, rendered with different badges — reusing the existing `source-quoted` vs `ai-generated` visual language:

- **`quoted`** — verbatim text from a named authority, with a verify link. Used for symptoms, the test list, thresholds, and untreated complications.
- **`inference`** — clinical-common-knowledge glue that has no single clean quotable source (e.g. the *sequencing* of screen-before-confirm, and the miniDx *combination logic*). Shown behind a visible **"reasoned, not quoted"** badge so the user can tell curated fact from connective tissue.

### Sources used for the iron-deficiency-anemia reference build

> "To help diagnose iron-deficiency anemia, your doctor will order a blood test to check your complete blood count (CBC), hemoglobin levels, blood iron levels, and ferritin levels."
> — National Heart, Lung, and Blood Institute (NHLBI), *Iron-Deficiency Anemia*. https://www.nhlbi.nih.gov/health/anemia/iron-deficiency-anemia

> "More serious iron-deficiency anemia may cause common symptoms of anemia, such as tiredness, shortness of breath, or chest pain. Other symptoms include: Fatigue; Dizziness or lightheadedness; Cold hands and feet; Pale skin."
> — NHLBI, *Iron-Deficiency Anemia*. https://www.nhlbi.nih.gov/health/anemia/iron-deficiency-anemia

> "In iron-deficiency anemia, blood levels of iron will be low, or less than 10 micromoles per liter (µmol/L) … Levels of ferritin will also be low, or less than 10 micrograms per liter (µg/L) … Normal levels are 40 to 300 for men and 20 to 200 for women." (figure text)
> — NHLBI, *Iron-Deficiency Anemia*. https://www.nhlbi.nih.gov/health/anemia/iron-deficiency-anemia

> "Undiagnosed or untreated iron-deficiency anemia may cause serious complications such as fatigue, headaches, restless legs syndrome, heart problems, pregnancy complications, and developmental delays in children."
> — NHLBI, *Iron-Deficiency Anemia*. https://www.nhlbi.nih.gov/health/anemia/iron-deficiency-anemia

> "A ferritin blood test measures the level of ferritin in your blood. Ferritin is a protein that binds to iron and stores it in your body."
> — MedlinePlus (NIH/NLM), *Ferritin Blood Test*. https://medlineplus.gov/lab-tests/ferritin-blood-test/

> "Lower than normal ferritin levels may mean you have iron deficiency anemia, or another condition related to low iron levels."
> — MedlinePlus (NIH/NLM), *Ferritin Blood Test*. https://medlineplus.gov/lab-tests/ferritin-blood-test/

> "You may also need this test if the results of other blood tests show that you have low levels of hematocrit … or hemoglobin …"
> — MedlinePlus (NIH/NLM), *Ferritin Blood Test*. https://medlineplus.gov/lab-tests/ferritin-blood-test/

**Flagged as inference (reasoned, not quoted)** in the build: that the CBC is the *screening* step and ferritin the *confirming* step (an ordering, not a quote); and that "low Hgb + low MCV + low ferritin together" reads as *consistent with* IDA (a combination of the individually-sourced facts above). Both are standard clinical reasoning, but no single MedlinePlus/NHLBI sentence states them as one rule, so they are labelled.

A note on thresholds: different bodies publish different ferritin cut-offs (NHLBI's figure uses <10–20 µg/L; WHO/CDC use <15 µg/L; the American Society of Hematology proposes ≤30 µg/L). The reference build quotes NHLBI and states plainly that cut-offs vary — it never presents a single number as *the* line.

---

## 6. Sequencing — how to roll this out without destabilising the file

1. **Reference build first (done):** `condition-lens.html`, iron-deficiency anemia, standalone, styled to match. React to it before anything touches `index.html`. *(This is the file shipped alongside this plan.)*
2. **Fold the lens into `index.html`** as the third view, reading a small `conditions` array added to the payload. No change to the existing concern engine.
3. **Author 6–10 more conditions** using the same schema and the same source discipline — start with ones whose screening hint is in the annual panel but whose confirmation is outside it (hypothyroidism: TSH → free T4 / TPO antibodies; type 2 diabetes: glucose → HbA1c; B12 deficiency: CBC/MCV → B12/MMA). Those give the strongest "you've had the hint, not the confirm" story.
4. **Add result-history import** later if desired (upload a past lab PDF / manual entry) to auto-fill `state.had` and `state.result`.

---

## 7. What the reference build demonstrates

`condition-lens.html` implements the full loop for one condition: the ripple diagram, the had-it / haven't checklist with the annual-panel pre-seed, the two-step path to Dx, and the miniDx card that stays locked until you supply results and then reads your pattern against the sourced thresholds — with quoted vs. reasoned clearly separated throughout. It is the thing to react to before scaling.
