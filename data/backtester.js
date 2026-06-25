// Run with: node data/backtester.js

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { runPrediction } from '../engine.js';
import { TEAMS } from './index.js';
import { getLambdaOverride, recomputeScorelines, applyDrawCorrection } from './enrichTeam.js';
import { getFixture } from './openFootballLayer.js';

// Setup file paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const CACHE_FILE = path.join(__dirname, '../cache/openfootball_cache.json');
const RESULTS_FILE = path.join(__dirname, '../cache/backtest_results.json');

export function getFormBeforeDate(teamCode, beforeDate, allMatches) {
  const priorMatches = allMatches.filter(m => {
    if (m.team1Code !== teamCode && m.team2Code !== teamCode) return false;
    return new Date(m.date) < new Date(beforeDate);
  });

  // Sort priorMatches by date ascending
  priorMatches.sort((a, b) => new Date(a.date) - new Date(b.date));

  // Take the last 5
  const last5 = priorMatches.slice(-5);

  // Map to W/D/L from the perspective of teamCode
  return last5.map(m => {
    const isTeam1 = m.team1Code === teamCode;
    const goalsFor = isTeam1 ? m.score.ft[0] : m.score.ft[1];
    const goalsAgainst = isTeam1 ? m.score.ft[1] : m.score.ft[0];
    if (goalsFor > goalsAgainst) return "W";
    if (goalsFor < goalsAgainst) return "L";
    return "D";
  });
}

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

export async function runBacktest() {
  // Load openfootball cache file
  let cacheContent;
  try {
    cacheContent = await fs.readFile(CACHE_FILE, 'utf8');
  } catch (err) {
    throw new Error(`Failed to read openfootball cache at ${CACHE_FILE}: ${err.message}`);
  }

  const cache = JSON.parse(cacheContent);
  const allMatches = cache.computed?.completedMatches || [];

  // Sort matches chronologically
  allMatches.sort((a, b) => new Date(a.date) - new Date(b.date));

  const results = [];

  for (const match of allMatches) {
    const codeA = match.team1Code;
    const codeB = match.team2Code;

    const teamA = TEAMS.find(t => t.id === codeA);
    const teamB = TEAMS.find(t => t.id === codeB);

    if (!teamA || !teamB) {
      if (!teamA) console.warn(`Warning: Team code "${codeA}" not found in TEAMS. Skipping match.`);
      if (!teamB) console.warn(`Warning: Team code "${codeB}" not found in TEAMS. Skipping match.`);
      continue;
    }

    // Build blind enriched versions of team objects
    const enrichedA = JSON.parse(JSON.stringify(teamA));
    const enrichedB = JSON.parse(JSON.stringify(teamB));

    enrichedA.last_6 = getFormBeforeDate(codeA, match.date, allMatches);
    enrichedB.last_6 = getFormBeforeDate(codeB, match.date, allMatches);

    const statsA = getStatsBeforeDate(codeA, match.date, allMatches);
    const statsB = getStatsBeforeDate(codeB, match.date, allMatches);

    enrichedA.liveStats = statsA;
    enrichedB.liveStats = statsB;

    enrichedA.matchesPlayedInTournament = statsA.matchesPlayed;
    enrichedB.matchesPlayedInTournament = statsB.matchesPlayed;

    enrichedA.hasLiveData = statsA.matchesPlayed >= 1;
    enrichedB.hasLiveData = statsB.matchesPlayed >= 1;

    // Determine home/away based on getFixture
    const fixture = await getFixture(codeA, codeB);
    const isAHome = fixture ? (fixture.homeTeamCode === codeA) : true;
    const isBHome = fixture ? (fixture.homeTeamCode === codeB) : false;

    // Run prediction using blind versions
    const options = {
      staleData: !enrichedA.hasLiveData && !enrichedB.hasLiveData,
      injureKeyA: false,
      injureKeyB: false
    };

    const prediction = runPrediction(enrichedA, enrichedB, options);

    // Override lambdas and recompute scorelines
    const newLambdaA = getLambdaOverride(enrichedA, prediction.P_dynamic_A, isAHome);
    const newLambdaB = getLambdaOverride(enrichedB, prediction.P_dynamic_B, isBHome);

    if (newLambdaA !== prediction.lambda_A || newLambdaB !== prediction.lambda_B) {
      prediction.lambda_A = newLambdaA;
      prediction.lambda_B = newLambdaB;
      const recomputed = recomputeScorelines(newLambdaA, newLambdaB);
      prediction.top5 = recomputed.top5;
      prediction.mostLikelyScoreline = recomputed.mostLikelyScoreline;
      prediction.sumProb = recomputed.sumProb;
    }

    // Apply draw correction
    const correctedPrediction = applyDrawCorrection(prediction);

    // Outcomes mapping
    let predictedOutcome = "DRAW";
    if (correctedPrediction.winA_pct > correctedPrediction.winB_pct && correctedPrediction.winA_pct > correctedPrediction.draw_pct) {
      predictedOutcome = "HOME";
    } else if (correctedPrediction.winB_pct > correctedPrediction.winA_pct && correctedPrediction.winB_pct > correctedPrediction.draw_pct) {
      predictedOutcome = "AWAY";
    }

    let actualOutcome = "DRAW";
    if (match.score.ft[0] > match.score.ft[1]) {
      actualOutcome = "HOME";
    } else if (match.score.ft[0] < match.score.ft[1]) {
      actualOutcome = "AWAY";
    }

    const actualScore = `${match.score.ft[0]}-${match.score.ft[1]}`;
    const outcomeCorrect = predictedOutcome === actualOutcome;
    const exactScoreCorrect = correctedPrediction.mostLikelyScoreline === actualScore;
    const inTop5 = correctedPrediction.top5.some(s => `${s.scoreA}-${s.scoreB}` === actualScore);

    // Calculate error for worst/best sorting
    const predProb = predictedOutcome === "HOME" ? correctedPrediction.winA_pct : (predictedOutcome === "AWAY" ? correctedPrediction.winB_pct : correctedPrediction.draw_pct);
    const actProb = actualOutcome === "HOME" ? correctedPrediction.winA_pct : (actualOutcome === "AWAY" ? correctedPrediction.winB_pct : correctedPrediction.draw_pct);
    
    // error is prediction confidence minus actual outcome probability if incorrect, else 0
    const error = outcomeCorrect ? 0 : (predProb - actProb);

    results.push({
      date: match.date,
      homeTeam: codeA,
      awayTeam: codeB,
      actualScore,
      predictedOutcome,
      actualOutcome,
      outcomeCorrect,
      mostLikelyScoreline: correctedPrediction.mostLikelyScoreline,
      exactScoreCorrect,
      inTop5,
      winA_pct: correctedPrediction.winA_pct,
      draw_pct: correctedPrediction.draw_pct,
      winB_pct: correctedPrediction.winB_pct,
      lambda_A: correctedPrediction.lambda_A,
      lambda_B: correctedPrediction.lambda_B,
      matchesPlayedBeforeThisMatch: statsA.matchesPlayed + statsB.matchesPlayed,
      group: match.group,
      round: match.round,
      tierA: teamA.tier,
      tierB: teamB.tier,
      error,
      actualOutcomeProbability: actProb,
      predictedOutcomeProbability: predProb,
      actualGoalsA: match.score.ft[0],
      actualGoalsB: match.score.ft[1]
    });
  }

  // 3. Compute Metrics
  const totalMatches = results.length;
  const outcomeCorrectCount = results.filter(r => r.outcomeCorrect).length;
  const exactScoreCorrectCount = results.filter(r => r.exactScoreCorrect).length;
  const inTop5Count = results.filter(r => r.inTop5).length;

  const overall = {
    totalMatches,
    outcomeCorrect: outcomeCorrectCount,
    outcomeAccuracy: totalMatches > 0 ? parseFloat(((outcomeCorrectCount / totalMatches) * 100).toFixed(1)) : 0,
    exactScoreCorrect: exactScoreCorrectCount,
    exactScoreAccuracy: totalMatches > 0 ? parseFloat(((exactScoreCorrectCount / totalMatches) * 100).toFixed(1)) : 0,
    inTop5: inTop5Count,
    top5Accuracy: totalMatches > 0 ? parseFloat(((inTop5Count / totalMatches) * 100).toFixed(1)) : 0
  };

  // byOutcome
  const byOutcome = {
    HOME: { predicted: 0, actual: 0, correct: 0, accuracy: 0 },
    DRAW: { predicted: 0, actual: 0, correct: 0, accuracy: 0 },
    AWAY: { predicted: 0, actual: 0, correct: 0, accuracy: 0 }
  };

  for (const r of results) {
    byOutcome[r.predictedOutcome].predicted += 1;
    byOutcome[r.actualOutcome].actual += 1;
    if (r.outcomeCorrect) {
      byOutcome[r.predictedOutcome].correct += 1;
    }
  }

  for (const key of Object.keys(byOutcome)) {
    const item = byOutcome[key];
    item.accuracy = item.predicted > 0 ? parseFloat(((item.correct / item.predicted) * 100).toFixed(1)) : 0;
  }

  // byMatchday
  const byMatchday = {};
  for (const r of results) {
    const round = r.round || "Unknown";
    if (!byMatchday[round]) {
      byMatchday[round] = { matches: 0, correct: 0, accuracy: 0 };
    }
    byMatchday[round].matches += 1;
    if (r.outcomeCorrect) {
      byMatchday[round].correct += 1;
    }
  }

  for (const round of Object.keys(byMatchday)) {
    const item = byMatchday[round];
    item.accuracy = item.matches > 0 ? parseFloat(((item.correct / item.matches) * 100).toFixed(1)) : 0;
  }

  // byTierMatchup
  const byTierMatchup = {};
  for (const r of results) {
    const tMin = Math.min(r.tierA, r.tierB);
    const tMax = Math.max(r.tierA, r.tierB);
    const key = `${tMin}v${tMax}`;
    if (!byTierMatchup[key]) {
      byTierMatchup[key] = { matches: 0, correct: 0, accuracy: 0 };
    }
    byTierMatchup[key].matches += 1;
    if (r.outcomeCorrect) {
      byTierMatchup[key].correct += 1;
    }
  }

  for (const key of Object.keys(byTierMatchup)) {
    const item = byTierMatchup[key];
    item.accuracy = item.matches > 0 ? parseFloat(((item.correct / item.matches) * 100).toFixed(1)) : 0;
  }

  // residuals
  const residualsA = results.map(r => r.actualGoalsA - r.lambda_A);
  const residualsB = results.map(r => r.actualGoalsB - r.lambda_B);

  const meanResidual_A = totalMatches > 0 ? residualsA.reduce((s, v) => s + v, 0) / totalMatches : 0;
  const meanResidual_B = totalMatches > 0 ? residualsB.reduce((s, v) => s + v, 0) / totalMatches : 0;

  const stdResidual_A = totalMatches > 0 ? Math.sqrt(residualsA.reduce((s, v) => s + Math.pow(v - meanResidual_A, 2), 0) / totalMatches) : 0;
  const stdResidual_B = totalMatches > 0 ? Math.sqrt(residualsB.reduce((s, v) => s + Math.pow(v - meanResidual_B, 2), 0) / totalMatches) : 0;

  const residuals = {
    meanResidual_A: parseFloat(meanResidual_A.toFixed(4)),
    meanResidual_B: parseFloat(meanResidual_B.toFixed(4)),
    stdResidual_A: parseFloat(stdResidual_A.toFixed(4)),
    stdResidual_B: parseFloat(stdResidual_B.toFixed(4))
  };

  // worstPredictions
  const sortedByError = [...results].sort((a, b) => b.error - a.error);
  const worstPredictions = sortedByError.slice(0, 5).map(r => ({
    match: `${r.homeTeam} vs ${r.awayTeam}`,
    predictedOutcome: r.predictedOutcome,
    predictedOutcomePct: r.predictedOutcomeProbability,
    actualOutcome: r.actualOutcome,
    actualScore: r.actualScore,
    error: r.error
  }));

  // bestPredictions
  const correctMatches = results.filter(r => r.outcomeCorrect && (r.exactScoreCorrect || r.inTop5));
  correctMatches.sort((a, b) => b.actualOutcomeProbability - a.actualOutcomeProbability);
  const bestPredictions = correctMatches.slice(0, 5).map(r => ({
    match: `${r.homeTeam} vs ${r.awayTeam}`,
    predictedOutcome: r.predictedOutcome,
    predictedOutcomePct: r.predictedOutcomeProbability,
    actualOutcome: r.actualOutcome,
    actualScore: r.actualScore,
    mostLikelyScoreline: r.mostLikelyScoreline,
    exactScoreCorrect: r.exactScoreCorrect,
    inTop5: r.inTop5
  }));

  const metrics = {
    overall,
    byOutcome,
    byMatchday,
    byTierMatchup,
    residuals,
    worstPredictions,
    bestPredictions
  };

  return { results, metrics };
}

// Auto-run execution block
const nodePath = process.argv[1];
if (nodePath) {
  const isDirectRun = path.resolve(nodePath) === path.resolve(__filename);
  if (isDirectRun) {
    (async () => {
      try {
        const { results, metrics } = await runBacktest();

        // Write full results to cache/backtest_results.json
        await fs.writeFile(RESULTS_FILE, JSON.stringify({ results, metrics }, null, 2), 'utf8');

        const dates = results.map(r => r.date).sort();
        const firstDate = dates[0] || "N/A";
        const lastDate = dates[dates.length - 1] || "N/A";

        console.log("=== ORACLE-26 BACKTEST REPORT ===");
        console.log(`Matches analysed: ${metrics.overall.totalMatches}`);
        console.log(`Date range: ${firstDate} to ${lastDate}\n`);

        console.log("OUTCOME ACCURACY");
        console.log(`  Overall: ${metrics.overall.outcomeAccuracy.toFixed(1)}% (${metrics.overall.outcomeCorrect}/${metrics.overall.totalMatches} correct)`);
        console.log(`  Home wins: ${metrics.byOutcome.HOME.accuracy.toFixed(1)}%`);
        console.log(`  Draws: ${metrics.byOutcome.DRAW.accuracy.toFixed(1)}%`);
        console.log(`  Away wins: ${metrics.byOutcome.AWAY.accuracy.toFixed(1)}%\n`);

        console.log("SCORELINE ACCURACY");
        console.log(`  Exact score: ${metrics.overall.exactScoreAccuracy.toFixed(1)}% (${metrics.overall.exactScoreCorrect}/${metrics.overall.totalMatches})`);
        console.log(`  Score in top 5: ${metrics.overall.top5Accuracy.toFixed(1)}% (${metrics.overall.inTop5}/${metrics.overall.totalMatches})\n`);

        console.log("GOAL MODEL CALIBRATION");
        const formatResidual = (v) => (v >= 0 ? `+${v.toFixed(2)}` : v.toFixed(2));
        console.log(`  Mean residual (home): ${formatResidual(metrics.residuals.meanResidual_A)} (positive = under-predicting)`);
        console.log(`  Mean residual (away): ${formatResidual(metrics.residuals.meanResidual_B)}`);
        console.log(`  Std deviation (home): ${metrics.residuals.stdResidual_A.toFixed(2)}`);
        console.log(`  Std deviation (away): ${metrics.residuals.stdResidual_B.toFixed(2)}\n`);

        console.log("BY ROUND");
        // Sort rounds numerically or alphabetically
        const rounds = Object.keys(metrics.byMatchday).sort((a, b) => {
          const numA = parseInt(a.replace(/\D/g, ''));
          const numB = parseInt(b.replace(/\D/g, ''));
          if (!isNaN(numA) && !isNaN(numB)) return numA - numB;
          return a.localeCompare(b);
        });
        for (const round of rounds) {
          const item = metrics.byMatchday[round];
          console.log(`  ${round}: ${item.accuracy.toFixed(1)}% (${item.correct}/${item.matches})`);
        }
        console.log("");

        console.log("BY TIER MATCHUP");
        const tierKeys = Object.keys(metrics.byTierMatchup).sort();
        for (const key of tierKeys) {
          const item = metrics.byTierMatchup[key];
          const [t1, t2] = key.split('v');
          console.log(`  Tier ${t1} vs Tier ${t2}: ${item.accuracy.toFixed(1)}% (${item.correct}/${item.matches})`);
        }
        console.log("");

        console.log("WORST PREDICTIONS");
        metrics.worstPredictions.forEach((w, i) => {
          console.log(`  ${i + 1}. ${w.match} — predicted ${w.predictedOutcome} (${w.predictedOutcomePct.toFixed(0)}%), actual ${w.actualOutcome} (Score: ${w.actualScore})`);
        });
        console.log("");

        console.log("BEST PREDICTIONS");
        metrics.bestPredictions.forEach((b, i) => {
          const scoreDetail = b.exactScoreCorrect ? `Exact Score: ${b.actualScore}` : `Top 5 Score: ${b.mostLikelyScoreline}`;
          console.log(`  ${i + 1}. ${b.match} — predicted ${b.predictedOutcome} (${b.predictedOutcomePct.toFixed(0)}%), actual ${b.actualOutcome} [${scoreDetail}]`);
        });

      } catch (err) {
        console.error("Backtester execution error:", err);
      }
    })();
  }
}
