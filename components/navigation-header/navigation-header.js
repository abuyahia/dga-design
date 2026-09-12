/** Root-scoped enhancement; returns an idempotent cleanup. No menu roles or focus trap. */
const mounted = new WeakMap();
export function initNavigationHeaders(scope = document) {
  const roots = [...(scope.matches?.('.nav-header') ? [scope] : []), ...scope.querySelectorAll('.nav-header')];
  const disposers = roots.map(root => {
    if (mounted.has(root)) return mounted.get(root);
    const controller = new AbortController();
    const on = (target, type, handler) => target.addEventListener(type, handler, {signal: controller.signal});
    const own = selector => [...root.querySelectorAll(selector)].filter(el => el.closest('.nav-header') === root);
    const nav = own('.nav-header__navigation')[0];
    const toggle = own('.nav-header__toggle')[0];
    if (!nav || !toggle || toggle.getAttribute('aria-controls') !== nav.id) return () => {};
    const pairs = own('.nav-header__item[aria-controls]').flatMap(trigger => {
      const matches = [...root.ownerDocument.querySelectorAll('[id]')].filter(el => el.id === trigger.getAttribute('aria-controls'));
      const panel = matches.length === 1 ? matches[0] : null;
      return panel?.matches('.nav-header__panel') && panel.closest('.nav-header') === root ? [{trigger, panel}] : [];
    });
    const mobile = matchMedia('(max-width: 960px)');
    const setPanel = (pair, open) => { pair.panel.hidden = !open; pair.trigger.setAttribute('aria-expanded', String(open)); };
    const closePanels = () => pairs.forEach(pair => setPanel(pair, false));
    const setMenu = open => { nav.dataset.collapsed = String(!open); toggle.setAttribute('aria-expanded', String(open)); if (!open) closePanels(); };
    root.dataset.enhanced = 'true'; toggle.hidden = false;
    pairs.forEach(pair => {
      if (pair.trigger.hasAttribute('data-enhancement-disabled')) pair.trigger.disabled = false;
      setPanel(pair, false);
      on(pair.trigger, 'click', () => {
        if (pair.trigger.disabled || pair.trigger.getAttribute('aria-disabled') === 'true') return;
        const open = pair.panel.hidden; closePanels(); setPanel(pair, open);
      });
    });
    setMenu(!mobile.matches);
    on(toggle, 'click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    on(root, 'keydown', event => {
      if (event.key !== 'Escape') return;
      const pair = pairs.find(pair => !pair.panel.hidden);
      if (pair) { setPanel(pair, false); pair.trigger.focus(); event.preventDefault(); }
      else if (mobile.matches && toggle.getAttribute('aria-expanded') === 'true') { setMenu(false); toggle.focus(); event.preventDefault(); }
    });
    on(root.ownerDocument, 'click', event => { if (!root.contains(event.target)) { closePanels(); if (mobile.matches) setMenu(false); } });
    on(root, 'focusout', () => queueMicrotask(() => { if (!root.contains(root.ownerDocument.activeElement)) closePanels(); }));
    on(root, 'click', event => {
      if (event.target.closest('a[href]')) {
        const panel = pairs.find(pair => pair.panel.contains(event.target));
        closePanels();
        if (mobile.matches) { setMenu(false); toggle.focus(); }
        else if (panel) panel.trigger.focus();
      }
    });
    on(mobile, 'change', () => {
      if (mobile.matches && nav.contains(root.ownerDocument.activeElement)) toggle.focus();
      closePanels(); setMenu(!mobile.matches);
    });
    const dispose = () => {
      if (!mounted.has(root)) return;
      controller.abort();
      pairs.forEach(pair => { setPanel(pair, true); if (pair.trigger.hasAttribute('data-enhancement-disabled')) pair.trigger.disabled = true; });
      toggle.hidden = true; toggle.setAttribute('aria-expanded', 'true');
      delete nav.dataset.collapsed; delete root.dataset.enhanced; mounted.delete(root);
    };
    mounted.set(root, dispose); return dispose;
  });
  return () => disposers.forEach(dispose => dispose());
}
