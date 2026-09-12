/** Explicit, idempotent enhancement. No automatic document-wide side effects. */
const mounted = new WeakMap();
export function initCore(root = document) {
  if (mounted.has(root)) return mounted.get(root);
  const cleanups = [];
  const all = selector => [...(root.matches?.(selector) ? [root] : []), ...root.querySelectorAll(selector)];
  const on = (element, name, handler, options) => {
    element.addEventListener(name, handler, options);
    cleanups.push(() => element.removeEventListener(name, handler, options));
  };
  const block = event => { event.preventDefault(); event.stopImmediatePropagation(); };
  on(root, 'click', event => {
    const control = event.target.closest?.('.btn[aria-disabled="true"], .link[aria-disabled="true"]');
    if (control && root.contains(control)) block(event);
  }, true);
  on(root, 'keydown', event => {
    if (['Enter', ' '].includes(event.key) && event.target.matches('.btn[aria-disabled="true"], .link[aria-disabled="true"]')) block(event);
  }, true);
  for (const input of all('.checkbox__input')) {
    const mixed = input.hasAttribute('data-indeterminate');
    if (mixed) input.indeterminate = true;
    const readonly = input.closest('.checkbox--readonly');
    if (readonly) {
      input.setAttribute('aria-readonly', 'true');
      if (input.hasAttribute('data-readonly-fallback')) {
        input.disabled = false;
        cleanups.push(() => { input.disabled = true; });
      }
      on(input, 'click', block, true);
      on(input, 'keydown', event => { if (event.key === ' ') block(event); }, true);
    }
    if (mixed && input.form) on(input.form, 'reset', event => {
      queueMicrotask(() => { if (!event.defaultPrevented && mounted.has(root)) input.indeterminate = true; });
    });
  }
  for (const accordion of all('.accordion')) {
    const trigger = [...accordion.querySelectorAll('.accordion__trigger')].find(el => el.closest('.accordion') === accordion);
    if (!trigger) continue;
    const id = trigger.getAttribute('aria-controls');
    const matches = [...accordion.ownerDocument.querySelectorAll('[id]')].filter(el => el.id === id);
    const panel = matches.length === 1 ? matches[0] : null;
    if (!panel?.matches('.accordion__panel') || panel.closest('.accordion') !== accordion) continue;
    const set = expanded => { trigger.setAttribute('aria-expanded', String(expanded)); panel.hidden = !expanded; };
    set(trigger.dataset.initialExpanded !== 'false');
    if (trigger.hasAttribute('data-enhancement-disabled')) trigger.disabled = false;
    on(trigger, 'click', event => {
      if (trigger.disabled || trigger.getAttribute('aria-disabled') === 'true') { block(event); return; }
      set(trigger.getAttribute('aria-expanded') !== 'true');
    });
    cleanups.push(() => {
      set(true);
      if (trigger.hasAttribute('data-enhancement-disabled')) trigger.disabled = true;
    });
  }
  const dispose = () => { cleanups.reverse().forEach(cleanup => cleanup()); mounted.delete(root); };
  mounted.set(root, dispose);
  return dispose;
}
