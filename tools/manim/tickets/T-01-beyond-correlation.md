# T-01 · Beyond Correlation (optimal transport metrics)

- **Paper:** Aoun*, Shetler*, Raghuraman, Rodriguez, Hussaini. *Beyond Correlation: Optimal
  Transport Metrics for Characterizing Representational Stability and Remapping in Neurons Encoding
  Spatial Memory.* Frontiers in Cellular Neuroscience, 2024. https://doi.org/10.3389/fncel.2023.1273283
- **slug:** `beyond-correlation`  ·  **priority:** 1 (proof of concept)  ·  **Oliver is co-first author**

## Main contribution to illustrate
A neuron's spatial firing map ("ratemap") can change in ways Pearson correlation cannot see. When
two firing fields stop overlapping, correlation collapses to ~0 and stays there, losing all
resolution. The Earth Mover's Distance (optimal transport) keeps measuring: it reports the cost of
moving one firing distribution onto the other, so it distinguishes a small shift from a large one
even when the fields are disjoint. This is the paper's headline: transport metrics are strictly
more informative than correlation for remapping.

## Animation concept (storyboard)
1. A square arena. A warm Gaussian blob switches on: "ratemap — where a place cell fires."
2. A second identical blob (field B) appears on top of field A. Two live readouts: `Pearson r`
   and `EMD`.
3. A `ValueTracker` slides field B steadily away from field A.
4. As overlap falls, `Pearson r` drops and pins near 0 the moment the fields separate (freeze it,
   grey it out: "correlation is blind here"). `EMD` rises smoothly and keeps rising with distance.
5. Draw the EMD as literal earth-moving: small arrows/particles carry mass from A's location to
   B's, annotated `cost = mass x distance`.
6. Hold on the punchline: "Correlation stops measuring where the fields separate. Optimal transport
   keeps going."
7. Loop: return field B to full overlap.

## Technical notes
- Blob: 2D Gaussian rendered as a low-opacity `DotCloud`/`ImageMobject`, or nested faded circles.
- Metrics: `DecimalNumber` bound to the separation tracker. EMD in 2D of two translated identical
  masses is just the translation distance; compute directly. Pearson r of the two sampled ratemaps
  drops to ~0 once supports are disjoint.
- Transport: animate `Arrow`s or streaming dots from A to B, length encoding cost.
- ~12-14s, seamless loop.

## Caption (goes in publications.ts animation.caption)
"Schematic: optimal transport distance keeps measuring spatial change where correlation goes blind."

## Acceptance
- `public/media/pubs/beyond-correlation.mp4` (+ `.webp` poster) rendered, < ~1.5 MB, muted, loops.
- Pearson-vs-EMD divergence is legible in under 10 seconds to a non-specialist.
- `publications.ts` entry for the Frontiers paper has `animation` populated; clip renders below it.
- Caption present and honest (schematic, not paper data).
