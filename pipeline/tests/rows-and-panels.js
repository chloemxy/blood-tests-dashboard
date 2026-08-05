const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});

  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return 1600}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return 900}});
}});
const w=dom.window,d=w.document;
setTimeout(()=>{
 const fail=[];
 const chips=[...d.querySelectorAll('#pChips .pchip')];
 console.log('picker chips:',chips.length);
 chips.forEach(c=>console.log('  ',c.dataset.pgroup,'|',c.textContent,'|',c.classList.contains('on')?'ON':'off'));
 if(chips.filter(c=>c.dataset.pgroup==='ANNUAL').length!==1) fail.push('no single ANNUAL chip');
 if(!chips.find(c=>c.dataset.pgroup==='ANNUAL').classList.contains('on')) fail.push('ANNUAL not on by default');

 // turn on BMP
 const bmp=chips.find(c=>c.dataset.pgroup==='BMP');
 bmp.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 const heads=[...d.querySelectorAll('#rail .grouphd')];
 console.log('\nrail groups after BMP on:');
 heads.forEach(h=>{
   let n=0,e=h.nextElementSibling;
   while(e&&!e.classList.contains('grouphd')){ if(e.classList.contains('mrow'))n++; e=e.nextElementSibling; }
   console.log('  ',h.textContent.trim(),'-> rows',n);
   if(n===0&&!h.querySelector('.dup')) fail.push('empty group with no note: '+h.textContent.trim());
 });
 const dupTexts=[...d.querySelectorAll('#rail .grouphd .dup')].map(x=>x.textContent);
 console.log('dup notes:',JSON.stringify(dupTexts));
 const svgdup=[...d.querySelectorAll('.map .grpdup')].map(x=>x.textContent);
 console.log('map dup notes:',JSON.stringify(svgdup));
 if(!svgdup.length) fail.push('map shows no dup note for BMP');

 // edges: no width difference between states
 const css=[...d.querySelectorAll('style')].map(s=>s.textContent).join('\n');
 const widths=[...css.matchAll(/\.map \.edge[^{]*\{[^}]*stroke-width:([\d.]+)/g)].map(m=>m[1]);
 console.log('\nedge stroke-widths:',widths.join(', '));
 if(new Set(widths.filter(x=>x!=='1')).size>1) fail.push('edge widths differ: '+widths);

 // follow-up rows: whole li is the target, no underline
 const c1=d.querySelector('[data-cn]');console.log('concern node:',!!c1);
 if(c1) c1.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 const lis=[...d.querySelectorAll('#next li[data-test]')];
 console.log('follow-up li with data-test:',lis.length);
 if(!lis.length) fail.push('no clickable follow-up rows');
 if(/text-decoration:underline/.test(css.match(/\.tlink\{[^}]*\}/)[0])) fail.push('tlink still underlined');
 const selCss=css.match(/\.mrow\.sel\{[^}]*\}/)[0];
 console.log('.mrow.sel ->',selCss);
 if(/border-color:var\(--accent\)/.test(selCss)) fail.push('mrow.sel still has visible border');

 console.log('\n'+(fail.length?'FAIL:\n - '+fail.join('\n - '):'ALL PASS')); if(fail.length) process.exitCode = 1;
},900);
