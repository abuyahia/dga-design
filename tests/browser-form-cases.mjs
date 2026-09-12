import path from 'node:path';
import {pathToFileURL} from 'node:url';

export async function runForm({send,evaluate,wait,root}) {
  const results=[];
  const url=pathToFileURL(path.join(root,'dist/government/form.html')).href;
  for(const direction of ['rtl','ltr']) for(const width of [320,430,768,1440]) {
    await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
    await send('Page.navigate',{url});await wait(100);
    await evaluate(`document.documentElement.dir=${JSON.stringify(direction)}`);
    const data=await evaluate(`(()=>{
      const compact=document.querySelector('.progress-indicator__compact');
      const steps=document.querySelector('.progress-indicator__steps');
      const row=document.querySelector('.form-template__row');
      const layout=document.querySelector('.form-page__layout');
      const main=document.querySelector('.form-page__main').getBoundingClientRect();
      const progress=document.querySelector('.progress-indicator').getBoundingClientRect();
      return {
        fits:document.documentElement.scrollWidth<=innerWidth,
        h1:document.querySelectorAll('h1').length===1,
        rows:document.querySelectorAll('[data-field-variant]').length,
        fields:document.querySelectorAll('.form-template .text-input').length,
        disabled:document.querySelectorAll('.form-template input:disabled').length,
        errors:document.querySelectorAll('.form-template input[aria-invalid=true][aria-describedby]').length,
        rowColumns:getComputedStyle(row).gridTemplateColumns.split(' ').length,
        layoutColumns:getComputedStyle(layout).gridTemplateColumns.split(' ').length,
        compactVisible:getComputedStyle(compact).display!=='none',
        stepsVisible:getComputedStyle(steps).display!=='none',
        sideCorrect:${JSON.stringify(direction)}==='rtl'?progress.right<=main.left:progress.left>=main.right
      };
    })()`);
    const mobile=width<768;
    results.push({name:`layout ${direction} ${width}`,details:data,pass:data.fits&&data.h1&&data.rows===7&&data.fields===14&&data.disabled===2&&data.errors===2&&data.rowColumns===(mobile?1:2)&&data.layoutColumns===(mobile?1:2)&&data.compactVisible===mobile&&data.stepsVisible!==mobile&&(mobile||data.sideCorrect)});
  }
  await send('Emulation.setDeviceMetricsOverride',{width:430,height:1000,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url});await wait(100);
  await evaluate(`document.querySelector('[data-form-next]').click()`);
  results.push({name:'next updates current step',pass:await evaluate(`document.querySelector('[data-progress-step="3"]').getAttribute('aria-current')==='step'&&document.querySelector('[data-progress-current]').textContent==='3'&&document.querySelector('[data-form-next]').disabled&&document.querySelector('[data-form-step-status]').textContent.includes('3 من 3')`)});
  await evaluate(`document.querySelector('[data-form-previous]').click();document.querySelector('[data-form-previous]').click()`);
  results.push({name:'previous reaches first step',pass:await evaluate(`document.querySelector('[data-progress-step="1"]').getAttribute('aria-current')==='step'&&document.querySelector('[data-form-previous]').disabled&&document.querySelectorAll('[aria-current="step"]').length===1`)});
  await send('Emulation.setScriptExecutionDisabled',{value:true});
  await send('Page.navigate',{url});await wait(50);
  results.push({name:'no JavaScript retains content and initial progress',pass:await evaluate(`document.querySelectorAll('.form-template input').length===14&&document.querySelector('[data-progress-step="2"]').getAttribute('aria-current')==='step'&&document.querySelectorAll('h1').length===1`)});
  await send('Emulation.setScriptExecutionDisabled',{value:false});
  return results;
}
