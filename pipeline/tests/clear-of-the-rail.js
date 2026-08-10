const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1280,720],[1440,900],[1600,900],[1920,1080],[1100,800]];
let idx=0,fail=[];
function next(){
 if(idx>=sizes.length){console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1;return;}
 const [W,H]=sizes[idx++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
   // The geometry checks want the full map: skip the first frame.
   try{ w.localStorage.setItem('v3.state', JSON.stringify({reveal:1, guide:{off:1}})); }catch(e){}
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});
 }});
 setTimeout(()=>{
  const w=dom.window,d=w.document;
  const L=320+16;
  // select all panels to stress the left column
  d.getElementById('pAll').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  let minLeft=1e9,worst='';
  [...d.querySelectorAll('.map .row.mkr text.lb, .map .fold text, .map text.grphd')].forEach(t=>{
   const x=+t.getAttribute('x'); if(isNaN(x))return;
   const fsz=parseFloat((t.getAttribute('style')||'').replace(/\D*([\d.]+)px.*/,'$1'))||8.5;
   const left=x-t.textContent.length*fsz*0.6;
   if(left<minLeft){minLeft=left;worst=t.textContent;}
  });
  const ys=[...d.querySelectorAll('.map .row.mkr text.lb, .map .fold text.lb')].map(t=>+t.getAttribute('y')).sort((a,b)=>a-b);
  let gap=1e9; for(let i=1;i<ys.length;i++) gap=Math.min(gap,ys[i]-ys[i-1]);
  console.log(W+'x'+H,'| rail edge+16 =',L,'| leftmost label at',minLeft.toFixed(0),
              (minLeft<L?'UNDER RAIL':'clear'),'| rows',ys.length,'min gap',gap.toFixed(1),'|',worst.slice(0,28));
  if(minLeft<L) fail.push(W+'x'+H+': "'+worst+'" runs under the rail by '+(L-minLeft).toFixed(0)+'px');
  if(gap<7) fail.push(W+'x'+H+': marker rows overlap, gap '+gap.toFixed(1));
  next();
 },700);
}
next();
