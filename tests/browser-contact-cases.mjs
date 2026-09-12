import path from 'node:path';
import {pathToFileURL} from 'node:url';
export async function runContact({send,evaluate,wait,root}) {
 const results=[];
 const load=async(width=1440,dir='rtl')=>{await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url:pathToFileURL(path.join(root,'dist/government/contact.html')).href});await evaluate(`document.documentElement.dir='${dir}'`);};
 const check=async(name,code)=>results.push({name,pass:await evaluate(code)});
 const fill=()=>evaluate(`(()=>{const f=document.querySelector('#contact-form');for(const [name,value] of Object.entries({first_name:'أحمد',last_name:'علي',email:'test@example.com',phone:'٠٥٥١٢٣٤٥٦٧',message:'رسالة اختبار'}))f.elements[name].value=value;})()`);
 const attach=(name,size,type)=>evaluate(`(()=>{const f=new File([new Uint8Array(${size})],${JSON.stringify(name)},{type:${JSON.stringify(type)}}),d=new DataTransfer();d.items.add(f);document.querySelector('#contact-attachment').files=d.files;document.querySelector('#contact-attachment').dispatchEvent(new Event('change'));})()`);
 await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const dir of ['rtl','ltr'])for(const width of [320,430,768,1440]) {
  await load(width,dir);
  await check('Layout '+dir+' '+width,`(()=>{const m=document.querySelector('.contact-page__main').getBoundingClientRect(),c=document.querySelector('.contact-card').getBoundingClientRect();return document.documentElement.scrollWidth<=innerWidth&&document.querySelectorAll('h1').length===1&&[...document.images].every(i=>i.complete&&i.naturalWidth>0)&&[...document.querySelectorAll('link[rel=stylesheet]')].every(i=>i.sheet)&&(innerWidth<768?c.top>=m.bottom:Math.abs(m.width/c.width-2)<.02)&&(innerWidth!==1440||(Math.abs(c.width-416)<1&&Math.abs(m.width-832)<1))})()`);
  await check('Fields and feedback '+dir+' '+width,`document.querySelector('#contact-form fieldset').disabled===false&&document.querySelector('[data-feedback-component]').dataset.feedbackComponent==='page'&&(()=>{const a=document.querySelector('#contact-first_name').getBoundingClientRect(),b=document.querySelector('#contact-last_name').getBoundingClientRect();return ${width<768?'b.top>a.bottom':'Math.abs(a.top-b.top)<1'}})()`);
 }
 await load(430);
 await evaluate(`document.querySelector('#contact-form').requestSubmit()`);
 await check('Required error summary and focus',`!document.querySelector('.contact-error-summary').hidden&&document.querySelectorAll('.contact-error-summary li').length===5&&document.activeElement.classList.contains('contact-error-summary')&&document.querySelector('#contact-message').getAttribute('aria-invalid')==='true'`);
 await evaluate(`document.querySelector('.contact-error-summary a').click()`);
 await check('Error link focuses input',`document.activeElement.id==='contact-first_name'`);
 await fill();await evaluate(`document.querySelector('#contact-email').value='bad';document.querySelector('#contact-form').requestSubmit()`);
 await check('Invalid email state',`document.querySelector('#contact-email').getAttribute('aria-invalid')==='true'&&document.querySelector('#contact-email').closest('.text-input').classList.contains('text-input--error')`);
 await fill();await attach('bad.exe',20,'application/octet-stream');
 await check('Attachment type rejected',`!document.querySelector('#contact-attachment-error').hidden&&document.querySelector('#contact-attachment').getAttribute('aria-invalid')==='true'`);
 await attach('large.pdf',2097153,'application/pdf');
 await check('Attachment size rejected',`document.querySelector('#contact-attachment-error').textContent.includes('2 ميجابايت')`);
 await attach('empty.pdf',0,'application/pdf');
 await check('Empty attachment rejected',`document.querySelector('#contact-attachment-error').textContent.includes('فارغ')`);
 await attach('document.pdf',40,'application/pdf');
 await check('Valid attachment selected',`document.querySelector('#contact-attachment-error').hidden&&document.querySelector('.contact-upload').classList.contains('is-uploaded')&&document.querySelector('[data-contact-file-name]').textContent==='document.pdf'`);
 await evaluate(`document.querySelector('[data-contact-remove]').click()`);
 await check('Remove clears selection and restores focus',`document.querySelector('#contact-attachment').files.length===0&&!document.querySelector('.contact-upload').classList.contains('is-uploaded')&&document.activeElement.hasAttribute('data-contact-browse')`);
 await evaluate(`document.querySelector('#contact-form').requestSubmit()`);await wait(50);
 await check('Local preview is honest and clears form',`document.querySelector('[data-contact-status]').textContent.includes('لم تُرسل')&&document.querySelector('#contact-email').value===''&&document.querySelector('#contact-form fieldset').disabled===false`);
 await fill();await attach('document.pdf',40,'application/pdf');
 await evaluate(`window.contactCalls=0;PlatformContact.setSubmitHandler(document.querySelector('#contact-form'),async data=>{window.contactCalls++;window.contactPayload=data;return new Promise(resolve=>window.finishContact=resolve)});document.querySelector('#contact-form').requestSubmit()`);
 await check('Pending locks canonical control states',`document.querySelector('#contact-form').dispatchEvent(new Event('submit',{cancelable:true}));window.contactCalls===1&&document.querySelector('#contact-form').getAttribute('aria-busy')==='true'&&document.querySelector('.textarea').classList.contains('text-input--disabled')&&document.querySelector('.select-input').classList.contains('text-input--disabled')&&document.querySelector('#contact-email').matches(':disabled')`);
 await evaluate(`window.finishContact(false)`);await wait(50);
 await check('Failure preserves data and attachment',`document.querySelector('[data-contact-status]').textContent.includes('تعذر')&&document.querySelector('#contact-email').value==='test@example.com'&&document.querySelector('#contact-attachment').files.length===1&&!document.querySelector('#contact-email').matches(':disabled')`);
 await evaluate(`PlatformContact.setSubmitHandler(document.querySelector('#contact-form'),async data=>{window.contactPayload=data;return true});document.querySelector('#contact-form').requestSubmit()`);await wait(50);
 await check('Confirmed success and normalized payload',`document.querySelector('[data-contact-status]').textContent==='تم إرسال رسالتك بنجاح.'&&window.contactPayload.get('phone')==='0551234567'&&window.contactPayload.get('attachment').name==='document.pdf'`);
 await load();
 for(const id of ['contact-first_name','contact-category','contact-message']) {
  await evaluate(`document.querySelector('#${id}').focus()`);
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  await evaluate(`document.querySelector('#${id}').focus()`);
  await check('Keyboard focus '+id,`getComputedStyle(document.querySelector('#${id}').closest('.text-input__field')).outlineStyle==='solid'`);
 }
 await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
 await evaluate(`document.querySelector('#contact-category').focus()`);
 await send('Input.dispatchKeyEvent',{type:'char',text:'ا'});await wait(100);
 const nativeSelect=await evaluate(`({index:document.querySelector('#contact-category').selectedIndex,value:document.querySelector('#contact-category').value,active:document.activeElement.id})`);results.push({name:'Native select keyboard typeahead',details:nativeSelect,pass:nativeSelect.index===1});
 await send('Emulation.setScriptExecutionDisabled',{value:true});await load(320);
 await check('No JS cannot silently submit',`document.querySelector('#contact-form fieldset').disabled&&document.querySelector('#contact-form [type=submit]').disabled&&document.querySelector('.contact-form noscript').textContent.includes('JavaScript')`);
 await send('Emulation.setScriptExecutionDisabled',{value:false});
 return results;
}
