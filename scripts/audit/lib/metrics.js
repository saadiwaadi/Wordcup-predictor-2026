const EPS = 1e-15;

function oneHot(outcome) {
  return {
    A: outcome === 'A' ? 1 : 0,
    D: outcome === 'D' ? 1 : 0,
    B: outcome === 'B' ? 1 : 0,
  };
}

function predictedOutcome(r) {
  if (r.winA_pct >= r.draw_pct && r.winA_pct >= r.winB_pct) return 'A';
  if (r.winB_pct >= r.draw_pct && r.winB_pct >= r.winA_pct) return 'B';
  return 'D';
}

// rows: array of { predicted: {winA_pct, draw_pct, winB_pct, mostLikelyScoreline}, actual: {scoreA, scoreB, outcome} }
export function computeMetrics(rows) {
  const ok = rows.filter(r => r.status === 'ok');
  const n = ok.length;

  if (n === 0) {
    return {
      n: 0, failedCount: rows.length - n,
      outcomeAccuracy: null, brierScore: null, logLoss: null, ece: null,
      scorelineAccuracy: null, meanTotalGoals: null, varTotalGoals: null,
    };
  }

  let correctOutcomes = 0;
  let brierSum = 0;
  let logLossSum = 0;
  let correctScorelines = 0;
  const totalGoalsSamples = [];

  const buckets = [
    { label: '50-60%', min: 0.5, max: 0.6, sumConf: 0, sumAcc: 0, count: 0 },
    { label: '60-70%', min: 0.6, max: 0.7, sumConf: 0, sumAcc: 0, count: 0 },
    { label: '70-80%', min: 0.7, max: 0.8, sumConf: 0, sumAcc: 0, count: 0 },
    { label: '80-90%', min: 0.8, max: 0.9, sumConf: 0, sumAcc: 0, count: 0 },
    { label: '90-95%', min: 0.9, max: 0.95, sumConf: 0, sumAcc: 0, count: 0 },
  ];

  ok.forEach(r => {
    const p = r.predicted;
    const a = r.actual;
    const P_A = p.winA_pct / 100, P_D = p.draw_pct / 100, P_B = p.winB_pct / 100;
    const O = oneHot(a.outcome);

    const predOutcome = predictedOutcome(p);
    if (predOutcome === a.outcome) correctOutcomes++;

    brierSum += Math.pow(P_A - O.A, 2) + Math.pow(P_D - O.D, 2) + Math.pow(P_B - O.B, 2);

    const pA = Math.min(Math.max(P_A, EPS), 1 - EPS);
    const pD = Math.min(Math.max(P_D, EPS), 1 - EPS);
    const pB = Math.min(Math.max(P_B, EPS), 1 - EPS);
    logLossSum += -(O.A * Math.log(pA) + O.D * Math.log(pD) + O.B * Math.log(pB));

    if (p.mostLikelyScoreline === `${a.scoreA}-${a.scoreB}`) correctScorelines++;

    totalGoalsSamples.push(p.lambda_A + p.lambda_B);

    const maxConf = Math.max(P_A, P_D, P_B);
    const bucket = buckets.find(b => maxConf >= b.min && maxConf < b.max) ||
      (maxConf >= 0.95 ? null : buckets.find(b => maxConf >= b.min && maxConf <= b.max));
    if (bucket) {
      bucket.sumConf += maxConf;
      bucket.sumAcc += (predOutcome === a.outcome) ? 1 : 0;
      bucket.count += 1;
    }
  });

  let eceSum = 0;
  const bucketReport = buckets.map(b => {
    if (b.count === 0) return { label: b.label, count: 0, avgConfidence: null, avgAccuracy: null };
    const avgConfidence = b.sumConf / b.count;
    const avgAccuracy = b.sumAcc / b.count;
    eceSum += (b.count / n) * Math.abs(avgConfidence - avgAccuracy);
    return { label: b.label, count: b.count, avgConfidence, avgAccuracy };
  });

  const mean = totalGoalsSamples.reduce((s, v) => s + v, 0) / n;
  const variance = totalGoalsSamples.reduce((s, v) => s + Math.pow(v - mean, 2), 0) / n;

  return {
    n,
    failedCount: rows.length - n,
    outcomeAccuracy: correctOutcomes / n,
    brierScore: brierSum / n,
    logLoss: logLossSum / n,
    ece: eceSum,
    eceBuckets: bucketReport,
    scorelineAccuracy: correctScorelines / n,
    meanTotalGoals: mean,
    varTotalGoals: variance,
  };
}
