/* Progressive enhancement: all cards and detail sections remain usable without JS. */
(() => {
 const normalize = value => value.normalize('NFKC').replace(/[\u064B-\u065F\u0670]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').trim().toLocaleLowerCase();
 document.querySelectorAll('[data-service-catalog]').forEach(root => {
  if(root.dataset.catalogInitialized)return;
  root.dataset.catalogInitialized='true';
  const form=root.querySelector('form'),input=form.querySelector('input'),filters=root.querySelector('.service-catalog__filters'),categoryWrap=root.querySelector('.service-catalog__category'),categoryInput=categoryWrap.querySelector('select'),buttons=[...filters.querySelectorAll('button')],cards=[...root.querySelectorAll('[data-service-card]')],status=root.querySelector('[data-catalog-status]'),empty=root.querySelector('[data-catalog-empty]');
  let audience='';
  const readURL=()=>{const params=new URLSearchParams(location.search);input.value=params.get('q')||'';audience=buttons.some(b=>b.dataset.audience===params.get('audience'))?params.get('audience'):'';categoryInput.value=[...categoryInput.options].some(o=>o.value===params.get('category'))?params.get('category'):'';};
  const update=(save=true)=>{
   const query=normalize(input.value);let count=0;
   for(const card of cards){card.hidden=!(normalize(card.dataset.search).includes(query)&&(!audience||card.dataset.audiences.split('|').includes(audience))&&(!categoryInput.value||card.dataset.category===categoryInput.value));if(!card.hidden)count++;}
   buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.audience===audience)));
   status.textContent=count+' خدمات من أصل '+cards.length;empty.hidden=count!==0;
   if(save){const url=new URL(location.href);if(input.value.trim())url.searchParams.set('q',input.value.trim());else url.searchParams.delete('q');if(audience)url.searchParams.set('audience',audience);else url.searchParams.delete('audience');if(categoryInput.value)url.searchParams.set('category',categoryInput.value);else url.searchParams.delete('category');history.replaceState(null,'',url);}
  };
  readURL();form.hidden=false;filters.hidden=false;categoryWrap.hidden=false;status.hidden=false;update(false);
  form.addEventListener('submit',event=>{event.preventDefault();update();});input.addEventListener('input',()=>update());
  buttons.forEach(button=>button.addEventListener('click',()=>{audience=button.dataset.audience;update();}));
  categoryInput.addEventListener('change',()=>update());
  root.querySelectorAll('[data-catalog-reset]').forEach(button=>button.addEventListener('click',()=>{input.value='';audience='';categoryInput.value='';update();input.focus();}));
  window.addEventListener('popstate',()=>{readURL();update(false);});
 });
 document.querySelectorAll('[data-service-tabs]').forEach(root=>{
  if(root.dataset.tabsIntegrated) return;
  root.dataset.tabsIntegrated='true';
  const instance=PlatformTabs.mount(root,{onSelect:panel=>history.replaceState(null,'','#'+panel.id)});
  if(!instance)return;
  const {select,panels}=instance;
  panels.forEach(panel=>panel.querySelector('h2').classList.add('sr-only'));
  const fromHash=()=>{const index=panels.findIndex(p=>'#'+p.id===location.hash);if(index>=0)select(index);};
  fromHash();window.addEventListener('hashchange',fromHash);
  document.querySelectorAll('[data-open-steps]').forEach(link=>link.addEventListener('click',()=>select(0)));
 });
})();
