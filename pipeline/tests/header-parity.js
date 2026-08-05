/* The four screens must wear the same header, and every one of them must be
 * able to reach the other two. This checks both documents at once: the atlas
 * and all three catalogue screens.
 *
 * It also guards the risky half of that change — the catalogue header was
 * rebuilt around JS that binds a dozen ids, so every one of them is asserted
 * to still exist, and the in-place route switch is exercised for real.
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
const SHAPE = 'id|nav|act :: Atlas>How you feel>Guided tests>All tests';

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
 if(sh!==SHAPE) fail.push('atlas: header shape is "'+sh+'", expected "'+SHAPE+'"');
 if(nv.length!==4) fail.push('atlas: '+nv.length+' nav items');
 if(!/Atlas\*/.test(nv.join())) fail.push('atlas: current screen not marked');
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
   if(sh2!==SHAPE) fail.push('catalogue bar '+(i+1)+' shape is "'+sh2+'", expected "'+SHAPE+'"');
   console.log('       shape: '+sh2);
  });
  // ids the existing JS binds to must survive
  // the screen-title tags are gone: the lit nav pill already says where you are
  const tags = d2.querySelectorAll('.sitehd .tag').length + d.querySelectorAll('.sitehd .tag').length;
  console.log('   repeated screen titles left:', tags);
  if(tags) fail.push(tags + ' .tag screen titles left in the headers');
  ['viewTog','rollup','rollgrid','sysbar','hdrTag','resetBtn','discBtn','cxMenuBtn','app','cxRoute','cxApp']
   .forEach(id=>{ if(!d2.getElementById(id)) fail.push('catalogue: #'+id+' was removed'); });
  console.log('   all bound ids present:', !fail.some(f=>f.includes('was removed')));
  console.log('   duplicate Menu button gone:', !d2.getElementById('cxToMenu'));
  if(d2.getElementById('cxToMenu')) fail.push('catalogue: duplicate Menu button still injected');
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
