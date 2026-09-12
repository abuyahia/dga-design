import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runDigitalStamp({send,evaluate,wait,root}) {
 const results=[];
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 const key=async(key,code,n)=>{await send('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode:n,...(key==='Enter'?{text:'\r'}:key===' '?{text:' '}: {})});await send('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:n});await wait(30);};
 for(const direction of ['rtl','ltr']) for(const width of [320,390,767,768,1728]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/digital-stamp/showcases',direction+'-closed.html')).href});await wait(120);await send('Page.bringToFront');
  await evaluate('document.fonts.ready.then(()=>true)');
  const check=async(name,expression)=>{const value=await evaluate(expression);results.push({name,direction,width,pass:value});};
  await check('Closed geometry and hidden content', `(()=>{const d=document.querySelector('details'),s=getComputedStyle(d);return !d.open&&s.backgroundColor==='rgb(243, 244, 246)'&&getComputedStyle(d.querySelector('.digital-stamp__body')).display==='none'&&(innerWidth!==390||d.getBoundingClientRect().height===(document.documentElement.dir==='rtl'?60:80))&&(innerWidth!==1728||d.getBoundingClientRect().height===32)})()`);
  await evaluate("document.querySelector('summary').focus()");
  await check('Visible keyboard focus', `getComputedStyle(document.querySelector('.digital-stamp__action')).outlineWidth==='2px'`);
  await key('Enter','Enter',13);
  const geometry=await evaluate(`(()=>{const d=document.querySelector('details'),icon=d.querySelector('.digital-stamp__featured'),flag=d.querySelector('.digital-stamp__flag'),body=d.querySelector('.digital-stamp__body');return {open:d.open,height:d.getBoundingClientRect().height,icon:icon.getBoundingClientRect().width,flag:[flag.getBoundingClientRect().width,flag.getBoundingClientRect().height],gap:getComputedStyle(body).marginTop,overflow:document.documentElement.scrollWidth>innerWidth,assets:[...d.querySelectorAll('img')].every(e=>e.complete&&e.naturalWidth>0),arrow:getComputedStyle(d.querySelector('.digital-stamp__arrow-open')).visibility}})()`);
  const expected=width===390?(direction==='rtl'?442:514):width===1728?(direction==='rtl'?240.574:272.574):null;
  results.push({name:'Open geometry, original assets and arrow',direction,width,actual:geometry,pass:geometry.open&&!geometry.overflow&&geometry.assets&&geometry.icon===(width<768?32:48)&&geometry.flag[0]===20&&geometry.flag[1]===14&&geometry.gap==='40px'&&geometry.arrow==='visible'&&(expected===null||Math.abs(geometry.height-expected)<1)});
  await key('Tab','Tab',9);
  await check('Tab reaches registration link', `document.activeElement.matches('.digital-stamp__registration a')`);
  await key('Escape','Escape',27);
  await check('Escape closes and returns focus', `!document.querySelector('details').open&&document.activeElement.tagName==='SUMMARY'`);
  await key(' ','Space',32);
  await check('Space opens native disclosure', `document.querySelector('details').open`);
  await key(' ','Space',32);
  await key('Tab','Tab',9);
  await check('Closed registration is skipped by Tab', `!document.activeElement.matches('.digital-stamp__registration a')`);
 }
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/digital-stamp/showcases/rtl-closed.html')).href});await wait(120);await send('Page.bringToFront');
 await evaluate("document.querySelector('summary').focus()");await key('Enter','Enter',13);
 results.push({name:'Native disclosure works without JavaScript',pass:await evaluate("document.querySelector('details').open")});
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/digital-stamp/showcases/index.html')).href});await wait(150);
 results.push({name:'Instances toggle independently',pass:await evaluate(`(()=>{const d=[...document.querySelectorAll('details')];const before=d[1].open;d[0].querySelector('summary').click();return d[0].open&&d[1].open===before})()`)});
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/index.html')).href});await wait(150);
 results.push({name:'First page element after skip link, before header; explicit preview data',pass:await evaluate(`(()=>{const d=document.querySelector('.digital-stamp');return document.body.children[0].classList.contains('skip-link')&&document.body.children[1]===d&&d.nextElementSibling.tagName==='HEADER'&&d.querySelector('summary').textContent.includes('معاينة')&&!d.querySelector('.digital-stamp__registration a')})()`)});
 return results;
}
