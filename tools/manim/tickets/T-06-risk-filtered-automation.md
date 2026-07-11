# T-06 · Risk-Filtered Claim Automation (ML Week talk)

- **Source:** Oliver Shetler, *From Medical Codes to Cash and Coverage: Risk-Filtered Insurance
  Claims Automation*, Machine Learning Week US 2026. Grounded in his own simulation code
  (charge-line denial model, threshold sweep, cost model, headcount ROI).
- **slug:** `risk-filtered-automation`  ·  placement: under the ML Week talk in the Speaking section
  (NOT a publication).

## STEALTH: keep it generic
Do NOT use any of these terms or metaphors anywhere in the clip: "Value Atlas", "Fordism",
"proximal decision", "lock and key", "keystone", "key juncture", "quality planning", "unit of
analysis". Use only plain language: denial risk, risk score, automate, human review, threshold,
cost per claim, failure rate, risk-stratified routing.

## Core idea to illustrate
Score every claim by predicted denial risk. Automate the low-risk majority cheaply; route the
high-risk tail to human coders. There is a cost-minimizing threshold: too much automation lets
denials slip (rework cost), too little wastes money on human review. At the optimal cutoff,
risk-stratified routing costs roughly half of all-human review while holding the failure rate at the
human baseline. That is the design pattern for safe partial automation in high-stakes workflows.

## Grounding numbers (schematic, from the sim)
- AI cost ~ $0.10/claim; human review ~ $5.00/claim; human baseline failure ~ 5%.
- Risk-stratified routing ~ 49% cheaper than all-human, at the same failure rate.
- Risk scores: most claims low (green), a heavy tail high (red).
Present these as schematic, not precise.

## Animation concept (storyboard, ~16-18s)
1. **Score.** A horizontal "denial risk score" axis (0 to 1). ~40 claim dots stream in, placed by
   score, colored on a green (low) to red (high) ramp. Most cluster low; a heavy tail reaches high.
   Title: "Score every claim by denial risk."
2. **Route.** A vertical **threshold** line drops in. Dots below slide into an "Automate (AI, $0.10)"
   lane; dots above slide into a "Human review ($5.00)" lane. Two live readouts: "automation rate"
   and "missed errors".
3. **Optimize.** Sweep the threshold left to right. Automation rate rises AND missed errors rise (the
   tradeoff). A **cost-per-claim curve** traces a U; a marker rides it to the valley; the threshold
   snaps to that "optimal cutoff".
4. **Payoff.** Three cost bars: "All human" (tall, safe), "All AI" (short, but a red failure marker
   high), "Risk-stratified" (short AND low failure), the last highlighted in ACCENT. Small labels:
   "~half the cost", "same failure rate".
5. Loop back to the scored cloud.

## Technical notes
- Manim CE 0.20.1, `Text`/`MarkupText` only (no LaTeX), site palette from `aiqri_palette.py`, plus a
  muted green (e.g. #2E7D5B) for low-risk/safe and a red (e.g. #A6321E) for high-risk/failure.
- Keep it legible: few, bold elements; schematic over exact. ~16-18s, seamless loop, 1280x720, muted.
- Render to `public/media/talks/risk-filtered-automation.mp4` (+ `.png` poster). < ~1.6 MB.

## Caption (Speaking talk animation.caption)
"Schematic of the talk's simulation: routing claims by predicted denial risk, automating the
low-risk majority and sending the risky tail to human review, cuts cost by roughly half while
holding the failure rate at the human baseline."

## Acceptance
- `public/media/talks/risk-filtered-automation.mp4` (+ poster) rendered, loops, muted, < ~1.6 MB.
- The route -> optimize -> payoff arc reads without audio; risk-stratified clearly wins on both cost
  and safety.
- No proprietary terms anywhere in the clip.
- Wired below the ML Week talk in the Speaking section (see SPEC6).
