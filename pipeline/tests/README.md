# Regression gate

```
npm install jsdom          # once
node pipeline/tests/run.js
```

Renders the built `index.html` (and, for `header-parity`, `catalogue.html`) in jsdom at several window sizes and measures the
result. A non-zero exit means do not promote.

Every check here is a mistake that shipped once:

| check | what it measures | the bug it catches |
|---|---|---|
| `default-view` | all 26 markers and 47 concerns drawn, annual panel only | rows silently rolled up on the first screen |
| `rows-and-panels` | one Annual chip, a subset panel names its overlap, edge weights equal, rows clickable | Basic Metabolic Panel rendering an empty group |
| `picker-shortcuts` | annual-only / select-all, and what they do to the rail | a shortcut that dims but does not act |
| `clear-of-the-panel` | widest label's right edge vs the 16px detail-panel gutter, 6 sizes | names sliding under the panel |
| `clear-of-the-rail` | leftmost label vs the rail edge, 5 sizes | names sliding under the rail |
| `equal-thirds` | three equal columns, two equal gaps, titles on one baseline | columns drifting out of proportion |
| `even-spacing` | gap spread within each column ≤ 0.6px | leftover height shared in proportion, not equally |
| `row-padding` | box-top to first baseline, last baseline to box-bottom | padding that grows with the window |
| `no-overlapping-highlights` | highlight boxes never overlap, all 13 panels on | a row pitch shorter than its own highlight |
| `scrolling-canvas` | canvas grows past the window, 68 markers drawn | content hidden instead of scrolled |
| `column-band` | titles live in the fixed band, no inline font sizes in the SVG | headings scrolling away |
| `header-parity` | one 56px header on all four screens, three nav items each, current marked, every bound id intact, in-place route switch | headers drifting apart, or a rebuilt header orphaning the JS that binds to it |
| `legend-and-band` | legend hidden at boot, band opaque and above the canvas | a background painted with an undefined variable |

The window size is stubbed through `clientWidth` / `clientHeight`, so these are
geometry checks, not screenshots — they fail with a number, not a judgement.
