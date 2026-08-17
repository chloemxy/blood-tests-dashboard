/* The tutorial overlay.
 *
 * It must: show on a first visit with an empty middle column, state one task at
 * reading size, ring the section that task is about, dim the rest without ever
 * swallowing a click, tick off the real action, and retire for good — while
 * changing no layout at all, which is the point of it being an overlay.
 *
 * jsdom does no layout, so the two elements the placement measures are given
 * real boxes below and the ring is checked against LAYOUT to the pixel. */
const fs = require('fs'), path = require('path'), { JSDOM } = require('jsdom');
const html = fs.readFileSync(path.join(__dirname, '..', '..', 'index.html'), 'utf8');
const CANVAS = { left:336, top:96, width:904, height:844, right:1240, bottom:940 };
const RAIL   = { left:0, top:200, width:320, height:520, right:320, bottom:720 };

const dom = new JSDOM(html, { url: 'http://localhost/', runScripts: 'dangerously', pretendToBeVisual: true,
 beforeParse(w){
  w.matchMedia = q => ({ matches: false, addEventListener(){}, addListener(){} });
  Object.defineProperty(w.HTMLElement.prototype, 'clientWidth',  { get(){ return 1600; } });
  Object.defineProperty(w.HTMLElement.prototype, 'clientHeight', { get(){ return 900; } });
  Object.defineProperty(w, 'innerWidth',  { get(){ return 1600; } });
  Object.defineProperty(w, 'innerHeight', { get(){ return 956; } });
  w.HTMLElement.prototype.getBoundingClientRect = function(){
   if (this.id === 'canvas') return CANVAS;
   if (this.id === 'rail')   return RAIL;
   return { left:0, top:0, width:0, height:0, right:0, bottom:0 };
  };
 }});

setTimeout(() => {
 const w = dom.window, d = w.document, fail = [];
 const click = el => el.dispatchEvent(new w.MouseEvent('click', { bubbles: true, cancelable: true }));
 const css = [...d.querySelectorAll('style')].map(x => x.textContent).join('');
 const num = v => parseFloat(v || '0');
 const ring = () => { const r = d.getElementById('tutRing');
   return { left:num(r.style.left), top:num(r.style.top), w:num(r.style.width), h:num(r.style.height) }; };
 const steps = () => [...d.querySelectorAll('#gSteps li')].map(li => li.className).join(',');
 const task = () => (d.getElementById('gI') || {}).textContent || '';
 const kick = () => (d.getElementById('gK') || {}).textContent || '';

 // ---- it is an overlay: fixed, above everything, and reserves no layout
 console.log('card position:', /\.guide\{[^}]*position:fixed/.test(css) ? 'fixed' : 'NOT fixed');
 if (!/\.guide\{[^}]*position:fixed/.test(css)) fail.push('the card is not an overlay');
 if (/body\.guiding \.canvas\{padding/.test(css)) fail.push('the overlay still reserves canvas height');
 // the dimming is the ring's own shadow, so it follows the rounded corners
 if (d.querySelector('.tutscrim')) fail.push('the four-rectangle scrim is still there');
 if (!/\.tutring\{[^}]*box-shadow:0 0 0 9999px/.test(css)) fail.push('the scrim does not follow the ring');
 if (!/\.tutring\{[^}]*border-radius:8px/.test(css)) fail.push('the ring lost its radius');
 if (/\.tutring\{[^}]*border:/.test(css)) fail.push('the highlight still has an outline');
 if (!/\.tutring\{[^}]*pointer-events:none/.test(css)) fail.push('the ring would swallow clicks');

 // ---- first visit
 console.log('showing:', d.body.classList.contains('guiding'), '| highlighting:', d.body.classList.contains('gtut'));
 if (!d.body.classList.contains('guiding')) fail.push('the guide is not shown on a first visit');
 if (!d.body.classList.contains('gtut')) fail.push('nothing is highlighted');
 console.log('concerns at boot:', d.querySelectorAll('.map .row.cnc').length,
             '| prompt:', /Mark a result on the left/.test(d.getElementById('map').textContent));
 if (d.querySelectorAll('.map .row.cnc').length) fail.push('the middle column is not empty on a first visit');

 console.log('step 1:', task());
 if (task().length < 30) fail.push('the task is not spelled out');
 if (!/\.gi\{[^}]*font-size:16px/.test(css)) fail.push('the task is not at reading size');
 console.log('step number:', kick(), '| skip button:', !!d.getElementById('gSkip'),
             'on the header line:', !!d.querySelector('.ghd #gSkip'));
 if (!/^Step 1 of 3$/.test(kick())) fail.push('the step number is not stated');
 if (!d.querySelector('.ghd #gSkip')) fail.push('no Skip button on the card header');

 // step 1 rings the rail, and the card sits beside it
 const r1 = ring();
 console.log('ring on the rail:', JSON.stringify(r1), '| card:', d.getElementById('guide').className);
 // flush: exactly the rail's box, no halo
 if (r1.left !== RAIL.left || r1.top !== RAIL.top
     || Math.abs(r1.w - RAIL.width) > 1 || Math.abs(r1.h - RAIL.height) > 1)
  fail.push('the ring is not flush with the rail');
 if (!/\bleft\b/.test(d.getElementById('guide').className)) fail.push('the card does not point at the rail');

 console.log('scrim: the ring\'s own shadow, so the hole is rounded like the ring');

 // ---- step 2: the concern column, from the real layout
 click(d.querySelector('#gEx [data-ex="iron"]'));
 const L = w.eval('LAYOUT');
 const r2 = ring(), want2 = { left: CANVAS.left + L.xC - 9, w: (L.xCend + 9) - (L.xC - 9) };
 console.log('step 2:', task());
 console.log('ring on the concern column:', JSON.stringify(r2), 'expected', JSON.stringify(want2));
 if (r2.top !== CANVAS.top || Math.abs(r2.h - CANVAS.height) > 1)
  fail.push('the ring is not flush with the canvas vertically');
 if (Math.abs(r2.left - want2.left) > 1 || Math.abs(r2.w - want2.w) > 1)
  fail.push('the ring is not around the concern column');
 if (steps().split(',')[0] !== 'done') fail.push('step 1 did not tick after marking');
 const cShown = d.querySelectorAll('.map .row.cnc').length, D = w.eval('D');
 console.log('concerns revealed:', cShown, 'of', D.meta.nConcerns);
 if (!cShown || cShown >= D.meta.nConcerns) fail.push('marking did not reveal exactly what it raised');

 // ---- step 3: the follow-up column
 click(d.querySelector('.map [data-cn]'));
 const B = w.eval('BOX');
 const r3 = ring(), want3 = { left: CANVAS.left + L.xT - 8, w: B.R - (L.xT - 8) };
 console.log('step 3:', task());
 console.log('ring on the follow-up column:', JSON.stringify(r3), 'expected', JSON.stringify(want3));
 if (Math.abs(r3.left - want3.left) > 1 || Math.abs(r3.w - want3.w) > 1)
  fail.push('the ring is not around the follow-up column');

 // ---- and it goes
 const t = d.querySelector('.map [data-test]');
 if (!t) fail.push('no follow-up row to open');
 else {
  click(t);
  console.log('after all three: guiding', d.body.classList.contains('guiding'),
              '| highlighting', d.body.classList.contains('gtut'),
              '| concerns', d.querySelectorAll('.map .row.cnc').length, '/', D.meta.nConcerns);
  if (d.body.classList.contains('guiding')) fail.push('the guide did not retire');
  if (d.body.classList.contains('gtut')) fail.push('the highlight outlived the guide');
  if (d.querySelectorAll('.map .row.cnc').length !== D.meta.nConcerns)
   fail.push('finishing did not restore the whole map');
  // a refresh starts the guide again: nothing about it is written to storage
  const saved = JSON.parse(w.localStorage.getItem('v3.state') || '{}');
  console.log('saved keys:', Object.keys(saved).join(','));
  if ('guide' in saved || 'reveal' in saved)
   fail.push('the guide was persisted, so a refresh would not start at step 1');
 }

 console.log(fail.length ? '\nFAIL:\n - ' + fail.join('\n - ') : '\nALL PASS');
 if (fail.length) process.exitCode = 1;
}, 800);
