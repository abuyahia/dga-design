import path from 'node:path';
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
export async function runServices({send,evaluate,wait,root}) {
 const results=[],data=JSON.parse(fs.readFileSync(path.join(root,'site/government.json'),'utf8'));
 const load=async(page,width=1440,dir='rtl')=>{await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government',page)).href});await evaluate(`document.documentElement.dir=${JSON.stringify(dir)}`);};
 const check=async(name,expression)=>results.push({name,pass:await evaluate(expression)});
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const page of ['services.html',...data.services.map(s=>'service-'+s.id+'.html')])for(const direction of ['rtl','ltr'])for(const width of [320,430,768,1440]) {
  await load(page,width,direction);
  const checks=await evaluate(`(()=>{const main=document.querySelector('.service-page__main'),sidebar=document.querySelector('.service-page__sidebar');return {fits:document.documentElement.scrollWidth<=innerWidth,h1:document.querySelectorAll('h1').length===1,assets:[...document.images].every(e=>e.complete&&e.naturalWidth>0),styles:[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>e.sheet),columns:!main||(innerWidth<768?sidebar.getBoundingClientRect().top>=main.getBoundingClientRect().bottom:(document.documentElement.dir==='rtl'?main.getBoundingClientRect().left>sidebar.getBoundingClientRect().left:main.getBoundingClientRect().left<sidebar.getBoundingClientRect().left)),figma:!main||innerWidth!==1440||(Math.abs(main.getBoundingClientRect().width-832)<1&&Math.abs(sidebar.getBoundingClientRect().width-416)<1&&getComputedStyle(document.querySelector('#page-title')).fontSize==='30px'),onePanel:!main||[...document.querySelectorAll('[role=tabpanel]')].filter(e=>!e.hidden).length===1}})()`);
  results.push({page,direction,width,checks,pass:Object.values(checks).every(Boolean)});
 }
 await load('services.html',430);
 await check('Arabic diacritics normalized in search', `document.querySelector('#catalog-query').value='تَقْدِيم';document.querySelector('#catalog-query').dispatchEvent(new Event('input'));document.querySelectorAll('[data-service-card]:not([hidden])').length===1`);
 await check('Audience combines with query', `document.querySelector('#catalog-query').value='متابعة';document.querySelector('#catalog-query').dispatchEvent(new Event('input'));[...document.querySelectorAll('[data-audience]')].find(e=>e.dataset.audience==='أعمال').click();document.querySelectorAll('[data-service-card]:not([hidden])').length===1&&new URLSearchParams(location.search).get('audience')==='أعمال'`);
 await check('Empty search results announced', `document.querySelector('#catalog-query').value='zzzz';document.querySelector('#catalog-query').dispatchEvent(new Event('input'));!document.querySelector('[data-catalog-empty]').hidden&&document.querySelector('[data-catalog-status]').textContent.startsWith('0')`);
 await check('Reset restores every card and focus', `document.querySelector('[data-catalog-empty] button').click();document.querySelectorAll('[data-service-card]:not([hidden])').length===${data.services.length}&&document.activeElement.id==='catalog-query'&&!location.search`);
 await evaluate(`document.querySelector('#catalog-query').value='متابعة';document.querySelector('#catalog-query').dispatchEvent(new Event('input'))`);
 await send('Page.navigate',{url:await evaluate('location.href')});await check('URL restores search query', `document.querySelector('#catalog-query').value==='متابعة'&&document.querySelectorAll('[data-service-card]:not([hidden])').length===1`);
 for(const direction of ['rtl','ltr']) {
  await load('service-new-request.html',430,direction);
  await check('Detail tab click '+direction, `document.querySelector('#tab-documents').click();!document.querySelector('#panel-documents').hidden&&document.querySelector('#panel-steps').hidden&&document.querySelector('#tab-documents').getAttribute('aria-selected')==='true'`);
  await evaluate(`document.querySelector('#tab-steps').focus()`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:direction==='rtl'?'ArrowLeft':'ArrowRight',code:direction==='rtl'?'ArrowLeft':'ArrowRight',windowsVirtualKeyCode:direction==='rtl'?37:39});
  await check('Directional arrow selects and focuses '+direction, `document.activeElement.id==='tab-requirements'&&!document.querySelector('#panel-requirements').hidden`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'End',code:'End',windowsVirtualKeyCode:35});
  await check('End selects last tab '+direction, `document.activeElement.id==='tab-documents'&&document.querySelectorAll('[role=tab][tabindex="0"]').length===1`);
  await check('Return to steps opens hidden panel '+direction, `document.querySelector('[data-open-steps]').click();!document.querySelector('#panel-steps').hidden`);
 }
 await load('service-new-request.html');await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/service-new-request.html')).href+'#panel-documents'});
 await check('Direct panel link opens correct section', `!document.querySelector('#panel-documents').hidden`);
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await load('services.html',320);await check('No JS catalogue retains all service links', `document.querySelectorAll('[data-service-card]').length===${data.services.length}&&[...document.querySelectorAll('[data-service-card]')].every(e=>!e.hidden)&&document.querySelector('.service-catalog form').hidden`);
 await load('service-new-request.html',320);await check('No JS detail sections remain readable', `[...document.querySelectorAll('.service-page__panel')].every(e=>!e.hidden)&&document.querySelector('.service-page__details .tab-list').hidden`);
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
