import { TEAMS as teams } from './teams.js';
import { RATINGS as ratings } from './ratings.js';
import { FORM as form } from './form.js';
import { H2H as h2h } from './h2h.js';
import { TOURNAMENT as tournament } from './tournament.js';

export function getTeamData(teamId) {
  const team = teams[teamId];
  if (!team) return null;
  const rating = ratings[teamId] || {};
  const teamForm = form[teamId] || [];
  
  return {
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
    injuries: team.injuries,
    confederation: team.confederation,
    players: team.players || []
  };
}

export function getRatings() {
  return ratings;
}

export function getForm() {
  return form;
}

export function getH2H(teamA, teamB) {
  const idA = typeof teamA === 'string' ? teamA : teamA?.id;
  const idB = typeof teamB === 'string' ? teamB : teamB?.id;
  if (!h2h[idA] || !h2h[idA][idB]) return null;
  return h2h[idA][idB];
}

export { tournament as TOURNAMENT };

// Export TEAMS as array for compatibility with dropdown population and backtesting
export const TEAMS = Object.keys(teams).map(id => getTeamData(id));
export { h2h as H2H_RECORDS }; // For any temporary compatibility if needed
