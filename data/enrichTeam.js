// Run with: node data/enrichTeam.js

import fs from 'fs';
import { getTeamForm, getTeamStats, getH2HResults, getFixture, STADIUM_CAPACITIES } from './openFootballLayer.js';
import { TEAMS } from './index.js';

export async function enrichTeamWithLiveData(teamObject) {
  if (!teamObject) return null;
  // Clone the team object to prevent mutating original
  const team = JSON.parse(JSON.stringify(teamObject));

  const form = await getTeamForm(team.id);
  if (form && form.length >= 1) {
    team.last_6 = form.map(f => f.result);
  }

  const liveStats = await getTeamStats(team.id);
  team.liveStats = liveStats;
  team.live2026H2H = null;
  team.matchesPlayedInTournament = liveStats ? liveStats.matchesPlayed : 0;
  team.hasLiveData = team.matchesPlayedInTournament >= 1;

  return team;
}

export async function enrichMatchup(teamAObject, teamBObject) {
  const enrichedA = await enrichTeamWithLiveData(teamAObject);
  const enrichedB = await enrichTeamWithLiveData(teamBObject);

  const h2hResults = await getH2HResults(enrichedA.id, enrichedB.id);
  enrichedA.live2026H2H = h2hResults;
  enrichedB.live2026H2H = h2hResults;

  const fixture = await getFixture(enrichedA.id, enrichedB.id);
  if (fixture) {
    enrichedA.isHome = (fixture.homeTeamCode === enrichedA.id);
    enrichedB.isHome = (fixture.homeTeamCode === enrichedB.id);
    enrichedA.ground = fixture.ground;
    enrichedB.ground = fixture.ground;
    enrichedA.fixtureDate = fixture.date;
    enrichedB.fixtureDate = fixture.date;
  } else {
    console.warn(`Warning: No scheduled fixture found between ${enrichedA.id} and ${enrichedB.id}. Defaulting ${enrichedA.id} as home.`);
    enrichedA.isHome = true;
    enrichedB.isHome = false;
    enrichedA.ground = "Unknown Stadium";
    enrichedB.ground = "Unknown Stadium";
    enrichedA.fixtureDate = null;
    enrichedB.fixtureDate = null;
  }

  let crowd_factor = 0.75;  // neutral venue default
  
  if (fixture && fixture.attendance) {
    const attendance = parseInt(fixture.attendance);
    const capacity = STADIUM_CAPACITIES[fixture.ground] 
                  || STADIUM_CAPACITIES[fixture.venue]
                  || 70000;
    crowd_factor = Math.min(1.0, attendance / capacity);
  }
  
  enrichedA.crowd_factor = crowd_factor;
  enrichedB.crowd_factor = crowd_factor;

  const lineupResult = getLineupAbsences(enrichedA.id, enrichedB.id);
  if (lineupResult && lineupResult.hasData) {
    if (lineupResult.homeAbsences) {
      if (!enrichedA.injuries || enrichedA.injuries.length === 0) {
        enrichedA.injuries = ["lineup_absence"];
      }
    }
    if (lineupResult.awayAbsences) {
      if (!enrichedB.injuries || enrichedB.injuries.length === 0) {
        enrichedB.injuries = ["lineup_absence"];
      }
    }
    console.log(`[LINEUP] Data found for ${enrichedA.id} vs ${enrichedB.id} — homeAbsences: ${lineupResult.homeAbsences}, awayAbsences: ${lineupResult.awayAbsences}`);
  }

  return { enrichedA, enrichedB, h2hResults, fixture };
}

export const CALIBRATION_CONSTANTS = {
  home_residual_correction: 0.20,  // from backtest
  away_residual_correction: 0.05  // from backtest
};


export function getLambdaOverride(enrichedTeam, P_dynamic, isHome) {
  if (!enrichedTeam) {
    const defaultLambda = Math.max(0.1, 1.8 * P_dynamic + 0.27);
    const residual_adj = isHome ? 0.54 * 0.65 : -0.27 * 0.3;
    return Math.max(0.1, defaultLambda + residual_adj);
  }
  
  let lambda;
  if (enrichedTeam.hasLiveData && enrichedTeam.matchesPlayedInTournament >= 2) {
    const avgGoalsFor = enrichedTeam.liveStats ? enrichedTeam.liveStats.avgGoalsFor : 0;
    lambda = (avgGoalsFor * 0.6) + (1.8 * P_dynamic + 0.27) * 0.4;
  } else {
    lambda = 1.8 * P_dynamic + 0.27;
  }

  const residual_adj = isHome ? 0.54 * 0.65 : -0.27 * 0.3;
  return Math.max(0.1, lambda + residual_adj);
}

// Poisson probability helpers
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

export function recomputeScorelines(lambda_A, lambda_B) {
  const matrix = [];
  let sumProb = 0.0;
  for (let i = 0; i <= 6; i++) {
    for (let j = 0; j <= 6; j++) {
      const prob = poissonPMF(i, lambda_A) * poissonPMF(j, lambda_B);
      matrix.push({ scoreA: i, scoreB: j, probability: prob });
      sumProb += prob;
    }
  }
  matrix.sort((a, b) => b.probability - a.probability);
  const top5 = matrix.slice(0, 5);
  const mostLikelyScoreline = `${top5[0].scoreA}-${top5[0].scoreB}`;
  return { top5, mostLikelyScoreline, sumProb };
}

// Auto-run block
const isNode = typeof window === 'undefined';
if (isNode) {
  const nodePath = process.argv[1];
  if (nodePath) {
    (async () => {
      const pathModule = await import('path');
      const urlModule = await import('url');
      const path = pathModule.default;
      const fileURLToPath = urlModule.fileURLToPath;
      
      const __filename = fileURLToPath(import.meta.url);
      const isDirectRun = path.resolve(nodePath) === path.resolve(__filename);
      
      if (isDirectRun) {
        console.log("=== data/enrichTeam.js self-test execution ===");
        
        const teamMEX = TEAMS.find(t => t.id === "MEX");
        const teamKOR = TEAMS.find(t => t.id === "KOR");
        const teamDEN = TEAMS.find(t => t.id === "DEN");

        if (!teamMEX || !teamKOR || !teamDEN) {
          console.error("Error: Could not find MEX, KOR, or DEN team data.");
          return;
        }

        console.log("\n--- TEST 1: Enrich Matchup MEX vs KOR (Both have live data) ---");
        const test1 = await enrichMatchup(teamMEX, teamKOR);
        console.log("MEX enriched properties:");
        console.log({
          id: test1.enrichedA.id,
          hasLiveData: test1.enrichedA.hasLiveData,
          matchesPlayedInTournament: test1.enrichedA.matchesPlayedInTournament,
          last_6: test1.enrichedA.last_6,
          liveStats: test1.enrichedA.liveStats
        });
        console.log("KOR enriched properties:");
        console.log({
          id: test1.enrichedB.id,
          hasLiveData: test1.enrichedB.hasLiveData,
          matchesPlayedInTournament: test1.enrichedB.matchesPlayedInTournament,
          last_6: test1.enrichedB.last_6,
          liveStats: test1.enrichedB.liveStats
        });

        console.log("\n--- TEST 2: Enrich Matchup MEX vs DEN (DEN has 0 matches) ---");
        const test2 = await enrichMatchup(teamMEX, teamDEN);
        console.log("DEN original last_6:", teamDEN.last_6);
        console.log("DEN enriched properties:");
        console.log({
          id: test2.enrichedB.id,
          hasLiveData: test2.enrichedB.hasLiveData,
          matchesPlayedInTournament: test2.enrichedB.matchesPlayedInTournament,
          last_6: test2.enrichedB.last_6,
          liveStats: test2.enrichedB.liveStats
        });

        console.log("\n--- TEST 3: Lambda Override Verification ---");
        const pDynamicMEX = 0.6;
        const pDynamicDEN = 0.4;
        
        const defaultLambdaMEX = 1.8 * pDynamicMEX + 0.27;
        const defaultLambdaDEN = 1.8 * pDynamicDEN + 0.27;
        
        const overrideMEX = getLambdaOverride(test1.enrichedA, pDynamicMEX, true);
        const overrideDEN = getLambdaOverride(test2.enrichedB, pDynamicDEN, false);

        console.log(`MEX (with live data, played >= 2 matches, P_dynamic = ${pDynamicMEX}):`);
        console.log(`  - Default lambda: ${defaultLambdaMEX.toFixed(4)}`);
        console.log(`  - Overridden lambda: ${overrideMEX.toFixed(4)}`);
        console.log(`  - Average goals for: ${test1.enrichedA.liveStats.avgGoalsFor}`);

        console.log(`DEN (no live data, P_dynamic = ${pDynamicDEN}):`);
        console.log(`  - Default lambda: ${defaultLambdaDEN.toFixed(4)}`);
        console.log(`  - Overridden lambda: ${overrideDEN.toFixed(4)}`);

        console.log("\n=== Self-test Completed ===");
      }
    })();
  }
}

export function getFixtureByTeamCodes(codeA, codeB) {
  if (typeof window !== 'undefined') {
    return null;
  }
  
  try {
    const fileUrl = new URL('../public/data/scraped/fixtures.json', import.meta.url);
    const content = fs.readFileSync(fileUrl, 'utf8');
    const fixtures = JSON.parse(content);
    
    const nameToCode = Object.fromEntries(TEAMS.map(t => [t.name, t.id]));
    
    for (const f of fixtures) {
      const homeCode = nameToCode[f.home_team];
      const awayCode = nameToCode[f.away_team];
      
      if (!homeCode) {
        console.warn(`Warning: No team code found for home team name "${f.home_team}"`);
        continue;
      }
      if (!awayCode) {
        console.warn(`Warning: No team code found for away team name "${f.away_team}"`);
        continue;
      }
      
      if ((homeCode === codeA && awayCode === codeB) || (homeCode === codeB && awayCode === codeA)) {
        return {
          match_id: f.match_id,
          homeCode,
          awayCode,
          kickoff_utc: f.kickoff_utc,
          stage: f.stage,
          venue: f.venue,
          attendance: f.attendance,
          result: f.result
        };
      }
    }
  } catch (e) {
    console.error("Error reading fixtures in getFixtureByTeamCodes:", e);
  }
  
  return null;
}

export function getLineupAbsences(codeA, codeB) {
  if (typeof window !== 'undefined') {
    return null;
  }
  
  try {
    const fileUrl = new URL('../public/data/scraped/lineups.json', import.meta.url);
    const content = fs.readFileSync(fileUrl, 'utf8');
    const lineups = JSON.parse(content);
    
    if (!lineups || Object.keys(lineups).length === 0) {
      return null;
    }
    
    for (const key of Object.keys(lineups)) {
      const entry = lineups[key];
      if ((entry.home === codeA && entry.away === codeB) || (entry.home === codeB && entry.away === codeA)) {
        const homeAbsences = (entry.home_starters || []).length < 9;
        const awayAbsences = (entry.away_starters || []).length < 9;
        
        return {
          hasData: true,
          homeAbsences,
          awayAbsences,
          homeStarters: entry.home_starters || [],
          awayStarters: entry.away_starters || []
        };
      }
    }
    
    return { hasData: false };
  } catch (e) {
    console.error("Error reading lineups in getLineupAbsences:", e);
    return null;
  }
}

