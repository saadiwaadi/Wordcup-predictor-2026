// Variant B's xG-informed lambda path. Deliberately NOT inside engine.js and NOT
// calling app.js's getLambdaOverride()/recomputeScorelines() (Known Issue #4): that
// override layer is a separate, unrelated feature (weather/live-tournament-form
// adjustments) and its recomputeScorelines() omits the Dixon-Coles tau correction
// entirely — an inconsistency in the live app we deliberately do not inherit here.
// This module re-implements the same Poisson + tau + normalization math as
// engine.js's internal runPrediction() (RHO = -0.04, same 7x7 matrix, same
// normalization), applied only to the two enriched lambdas, so Variant B's
// scoreline output stays methodologically consistent with Variant A's.

const FACTORIALS = [1, 1, 2, 6, 24, 120, 720];
function factorial(n) {
  if (n < 0) return 1;
  if (n <= 6) return FACTORIALS[n];
  let res = 1;
  for (let i = 2; i <= n; i++) res *= i;
  return res;
}
function poissonPMF(k, lambda) {
  return (Math.exp(-lambda) * Math.pow(lambda, k)) / factorial(k);
}
function dixonColesTau(i, j, lambda_A, lambda_B, rho) {
  if (i === 0 && j === 0) return 1 - (lambda_A * lambda_B * rho);
  if (i === 1 && j === 0) return 1 + (lambda_B * rho);
  if (i === 0 && j === 1) return 1 + (lambda_A * rho);
  if (i === 1 && j === 1) return 1 - rho;
  return 1.0;
}

// NEW, unvalidated parameter for this audit only — not part of the frozen model.
// The spec's own suggested default (0.5/0.5 blend of original vs xG-implied lambda).
export const XG_BLEND_WEIGHT = 0.5;

export function calculateXGAdjustedLambda(lambdaOriginal, ownRollingXgScored, opponentRollingXgConceded, blendWeight = XG_BLEND_WEIGHT) {
  if (ownRollingXgScored == null || opponentRollingXgConceded == null) {
    // No causal xG history available yet (should not happen post-match-1, since
    // match_prediction_features.csv seeds a neutral prior for first matches, but
    // guarded defensively) — fall back to the original lambda, unblended.
    return { lambda: lambdaOriginal, blended: false, xgBasedLambda: null, blendWeight };
  }
  const xgBasedLambda = (ownRollingXgScored + opponentRollingXgConceded) / 2;
  const lambda = Math.max(0.1, lambdaOriginal * (1 - blendWeight) + xgBasedLambda * blendWeight);
  return { lambda, blended: true, xgBasedLambda, blendWeight };
}

export function recomputeScorelinesWithTau(lambda_A, lambda_B, RHO) {
  const matrix = [];
  for (let i = 0; i <= 6; i++) {
    for (let j = 0; j <= 6; j++) {
      const tau = dixonColesTau(i, j, lambda_A, lambda_B, RHO);
      const prob = poissonPMF(i, lambda_A) * poissonPMF(j, lambda_B) * tau;
      matrix.push({ scoreA: i, scoreB: j, probability: prob });
    }
  }
  const totalProb = matrix.reduce((sum, cell) => sum + cell.probability, 0);
  matrix.forEach(cell => { cell.probability = cell.probability / totalProb; });
  matrix.sort((a, b) => b.probability - a.probability);
  const top5 = matrix.slice(0, 5);
  const mostLikelyScoreline = `${top5[0].scoreA}-${top5[0].scoreB}`;
  return { top5, mostLikelyScoreline, sumProb: totalProb };
}
