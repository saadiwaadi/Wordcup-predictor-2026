// scripts/benchmark_2026.js - Locally runnable benchmark script for ORACLE-26 completed fixtures
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { runPrediction } from '../engine.js';
import { TEAMS } from '../data/index.js';
import { getLambdaOverride, recomputeScorelines } from '../data/enrichTeam.js';

// Setup file paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const FIXTURES_FILE = path.join(__dirname, '../data/scraped/fixtures.json');

// Step 1 - Build a name-to-code map
const NAME_OVERRIDES = {
  "Czech Republic": "CZE",
  "Bosnia and Herzegovina": "BIH",
  "Bosnia & Herzegovina": "BIH",
  "DR Congo": "COD",
  "USA": "USA",
  "United States": "USA",
  "Ivory Coast": "CIV"
};

const staticMap = {};
TEAMS.forEach(team => {
  staticMap[team.name] = team.id;
});

function nameToCode(name) {
  if (NAME_OVERRIDES[name]) return NAME_OVERRIDES[name];
  if (staticMap[name]) return staticMap[name];
  
  const lower = name.toLowerCase();
  const matched = Object.keys(staticMap).find(k => k.toLowerCase() === lower);
  if (matched) return staticMap[matched];
  return undefined;
}

// Replicating getFormBeforeDate from backtester.js
export function getFormBeforeDate(teamCode, beforeDate, allMatches) {
  const priorMatches = allMatches.filter(m => {
    if (m.team1Code !== teamCode && m.team2Code !== teamCode) return false;
    return new Date(m.date) < new Date(beforeDate);
  });

  priorMatches.sort((a, b) => new Date(a.date) - new Date(b.date));

  // Take the last 5
  const last5 = priorMatches.slice(-5);

  // Map to W/D/L from perspective of teamCode
  return last5.map(m => {
    const isTeam1 = m.team1Code === teamCode;
    const goalsFor = isTeam1 ? m.score.ft[0] : m.score.ft[1];
    const goalsAgainst = isTeam1 ? m.score.ft[1] : m.score.ft[0];
    if (goalsFor > goalsAgainst) return "W";
    if (goalsFor < goalsAgainst) return "L";
    return "D";
  });
}

// Replicating getStatsBeforeDate from backtester.js
export function getStatsBeforeDate(teamCode, beforeDate, allMatches) {
  const priorMatches = allMatches.filter(m => {
    if (m.team1Code !== teamCode && m.team2Code !== teamCode) return false;
    return new Date(m.date) < new Date(beforeDate);
  });

  let goalsFor = 0;
  let goalsAgainst = 0;
  const matchesPlayed = priorMatches.length;

  for (const m of priorMatches) {
    const isTeam1 = m.team1Code === teamCode;
    const gFor = isTeam1 ? m.score.ft[0] : m.score.ft[1];
    const gAgainst = isTeam1 ? m.score.ft[1] : m.score.ft[0];
    goalsFor += gFor;
    goalsAgainst += gAgainst;
  }

  const avgGoalsFor = matchesPlayed > 0 ? parseFloat((goalsFor / matchesPlayed).toFixed(4)) : 0;
  const avgGoalsAgainst = matchesPlayed > 0 ? parseFloat((goalsAgainst / matchesPlayed).toFixed(4)) : 0;

  return {
    goalsFor,
    goalsAgainst,
    matchesPlayed,
    avgGoalsFor,
    avgGoalsAgainst
  };
}

async function runBenchmark() {
  let fileContent;
  try {
    fileContent = await fs.readFile(FIXTURES_FILE, 'utf8');
  } catch (err) {
    console.error(`Error: Could not read fixtures file at ${FIXTURES_FILE}: ${err.message}`);
    process.exit(1);
  }

  const fixtures = JSON.parse(fileContent);
  const completedFixtures = fixtures.filter(f => f.result && f.result.ft);

  // Step 2 - Convert completed fixtures to backtester match format
  const convertedMatches = [];
  for (const f of completedFixtures) {
    const code1 = nameToCode(f.home_team);
    const code2 = nameToCode(f.away_team);

    if (!code1 || !code2) {
      if (!code1) console.warn(`Warning: Could not map home team "${f.home_team}" to ID.`);
      if (!code2) console.warn(`Warning: Could not map away team "${f.away_team}" to ID.`);
      continue;
    }

    convertedMatches.push({
      team1Code: code1,
      team2Code: code2,
      date: f.kickoff_utc,
      score: { ft: f.result.ft },
      round: f.stage || "Group Stage",
      group: f.stage || "Group Stage"
    });
  }

  // Sort matches chronologically
  convertedMatches.sort((a, b) => new Date(a.date) - new Date(b.date));

  const results = [];

  // Step 3 - Run backtester logic loop
  for (const match of convertedMatches) {
    const codeA = match.team1Code;
    const codeB = match.team2Code;

    const teamA = TEAMS.find(t => t.id === codeA);
    const teamB = TEAMS.find(t => t.id === codeB);

    if (!teamA || !teamB) {
      continue;
    }

    // Clone team objects
    const enrichedA = JSON.parse(JSON.stringify(teamA));
    const enrichedB = JSON.parse(JSON.stringify(teamB));

    // Get historical form/stats prior to match date
    enrichedA.last_6 = getFormBeforeDate(codeA, match.date, convertedMatches);
    enrichedB.last_6 = getFormBeforeDate(codeB, match.date, convertedMatches);

    const statsA = getStatsBeforeDate(codeA, match.date, convertedMatches);
    const statsB = getStatsBeforeDate(codeB, match.date, convertedMatches);

    enrichedA.liveStats = statsA;
    enrichedB.liveStats = statsB;
    enrichedA.matchesPlayedInTournament = statsA.matchesPlayed;
    enrichedB.matchesPlayedInTournament = statsB.matchesPlayed;
    enrichedA.hasLiveData = statsA.matchesPlayed >= 1;
    enrichedB.hasLiveData = statsB.matchesPlayed >= 1;

    // Run prediction
    const options = {
      staleData: !enrichedA.hasLiveData && !enrichedB.hasLiveData,
      injureKeyA: false,
      injureKeyB: false
    };

    const prediction = runPrediction(enrichedA, enrichedB, options);

    // Apply lambda overrides and scoreline recomputation
    const newLambdaA = getLambdaOverride(enrichedA, prediction.P_dynamic_A, true); // teamA is home
    const newLambdaB = getLambdaOverride(enrichedB, prediction.P_dynamic_B, false); // teamB is away

    if (newLambdaA !== prediction.lambda_A || newLambdaB !== prediction.lambda_B) {
      prediction.lambda_A = newLambdaA;
      prediction.lambda_B = newLambdaB;
      const recomputed = recomputeScorelines(newLambdaA, newLambdaB);
      prediction.top5 = recomputed.top5;
      prediction.mostLikelyScoreline = recomputed.mostLikelyScoreline;
      prediction.sumProb = recomputed.sumProb;
    }

    // Determine predicted outcome
    const winA = prediction.winA_pct;
    const winB = prediction.winB_pct;
    const draw = prediction.draw_pct;

    let predictedOutcome;
    if (draw >= winA && draw >= winB) {
      predictedOutcome = 'DRAW';
    } else if (winA >= winB) {
      predictedOutcome = 'HOME';
    } else {
      predictedOutcome = 'AWAY';
    }

    // Determine actual outcome
    let actualOutcome = 'DRAW';
    if (match.score.ft[0] > match.score.ft[1]) {
      actualOutcome = 'HOME';
    } else if (match.score.ft[0] < match.score.ft[1]) {
      actualOutcome = 'AWAY';
    }

    const outcomeCorrect = (predictedOutcome === actualOutcome);

    results.push({
      round: match.round,
      predictedOutcome,
      actualOutcome,
      outcomeCorrect,
      winA_pct: winA,
      draw_pct: draw,
      winB_pct: winB
    });
  }

  // Step 4 - Output metrics
  const totalMatches = results.length;
  const outcomeCorrectCount = results.filter(r => r.outcomeCorrect).length;
  const accuracy = totalMatches > 0 ? (outcomeCorrectCount / totalMatches) * 100 : 0;

  // Brier score calculation
  let totalBS = 0;
  results.forEach(r => {
    const p_home = r.winA_pct / 100;
    const p_draw = r.draw_pct / 100;
    const p_away = r.winB_pct / 100;

    const act_home = r.actualOutcome === 'HOME' ? 1 : 0;
    const act_draw = r.actualOutcome === 'DRAW' ? 1 : 0;
    const act_away = r.actualOutcome === 'AWAY' ? 1 : 0;

    const bs = Math.pow(p_home - act_home, 2) +
               Math.pow(p_draw - act_draw, 2) +
               Math.pow(p_away - act_away, 2);
    totalBS += bs;
  });
  const brierScore = totalMatches > 0 ? totalBS / totalMatches : 0;

  // Breakdown by round/stage
  const byRound = {};
  results.forEach(r => {
    const rnd = r.round;
    if (!byRound[rnd]) {
      byRound[rnd] = { matches: 0, correct: 0 };
    }
    byRound[rnd].matches++;
    if (r.outcomeCorrect) {
      byRound[rnd].correct++;
    }
  });

  // Display report
  console.log("=== ORACLE-26 BENCHMARK 2026 REPORT ===");
  console.log(`Total Matches Evaluated: ${totalMatches}`);
  console.log(`Outcome Accuracy:        ${accuracy.toFixed(1)}% (${outcomeCorrectCount}/${totalMatches} correct)`);
  console.log(`Brier Score:             ${brierScore.toFixed(4)}`);
  console.log("\n=== BASELINE COMPARISON ===");
  console.log(`Baseline Accuracy:       60.0% (Old 60-match set)`);
  console.log(`ORACLE-26 Accuracy:      ${accuracy.toFixed(1)}%`);
  console.log(`Difference:              ${(accuracy - 60).toFixed(1)} pp`);
  console.log(`\nBaseline Brier Score:    0.5510`);
  console.log(`ORACLE-26 Brier Score:   ${brierScore.toFixed(4)}`);
  console.log(`Difference:              ${(brierScore - 0.551).toFixed(4)} (lower is better)`);

  console.log("\n=== BREAKDOWN BY ROUND/STAGE ===");
  const rounds = Object.keys(byRound).sort();
  rounds.forEach(rnd => {
    const stats = byRound[rnd];
    const rndAcc = (stats.correct / stats.matches) * 100;
    console.log(`  ${rnd.padEnd(20)}: ${rndAcc.toFixed(1)}% (${stats.correct}/${stats.matches})`);
  });
}

runBenchmark();
