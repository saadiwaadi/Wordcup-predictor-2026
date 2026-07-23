// Minimal CSV parser. Verified against every file in data/raw/: none of them
// use quoting or embedded commas (checked with `grep -c '"'` before writing this),
// so a plain split is safe and a full RFC4180 parser would be unused complexity.
export function parseCSV(text) {
  const lines = text.split('\n').filter(l => l.length > 0);
  const header = lines[0].split(',');
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split(',');
    const row = {};
    header.forEach((key, idx) => {
      row[key] = cells[idx] === undefined ? '' : cells[idx];
    });
    rows.push(row);
  }
  return rows;
}

export function num(v) {
  if (v === '' || v === undefined || v === null) return null;
  const n = Number(v);
  return Number.isNaN(n) ? null : n;
}

export function bool(v) {
  return v === 'True' || v === 'true' || v === '1';
}
