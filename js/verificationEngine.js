import { getCache, getFixture } from '../data/openFootballLayer.js';
import { TEAMS } from '../data/index.js';
import { runPrediction } from '../engine.js';
import { getLambdaOverride, recomputeScorelines } from '../data/enrichTeam.js';
import * as openFootball from '../data/openFootballLayer.js';

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

export async function runLiveBacktest() {
  // Silent refresh cache check (isNode checks inside will return early)
  if (typeof openFootball.refreshCache === 'function') {
    try {
      await openFootball.refreshCache();
    } catch (e) {
      console.warn("Silent failed to refresh cache inside live backtest:", e);
    }
  }

  const cache = await getCache();
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
    const newLambdaA = getLambdaOverride(enrichedA, prediction.P_dynamic_A, isAHome, enrichedB);
    const newLambdaB = getLambdaOverride(enrichedB, prediction.P_dynamic_B, isBHome, enrichedA);

    if (newLambdaA !== prediction.lambda_A || newLambdaB !== prediction.lambda_B) {
      prediction.lambda_A = newLambdaA;
      prediction.lambda_B = newLambdaB;
      const recomputed = recomputeScorelines(newLambdaA, newLambdaB);
      prediction.top5 = recomputed.top5;
      prediction.mostLikelyScoreline = recomputed.mostLikelyScoreline;
      prediction.sumProb = recomputed.sumProb;
    }

    // Assign prediction directly (draw correction removed in favor of Dixon-Coles)
    const correctedPrediction = prediction;

    // Outcomes mapping (reverted simple logic)
    const winA_pct = correctedPrediction.winA_pct;
    const winB_pct = correctedPrediction.winB_pct;
    const draw_pct = correctedPrediction.draw_pct;

    let predictedOutcome;
    if (draw_pct >= winA_pct && draw_pct >= winB_pct) {
      predictedOutcome = 'DRAW';
    } else if (winA_pct >= winB_pct) {
      predictedOutcome = 'HOME';
    } else {
      predictedOutcome = 'AWAY';
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
      actualGoalsB: match.score.ft[1],
      top5: correctedPrediction.top5,
      hasLiveData: enrichedA.hasLiveData || enrichedB.hasLiveData
    });
  }

  // Compute Metrics
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

  const sortedByError = [...results].sort((a, b) => b.error - a.error);
  const worstPredictions = sortedByError.slice(0, 5).map(r => ({
    match: `${r.homeTeam} vs ${r.awayTeam}`,
    predictedOutcome: r.predictedOutcome,
    predictedOutcomePct: r.predictedOutcomeProbability,
    actualOutcome: r.actualOutcome,
    actualScore: r.actualScore,
    error: r.error
  }));

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

  // --- STATISTICAL VALIDATION TESTS ---
  const buckets = ['45-50%', '50-55%', '55-60%', '60-65%', '65-70%', '70%+'];
  const bucketStats = {};
  buckets.forEach(b => {
    bucketStats[b] = { total: 0, correct: 0 };
  });

  results.forEach(r => {
    const p = r.predictedOutcomeProbability;
    let bucket = null;
    if (p >= 45 && p < 50) bucket = '45-50%';
    else if (p >= 50 && p < 55) bucket = '50-55%';
    else if (p >= 55 && p < 60) bucket = '55-60%';
    else if (p >= 60 && p < 65) bucket = '60-65%';
    else if (p >= 65 && p < 70) bucket = '65-70%';
    else if (p >= 70) bucket = '70%+';

    if (bucket) {
      bucketStats[bucket].total++;
      if (r.outcomeCorrect) {
        bucketStats[bucket].correct++;
      }
    }
  });

  const midpoints = {
    '45-50%': 47.5,
    '50-55%': 52.5,
    '55-60%': 57.5,
    '60-65%': 62.5,
    '65-70%': 67.5,
    '70%+': 75.0
  };
  const activeBuckets = buckets.filter(b => bucketStats[b].total > 0);
  let trend = 'FLAT';
  if (activeBuckets.length >= 2) {
    let sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
    activeBuckets.forEach(b => {
      const x = midpoints[b];
      const y = (bucketStats[b].correct / bucketStats[b].total) * 100;
      sumX += x;
      sumY += y;
      sumXY += x * y;
      sumXX += x * x;
    });
    const N = activeBuckets.length;
    const num = N * sumXY - sumX * sumY;
    if (num > 0.1) trend = 'IMPROVING';
    else if (num < -0.1) trend = 'DEGRADING';
  }

  // Baseline A: Always Home
  const homeCorrect = results.filter(r => r.actualOutcome === 'HOME').length;
  const alwaysHomeAcc = totalMatches > 0 ? (homeCorrect / totalMatches) * 100 : 0;

  // Baseline B: Always Favorite (lower FIFA rank wins, predict HOME if equal)
  let fifaCorrect = 0;
  results.forEach(r => {
    const teamAObj = TEAMS.find(t => t.id === r.homeTeam);
    const teamBObj = TEAMS.find(t => t.id === r.awayTeam);
    let pred = 'HOME';
    if (teamAObj && teamBObj) {
      if (teamAObj.fifa_rank < teamBObj.fifa_rank) pred = 'HOME';
      else if (teamBObj.fifa_rank < teamAObj.fifa_rank) pred = 'AWAY';
    }
    if (pred === r.actualOutcome) {
      fifaCorrect++;
    }
  });
  const fifaRankAcc = totalMatches > 0 ? (fifaCorrect / totalMatches) * 100 : 0;

  // Baseline C: Pure Random
  let totalRandomCorrect = 0;
  const randOptions = ['HOME', 'DRAW', 'AWAY'];
  for (let sim = 0; sim < 1000; sim++) {
    results.forEach(r => {
      const randPred = randOptions[Math.floor(Math.random() * 3)];
      if (randPred === r.actualOutcome) {
        totalRandomCorrect++;
      }
    });
  }
  const randomChanceAcc = totalMatches > 0 ? (totalRandomCorrect / (1000 * totalMatches)) * 100 : 0;

  const oracle26Acc = overall.outcomeAccuracy;

  // Test 3: Brier Score
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

  let brierInterpretation = 'POOR';
  if (brierScore < 0.4) brierInterpretation = 'EXCELLENT';
  else if (brierScore <= 0.5) brierInterpretation = 'GOOD';
  else if (brierScore <= 0.6) brierInterpretation = 'FAIR';

  const beatsRandom = oracle26Acc > randomChanceAcc;
  const beatsHome = oracle26Acc > alwaysHomeAcc;
  const beatsFIFA = oracle26Acc > fifaRankAcc;
  const goodBrier = brierScore < 0.5;

  let verdict = 'NO SIGNAL';
  if (!beatsRandom) {
    verdict = 'NO SIGNAL';
  } else {
    if (beatsHome && beatsFIFA && goodBrier) {
      verdict = 'STRONG SIGNAL';
    } else if (oracle26Acc - randomChanceAcc <= 3) {
      verdict = 'WEAK SIGNAL';
    } else {
      verdict = 'MODERATE SIGNAL';
    }
  }

  const metrics = {
    overall,
    byOutcome,
    byMatchday,
    byTierMatchup,
    residuals,
    worstPredictions,
    bestPredictions,
    calibration: {
      buckets,
      bucketStats,
      trend
    },
    baselines: {
      randomChanceAcc,
      alwaysHomeAcc,
      fifaRankAcc,
      oracle26Acc,
      vsRandom: oracle26Acc - randomChanceAcc,
      vsHome: oracle26Acc - alwaysHomeAcc,
      vsFIFA: oracle26Acc - fifaRankAcc
    },
    brier: {
      score: brierScore,
      interpretation: brierInterpretation
    },
    verdict
  };

  return { results, metrics };
}
