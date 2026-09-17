/* The atlas is the front door now: there is no nav left to speak of — the
 * logo is the way back to the map, and "Database" moved out to the secondary
 * actions since it is reference material, not a primary tab. catalogue.html
 * is no longer linked from there — it keeps its own older header shape,
 * reachable only by a direct URL — so the two documents are checked against
 * separate expectations rather than asserted to be identical.
 *
 * This still guards the risky half of the catalogue header — it was built
 * around JS that binds a dozen ids, so every one of them is asserted to still
 * exist, and the in-place route switch is exercised for real.
 */
const fs=require('fs'),path=require('path'),{JSDOM,VirtualConsole}=require('jsdom');
const R = path.join(__dirname, '..', '..') + path.sep;
let fail=[];
/* jsdom does no real layout, so "the pills sit in the same place" is checked
   structurally instead: every header must be the same three-column grid with
   the same three children in the same order — identity, nav, actions — and the
   nav must hold the same three labels. Same structure, same CSS, same x. */
function shape(bar){
 const kids = [...bar.children].map(el => el.tagName === 'NAV' ? 'nav' : (el.className || el.tagName));
 const labels = [...bar.querySelectorAll('.nv')].map(a => a.textContent).join('>');
 return kids.join('|') + ' :: ' + labels;
}
// The atlas nav is empty now — the logo (data-view2="map") is the only way
// back to the map, so "current screen" is read off [data-view2].on instead.
const ATLAS_SHAPE = 'id|nav|act :: ';
const CATALOGUE_SHAPE = 'id|nav|act :: Atlas>How you feel>Guided tests>All tests';

function load(file, cb){
 const errs=[];
 const vc=new VirtualConsole();
 vc.on('jsdomError',e=>{const m=String(e.message); if(!/Not implemented/.test(m)) errs.push(m.slice(0,140));});
 const dom=new JSDOM(fs.readFileSync(R+file,'utf8'),{url:'http://localhost/'+file,runScripts:'dangerously',
  pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
   w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
   Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return 1600}});
   Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return 900}});
  }});
 setTimeout(()=>cb(dom.window,dom.window.document,errs),900);
}
load('index.html',(w,d,errs)=>{
 console.log('== index.html (atlas)');
 console.log('   js errors:', errs.length?errs.join(' | '):'none');
 if(errs.length) fail.push('atlas: js error');
 const hd=d.querySelector('.sitehd');
 const nv=[...d.querySelectorAll('.sitehd .nv')].map(a=>a.textContent+(a.classList.contains('on')?'*':''));
 console.log('   header .sitehd:', !!hd, '| nav:', nv.join(' , '));
 console.log('   actions:', [...d.querySelectorAll('.sitehd .act button')].map(b=>b.textContent).join(' , '));
 const sh=shape(hd);
 console.log('   shape:', sh);
 if(sh!==ATLAS_SHAPE) fail.push('atlas: header shape is "'+sh+'", expected "'+ATLAS_SHAPE+'"');
 if(nv.length!==0) fail.push('atlas: '+nv.length+' nav items, expected the nav to be empty');
 // current screen is marked on whichever [data-view2] element matches the
 // live view — the logo doubles as the map tab, Database as the table one
 const cur=[...d.querySelectorAll('.sitehd [data-view2]')].filter(el=>el.classList.contains('on'));
 console.log('   current screen marked on:', cur.map(el=>el.dataset.view2).join(','));
 if(cur.length!==1 || cur[0].dataset.view2!=='map') fail.push('atlas: current screen (map) not marked via [data-view2].on');
 load('catalogue.html',(w2,d2,errs2)=>{
  console.log('\n== catalogue.html');
  console.log('   js errors:', errs2.length?errs2.join(' | '):'none');
  if(errs2.length) fail.push('catalogue: js error');
  const bars=[...d2.querySelectorAll('.sitehd')];
  console.log('   headers with .sitehd:', bars.length);
  if(bars.length!==3) fail.push('catalogue: '+bars.length+' unified headers, expected 3');
  bars.forEach((b,i)=>{
   const nv2=[...b.querySelectorAll('.nv')].map(a=>a.textContent+(a.classList.contains('on')?'*':''));
   const tag=(b.querySelector('.tag')||{}).textContent||'(dynamic)';
   console.log('     bar '+(i+1)+' tag "'+tag+'" nav: '+nv2.join(' , '));
   if(nv2.length!==4) fail.push('catalogue bar '+(i+1)+': '+nv2.length+' nav items');
   const sh2=shape(b);
   if(sh2!==CATALOGUE_SHAPE) fail.push('catalogue bar '+(i+1)+' shape is "'+sh2+'", expected "'+CATALOGUE_SHAPE+'"');
   console.log('       shape: '+sh2);
  });
  // ids the existing JS binds to must survive
  // the screen-title tags are gone: the lit nav pill already says where you are
  const tags = d2.querySelectorAll('.sitehd .tag').length + d.querySelectorAll('.sitehd .tag').length;
  console.log('   repeated screen titles left:', tags);
  if(tags) fail.push(tags + ' .tag screen titles left in the headers');
  ['viewTog','rollup','rollgrid','sysbar','hdrTag','resetBtn','app','cxRoute','cxApp']
   .forEach(id=>{ if(!d2.getElementById(id)) fail.push('catalogue: #'+id+' was removed'); });
  console.log('   all bound ids present:', !fail.some(f=>f.includes('was removed')));
  // feedback on every screen, and the "i" gone from all of them. atlas moved
  // its feedback link out of the header entirely, into the corner hint that
  // used to open keyboard shortcuts (shortcuts are still reachable via "?"),
  // so it is checked page-wide there rather than scoped to .sitehd .act.
  const fb = [...d2.querySelectorAll('.sitehd .act a[href^="mailto:"]')].length;
  const fbAtlas = d.querySelectorAll('a[href^="mailto:"]').length;
  console.log('   feedback pills: atlas', fbAtlas, '+ catalogue', fb, '| "i" buttons:', d2.querySelectorAll('.discbtn').length);
  // one in the corner hint, one in the About modal's own copy
  if(fbAtlas !== 2) fail.push('atlas: '+fbAtlas+' feedback links, expected 2');
  if(fb !== 3) fail.push('catalogue: '+fb+' feedback pills, expected one per screen');
  console.log('   shortcuts corner hint replaced by feedback:', !d.getElementById('kbdHint'), '| feedback hint present:', !!d.getElementById('feedbackHint'));
  if(d.getElementById('kbdHint')) fail.push('atlas: the old shortcuts corner button is still there');
  if(!d.getElementById('feedbackHint')) fail.push('atlas: no feedback link in the corner hint');
  // Upload lives in the centred nav now. Clear moved out of the header
  // entirely, down into the map's own column-3 toolbar next to Edit — so
  // .act is just About and Database as plain text links, then the (iconic,
  // textless) theme toggle. The (unlinked) catalogue screens keep their
  // original two, in the same order, on every screen. Button text includes
  // both the full and short label spans (jsdom does not evaluate the CSS
  // that picks between them).
  const acts = b => [...b.querySelectorAll('.act > *')].map(x => x.textContent.trim()).join(' > ');
  const ATLAS_WANT = 'About > Database > ';
  const WANT = 'Clear all answers > feedback';
  const aAtlas = acts(d.querySelector('.sitehd'));
  console.log('   atlas actions:', JSON.stringify(aAtlas));
  if(aAtlas !== ATLAS_WANT) fail.push('atlas actions are "'+aAtlas+'", expected "'+ATLAS_WANT+'"');
  bars.forEach((b,i)=>{
   const got = acts(b);
   console.log('   bar '+(i+1)+' actions:', JSON.stringify(got));
   if(got !== WANT) fail.push('catalogue bar '+(i+1)+' actions are "'+got+'", expected "'+WANT+'"');
  });
  // clearing is defined once: the other pills must reach the real one
  const feelClear = bars[1].querySelector('.clearall');
  d2.getElementById('qbox').value = 'tired';
  feelClear.dispatchEvent(new w2.MouseEvent('click',{bubbles:true,cancelable:true}));
  console.log('   clear from another screen emptied the query:', d2.getElementById('qbox').value === '');
  if(d2.getElementById('qbox').value !== '') fail.push('a delegated Clear all answers did nothing');
  if(d2.querySelector('.discbtn')) fail.push('catalogue: the "i" button is still there');
  // its modal must still be reachable, from the counts line
  const h = d2.getElementById('hdrTag');
  console.log('   provenance opens from the counts line:', typeof h.onclick === 'function');
  if(typeof h.onclick !== 'function') fail.push('the provenance modal is unreachable');
  console.log('   menu buttons left:', ['cxToMenu','cxMenuBtn'].filter(i=>d2.getElementById(i)).join(',') || 'none');
  ['cxToMenu','cxMenuBtn'].forEach(i=>{ if(d2.getElementById(i)) fail.push('catalogue: #'+i+' is still there'); });
  console.log('   __cxSetMode exposed:', typeof w2.__cxSetMode);
  // in-place route switch
  d2.querySelector('.sitehd [data-go="tests"]').dispatchEvent(new w2.MouseEvent('click',{bubbles:true,cancelable:true}));
  const guided = d2.querySelector('#viewTog button[data-view="guided"]').classList.contains('on');
  console.log('   Guided tests -> #app', d2.getElementById('app').style.display, '| guided view on:', guided,
              '| hash', w2.location.hash);
  if(d2.getElementById('app').style.display!=='grid') fail.push('catalogue: nav did not open the dashboard');
  if(!guided) fail.push('catalogue: Guided tests tab did not select the guided view');
  d2.querySelector('.sitehd [data-go="table"]').dispatchEvent(new w2.MouseEvent('click',{bubbles:true,cancelable:true}));
  const tbl = d2.querySelector('#viewTog button[data-view="table"]').classList.contains('on');
  const tblShown = d2.getElementById('tableSection').style.display !== 'none';
  console.log('   All tests   -> table view on:', tbl, '| table section shown:', tblShown, '| hash', w2.location.hash);
  if(!tbl) fail.push('catalogue: All tests tab did not select the table view');
  if(!tblShown) fail.push('catalogue: All tests tab did not reveal the table');
  console.log('\n'+(fail.length?'FAIL:\n - '+fail.join('\n - '):'ALL PASS'));
  if(fail.length) process.exitCode=1;
 });
});
