# T-05 · Quantile Formulation under a Qualitative Risk Constraint  (2D, REVISED)

- **Paper:** Vazquez-Abad, Shetler, Soto. *Quantile Formulation for Optimization Under a Qualitative
  Risk Constraint.* IEEE Conference on Decision and Control (CDC), 2022.
  https://doi.org/10.1109/CDC51059.2022.9992955
- **slug:** `quantile-risk`  ·  **priority:** 2 (the bridge to the AI-risk positioning)

## Why the first version was wrong
The first cut put a 1D tail against a vertical line. That is the "trivial" 1D case the authors
explicitly criticize, and it hides that the real constraint is a **probability inequality**, not a
hard line in outcome space. Redo it in 2D.

## Main contribution to illustrate (corrected)
The paper handles optimization under a **chance constraint**: keep the system safe with high
probability, `P(outcome leaves the safe region) <= alpha`. Differentiating a probability directly is
pathological, so the constraint is reformulated as a **quantile** (a smooth sample-average
approximation), which behaves under gradient methods. Geometrically, for a Gaussian outcome the
constraint says the `(1 - alpha)` confidence ellipse must sit inside the safe region. The optimizer
improves its objective by pushing toward the operating limit while keeping that ellipse inside,
riding the boundary rather than crossing it.

## Animation concept (2D, storyboard)
1. A 2D outcome plane. Shade a **safe region** below/left of an operating-limit boundary (a straight
   `boundary` line in ACCENT). Faint axes; label "outcome (2D)" and "safe region".
2. Draw the uncertain outcome as a **2D Gaussian**: a mean `Dot`, a bold `(1 - alpha)` confidence
   `Ellipse`, and one or two fainter concentric density ellipses. Label the ellipse
   "confidence ellipse: holds 1 - alpha of outcomes".
3. An `objective` arrow points toward the boundary (improving direction = operate nearer the limit).
4. **Beat A, "ignore the noise":** slide the mean up to the boundary line itself. The ellipse now
   straddles the line; shade the part past the boundary red and label
   "P(unsafe) ~ 50%, over risk budget alpha". Hold, then flash/mark it as infeasible.
5. **Reset. Beat B, "quantile constraint":** slide the mean up but STOP when the ellipse is exactly
   tangent to the boundary. Show the gap between the mean and the boundary as the quantile margin;
   label "P(unsafe) = alpha, feasible". Then slide the mean ALONG the boundary (ellipse stays
   tangent) to the best objective point.
6. Punchline: "The risk constraint is a probability. Optimize by keeping the confidence ellipse
   inside the safe region."
7. Loop (return mean to start, ellipse fully inside).

## Technical notes
- Constraint math for a half-plane `a . x <= b` and Gaussian `N(mu, Sigma)`:
  feasible iff `a . mu + z_{1-alpha} * sqrt(a^T Sigma a) <= b`. The tangency in beat B is this
  equality. Use a fixed `Sigma` (e.g. a tilted ellipse) and move only `mu`; compute the tangent mean
  position directly from that formula so the ellipse genuinely kisses the line.
- Confidence ellipse: `Ellipse` scaled to the chosen `1 - alpha` (e.g. ~90%, radius factor from the
  chi-square-2 quantile, or just a fixed visually-clear size; this is schematic).
- Overhang shading (beat A): intersect the ellipse with the unsafe half-plane; approximate with a
  clipped `Polygon`/`Intersection` or a red-tinted `Ellipse` masked by the boundary. Keep it simple
  and legible over exact.
- No LaTeX: all labels via `Text` ("alpha", "P(unsafe)", "1 - alpha", "objective"). Use ACCENT for
  the boundary and the key ellipse, INK/MUTED for context, red (`#B0502F` is fine, or a deeper red
  like `#A33` ) for the violation.
- ~13-15s, seamless loop.

## Caption (publications.ts animation.caption)
"Schematic: an optimizer improves its objective while keeping the 2D outcome distribution's
confidence ellipse inside the risk boundary (probability of failure within budget)."

## Acceptance
- `public/media/pubs/quantile-risk.mp4` (+ `.png` poster) re-rendered, < ~1.5 MB, muted, loops.
- The contrast reads without audio: mean-on-boundary (ellipse straddles, ~50% unsafe) vs
  ellipse-tangent (feasible, margin = the quantile), then riding the boundary to the optimum.
- It is unmistakably 2D and the constraint is clearly a probability inequality, not a hard line.
- `publications.ts` caption updated to the new caption above.
