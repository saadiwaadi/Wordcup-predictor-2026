// engine.js - Core prediction calculations for ORACLE-26
import { getH2H } from './data/index.js';

export const RHO = -0.04;

// Helper: factorial for Poisson
const FACTORIALS = [1, 1, 2, 6, 24, 120, 720];
function factorial(n) {
  if (n < 0) return 1;
  if (n <= 6) return FACTORIALS[n];
  let res = 1;
  for (let i = 2; i <= n; i++) res *= i;
  return res;
}

// Poisson Probability Mass Function
function poissonPMF(k, lambda) {
  return (Math.exp(-lambda) * Math.pow(lambda, k)) / factorial(k);
}

// Layer 1: Static Strength
function calculateStaticStrength(teamA, teamB) {
  // Elo win probability
  const P_elo = 1 / (1 + Math.pow(10, -(teamA.elo - teamB.elo) / 400));

  // FIFA ranking points
  const pts_A = Math.max(0, 200 - teamA.fifa_rank * 3);
  const pts_B = Math.max(0, 200 - teamB.fifa_rank * 3);
  const P_fifa = 1 / (1 + Math.exp(-(pts_A - pts_B) / 291.5));

  // Market value win probability
  const ratio_val = teamA.market_value_m / teamB.market_value_m;
  const P_val = 1 / (1 + Math.exp(-Math.log(ratio_val) / 1.3026));

  const crowd_factor = teamA.crowd_factor || 0.75
  
  // Home advantage: base 3% + up to 8% from crowd
  // Only applies when one team has home advantage
  // For WC2026: USA, MEX, CAN are home nations
  
  const homeAdvantage = 0.03 + (crowd_factor * 0.08)
  
  const hostBonusA = teamA.host && teamA.isHome 
    ? homeAdvantage : 0.0
  const hostBonusB = teamB.host && teamB.isHome
    ? homeAdvantage : 0.0

  // Combined (weighted) for Team A
  let P_static_A = (P_elo * 1.0 + P_fifa * 0.5 + P_val * 0.25) / 1.75 + (hostBonusA - hostBonusB);
  P_static_A = Math.max(0.05, Math.min(0.95, P_static_A));

  // Combined for Team B
  let P_static_B = 1 - P_static_A;
  P_static_B = Math.max(0.05, Math.min(0.95, P_static_B));

  return { P_static_A, P_static_B };
}

// Helper: Form Score
function calculateFormRatio(team) {
  let score = 0;
  team.last_6.forEach(r => {
    if (r === "W") score += 3;
    else if (r === "D") score += 1;
  });
  return score / 18;
}

// Layer 2: Dynamic Form
function calculateDynamicForm(teamA, teamB, options) {
  const { P_static_A, P_static_B } = calculateStaticStrength(teamA, teamB);

  const ratioA = calculateFormRatio(teamA);
  const ratioB = calculateFormRatio(teamB);

  const FormDelta_A = ratioA - ratioB;
  const FormDelta_B = ratioB - ratioA;

  // Injury penalties
  const injury_penalty_A = options.injureKeyA ? 0.05 : 0.0;
  const injury_penalty_B = options.injureKeyB ? 0.05 : 0.0;

  // Elo momentum delta
  const eloDelta_A = teamA.elo_delta_90 / 100;
  const eloDelta_B = teamB.elo_delta_90 / 100;

  // Symmetric dynamic probabilities
  let P_dynamic_A = P_static_A * 0.65 + (0.5 + FormDelta_A * 0.5) * 0.35 - injury_penalty_A + injury_penalty_B * 0.5 + (eloDelta_A - eloDelta_B) * 0.02;
  P_dynamic_A = Math.max(0.05, Math.min(0.95, P_dynamic_A));

  let P_dynamic_B = P_static_B * 0.65 + (0.5 + FormDelta_B * 0.5) * 0.35 - injury_penalty_B + injury_penalty_A * 0.5 + (eloDelta_B - eloDelta_A) * 0.02;
  P_dynamic_B = Math.max(0.05, Math.min(0.95, P_dynamic_B));

  return { P_dynamic_A, P_dynamic_B, P_static_A, P_static_B };
}

// Main Prediction Engine
function runPrediction(teamA, teamB, options = {}) {
  // 1 & 2. Static & Dynamic Strengths
  const { P_dynamic_A, P_dynamic_B, P_static_A, P_static_B } = calculateDynamicForm(teamA, teamB, options);

  // 3. Expected Goals
  const lambda_A = Math.max(0.1, 1.8 * P_dynamic_A + 0.27);
  const lambda_B = Math.max(0.1, 1.8 * P_dynamic_B + 0.27);

  // 4. Scoreline Matrix (7x7)
  function dixonColesTau(i, j, lambda_A, lambda_B, rho) {
    if (i === 0 && j === 0) 
      return 1 - (lambda_A * lambda_B * rho);
    if (i === 1 && j === 0) 
      return 1 + (lambda_B * rho);
    if (i === 0 && j === 1) 
      return 1 + (lambda_A * rho);
    if (i === 1 && j === 1) 
      return 1 - rho;
    return 1.0;
  }

  const matrix = [];
  let sumProb = 0.0;
  for (let i = 0; i <= 6; i++) {
    for (let j = 0; j <= 6; j++) {
      const tau = dixonColesTau(i, j, lambda_A, lambda_B, RHO);
      const prob = poissonPMF(i, lambda_A) * poissonPMF(j, lambda_B) * tau;
      matrix.push({ scoreA: i, scoreB: j, probability: prob });
      sumProb += prob;
    }
  }

  // Normalize the matrix after building it (Dixon-Coles adjustment normalization)
  const totalProb = matrix.reduce((sum, cell) => sum + cell.probability, 0);
  matrix.forEach(cell => {
    cell.probability = cell.probability / totalProb;
  });

  // Sort by probability descending
  matrix.sort((a, b) => b.probability - a.probability);

  // Top 5 scorelines
  const top5 = matrix.slice(0, 5);
  const mostLikelyScoreline = `${top5[0].scoreA}-${top5[0].scoreB}`;

  // Gaussian draw probability (outcome prediction)
  const P_draw = (1/3) * Math.exp(
    -Math.pow(P_dynamic_A - 0.5, 2) / 
    (2 * Math.pow(0.28, 2))
  )

  const raw_win_A = P_dynamic_A * (1 - P_draw)
  const raw_win_B = P_dynamic_B * (1 - P_draw)
  const total = raw_win_A + P_draw + raw_win_B

  const winA_pct = (raw_win_A / total) * 100
  const draw_pct = (P_draw / total) * 100
  const winB_pct = (raw_win_B / total) * 100

  // 6. Confidence Scoring
  let confidence = 100;

  if (teamA.tier === 4) confidence -= 20;
  if (teamB.tier === 4) confidence -= 20;

  if (teamA.wc_appearances < 3) confidence -= 15;
  if (teamB.wc_appearances < 3) confidence -= 15;

  // Check H2H
  const h2hData = getH2H(teamA, teamB);
  if (!h2hData) {
    confidence -= 10;
  }

  if (options.staleData) confidence -= 15;
  if (options.injureKeyA || options.injureKeyB) confidence -= 5;
  confidence -= 5; // Neutral venue deduction (always)

  confidence = Math.max(0, Math.min(100, confidence));

  let confidenceBand = "VERY LOW";
  if (confidence >= 85) confidenceBand = "HIGH";
  else if (confidence >= 65) confidenceBand = "MEDIUM";
  else if (confidence >= 45) confidenceBand = "LOW";

  // 7. Prediction Drivers
  const drivers = [];
  if (Math.abs(teamA.elo - teamB.elo) > 80) {
    const stronger = teamA.elo > teamB.elo ? teamA.name : teamB.name;
    const diff = Math.abs(teamA.elo - teamB.elo);
    drivers.push(`${stronger} holds Elo advantage (+${diff} pts)`);
  }

  const ratioA = calculateFormRatio(teamA);
  const ratioB = calculateFormRatio(teamB);
  if (Math.abs(ratioA - ratioB) > 0.2) {
    const betterForm = ratioA > ratioB ? teamA.name : teamB.name;
    drivers.push(`${betterForm} in significantly better recent form`);
  }

  if (options.injureKeyA) {
    drivers.push(`${teamA.name} missing key player — penalty applied`);
  }
  if (options.injureKeyB) {
    drivers.push(`${teamB.name} missing key player — penalty applied`);
  }

  if (teamA.host) {
    drivers.push(`${teamA.name} benefits from host nation advantage (+8%)`);
  }
  if (teamB.host) {
    drivers.push(`${teamB.name} benefits from host nation advantage (+8%)`);
  }

  if (drivers.length === 0) {
    drivers.push("Closely matched — within margin of error");
  }

  // H2H Info
  let h2hText = "No record found";
  let h2hNote = "";
  if (h2hData) {
    h2hText = `${teamA.name} ${h2hData.wins} — ${h2hData.draws} draw — ${h2hData.losses} ${teamB.name}`;
    h2hNote = h2hData.note || "No notable notes in archive.";
  }

  return {
    winA_pct,
    draw_pct,
    winB_pct,
    lambda_A,
    lambda_B,
    top5,
    mostLikelyScoreline,
    confidence,
    confidenceBand,
    drivers,
    h2hText,
    h2hNote,
    P_static_A,
    P_static_B,
    P_dynamic_A,
    P_dynamic_B,
    sumProb
  };
}

export { runPrediction };

