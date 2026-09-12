// Browser verification through Chrome DevTools; Node 22+, no npm dependencies.
// Launch a dedicated headless Chrome with --remote-debugging-port=9337 first.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const args = process.argv.slice(2);
const mode = args[0] || 'foundation';
const root = path.resolve(args[1] || '.');
const output = args[2] || '/tmp/ds-browser.json';
const target = await (await fetch('http://127.0.0.1:9337/json/new?about:blank', {method:'PUT'})).json();
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { ws.onopen=resolve; ws.onerror=reject; });
let sequence=0;
const pending=new Map();
const loadedDocuments=new Set();
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.method==='Page.lifecycleEvent'&&m.params.name==='load')loadedDocuments.add(m.params.loaderId);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}};
function rawSend(method,params={}) { return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));}); }
async function send(method,params={}) {
 const result=await rawSend(method,params);
 if(method==='Page.navigate') {
  if(result.errorText) throw new Error(result.errorText);
  const deadline=Date.now()+15000;
  while(result.loaderId&&!loadedDocuments.has(result.loaderId)) {
   if(Date.now()>deadline) throw new Error('Page load timed out: '+params.url);
   await new Promise(resolve=>setTimeout(resolve,25));
  }
  await rawSend('Runtime.evaluate',{expression:'document.fonts.ready.then(()=>true)',awaitPromise:true});
 }
 return result;
}
const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
await send('Page.enable');
await send('Page.setLifecycleEventsEnabled',{enabled:true});
await send('Network.enable');
await send('Network.setBlockedURLs',{urls:mode==='core'?['https://*']:['http://*','https://*']});
const results=[];
try {
 if(mode==='capture') {
  await send('Emulation.setDeviceMetricsOverride',{width:Number(args[3] || 1440),height:1000,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(root).href});await wait(800);
  if(args[5]==='open') { await evaluate(`document.querySelector(${JSON.stringify(args[4])}).querySelector('[data-feedback], [data-rating-open]').click()`); await wait(100); }
  const clip=mode==='capture'&&args[4]?await evaluate(`(()=>{const r=document.querySelector(${JSON.stringify(args[4])}).getBoundingClientRect();return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,scale:1}})()`):undefined;
  const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,...(clip?{clip}:{})});
  fs.writeFileSync(output+'.png',Buffer.from(shot.data,'base64'));
 } else if(mode==='content') {
  const {runContent}=await import('./browser-content-cases.mjs');
  results.push(...await runContent({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='faq') {
  const {runFaq}=await import('./browser-faq-cases.mjs');
  results.push(...await runFaq({send,evaluate,wait,root}));
   if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='form') {
  const {runForm}=await import('./browser-form-cases.mjs');
  results.push(...await runForm({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='contact') {
  const {runContact}=await import('./browser-contact-cases.mjs');
  results.push(...await runContact({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='radio') {
  const {runRadio}=await import('./browser-radio-cases.mjs');
  results.push(...await runRadio({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='feedback') {
  const {runFeedback}=await import('./browser-feedback-cases.mjs');
  results.push(...await runFeedback({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='services') {
  const {runServices}=await import('./browser-service-cases.mjs');
  results.push(...await runServices({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='digital-stamp') {
  const {runDigitalStamp}=await import('./browser-digital-stamp-cases.mjs');
  results.push(...await runDigitalStamp({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='footer') {
  const {runFooter}=await import('./browser-footer-cases.mjs');
  results.push(...await runFooter({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='navigation-figma') {
  const {runFigma}=await import('./browser-navigation-figma-cases.mjs');
  results.push(...await runFigma({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='template') {
  const {runTemplate}=await import('./browser-template-cases.mjs');
  results.push(...await runTemplate({send,evaluate,wait,root}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='core') {
  const {runCore}=await import('./browser-core-cases.mjs');
  results.push(...await runCore({send,evaluate,wait}));
  if(results.some(r=>!r.pass)) process.exitCode=1;
 } else if(mode==='snapshot') {
  for(const dir of fs.readdirSync(path.join(root,'components'))) {
   const page=path.join(root,'components',dir,'showcases/index.html');
   if(!fs.existsSync(page))continue;
   for(const direction of ['ltr','rtl']) {
    await send('Emulation.setDeviceMetricsOverride',{width:1280,height:900,deviceScaleFactor:1,mobile:false});
    await send('Page.navigate',{url:pathToFileURL(page).href});await wait(100);
    await evaluate(`document.documentElement.dir=${JSON.stringify(direction)}`);
    const data=await evaluate(`(() => {
      const props=['color','backgroundColor','borderTopColor','borderTopWidth','borderRadius','fontSize','fontWeight','lineHeight','paddingTop','paddingRight','paddingBottom','paddingLeft','gap'];
      return [...document.querySelectorAll('[class]')].filter(e=>[...e.classList].some(c=>!c.startsWith('showcase')&&!c.startsWith('prop-')&&!c.startsWith('is-'))).map(e=>{
        const s=getComputedStyle(e);return {tag:e.tagName,class:e.className,styles:Object.fromEntries(props.map(p=>[p,s[p]]))};
      });})()`);
    results.push({component:dir,direction,data});
   }
  }
 } else {
  for(const direction of ['ltr','rtl'])for(const width of [320,375,768,1280,1600]) {
   await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
   await send('Page.navigate',{url:pathToFileURL(path.join(root,direction==='rtl'?'tests/fixtures/foundation.html':'tests/fixtures/foundation-ltr.html')).href});await wait(100);
   await evaluate(`document.documentElement.dir=${JSON.stringify(direction)};document.documentElement.lang=${JSON.stringify(direction==='rtl'?'ar':'en')}`);
   const checks=await evaluate(`(() => {
     const container=document.querySelector('.ds-container'), c=container.getBoundingClientRect();
     const grid=document.querySelector('.ds-grid'), cards=[...grid.children].map(e=>e.getBoundingClientRect());
     const hidden=document.querySelector('.sr-only').getBoundingClientRect();
     const track=document.querySelector('.slider__track').getBoundingClientRect(), fill=document.querySelector('.slider__fill').getBoundingClientRect();
     const fillStart=document.documentElement.dir==='rtl'?(track.right-fill.right)/track.width:(fill.left-track.left)/track.width;
     return {overflow:document.documentElement.scrollWidth>innerWidth,containerWidth:c.width,
       containerCentered:Math.abs(c.left-(innerWidth-c.width)/2)<2,
       columns:getComputedStyle(grid).gridTemplateColumns.split(' ').length,
       firstCardAtStart:document.documentElement.dir==='rtl'?cards[0].right>cards[1].right:cards[0].left<cards[1].left,
       hiddenTextClipped:hidden.width<=1&&hidden.height<=1,
       rangeFillCorrect:Math.abs(fillStart-.25)<.01&&Math.abs(fill.width/track.width-.5)<.01,
       buttonFont:getComputedStyle(document.querySelector('.btn')).fontFamily,
       formFits:[...document.querySelectorAll('input,textarea,select')].every(e=>e.getBoundingClientRect().right<=innerWidth+1&&e.getBoundingClientRect().left>=-1)};
   })()`);
   await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
   await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
   checks.skipFocused=await evaluate(`document.activeElement.classList.contains('skip-link') && getComputedStyle(document.activeElement).clipPath==='none' && getComputedStyle(document.activeElement).outlineStyle!=='none'`);
   await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
   await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
   checks.skipTarget=await evaluate(`document.activeElement.id==='main-content'`);
   results.push({direction,width,checks});
  }
  await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  results.push({reducedMotion:await evaluate(`getComputedStyle(document.querySelector('.motion-probe')).animationDuration==='0s'`)});
  await send('Emulation.setEmulatedMedia',{features:[]});
  const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});
  fs.writeFileSync(output.replace(/\.json$/, '')+'.png',Buffer.from(shot.data,'base64'));
 }
 fs.writeFileSync(output,JSON.stringify(results,null,2)+'\n');
 console.log(`${mode}: ${results.length} cases written to ${output}`);
 if(mode==='foundation') {
   const failed=results.filter(x=>x.checks && (x.checks.overflow||!x.checks.containerCentered||!x.checks.hiddenTextClipped||!x.checks.formFits||!x.checks.skipFocused||!x.checks.skipTarget||!x.checks.rangeFillCorrect||(x.width>=768&&!x.checks.firstCardAtStart)||x.checks.columns!==(x.width>=1280?3:x.width>=768?2:1)))
   if(failed.length||!results.at(-1).reducedMotion){console.error(JSON.stringify(failed,null,2));process.exitCode=1;}
 }
} finally {ws.close();await fetch(`http://127.0.0.1:9337/json/close/${target.id}`);}
