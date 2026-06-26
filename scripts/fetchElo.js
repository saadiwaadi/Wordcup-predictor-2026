// scripts/fetchElo.js
import fs from 'fs';
import path from 'path';

const url = 'https://www.eloratings.net/World.tsv';

const MAPPING = {
  "AR": "ARG", "ES": "ESP", "FR": "FRA",
  "EN": "ENG", "BR": "BRA", "PT": "POR",
  "NL": "NED", "BE": "BEL", "HR": "CRO",
  "DE": "GER", "IT": "ITA", "MX": "MEX",
  "US": "USA", "CO": "COL", "UY": "URU",
  "SN": "SEN", "MA": "MAR", "JP": "JPN",
  "IR": "IRN", "AU": "AUS", "CH": "SUI",
  "DK": "DEN", "SE": "SWE", "PL": "POL",
  "RS": "SRB", "AT": "AUT", "TR": "TUR",
  "UA": "UKR", "GH": "GHA", "EG": "EGY",
  "NG": "NGR", "SA": "SAU", "QA": "QAT",
  "CM": "CMR", "TN": "TUN", "EC": "ECU",
  "PA": "PAN", "CR": "CRI", "SV": "SLV",
  "CA": "CAN", "ZA": "RSA", "KR": "KOR",
  "CZ": "CZE", "RO": "ROU", "GE": "GEO",
  "SI": "SLO", "DZ": "ALG", "VE": "VEN",
  "CL": "CHI", "IQ": "IRQ", "JO": "JOR",
  "NO": "NOR", "NZ": "NZL", "HT": "HAI",
  "UZ": "UZB", "CD": "COD", "CV": "CPV",
  "CI": "CIV", "SC": "SCO", "BA": "BIH",
  "CW": "CUW", "PY": "PAR", "SY": "SYR"
};

const WC_48 = new Set([
  "ARG", "ESP", "FRA", "ENG", "POR", "BRA", "NED", "MAR", "BEL", "GER",
  "CRO", "COL", "SEN", "MEX", "URU", "JPN", "USA", "SUI", "DEN", "AUT",
  "UKR", "KOR", "TUR", "POL", "AUS", "SWE", "SRB", "ECU", "IRN", "CAN",
  "VEN", "CZE", "SCO", "NGR", "ROU", "CHI", "TUN", "EGY", "ALG", "PAR",
  "GHA", "CMR", "CIV", "CRI", "SAU", "RSA", "PAN", "QAT"
]);

async function fetchElo() {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch Elo ratings: ${response.status} ${response.statusText}`);
    }
    const text = await response.text();
    const lines = text.split('\n');

    const parsedWC = [];
    const unmappedList = new Set();
    const cacheTeams = {};

    lines.forEach(line => {
      if (!line.trim()) return;
      const cols = line.split('\t');
      if (cols.length < 11) return;

      const rank = parseInt(cols[0], 10);
      const rawCode = cols[2];
      const elo = parseInt(cols[3], 10);
      let rawDelta = cols[10] || '0';

      // Parse delta value
      rawDelta = rawDelta.replace(/\u2212/g, '-').replace(/−/g, '-').trim();
      let delta = parseInt(rawDelta, 10);
      if (isNaN(delta)) {
        delta = 0;
      }

      const mappedCode = MAPPING[rawCode];
      if (!mappedCode) {
        console.log(`UNMAPPED: ${rawCode} rank ${rank} Elo ${elo}`);
        unmappedList.add(rawCode);
        return;
      }

      if (WC_48.has(mappedCode)) {
        parsedWC.push({
          rank,
          code: mappedCode,
          elo,
          delta
        });
        cacheTeams[mappedCode] = { elo, rank, delta };
      }
    });

    // Sort by Elo descending
    parsedWC.sort((a, b) => b.elo - a.elo);

    // Print sorted WC team results
    parsedWC.forEach(item => {
      const deltaStr = item.delta >= 0 ? `+${item.delta}` : `${item.delta}`;
      console.log(`[${item.rank}] ${item.code} | Elo: ${item.elo} | delta: ${deltaStr}`);
    });

    console.log(`FOUND: ${parsedWC.length}/48 teams`);
    console.log(`UNMAPPED codes: ${[...unmappedList].sort().join(', ')}`);

    // Save to cache/elo_cache.json
    const cacheData = {
      fetchedAt: new Date().toISOString(),
      teams: cacheTeams
    };

    const cacheDir = path.join(process.cwd(), 'cache');
    if (!fs.existsSync(cacheDir)) {
      fs.mkdirSync(cacheDir, { recursive: true });
    }
    fs.writeFileSync(path.join(cacheDir, 'elo_cache.json'), JSON.stringify(cacheData, null, 2), 'utf8');

  } catch (error) {
    console.error('Error processing Elo ratings:', error);
  }
}

fetchElo();
