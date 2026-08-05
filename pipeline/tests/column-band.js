const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1280,720],[1440,900],[1600,900],[1920,1080]];let i=0,fail=[];
(function go(){ if(i>=sizes.length){console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1;return;}
 const [W,H]=sizes[i++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});}});
 setTimeout(()=>{const w=dom.window,d=w.document;
  const cnc=d.querySelectorAll('.map .row.cnc').length;
  const bar=[...d.querySelectorAll('#colBar span')].map(x=>x.textContent);
  const inline=[...d.querySelectorAll('.map [style*="font-size"]')].length;
  console.log(W+'x'+H,'concerns drawn',cnc,'| titles in band',bar.length,'| inline font-size in svg',inline);
  if(cnc!==47) fail.push(W+'x'+H+': '+cnc+' concerns drawn, expected all 47');
  if(bar.length!==3) fail.push(W+'x'+H+': column band has '+bar.length+' titles');
  if(inline) fail.push(W+'x'+H+': '+inline+' inline font-size overrides left in the svg');
  if(d.querySelectorAll('.map .colttl').length) fail.push('titles still drawn inside the scrolling canvas');
  go();},700);
})();
