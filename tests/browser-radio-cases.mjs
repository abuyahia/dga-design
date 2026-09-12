import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runRadio({send,evaluate,root}) {
 const results=[];
 const check=async(name,code)=>results.push({name,pass:await evaluate(code)});
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const dir of ['rtl','ltr']) {
  await send('Emulation.setDeviceMetricsOverride',{width:430,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:pathToFileURL(path.join(root,'components/radio/showcases/index.html')).href});
  await evaluate(`document.documentElement.dir='${dir}'`);
  await check('Control geometry and default '+dir,`(()=>{const c=document.querySelector('.radio__control');return getComputedStyle(c).width==='24px'&&getComputedStyle(c).height==='24px'&&getComputedStyle(c,'::before').transform==='matrix(0, 0, 0, 0, 0, 0)'&&document.documentElement.scrollWidth<=innerWidth})()`);
  await check('Brand checked '+dir,`(()=>{const i=document.querySelector('.radio--brand input:checked:not(:disabled)'),c=i.nextElementSibling;return getComputedStyle(c,'::before').backgroundColor==='rgb(27, 131, 84)'&&getComputedStyle(c,'::before').width==='15px'&&getComputedStyle(c,'::before').transform==='matrix(1, 0, 0, 1, 0, 0)'})()`);
  await check('Neutral checked '+dir,`getComputedStyle(document.querySelector('.radio:not(.radio--brand) input:checked').nextElementSibling,'::before').backgroundColor==='rgb(13, 18, 28)'`);
  await check('Disabled preserves selection '+dir,`(()=>{const i=[...document.querySelectorAll('.radio--brand input:disabled')];return getComputedStyle(i[0].nextElementSibling,'::before').transform==='matrix(0, 0, 0, 0, 0, 0)'&&getComputedStyle(i[1].nextElementSibling,'::before').transform==='matrix(1, 0, 0, 1, 0, 0)'&&i.every(e=>getComputedStyle(e.nextElementSibling).borderColor==='rgb(157, 164, 174)')})()`);
  const rect=await evaluate(`(()=>{const r=document.querySelector('.radio').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
  await send('Input.dispatchMouseEvent',{type:'mouseMoved',...rect});
  await check('Hover halo '+dir,`getComputedStyle(document.querySelector('.radio__control'),'::after').opacity==='1'&&getComputedStyle(document.querySelector('.radio__control'),'::after').width==='48px'`);
  await send('Input.dispatchMouseEvent',{type:'mousePressed',...rect,button:'left',clickCount:1});
  await check('Pressed unchecked '+dir,`getComputedStyle(document.querySelector('.radio__control')).backgroundColor==='rgb(210, 214, 219)'`);
  await send('Input.dispatchMouseEvent',{type:'mouseReleased',...rect,button:'left',clickCount:1});
  await check('Click selects exclusively '+dir,`document.querySelector('input[name=brand]').checked&&document.querySelectorAll('input[name=brand]:checked').length===1`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});
  await check('Arrow changes selection and focus '+dir,`document.activeElement.value==='two'&&document.activeElement.checked`);
  await check('Keyboard focus square '+dir,`(()=>{const c=document.activeElement.nextElementSibling,s=getComputedStyle(c,'::after');return s.borderTopWidth==='2px'&&s.borderRadius==='0px'&&s.width==='32px'})()`);
 }
 await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/about.html')).href});
 await evaluate(`document.querySelector('[data-feedback=yes]').click()`);
 await check('Feedback reuses canonical markup',`document.querySelectorAll('.feedback-gender .radio__input').length===3&&document.querySelector('.feedback-gender input:checked').value==='unspecified'&&getComputedStyle(document.querySelector('.feedback-gender .radio__control')).width==='24px'`);
 await evaluate(`document.querySelector('.feedback-gender input[value=male]').click()`);
 await check('Feedback group remains exclusive',`document.querySelectorAll('.feedback-gender input:checked').length===1&&new FormData(document.querySelector('.feedback-form')).get('gender')==='male'`);
 await evaluate(`document.querySelectorAll('.feedback-gender input').forEach(i=>i.disabled=true)`);
 await check('Feedback disabled appearance inherited',`[...document.querySelectorAll('.feedback-gender .radio__label')].every(e=>getComputedStyle(e).color==='rgb(157, 164, 174)')`);
 return results;
}
