# Dataset Provenance

**Source:** [mominullptr/FIFA-World-Cup-2026-Dataset](https://github.com/mominullptr/FIFA-World-Cup-2026-Dataset)
(also mirrored on Kaggle as `mominullptr/fifa-world-cup-2026-dataset` and on Hugging Face as
`Mominullptr/fifa-world-cup-2026-dataset`). License: CC0-1.0 (Public Domain Dedication).

**Fetched:** 2026-07-23, via `raw.githubusercontent.com/mominullptr/FIFA-World-Cup-2026-Dataset/main/<file>.csv`
(direct HTTPS GET, unauthenticated — the GitHub API was not reachable from this session to pin an
exact commit SHA, so provenance is anchored to fetch date + file list + row counts below instead).

**Files copied verbatim into `data/raw/` (no transformation applied at copy time):**

| File | Rows (excl. header) | Notes |
|---|---|---|
| `teams.csv` | 48 | FIFA rankings, ELO, confederation per team |
| `venues.csv` | 16 | Stadiums, geolocation, capacity, elevation |
| `tournament_stages.csv` | 7 | Stage lookup table incl. `is_knockout` |
| `referees.csv` | 28 | Officials + historical card averages |
| `matches.csv` | 104 | Normalized match records (FK-based) |
| `matches_detailed.csv` | 104 | Denormalized, human-readable match records |
| `squads_and_players.csv` | 1248 | 26 players × 48 teams, incl. pre-tournament `market_value_eur` |
| `match_events.csv` | 834 | Goals/cards/VAR time-series |
| `match_team_stats.csv` | 208 | Per-team per-match possession/shots/corners/etc. |
| `match_lineups.csv` | 5408 | Full 26-man squad × 104 matches, `is_starting_xi` + `minutes_played` |
| `player_stats.csv` | 1248 | **Cumulative tournament totals — NOT used for any pre-match input** (would leak future info) |
| `match_prediction_features.csv` | 104 | 65 pre-calculated ML features, incl. causal rolling pre-match averages (`*_prev_avg_*`) |

**Match count check:** 104 matches total, confirmed against the stage breakdown required by the audit
spec: Group Stage 72, Round of 32 16, Round of 16 8, Quarter-finals 4, Semi-finals 2,
Third-place match 1, Final 1 → sums to 104. ✅

**Team roster note:** this repo's pre-tournament `data/teams.js` / `data/ratings.js` speculatively
included several teams that did not, in fact, qualify for the real tournament (SRB, DEN, POL, NGR,
CRI, VEN, CHI, ROU, UKR). Those teams simply never appear in any of the 104 real matches and require
no special handling. One code alias is required: the real dataset uses `KSA` (Saudi Arabia) where
this repo's `data/teams.js` / `data/ratings.js` use `SAU` for the same team — see
`lib/teamCodeMap.js`.
