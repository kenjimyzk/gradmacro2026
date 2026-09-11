// Check the regenerated HTML's math with an existing local KaTeX installation.
const fs = require('node:fs');
const path = require('node:path');
const katex = require(process.argv[2] || 'katex');
const math = JSON.parse(fs.readFileSync(path.join(__dirname, 'html-math.json'), 'utf8'));
const results = {}; let total = 0; const errors = [];
for (const [name, formulas] of Object.entries(math)) {
  let count = 0;
  for (const formula of formulas) {
    const raw = formula.tex;
    const display = formula.display;
    const tex = raw.replace(/^\\[([]/, '').replace(/\\[)\]]$/, '');
    try { katex.renderToString(tex, {displayMode: display, throwOnError: true, strict: false}); count++; }
    catch (error) { errors.push({name, tex, message: error.message}); }
  }
  results[name] = {formulas: formulas.length, parsed: count}; total += formulas.length;
}
const result = {katexVersion: katex.version, total, results, errors,
  scope: 'Syntax/renderToString check with local KaTeX; not browser layout or CDN availability'};
fs.writeFileSync(path.join(__dirname, 'katex-checks.json'), JSON.stringify(result, null, 2)+'\n');
console.log(JSON.stringify({katexVersion:katex.version, total, errors}, null, 2));
if (errors.length) process.exitCode = 1;
