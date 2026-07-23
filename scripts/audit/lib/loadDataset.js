import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseCSV, num, bool } from './csv.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const RAW_DIR = path.join(__dirname, '..', 'data', 'raw');

function readCSV(name) {
  const text = fs.readFileSync(path.join(RAW_DIR, name), 'utf-8');
  return parseCSV(text);
}

export function loadDataset() {
  const teamsRaw = readCSV('teams.csv');
  const venuesRaw = readCSV('venues.csv');
  const stagesRaw = readCSV('tournament_stages.csv');
  const refereesRaw = readCSV('referees.csv');
  const matchesDetailedRaw = readCSV('matches_detailed.csv');
  const squadsRaw = readCSV('squads_and_players.csv');
  const matchTeamStatsRaw = readCSV('match_team_stats.csv');
  const matchLineupsRaw = readCSV('match_lineups.csv');
  const matchFeaturesRaw = readCSV('match_prediction_features.csv');

  const teamsById = new Map();
  teamsRaw.forEach(r => {
    teamsById.set(r.team_id, {
      team_id: r.team_id,
      team_name: r.team_name,
      fifa_code: r.fifa_code,
      group_letter: r.group_letter,
      confederation: r.confederation,
      fifa_ranking_pre_tournament: num(r.fifa_ranking_pre_tournament),
      elo_rating: num(r.elo_rating),
      manager_name: r.manager_name,
    });
  });

  const stagesById = new Map();
  stagesRaw.forEach(r => {
    stagesById.set(r.stage_id, { stage_name: r.stage_name, is_knockout: bool(r.is_knockout) });
  });

  const venuesById = new Map();
  venuesRaw.forEach(r => {
    venuesById.set(r.venue_id, {
      stadium_name: r.stadium_name,
      city: r.city,
      country: r.country,
      capacity: num(r.capacity),
      elevation_meters: num(r.elevation_meters),
    });
  });

  // matches_detailed.csv is the primary match record: has team fifa_codes directly,
  // scores, xG, stage name as text. Sort chronologically — this ordering is what
  // makes causal (pre-match-only) form/xG computation possible.
  const matches = matchesDetailedRaw.map(r => ({
    match_id: r.match_id,
    date: r.date,
    kickoff_time_utc: r.kickoff_time_utc,
    stage_name: r.stage_name,
    stadium_name: r.stadium_name,
    home_team_name: r.home_team_name,
    home_fifa_code: r.home_fifa_code,
    away_team_name: r.away_team_name,
    away_fifa_code: r.away_fifa_code,
    home_score: num(r.home_score),
    away_score: num(r.away_score),
    status: r.status,
    home_xg: num(r.home_xg),
    away_xg: num(r.away_xg),
  })).sort((a, b) => {
    const dtA = `${a.date}T${a.kickoff_time_utc}`;
    const dtB = `${b.date}T${b.kickoff_time_utc}`;
    return dtA < dtB ? -1 : dtA > dtB ? 1 : 0;
  });

  const matchFeaturesById = new Map();
  matchFeaturesRaw.forEach(r => {
    matchFeaturesById.set(r.match_id, {
      home_team_id: r.home_team_id,
      away_team_id: r.away_team_id,
      home_is_host: bool(r.home_is_host),
      away_is_host: bool(r.away_is_host),
      home_prev_avg_xg_scored: num(r.home_prev_avg_xg_scored),
      home_prev_avg_xg_conceded: num(r.home_prev_avg_xg_conceded),
      away_prev_avg_xg_scored: num(r.away_prev_avg_xg_scored),
      away_prev_avg_xg_conceded: num(r.away_prev_avg_xg_conceded),
    });
  });

  // team_id -> fifa_code, needed because match_lineups/squads key by team_id
  const teamIdToFifaCode = new Map();
  teamsById.forEach((v, k) => teamIdToFifaCode.set(k, v.fifa_code));
  const fifaCodeToTeamId = new Map();
  teamsById.forEach((v, k) => fifaCodeToTeamId.set(v.fifa_code, k));

  const squadsByTeamId = new Map();
  squadsRaw.forEach(r => {
    const list = squadsByTeamId.get(r.team_id) || [];
    list.push({
      player_id: r.player_id,
      player_name: r.player_name,
      position: r.position,
      market_value_eur: num(r.market_value_eur),
      caps: num(r.caps),
    });
    squadsByTeamId.set(r.team_id, list);
  });

  // key: `${match_id}_${team_id}` -> array of {player_id, is_starting_xi, minutes_played}
  const lineupsByMatchTeam = new Map();
  matchLineupsRaw.forEach(r => {
    const key = `${r.match_id}_${r.team_id}`;
    const list = lineupsByMatchTeam.get(key) || [];
    list.push({
      player_id: r.player_id,
      is_starting_xi: bool(r.is_starting_xi) || r.is_starting_xi === '1',
      minutes_played: num(r.minutes_played) || 0,
    });
    lineupsByMatchTeam.set(key, list);
  });

  const teamStatsByMatchTeam = new Map();
  matchTeamStatsRaw.forEach(r => {
    teamStatsByMatchTeam.set(`${r.match_id}_${r.team_id}`, {
      possession_pct: num(r.possession_pct),
      total_shots: num(r.total_shots),
      shots_on_target: num(r.shots_on_target),
      corners: num(r.corners),
    });
  });

  return {
    teamsById,
    stagesById,
    venuesById,
    matches,
    matchFeaturesById,
    teamIdToFifaCode,
    fifaCodeToTeamId,
    squadsByTeamId,
    lineupsByMatchTeam,
    teamStatsByMatchTeam,
  };
}
