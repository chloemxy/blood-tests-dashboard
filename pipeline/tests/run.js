#!/usr/bin/env node
/* Regression gate for index.html — the ripple atlas.
 *
 *   node pipeline/tests/run.js
 *
 * Each check renders the built page in jsdom at several window sizes and
 * measures the result. They exist because every one of them is a mistake that
 * shipped once: labels sliding under a panel, highlights overlapping, a column
 * measured at one type size and drawn at another. Run this before promoting a
 * build; a non-zero exit means do not ship.
 *
 * Requires jsdom:  npm install jsdom
 */
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path');

const dir = __dirname;
const files = fs.readdirSync(dir)
  .filter(f => f.endsWith('.js') && f !== 'run.js')
  .sort();

try { require('jsdom'); }
catch (e) {
  console.error('jsdom is not installed. Run:  npm install jsdom');
  process.exit(2);
}

const build = path.join(dir, '..', '..', 'index.html');
if (!fs.existsSync(build)) {
  console.error('index.html not found — run pipeline/build_v3.py first.');
  process.exit(2);
}
console.log('checking ' + path.relative(process.cwd(), build)
  + '  (' + (fs.statSync(build).size / 1024).toFixed(0) + ' KB)\n');

let failed = [];
files.forEach(f => {
  const name = f.replace(/\.js$/, '');
  process.stdout.write('  ' + name.padEnd(28));
  try {
    const out = execFileSync(process.execPath, [path.join(dir, f)], { encoding: 'utf8' });
    if (/ALL PASS/.test(out)) console.log('pass');
    else { console.log('FAIL'); failed.push([name, out]); }
  } catch (e) {
    console.log('FAIL');
    failed.push([name, (e.stdout || '') + (e.stderr || '')]);
  }
});

if (failed.length) {
  console.log('\n' + failed.length + ' of ' + files.length + ' checks failed:\n');
  failed.forEach(([name, out]) => {
    console.log('--- ' + name + ' ---');
    console.log(out.trim());
    console.log('');
  });
  process.exit(1);
}
console.log('\n' + files.length + ' checks passed. Safe to promote.');
