// Run with: node data/openFootballLayer.js

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

// Team name mapping: openfootball names to internal codes
const teamNameToCode = {
  "Mexico": "MEX", "South Africa": "RSA", "South Korea": "KOR",
  "Czech Republic": "CZE", "Canada": "CAN", 
  "Bosnia & Herzegovina": "BIH", "Qatar": "QAT", 
  "Switzerland": "SUI", "Brazil": "BRA", "Morocco": "MAR",
  "Haiti": "HAI", "Scotland": "SCO", "USA": "USA",
  "Paraguay": "PAR", "Australia": "AUS", "Turkey": "TUR",
  "Germany": "GER", "Curaçao": "CUW", "Ivory Coast": "CIV",
  "Ecuador": "ECU", "Netherlands": "NED", "Japan": "JPN",
  "Sweden": "SWE", "Tunisia": "TUN", "Belgium": "BEL",
  "Egypt": "EGY", "Iran": "IRN", "New Zealand": "NZL",
  "Spain": "ESP", "Cape Verde": "CPV", "Saudi Arabia": "SAU",
  "Uruguay": "URU", "France": "FRA", "Senegal": "SEN",
  "Iraq": "IRQ", "Norway": "NOR", "Argentina": "ARG",
  "Algeria": "ALG", "Austria": "AUT", "Jordan": "JOR",
  "Portugal": "POR", "DR Congo": "COD", "Uzbekistan": "UZB",
  "Colombia": "COL", "England": "ENG", "Croatia": "CRO",
  "Ghana": "GHA", "Panama": "PAN"
};

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
    const team1Code = teamNameToCode[m.team1] || null;
    const team2Code = teamNameToCode[m.team2] || null;

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
  for (const code of Object.values(teamNameToCode)) {
    stats[code] = {
      goalsFor: 0,
      goalsAgainst: 0,
      matchesPlayed: 0,
      avgGoalsFor: 0,
      avgGoalsAgainst: 0
    };
  }

  for (const m of completedMatches) {
    const t1 = m.team1Code;
    const t2 = m.team2Code;
    if (!t1 || !t2) continue;

    const g1 = m.score.ft[0];
    const g2 = m.score.ft[1];

    if (stats[t1]) {
      stats[t1].goalsFor += g1;
      stats[t1].goalsAgainst += g2;
      stats[t1].matchesPlayed += 1;
    }

    if (stats[t2]) {
      stats[t2].goalsFor += g2;
      stats[t2].goalsAgainst += g1;
      stats[t2].matchesPlayed += 1;
    }
  }

  // Compute averages
  for (const code of Object.keys(stats)) {
    const t = stats[code];
    if (t.matchesPlayed > 0) {
      t.avgGoalsFor = parseFloat((t.goalsFor / t.matchesPlayed).toFixed(4));
      t.avgGoalsAgainst = parseFloat((t.goalsAgainst / t.matchesPlayed).toFixed(4));
    }
  }

  // Compute team forms (last 5 completed matches, chronological order)
  const form = {};
  for (const code of Object.values(teamNameToCode)) {
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
      const code = teamNameToCode[name] || null;
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
async function refreshCache() {
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
  try {
    const res = await fetch('http://localhost:3001/cache/openfootball_cache.json');
    if (res.ok) return await res.json();
  } catch {}
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
async function getCache() {
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

// Auto-run execution block
const nodePath = process.argv[1];
if (nodePath) {
  (async () => {
    if (isNode) {
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

        console.log("\n=== Verification Completed ===");
      }
    }
  })();
}
