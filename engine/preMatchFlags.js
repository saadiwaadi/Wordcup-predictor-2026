export function runPreMatchFlags(teamId) {
  const teamData = JSON.parse(localStorage.getItem(`oracle26_team_${teamId}`));
  const injuryData = JSON.parse(localStorage.getItem(`oracle26_injuries_${teamId}`));
  const flags = { critical: [], warning: [], info: [] };

  if (!teamData) {
    flags.critical.push("NO_DATA: Team record missing entirely");
    return flags;
  }

  const starters = (teamData.squad || []).filter(p => p.is_starter);
  const gk = starters.find(p => p.position === 'GK');
  const unknownCount = starters.filter(p => p.data_quality === 'UNKNOWN').length;
  const minimalCount = starters.filter(p => p.data_quality === 'MINIMAL').length;
  
  // Get top player sorted by xG_approx (or fall back to mean_xG_per90)
  const topPlayer = [...starters].sort((a, b) => {
    const xGA = a.xG_approx !== undefined ? a.xG_approx : (a.mean_xG_per90 || 0);
    const xGB = b.xG_approx !== undefined ? b.xG_approx : (b.mean_xG_per90 || 0);
    return xGB - xGA;
  })[0];

  // CRITICAL checks
  if (!gk || gk.data_quality === 'UNKNOWN') {
    flags.critical.push("GK_UNKNOWN: Goalkeeper data missing");
  }
  if (unknownCount > 3) {
    flags.critical.push(`STARTERS_UNKNOWN: ${unknownCount} starters have no data`);
  }

  // Injury data age check
  if (injuryData && injuryData.updated_at) {
    const updatedTime = new Date(injuryData.updated_at).getTime() || Date.now();
    const ageHrs = (Date.now() - updatedTime) / 3600000;
    if (ageHrs > 72) {
      flags.critical.push(`INJURY_STALE: Last updated ${Math.floor(ageHrs)}hrs ago`);
    } else if (ageHrs > 24) {
      flags.warning.push(`INJURY_AGING: Data is ${Math.floor(ageHrs)}hrs old`);
    }
  } else {
    flags.critical.push("INJURY_MISSING: No injury data pulled for this team");
  }

  // WARNING checks
  if (topPlayer && ['MINIMAL', 'UNKNOWN'].includes(topPlayer.data_quality)) {
    flags.warning.push(`TOP_PLAYER_WEAK: ${topPlayer.name} has ${topPlayer.data_quality} data`);
  }
  if (minimalCount >= 2) {
    flags.warning.push(`SQUAD_THIN: ${minimalCount} starters rated MINIMAL`);
  }

  // INFO checks
  starters.forEach(p => {
    if (p.xG_source === 'APPROX') {
      flags.info.push(`APPROX_XG: ${p.name} xG is approximated, not real`);
    }
  });

  return flags;
}
