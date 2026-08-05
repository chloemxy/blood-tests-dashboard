const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1280,720],[1440,900],[1600,900],[1920,1080],[1100,800],[1024,768]];
let idx=0,fail=[];
function next(){
 if(idx>=sizes.length){ console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1; return; }
 const [W,H]=sizes[idx++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});
 }});
 setTimeout(()=>{
  const w=dom.window,d=w.document;
  const hasDet=W>1080, R=W-(hasDet?344+16:16);
  let worst=0, worstT='', checked=0;
  const cns=[...d.querySelectorAll('[data-cn]')];
  cns.slice(0,12).forEach(c=>{
   c.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
   [...d.querySelectorAll('.map .row.tst text.lb, .map g.tst text')].forEach(t=>{
    const x=+t.getAttribute('x'); if(isNaN(x))return;
    const fsz=parseFloat((t.getAttribute('style')||'').replace(/\D*([\d.]+)px.*/,'$1'))||12;
    const right=x+t.textContent.length*fsz*0.6; checked++;
    if(right>worst){worst=right;worstT=t.textContent;}
   });
  });
  const over=worst-R;
  console.log(W+'x'+H,'| det panel at',R+16,'| map right edge',R,'| widest label ends',worst.toFixed(0),
              '('+(over>0?'OVER by '+over.toFixed(0):'clear by '+(-over).toFixed(0))+')','|',checked,'labels');
  if(over>0) fail.push(W+'x'+H+': label past the panel gutter by '+over.toFixed(0)+'px — "'+worstT+'"');
  next();
 },700);
}
next();
