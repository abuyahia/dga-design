import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runFeedback({send,evaluate,wait,root}) {
 const results=[];
 const load=async(file,width=1440,dir='rtl')=>{await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:pathToFileURL(path.join(root,file)).href});await evaluate(`document.documentElement.dir=${JSON.stringify(dir)}`);};
 const check=async(name,expression)=>results.push({name,pass:await evaluate(expression)});
 const click=selector=>evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const kind of ['page','service'])for(const dir of ['rtl','ltr'])for(const width of [320,430,768,1440]) {
  await load('dist/government/'+(kind==='page'?'about.html':'service-new-request.html'),width,dir);
  await check(`${kind} default ${dir} ${width}`,`document.documentElement.scrollWidth<=innerWidth&&document.querySelectorAll('[data-feedback-component]').length===1&&document.querySelector('[data-feedback-component]').dataset.feedbackComponent==='${kind}'&&[...document.images].every(i=>i.complete&&i.naturalWidth>0)&&document.querySelector('.feedback-form').hidden`);
  await click(kind==='page'?'[data-feedback=no]':'[data-rating-open]');
  await check(`${kind} open ${dir} ${width}`,`!document.querySelector('.feedback-form').hidden&&document.documentElement.scrollWidth<=innerWidth&&document.activeElement.name==='${kind==='page'?'reason':'score'}'&&getComputedStyle(document.querySelector('.feedback-body')).gridTemplateColumns.split(' ').length===${width<768?1:2}`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await check(`${kind} escape ${dir} ${width}`,`document.querySelector('.feedback-form').hidden&&document.activeElement.matches('[data-feedback], [data-rating-open]')`);
 }
 await load('dist/government/about.html'); await click('[data-feedback=yes]');
 await check('Page reason required',`document.querySelector('.feedback-form').requestSubmit();!document.querySelector('.feedback-error').hidden&&!document.querySelector('.feedback-form').hidden`);
 await check('Two reason limit',`[...document.querySelectorAll('[data-reason-group=yes] input')].slice(0,3).forEach(i=>i.click());document.querySelectorAll('input[name=reason]:checked').length===2&&!document.querySelector('.feedback-error').hidden`);
 await check('Changing choice clears stale reasons',`document.querySelector('[data-feedback=no]').click();document.querySelectorAll('input[name=reason]:checked').length===0&&[...document.querySelectorAll('[data-reason-group=yes] input')].every(i=>i.disabled)&&document.querySelectorAll('[data-reason-group=no]:not([hidden])').length===5`);
 await click('[data-reason-group=no] input');await evaluate(`document.querySelector('.feedback-form').requestSubmit()`);await wait(50);
 await check('Page local completion honest',`document.querySelector('.feedback-form').hidden&&!document.querySelector('.feedback-result').hidden&&document.querySelector('.feedback-status').textContent.includes('لم تُرسل')&&document.activeElement.classList.contains('feedback-result')`);
 await load('dist/government/service-new-request.html');await click('[data-rating-open]');
 await check('Score required before submitting',`document.querySelector('.feedback-form').requestSubmit();!document.querySelector('.feedback-form').hidden&&document.querySelector('input[name=score]').validity.valueMissing`);
 await evaluate(`document.querySelector('input[name=score]').focus()`);
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});
 await check('Native stars keyboard selection',`document.querySelector('input[name=score]:checked')?.value==='2'&&document.activeElement.value==='2'`);
 await click('input[name=score][value="4"]');
 await check('Selected stars fill up to score',`[...document.querySelectorAll('.service-rating-input .rating__star-icon')].filter(i=>i.src.includes('StateSelected')).length===4`);
 await evaluate(`document.querySelector('.feedback-form').requestSubmit()`);await wait(50);
 await check('Service local completion and chosen value',`document.querySelector('.feedback-result-value').textContent.includes('(4.0)')&&document.querySelector('.feedback-status').textContent.includes('لم تُرسل')&&document.querySelectorAll('.feedback-result input').length===0`);
 await load('dist/government/service-new-request.html');await click('[data-rating-open]');await click('input[value="5"]');
 await evaluate(`window.adapterCalls=0;PlatformFeedback.setSubmitHandler(document.querySelector('.feedback'),async payload=>{window.adapterCalls++;window.savedPayload=payload;return new Promise(resolve=>window.finishFeedback=resolve)});document.querySelector('textarea').value='تجربة';document.querySelector('form.feedback-form').requestSubmit()`);
 await check('Pending disables controls and prevents duplicate submit',`document.querySelector('.feedback-form').dispatchEvent(new Event('submit',{cancelable:true}));window.adapterCalls===1&&document.querySelector('.feedback-form').getAttribute('aria-busy')==='true'&&document.querySelector('[data-feedback-close]').disabled`);
 await evaluate(`window.finishFeedback(false)`);await wait(50);
 await check('Failure keeps input and permits retry',`!document.querySelector('.feedback-error').hidden&&!document.querySelector('.feedback-form').hidden&&document.querySelector('textarea').value==='تجربة'&&!document.querySelector('[type=submit]').disabled`);
 await evaluate(`PlatformFeedback.setSubmitHandler(document.querySelector('.feedback'),async p=>{window.savedPayload=p;return true});document.querySelector('.feedback-form').requestSubmit()`);await wait(50);
 await check('Confirmed adapter success and subject',`document.querySelector('.feedback-status').textContent==='تم إرسال ردك بنجاح!'&&window.savedPayload.score===5&&window.savedPayload.subject==='new-request'&&window.savedPayload.comment==='تجربة'`);
 for(const name of ['page-feedback','service-rating']) {
  await load('components/'+name+'/showcases/index.html',430);
  await check(`${name} multiple instances valid`, `[...document.querySelectorAll('[id]')].length===new Set([...document.querySelectorAll('[id]')].map(e=>e.id)).size&&document.querySelectorAll('[data-feedback-component]').length===2&&[...document.images].every(i=>i.complete&&i.naturalWidth>0)`);
  await click(name==='page-feedback'?'[data-feedback=yes]':'[data-rating-open]');
  await check(`${name} instances isolated`,`document.querySelectorAll('.feedback-form:not([hidden])').length===1&&document.querySelectorAll('.feedback-form')[1].hidden`);
 }
 await send('Emulation.setScriptExecutionDisabled',{value:true});
 await load('dist/government/about.html',320);await check('No JS feedback explains availability',`document.querySelector('[data-feedback=yes]').hidden&&document.querySelector('noscript').textContent.includes('JavaScript')&&document.documentElement.scrollWidth<=innerWidth`);
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
