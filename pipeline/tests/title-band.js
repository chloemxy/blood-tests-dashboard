/* The column-title band must be opaque and above the canvas, or rows scroll
 * straight under its text — which is what happened when it was painted with a
 * custom property this palette does not define.
 *
 * Also asserts the legend is gone: it was reference material restating what the
 * toggle and the dot colours already say in place, and the atlas reclaimed its
 * 72px. */
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
 const css = [...d.querySelectorAll('style')].map(x => x.textContent).join('');
 const band = css.match(/\.colbar\{[^}]*\}/)[0];
 console.log('band:', band.replace(/\s+/g, ' '));
 if(/var\(--bg\)/.test(band)) fail.push('band painted with an undefined variable');
 if(!/background:var\(--paper\)/.test(band)) fail.push('band has no opaque background');
 const zBand = +band.match(/z-index:(\d+)/)[1];
 const zCanvas = +css.match(/\.canvas\{[^}]*\}/)[0].match(/z-index:(\d+)/)[1];
 console.log('z-index: band', zBand, '> canvas', zCanvas);
 if(zBand <= zCanvas) fail.push('band is not above the canvas');

 const titles = d.querySelectorAll('#colBar span').length;
 console.log('titles in the band:', titles);
 if(titles !== 3) fail.push(titles + ' titles in the band, expected 3');

 console.log('legend button:', !!d.getElementById('btnFoot'), '| legend panel:', !!d.querySelector('.pnl.foot'),
             '| footer height var:', /--footH/.test(css));
 if(d.getElementById('btnFoot')) fail.push('the Legend button is still there');
 if(d.querySelector('.pnl.foot')) fail.push('the legend panel is still there');
 if(/--footH/.test(css)) fail.push('--footH is still reserved for a panel that no longer exists');

 const stat = (d.getElementById('hdrStat') || {}).textContent || '';
 console.log('header counts line:', JSON.stringify(stat.slice(0, 70)));
 if(!stat.trim()) fail.push('the counts sentence did not move to the header');

 console.log(fail.length ? '\nFAIL:\n - ' + fail.join('\n - ') : '\nALL PASS');
 if(fail.length) process.exitCode = 1;
}, 700);
