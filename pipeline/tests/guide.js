/* The three-step guide strip: it must state where to start, tick off what you
 * actually did, disappear for good when finished, and never leave a marker row
 * hidden underneath itself. Also checks the examples mark real markers. */
const fs = require('fs'), path = require('path'), { JSDOM } = require('jsdom');
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'index.html'), 'utf8');
const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', pretendToBeVisual: true,
 beforeParse(w){
  w.matchMedia = q => ({ matches: false, addEventListener(){}, addListener(){} });
  Object.defineProperty(w.HTMLElement.prototype, 'clientWidth',  { get(){ return 1600; } });
  Object.defineProperty(w.HTMLElement.prototype, 'clientHeight', { get(){ return 900; } });
 }});
setTimeout(() => {
 const w = dom.window, d = w.document, fail = [];
 const click = el => el.dispatchEvent(new w.MouseEvent('click', { bubbles: true, cancelable: true }));
 const state = () => [...d.querySelectorAll('#gSteps li')].map(li => li.className).join(',');

 console.log('showing at boot:', d.body.classList.contains('guiding'));
 if (!d.body.classList.contains('guiding')) fail.push('the guide is not shown on a first visit');
 console.log('steps:', d.querySelectorAll('#gSteps li').length, '|', state());
 if (d.querySelectorAll('#gSteps li').length !== 3) fail.push('expected three steps');
 if (!/now/.test(state())) fail.push('no step is marked as the one to do next');

 const ex = [...d.querySelectorAll('#gEx [data-ex]')];
 console.log('examples offered:', ex.map(b => b.textContent).join(', '));
 if (ex.length !== 3) fail.push(ex.length + ' examples, expected 3');

 // pattern 01: the middle column starts empty and says what it is waiting for
 console.log('concerns at boot:', d.querySelectorAll('.map .row.cnc').length,
             '| prompt:', /Mark a result on the left/.test(d.getElementById('map').textContent));
 if (d.querySelectorAll('.map .row.cnc').length) fail.push('the middle column is not empty on a first visit');
 if (!/Mark a result on the left/.test(d.getElementById('map').textContent))
  fail.push('the empty column does not say what it is waiting for');
 if (!d.querySelector('#gEx [data-reveal]')) fail.push('no way out of the first frame');

 // step 1 via an example
 click(ex[0]);
 const marked = d.querySelectorAll('.map .row.mkr.lo, .map .row.mkr.hi').length;
 console.log('after the low-iron example: marked rows', marked, '|', state());
 if (!marked) fail.push('the example marked nothing — the slugs may not exist');
 if (!/^done/.test(state())) fail.push('step 1 did not tick after marking');
 if (d.querySelectorAll('#gEx [data-ex]').length) fail.push('examples still offered after marking');
 const cShown = d.querySelectorAll('.map .row.cnc').length, D = w.eval('D');
 console.log('concerns after one example:', cShown, 'of', D.meta.nConcerns);
 if (!cShown) fail.push('marking revealed no concerns');
 if (cShown >= D.meta.nConcerns) fail.push('marking revealed the whole column, not just what it raised');

 // step 2
 click(d.querySelector('.map [data-cn]'));
 console.log('after opening a concern:', state());
 if (state().split(',')[1] !== 'done') fail.push('step 2 did not tick after opening a concern');

 // step 3 — and the strip must go
 const t = d.querySelector('.map [data-test]');
 if (!t) fail.push('no follow-up row to open');
 else {
  click(t);
  console.log('after opening a follow-up: guiding =', d.body.classList.contains('guiding'));
  if (d.body.classList.contains('guiding')) fail.push('the guide did not retire once all three were done');
  const saved = JSON.parse(w.localStorage.getItem('v3.state') || '{}');
  console.log('remembered as finished:', !!(saved.guide && saved.guide.off));
  if (!(saved.guide && saved.guide.off)) fail.push('finishing was not remembered, so it will come back');
 }

 // and Show all is a real way out
 const seen = d.querySelectorAll('.map .row.cnc').length;
 console.log('after all three steps, the whole column is back:', seen, '/', w.eval('D').meta.nConcerns);
 if (seen !== w.eval('D').meta.nConcerns) fail.push('finishing the steps did not restore the whole map');

 // nothing hides under it: the canvas reserves the strip's height while it shows
 const css = [...d.querySelectorAll('style')].map(x => x.textContent).join('');
 const pad = /body\.guiding \.canvas\{padding-bottom:48px\}/.test(css);
 const h = /\.guide\{[^}]*height:48px/.test(css);
 console.log('canvas reserves the strip height:', pad, '| strip is 48px:', h);
 if (!pad || !h) fail.push('the canvas does not reserve the strip height, so rows can hide under it');

 console.log(fail.length ? '\nFAIL:\n - ' + fail.join('\n - ') : '\nALL PASS');
 if (fail.length) process.exitCode = 1;
}, 800);
