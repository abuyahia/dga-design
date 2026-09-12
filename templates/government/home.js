/* Progressive enhancement of the static home template. No third-party runtime. */
(() => {
  const search = document.querySelector('.site-search');
  const openSearch = document.querySelector('.site-search-trigger');
  const input = document.querySelector('#site-search-input');
  const clear = document.querySelector('[data-search-clear]');
  const entries = [...document.querySelectorAll('#search-results li')];
  const normalize = text => text.normalize('NFKC').replace(/[\u064B-\u065F\u0670]/g, '').trim().toLocaleLowerCase();
  const filter = () => {
    const query = normalize(input.value);
    entries.forEach(item => { item.hidden = !normalize(item.textContent).includes(query); });
    clear.hidden = !input.value;
    document.querySelector('[data-search-status]').textContent = entries.some(item => !item.hidden) ? `${entries.filter(item => !item.hidden).length} خدمات متاحة` : 'لا توجد خدمات مطابقة. جرّب كلمة أخرى.';
  };
  openSearch.hidden = false;
  openSearch.addEventListener('click', () => { search.showModal(); openSearch.setAttribute('aria-expanded', 'true'); openSearch.dataset.selected = 'true'; filter(); input.focus(); });
  document.querySelector('[data-search-close]').addEventListener('click', () => search.close());
  search.addEventListener('close', () => { openSearch.setAttribute('aria-expanded', 'false'); openSearch.dataset.selected = 'false'; openSearch.focus(); });
  input.addEventListener('input', filter);
  clear.addEventListener('click', () => { input.value = ''; filter(); input.focus(); });

  document.querySelectorAll('.home-hero__dots').forEach(group => {
    group.hidden = false;
    group.addEventListener('click', event => {
      const dot = event.target.closest('button');
      if (!dot) return;
      group.querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(button === dot)));
      document.querySelector('#page-title').textContent = dot.dataset.title;
      document.querySelector('.home-hero__description').textContent = dot.dataset.description;
    });
  });
  document.querySelectorAll('[data-carousel]').forEach(root => {
    const track = root.querySelector('.home-carousel');
    const controls = root.querySelector('.carousel-controls');
    const cards = [...track.children];
    if (!cards.length) return;
    const prev = root.querySelector('[data-prev]');
    const next = root.querySelector('[data-next]');
    controls.hidden = false;
    const current = () => {
      const rect = track.getBoundingClientRect();
      const rtl = getComputedStyle(track).direction === 'rtl';
      const distances = cards.map(card => Math.abs((rtl ? card.getBoundingClientRect().right - rect.right : card.getBoundingClientRect().left - rect.left)));
      return distances.indexOf(Math.min(...distances));
    };
    const update = () => {
      const index = current();
      prev.disabled = Math.abs(track.scrollLeft) < 2;
      next.disabled = Math.abs(track.scrollLeft) >= track.scrollWidth - track.clientWidth - 2;
      root.querySelector('[data-position]').textContent = `${index + 1} / ${cards.length}`;
    };
    const move = delta => {
      const card = cards[Math.max(0, Math.min(cards.length - 1, current() + delta))];
      const rtl = getComputedStyle(track).direction === 'rtl';
      const gap = rtl ? card.getBoundingClientRect().right - track.getBoundingClientRect().right : card.getBoundingClientRect().left - track.getBoundingClientRect().left;
      track.scrollBy({left: gap, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    };
    prev.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    track.addEventListener('scroll', update, {passive: true});
    new ResizeObserver(update).observe(track);
    update();
  });
})();
