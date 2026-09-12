(() => {
 const handlers = new WeakMap();
 const digits = value => value.replace(/[٠-٩]/g,c=>String(c.charCodeAt(0)-1632)).replace(/[۰-۹]/g,c=>String(c.charCodeAt(0)-1776));
 function init(root=document) {
  root.querySelectorAll('.contact-form').forEach(form=>{
   if(form.dataset.initialized) return;
   form.dataset.initialized='true';
   const fields=form.querySelector('fieldset'), summary=form.querySelector('.contact-error-summary'), status=form.querySelector('[data-contact-status]');
   const file=form.elements.attachment, upload=file.closest('.file-upload'), submit=form.querySelector('[type=submit]');
   let pending=false;
   fields.disabled=false; submit.disabled=false; upload.removeAttribute('aria-disabled');
   const syncStates=()=>form.querySelectorAll('.text-input').forEach(w=>w.classList.toggle('text-input--disabled',w.querySelector('input,select,textarea').matches(':disabled')));
   const errorFor=(input,message)=>{
    const wrapper=input.closest('[data-field]'), error=wrapper.querySelector('.form-field-error');
    error.textContent=message;error.hidden=!message;input.setAttribute('aria-invalid',String(Boolean(message)));
    wrapper.classList.toggle('text-input--error',Boolean(message));
   };
   const attachmentError=()=>{
    const f=file.files[0];if(!f)return '';
    if(f.size>2*1024*1024)return 'حجم الملف يتجاوز 2 ميجابايت.';
    const ext=f.name.split('.').pop().toLowerCase(),types={jpg:'image/jpeg',jpeg:'image/jpeg',png:'image/png',pdf:'application/pdf'};
    if(!types[ext] || (f.type && f.type!==types[ext]))return 'اختر ملف JPG أو PNG أو PDF.';
    if(!f.size)return 'الملف فارغ. اختر ملفًا آخر.';
    return '';
   };
   const validate=input=>{
    if(input===file)return attachmentError();
    const value=input.value.trim();
    if(input.required&&!value)return 'هذا الحقل مطلوب.';
    if(input.name==='email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))return 'أدخل بريدًا إلكترونيًا صحيحًا.';
    if(input.name==='phone' && value && !/^\+?[0-9]{8,15}$/.test(digits(value).replace(/[\s()-]/g,'')))return 'أدخل رقم جوال صحيحًا من 8 إلى 15 رقمًا.';
    if(input.maxLength>0 && value.length>input.maxLength)return `الحد الأقصى ${input.maxLength} حرفًا.`;
    return '';
   };
   form.querySelector('[data-contact-browse]').addEventListener('click',()=>file.click());
   const clearFile=()=>{file.value='';upload.classList.remove('is-uploaded');form.querySelector('[data-contact-file-name]').textContent='';errorFor(file,'');};
   form.querySelector('[data-contact-remove]').addEventListener('click',()=>{clearFile();form.querySelector('[data-contact-browse]').focus();});
   file.addEventListener('change',()=>{
    const error=attachmentError();errorFor(file,error);
    upload.classList.toggle('is-uploaded',Boolean(file.files[0]));
    form.querySelector('[data-contact-file-name]').textContent=file.files[0]?.name || '';
    upload.querySelector('.file-item').classList.toggle('file-item--error',Boolean(error));
   });
   form.addEventListener('focusout',event=>{if(event.target.matches('input:not([type=file]),textarea,select'))errorFor(event.target,validate(event.target));});
   form.addEventListener('input',event=>{if(event.target.matches('input:not([type=file]),textarea,select')&&event.target.getAttribute('aria-invalid')==='true')errorFor(event.target,validate(event.target));});
   form.addEventListener('submit',async event=>{
    event.preventDefault();if(pending)return;
    summary.hidden=true;summary.querySelector('ul').replaceChildren();status.textContent='';
    const invalid=[];
    [...fields.querySelectorAll('input,textarea,select')].forEach(input=>{const error=validate(input);errorFor(input,error);if(error)invalid.push({input,error});});
    if(invalid.length){
     invalid.forEach(({input,error})=>{const li=document.createElement('li'),a=document.createElement('a');a.className='link link--inline';a.href='#'+input.id;a.textContent=input.closest('[data-field]').querySelector('label').textContent+': '+error;a.addEventListener('click',e=>{e.preventDefault();(input===file?form.querySelector('[data-contact-browse]'):input).focus();});li.append(a);summary.querySelector('ul').append(li);});
     summary.hidden=false;summary.focus();return;
    }
    const payload=new FormData(form);for(const name of ['first_name','last_name','email','subject','message'])payload.set(name,payload.get(name).trim());payload.set('phone',digits(payload.get('phone')).replace(/[\s()-]/g,''));
    if(!file.files.length)payload.delete('attachment');
    pending=true;fields.disabled=true;submit.disabled=true;form.setAttribute('aria-busy','true');upload.setAttribute('aria-disabled','true');syncStates();status.textContent='جارٍ معالجة الرسالة…';
    try {
     const handler=handlers.get(form);if(handler && await handler(payload)!==true)throw new Error('Submission not confirmed');
     status.textContent=handler?'تم إرسال رسالتك بنجاح.':'اكتملت المعاينة محليًا؛ لم تُرسل الرسالة أو المرفقات.';
     form.reset();clearFile();form.querySelectorAll('input,textarea,select').forEach(input=>errorFor(input,''));
     status.tabIndex=-1;status.focus();
    }catch{status.textContent='تعذر إرسال الرسالة. احتُفظ ببياناتك؛ يرجى المحاولة مرة أخرى.';}
    finally{pending=false;fields.disabled=false;submit.disabled=false;form.removeAttribute('aria-busy');upload.removeAttribute('aria-disabled');syncStates();}
   });
   syncStates();
  });
 }
 window.PlatformContact={init,setSubmitHandler(form,handler){if(typeof handler!=='function')throw new TypeError('Expected a submission handler');handlers.set(form,handler);form.querySelector('.contact-form__note').textContent='ستُرسل بيانات النموذج ومرفقاته إلى الجهة لمعالجة رسالتك.';}};
 init();
})();
