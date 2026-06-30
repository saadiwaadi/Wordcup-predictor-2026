import { TEAMS } from './teams.js';

// Define aliases mapping to canonical team codes (ISO/FIFA)
// All keys must be in lowercase for case-insensitive lookup.
const ALIASES = {
  // USA
  "usa": "USA",
  "united states": "USA",
  
  // Czechia / Czech Republic
  "czechia": "CZE",
  "czech republic": "CZE",
  "czechia republic": "CZE",

  // Bosnia & Herzegovina
  "bosnia & herzegovina": "BIH",
  "bosnia and herzegovina": "BIH",
  "bosnia-herzegovina": "BIH",

  // DR Congo
  "dr congo": "COD",
  "congo dr": "COD",
  "democratic republic of congo": "COD",

  // Ivory Coast
  "ivory coast": "CIV",
  "côte d'ivoire": "CIV",
  "cote d'ivoire": "CIV",

  // Cape Verde
  "cape verde": "CPV",
  "cabo verde": "CPV",

  // Turkey
  "turkey": "TUR",
  "türkiye": "TUR",

  // South Korea
  "south korea": "KOR",
  "korea republic": "KOR",

  // Iran
  "iran": "IRN",
  "ir iran": "IRN",
};

// Populate default mappings from canonical TEAMS names and codes to their codes (lowercase)
for (const [code, team] of Object.entries(TEAMS)) {
  const normName = team.name.toLowerCase();
  if (!ALIASES[normName]) {
    ALIASES[normName] = code;
  }
  // Also map code itself to code
  ALIASES[code.toLowerCase()] = code;
}

/**
 * Normalizes any team name, alias, or code to its canonical code (e.g. "USA", "CZE").
 * Case-insensitive.
 * @param {string} name - The input team name/alias/code
 * @returns {string|null} Canonical code, or null if not found
 */
export function getTeamCode(name) {
  if (!name) return null;
  const cleanName = name.trim().toLowerCase();
  return ALIASES[cleanName] || null;
}

/**
 * Normalizes any team name, alias, or code to its canonical database name (e.g. "United States", "Czechia").
 * Case-insensitive.
 * @param {string} name - The input team name/alias/code
 * @returns {string} Canonical team name, or the original input if not found
 */
export function normalizeName(name) {
  const code = getTeamCode(name);
  if (code && TEAMS[code]) {
    return TEAMS[code].name;
  }
  return name;
}

/**
 * Returns all known identifiers (names, aliases, codes) for a given team name/alias/code.
 * All return values are in their original case (or standard capitalization).
 * @param {string} nameOrCode
 * @returns {string[]} Array of identifiers
 */
export function getTeamIdentifiers(nameOrCode) {
  const code = getTeamCode(nameOrCode);
  if (!code) return nameOrCode ? [nameOrCode] : [];
  
  const identifiers = new Set();
  identifiers.add(code);
  if (TEAMS[code]) {
    identifiers.add(TEAMS[code].name);
  }
  
  // Find all aliases that map to this code
  for (const [alias, mappedCode] of Object.entries(ALIASES)) {
    if (mappedCode === code) {
      identifiers.add(alias);
      // Capitalize first letters of each word
      const titleCase = alias.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
      identifiers.add(titleCase);
      if (alias.includes('&')) {
        identifiers.add(alias.replace('&', 'and'));
        identifiers.add(titleCase.replace('&', 'and'));
      }
      if (alias.includes('and')) {
        identifiers.add(alias.replace('and', '&'));
        identifiers.add(titleCase.replace('and', '&'));
      }
    }
  }
  
  return Array.from(identifiers);
}
