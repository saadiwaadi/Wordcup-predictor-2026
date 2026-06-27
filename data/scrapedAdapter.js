const NAME_MAP = {
  "Czech Republic": "Czechia",
  "Czechia": "Czech Republic",
  "Bosnia and Herzegovina": "Bosnia & Herzegovina",
  "Bosnia & Herzegovina": "Bosnia and Herzegovina",
  "DR Congo": "DR Congo",
  "Ivory Coast": "Ivory Coast",
  "United States": "United States",
  "USA": "United States"
};

export function normalizeName(name) {
  return NAME_MAP[name] ?? name;
}

let _squads = null;
let _fixtures = null;
let _lineups = null;
let _matchEvents = null;
let _fetchPromise = null;

async function performFetch() {
  try {
    const [squadsRes, fixturesRes, lineupsRes, matchEventsRes] = await Promise.all([
      fetch('/data/scraped/squads.json'),
      fetch('/data/scraped/fixtures.json'),
      fetch('/data/scraped/lineups.json'),
      fetch('/data/scraped/match_events.json')
    ]);

    if (squadsRes.ok) {
      _squads = await squadsRes.json();
    } else {
      console.warn(`Failed to fetch squads: ${squadsRes.statusText}`);
    }

    if (fixturesRes.ok) {
      _fixtures = await fixturesRes.json();
    } else {
      console.warn(`Failed to fetch fixtures: ${fixturesRes.statusText}`);
    }

    if (lineupsRes.ok) {
      _lineups = await lineupsRes.json();
    } else {
      console.warn(`Failed to fetch lineups: ${lineupsRes.statusText}`);
    }

    if (matchEventsRes.ok) {
      _matchEvents = await matchEventsRes.json();
    } else {
      console.warn(`Failed to fetch match events: ${matchEventsRes.statusText}`);
    }
  } catch (error) {
    console.warn("Failed loading scraped data from browser:", error);
  }
}

export async function initScrapedData() {
  if (typeof window === 'undefined') {
    return;
  }
  if (!_fetchPromise) {
    _fetchPromise = performFetch();
  }
  await _fetchPromise;
}

export function getScrapedSquad(teamName) {
  if (!_squads) return [];
  const normalized = normalizeName(teamName);
  return _squads[normalized] || _squads[teamName] || [];
}

export function getCompletedFixtures() {
  if (!_fixtures) return [];
  return _fixtures.filter(f => f.result && f.result.ft);
}

export function getUpcomingFixtures() {
  if (!_fixtures) return [];
  return _fixtures.filter(f => !f.result || !f.result.ft);
}

export function getLineup(matchId) {
  if (!_lineups) return null;
  return _lineups[matchId] || _lineups[String(matchId)] || null;
}

export function getMatchEvents(matchId) {
  if (!_matchEvents) return null;
  return _matchEvents[matchId] || _matchEvents[String(matchId)] || null;
}

export function getFixtureByTeams(teamA, teamB) {
  if (!_fixtures) return null;
  const normA = normalizeName(teamA).toLowerCase();
  const normB = normalizeName(teamB).toLowerCase();
  const rawA = teamA.toLowerCase();
  const rawB = teamB.toLowerCase();

  return _fixtures.find(f => {
    const homeNorm = normalizeName(f.home_team).toLowerCase();
    const awayNorm = normalizeName(f.away_team).toLowerCase();
    const homeRaw = f.home_team.toLowerCase();
    const awayRaw = f.away_team.toLowerCase();

    const match1 = (homeNorm === normA || homeRaw === rawA) && (awayNorm === normB || awayRaw === rawB);
    const match2 = (homeNorm === normB || homeRaw === rawB) && (awayNorm === normA || awayRaw === rawA);

    return match1 || match2;
  }) || null;
}

// Auto-trigger fetch at module load in browser context
if (typeof window !== 'undefined') {
  _fetchPromise = performFetch();
}
