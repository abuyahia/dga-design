// Browser verification through Chrome DevTools; Node 22+, no npm dependencies.
// Launch a dedicated headless Chrome with --remote-debugging-port=9341 first.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const args = process.argv.slice(2);
const mode = 'ownership';
const root = path.resolve(args[0] || '/tmp/f03-after/site');
const output = args[1] || '/tmp/f03-runtime.json';
const target = await (await fetch('http://127.0.0.1:9341/json/new?about:blank', {method:'PUT'})).json();
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
const check=async(name,expression)=>{const pass=await evaluate(expression);results.push({name,pass});if(!pass)throw new Error(name);};
const load=async page=>send('Page.navigate',{url:pathToFileURL(path.join(root,page)).href});
try {
 await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
 for(const page of ['about.html','news.html','services.html','faq.html','content.html','service-new-request.html','form.html','contact.html']) {
  await load(page);
  await check(page+' assets',`[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>e.sheet)&&[...document.images].every(e=>e.complete&&e.naturalWidth>0)&&document.querySelectorAll('h1').length===1&&(()=>{const refs=[...document.querySelectorAll('script[src],link[rel=stylesheet]')].map(e=>e.src||e.href);return new Set(refs).size===refs.length})()`);
 }
 await load('faq.html');
 await check('FAQ toggles once',`(()=>{const b=document.querySelector('.accordion__trigger');b.click();return b.getAttribute('aria-expanded')==='true'&&!document.getElementById(b.getAttribute('aria-controls')).hidden})()`);
 await check('CTA own styling',`getComputedStyle(document.querySelector('.contact-cta__icon')).width==='48px'&&getComputedStyle(document.querySelector('.contact-cta')).paddingTop==='40px'`);
 await load('content.html');
 await check('TOC idempotent init and current link',`(()=>{PlatformTableOfContents.init();PlatformTableOfContents.init();const links=[...document.querySelectorAll('.table-of-contents__link')];links[2].click();return links[2].getAttribute('aria-current')==='location'&&links.filter(e=>e.hasAttribute('aria-current')).length===1})()`);
 await load('service-new-request.html');
 await check('Tabs mount returns same controller',`(()=>{const root=document.querySelector('[data-service-tabs]');return PlatformTabs.mount(root)===PlatformTabs.mount(root)})()`);
 for (const dir of ['rtl','ltr']) {
  await evaluate(`document.documentElement.dir='${dir}'`);
  await check('Tab arrows and route '+dir,`(()=>{const b=document.querySelector('#tab-steps');b.dispatchEvent(new KeyboardEvent('keydown',{key:'${dir==='rtl'?'ArrowLeft':'ArrowRight'}',bubbles:true}));return document.activeElement.id==='tab-requirements'&&!document.querySelector('#panel-requirements').hidden&&location.hash==='#panel-requirements'})()`);
 }
 await check('Tab End and steps integration',`(()=>{document.querySelector('#tab-requirements').dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));const ok=!document.querySelector('#panel-documents').hidden;document.querySelector('[data-open-steps]').click();return ok&&!document.querySelector('#panel-steps').hidden})()`);
 await load('form.html');
 await check('Progress no double mount',`(()=>{PlatformFormTemplate.init();PlatformFormTemplate.init();const root=document.querySelector('[data-progress-indicator]');const same=PlatformProgressIndicator.mount(root)===PlatformProgressIndicator.mount(root);document.querySelector('[data-form-next]').click();return same&&document.querySelector('[data-progress-current]').textContent==='3'&&document.querySelectorAll('[aria-current=step]').length===1})()`);
 await check('Progress previous and announcement',`(()=>{document.querySelector('[data-form-previous]').click();return document.querySelector('[data-progress-current]').textContent==='2'&&document.querySelector('[data-form-step-status]').textContent.includes('2')})()`);
 await load('contact.html');
 await check('Upload mount returns same controller',`(()=>{PlatformContact.init();const root=document.querySelector('.file-upload');return PlatformFileUpload.mount(root)===PlatformFileUpload.mount(root)})()`);
 const attach=async(name,size,type)=>evaluate(`(()=>{const d=new DataTransfer();d.items.add(new File([new Uint8Array(${size})],${JSON.stringify(name)},{type:${JSON.stringify(type)}}));const input=document.querySelector('#contact-attachment');input.files=d.files;input.dispatchEvent(new Event('change'));})()`);
 for(const [name,size,type,message] of [['bad.exe',20,'application/octet-stream','JPG'],['large.pdf',2097153,'application/pdf','2 ميجابايت'],['empty.pdf',0,'application/pdf','فارغ']]) {
  await attach(name,size,type);
  await check('Contact attachment policy '+name,`document.querySelector('#contact-attachment-error').textContent.includes(${JSON.stringify(message)})&&document.querySelector('#contact-attachment').getAttribute('aria-invalid')==='true'`);
 }
 await attach('document.pdf',40,'application/pdf');
 await check('Valid upload UI',`document.querySelector('.file-upload').classList.contains('is-uploaded')&&document.querySelector('[data-file-name]').textContent==='document.pdf'&&document.querySelector('#contact-attachment-error').hidden`);
 await check('Remove restores focus',`(()=>{document.querySelector('[data-file-remove]').click();return document.querySelector('#contact-attachment').files.length===0&&!document.querySelector('.file-upload').classList.contains('is-uploaded')&&document.activeElement.hasAttribute('data-file-browse')})()`);
 console.log(JSON.stringify({passed:results.length,results}));
} finally {
 fs.writeFileSync(output,JSON.stringify(results,null,2));
 ws.close();
}
