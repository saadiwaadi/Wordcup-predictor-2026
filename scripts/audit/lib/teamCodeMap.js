// The real-tournament dataset (mominullptr) uses "KSA" for Saudi Arabia.
// This repo's data/teams.js and data/ratings.js use "SAU" for the same team.
// No other code mismatches exist between the 48 real qualifiers and this repo's roster.
export const DATASET_TO_ENGINE_CODE = {
  KSA: 'SAU',
};

export function toEngineCode(datasetCode) {
  return DATASET_TO_ENGINE_CODE[datasetCode] || datasetCode;
}

export const HOST_NATIONS = new Set(['USA', 'MEX', 'CAN']);
