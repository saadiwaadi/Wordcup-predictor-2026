const fs = require('fs');
const path = require('path');
const files = ['style.css', 'index.html', 'app.js'];

for (const file of files) {
  const filePath = path.join(__dirname, '..', file);
  if (!fs.existsSync(filePath)) continue;
  const lines = fs.readFileSync(filePath, 'utf8').split('\n');
  lines.forEach((line, i) => {
    if (line.match(/(color|fill)\s*:\s*#[345][345a-f][345a-f]/i) || line.match(/#[34567][34567][34567]/i)) {
      if (line.includes('color:') || line.includes('color :')) {
        console.log(`[${file}:${i + 1}] ${line.trim()}`);
      }
    }
  });
}
