import { runPrediction } from './engine.js';
import { TEAMS } from './data/index.js';

const ACTUAL_RESULTS = [
  {
    teamA: "MEX",
    teamB: "RSA",
    stage: "Group",
    actualGoalsA: 2,
    actualGoalsB: 0,
    actualOutcome: "A"
  },
  {
    teamA: "KOR",
    teamB: "CZE",
    stage: "Group",
    actualGoalsA: 2,
    actualGoalsB: 1,
    actualOutcome: "A"
  },
  {
    teamA: "CAN",
    teamB: "BIH",
    stage: "Group",
    actualGoalsA: 1,
    actualGoalsB: 1,
    actualOutcome: "D"
  },
  {
    teamA: "USA",
    teamB: "PAR",
    stage: "Group",
    actualGoalsA: 4,
    actualGoalsB: 1,
    actualOutcome: "A"
  },
  {
    teamA: "QAT",
    teamB: "SUI",
    stage: "Group",
    actualGoalsA: 1,
    actualGoalsB: 1,
    actualOutcome: "D"
  },
  {
    teamA: "BRA",
    teamB: "MAR",
    stage: "Group",
    actualGoalsA: 1,
    actualGoalsB: 1,
    actualOutcome: "D"
  },
  {
    teamA: "SCO",
    teamB: "HAI",
    stage: "Group",
    actualGoalsA: 1,
    actualGoalsB: 0,
    actualOutcome: "A"
  },
  {
    teamA: "AUS",
    teamB: "TUR",
    stage: "Group",
    actualGoalsA: 2,
    actualGoalsB: 0,
    actualOutcome: "A"
  },
  {
    teamA: "GER",
    teamB: "CUW",
    stage: "Group",
    actualGoalsA: 7,
    actualGoalsB: 1,
    actualOutcome: "A"
  },
  {
    teamA: "CIV",
    teamB: "ECU",
    stage: "Group",
    actualGoalsA: 1,
    actualGoalsB: 0,
    actualOutcome: "A"
  },
  {
    teamA: "NED",
    teamB: "JPN",
    stage: "Group",
    actualGoalsA: 2,
    actualGoalsB: 2,
    actualOutcome: "D"
  },
  {
    teamA: "SWE",
    teamB: "TUN",
    stage: "Group",
    actualGoalsA: 5,
    actualGoalsB: 1,
    actualOutcome: "A"
  }
];

function runBacktest() {
  return ACTUAL_RESULTS.map(match => {
    const teamAObj = TEAMS.find(t => t.id === match.teamA);
    const teamBObj = TEAMS.find(t => t.id === match.teamB);

    if (!teamAObj || !teamBObj) {
      throw new Error(`Team object not found in TEAMS: ${match.teamA} or ${match.teamB}`);
    }

    const prediction = runPrediction(teamAObj, teamBObj, {
      stage: 'Group',
      injureKeyA: false,
      injureKeyB: false,
      staleData: false
    });

    const predictedWinA = prediction.winA_pct;
    const predictedDraw = prediction.draw_pct;
    const predictedWinB = prediction.winB_pct;
    const confidenceScore = prediction.confidence;

    let predictedOutcome = 'D';
    if (predictedWinA > predictedDraw && predictedWinA > predictedWinB) {
      predictedOutcome = 'A';
    } else if (predictedWinB > predictedWinA && predictedWinB > predictedDraw) {
      predictedOutcome = 'B';
    }

    const topScore = prediction.top5[0];
    const predictedTopScore = [topScore.scoreA, topScore.scoreB];

    const correct = predictedOutcome === match.actualOutcome;

    return {
      teamA: match.teamA,
      teamB: match.teamB,
      predictedOutcome,
      actualOutcome: match.actualOutcome,
      predictedWinA,
      predictedDraw,
      predictedWinB,
      predictedTopScore,
      actualGoalsA: match.actualGoalsA,
      actualGoalsB: match.actualGoalsB,
      correct,
      confidenceScore,
      lambda_A: prediction.lambda_A,
      lambda_B: prediction.lambda_B
    };
  });
}

function computeMetrics(backtestResults) {
  const totalMatches = backtestResults.length;
  if (totalMatches === 0) {
    return {
      totalMatches: 0,
      outcomesCorrect: 0,
      outcomeAccuracy: 0,
      avgConfidence: 0,
      correctByConfidenceBand: {
        HIGH: { correct: 0, total: 0 },
        MEDIUM: { correct: 0, total: 0 },
        LOW: { correct: 0, total: 0 },
        VERY_LOW: { correct: 0, total: 0 }
      },
      upsets: [],
      avgGoalDeltaA: 0,
      avgGoalDeltaB: 0
    };
  }

  let outcomesCorrect = 0;
  let sumConfidence = 0;
  let sumGoalDeltaA = 0;
  let sumGoalDeltaB = 0;

  const correctByConfidenceBand = {
    HIGH: { correct: 0, total: 0 },
    MEDIUM: { correct: 0, total: 0 },
    LOW: { correct: 0, total: 0 },
    VERY_LOW: { correct: 0, total: 0 }
  };

  const upsets = [];

  backtestResults.forEach(match => {
    if (match.correct) {
      outcomesCorrect++;
    }

    sumConfidence += match.confidenceScore;

    // Confidence band grouping
    let band = "VERY_LOW";
    if (match.confidenceScore >= 85) band = "HIGH";
    else if (match.confidenceScore >= 65) band = "MEDIUM";
    else if (match.confidenceScore >= 45) band = "LOW";

    correctByConfidenceBand[band].total++;
    if (match.correct) {
      correctByConfidenceBand[band].correct++;
    }

    // Upset check
    const actualWinnerProb =
      match.actualOutcome === 'A' ? match.predictedWinA :
      match.actualOutcome === 'B' ? match.predictedWinB :
      match.predictedDraw; // actualOutcome === 'D'

    if (!match.correct && actualWinnerProb < 35) {
      upsets.push(match);
    }

    // Goal Deltas
    sumGoalDeltaA += Math.abs(match.lambda_A - match.actualGoalsA);
    sumGoalDeltaB += Math.abs(match.lambda_B - match.actualGoalsB);
  });

  const outcomeAccuracy = (outcomesCorrect / totalMatches) * 100;
  const avgConfidence = sumConfidence / totalMatches;
  const avgGoalDeltaA = sumGoalDeltaA / totalMatches;
  const avgGoalDeltaB = sumGoalDeltaB / totalMatches;

  return {
    totalMatches,
    outcomesCorrect,
    outcomeAccuracy,
    avgConfidence,
    correctByConfidenceBand,
    upsets,
    avgGoalDeltaA,
    avgGoalDeltaB
  };
}

function diagnoseWeaknesses(backtestResults) {
  const total = backtestResults.length;
  if (total === 0) return [];

  // 1. Draws underestimated
  const draws = backtestResults.filter(m => m.actualOutcome === 'D');
  const drawTotal = draws.length;
  const drawMissed = draws.filter(m => m.predictedOutcome !== 'D').length;

  // 2. Overconfident on heavy favorites
  // Define heavy favorites as predicted win% >= 45% for the predicted winner
  const favoritesLost = backtestResults.filter(m => {
    if (m.correct) return false;
    if (m.predictedOutcome === 'A') return m.predictedWinA >= 45;
    if (m.predictedOutcome === 'B') return m.predictedWinB >= 45;
    return false;
  });
  const totalFavLost = favoritesLost.length;
  const avgFavProb = totalFavLost > 0
    ? favoritesLost.reduce((sum, m) => sum + (m.predictedOutcome === 'A' ? m.predictedWinA : m.predictedWinB), 0) / totalFavLost
    : 0;

  // 3. Underdog wins (upsets)
  // An underdog win occurs when the team with the lower predicted win% actually wins
  const underdogWins = backtestResults.filter(m => {
    if (m.actualOutcome === 'A') return m.predictedWinA < m.predictedWinB;
    if (m.actualOutcome === 'B') return m.predictedWinB < m.predictedWinA;
    return false;
  });
  const N = underdogWins.length;
  const M = underdogWins.filter(m => !m.correct).length;

  // 4. Goal volume
  const totalPredGoals = backtestResults.reduce((sum, m) => sum + m.lambda_A + m.lambda_B, 0);
  const totalActualGoals = backtestResults.reduce((sum, m) => sum + m.actualGoalsA + m.actualGoalsB, 0);
  const avgX = totalPredGoals / total;
  const avgY = totalActualGoals / total;

  return [
    `Engine underestimates draws: ${drawMissed} out of ${drawTotal} draws predicted incorrectly`,
    `Engine overconfident on heavy favorites: avg predicted win% was ${avgFavProb.toFixed(1)}% for matches lost`,
    `Underdog wins (upsets): ${N} occurred, engine missed ${M} of them`,
    `Goal volume: engine predicts avg ${avgX.toFixed(2)} goals/match, actual avg is ${avgY.toFixed(2)}`
  ];
}

export { runBacktest, computeMetrics, diagnoseWeaknesses };
export default ACTUAL_RESULTS;
