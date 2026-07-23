# ORACLE-26 — As-Is Blind Test Results

Run against commit `562807df1d6600366d965ebfa34cd59891821de4` (engine.js, app.js, data/ratings.js unmodified — verified clean before and after this run).

This is the model exactly as it exists in the repository today, with zero injury signal, zero bug fixes, and zero new data. Known issues (NaN teams, static ratings snapshot, disconnected draw probability) are present and reflected in these numbers as-is.

## NaN bug — finding, precisely stated

`data/ratings.js` as committed is genuinely missing the snake_case `elo_delta_90` key for 11 teams: **SCO, NOR, NZL, BIH, HAI, CUW, CPV, IRQ, JOR, COD, UZB** — they only have the camelCase `eloDelta90`.

However, running this blind test surfaced that this does **not** currently propagate into a NaN prediction: **0 / 104** matches produced a NaN/undefined result (teams observed hitting it: none).

Root cause of why it's currently inert: `data/index.js` line 109 builds every team object via `elo_delta_90: rating.eloDelta90` — it reads the **camelCase** source field, which is present for all teams, and re-exposes it under the snake_case name `engine.js` actually consumes (`teamA.elo_delta_90 / 100`). The redundant snake_case key inside `RATINGS` itself is dead data as far as the live `TEAMS` pipeline is concerned. Verified directly: `TEAMS.find(t => t.id === 'SCO').elo_delta_90` resolves to `-3`, not `NaN`, and likewise for the other 10 teams (all resolve to a real number, mostly `0`).

This is still a real defect worth flagging — `data/ratings.js` carries an inconsistent, partially-missing duplicate key that would bite immediately if any future code read `RATINGS[code].elo_delta_90` directly (bypassing `getTeamData()`), which is exactly what the earlier two-variant audit spec's own input-builder was about to do before this blind test caught it. It just isn't live today. Reporting the mechanism, not just the absence of NaN, is the honest version of this finding.

## Overall

| Metric | Value |
|---|---|
| Total matches | 104 |
| Failed (no prediction produced) | 0 |
| NaN/undefined predictions | 0 |
| Outcome Accuracy | 64.4% |
| Brier Score (NaN rows scored as uniform 1/3,1/3,1/3) | 0.4781 |
| Exact Scoreline Accuracy | 15.4% |
| Mean total goals (λ_A + λ_B), non-NaN matches only, n=104 | 2.296 |
| Variance of total goals | 0.0049 |

## Per stage

| Stage | N | Failed | NaN | Accuracy | Brier | Scoreline Acc. | Mean λ_A+λ_B |
|---|---|---|---|---|---|---|---|
| Group Stage | 72 | 0 | 0 | 63.9% | 0.4685 | 15.3% | 2.340 |
| Round of 32 | 16 | 0 | 0 | 75.0% | 0.4430 | 25.0% | 2.223 |
| Round of 16 | 8 | 0 | 0 | 50.0% | 0.5798 | 12.5% | 2.223 |
| Quarter-finals | 4 | 0 | 0 | 100.0% | 0.3986 | 0.0% | 2.153 |
| Semi-finals | 2 | 0 | 0 | 50.0% | 0.5860 | 0.0% | 2.106 |
| Third-place match | 1 | 0 | 0 | 0.0% | 0.7875 | 0.0% | 2.106 |
| Final | 1 | 0 | 0 | 0.0% | 0.7118 | 0.0% | 2.059 |

## Explicit assumptions in this pass

- `injureKeyA`/`injureKeyB` = `false` for every match — zero injury signal used, not an inferred one.
- `staleData` = `false` for every match — no retrospective staleness signal exists.
- Third-place play-off mapped to `stage: "SF"` — no dedicated modifier exists for it.
- Penalty-shootout winners (4 matches) are scored as a Draw for outcome/Brier/scoreline purposes — the engine models goals via Poisson, never penalties.
- NaN/undefined predictions are scored as uniform [1/3, 1/3, 1/3] for Brier purposes and as incorrect for outcome/scoreline accuracy — not excluded from the match count.
- `last_6` form comes from whatever `data/index.js`'s `getForm()` already returns under Node with no scraped-data fetch available — i.e. the static, pre-tournament `data/form.js` values as committed, unmodified.
