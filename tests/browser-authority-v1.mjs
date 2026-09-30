import path from 'node:path';
import {pathToFileURL} from 'node:url';

export async function runAuthority({send,evaluate,wait,root}) {
 const results=[],base=path.join(root,'dist/products/authority');
 const load=async(page,width=1280,dir='rtl')=>{await send('Emulation.setDeviceMetricsOverride',{width,height:950,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:pathToFileURL(path.join(base,page)).href});await wait(120);await evaluate(`document.documentElement.dir=${JSON.stringify(dir)}`);};
 const pages=['index.html','services.html','service-journey-readiness.html','news-demo-work-guide-library.html','program-ecosystems-360.html','resource-service-journey-guide.html','regulations.html','regulation-service-ecosystem-improvement-framework.html','search.html'];
 for(const page of pages)for(const dir of ['rtl','ltr'])for(const width of [320,768,1280]){
  await load(page,width,dir);
  const checks=await evaluate(`(()=>{const failures=[...document.querySelectorAll('body *')].filter(x=>{const r=x.getBoundingClientRect();return r.width>0&&(r.left < -1||r.right>innerWidth+1)&&!x.closest('.home-carousel')}).slice(0,8).map(x=>({tag:x.tagName,class:x.className,left:x.getBoundingClientRect().left,right:x.getBoundingClientRect().right,width:x.getBoundingClientRect().width}));return {fits:document.documentElement.scrollWidth<=innerWidth,h1:document.querySelectorAll('h1').length===1,styles:[...document.querySelectorAll('link[rel=stylesheet]')].every(x=>x.sheet),images:[...document.images].every(x=>x.complete&&x.naturalWidth>0),cards:[...document.querySelectorAll('.card:not(.home-carousel .card)')].every(x=>x.getBoundingClientRect().left>=-1&&x.getBoundingClientRect().right<=innerWidth+1),failures}})()`);
  results.push({page,dir,width,checks,pass:checks.fits&&checks.h1&&checks.styles&&checks.images&&checks.cards});
 }
 const check=async(name,expression)=>results.push({name,pass:await evaluate(expression)});
 await load('services.html',430);
 await check('service category filter',`document.querySelector('#catalog-category').value='البيانات';document.querySelector('#catalog-category').dispatchEvent(new Event('change'));document.querySelectorAll('[data-service-card]:not([hidden])').length===1`);
 await check('service empty and reset',`document.querySelector('#catalog-query').value='لا-نتيجة';document.querySelector('#catalog-query').dispatchEvent(new Event('input'));!document.querySelector('[data-catalog-empty]').hidden&&(document.querySelector('[data-catalog-empty] button').click(),document.querySelectorAll('[data-service-card]:not([hidden])').length===5)`);
 await load('programs.html',430);await check('portfolio kind filter',`document.querySelector('[data-filter-kind]').value='initiative';document.querySelector('[data-filter-kind]').dispatchEvent(new Event('input'));document.querySelectorAll('[data-record]:not([hidden])').length===2`);
 await load('knowledge.html',430);await check('resource search and empty state',`document.querySelector('[data-filter-query]').value='قاموس';document.querySelector('[data-filter-query]').dispatchEvent(new Event('input'));document.querySelectorAll('[data-record]:not([hidden])').length===1`);
 await load('regulations.html',430);await check('regulatory status filter',`document.querySelector('[data-filter-status]').value='draft';document.querySelector('[data-filter-status]').dispatchEvent(new Event('input'));document.querySelectorAll('[data-record]:not([hidden])').length===1`);
 await load('search.html',430);await check('search finds portfolio',`document.querySelector('[name="q"]').value='منظومات 360';document.querySelector('[name="q"]').dispatchEvent(new Event('input'));document.querySelectorAll('[data-search-record]:not([hidden])').length>=1`);
 await load('service-journey-readiness.html',430,'rtl');await check('service tabs enhanced',`document.querySelector('#tab-requirements').click();!document.querySelector('#panel-requirements').hidden&&document.querySelector('#tab-requirements').getAttribute('aria-selected')==='true'`);
 await load('index.html',375);await check('mobile navigation opens',`document.querySelector('.site-menu-toggle').focus();document.querySelector('.site-menu-toggle').click();document.querySelector('.site-menu-toggle').getAttribute('aria-expanded')==='true'`);await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await check('mobile navigation closes with Escape',`document.querySelector('.site-menu-toggle').getAttribute('aria-expanded')==='false'`);
 await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});await load('index.html',1280);await check('reduced motion honored',`[...document.querySelectorAll('*')].every(x=>{const s=getComputedStyle(x);return parseFloat(s.animationDuration||0)===0&&parseFloat(s.transitionDuration||0)===0})`);await send('Emulation.setEmulatedMedia',{features:[]});
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await load('services.html',320);await check('no JS services remain complete',`document.querySelectorAll('[data-service-card]').length===5&&[...document.querySelectorAll('[data-service-card]')].every(x=>!x.hidden)&&document.querySelector('.service-catalog__search').hidden`);
 await load('programs.html',320);await check('no JS portfolio remains complete',`document.querySelectorAll('[data-record]').length===4&&document.querySelector('.record-collection__controls').hidden`);
 await load('regulations.html',320);await check('no JS regulations remain complete',`document.querySelectorAll('[data-record]').length===3&&document.querySelector('.regulatory-library__controls').hidden`);
 await load('service-journey-readiness.html',320);await check('no JS service details readable',`[...document.querySelectorAll('.service-page__panel')].every(x=>!x.hidden)&&document.querySelector('.tab-list').hidden`);
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
