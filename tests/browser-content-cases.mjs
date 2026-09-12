import {pathToFileURL} from 'node:url';
import path from 'node:path';

export async function runContent({send,evaluate,wait,root}) {
 const results=[];
 const url=pathToFileURL(path.join(root,'dist/government/content.html')).href;
 for(const direction of ['rtl','ltr']) for(const width of [320,430,768,1440]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url});
  await evaluate(`document.documentElement.dir=${JSON.stringify(direction)}`);
  const layout=await evaluate(`(()=>{const toc=document.querySelector('.table-of-contents'),body=document.querySelector('.heavy-content__body'),links=[...toc.querySelectorAll('a')],targets=links.map(link=>document.getElementById(link.hash.slice(1)));const t=toc.getBoundingClientRect(),b=body.getBoundingClientRect();return {fits:document.documentElement.scrollWidth<=innerWidth,h1:document.querySelectorAll('h1').length===1,sections:document.querySelectorAll('[data-content-section]').length===9,links:links.length===9,targets:targets.every(Boolean),order:innerWidth<768?t.bottom<=b.top+1:(document.documentElement.dir==='rtl'?t.left>b.left:t.left<b.left),tocWidth:innerWidth!==1440||Math.abs(t.width-222)<1,position:getComputedStyle(toc).position};})()`);
  results.push({name:`content layout ${direction} ${width}`,pass:Object.values(layout).slice(0,7).every(Boolean)&&(width<768?layout.position==='static':layout.position==='sticky')});
  await evaluate(`document.querySelectorAll('.table-of-contents__link')[2].click()`);await wait(50);
  results.push({name:`content navigation ${direction} ${width}`,pass:await evaluate(`location.hash==='#section-3'&&document.querySelectorAll('.table-of-contents__link[aria-current="location"]').length===1&&document.querySelector('.table-of-contents__link[aria-current="location"]').hash==='#section-3'`)});
 }
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await send('Page.navigate',{url});
 const noScript=await evaluate(`(()=>{const links=[...document.querySelectorAll('.table-of-contents__link')];links[1].click();return links.length===9&&location.hash==='#section-2'&&document.getElementById('section-2')!==null;})()`);
 results.push({name:'Content anchors work without JavaScript',pass:noScript});
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
