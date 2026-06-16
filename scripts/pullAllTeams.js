// scripts/pullAllTeams.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from project root
dotenv.config({ path: path.join(__dirname, '../.env') });

const apiKey = process.env.API_FOOTBALL_KEY;
if (!apiKey) {
  console.error("ERROR: API_FOOTBALL_KEY is missing in your .env file.");
  process.exit(1);
}

// 48 qualified World Cup 2026 teams mapped to API-Football IDs
const TEAM_MAP = {
  "BRA": { apiId: 6, name: "Brazil" },
  "FRA": { apiId: 2, name: "France" },
  "ENG": { apiId: 10, name: "England" },
  "GER": { apiId: 25, name: "Germany" },
  "ESP": { apiId: 9, name: "Spain" },
  "ARG": { apiId: 26, name: "Argentina" },
  "POR": { apiId: 27, name: "Portugal" },
  "NED": { apiId: 11, name: "Netherlands" },
  "BEL": { apiId: 1, name: "Belgium" },
  "CRO": { apiId: 3, name: "Croatia" },
  "SEN": { apiId: 13, name: "Senegal" },
  "MAR": { apiId: 31, name: "Morocco" },
  "JPN": { apiId: 12, name: "Japan" },
  "USA": { apiId: 16, name: "United States" },
  "MEX": { apiId: 15, name: "Mexico" },
  "CAN": { apiId: 14, name: "Canada" },
  "COL": { apiId: 8, name: "Colombia" },
  "URU": { apiId: 7, name: "Uruguay" },
  "SUI": { apiId: 17, name: "Switzerland" },
  "SRB": { apiId: 1464, name: "Serbia" },
  "DEN": { apiId: 21, name: "Denmark" },
  "AUT": { apiId: 22, name: "Austria" },
  "TUR": { apiId: 23, name: "Turkey" },
  "KOR": { apiId: 24, name: "South Korea" },
  "POL": { apiId: 28, name: "Poland" },
  "AUS": { apiId: 29, name: "Australia" },
  "IRN": { apiId: 30, name: "Iran" },
  "ECU": { apiId: 1187, name: "Ecuador" },
  "NGR": { apiId: 19, name: "Nigeria" },
  "GHA": { apiId: 1504, name: "Ghana" },
  "CMR": { apiId: 1530, name: "Cameroon" },
  "EGY": { apiId: 32, name: "Egypt" },
  "ALG": { apiId: 1395, name: "Algeria" },
  "CIV": { apiId: 1459, name: "Ivory Coast" },
  "SAU": { apiId: 222, name: "Saudi Arabia" },
  "QAT": { apiId: 1561, name: "Qatar" },
  "CRI": { apiId: 1460, name: "Costa Rica" },
  "PAN": { apiId: 1461, name: "Panama" },
  "VEN": { apiId: 1462, name: "Venezuela" },
  "CHI": { apiId: 1465, name: "Chile" },
  "ROU": { apiId: 1467, name: "Romania" },
  "UKR": { apiId: 1083, name: "Ukraine" },
  "RSA": { apiId: 1469, name: "South Africa" },
  "CZE": { apiId: 1470, name: "Czechia" },
  "PAR": { apiId: 1472, name: "Paraguay" },
  "SCO": { apiId: 1473, name: "Scotland" },
  "SWE": { apiId: 1476, name: "Sweden" },
  "TUN": { apiId: 1477, name: "Tunisia" }
};

const LEAGUE_COEFFS = {
  39: 1.00,  // Premier League
  140: 1.00, // La Liga
  78: 1.00,  // Bundesliga
  135: 0.92, // Serie A
  61: 0.92,  // Ligue 1
  88: 0.85,  // Eredivisie
  94: 0.85,  // Primeira Liga
  253: 0.78, // MLS
  262: 0.78, // Liga MX
  307: 0.72, // Saudi Pro League
};

const POS_MAP = {
  "Goalkeeper": "GK",
  "Defender":   "CB",
  "Midfielder": "CM",
  "Attacker":   "FW"
};

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function fetchTeamData(teamCode, apiId) {
  const headers = { 'x-apisports-key': apiKey };
  
  // Call 1: Squad
  const squadRes = await fetch(`https://v3.football.api-sports.io/players/squads?team=${apiId}`, { headers });
  if (!squadRes.ok) throw new Error(`Squad API error: ${squadRes.statusText}`);
  const squadData = await squadRes.json();
  
  // Call 2: Stats (Season 2024)
  const statsRes = await fetch(`https://v3.football.api-sports.io/players?team=${apiId}&season=2024`, { headers });
  if (!statsRes.ok) throw new Error(`Stats API error: ${statsRes.statusText}`);
  const statsData = await statsRes.json();

  return { squadData, statsData };
}

async function run() {
  const cacheDir = path.join(__dirname, '../data/cache');
  if (!fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir, { recursive: true });
  }

  const teamCodes = Object.keys(TEAM_MAP);
  console.log(`Starting squad pull for ${teamCodes.length} teams...`);
  
  let successCount = 0;

  for (let i = 0; i < teamCodes.length; i++) {
    const code = teamCodes[i];
    const { apiId, name } = TEAM_MAP[code];
    console.log(`[${i + 1}/${teamCodes.length}] Pulling ${name} (${code}) [ID: ${apiId}]...`);
    
    try {
      const { squadData, statsData } = await fetchTeamData(code, apiId);
      
      const squadPlayers = squadData.response?.[0]?.players || [];
      const statsPlayers = statsData.response || [];

      // Create lookup of stats by player name or ID
      const statsLookup = {};
      statsPlayers.forEach(item => {
        if (item.player && item.player.id) {
          statsLookup[item.player.id] = item;
        }
      });

      // Process players
      let processedPlayers = squadPlayers.map(p => {
        const match = statsLookup[p.id];
        const stats = match?.statistics?.[0];

        const goals = stats?.goals?.total || 0;
        const minutes = stats?.games?.minutes || 0;
        const shotsOn = stats?.shots?.on || 0;
        const shotsTotal = stats?.shots?.total || 0;
        const leagueId = stats?.league?.id;

        const xG_approx = minutes > 0
          ? ((goals / minutes) * 90 * 0.85) + ((shotsTotal > 0 ? (shotsOn / shotsTotal) : 0) * 0.15)
          : 0.00;

        const data_quality = (goals > 0 && minutes > 270) ? "FULL"
                           : (minutes > 90) ? "PARTIAL"
                           : (minutes > 0)  ? "MINIMAL"
                           : "UNKNOWN";

        const mappedPos = POS_MAP[p.position] || "CB";

        return {
          name: p.name,
          position: mappedPos,
          club_appearances: stats?.games?.appearences || 0,
          caps: 0,
          caps_source: "UNAVAILABLE",
          data_quality,
          is_starter: false, // will update below
          xG_intl_per90: 0.00,
          xG_club_per90: xG_approx,
          league_difficulty_coeff: LEAGUE_COEFFS[leagueId] || 0.75,
          xG_best_single_match: 0.00,
          best_match_source: "UNAVAILABLE",
          mean_xG_per90: xG_approx,
          xG_approx,
          xG_source: "APPROX",
          minutes // temporary for sorting
        };
      });

      // Sort & Select Starters:
      // 1. Separate GKs and outfielders
      const gks = processedPlayers.filter(p => p.position === "GK").sort((a, b) => b.minutes - a.minutes);
      const outfield = processedPlayers.filter(p => p.position !== "GK").sort((a, b) => b.minutes - a.minutes);

      // 2. Mark starter GK
      if (gks.length > 0) {
        gks[0].is_starter = true;
      }
      // 3. Mark top 10 outfielders
      for (let j = 0; j < Math.min(10, outfield.length); j++) {
        outfield[j].is_starter = true;
      }

      // Recombine and remove temporary minutes key
      const finalSquad = [...gks, ...outfield].map(p => {
        const { minutes, ...cleanPlayer } = p;
        return cleanPlayer;
      });

      // Save to cache file
      const resultObj = {
        team_id: code,
        squad: finalSquad,
        updated_at: new Date().toISOString()
      };

      fs.writeFileSync(
        path.join(cacheDir, `${code}.json`),
        JSON.stringify(resultObj, null, 2)
      );

      // Compute statistics for log line
      const qualityCount = { FULL: 0, PARTIAL: 0, MINIMAL: 0, UNKNOWN: 0 };
      finalSquad.forEach(p => {
        qualityCount[p.data_quality] = (qualityCount[p.data_quality] || 0) + 1;
      });

      console.log(`[SUCCESS] ${code}: ${finalSquad.length} players. Breakdown: FULL=${qualityCount.FULL}, PARTIAL=${qualityCount.PARTIAL}, MINIMAL=${qualityCount.MINIMAL}, UNKNOWN=${qualityCount.UNKNOWN}`);
      successCount++;
    } catch (err) {
      console.error(`[ERROR] Failed to fetch or process ${code}: ${err.message}`);
    }

    // Rate-limiting delay
    if (i < teamCodes.length - 1) {
      await delay(1200);
    }
  }

  console.log(`\nSquad pull process complete. Successfully pulled ${successCount}/${teamCodes.length} teams.`);
}

run().catch(err => {
  console.error("FATAL ERROR in pull script:", err);
  process.exit(1);
});
