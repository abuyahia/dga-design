/* Generic horizontal tabs. Routes and page-specific headings belong to consumers. */
(() => {
  const mounted = new WeakMap();
  function mount(root, {onSelect = () => {}} = {}) {
    if (mounted.has(root)) return mounted.get(root);
    const list = root.querySelector('.tab-list');
    const buttons = [...list.querySelectorAll('button')];
    const panels = buttons.map(button => root.querySelector('#' + button.dataset.panel));
    if (!buttons.length || panels.some(panel => !panel)) return null;
    list.hidden = false;
    list.setAttribute('role', 'tablist');
    buttons.forEach((button, i) => {
      button.setAttribute('role', 'tab');
      button.setAttribute('aria-controls', panels[i].id);
      panels[i].setAttribute('role', 'tabpanel');
      panels[i].setAttribute('aria-labelledby', button.id);
      panels[i].tabIndex = 0;
    });
    const select = (index, focus = false) => {
      buttons.forEach((button, i) => {
        button.setAttribute('aria-selected', String(i === index));
        button.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) buttons[index].focus();
    };
    const activate = (index, focus = false) => { select(index, focus); onSelect(panels[index], index); };
    buttons.forEach((button, i) => {
      button.addEventListener('click', () => activate(i));
      button.addEventListener('keydown', event => {
        let next = i;
        const rtl = getComputedStyle(root).direction === 'rtl';
        if (event.key === 'ArrowRight') next = (i + (rtl ? -1 : 1) + buttons.length) % buttons.length;
        else if (event.key === 'ArrowLeft') next = (i + (rtl ? 1 : -1) + buttons.length) % buttons.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = buttons.length - 1;
        else return;
        event.preventDefault();
        activate(next, true);
      });
    });
    const instance = {select, panels};
    mounted.set(root, instance);
    select(0);
    return instance;
  }
  window.PlatformTabs = {mount};
})();
