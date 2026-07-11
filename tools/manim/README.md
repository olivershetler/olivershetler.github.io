# Per-paper Manim animations

A short (10-14s), silent, looping clip sits below each publication on the site, distilling the
one idea a smart non-specialist would find striking about that paper. This directory holds the
Manim source; only rendered assets ship.

## How it wires into the site

`src/data/publications.ts` already carries an optional `animation` field per entry:

```ts
animation?: { src: string; poster?: string; caption: string }
```

Set `animation.src` to `/media/pubs/<slug>.mp4` (with a `.png` poster and a caption) and the site
renders a captioned `<video>` below that paper automatically. No component or JS changes. The site
stays zero-JS (native `<video>`).

## Ticket-to-paper map

| Ticket | Paper | slug |
|---|---|---|
| T-01 | Beyond Correlation (optimal transport metrics) | `beyond-correlation` |
| T-02 | Impaired Spatial Coding & Neuronal Hyperactivity (MEC, App KI) | `mec-spatial-coding` |
| T-03 | Lateral Entorhinal Cortex Dysfunction | `lec-dysfunction` |
| T-04 | Open-Source Tools for LFPs (hfoGUI + SSM) | `lfp-tools` |
| T-05 | Quantile Formulation under a Qualitative Risk Constraint | `quantile-risk` |

## Shared conventions (all clips)

- **Tooling:** Manim Community edition (Python). `requirements.txt`: `manim`, `numpy`; T-01 also
  uses `pot` (python optimal transport) or a hand-rolled 1D EMD.
- **Output:** `public/media/pubs/<slug>.mp4` (H.264, 1280x720, 30fps, muted) plus a poster frame
  `public/media/pubs/<slug>.png`. Target < ~1.5 MB per clip (short duration + `-q m`).
- **Loop:** design each scene so the end state returns to the start (or clean fade) for a seamless
  `loop`. Clips are muted, `playsinline`, `preload="metadata"`, with `controls` for accessibility.
- **Palette (from the site tokens, so clips match the page):** ink `#1C1A17`, muted `#5C564C`,
  accent `#B0502F`, warm background `#FAF6EF`, rule `#E2D9C8`. Render on the warm background (or
  transparent). A dark-mode render per clip (bg `#191613`, accent `#D97A4C`) is a nice-to-have v2
  via `<source media>`, not required for v1.
- **Honesty:** these are schematic illustrations of the idea, not reproductions of paper figures
  or data. Every caption says so (see each ticket's caption).

## Directory layout

```
tools/manim/
  README.md            # this file
  requirements.txt
  aiqri_palette.py     # shared colors + a base Scene with site styling
  render_all.sh        # renders each scene, copies mp4 + poster into public/media/pubs/
  scenes/
    beyond_correlation.py
    mec_spatial_coding.py
    lec_dysfunction.py
    lfp_tools.py
    quantile_risk.py
  tickets/
    T-01-beyond-correlation.md ... T-05-quantile-risk.md
```

Rendering is a local/offline step. Do NOT add Manim to the GitHub Actions build; render locally
and commit the rendered `public/media/pubs/*` assets so Pages deploys stay fast and dependency-free.

## Recommended build order

1. **T-01 Beyond Correlation** first, as the proof of concept (mass transport is the most naturally
   animative subject, and the flagship paper).
2. **T-05 Quantile risk** next: it is the bridge from the neuroscience record to the AI-risk
   positioning, so it earns its place on this particular site.
3. Then T-02 and T-04. Reassess **T-03** (hardest to make legible) after the others land; it may
   reduce to a simpler schematic or be dropped.

Gate the full set on T-01 landing well on the live page before committing to all five.
