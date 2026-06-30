import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function main() {
  try {
    // 1. Resolve and read cache
    const cachePath = fs.existsSync(path.join(__dirname, '../public/cache/openfootball_cache.json'))
      ? path.join(__dirname, '../public/cache/openfootball_cache.json')
      : path.join(__dirname, '../cache/openfootball_cache.json');

    const cacheContent = fs.readFileSync(cachePath, 'utf8');
    const cache = JSON.parse(cacheContent);

    // 2. Import TEAMS dynamically
    const indexModule = await import('../data/index.js');
    const TEAMS = indexModule.TEAMS || indexModule.default?.TEAMS;
    const nameToCode = Object.fromEntries(TEAMS.map(t => [t.name, t.id]));

    // 3. Filter completed (scored) matches
    const matches = (cache.matches?.matches || []).filter(m => m.score && m.score.ft && typeof m.score.ft[0] === 'number');

    // 4. Sort scored matches by date ascending (oldest first)
    matches.sort((a, b) => new Date(a.date) - new Date(b.date));

    // 5. Build results map
    const resultsMap = {};
    matches.forEach(m => {
      const code1 = nameToCode[m.team1];
      const code2 = nameToCode[m.team2];
      if (!code1 || !code2) return;

      const score1 = m.score.ft[0];
      const score2 = m.score.ft[1];

      let res1, res2;
      if (score1 > score2) {
        res1 = 'W';
        res2 = 'L';
      } else if (score1 < score2) {
        res1 = 'L';
        res2 = 'W';
      } else {
        res1 = 'D';
        res2 = 'D';
      }

      if (!resultsMap[code1]) resultsMap[code1] = [];
      resultsMap[code1].push(res1);

      if (!resultsMap[code2]) resultsMap[code2] = [];
      resultsMap[code2].push(res2);
    });

    // 6. Dynamically import current form object
    const formModule = await import('../data/form.js');
    const currentForm = formModule.FORM || formModule.default?.FORM || {};
    const updatedForm = { ...currentForm };

    // 7. Update FORM entries for all 48 teams
    TEAMS.forEach(team => {
      const code = team.id;
      if (resultsMap[code]) {
        // Take the last 6 results
        const last6 = resultsMap[code].slice(-6);
        updatedForm[code] = last6;
        console.log(`[FORM] ${code}: ${JSON.stringify(last6)} (${resultsMap[code].length} matches)`);
      } else {
        console.log(`[FORM] ${code}: no tournament results — keeping existing`);
      }
    });

    // 8. Write updated FORM back to data/form.js
    const formFilePath = path.join(__dirname, '../data/form.js');
    const formString = `// Update after each match — most recent result goes at index 0
export const FORM = ${JSON.stringify(updatedForm, null, 2)};
`;
    fs.writeFileSync(formFilePath, formString, 'utf8');
    console.log(`\nSuccessfully updated form data in ${formFilePath}`);
  } catch (error) {
    console.error('Error executing updateForm script:', error);
    process.exit(1);
  }
}

main();
