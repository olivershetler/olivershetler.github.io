# T-03 · Lateral Entorhinal Cortex Dysfunction

- **Paper:** Raghuraman, Aoun, Herman, Shetler, Nahmani, Hussaini. *Lateral Entorhinal Cortex
  Dysfunction in Alzheimer's Disease Mice.* bioRxiv 2024, https://doi.org/10.1101/2024.04.15.589589
- **slug:** `lec-dysfunction`  ·  **priority:** 5 (hardest to make legible; reassess or simplify)

## Main contribution to illustrate
The lateral entorhinal cortex (LEC) encodes objects and their lingering memory traces: "object
cells" fire precisely when the animal is near an object, and "trace cells" keep firing at the spot
where an object used to be. In the EC-App/Tau Alzheimer's model, these LEC neurons become
hyperactive with low information content and high sparsity (poor firing fidelity): object and trace
cells fire less precisely, so the brain's tag for "what was here" blurs.

## Animation concept (storyboard)
1. Arena with a small object icon at one location.
2. Healthy LEC "object cell": as the mouse approaches the object, the cell fires a tight, precise
   burst localized to the object. Remove the object and a faint "trace" tag persists at its old
   spot (trace cell).
3. Disease panel (same setup): the cell fires diffusely and too often (hyperactive), not locked to
   the object; the memory trace is smeared or absent.
4. Punchline: "The lateral entorhinal cortex tags objects and their traces. In disease, the tag
   blurs."
5. Loop.

## Technical notes
- Object: a simple icon (`SVGMobject` or a labeled shape).
- Precise firing: a tight cluster of `Dot`s at the object; imprecise firing: a wide, dense,
  jittered cloud with higher baseline (hyperactivity).
- Trace: a low-opacity residual cluster that lingers after the object is removed (healthy) vs none
  (disease).
- Legibility risk is real: keep labels explicit ("object cell", "memory trace"). If it does not
  read cleanly, fall back to a two-panel static-to-animated schematic, or drop this clip for v1.
- ~12s, seamless loop.

## Caption
"Schematic: the lateral entorhinal cortex tags objects; in disease the tag blurs."

## Acceptance
- `public/media/pubs/lec-dysfunction.mp4` (+ poster) rendered, < ~1.5 MB, muted, loops.
- A non-specialist can see "precise, object-locked firing" degrade into "diffuse, hyperactive
  firing" and the memory trace fade.
- `publications.ts` entry populated; caption honest. OR: explicitly deferred with a note in the
  README if legibility cannot be reached.
