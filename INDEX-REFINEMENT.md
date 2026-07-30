# Refining the index page: from "choose your route" to an atlas of blood

A response to the feedback on `blood-tests-dashboard/index.html`. Every number below is derived from the `#payload` JSON inside that file — the derivation script is in §7 so you can re-run it.

---

## 1. The shift, in one sentence

The landing page today asks a **navigation** question — *"Where do you want to start?"* — and offers two doors that both end in a list. The feedback asks it to make a **claim**: that blood is a structured system, that the structure is mostly unmeasured, and that this page is the map. The refinement is to move the thesis onto the front door and let the routes follow from it, rather than the other way round.

---

## 2. What the data already says about the current landing

These are the numbers the index page is sitting on and not using. Each one is an argument the feedback makes, already true in our own dataset.

| Fact | Value | Which point of the feedback it proves |
|---|---|---|
| Tests in the catalogue | 6,192 | — |
| Tests in a routine annual panel (CBC + CMP + lipid) | **26** | "The most valuable information may be what's missing." A routine checkup measures 0.4% of what is measurable. |
| Tests reachable by *no* symptom in the app | **1,602** (26%) | The symptom route cannot reach a quarter of the atlas. "What data doesn't exist" applies to our own navigation. |
| Entries quoted verbatim from a named source (`v`) | **216** | — |
| Entries written by an AI model from the LOINC name | **5,976** (96.5%) | "What remains unknown" — including what *we* don't yet know. |
| Families with **zero** quoted content | **4 of 17** | Amino acids, therapeutic drug/tox, trace elements, other chemistry are unsurveyed. |
| Infectious disease markers, of which quoted | **1,903 → 5** | The largest family on the map is 0.3% surveyed. |
| Tests carrying a cross-listing to another family | **6** | **The relationship layer does not exist yet.** See §5. |
| Panels with a sourced screening interval (`screen`) | **3** | "What can safely wait" is evidenced for three things only. |

The headline pair — **26 of 6,192** — is the single most important number on the page and it is currently nowhere on it. The landing instead shows *"6,192 tests · 17 body systems"*, which is a volume statistic. That is precisely the framing the Wachter joke is about: more data presented as more data.

---

## 3. Seven changes to the index page

### R1 — Replace the navigation question with the thesis

**Now:** `<h1 class="cxhero">Where do you want to start?</h1>` with tagline *"choose your route."*

**Change to:** a two-line claim built from the real numbers, e.g.

> **There are 6,192 things that can be measured in your blood.**
> A routine annual checkup measures 26 of them. This is a map of the rest — what each marker means, what it sits next to, and what has never been looked at.

**Why:** the feedback's core move is from list to map. The hero is where that gets asserted or lost. Keep the ECG rule and the figure animation; they're doing tonal work. Retire the *"choose your route"* tag.

### R2 — Reframe the stat strip from volume to structure and gaps

**Now:** `cxBig` inside the "Explore all tests" card reads *6,192 tests · 17 body systems*.

**Change to** three stats that are each a gap, not a total:

- **26 of 6,192** measured in a routine annual panel
- **1,602** markers no symptom in this app currently points to
- **4 of 17** families with no source-quoted entry yet

**Why:** "Information reduces uncertainty" only if the number shown is the one that changes a decision. A count of rows doesn't; a coverage ratio does. This also puts the project's no-hallucination rule on the front door instead of two clicks in.

### R3 — Add a third route: start from what you've already had

**Now:** two routes — *how you feel* and *explore all tests*. The notion of tests-you've-had (`state.had`, seeded from the annual panel) exists only inside the condition lens, per `IMPROVEMENT-PLAN.md` §3.3.

**Change to:** promote it to a landing route — *"Start from the bloodwork you've already had."* One click for *"I've had a standard annual panel"* seeds the 26 baseline markers; the output is a **gap map**, not a test list: which families are complete, which are partial, which have never been touched.

**Why:** this is the feedback's strongest single claim — *"missing data is itself clinical information"* — and it currently has no entry point. It is also the cheapest route to build, because the seeding logic and the panel↔test links (`panels[].linked`, `b` flag) already exist.

### R4 — Rename and re-promise the catalogue route

**Now:** *"Explore all tests"* → a 6,192-row table grouped by body system.

**Change to:** *"Open the atlas"* → land on the **17 families as a map**, sized by how much sits inside each and shaded by how much of it you've had or how much is sourced. The table stays, one level down, as the way to read a family in detail.

**Why:** the table is a good instrument and shouldn't be cut. But a route whose promise is "here are 6,192 rows" is the isolated-planets view. The route should promise the solar system and deliver the planet list inside it.

### R5 — Make the six questions the page's spine

Put the feedback's six questions on the page verbatim as a strip of cards, each labelled with where it currently stands:

| Question | Surface | Status |
|---|---|---|
| What do we know? | Marker entry, family view | built |
| What don't we know? | Gap map, source-coverage view | **not built** |
| What's most likely happening? | Condition lens, miniDx | prototype (`condition-lens.html`) |
| What's worth measuring next? | Path to Dx | prototype |
| What can safely wait? | Screening intervals (`screen`) | 3 panels only |
| How has this changed over time? | Trends | **not built** |

**Why:** it converts an abstract framing into navigation, and it is honest about the two-thirds that don't exist yet. A landing page that names its own gaps is consistent with the argument it is making.

### R6 — Make the map illustration real instead of decorative

**Now:** the `vizmap` SVG on the "how you feel" card is hand-drawn with invented example nodes (*always tired → anemia → CBC*).

**Change to:** generate the preview from the payload at load — 17 family nodes sized by their true counts (Infectious disease 1,903; Other blood chemistry 688; Therapeutic drug 594; Hematology 554; … Lab-developed 49), filled where a routine panel touches them, hollow where it doesn't.

**Why:** the illustration is the only place the landing page shows structure, and right now the structure it shows is fictional. Generated from data it cannot drift from the truth, and the hollow majority *is* the argument.

### R7 — Say what the atlas doesn't know, on the landing

Add a short honesty band above the footnote: 216 entries quoted verbatim from a named authority (MedlinePlus and MedlinePlus Genetics (NIH), NCBI, the National Cancer Institute, and the ARUP / Mayo / Labcorp / Quest test directories); 5,976 written by a model from the official LOINC name and category, every one linking to its LOINC record. Four families have no quoted entry yet.

**Why:** the project rule is quote-don't-rephrase and no hallucination. Surfacing the ratio makes the same point the product makes about patients — an unmeasured region is information, not an embarrassment — and it pre-empts the obvious critique from a clinician reader.

---

## 4. What to cut

The *"choose your route"* tag, the volume stat pair, and the fictional `vizmap` nodes. Nothing else — the figure, the ECG, the drifting gradients, the footnote disclaimer and feedback address all survive intact.

---

## 5. The honest blocker: there is no relationship layer yet

The feedback asks for *"what other markers surround a result"* and *"how one abnormal finding ripples through the rest of the system."* Our data cannot answer that today:

- **6** of 6,192 tests carry any cross-family link (`x`).
- The only "these tests belong together" sets are the **3** annual panels.
- There are no marker→marker edges: no reflex testing (low MCV → ferritin), no shared-mechanism links, no confirm-after-screen ordering outside the one hand-authored condition in `condition-lens.html`.

So the index page can honestly *promise* the map, and the family-level map in R4/R6 is real and buildable now. But a marker-level ripple view would be drawing edges that don't exist. The next data pass needs two small additions alongside `tests`:

```json
"sets":  [{ "id":"iron-studies", "label":"Iron studies", "members":["ferritin","iron","tibc","tsat"],
            "why":"ordered together to assess iron stores", "src":{...} }],
"edges": [{ "from":"mcv", "to":"ferritin", "kind":"reflex",
            "when":"low", "why":"a low MCV prompts iron studies", "src":{...} }]
```

Same sourcing discipline as `tests` — each set and edge carries a `quoted` or `reasoned` badge. This is the piece that turns the atlas from a taxonomy into a network, and it is the right thing to scope next.

---

## 6. Suggested order

**Now, copy and layout only, no new data:** R1, R2, R5, R7. These are edits to the existing landing markup and can ship this week.

**Next, uses data we already have:** R3 (gap route, reuses `b` and `panels[].linked`) and R6 (generated family map, reuses `groups` + `g` counts).

**After the data pass:** R4's full atlas and any marker-level ripple, gated on `sets` and `edges` from §5.

---

## 7. Reproducing the numbers

```python
import json, re
from collections import Counter
s = open('index.html', encoding='utf8').read()
i = s.index('id="payload" type="application/json">') + len('id="payload" type="application/json">')
d = json.loads(s[i:s.index('</script>', i)])
T = d['tests']
print(len(T))                                  # 6192
print(sum(1 for t in T if t.get('b')))         # 26   in a routine annual panel
print(sum(1 for t in T if not t.get('k')))     # 1602 reachable by no symptom
print(sum(1 for t in T if t.get('v')))         # 216  source-quoted  (v is the quoted flag)
print(sum(1 for t in T if t.get('x')))         # 6    cross-listed
print(Counter(d['groups'][t['g']] for t in T if t.get('b')))
# Counter({'Chemistry / Metabolic': 13, 'Hematology': 8, 'Lipids': 5}) — 3 of 17 families
```

Two field notes for whoever implements this: the quoted/AI badge is driven by **`v`**, not `sr` (`sr` is the sex-specific-range flag, 406 rows, matching `meta.sexrange`). And `meta.quoted` = 216 agrees exactly with the `v` count, so no reconciliation is needed.

---

## 8. Status — implemented in `index-v2.html`

All seven are built. `index-v2.html` sits alongside `index.html` for side-by-side review; swap when you're happy.

| | Change | Where it lands |
|---|---|---|
| R1 | Hero states the thesis, numbers injected at run time | landing |
| R2 | Three gap stats replace the volume pair | landing |
| R3 | **New** gap-map screen (`#cxGaps`) — panel toggles, marker search, per-family coverage, `localStorage` persistence | new route |
| R4 | **New** atlas screen (`#cxAtlas`) — 17 family cards, shade by panel/source coverage, sort by size/least-covered/A–Z, each opens that family in the existing table | new route, table demoted one level |
| R5 | Six-question spine with honest status pills | landing |
| R6 | Family map generated by deterministic circle packing from `groups` + `tests[].g` + `tests[].b`; viewBox auto-trimmed; **no edges drawn** | landing + atlas |
| R7 | Honesty band, source names read out of `tests[].qs` | landing |

Notes for review:

- **Nothing is hardcoded.** Every figure on the page is computed from the payload at load. If the dataset changes, the copy changes with it — including "3 of 17 families are lit" and the iron-studies callout.
- **No fake edges.** The map draws circles only, with a visible line of copy explaining that 6 of 6,192 markers carry a link to another family, "so this map shows regions, not roads." The atlas screen repeats it as a scoped caveat.
- **The gap map carries a clinical caveat**: *"This is a map, not a to-do list."* A large share of the 6,192 are infection-specific assays, drug levels and specialist panels that only make sense given a particular question. An empty family is worth knowing about; it does not mean something was missed.
- Existing routes, the condition lens, the table, the browser back button and the URL hashes (`#atlas`, `#gaps` added) all still work.
- Regenerate from a changed `index.html` with `pipeline/build_v2.py` — it asserts on every anchor string, so it fails loudly rather than silently mis-patching.

---

## Sources

- Data and current markup: `blood-tests-dashboard/index.html` (payload at line 923; landing markup from line 569)
- Prior plan this builds on: `blood-tests-dashboard/IMPROVEMENT-PLAN.md`
- Working condition prototype: `blood-tests-dashboard/condition-lens.html`
- Panel definitions and screening intervals are quoted in-payload from MedlinePlus (NIH), e.g. [Complete Blood Count (CBC)](https://medlineplus.gov/lab-tests/complete-blood-count-cbc/) and [Cholesterol Levels](https://medlineplus.gov/lab-tests/cholesterol-levels/)
