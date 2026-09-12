import {pathToFileURL} from 'node:url';
import path from 'node:path';
export async function runTemplate({send,evaluate,wait,root}) {
 const results=[];
 for(const page of ['index.html','services.html','news.html','about.html']) for(const dir of ['rtl','ltr']) for(const width of [320,768,1280]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government',page)).href});await wait(150);
  await evaluate(`document.documentElement.dir='${dir}'`);
  const checks=await evaluate(`({fits:document.documentElement.scrollWidth<=innerWidth,heading:document.querySelectorAll('h1').length===1,cards:[...document.querySelectorAll('.card')].every(e=>e.getBoundingClientRect().width<=innerWidth),styles:[...document.querySelectorAll('link[rel=stylesheet]')].every(e=>e.sheet) && !!document.querySelector('link[href="components/footer/footer.css"]')})`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  checks.skip=await evaluate(`document.activeElement.classList.contains('skip-link')`);
  results.push({page,dir,width,checks,pass:Object.values(checks).every(Boolean)});
 }
 for (const dir of ['rtl','ltr']) {
  await send('Emulation.setDeviceMetricsOverride',{width:375,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/index.html')).href});await wait(250);
  await evaluate(`document.documentElement.dir='${dir}'`);
  const check=async(name,expression)=>results.push({name:dir+': '+name,pass:await evaluate(expression)});
  await check('mobile menu opens', `document.querySelector('.site-menu-toggle').focus();document.querySelector('.site-menu-toggle').click(); getComputedStyle(document.querySelector('#main-navigation')).display!=='none'`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await check('Escape closes menu', `document.querySelector('.site-menu-toggle').getAttribute('aria-expanded')==='false'`);
  await check('search modal', `document.querySelector('.site-search-trigger').click();document.querySelector('.site-search').open && document.activeElement.id==='site-search-input'`);
  await check('search suggestions', `document.querySelector('#site-search-input').value='متابعة';document.querySelector('#site-search-input').dispatchEvent(new Event('input'));[...document.querySelectorAll('#search-results li')].filter(e=>!e.hidden).length===1`);
  await check('search clear', `document.querySelector('[data-search-clear]').click();document.querySelector('#site-search-input').value==='' && document.querySelector('[data-search-clear]').hidden`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await wait(80);
  await check('search restores focus', `!document.querySelector('.site-search').open && document.activeElement.classList.contains('site-search-trigger')`);
  await check('hero selection', `document.querySelectorAll('.hero-dot')[1].click();document.querySelector('#page-title').textContent===document.querySelectorAll('.hero-dot')[1].dataset.title && document.querySelectorAll('h1').length===1`);
  await evaluate(`document.querySelector('[data-next]').click()`);await wait(600);
  await check('carousel advances', `Math.abs(document.querySelector('#services-track').scrollLeft)>50`);
  await check('feedback opens', `document.querySelector('[data-feedback="yes"]').click();!document.querySelector('.feedback-form').hidden`);
  await check('feedback local completion', `document.querySelector('.feedback-form input[name="reason"]:not(:disabled)').checked=true;document.querySelector('.feedback-form').requestSubmit();document.querySelector('.feedback-form').hidden && document.querySelector('.feedback-status').textContent.includes('لم تُرسل')`);
 }
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/index.html')).href});await wait(200);
 results.push({name:'No JavaScript: navigation and content remain available',pass:await evaluate(`getComputedStyle(document.querySelector('#main-navigation')).display!=='none' && document.querySelectorAll('#services-track .card').length===6 && document.querySelector('.site-menu-toggle').hidden`)});
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 const {runNavigation}=await import('./browser-navigation-cases.mjs');
 results.push(...await runNavigation({send,evaluate,wait,root}));
 return results;
}
