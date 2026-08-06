/* The default view must draw every marker in your annual panel and every
 * concern, at every window size. Nothing rolled up, nothing dropped: this is
 * the first thing anyone sees.
 *
 * The expected counts come from the build's own payload, not from constants —
 * the panel definition changes, the invariant does not. */
const fs = require('fs'), path = require('path'), { JSDOM } = require('jsdom');
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'index.html'), 'utf8');
const sizes = [[1280, 720], [1440, 900], [1600, 900], [1920, 1080]];
let i = 0, fail = [];

(function go(){
 if (i >= sizes.length) {
  console.log(fail.length ? '\nFAIL:\n - ' + fail.join('\n - ') : '\nALL PASS');
  if (fail.length) process.exitCode = 1;
  return;
 }
 const [W, H] = sizes[i++];
 const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', pretendToBeVisual: true,
  beforeParse(w){
   w.matchMedia = q => ({ matches: false, addEventListener(){}, addListener(){} });
   Object.defineProperty(w.HTMLElement.prototype, 'clientWidth',  { get(){ return W; } });
   Object.defineProperty(w.HTMLElement.prototype, 'clientHeight', { get(){ return H; } });
  }});
 setTimeout(() => {
  const w = dom.window, d = w.document, D = w.eval('D');
  const want = [];
  D.panels.filter(p => p.default).forEach(p => p.slugs.forEach(sl => {
   if (want.indexOf(sl) < 0) want.push(sl);
  }));
  const markers = d.querySelectorAll('.map .row.mkr').length;
  const concerns = d.querySelectorAll('.map .row.cnc').length;
  const rolled = d.querySelectorAll('.map .fold').length;
  console.log(W + 'x' + H, 'markers', markers, '/', want.length,
              '| concerns', concerns, '/', D.meta.nConcerns, '| rolled up', rolled);
  if (markers !== want.length)        fail.push(W+'x'+H+': '+markers+' markers drawn, expected '+want.length);
  if (concerns !== D.meta.nConcerns)  fail.push(W+'x'+H+': '+concerns+' concerns drawn, expected '+D.meta.nConcerns);
  if (rolled)                         fail.push(W+'x'+H+': '+rolled+' rows rolled up in the default view');
  go();
 }, 700);
})();
