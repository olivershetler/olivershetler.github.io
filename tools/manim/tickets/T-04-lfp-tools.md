# T-04 · Open-Source Tools for LFPs (hfoGUI + SSM)

- **Paper:** Barrett*, Vajram*, Shetler, Aoun, Hussaini. *Open-Source Tools to Analyze Temporal and
  Spatial Properties of Local Field Potentials.* bioRxiv 2024, https://doi.org/10.1101/2024.03.14.584529
- **slug:** `lfp-tools`  ·  **priority:** 4

## Main contribution to illustrate
Two open-source tools read the same local field potential (LFP) signal two ways: **hfoGUI** does
temporal analysis, detecting and scoring high-frequency oscillations such as ripples and fast
ripples; **SSM (Spatial Spectral Mapper)** does spatial analysis, mapping spectral power across
electrode locations. One signal, a time lens and a space lens, both free and open.

## Animation concept (storyboard)
1. A scrolling LFP voltage trace moves across the screen.
2. Zoom into a segment where a high-frequency oscillation burst (a ripple) rides on the slow wave;
   box and label it: "hfoGUI: detect ripples & fast ripples (time)."
3. Transition: the single trace fans out into several stacked traces at different electrode
   positions; a frequency-by-space heatmap builds beside them, lighting up where power concentrates.
   Label: "SSM: spectral power across space."
4. Punchline: "One signal, two lenses: time and space. Open source."
5. Loop: collapse back to the single scrolling trace.

## Technical notes
- LFP trace: sum of a few sines plus noise; inject a short high-frequency burst for the ripple.
- Ripple highlight: a `SurroundingRectangle` + zoom (`ScaleInPlace` / moving camera).
- Heatmap: a grid of colored `Square`s (frequency on one axis, electrode/space on the other),
  colored on the accent-to-background ramp.
- ~10-12s, seamless loop.

## Caption
"Schematic: hfoGUI reads ripples in time; the Spatial Spectral Mapper reads power across space."

## Acceptance
- `public/media/pubs/lfp-tools.mp4` (+ poster) rendered, < ~1.5 MB, muted, loops.
- The "same signal, two lenses (time / space)" idea is legible without narration.
- `publications.ts` entry populated; caption honest.
