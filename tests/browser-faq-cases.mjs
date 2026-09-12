import {pathToFileURL} from 'node:url';
import path from 'node:path';
export async function runFaq({send,evaluate,root}) {
 const results=[];
 const url=pathToFileURL(path.join(root,'dist/government/faq.html')).href;
 for(const direction of ['rtl','ltr']) for(const width of [320,430,768,1440]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url});
  await evaluate(`document.documentElement.dir=${JSON.stringify(direction)}`);
  results.push({name:`layout ${direction} ${width}`,pass:await evaluate(`document.documentElement.scrollWidth<=innerWidth && document.querySelectorAll('h1').length===1 && document.querySelectorAll('[data-faq] .accordion').length===5`)});
  results.push({name:`toggle ${direction} ${width}`,pass:await evaluate(`(()=>{const b=document.querySelector('.accordion__trigger'),p=document.getElementById(b.getAttribute('aria-controls'));const initial=p.hidden;b.click();const opened=!p.hidden&&b.getAttribute('aria-expanded')==='true';b.click();return initial&&opened&&p.hidden;})()`)});
 }
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await send('Page.navigate',{url});
 results.push({name:'Answers available without JavaScript',pass:await evaluate(`Array.from(document.querySelectorAll('.accordion__panel')).every(p=>getComputedStyle(p).display!=='none')`)});
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
