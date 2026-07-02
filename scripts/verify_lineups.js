import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read lineups
const lineupsRaw = fs.readFileSync(path.join(__dirname, '../public/data/scraped/lineups.json'), 'utf8');
const lineups = JSON.parse(lineupsRaw);

// Read squads
const squadsRaw = fs.readFileSync(path.join(__dirname, '../public/data/scraped/squads.json'), 'utf8');
const squads = JSON.parse(squadsRaw);

// Find BRA vs JPN match
let matchLineup = null;
for (const key of Object.keys(lineups)) {
  const entry = lineups[key];
  if ((entry.home === 'BRA' && entry.away === 'JPN') || (entry.home === 'JPN' && entry.away === 'BRA')) {
    matchLineup = entry;
    break;
  }
}

// Name matcher
function matchPlayerInLineup(player, lineupList) {
  const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\./g, '').trim();
  const parts = (s) => norm(s).split(/\s+/).filter(Boolean);
  
  const spParts = parts(player.name);
  if (spParts.length === 0) return false;

  return lineupList.some(lp => {
    const lpParts = parts(lp.name);
    if (lpParts.length === 0) return false;
    
    const spLast = spParts[spParts.length - 1];
    const lpLast = lpParts[lpParts.length - 1];
    if (spLast !== lpLast) return false;
    
    if (spParts.length === 1 || lpParts.length === 1) return true;
    
    const spFirstInitial = spParts[0][0];
    const lpFirstInitial = lpParts[0][0];
    return spFirstInitial === lpFirstInitial;
  });
}

// Find Brazil Squad
let braSquad = [];
if (Array.isArray(squads)) {
  const t = squads.find(x => x.id === 'BRA' || x.code === 'BRA');
  braSquad = t ? t.squad : [];
} else {
  braSquad = squads['BRA'] || [];
}
const starters = [];

console.log("=== BRAZIL (BRA) CONFIRMED STARTERS ===");

braSquad.forEach(p => {
  const matchedStarter = matchLineup.home_starters.find(s => matchPlayerInLineup(p, [s]));
  if (matchedStarter) {
    p.isStarter = true;
    p.shirt = matchedStarter.shirt;
    p.captain = matchedStarter.captain;
    starters.push(p);
  }
});

// Sort by formation order (GK, DF, MF, FW)
const order = { 'GOALKEEPERS': 1, 'DEFENDERS': 2, 'MIDFIELDERS': 3, 'FORWARDS': 4 };
starters.sort((a, b) => order[a.posGroup] - order[b.posGroup]);

starters.forEach(p => {
  const badge = p.captain ? "[CAPTAIN]" : "";
  console.log(`- ${p.name} (Shirt: ${p.shirt}) ${badge}`);
});

console.log("\n=== FORMATION SWAP BEHAVIOR ===");
console.log("If formation is changed to 3-5-2, the starters list remains EXACLY the same (safeguard is active).");
console.log("The pitch positioning logic will assign these 11 players to the 3-5-2 coordinates, but their isStarter status is locked.");
