/* Component-scoped progressive enhancement. No network request without an explicit adapter. */
(() => {
 const handlers = new WeakMap();
 const assetRoot = new URL('../../components/service-rating/assets/', document.currentScript.src);
 const normal = new URL('default-imgSizeMediumStateNormalStyleBrand.svg', assetRoot).href;
 const filled = new URL('default-imgSizeMediumStateSelectedStyleBrand.svg', assetRoot).href;
 function init(root = document) {
  root.querySelectorAll('[data-feedback-component]').forEach(component => {
   if (component.dataset.initialized) return;
   component.dataset.initialized = 'true';
   const form = component.querySelector('form'), summary = component.querySelector('.feedback-summary');
   const result = component.querySelector('.feedback-result'), error = component.querySelector('.feedback-error');
   const triggers = [...component.querySelectorAll('[data-feedback], [data-rating-open]')];
   const isService = component.dataset.feedbackComponent === 'service';
   let choice = null, opener = null, pending = false;
   const showError = message => { error.hidden = false; error.textContent = message; };
   const paint = score => component.querySelectorAll('input[name=score]').forEach(input => { input.nextElementSibling.src = +input.value <= score ? filled : normal; });
   const close = () => {
    if (pending) return;
    form.hidden = true; summary.hidden = false;
    triggers.forEach(button => button.setAttribute('aria-expanded', 'false'));
    error.hidden = true;
    if (opener) opener.focus();
   };
   triggers.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
     opener = button;
     if (!isService && choice !== button.dataset.feedback) {
      form.reset(); choice = button.dataset.feedback;
     }
     triggers.forEach(trigger => { trigger.setAttribute('aria-expanded', String(trigger === button)); if (!isService) trigger.setAttribute('aria-pressed', String(trigger === button)); });
     form.hidden = false; result.hidden = true; summary.hidden = isService; error.hidden = true;
     form.querySelectorAll('[data-reason-group]').forEach(label => {
      label.hidden = label.dataset.reasonGroup !== choice;
      label.querySelector('input').disabled = label.hidden;
     });
     const target = form.querySelector(isService ? 'input[name=score]' : 'input[name=reason]:not(:disabled)');
     target.focus();
    });
   });
   component.querySelector('[data-feedback-close]').addEventListener('click', close);
   form.addEventListener('keydown', event => { if (event.key === 'Escape') { event.preventDefault(); close(); } });
   form.addEventListener('change', event => {
    error.hidden = true;
    if (event.target.name === 'score') paint(+event.target.value);
    if (event.target.name === 'reason' && form.querySelectorAll('input[name=reason]:checked:not(:disabled)').length > 2) {
     event.target.checked = false; showError('يمكنك اختيار سببين كحد أقصى.');
    }
   });
   form.addEventListener('submit', async event => {
    event.preventDefault(); if (pending) return;
    const data = new FormData(form), reasons = data.getAll('reason');
    if (!isService && (!choice || reasons.length < 1 || reasons.length > 2)) { showError('اختر سببًا واحدًا أو سببين.'); form.querySelector('input[name=reason]:not(:disabled)').focus(); return; }
    if (isService && !(+data.get('score') >= 1 && +data.get('score') <= 5)) { showError('اختر تقييمًا من 1 إلى 5.'); return; }
    const payload = {kind: component.dataset.feedbackComponent, subject: component.dataset.feedbackId, comment: data.get('comment'), ...(isService ? {score: +data.get('score')} : {useful: choice === 'yes', reasons, gender: data.get('gender')})};
    const adapter = handlers.get(component);
    pending = true; form.setAttribute('aria-busy', 'true'); error.hidden = true;
    const controls = [...component.querySelectorAll('button,input,textarea')]; const disabled = controls.map(control => control.disabled);
    controls.forEach(control => control.disabled = true);
    try {
     if (adapter && await adapter(payload) !== true) throw new Error('Submission not confirmed');
     form.hidden = true; summary.hidden = true; result.hidden = false;
     const value = result.querySelector('.feedback-result-value');
     value.textContent = isService ? `لقد قيّمت هذه الخدمة بـ (${payload.score}.0)` : 'شكرًا لمشاركتك رأيك في هذه الصفحة.';
     if (isService) {
      const stars = form.querySelector('.rating').cloneNode(true); stars.setAttribute('aria-hidden', 'true'); stars.removeAttribute('aria-describedby');
      stars.querySelectorAll('input').forEach(input => input.remove()); value.append(stars);
     }
     const status = result.querySelector('.feedback-status');
     status.textContent = adapter ? 'تم إرسال ردك بنجاح!' : 'اكتملت المعاينة محليًا؛ لم تُرسل بيانات.';
     const successIcon = document.createElement('img');
     successIcon.src = new URL('submitted-imgElements.svg', assetRoot).href;
     successIcon.alt = ''; successIcon.width = 24; successIcon.height = 24; status.prepend(successIcon);
     triggers.forEach(trigger => trigger.setAttribute('aria-expanded', 'false'));
     result.focus(); form.reset();
     component.dispatchEvent(new CustomEvent('feedback:complete', {bubbles: true, detail: {kind: payload.kind, subject: payload.subject, preview: !adapter}}));
    } catch {
     showError('تعذر إرسال التقييم. حاول مرة أخرى.');
    } finally {
     controls.forEach((control,i) => control.disabled = disabled[i]);
     pending = false; form.removeAttribute('aria-busy');
    }
   });
  });
 }
 window.PlatformFeedback = {init, setSubmitHandler(component, handler) {
  if (typeof handler !== 'function') throw new TypeError('Expected an async submission function');
  handlers.set(component, handler);
  component.querySelector('.feedback-note').textContent = 'يرجى عدم تضمين معلومات شخصية أو مالية. سيتم إرسال تعليقك وتسجيله لغرض تحسين الخدمات.';
 }};
 init();
})();
