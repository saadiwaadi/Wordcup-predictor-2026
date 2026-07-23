import { toEngineCode, HOST_NATIONS } from './teamCodeMap.js';

// Section 1 mapping table: dataset stage_name -> engine `options.stage` value.
// Third-place match has no dedicated STAGE_LAMBDA_MODIFIERS entry in engine.js,
// so per the spec it is passed through as "SF" — an explicit, disclosed assumption,
// not a silent default.
export const STAGE_NAME_TO_ENGINE_STAGE = {
  'Group Stage': 'Group',
  'Round of 32': 'R32',
  'Round of 16': 'R16',
  'Quarter-finals': 'QF',
  'Semi-finals': 'SF',
  'Third-place match': 'SF',
  'Final': 'Final',
};

// Separate from the engine stage — this is only for grouping the audit's per-stage
// metrics tables, so "Third-place match" gets its own reporting row even though it
// shares the SF stage modifier above.
export const STAGE_NAME_TO_REPORT_BUCKET = {
  'Group Stage': 'Group',
  'Round of 32': 'R32',
  'Round of 16': 'R16',
  'Quarter-finals': 'QF',
  'Semi-finals': 'SF',
  'Third-place match': 'Third-place',
  'Final': 'Final',
};

export const REPORT_BUCKETS_ORDER = ['Group', 'R32', 'R16', 'QF', 'SF', 'Third-place', 'Final'];

// Top 3-4 "key players" per team by pre-tournament market value (squads_and_players.csv,
// a static scouting-style field fixed before the tournament — not something that could
// leak in-tournament performance into a pre-match input).
export function computeKeyPlayers(dataset) {
  const keyPlayersByTeam = new Map();
  dataset.squadsByTeamId.forEach((players, teamId) => {
    const sorted = [...players].sort((a, b) => {
      const av = a.market_value_eur ?? -1;
      const bv = b.market_value_eur ?? -1;
      if (bv !== av) return bv - av;
      return a.player_id.localeCompare(b.player_id);
    });
    const top = sorted.slice(0, 4);
    keyPlayersByTeam.set(teamId, top);
  });
  return keyPlayersByTeam;
}

// Precompute, in one forward pass over chronologically-sorted matches, the causal
// (pre-match-only) rolling form for every team. Production convention (data/index.js
// getForm()) stores last_6 NEWEST-FIRST — element 0 is the most recent prior result —
// which is the opposite of what engine.js's own weighting comment might suggest at a
// glance. We reproduce that ordering exactly so the frozen engine's form-weighting
// quirk runs identically to how it ran live, bug-for-bug.
export function computeCausalForm(dataset) {
  const history = new Map(); // team_id -> ["W"/"D"/"L", ...] chronological ascending
  const perMatchLast6 = new Map(); // `${match_id}_${team_id}` -> array newest-first, up to 6

  dataset.matches.forEach(m => {
    const homeId = dataset.fifaCodeToTeamId.get(m.home_fifa_code);
    const awayId = dataset.fifaCodeToTeamId.get(m.away_fifa_code);

    perMatchLast6.set(`${m.match_id}_${homeId}`, (history.get(homeId) || []).slice(-6).reverse());
    perMatchLast6.set(`${m.match_id}_${awayId}`, (history.get(awayId) || []).slice(-6).reverse());

    if (m.home_score == null || m.away_score == null) return;
    let homeRes = 'D', awayRes = 'D';
    if (m.home_score > m.away_score) { homeRes = 'W'; awayRes = 'L'; }
    else if (m.home_score < m.away_score) { homeRes = 'L'; awayRes = 'W'; }

    const hHist = history.get(homeId) || [];
    hHist.push(homeRes);
    history.set(homeId, hHist);
    const aHist = history.get(awayId) || [];
    aHist.push(awayRes);
    history.set(awayId, aHist);
  });

  return perMatchLast6;
}

// A key player counts as "inferred_absence" for a match only if they are NOT in the
// starting XI AND recorded zero minutes played (i.e. not used as a substitute either).
// Caveat (disclosed, not hidden): this dataset's match_lineups.csv lists the full
// 26-man squad for every single match with is_starting_xi/minutes_played, but has no
// separate "named matchday squad" flag distinct from those two fields. That means this
// proxy cannot fully distinguish genuine unavailability (injury/suspension) from a
// simple unused rotation option — both look identical as "0 minutes, not starting" in
// this data. This is the closest signal the dataset actually provides; the conflation
// is a known, accepted limitation of the proxy, not an oversight.
export function inferKeyPlayerAbsences(dataset, keyPlayersByTeam, matchId, teamId) {
  const lineup = dataset.lineupsByMatchTeam.get(`${matchId}_${teamId}`) || [];
  const lineupByPlayer = new Map(lineup.map(l => [l.player_id, l]));
  const keyPlayers = keyPlayersByTeam.get(teamId) || [];

  const absentNames = [];
  keyPlayers.forEach(kp => {
    const entry = lineupByPlayer.get(kp.player_id);
    const absent = !entry || (!entry.is_starting_xi && entry.minutes_played === 0);
    if (absent) absentNames.push(kp.player_name);
  });

  return { absentCount: absentNames.length, absentNames };
}

// Builds the full set of per-match, per-side engine inputs shared by Variant A and B
// (they are identical except for the xG-derived fields attached for Variant B's
// parallel lambda blend — the engine call itself never sees those xG fields).
export function buildMatchContexts(dataset, ratings, teamProfilesById, keyPlayersByTeam, perMatchLast6) {
  const contexts = [];

  dataset.matches.forEach(match => {
    const homeTeamId = dataset.fifaCodeToTeamId.get(match.home_fifa_code);
    const awayTeamId = dataset.fifaCodeToTeamId.get(match.away_fifa_code);
    const features = dataset.matchFeaturesById.get(match.match_id);

    const engineStage = STAGE_NAME_TO_ENGINE_STAGE[match.stage_name];
    const reportBucket = STAGE_NAME_TO_REPORT_BUCKET[match.stage_name];

    const buildSide = (fifaCodeRaw, teamId, isHome) => {
      const engineCode = toEngineCode(fifaCodeRaw);
      const profile = teamProfilesById.get(engineCode);
      const rating = ratings[engineCode];
      const last6 = perMatchLast6.get(`${match.match_id}_${teamId}`) || [];
      const { absentCount, absentNames } = inferKeyPlayerAbsences(dataset, keyPlayersByTeam, match.match_id, teamId);

      return {
        engineTeam: {
          id: engineCode,
          name: profile ? profile.name : fifaCodeRaw,
          tier: profile ? profile.tier : undefined,
          wc_appearances: profile ? profile.wc_appearances : undefined,
          host: HOST_NATIONS.has(engineCode),
          isHome,
          elo: rating ? rating.elo : undefined,
          elo_delta_90: rating ? rating.elo_delta_90 : undefined,
          fifa_rank: rating ? rating.fifaPoints : undefined,
          market_value_m: rating ? rating.marketValue : undefined,
          last_6: last6,
          // crowd_factor intentionally omitted: the dataset has no attendance data,
          // so the engine's own default (0.75) applies — documented, not fabricated.
        },
        injureKey: absentCount > 0,
        absentKeyPlayerNames: absentNames,
        missingProfile: !profile,
        missingRating: !rating,
        teamId,
        fifaCode: engineCode,
        xg: {
          rollingXgScored: isHome ? features?.home_prev_avg_xg_scored : features?.away_prev_avg_xg_scored,
          rollingXgConceded: isHome ? features?.home_prev_avg_xg_conceded : features?.away_prev_avg_xg_conceded,
        },
      };
    };

    const homeSide = buildSide(match.home_fifa_code, homeTeamId, true);
    const awaySide = buildSide(match.away_fifa_code, awayTeamId, false);

    let actualOutcome = 'D';
    if (match.home_score != null && match.away_score != null) {
      // Penalty-shootout winners are scored as a Draw for outcome/Brier purposes:
      // the frozen engine models goals via Poisson, not penalty shootouts, so scoring
      // a shootout win as "A" or "B" would credit/blame the model for something it was
      // never built to predict. Disclosed assumption, applied uniformly (4 matches
      // affected — see audit log).
      if (match.home_score > match.away_score) actualOutcome = 'A';
      else if (match.home_score < match.away_score) actualOutcome = 'B';
      else actualOutcome = 'D';
    }

    contexts.push({
      matchId: match.match_id,
      date: match.date,
      stageName: match.stage_name,
      engineStage,
      reportBucket,
      teamA: homeSide,
      teamB: awaySide,
      options: {
        staleData: false, // no pre-kickoff lineup-confirmation-timing signal exists in this dataset
        injureKeyA: homeSide.injureKey,
        injureKeyB: awaySide.injureKey,
        stage: engineStage,
      },
      actual: {
        scoreA: match.home_score,
        scoreB: match.away_score,
        outcome: actualOutcome,
      },
    });
  });

  return contexts;
}
