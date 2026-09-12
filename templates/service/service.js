/* Progressive enhancement: all cards and detail sections remain usable without JS. */
(() => {
 const normalize = value => value.normalize('NFKC').replace(/[\u064B-\u065F\u0670]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').trim().toLocaleLowerCase();
 document.querySelectorAll('[data-service-catalog]').forEach(root => {
  const form=root.querySelector('form'),input=form.querySelector('input'),filters=root.querySelector('.service-catalog__filters'),buttons=[...filters.querySelectorAll('button')],cards=[...root.querySelectorAll('[data-service-card]')],status=root.querySelector('[data-catalog-status]'),empty=root.querySelector('[data-catalog-empty]');
  let audience='';
  const readURL=()=>{const params=new URLSearchParams(location.search);input.value=params.get('q')||'';audience=buttons.some(b=>b.dataset.audience===params.get('audience'))?params.get('audience'):'';};
  const update=(save=true)=>{
   const query=normalize(input.value);let count=0;
   for(const card of cards){card.hidden=!(normalize(card.dataset.search).includes(query)&&(!audience||card.dataset.audiences.split('|').includes(audience)));if(!card.hidden)count++;}
   buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.audience===audience)));
   status.textContent=count+' خدمات من أصل '+cards.length;empty.hidden=count!==0;
   if(save){const url=new URL(location.href);if(input.value.trim())url.searchParams.set('q',input.value.trim());else url.searchParams.delete('q');if(audience)url.searchParams.set('audience',audience);else url.searchParams.delete('audience');history.replaceState(null,'',url);}
  };
  readURL();form.hidden=false;filters.hidden=false;status.hidden=false;update(false);
  form.addEventListener('submit',event=>{event.preventDefault();update();});input.addEventListener('input',()=>update());
  buttons.forEach(button=>button.addEventListener('click',()=>{audience=button.dataset.audience;update();}));
  root.querySelectorAll('[data-catalog-reset]').forEach(button=>button.addEventListener('click',()=>{input.value='';audience='';update();input.focus();}));
  window.addEventListener('popstate',()=>{readURL();update(false);});
 });
 document.querySelectorAll('[data-service-tabs]').forEach(root=>{
  const list=root.querySelector('.tab-list'),buttons=[...list.querySelectorAll('button')],panels=buttons.map(button=>root.querySelector('#'+button.dataset.panel));
  list.hidden=false;list.setAttribute('role','tablist');
  buttons.forEach((button,i)=>{button.setAttribute('role','tab');button.setAttribute('aria-controls',panels[i].id);panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',button.id);panels[i].tabIndex=0;panels[i].querySelector('h2').classList.add('sr-only');});
  const select=(index,focus=false,save=false)=>{buttons.forEach((button,i)=>{button.setAttribute('aria-selected',String(i===index));button.tabIndex=i===index?0:-1;panels[i].hidden=i!==index;});if(focus)buttons[index].focus();if(save)history.replaceState(null,'','#'+panels[index].id);};
  const fromHash=()=>{const index=panels.findIndex(p=>'#'+p.id===location.hash);if(index>=0)select(index);};
  select(0);fromHash();window.addEventListener('hashchange',fromHash);
  buttons.forEach((button,i)=>{button.addEventListener('click',()=>select(i,false,true));button.addEventListener('keydown',event=>{let next=i;const rtl=getComputedStyle(root).direction==='rtl';if(event.key==='ArrowRight')next=(i+(rtl?-1:1)+buttons.length)%buttons.length;else if(event.key==='ArrowLeft')next=(i+(rtl?1:-1)+buttons.length)%buttons.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=buttons.length-1;else return;event.preventDefault();select(next,true,true);});});
  document.querySelectorAll('[data-open-steps]').forEach(link=>link.addEventListener('click',()=>select(0)));
 });
})();
