import { getScrapedSquad } from './scrapedAdapter.js';
import { getTeamCode } from './teamRegistry.js';
import { TEAMS } from './teams.js';
import { FORM_DECAY } from '../engine.js';

// Check environment
const isNode = typeof window === 'undefined';

let fs, path, fileURLToPath;
let CACHE_DIR = '';
let CACHE_FILE = '';

async function initNode() {
  if (fs) return;
  const fsName = 'fs/promises';
  const pathName = 'path';
  const urlName = 'url';
  
  fs = (await import(fsName)).default;
  path = (await import(pathName)).default;
  const urlModule = await import(urlName);
  fileURLToPath = urlModule.fileURLToPath;
  
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  CACHE_DIR = path.join(__dirname, '../cache');
  CACHE_FILE = path.join(CACHE_DIR, 'openfootball_cache.json');
}

const CACHE_EXPIRY_MS = 6 * 60 * 60 * 1000; // 6 hours

// GitHub Raw URLs for openfootball dataset
const URL_MATCHES = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json';
const URL_GROUPS = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.groups.json';
const URL_TEAMS = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.teams.json';
const URL_SQUADS = 'https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.squads.json';


const DEFAULT_STATS = {
  goalsFor: 0,
  goalsAgainst: 0,
  matchesPlayed: 0,
  avgGoalsFor: 0,
  avgGoalsAgainst: 0
};

// Ensure cache directory exists
async function ensureCacheDir() {
  if (!isNode) return;
  await initNode();
  try {
    await fs.mkdir(CACHE_DIR, { recursive: true });
  } catch (err) {
    // Ignore error if it already exists
  }
}

// Load cache file
async function loadCache() {
  if (!isNode) return {};
  await initNode();
  try {
    const data = await fs.readFile(CACHE_FILE, 'utf8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

// Save cache file
async function saveCache(data) {
  if (!isNode) return;
  await initNode();
  await fs.writeFile(CACHE_FILE, JSON.stringify(data, null, 2), 'utf8');
}

// Check if cache file is valid (less than 6 hours old)
async function isCacheValid() {
  if (!isNode) return true;
  await initNode();
  try {
    const data = await fs.readFile(CACHE_FILE, 'utf8');
    const cache = JSON.parse(data);
    if (!cache.timestamp) return false;
    const cacheAge = Date.now() - new Date(cache.timestamp).getTime();
    return cacheAge < CACHE_EXPIRY_MS;
  } catch {
    return false;
  }
}

// Fetch helper with native fetch
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`HTTP error ${res.status}: ${res.statusText}`);
  }
  return await res.json();
}

// Core computation engine
function computeAll(matchesData, groupsData) {
  const rawMatches = matchesData.matches || [];
  const completedMatches = [];
  const upcomingMatches = [];

  for (const m of rawMatches) {
    const team1Code = getTeamCode(m.team1) || null;
    const team2Code = getTeamCode(m.team2) || null;

    if (m.score && m.score.ft) {
      completedMatches.push({
        team1Code,
        team2Code,
        score: m.score,
        goals1: m.goals1 || [],
        goals2: m.goals2 || [],
        date: m.date,
        round: m.round,
        group: m.group || null
      });
    } else {
      upcomingMatches.push({
        team1Code,
        team2Code,
        date: m.date,
        time: m.time || null,
        round: m.round,
        group: m.group || null
      });
    }
  }

  // Compute stats running totals
  const stats = {};
  for (const code of Object.keys(TEAMS)) {
    stats[code] = {
      goalsFor: 0,
      goalsAgainst: 0,
      matchesPlayed: 0,
      avgGoalsFor: 0,
      avgGoalsAgainst: 0
    };
  }

  for (const code of Object.keys(stats)) {
    const teamMatches = completedMatches
      .filter(m => m.team1Code === code || m.team2Code === code)
      .sort((a, b) => new Date(a.date) - new Date(b.date));
      
    const N = teamMatches.length;
    let weightedGF = 0;
    let weightedGA = 0;
    let weightSum = 0;
    let unweightedGF = 0;
    let unweightedGA = 0;

    for (let i = 0; i < N; i++) {
      const m = teamMatches[i];
      const isTeam1 = m.team1Code === code;
      const gFor = isTeam1 ? m.score.ft[0] : m.score.ft[1];
      const gAgainst = isTeam1 ? m.score.ft[1] : m.score.ft[0];
      
      unweightedGF += gFor;
      unweightedGA += gAgainst;

      const w = Math.pow(FORM_DECAY, N - 1 - i);
      weightedGF += gFor * w;
      weightedGA += gAgainst * w;
      weightSum += w;
    }
    
    stats[code].goalsFor = unweightedGF;
    stats[code].goalsAgainst = unweightedGA;
    stats[code].matchesPlayed = N;
    
    if (weightSum > 0) {
      stats[code].avgGoalsFor = parseFloat((weightedGF / weightSum).toFixed(4));
      stats[code].avgGoalsAgainst = parseFloat((weightedGA / weightSum).toFixed(4));
    }
  }

  // Compute team forms (last 5 completed matches, chronological order)
  const form = {};
  for (const code of Object.keys(TEAMS)) {
    form[code] = [];
  }

  for (const code of Object.keys(form)) {
    const teamMatches = completedMatches
      .filter(m => m.team1Code === code || m.team2Code === code)
      .sort((a, b) => new Date(a.date) - new Date(b.date));

    const recent = teamMatches.slice(-5);
    form[code] = recent.map(m => {
      const isTeam1 = m.team1Code === code;
      const opponent = isTeam1 ? m.team2Code : m.team1Code;
      const goalsFor = isTeam1 ? m.score.ft[0] : m.score.ft[1];
      const goalsAgainst = isTeam1 ? m.score.ft[1] : m.score.ft[0];
      let result = 'D';
      if (goalsFor > goalsAgainst) result = 'W';
      else if (goalsFor < goalsAgainst) result = 'L';

      return {
        opponent,
        result,
        goalsFor,
        goalsAgainst,
        date: m.date
      };
    });
  }

  // Compute Standings
  const standings = {};
  const rawGroups = groupsData.groups || [];

  for (const grp of rawGroups) {
    const groupName = grp.name;
    const groupTeams = grp.teams || [];

    const groupStandings = groupTeams.map(name => {
      const code = getTeamCode(name) || null;
      return {
        teamCode: code,
        played: 0,
        won: 0,
        drawn: 0,
        lost: 0,
        goalsFor: 0,
        goalsAgainst: 0,
        goalDiff: 0,
        points: 0
      };
    });

    const groupMatches = completedMatches.filter(m => m.group === groupName);

    for (const m of groupMatches) {
      const t1 = m.team1Code;
      const t2 = m.team2Code;
      if (!t1 || !t2) continue;

      const g1 = m.score.ft[0];
      const g2 = m.score.ft[1];

      const row1 = groupStandings.find(r => r.teamCode === t1);
      const row2 = groupStandings.find(r => r.teamCode === t2);

      if (row1 && row2) {
        row1.played += 1;
        row1.goalsFor += g1;
        row1.goalsAgainst += g2;
        row1.goalDiff += (g1 - g2);

        row2.played += 1;
        row2.goalsFor += g2;
        row2.goalsAgainst += g1;
        row2.goalDiff += (g2 - g1);

        if (g1 > g2) {
          row1.won += 1;
          row1.points += 3;
          row2.lost += 1;
        } else if (g1 < g2) {
          row2.won += 1;
          row2.points += 3;
          row1.lost += 1;
        } else {
          row1.drawn += 1;
          row1.points += 1;
          row2.drawn += 1;
          row2.points += 1;
        }
      }
    }

    // Sort standings by points desc, then goalDiff desc
    groupStandings.sort((a, b) => {
      if (b.points !== a.points) {
        return b.points - a.points;
      }
      return b.goalDiff - a.goalDiff;
    });

    standings[groupName] = groupStandings;
  }

  return {
    completedMatches,
    upcomingMatches,
    stats,
    form,
    standings
  };
}

// Main fetcher and caching refresh function
export async function refreshCache() {
  if (!isNode) return;
  await ensureCacheDir();
  const existingCache = await loadCache();

  let matchesData = null;
  let groupsData = null;
  let teamsData = null;
  let squadsData = null;

  // Fetch all four files with silent fallbacks to cache
  try {
    matchesData = await fetchJSON(URL_MATCHES);
  } catch (err) {
    console.warn(`Silently failed to fetch matches. Falling back to cache. Error: ${err.message}`);
    matchesData = existingCache.matches || null;
  }

  try {
    groupsData = await fetchJSON(URL_GROUPS);
  } catch (err) {
    console.warn(`Silently failed to fetch groups. Falling back to cache. Error: ${err.message}`);
    groupsData = existingCache.groups || null;
  }

  try {
    teamsData = await fetchJSON(URL_TEAMS);
  } catch (err) {
    console.warn(`Silently failed to fetch teams. Falling back to cache. Error: ${err.message}`);
    teamsData = existingCache.teams || null;
  }

  try {
    squadsData = await fetchJSON(URL_SQUADS);
  } catch (err) {
    console.warn(`Silently failed to fetch squads. Falling back to cache. Error: ${err.message}`);
    squadsData = existingCache.squads || null;
  }

  // Ensure non-null shapes
  matchesData = matchesData || { matches: [] };
  groupsData = groupsData || { groups: [] };
  teamsData = teamsData || { teams: [] };
  squadsData = squadsData || { squads: [] };

  const computed = computeAll(matchesData, groupsData);

  const newCache = {
    timestamp: new Date().toISOString(),
    matches: matchesData,
    groups: groupsData,
    teams: teamsData,
    squads: squadsData,
    computed
  };

  await saveCache(newCache);
}

// Fetch cache in browser environment
async function fetchCacheFromBrowser() {
  try {
    const res = await fetch('/cache/openfootball_cache.json');
    if (res.ok) return await res.json();
  } catch {}
  if (import.meta.env.DEV) {
    try {
      const res = await fetch('http://localhost:3001/cache/openfootball_cache.json');
      if (res.ok) return await res.json();
    } catch {}
  }
  return {
    computed: {
      completedMatches: [],
      upcomingMatches: [],
      stats: {},
      form: {},
      standings: {}
    }
  };
}

// Fetch cache wrapper
export async function getCache() {
  if (!isNode) {
    return await fetchCacheFromBrowser();
  }

  const valid = await isCacheValid();
  if (!valid) {
    await refreshCache();
  }
  try {
    const data = await fs.readFile(CACHE_FILE, 'utf8');
    return JSON.parse(data);
  } catch {
    return {
      computed: {
        completedMatches: [],
        upcomingMatches: [],
        stats: {},
        form: {},
        standings: {}
      }
    };
  }
}

// EXPORTED FUNCTIONS

export async function getTeamForm(teamCode) {
  const cache = await getCache();
  return cache.computed.form[teamCode] || [];
}

export async function getTeamStats(teamCode) {
  const cache = await getCache();
  return cache.computed.stats[teamCode] || DEFAULT_STATS;
}

export async function getGroupStandings(groupName) {
  const cache = await getCache();
  return cache.computed.standings[groupName] || [];
}

export async function getH2HResults(team1Code, team2Code) {
  const cache = await getCache();
  const completed = cache.computed.completedMatches || [];
  return completed.filter(m =>
    (m.team1Code === team1Code && m.team2Code === team2Code) ||
    (m.team1Code === team2Code && m.team2Code === team1Code)
  );
}

export async function getUpcomingMatches(teamCode) {
  const cache = await getCache();
  const upcoming = cache.computed.upcomingMatches || [];
  return upcoming
    .filter(m => m.team1Code === teamCode || m.team2Code === teamCode)
    .sort((a, b) => new Date(a.date) - new Date(b.date))
    .slice(0, 3);
}

export async function getEnrichedMatchData(homeCode, awayCode) {
  const cache = await getCache();
  const homeForm = await getTeamForm(homeCode);
  const homeStats = await getTeamStats(homeCode);

  const awayForm = await getTeamForm(awayCode);
  const awayStats = await getTeamStats(awayCode);

  const h2h = await getH2HResults(homeCode, awayCode);

  // Find standing row for home and away
  let homeStanding = null;
  let awayStanding = null;
  const standings = cache.computed.standings || {};

  for (const groupName of Object.keys(standings)) {
    if (!homeStanding) {
      homeStanding = standings[groupName].find(r => r.teamCode === homeCode) || null;
    }
    if (!awayStanding) {
      awayStanding = standings[groupName].find(r => r.teamCode === awayCode) || null;
    }
  }

  const bothTeamsHavePlayed = homeStats.matchesPlayed > 0 && awayStats.matchesPlayed > 0;

  return {
    home: {
      form: homeForm,
      stats: homeStats,
      standing: homeStanding
    },
    away: {
      form: awayForm,
      stats: awayStats,
      standing: awayStanding
    },
    h2h,
    bothTeamsHavePlayed
  };
}

export async function getFixture(team1Code, team2Code) {
  let fixtures = [];
  if (isNode) {
    await initNode();
    try {
      const __filename = fileURLToPath(import.meta.url);
      const __dirname = path.dirname(__filename);
      const filePath = path.join(__dirname, '../public/data/scraped/fixtures.json');
      const content = await fs.readFile(filePath, 'utf8');
      fixtures = JSON.parse(content);
    } catch (e) {
      const cache = await getCache();
      fixtures = cache.matches?.matches || [];
    }
  } else {
    try {
      const res = await fetch('/data/scraped/fixtures.json');
      if (res.ok) {
        fixtures = await res.json();
      } else {
        const cache = await getCache();
        fixtures = cache.matches?.matches || [];
      }
    } catch {
      const cache = await getCache();
      fixtures = cache.matches?.matches || [];
    }
  }

  for (const m of fixtures) {
    const homeName = m.home_team || m.team1;
    const awayName = m.away_team || m.team2;
    
    const code1 = getTeamCode(homeName) || null;
    const code2 = getTeamCode(awayName) || null;
    
    if ((code1 === team1Code && code2 === team2Code) || (code1 === team2Code && code2 === team1Code)) {
      return {
        homeTeamCode: code1,
        awayTeamCode: code2,
        date: m.date || m.kickoff_utc,
        ground: m.venue || m.ground || "Unknown Stadium",
        venue: m.venue || m.ground || "Unknown Stadium",
        round: m.round || m.stage,
        group: m.group || null,
        isCompleted: !!(m.result && (m.result.ft || m.score?.ft)),
        score: m.result || m.score || null,
        attendance: m.attendance || null
      };
    }
  }
  
  return null;
}

export const STADIUM_CAPACITIES = {
  "Mexico City Stadium": 87523,
  "Estadio Azteca": 87523,
  "AT&T Stadium": 80000,
  "SoFi Stadium": 70240,
  "MetLife Stadium": 82500,
  "Levi's Stadium": 68500,
  "Arrowhead Stadium": 76416,
  "Rose Bowl Stadium": 90888,
  "Gillette Stadium": 65878,
  "Lincoln Financial Field": 69796,
  "NRG Stadium": 72220,
  "BC Place": 54500,
  "BMO Field": 45736,
  "Estadio Akron": 49850,
  "Estadio BBVA": 53500,
  "Commonwealth Stadium": 56302
};

export const VENUE_COORDINATES = {
  "Mexico City Stadium": { lat: 19.3029, lon: -99.1505 },
  "Guadalajara Stadium": { lat: 20.6817, lon: -103.4628 },
  "Monterrey Stadium": { lat: 25.6698, lon: -100.2444 },
  "Toronto Stadium": { lat: 43.6332, lon: -79.4186 },
  "BC Place Vancouver": { lat: 49.2768, lon: -123.1120 },
  "New York/New Jersey Stadium": { lat: 40.8136, lon: -74.0745 },
  "Boston Stadium": { lat: 42.0909, lon: -71.2643 },
  "Philadelphia Stadium": { lat: 39.9008, lon: -75.1675 },
  "Miami Stadium": { lat: 25.9580, lon: -80.2389 },
  "Atlanta Stadium": { lat: 33.7554, lon: -84.4006 },
  "Dallas Stadium": { lat: 32.7473, lon: -97.0945 },
  "Houston Stadium": { lat: 29.6847, lon: -95.4107 },
  "Kansas City Stadium": { lat: 39.0489, lon: -94.4839 },
  "Los Angeles Stadium": { lat: 33.9535, lon: -118.3390 },
  "San Francisco Bay Area Stadium": { lat: 37.4032, lon: -121.9698 },
  "Seattle Stadium": { lat: 47.5952, lon: -122.3316 }
};

export function getAttendanceFactor(venueNameFromFixture) {
  const capacity = STADIUM_CAPACITIES[venueNameFromFixture] || 70000;
  return capacity;
}

export async function getTeamSquad(teamCode) {
  if (typeof window !== 'undefined') {
    const scraped = getScrapedSquad(teamCode);
    if (scraped && scraped.length > 0) {
        return scraped.map((p, idx) => {
          let posGroup = "FORWARDS";
          if (p.position === "GK") posGroup = "GOALKEEPERS";
          else if (p.position === "DF") posGroup = "DEFENDERS";
          else if (p.position === "MF") posGroup = "MIDFIELDERS";

          const number = p.number || (idx + 1);
          const starter = number <= 11;

          return {
            number,
            pos: p.position || "FW",
            name: p.name,
            age: p.age || 26,
            posGroup,
            starter
          };
        });
    }
  }

  const cache = await getCache();
  const squads = cache.squads || [];
  const teamSquad = squads.find(s => s.fifa_code === teamCode);
  if (!teamSquad || !teamSquad.players) return [];

  return teamSquad.players.map(p => {
    // compute age from date_of_birth to today
    let age = 0;
    if (p.date_of_birth) {
      const dob = new Date(p.date_of_birth);
      const today = new Date();
      age = today.getFullYear() - dob.getFullYear();
      const m = today.getMonth() - dob.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
      }
    }
    
    // posGroup
    let posGroup = "FORWARDS";
    if (p.pos === "GK") posGroup = "GOALKEEPERS";
    else if (p.pos === "DF") posGroup = "DEFENDERS";
    else if (p.pos === "MF") posGroup = "MIDFIELDERS";

    // numbers 1-11 starter: true, 12-26 starter: false
    const starter = p.number >= 1 && p.number <= 11;

    return {
      number: p.number,
      pos: p.pos,
      name: p.name,
      age,
      posGroup,
      starter
    };
  });
}

export async function getTopScorers(limit = 10) {
  const cache = await getCache();
  const completed = cache.computed?.completedMatches || [];
  const scorerMap = {}; // key: name|teamCode -> count

  completed.forEach(m => {
    const t1 = m.team1Code;
    const t2 = m.team2Code;
    if (Array.isArray(m.goals1)) {
      m.goals1.forEach(g => {
        if (g.name && t1) {
          const key = `${g.name}|${t1}`;
          scorerMap[key] = (scorerMap[key] || 0) + 1;
        }
      });
    }
    if (Array.isArray(m.goals2)) {
      m.goals2.forEach(g => {
        if (g.name && t2) {
          const key = `${g.name}|${t2}`;
          scorerMap[key] = (scorerMap[key] || 0) + 1;
        }
      });
    }
  });

  const list = Object.entries(scorerMap).map(([key, goals]) => {
    const [name, teamCode] = key.split('|');
    return { name, teamCode, goals };
  });

  list.sort((a, b) => {
    if (b.goals !== a.goals) return b.goals - a.goals;
    return a.name.localeCompare(b.name);
  });

  return list.slice(0, limit);
}

export async function getTeamCleanSheets(teamCode) {
  const cache = await getCache();
  const completed = cache.computed?.completedMatches || [];
  let cleanSheets = 0;

  completed.forEach(m => {
    if (m.team1Code === teamCode) {
      if (m.score && Array.isArray(m.score.ft) && m.score.ft[1] === 0) {
        cleanSheets++;
      }
    } else if (m.team2Code === teamCode) {
      if (m.score && Array.isArray(m.score.ft) && m.score.ft[0] === 0) {
        cleanSheets++;
      }
    }
  });

  return cleanSheets;
}


// Auto-run execution block
if (isNode) {
  const nodePath = process.argv[1];
  if (nodePath) {
    (async () => {
      await initNode();
      const isDirectRun = path.resolve(nodePath) === path.resolve(fileURLToPath(import.meta.url));
      if (isDirectRun) {
        console.log("=== openfootball layer auto-run execution ===");
        await refreshCache();
        const cache = await getCache();

        const completedCount = cache.computed.completedMatches.length;
        const upcomingCount = cache.computed.upcomingMatches.length;
        console.log(`Completed matches so far: ${completedCount}`);
        console.log(`Upcoming matches: ${upcomingCount}`);

        // Calculate top 3 teams by points across all groups
        const allTeamsStandings = [];
        const standings = cache.computed.standings || {};
        for (const groupName of Object.keys(standings)) {
          for (const row of standings[groupName]) {
            allTeamsStandings.push({
              group: groupName,
              ...row
            });
          }
        }
        // Sort all teams standings
        allTeamsStandings.sort((a, b) => {
          if (b.points !== a.points) return b.points - a.points;
          return b.goalDiff - a.goalDiff;
        });
        console.log("\nTop 3 teams by points across all groups:");
        allTeamsStandings.slice(0, 3).forEach((t, i) => {
          console.log(`${i+1}. Team: ${t.teamCode} (${t.group}) - Points: ${t.points}, GD: ${t.goalDiff}, Won: ${t.won}, Played: ${t.played}`);
        });

        console.log("\n=== Testing Exported Functions ===");

        console.log("\n1. Testing getTeamForm('MEX'):");
        const mexForm = await getTeamForm('MEX');
        console.log(JSON.stringify(mexForm, null, 2));

        console.log("\n2. Testing getTeamStats('FRA'):");
        const fraStats = await getTeamStats('FRA');
        console.log(JSON.stringify(fraStats, null, 2));

        console.log("\n3. Testing getTeamStats('XYZ') (team with 0 matches - should return default zeros):");
        const xyzStats = await getTeamStats('XYZ');
        console.log(JSON.stringify(xyzStats, null, 2));

        console.log("\n4. Testing getGroupStandings('Group A'):");
        const groupAStandings = await getGroupStandings('Group A');
        console.log(JSON.stringify(groupAStandings, null, 2));

        console.log("\n5. Testing getH2HResults('MEX', 'RSA'):");
        const h2h = await getH2HResults('MEX', 'RSA');
        console.log(JSON.stringify(h2h, null, 2));

        console.log("\n6. Testing getUpcomingMatches('USA'):");
        const upcomingUSA = await getUpcomingMatches('USA');
        console.log(JSON.stringify(upcomingUSA, null, 2));

        console.log("\n7. Testing getEnrichedMatchData('MEX', 'KOR'):");
        const enriched = await getEnrichedMatchData('MEX', 'KOR');
        console.log(JSON.stringify(enriched, null, 2));

        console.log("\n8. Testing getFixture('MEX', 'RSA'):");
        console.log(await getFixture('MEX', 'RSA'));

        console.log("\n9. Testing getFixture('RSA', 'MEX'):");
        console.log(await getFixture('RSA', 'MEX'));

        console.log("\n10. Testing getFixture('FRA', 'SEN'):");
        console.log(await getFixture('FRA', 'SEN'));

        console.log("\n11. Testing getFixture('ARG', 'FRA') (should be null):");
        console.log(await getFixture('ARG', 'FRA'));

        console.log("\n=== Verification Completed ===");
      }
    })();
  }
}
