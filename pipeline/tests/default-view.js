/* The default view — annual panel only — must show all 26 markers individually
 * at every window size. Nothing rolled up, nothing dropped: this is the first
 * thing anyone sees. */
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
  const d = dom.window.document;
  const markers = d.querySelectorAll('.map .row.mkr').length;
  const concerns = d.querySelectorAll('.map .row.cnc').length;
  const rolled = d.querySelectorAll('.map .fold').length;
  console.log(W + 'x' + H, 'markers', markers, '| concerns', concerns, '| rolled up', rolled);
  if (markers !== 26) fail.push(W + 'x' + H + ': ' + markers + ' markers drawn, expected all 26');
  if (concerns !== 47) fail.push(W + 'x' + H + ': ' + concerns + ' concerns drawn, expected all 47');
  if (rolled)          fail.push(W + 'x' + H + ': ' + rolled + ' rows rolled up in the default view');
  go();
 }, 700);
})();
