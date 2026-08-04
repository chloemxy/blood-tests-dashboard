# Design rules

Standing rules for this project. They apply to every build, at every level of
the design — not just the outer layout.

---

## 1. The 8px system — everywhere

**Every spacing value is a multiple of 8.** Padding, margin, gap, row height,
panel height, column width, offsets. 4px is permitted as a deliberate half-step
for tight inline cases (a badge's vertical padding, a 4px label gap); anything
else is a mistake.

Not on the system, and correctly so:

- **1px borders and rules.** A hairline is a hairline.
- **Font sizes and line-heights.** Type is sized for reading, not for the grid.
  A 24px row can carry 11px text.
- **Border radii.** Follow the shape, not the grid.
- **Percentages and fractions** used for proportional layout.

Reference values in use:

| | |
|---|---|
| Base unit | 8px |
| Panel gap / outer margin | 16px |
| Panel padding | 16px |
| Section header padding | 16px 16px 8px |
| List row height | 32px |
| Control height | 24px |
| Control inner padding | 0 8px |
| Chip padding | 4px 8px |
| Map row pitch | 24px |
| Left rail width | 320px (8×40) |
| Toggle column | 96px (8×12) |
| Detail panel width | 344px |
| Header height | 56px |
| Footer height | 72px |

Audit the CSS before shipping. `pipeline/build_v3.py` builds are checked with:

```python
# flags any padding/margin/gap/height that is not a multiple of 8 (or 4)
import re
for m in re.finditer(r'([\w.#>\-\s,:\[\]()="]+)\{([^}]*)\}', css):
    for pm in re.finditer(r'\b(padding|margin|gap|height|min-height|max-height)\s*:\s*([^;]+)', m.group(2)):
        for num in re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)px', pm.group(2)):
            n = float(num)
            if n and n % 8 and n % 4:
                print('off-grid:', m.group(1), pm.group(1), num)
```

---

## 2. Nothing shifts under the cursor

Interacting with the page must not move anything already on screen.

- Column and panel positions are constants, not functions of state.
- Panels hold their size; content that could overflow scrolls **inside its own
  box** rather than growing the box.
- Scroll areas reserve their gutter (`overflow-y: scroll; scrollbar-gutter: stable`)
  so a scrollbar appearing never nudges content sideways.
- Layout is a pure function of state and window size — same inputs, same pixels.

The one deliberate exception: a section explicitly labelled as expandable, where
the user asked for the growth.

## 3. No ambient motion

Nothing drifts, floats, breathes or animates on its own. Transitions are for
colour and opacity on direct interaction, and are short. A diagram that moves is
harder to read than one that does not.

## 4. Reveal, don't clip

**Names are shown in full.** A label wraps onto as many rows as it needs; it is
never cut with an ellipsis while there is a way to wrap it. Truncation is a last
resort for when the container genuinely cannot hold the text at the minimum
type size, and even then the full name stays in the tooltip.

**Padding is constant regardless of line count.** An entry with a three-line
name carries exactly the same space above and below as a one-line one — the row
grows, the padding does not change. Rows in a list may therefore have different
heights; that is correct.

If a section's job is to explain something, it grows to fit its content rather
than scrolling or truncating it. Long *lists* may be capped with an explicit
expander that states the true total. Truncation without a stated count is never
acceptable.

**Long lists are grouped, not cut.** Past about ten entries, group by a
meaningful axis, show the commonly-relevant members by default, and put the true
count on every group header so nothing is hidden without being counted.

## 5. Sourcing

- No hallucination. Every claim carries a credible reference with a link.
- Quote the source verbatim; do not paraphrase it.
- Say what is quoted and what is generated, on the thing itself.
- State true totals even when showing a subset.

## 6. Style

Follow `goinvo-style-guide.md`. Palette, type and tone come from there.
