export function simpleHash(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return hash.toString(16);
}

export function deltaUpdateTeam(teamId, incomingSquad, incomingStats) {
  const key = `oracle26_team_${teamId}`;
  const stored = JSON.parse(localStorage.getItem(key) || 'null');
  const incomingHash = simpleHash(JSON.stringify({ incomingSquad, incomingStats }));

  if (stored && stored.hash === incomingHash) {
    return { updated: false, reason: "NO_CHANGE" };
  }

  // Find what actually changed
  const changes = [];
  if (stored) {
    incomingSquad.forEach(player => {
      const old = stored.squad.find(p => p.id === player.id);
      if (!old) changes.push(`ADDED: ${player.name}`);
      else if (JSON.stringify(old) !== JSON.stringify(player)) {
        changes.push(`UPDATED: ${player.name}`);
      }
    });
  }

  localStorage.setItem(key, JSON.stringify({
    team_id: teamId,
    squad: incomingSquad,
    stats: incomingStats,
    hash: incomingHash,
    updated_at: new Date().toISOString(),
    pull_count: stored ? stored.pull_count + 1 : 1
  }));

  return { updated: true, changes };
}
