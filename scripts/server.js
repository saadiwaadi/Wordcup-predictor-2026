// scripts/server.js
import express from 'express';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env
dotenv.config({ path: path.join(__dirname, '../.env') });

const apiKey = process.env.API_FOOTBALL_KEY;

const app = express();
const PORT = 3001;

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

// Enable CORS
app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// JSON body parsing support
app.use(express.json());

// Log state variables
let logBuffer = [];
let activeClients = [];
let isPulling = false;

// POST /api/pull -> Spawns the pullAllTeams script
app.post('/api/pull', (req, res) => {
  if (isPulling) {
    return res.status(400).json({ error: "Data pull already in progress" });
  }

  isPulling = true;
  logBuffer = []; // reset buffer
  
  const child = spawn('node', [path.join(__dirname, 'pullAllTeams.js')]);
  
  const handleLine = (line) => {
    logBuffer.push(line);
    activeClients.forEach(client => {
      client.write(`data: ${JSON.stringify({ log: line })}\n\n`);
    });
  };

  child.stdout.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.trim()) handleLine(line);
    });
  });

  child.stderr.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.trim()) handleLine(`ERROR: ${line}`);
    });
  });

  child.on('close', (code) => {
    handleLine(`PROCESS EXITED WITH CODE ${code}`);
    isPulling = false;
    activeClients.forEach(client => client.end());
    activeClients = [];
  });

  res.json({ started: true });
});

// GET /api/pull-stream -> SSE endpoint for streaming logs
app.get('/api/pull-stream', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  // Flush buffer immediately
  logBuffer.forEach(line => {
    res.write(`data: ${JSON.stringify({ log: line })}\n\n`);
  });

  if (isPulling) {
    activeClients.push(res);
    req.on('close', () => {
      activeClients = activeClients.filter(c => c !== res);
    });
  } else {
    res.write(`data: ${JSON.stringify({ log: "No active pull process." })}\n\n`);
    res.end();
  }
});

// GET /api/injuries?team={teamCode} -> Fetches injuries for the team for season=2025
app.get('/api/injuries', async (req, res) => {
  const teamCode = req.query.team;
  if (!teamCode || !TEAM_MAP[teamCode]) {
    return res.status(400).json({ error: "Invalid or missing team code parameter" });
  }

  if (!apiKey) {
    return res.status(500).json({ error: "API_FOOTBALL_KEY is missing on server" });
  }

  const { apiId, name } = TEAM_MAP[teamCode];
  const url = `https://v3.football.api-sports.io/injuries?team=${apiId}&season=2025`;

  try {
    const response = await fetch(url, {
      headers: { 'x-apisports-key': apiKey }
    });

    if (!response.ok) {
      throw new Error(`API-Football error: ${response.statusText}`);
    }

    const data = await response.json();
    const injuriesList = data.response || [];

    // Map to simple array of injured player names
    const injuredPlayers = injuriesList.map(item => item.player.name);

    const result = {
      team_id: teamCode,
      injured_players: injuredPlayers,
      updated_at: new Date().toISOString()
    };

    // Save to cache file
    const cacheDir = path.join(__dirname, '../data/cache');
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }

    fs.writeFileSync(
      path.join(cacheDir, `${teamCode}_injuries.json`),
      JSON.stringify(result, null, 2)
    );

    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/cache-status -> Scan cache status for all 48 teams
app.get('/api/cache-status', (req, res) => {
  const cacheDir = path.join(__dirname, '../data/cache');
  const teamCodes = Object.keys(TEAM_MAP);
  const statusList = [];

  teamCodes.forEach(code => {
    const squadPath = path.join(cacheDir, `${code}.json`);
    const injuryPath = path.join(cacheDir, `${code}_injuries.json`);
    
    let playerCount = 0;
    const qualityBreakdown = { FULL: 0, PARTIAL: 0, MINIMAL: 0, UNKNOWN: 0 };
    let lastPulled = null;
    let injuryAge = null;

    if (fs.existsSync(squadPath)) {
      try {
        const fileContent = JSON.parse(fs.readFileSync(squadPath, 'utf8'));
        const squad = fileContent.squad || [];
        playerCount = squad.length;
        
        squad.forEach(p => {
          qualityBreakdown[p.data_quality] = (qualityBreakdown[p.data_quality] || 0) + 1;
        });

        const stat = fs.statSync(squadPath);
        lastPulled = stat.mtime;
      } catch (err) {
        // Ignore JSON error
      }
    }

    if (fs.existsSync(injuryPath)) {
      try {
        const stat = fs.statSync(injuryPath);
        injuryAge = stat.mtime;
      } catch (err) {
        // Ignore
      }
    }

    statusList.push({
      code,
      name: TEAM_MAP[code].name,
      playerCount,
      qualityBreakdown,
      lastPulled,
      injuryAge
    });
  });

  res.json({ teams: statusList });
});

// Serve cached folder statically
app.use('/cache', express.static(path.join(__dirname, '../data/cache')));

app.listen(PORT, () => {
  console.log(`ORACLE-26 Backend Server running on http://localhost:${PORT}`);
});
