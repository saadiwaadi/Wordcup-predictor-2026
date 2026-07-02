const fs = require('fs');
const path = require('path');

const files = ['style.css', 'index.html', 'app.js'];
let totalReplaced = 0;

for (const file of files) {
  const filePath = path.join(__dirname, '..', file);
  if (!fs.existsSync(filePath)) continue;

  let content = fs.readFileSync(filePath, 'utf8');
  let replacedInFile = 0;

  // Insert variables in style.css
  if (file === 'style.css' && !content.includes('--text-secondary')) {
    content = content.replace(/:root\s*\{/, ":root {\n  --text-secondary: #9a9a9a;\n  --text-muted: #707070;");
  }

  // Find color:#333, color: #444, color: #4a4a4a, etc.
  // Using a regex to match common dark greys in styles
  const colorRegex = /(color|border(?:-[a-z]+)?|background(?:-[a-z]+)?)\s*:\s*(#333333|#333|#444444|#444|#4a4a4a|#555555|#555|#111111|#111)\b/gi;
  // Wait! We only want to replace TEXT colors with --text-secondary, not borders or backgrounds!
  // The user said: "Fix low-contrast subtext globally... Audit style.css for the muted/secondary text colors"
  const textRegex = /(color|fill)\s*:\s*(#333333|#333|#444444|#444|#4a4a4a|#555555|#555)\b/gi;

  content = content.replace(textRegex, (match, prop, hex) => {
    replacedInFile++;
    totalReplaced++;
    // Use --text-muted for the darkest ones (#333), --text-secondary for others?
    // User said: "target roughly #8a8a8a–#9a9a9a for secondary text and no darker than #707070 for tertiary/placeholder text"
    // Usually placeholder text was #333. Let's make #333 -> var(--text-muted) and #444/#555 -> var(--text-secondary).
    const isMuted = hex === '#333' || hex === '#333333';
    return `${prop}: var(${isMuted ? '--text-muted' : '--text-secondary'})`;
  });

  if (replacedInFile > 0) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Replaced ${replacedInFile} instances in ${file}`);
  }
}

console.log(`Total scattered text color instances replaced: ${totalReplaced}`);
