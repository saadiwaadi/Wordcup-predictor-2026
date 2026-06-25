// Run this with: node data/apiLayer.js

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from project root
dotenv.config({ path: path.join(__dirname, '../.env') });

const API_KEY = process.env.API_FOOTBALL_KEY;
const BASE_URL = 'https://v3.football.api-sports.io';
const LEAGUE = 1;
const SEASON = 2026;
const CACHE_DIR = path.join(__dirname, '../cache');
const ORACLE_CACHE_PATH = path.join(CACHE_DIR, 'oracle_cache.json');
const H2H_CACHE_PATH = path.join(CACHE_DIR, 'h2h_cache.json');
const CACHE_EXPIRY_MS = 48 * 60 * 60 * 1000; // 48 hours

// Mapping from internal team codes to API-Football numeric team IDs
const teamCodeToApiId = {
  "BRA": 6,
  "FRA": 2,
  "ENG": 10,
  "GER": 25,
  "ESP": 9,
  "ARG": 26,
  "POR": 27,
  "NED": 11,
  "BEL": 1,
  "CRO": 3,
  "SEN": 13,
  "MAR": 31,
  "JPN": 12,
  "USA": 16,
  "MEX": 15,
  "CAN": 14,
  "COL": 8,
  "URU": 7,
  "SUI": 17,
  "SRB": 1464,
  "DEN": 21,
  "AUT": 22,
  "TUR": 23,
  "KOR": 24,
  "POL": 28,
  "AUS": 29,
  "IRN": 30,
  "ECU": 1187,
  "NGR": 19,
  "GHA": 1504,
  "CMR": 1530,
  "EGY": 32,
  "ALG": 1395,
  "CIV": 1459,
  "SAU": 222,
  "QAT": 1561,
  "CRI": 1460,
  "PAN": 1461,
  "VEN": 1462,
  "CHI": 1465,
  "ROU": 1467,
  "UKR": 1083,
  "RSA": 1469,
  "CZE": 1470,
  "PAR": 1472,
  "SCO": 1473,
  "SWE": 1476,
  "TUN": 1477
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let apiLimitReached = false;

// Ensure cache directory and empty cache files exist
async function ensureCacheFilesExist() {
  try {
    await fs.mkdir(CACHE_DIR, { recursive: true });
  } catch (err) {
    // Ignore error if directory already exists
  }
  try {
    await fs.access(ORACLE_CACHE_PATH);
  } catch {
    await fs.writeFile(ORACLE_CACHE_PATH, '{}', 'utf8');
  }
  try {
    await fs.access(H2H_CACHE_PATH);
  } catch {
    await fs.writeFile(H2H_CACHE_PATH, '{}', 'utf8');
  }
}

// Read JSON file utility
async function loadJSON(filePath) {
  try {
    const data = await fs.readFile(filePath, 'utf8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

// Write JSON file utility
async function saveJSON(filePath, obj) {
  await fs.writeFile(filePath, JSON.stringify(obj, null, 2), 'utf8');
}

// Checks if the oracle cache is present and within the 48-hour validity period
async function isCacheValid() {
  await ensureCacheFilesExist();
  try {
    const cache = await loadJSON(ORACLE_CACHE_PATH);
    if (!cache.timestamp) {
      return false;
    }
    const cacheAge = Date.now() - new Date(cache.timestamp).getTime();
    return cacheAge < CACHE_EXPIRY_MS;
  } catch {
    return false;
  }
}

// General API request wrapper with rate-limit tracking and 300ms sleep delay
async function apiRequest(endpoint, params = {}) {
  if (apiLimitReached) {
    console.warn(`WARNING: Skipping API call to ${endpoint} because rate limit remaining is under threshold (< 10).`);
    return null;
  }

  if (!API_KEY) {
    throw new Error("API_FOOTBALL_KEY environment variable is not defined.");
  }

  // 300ms delay between calls
  await sleep(300);

  const url = new URL(`${BASE_URL}${endpoint}`);
  Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'x-apisports-key': API_KEY
    }
  });

  if (!response.ok) {
    throw new Error(`API response status error: ${response.status} ${response.statusText}`);
  }

  // Read rate limit headers
  const remaining = response.headers.get('x-ratelimit-requests-remaining');
  if (remaining !== null) {
    const remainingVal = parseInt(remaining, 10);
    if (!isNaN(remainingVal) && remainingVal < 10) {
      console.warn(`WARNING: API rate limit is almost reached (${remainingVal} requests remaining). Stopping further requests.`);
      apiLimitReached = true;
    }
  }

  const data = await response.json();
  if (data.errors && Object.keys(data.errors).length > 0) {
    throw new Error(`API returned errors: ${JSON.stringify(data.errors)}`);
  }

  return data;
}

// Fetch standings, fixtures, injuries, predictions, and H2H from API and save to cache
async function fetchAndCacheData() {
  await ensureCacheFilesExist();
  console.log("Fetching fresh tournament data from API-Football...");

  try {
    // a. GET /standings?league=1&season=2026
    console.log("Fetching standings...");
    const standingsData = await apiRequest('/standings', { league: LEAGUE, season: SEASON });
    const standings = {};
    if (standingsData && standingsData.response && standingsData.response[0]?.league?.standings) {
      const groups = standingsData.response[0].league.standings;
      for (const group of groups) {
        for (const row of group) {
          const teamId = row.team?.id;
          if (teamId) {
            standings[teamId] = {
              points: row.points || 0,
              wins: row.all?.win || 0,
              draws: row.all?.draw || 0,
              losses: row.all?.lose || 0,
              goalsFor: row.all?.goals?.for || 0,
              goalsAgainst: row.all?.goals?.against || 0,
              goalDifference: row.goalsDiff || 0,
              form: row.form || ""
            };
          }
        }
      }
    }

    // b. GET /fixtures?league=1&season=2026
    console.log("Fetching fixtures...");
    const fixturesData = await apiRequest('/fixtures', { league: LEAGUE, season: SEASON });
    const fixtures = [];
    if (fixturesData && fixturesData.response) {
      for (const item of fixturesData.response) {
        fixtures.push({
          id: item.fixture.id,
          date: item.fixture.date,
          homeTeam: {
            id: item.teams?.home?.id,
            name: item.teams?.home?.name
          },
          awayTeam: {
            id: item.teams?.away?.id,
            name: item.teams?.away?.name
          },
          status: item.fixture.status,
          goals: item.goals
        });
      }
    }

    // c. GET /injuries?league=1&season=2026
    console.log("Fetching injuries...");
    const injuriesData = await apiRequest('/injuries', { league: LEAGUE, season: SEASON });
    const injuries = {};
    if (injuriesData && injuriesData.response) {
      for (const item of injuriesData.response) {
        const teamId = item.team?.id;
        if (teamId) {
          if (!injuries[teamId]) {
            injuries[teamId] = [];
          }
          injuries[teamId].push({
            playerName: item.player?.name || null,
            teamName: item.team?.name || null,
            injuryType: item.player?.type || item.player?.reason || null,
            isStarter: item.player?.is_starter !== undefined ? item.player.is_starter : null
          });
        }
      }
    }

    // Identify next 6 upcoming fixtures (status = NS = Not Started) sorted by date ascending
    const upcomingFixtures = fixtures
      .filter(f => f.status && f.status.short === 'NS')
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .slice(0, 6);

    // d. GET /predictions?fixture=FIXTURE_ID
    console.log(`Fetching predictions for ${upcomingFixtures.length} upcoming fixtures...`);
    const predictions = {};
    for (const fixture of upcomingFixtures) {
      if (apiLimitReached) break;
      try {
        console.log(`Fetching predictions for fixture ID ${fixture.id} (${fixture.homeTeam.name} vs ${fixture.awayTeam.name})...`);
        const predData = await apiRequest('/predictions', { fixture: fixture.id });
        if (predData && predData.response && predData.response[0]) {
          const predObj = predData.response[0].predictions;
          predictions[fixture.id] = {
            winner: predObj?.winner?.name || null,
            homeWinPct: predObj?.percent?.home || null,
            drawPct: predObj?.percent?.draw || null,
            awayWinPct: predObj?.percent?.away || null,
            predictedScore: predObj?.goals?.home !== undefined && predObj?.goals?.away !== undefined
              ? `${predObj.goals.home}-${predObj.goals.away}`
              : null
          };
        }
      } catch (err) {
        console.error(`Skipping predictions for fixture ${fixture.id}:`, err.message);
      }
    }

    // e. GET /fixtures/headtohead?h2h=TEAM_A_ID-TEAM_B_ID (cache permanently in h2h_cache.json)
    console.log("Processing Head-to-Head (H2H) records for upcoming matches...");
    const allUpcoming = fixtures.filter(f => f.status && f.status.short === 'NS');
    const h2hCache = await loadJSON(H2H_CACHE_PATH);
    let h2hUpdated = false;

    for (const fixture of allUpcoming) {
      if (apiLimitReached) break;
      const homeId = fixture.homeTeam.id;
      const awayId = fixture.awayTeam.id;
      if (!homeId || !awayId) continue;

      const key1 = `${homeId}-${awayId}`;
      const key2 = `${awayId}-${homeId}`;

      // Skip fetching if already permanently cached
      if (h2hCache[key1] || h2hCache[key2]) {
        continue;
      }

      try {
        console.log(`Fetching H2H for ${fixture.homeTeam.name} vs ${fixture.awayTeam.name} (${key1})...`);
        const h2hData = await apiRequest('/fixtures/headtohead', { h2h: key1 });
        if (h2hData && h2hData.response) {
          const results = h2hData.response
            .sort((a, b) => new Date(b.fixture.date) - new Date(a.fixture.date))
            .slice(0, 5)
            .map(item => ({
              date: item.fixture.date,
              homeTeam: { id: item.teams?.home?.id, name: item.teams?.home?.name },
              awayTeam: { id: item.teams?.away?.id, name: item.teams?.away?.name },
              goals: { home: item.goals?.home, away: item.goals?.away },
              score: item.score?.fulltime || null
            }));

          h2hCache[key1] = results;
          h2hUpdated = true;
        }
      } catch (err) {
        console.error(`Skipping H2H for matchup ${key1}:`, err.message);
      }
    }

    if (h2hUpdated) {
      await saveJSON(H2H_CACHE_PATH, h2hCache);
    }

    // Save final offline cache data
    const oracleCacheData = {
      timestamp: new Date().toISOString(),
      standings,
      fixtures,
      injuries,
      predictions
    };
    await saveJSON(ORACLE_CACHE_PATH, oracleCacheData);
    console.log("Offline cache successfully synchronized and written to disk.");

  } catch (err) {
    console.error("Fetch process failed. Falling back to cached data silently. Error detail:", err.message);
  }
}

// Exports a single function that retrieves offline-cached matching data resolved by internal team codes or numeric IDs
export async function getEnrichedMatchData(homeTeam, awayTeam, fixtureId) {
  // Helper to map and resolve team inputs to numeric API team IDs
  const resolveTeamId = (teamInput, roleLabel) => {
    if (typeof teamInput === 'number') {
      return teamInput;
    }
    if (typeof teamInput === 'string') {
      if (/^\d+$/.test(teamInput)) {
        return parseInt(teamInput, 10);
      }
      const resolved = teamCodeToApiId[teamInput.toUpperCase()];
      if (!resolved) {
        console.warn(`WARNING: Team code "${teamInput}" (${roleLabel}) has no API ID mapping entry. Skipping call resolution.`);
      }
      return resolved || null;
    }
    return null;
  };

  const homeTeamId = resolveTeamId(homeTeam, "home");
  const awayTeamId = resolveTeamId(awayTeam, "away");

  await ensureCacheFilesExist();

  const oracleCache = await loadJSON(ORACLE_CACHE_PATH);
  const h2hCache = await loadJSON(H2H_CACHE_PATH);

  // Return null gracefully if cache doesn't exist yet and API failed
  if (!oracleCache || Object.keys(oracleCache).length === 0) {
    return null;
  }

  const standings = oracleCache.standings || {};
  const homeStanding = homeTeamId ? standings[homeTeamId] : null;
  const awayStanding = awayTeamId ? standings[awayTeamId] : null;

  const injuries = oracleCache.injuries || {};
  const homeInjuries = homeTeamId ? (injuries[homeTeamId] || []) : [];
  const awayInjuries = awayTeamId ? (injuries[awayTeamId] || []) : [];

  let h2hResults = [];
  if (homeTeamId && awayTeamId) {
    const key1 = `${homeTeamId}-${awayTeamId}`;
    const key2 = `${awayTeamId}-${homeTeamId}`;
    h2hResults = h2hCache[key1] || h2hCache[key2] || [];
  }

  const predictions = oracleCache.predictions || {};
  const pred = fixtureId ? (predictions[fixtureId] || null) : null;

  return {
    homeTeam: {
      standings: homeStanding || null,
      recentForm: homeStanding?.form || "",
      injuries: homeInjuries
    },
    awayTeam: {
      standings: awayStanding || null,
      recentForm: awayStanding?.form || "",
      injuries: awayInjuries
    },
    h2h: h2hResults,
    prediction: pred ? {
      winner: pred.winner,
      "homeWin%": pred.homeWinPct,
      "draw%": pred.drawPct,
      "awayWin%": pred.awayWinPct,
      predictedScore: pred.predictedScore
    } : null
  };
}

// Auto-run execution block
const nodePath = process.argv[1];
if (nodePath) {
  const isDirectRun = path.resolve(nodePath) === path.resolve(fileURLToPath(import.meta.url));
  if (isDirectRun) {
    (async () => {
      const valid = await isCacheValid();
      if (valid) {
        console.log("Offline cache is valid (under 48 hours old). Skipping fetch synchronization.");
      } else {
        await fetchAndCacheData();
      }
    })();
  }
}
