(function () {
  const root = document.querySelector('[data-search-results]');
  if (!root) return;
  const form = root.querySelector('form');
  const query = root.querySelector('[name="q"]');
  const type = root.querySelector('[name="type"]');
  const records = Array.from(root.querySelectorAll('[data-search-record]'));
  const count = root.querySelector('[data-search-count]');
  const empty = root.querySelector('[data-search-empty]');

  function apply(updateUrl) {
    const text = query.value.trim().toLocaleLowerCase('ar');
    const selected = type.value;
    let visible = 0;
    records.forEach((record) => {
      const matches = (!text || record.dataset.search.includes(text)) && (!selected || record.dataset.type === selected);
      record.hidden = !matches;
      if (matches) visible += 1;
    });
    count.textContent = String(visible);
    empty.hidden = visible !== 0;
    if (updateUrl && window.history && window.history.replaceState) {
      const params = new URLSearchParams();
      if (query.value.trim()) params.set('q', query.value.trim());
      if (selected) params.set('type', selected);
      window.history.replaceState({}, '', 'search.html' + (params.toString() ? '?' + params : ''));
    }
  }

  const params = new URLSearchParams(window.location.search);
  query.value = params.get('q') || '';
  type.value = params.get('type') || '';
  form.addEventListener('submit', (event) => { event.preventDefault(); apply(true); });
  query.addEventListener('input', () => apply(false));
  type.addEventListener('change', () => apply(true));
  apply(false);
}());
