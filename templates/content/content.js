(function () {
  for (const toc of document.querySelectorAll('[data-table-of-contents]')) {
    const links = [...toc.querySelectorAll('.table-of-contents__link')];
    const entries = links.map(link => ({link, section: document.getElementById(link.hash.slice(1))})).filter(entry => entry.section);
    if (!entries.length) continue;

    const setActive = link => {
      for (const entry of entries) {
        if (entry.link === link) entry.link.setAttribute('aria-current', 'location');
        else entry.link.removeAttribute('aria-current');
      }
    };

    for (const entry of entries) entry.link.addEventListener('click', () => setActive(entry.link));

    let scheduled = false;
    const update = () => {
      scheduled = false;
      const active = entries.reduce((current, entry) => entry.section.getBoundingClientRect().top <= 160 ? entry : current, entries[0]);
      setActive(active.link);
    };
    const requestUpdate = () => {
      if (scheduled) return;
      scheduled = true;
      requestAnimationFrame(update);
    };

    addEventListener('scroll', requestUpdate, {passive: true});
    addEventListener('hashchange', () => {
      const match = entries.find(entry => entry.link.hash === location.hash);
      if (match) setActive(match.link);
    });
    update();
  }
})();
