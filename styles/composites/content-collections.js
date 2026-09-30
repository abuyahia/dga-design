(() => {
 document.querySelectorAll('[data-record-filter]').forEach(root => {
  const controls=root.querySelector('.record-collection__controls, .regulatory-library__controls');
  if(!controls)return;
  const records=[...root.querySelectorAll('[data-record]')],status=root.querySelector('[data-filter-status-text]'),empty=root.querySelector('[data-filter-empty]');
  const query=root.querySelector('[data-filter-query]'),kind=root.querySelector('[data-filter-kind]'),state=root.querySelector('[data-filter-status]'),topic=root.querySelector('[data-filter-topic]'),sort=root.querySelector('[data-sort]');
  const update=()=>{
   const term=(query?.value||'').trim().toLocaleLowerCase();let count=0;
   records.forEach(record=>{const shown=(!term||(record.dataset.search||record.textContent).toLocaleLowerCase().includes(term))&&(!kind?.value||record.dataset.kind===kind.value)&&(!state?.value||record.dataset.status===state.value)&&(!topic?.value||(record.dataset.topic||'').split('|').includes(topic.value));record.hidden=!shown;if(shown)count++;});
   if(sort?.value==='alpha'){const container=records[0]?.parentElement;records.slice().sort((a,b)=>a.textContent.localeCompare(b.textContent,'ar')).forEach(x=>container.append(x));}
   status.textContent=count+' نتائج من أصل '+records.length;empty.hidden=count!==0;
  };
  controls.hidden=false;status.hidden=false;
  controls.querySelectorAll('input,select').forEach(control=>control.addEventListener('input',update));
  controls.querySelector('[data-filter-reset]')?.addEventListener('click',()=>{controls.querySelectorAll('input,select').forEach(x=>x.value='');update();query?.focus();});
  update();
 });
})();
