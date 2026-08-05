const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
function run(W,H,cb){
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});
 }});
 setTimeout(()=>cb(dom.window,dom.window.document),700);
}
run(1600,900,(w,d)=>{
 const fail=[];
 const reset=d.getElementById('pReset'), all=d.getElementById('pAll');
 console.log('default: reset disabled?',reset.disabled,'| all label:',all.textContent,'disabled?',all.disabled);
 if(!reset.disabled) fail.push('reset should be dim at default');
 all.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 const on=[...d.querySelectorAll('#pChips .pchip.on')].length, tot=[...d.querySelectorAll('#pChips .pchip')].length;
 console.log('after select all: chips on',on,'/',tot,'| rail rows',d.querySelectorAll('#rail .mrow').length,
             '| map marker labels',d.querySelectorAll('.map .row.mkr').length);
 if(on!==tot) fail.push('select all did not select all');
 if(!d.getElementById('pAll').disabled) fail.push('all should dim when everything is on');
 if(d.getElementById('pReset').disabled) fail.push('reset should be live when all on');
 // overlap check on the map at full selection
 const ys=[...d.querySelectorAll('.map .row.mkr text')].map(t=>+t.getAttribute('y')).sort((a,b)=>a-b);
 let minGap=1e9; for(let i=1;i<ys.length;i++) minGap=Math.min(minGap, ys[i]-ys[i-1]);
 const fs2=w.getComputedStyle||null;
 console.log('map label rows',ys.length,'min y-gap',minGap.toFixed(2));
 if(minGap<7) fail.push('map labels too tight at 13 panels: '+minGap.toFixed(2));
 d.getElementById('pReset').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 const on2=[...d.querySelectorAll('#pChips .pchip.on')].map(c=>c.dataset.pgroup);
 console.log('after annual only:',on2.join(','),'| rail rows',d.querySelectorAll('#rail .mrow').length);
 if(on2.join(',')!=='ANNUAL') fail.push('reset did not go back to annual only');
 console.log(fail.length?'FAIL:\n - '+fail.join('\n - '):'ALL PASS'); if(fail.length) process.exitCode = 1;
});
