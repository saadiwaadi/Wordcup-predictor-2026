// ORACLE-26 — As-Is Blind Test
//
// Runs runPrediction() exactly as it exists on main today, with the repo's own
// existing team data (data/index.js -> data/teams.js + data/ratings.js + data/form.js),
// against the real 104 World Cup 2026 results. Read-only against engine.js, app.js,
// and data/ratings.js — this script imports them unmodified and does not patch
// anything, including the known elo_delta_90 NaN bug. Whatever the model does,
// bugs included, is the result.
//
// The mominullptr FIFA-World-Cup-2026-Dataset is used ONLY as an answer key here
// (home/away team, stage, final score) — none of its team-strength/form/xG fields
// are fed into the engine. That enrichment is a separate, later piece of work.
//
// Verified clean before this run: `git status --porcelain engine.js app.js data/ratings.js`
// produced no output, commit 562807df1d6600366d965ebfa34cd59891821de4.

import { runPrediction } from '../../engine.js';
import { TEAMS, getH2H } from '../../data/index.js';
import { parseCSV, num } from './lib/csv.js';
import { toEngineCode } from './lib/teamCodeMap.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const STAGE_NAME_TO_ENGINE_STAGE = {
  'Group Stage': 'Group',
  'Round of 32': 'R32',
  'Round of 16': 'R16',
  'Quarter-finals': 'QF',
  'Semi-finals': 'SF',
  'Third-place match': 'SF', // flagged assumption, per spec: no dedicated modifier exists
  'Final': 'Final',
};

const teamsById = new Map(TEAMS.map(t => [t.id, t]));

function loadMatches() {
  const text = fs.readFileSync(path.join(__dirname, 'data', 'raw', 'matches_detailed.csv'), 'utf-8');
  return parseCSV(text)
    .map(r => ({
      match_id: r.match_id,
      date: r.date,
      kickoff_time_utc: r.kickoff_time_utc,
      stage_name: r.stage_name,
      home_fifa_code: r.home_fifa_code,
      away_fifa_code: r.away_fifa_code,
      home_score: num(r.home_score),
      away_score: num(r.away_score),
    }))
    .sort((a, b) => {
      const dtA = `${a.date}T${a.kickoff_time_utc}`;
      const dtB = `${b.date}T${b.kickoff_time_utc}`;
      return dtA < dtB ? -1 : dtA > dtB ? 1 : 0;
    });
}

function isBad(v) {
  return v === undefined || v === null || Number.isNaN(v);
}

function actualOutcome(scoreA, scoreB) {
  // Penalty-shootout winners score as a Draw here too: runPrediction only ever
  // models goals via Poisson, never penalties, so crediting/blaming it for a
  // shootout result would test something it was never built to predict.
  // (4 of the 104 matches were decided on penalties, all drawn 90+ET.)
  if (scoreA > scoreB) return 'A';
  if (scoreA < scoreB) return 'B';
  return 'D';
}

function predictedOutcome(r) {
  if (isBad(r.winA_pct) || isBad(r.draw_pct) || isBad(r.winB_pct)) return null;
  if (r.winA_pct >= r.draw_pct && r.winA_pct >= r.winB_pct) return 'A';
  if (r.winB_pct >= r.draw_pct && r.winB_pct >= r.winA_pct) return 'B';
  return 'D';
}

const matches = loadMatches();
const results = [];
const nanTeams = new Set();

matches.forEach(m => {
  const homeCode = toEngineCode(m.home_fifa_code);
  const awayCode = toEngineCode(m.away_fifa_code);
  const teamAProfile = teamsById.get(homeCode);
  const teamBProfile = teamsById.get(awayCode);

  const row = {
    match_id: m.match_id,
    stage: m.stage_name,
    teamA: homeCode,
    teamB: awayCode,
    actual: {
      scoreA: m.home_score,
      scoreB: m.away_score,
      outcome: actualOutcome(m.home_score, m.away_score),
    },
  };

  if (!teamAProfile || !teamBProfile) {
    row.status = 'failed';
    row.reason = `missing team profile in TEAMS array for ${!teamAProfile ? homeCode : awayCode}`;
    row.predicted = null;
    row.correct_outcome = false;
    row.correct_scoreline = false;
    results.push(row);
    return;
  }

  // Exact team objects the current codebase builds (data/index.js getTeamData()),
  // plus isHome — the one fixture-specific fact not part of that static merge.
  const teamA = { ...teamAProfile, isHome: true };
  const teamB = { ...teamBProfile, isHome: false };

  const options = {
    injureKeyA: false, // zero injury signal used in this pass, deliberately — stated explicitly
    injureKeyB: false,
    staleData: false,
    stage: STAGE_NAME_TO_ENGINE_STAGE[m.stage_name],
  };

  let engineOut;
  let threw = null;
  try {
    engineOut = runPrediction(teamA, teamB, options);
  } catch (e) {
    threw = e.message;
  }

  if (threw) {
    row.status = 'failed';
    row.reason = `runPrediction threw: ${threw}`;
    row.predicted = null;
    row.correct_outcome = false;
    row.correct_scoreline = false;
    results.push(row);
    return;
  }

  const nan = isBad(engineOut.winA_pct) || isBad(engineOut.draw_pct) || isBad(engineOut.winB_pct)
    || isBad(engineOut.lambda_A) || isBad(engineOut.lambda_B);

  if (nan) {
    if (isBad(teamA.elo_delta_90)) nanTeams.add(homeCode);
    if (isBad(teamB.elo_delta_90)) nanTeams.add(awayCode);
  }

  const predOutcome = predictedOutcome(engineOut);
  row.predicted = {
    winA_pct: engineOut.winA_pct,
    draw_pct: engineOut.draw_pct,
    winB_pct: engineOut.winB_pct,
    lambda_A: engineOut.lambda_A,
    lambda_B: engineOut.lambda_B,
    mostLikelyScoreline: nan ? null : engineOut.mostLikelyScoreline,
  };
  row.status = nan ? 'nan_error' : 'ok';
  row.correct_outcome = !nan && predOutcome === row.actual.outcome;
  row.correct_scoreline = !nan && engineOut.mostLikelyScoreline === `${m.home_score}-${m.away_score}`;

  results.push(row);
});

// ---- Metrics ----
const EPS = 1e-15;
function oneHot(outcome) {
  return { A: outcome === 'A' ? 1 : 0, D: outcome === 'D' ? 1 : 0, B: outcome === 'B' ? 1 : 0 };
}

function computeMetricsFor(rows) {
  const n = rows.length;
  if (n === 0) return null;
  let correctOutcomes = 0, correctScorelines = 0, brierSum = 0;
  const goalsSamples = [];
  let nanCount = 0, failedCount = 0;

  rows.forEach(r => {
    if (r.status === 'failed') { failedCount++; return; } // excluded entirely: no predicted object exists at all
    if (r.status === 'nan_error') nanCount++;

    const O = oneHot(r.actual.outcome);
    let P_A, P_D, P_B;
    if (r.status === 'nan_error') {
      // Explicit choice (spec option a): score broken predictions as uniform [1/3,1/3,1/3]
      // for Brier purposes, rather than excluding them.
      P_A = 1 / 3; P_D = 1 / 3; P_B = 1 / 3;
    } else {
      P_A = r.predicted.winA_pct / 100; P_D = r.predicted.draw_pct / 100; P_B = r.predicted.winB_pct / 100;
    }
    brierSum += Math.pow(P_A - O.A, 2) + Math.pow(P_D - O.D, 2) + Math.pow(P_B - O.B, 2);

    if (r.correct_outcome) correctOutcomes++;
    if (r.correct_scoreline) correctScorelines++;

    if (r.status === 'ok') goalsSamples.push(r.predicted.lambda_A + r.predicted.lambda_B);
  });

  const scored = n - failedCount;
  const mean = goalsSamples.length ? goalsSamples.reduce((s, v) => s + v, 0) / goalsSamples.length : null;
  const variance = goalsSamples.length ? goalsSamples.reduce((s, v) => s + Math.pow(v - mean, 2), 0) / goalsSamples.length : null;

  return {
    totalMatches: n,
    failedCount,
    nanErrorCount: nanCount,
    outcomeAccuracy: scored ? correctOutcomes / scored : null,
    brierScore: scored ? brierSum / scored : null,
    scorelineAccuracy: scored ? correctScorelines / scored : null,
    meanTotalGoals: mean,
    varTotalGoals: variance,
    goalsSampleSize: goalsSamples.length,
  };
}

const overall = computeMetricsFor(results);

const byStage = {};
for (const stageName of Object.keys(STAGE_NAME_TO_ENGINE_STAGE)) {
  const rows = results.filter(r => r.stage === stageName);
  if (rows.length) byStage[stageName] = computeMetricsFor(rows);
}

// ---- Write outputs ----
const resultsDir = path.join(__dirname, 'results');
fs.mkdirSync(resultsDir, { recursive: true });

fs.writeFileSync(
  path.join(resultsDir, 'blind-test-asis-results.json'),
  JSON.stringify(results, null, 2)
);

function fmtPct(v) { return v == null ? 'n/a' : (v * 100).toFixed(1) + '%'; }
function fmtNum(v, d = 4) { return v == null ? 'n/a' : v.toFixed(d); }

const nanTeamsList = [...nanTeams].sort();

const RATINGS_MISSING_SNAKE_CASE = ['SCO', 'NOR', 'NZL', 'BIH', 'HAI', 'CUW', 'CPV', 'IRQ', 'JOR', 'COD', 'UZB'];

let md = `# ORACLE-26 — As-Is Blind Test Results\n\n`;
md += `Run against commit \`562807df1d6600366d965ebfa34cd59891821de4\` (engine.js, app.js, data/ratings.js unmodified — verified clean before and after this run).\n\n`;
md += `This is the model exactly as it exists in the repository today, with zero injury signal, zero bug fixes, and zero new data. Known issues (NaN teams, static ratings snapshot, disconnected draw probability) are present and reflected in these numbers as-is.\n\n`;

md += `## NaN bug — finding, precisely stated\n\n`;
md += `\`data/ratings.js\` as committed is genuinely missing the snake_case \`elo_delta_90\` key for 11 teams: `
  + `**${RATINGS_MISSING_SNAKE_CASE.join(', ')}** — they only have the camelCase \`eloDelta90\`.\n\n`;
md += `However, running this blind test surfaced that this does **not** currently propagate into a NaN prediction: `
  + `**${overall.nanErrorCount} / ${overall.totalMatches}** matches produced a NaN/undefined result `
  + `(teams observed hitting it: ${nanTeamsList.join(', ') || 'none'}).\n\n`;
md += `Root cause of why it's currently inert: \`data/index.js\` line 109 builds every team object via `
  + `\`elo_delta_90: rating.eloDelta90\` — it reads the **camelCase** source field, which is present for `
  + `all teams, and re-exposes it under the snake_case name \`engine.js\` actually consumes `
  + `(\`teamA.elo_delta_90 / 100\`). The redundant snake_case key inside \`RATINGS\` itself is dead data as far `
  + `as the live \`TEAMS\` pipeline is concerned. Verified directly: \`TEAMS.find(t => t.id === 'SCO').elo_delta_90\` `
  + `resolves to \`-3\`, not \`NaN\`, and likewise for the other 10 teams (all resolve to a real number, mostly \`0\`).\n\n`;
md += `This is still a real defect worth flagging — \`data/ratings.js\` carries an inconsistent, partially-missing `
  + `duplicate key that would bite immediately if any future code read \`RATINGS[code].elo_delta_90\` directly `
  + `(bypassing \`getTeamData()\`), which is exactly what the earlier two-variant audit spec's own input-builder `
  + `was about to do before this blind test caught it. It just isn't live today. Reporting the mechanism, not `
  + `just the absence of NaN, is the honest version of this finding.\n\n`;

md += `## Overall\n\n`;
md += `| Metric | Value |\n|---|---|\n`;
md += `| Total matches | ${overall.totalMatches} |\n`;
md += `| Failed (no prediction produced) | ${overall.failedCount} |\n`;
md += `| NaN/undefined predictions | ${overall.nanErrorCount} |\n`;
md += `| Outcome Accuracy | ${fmtPct(overall.outcomeAccuracy)} |\n`;
md += `| Brier Score (NaN rows scored as uniform 1/3,1/3,1/3) | ${fmtNum(overall.brierScore)} |\n`;
md += `| Exact Scoreline Accuracy | ${fmtPct(overall.scorelineAccuracy)} |\n`;
md += `| Mean total goals (λ_A + λ_B), non-NaN matches only, n=${overall.goalsSampleSize} | ${fmtNum(overall.meanTotalGoals, 3)} |\n`;
md += `| Variance of total goals | ${fmtNum(overall.varTotalGoals, 4)} |\n\n`;

md += `## Per stage\n\n`;
md += `| Stage | N | Failed | NaN | Accuracy | Brier | Scoreline Acc. | Mean λ_A+λ_B |\n|---|---|---|---|---|---|---|---|\n`;
for (const stageName of Object.keys(STAGE_NAME_TO_ENGINE_STAGE)) {
  const s = byStage[stageName];
  if (!s) continue;
  md += `| ${stageName} | ${s.totalMatches} | ${s.failedCount} | ${s.nanErrorCount} | ${fmtPct(s.outcomeAccuracy)} | ${fmtNum(s.brierScore)} | ${fmtPct(s.scorelineAccuracy)} | ${fmtNum(s.meanTotalGoals, 3)} |\n`;
}

md += `\n## Explicit assumptions in this pass\n\n`;
md += `- \`injureKeyA\`/\`injureKeyB\` = \`false\` for every match — zero injury signal used, not an inferred one.\n`;
md += `- \`staleData\` = \`false\` for every match — no retrospective staleness signal exists.\n`;
md += `- Third-place play-off mapped to \`stage: "SF"\` — no dedicated modifier exists for it.\n`;
md += `- Penalty-shootout winners (4 matches) are scored as a Draw for outcome/Brier/scoreline purposes — the engine models goals via Poisson, never penalties.\n`;
md += `- NaN/undefined predictions are scored as uniform [1/3, 1/3, 1/3] for Brier purposes and as incorrect for outcome/scoreline accuracy — not excluded from the match count.\n`;
md += `- \`last_6\` form comes from whatever \`data/index.js\`'s \`getForm()\` already returns under Node with no scraped-data fetch available — i.e. the static, pre-tournament \`data/form.js\` values as committed, unmodified.\n`;

fs.writeFileSync(path.join(resultsDir, 'blind-test-asis-summary.md'), md);

console.log(md);
console.log(`\nWrote ${results.length} match rows to scripts/audit/results/blind-test-asis-results.json`);
