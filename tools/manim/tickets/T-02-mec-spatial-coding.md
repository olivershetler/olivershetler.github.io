# T-02 · Impaired Spatial Coding & Neuronal Hyperactivity (MEC, App KI)

- **Paper:** Rodriguez, Rothenberg, Shetler, Aoun, Posani, Vajram, Tedesco, Fusi, Hussaini.
  *Impaired Spatial Coding and Neuronal Hyperactivity in the Medial Entorhinal Cortex of Aged
  AppNL-G-F Mice.* bioRxiv 2024, https://doi.org/10.1101/2024.11.26.624990
- **NOTE:** now published in **Cell Reports, June 2026** (S2211-1247(26)00583-8). Consider updating
  the site citation to the peer-reviewed version and marking it peer-reviewed.
- **slug:** `mec-spatial-coding`  ·  **priority:** 3

## Main contribution to illustrate
In aged App knock-in Alzheimer's-model mice, the medial entorhinal cortex map degrades: grid-cell
spatial periodicity is disrupted, border-cell preferences are unstable across sessions, and spatial
information scores fall, so position and speed can no longer be decoded well. At the same time the
network shows mild hyperactivity (driven by narrow-spiking putative interneurons). Two things at
once: the map breaks down and the noise floor rises.

## Animation concept (storyboard)
1. Split screen: "Healthy" | "Alzheimer's model (App KI)". Identical square arenas.
2. A simulated mouse trajectory scribbles across both arenas simultaneously.
3. Healthy side: firing dots deposit into a clean hexagonal grid pattern (a grid cell). A "spatial
   information" meter reads high; baseline firing moderate.
4. Disease side: firing dots scatter, the hexagonal periodicity dissolves, the meter reads low, and
   the background fires more densely (hyperactivity) with an elevated rate readout.
5. Punchline: "Amyloid pathology degrades the entorhinal map and raises the noise floor."
6. Loop: clear both arenas and rerun the trajectory.

## Technical notes
- Trajectory: a smooth random-walk `VMobject` path, shared across both panels.
- Grid firing: place `Dot`s at a hexagonal lattice intersected with the path (healthy), vs the same
  count of dots with heavy positional jitter and no lattice (disease).
- Meters: two vertical bars (`Rectangle` fill via `ValueTracker`), one per side.
- Hyperactivity: higher dot density / faster deposition on the disease side.
- ~12s, seamless loop.

## Caption
"Schematic: in the Alzheimer's model, the entorhinal grid degrades and baseline firing rises."

## Acceptance
- `public/media/pubs/mec-spatial-coding.mp4` (+ poster) rendered, < ~1.5 MB, muted, loops.
- Healthy hexagonal grid vs degraded scatter is obvious side by side; hyperactivity readable.
- `publications.ts` entry populated; caption honest.
