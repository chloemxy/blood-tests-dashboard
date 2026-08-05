const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1280,720],[1600,900],[1920,1080]];let i=0,fail=[];
(function go(){ if(i>=sizes.length){console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1;return;}
 const [W,H]=sizes[i++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});}});
 setTimeout(()=>{const w=dom.window,d=w.document;
  const mk=()=>d.querySelectorAll('.map .row.mkr').length;
  const cn=()=>d.querySelectorAll('.map .row.cnc').length;
  const svgH=()=>+d.getElementById('map').getAttribute('height');
  console.log(W+'x'+H,'default: markers',mk(),'concerns',cn(),'canvas height',svgH());
  if(mk()!==26) fail.push(W+'x'+H+' default draws '+mk()+' markers, expected 26');
  if(cn()!==47) fail.push(W+'x'+H+' default draws '+cn()+' concerns, expected 47');
  d.getElementById('pAll').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  console.log('   all 13:   markers',mk(),'concerns',cn(),'canvas height',svgH(),'(window',H-56,')');
  if(mk()!==68) fail.push(W+'x'+H+' all-panels draws '+mk()+' markers, expected 68');
  if(svgH() < 68*16) fail.push(W+'x'+H+' canvas did not grow for 68 rows');
  if(d.querySelectorAll('.map .fold').length) fail.push('a folded row is still being drawn');
  // rows must not overlap now that nothing folds
  const ys=[...d.querySelectorAll('.map .row.mkr text.lb')].map(t=>+t.getAttribute('y')).sort((a,b)=>a-b);
  let g=1e9; for(let k=1;k<ys.length;k++) g=Math.min(g,ys[k]-ys[k-1]);
  console.log('   tightest marker line gap',g.toFixed(1));
  if(g<12) fail.push(W+'x'+H+' marker lines overlap at '+g.toFixed(1)+'px');
  go();},700);
})();
