import { TEAMS as teams } from './teams.js';
import { RATINGS as ratings } from './ratings.js';
import { FORM as form } from './form.js';
import { H2H as h2h } from './h2h.js';
import { TOURNAMENT as tournament } from './tournament.js';
import { simpleHash } from './deltaSync.js';
import { getScrapedSquad, getCompletedFixtures, normalizeName } from './scrapedAdapter.js';
const WC_48_TEAMS = new Set([
  "BRA", "FRA", "ENG", "GER", "ESP", "ARG", "POR", "NED", "BEL", "CRO",
  "SEN", "MAR", "JPN", "USA", "MEX", "CAN", "COL", "URU", "SUI", "SRB",
  "DEN", "AUT", "TUR", "KOR", "POL", "AUS", "IRN", "ECU", "NGR", "GHA",
  "CMR", "EGY", "ALG", "CIV", "SAU", "QAT", "CRI", "PAN", "VEN", "CHI",
  "ROU", "UKR", "RSA", "CZE", "PAR", "SCO", "SWE", "TUN",
  "NOR", "NZL", "BIH", "HAI", "CUW", "CPV", "IRQ", "JOR", "COD", "UZB"
]);

export function initializeLocalStorageCache() {
  if (typeof localStorage === 'undefined') return;
  if (localStorage.getItem('oracle26_meta')) return;

  let totalTeams = 0;
  let totalPlayers = 0;

  Object.keys(teams).forEach(teamId => {
    if (!WC_48_TEAMS.has(teamId)) return;
    const team = teams[teamId];
    const squad = team.players || [];
    totalTeams++;
    totalPlayers += squad.length;

    // Map squad players and add xG_approx = 0.00 and xG_source = 'MOCK'
    const teamKey = `oracle26_team_${teamId}`;
    const mappedSquad = squad.map((p, idx) => ({
      id: p.id || `${teamId}_${idx}`,
      name: p.name,
      position: p.position,
      caps: p.caps || 0,
      data_quality: p.data_quality || 'UNKNOWN',
      is_starter: p.is_starter !== undefined ? p.is_starter : true,
      xG_intl_per90: p.xG_intl_per90 || 0,
      xG_club_per90: p.xG_club_per90 || 0,
      league_difficulty_coeff: p.league_difficulty_coeff || 1.0,
      xG_best_single_match: p.xG_best_single_match || 0,
      mean_xG_per90: p.mean_xG_per90 || 0,
      xG_approx: 0.00,  // fixed placeholder value of 0.00 at seed time
      xG_source: 'MOCK' // tagged 'MOCK' at seed time
    }));

    const teamData = {
      team_id: teamId,
      squad: mappedSquad,
      stats: {},
      hash: "",
      updated_at: new Date().toISOString(),
      pull_count: 0
    };

    teamData.hash = simpleHash(JSON.stringify({ incomingSquad: teamData.squad, incomingStats: teamData.stats }));
    localStorage.setItem(teamKey, JSON.stringify(teamData));

    // Seed injuries
    const injuriesKey = `oracle26_injuries_${teamId}`;
    localStorage.setItem(injuriesKey, JSON.stringify({
      team_id: teamId,
      injured_players: team.injuries || [],
      updated_at: new Date().toISOString()
    }));
  });

  localStorage.setItem('oracle26_meta', JSON.stringify({
    version: 1,
    total_teams: totalTeams,
    total_players: totalPlayers,
    created_at: new Date().toISOString(),
    last_pull_attempt: null
  }));
}

export function getTeamData(teamId) {
  const team = teams[teamId];
  if (!team) return null;
  const rating = ratings[teamId] || {};
  const dynamicForm = getForm();
  const teamForm = dynamicForm[teamId] || [];
  
  let squad = team.players || [];
  let injuries = team.injuries || [];
  
  if (typeof localStorage !== 'undefined') {
    const cachedTeam = JSON.parse(localStorage.getItem(`oracle26_team_${teamId}`) || 'null');
    const cachedInjuries = JSON.parse(localStorage.getItem(`oracle26_injuries_${teamId}`) || 'null');
    if (cachedTeam) squad = cachedTeam.squad;
    if (cachedInjuries) injuries = cachedInjuries.injured_players;
  }
  
  const baseTeam = {
    id: team.id,
    name: team.name,
    flag: team.flag,
    tier: team.tier,
    fifa_rank: rating.fifaPoints,
    elo: rating.elo,
    elo_delta_90: rating.eloDelta90,
    market_value_m: rating.marketValue,
    avg_age: team.avgAge,
    last_6: teamForm,
    wc_appearances: team.worldCupAppearances,
    host: team.isHost,
    injuries: injuries,
    confederation: team.confederation,
    players: squad
  };

  const scraped = getScrapedSquad(team.name);
  if (scraped && scraped.length > 0) {
    baseTeam.players = scraped.map((p, idx) => {
      const staticPlayer = (squad || []).find(sp => sp.name.toLowerCase() === p.name.toLowerCase()) || {};
      const hasMatch = !!staticPlayer.name;

      return {
        id: staticPlayer.id || `${teamId}_scraped_${idx}`,
        name: p.name,
        position: staticPlayer.position || p.position || "FW",
        caps: hasMatch ? (staticPlayer.caps !== undefined ? staticPlayer.caps : 0) : null,
        data_quality: hasMatch ? (staticPlayer.data_quality || "UNKNOWN") : "UNKNOWN",
        is_starter: hasMatch ? (staticPlayer.is_starter !== undefined ? staticPlayer.is_starter : false) : false,
        xG_intl_per90: hasMatch ? (staticPlayer.xG_intl_per90 !== undefined ? staticPlayer.xG_intl_per90 : 0) : null,
        xG_club_per90: hasMatch ? (staticPlayer.xG_club_per90 !== undefined ? staticPlayer.xG_club_per90 : 0) : null,
        league_difficulty_coeff: hasMatch ? (staticPlayer.league_difficulty_coeff !== undefined ? staticPlayer.league_difficulty_coeff : 1.0) : null,
        xG_best_single_match: hasMatch ? (staticPlayer.xG_best_single_match !== undefined ? staticPlayer.xG_best_single_match : 0) : null,
        mean_xG_per90: hasMatch ? (staticPlayer.mean_xG_per90 !== undefined ? staticPlayer.mean_xG_per90 : 0) : null,
        xG_approx: hasMatch ? (staticPlayer.xG_approx !== undefined ? staticPlayer.xG_approx : 0) : null,
        xG_source: hasMatch ? (staticPlayer.xG_source || null) : null,
        club: p.club || null
      };
    });
  }

  return baseTeam;
}

export function getRatings() {
  return ratings;
}

export function getForm() {
  const completed = getCompletedFixtures();
  if (!completed || completed.length === 0) {
    return form;
  }

  // Sort by kickoff_utc ascending (oldest first)
  const sorted = [...completed].sort((a, b) => new Date(a.kickoff_utc) - new Date(b.kickoff_utc));

  // Build liveResults map: { teamName: ["W"/"D"/"L", ...] }
  const liveResults = {};
  
  sorted.forEach(f => {
    const home = normalizeName(f.home_team);
    const away = normalizeName(f.away_team);
    
    if (f.result && f.result.ft) {
      const [homeGoals, awayGoals] = f.result.ft;
      
      let homeRes = "D";
      let awayRes = "D";
      if (homeGoals > awayGoals) {
        homeRes = "W";
        awayRes = "L";
      } else if (homeGoals < awayGoals) {
        homeRes = "L";
        awayRes = "W";
      }
      
      if (!liveResults[home]) liveResults[home] = [];
      if (!liveResults[away]) liveResults[away] = [];
      
      liveResults[home].push(homeRes);
      liveResults[away].push(awayRes);
    }
  });

  const finalForm = {};
  Object.keys(teams).forEach(id => {
    const t = teams[id];
    const staticArray = form[id] || [];
    
    const normName = normalizeName(t.name);
    const liveArray = liveResults[normName] || [];
    
    const reversedLive = [...liveArray].reverse();
    finalForm[id] = [...reversedLive, ...staticArray].slice(0, 6);
  });

  return finalForm;
}

export function getH2H(teamA, teamB) {
  const idA = typeof teamA === 'string' ? teamA : teamA?.id;
  const idB = typeof teamB === 'string' ? teamB : teamB?.id;
  if (!h2h[idA] || !h2h[idA][idB]) return null;
  return h2h[idA][idB];
}

export { tournament as TOURNAMENT };

// Initialize cache if in browser context before mapping TEAMS
if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
  initializeLocalStorageCache();
}

// Export TEAMS as array for compatibility with dropdown population and backtesting
export const TEAMS = Object.keys(teams).filter(id => WC_48_TEAMS.has(id)).map(id => getTeamData(id));

export function reloadTeams() {
  TEAMS.length = 0;
  TEAMS.push(...Object.keys(teams).filter(id => WC_48_TEAMS.has(id)).map(id => getTeamData(id)));
}

export { h2h as H2H_RECORDS }; // For any temporary compatibility if needed
