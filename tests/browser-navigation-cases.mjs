import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runNavigation({send,evaluate,wait,root}) {
 const results=[];
 const key=async(key,code,n)=>{for(const type of ['keyDown','keyUp'])await send('Input.dispatchKeyEvent',{type,key,code,windowsVirtualKeyCode:n,...(type==='keyDown'&&key==='Enter'?{text:'\r'}:{})});};
 for(const dir of ['rtl','ltr'])for(const width of [375,1280]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/services.html')).href});await wait(200);
  await evaluate(`document.documentElement.dir='${dir}';window.navTriggers=[...document.querySelectorAll('.nav-header__item[aria-controls]')];if(innerWidth<=960)document.querySelector('.nav-header__toggle').click()`);
  const check=async(name,expression)=>results.push({name:`navigation ${dir}/${width}: ${name}`,pass:await evaluate(expression)});
  await check('selected appearance', `getComputedStyle(navTriggers[1]).backgroundColor==='rgb(27, 131, 84)' && getComputedStyle(navTriggers[1],'::after').height==='6px' && navTriggers[1].getAttribute('aria-expanded')==='false'`);
  await evaluate('navTriggers[1].focus()');await key('Enter','Enter',13);
  await check('Enter opens submenu', `navTriggers[1].getAttribute('aria-expanded')==='true' && !document.getElementById(navTriggers[1].getAttribute('aria-controls')).hidden`);
  await check('focus ring', `getComputedStyle(navTriggers[1],'::before').borderTopWidth==='2px'`);
  await key('Escape','Escape',27);
  await check('Escape restores trigger', `navTriggers[1].getAttribute('aria-expanded')==='false' && document.activeElement===navTriggers[1]`);
  await key(' ','Space',32);
  await check('Space opens submenu', `navTriggers[1].getAttribute('aria-expanded')==='true'`);
  await check('one submenu open', `navTriggers[0].click();navTriggers[0].getAttribute('aria-expanded')==='true' && navTriggers[1].getAttribute('aria-expanded')==='false'`);
  await check('outside click closes', `document.querySelector('main').click();navTriggers.every(t=>t.getAttribute('aria-expanded')==='false')`);
  await check('page fits', 'document.documentElement.scrollWidth<=innerWidth');
 }
 const source=fs.readFileSync(path.join(root,'components/navigation-header/navigation-header.js'),'utf8').replace('export function initNavigationHeaders','function initNavigationHeaders');
 await evaluate(`window.initNavForTest=(()=>{${source};return initNavigationHeaders})()`);
 await evaluate(`window.navClone=document.querySelector('.nav-header').cloneNode(true);for(const e of navClone.querySelectorAll('[id]'))e.id='clone-'+e.id;for(const e of navClone.querySelectorAll('[aria-controls]'))e.setAttribute('aria-controls','clone-'+e.getAttribute('aria-controls'));document.body.append(navClone);window.disposeNav=initNavForTest(navClone);initNavForTest(navClone);`);
 results.push({name:'navigation: idempotence and instance isolation',pass:await evaluate(`navClone.querySelector('.nav-header__item[aria-controls]').click();navClone.querySelector('.nav-header__item[aria-controls]').getAttribute('aria-expanded')==='true' && document.querySelector('.nav-header__item[aria-controls]').getAttribute('aria-expanded')==='false'`)});
 results.push({name:'navigation: cleanup restores readable fallback',pass:await evaluate(`disposeNav();!navClone.hasAttribute('data-enhanced') && [...navClone.querySelectorAll('.nav-header__panel')].every(e=>!e.hidden) && navClone.querySelector('[data-enhancement-disabled]').disabled`)});
 results.push({name:'navigation: remount works',pass:await evaluate(`window.disposeNav=initNavForTest(navClone);navClone.querySelector('.nav-header__item[aria-controls]').click();navClone.querySelector('.nav-header__item[aria-controls]').getAttribute('aria-expanded')==='true'`)});
 await evaluate('disposeNav();navClone.remove()');
 return results;
}
