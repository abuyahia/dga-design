export async function runLink({send,evaluate,wait}) {
  const results=[];
  const check=async(name,expression)=>results.push({name,pass:await evaluate(expression)});
  const key=async(key,code,n)=>{for(const type of ['keyDown','keyUp'])await send('Input.dispatchKeyEvent',{type,key,code,windowsVirtualKeyCode:n});};

  await send('Page.navigate',{url:'http://127.0.0.1:8765/components/link/showcases/index.html'});
  await wait(100);
  await check('showcase: three disabled variants', `document.querySelectorAll('.link[aria-disabled="true"]').length===3`);
  await check('showcase: disabled markup contract', `[...document.querySelectorAll('.link[aria-disabled="true"]')].every(link=>!link.hasAttribute('href')&&link.getAttribute('role')==='link'&&!link.hasAttribute('tabindex'))`);
  await check('showcase: disabled pointer contract', `[...document.querySelectorAll('.link[aria-disabled="true"]')].every(link=>getComputedStyle(link).pointerEvents==='none')`);
  await check('showcase: disabled cursor contract', `[...document.querySelectorAll('.link[aria-disabled="true"]')].every(link=>getComputedStyle(link).cursor==='not-allowed')`);
  await check('showcase: disabled decoration contract', `[...document.querySelectorAll('.link[aria-disabled="true"]')].every(link=>getComputedStyle(link).textDecorationLine==='none')`);
  await check('showcase: active destinations intact', `[...document.querySelectorAll('.link:not([aria-disabled="true"])')].every(link=>link.hasAttribute('href'))`);

  await send('Page.navigate',{url:'http://127.0.0.1:8765/tests/fixtures/core.html'});
  for(let i=0;i<50&&!await evaluate('window.ready===true');i++)await wait(50);
  await check('core fixture: optional focus policy', `(()=>{const link=document.querySelector('#disabled-link');return !link.hasAttribute('href')&&link.getAttribute('role')==='link'&&link.getAttribute('aria-disabled')==='true'&&link.tabIndex===0})()`);
  await evaluate(`window.__disabledLinkActivated=false;document.querySelector('#disabled-link').addEventListener('click',()=>{window.__disabledLinkActivated=true});document.querySelector('#disabled-link').focus()`);
  await key('Enter','Enter',13);
  await check('core runtime: defensive guard', `!window.__disabledLinkActivated&&location.hash===''`);
  await evaluate(`document.querySelector('a.link[href="#field"]').click()`);
  await check('core runtime: active navigation intact', `location.hash==='#field'`);

  return results;
}
