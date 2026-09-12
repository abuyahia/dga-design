export async function runCore({send,evaluate,wait}) {
 const results=[];
 const check=async(name,expression)=>results.push({name,pass:await evaluate(expression)});
 const key=async(key,code,n)=>{for(const type of ['keyDown','keyUp'])await send('Input.dispatchKeyEvent',{type,key,code,windowsVirtualKeyCode:n});};
 for(const direction of ['rtl','ltr']) for(const width of [320,768,1280]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:'http://127.0.0.1:8765/tests/fixtures/core.html'});
  for(let i=0;i<50&&!await evaluate('window.ready===true');i++)await wait(50);
  await evaluate(`document.documentElement.dir='${direction}'`);
  await check(`${direction}/${width}: responsive`, 'document.documentElement.scrollWidth<=innerWidth');
  await check(`${direction}/${width}: initial states`, `document.querySelector('#panel').hidden && !document.querySelector('#panel2').hidden && document.querySelector('#mixed').indeterminate`);
  await evaluate(`document.querySelector('#trigger').focus()`);await key('Enter','Enter',13);
  await check(`${direction}/${width}: keyboard and isolation`, `!document.querySelector('#panel').hidden && !document.querySelector('#panel2').hidden && document.querySelector('#trigger').getAttribute('aria-expanded')==='true'`);
  await evaluate(`document.querySelector('#check-readonly').focus()`);await key(' ','Space',32);
  await check(`${direction}/${width}: readonly keyboard`, `document.querySelector('#check-readonly').checked && !document.querySelector('#check-readonly').disabled`);
  await check(`${direction}/${width}: readonly click`, `document.querySelector('#check-readonly').click();document.querySelector('#check-readonly').checked`);
  await check(`${direction}/${width}: idempotence`, `window.initCore()===window.dispose`);
  await check(`${direction}/${width}: cleanup`, `window.dispose();!document.querySelector('#panel').hidden && document.querySelector('#trigger').disabled && document.querySelector('#check-readonly').disabled`);
  await check(`${direction}/${width}: remount`, `window.dispose=window.initCore();document.querySelector('#panel').hidden`);
 }
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await send('Page.navigate',{url:'http://127.0.0.1:8765/tests/fixtures/core.html?nojs'});await wait(200);
 await check('JavaScript disabled: readable content and safe readonly', `getComputedStyle(document.querySelector('#panel')).display!=='none' && document.querySelector('#check-readonly').disabled`);
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
