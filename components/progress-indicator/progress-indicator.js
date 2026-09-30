/* Presentation only: the consumer owns step navigation and workflow. */
(() => {
  const mounted = new WeakMap();
  function mount(root) {
    if (mounted.has(root)) return mounted.get(root);
    const steps = [...root.querySelectorAll('[data-progress-step]')];
    const currentText = root.querySelector('[data-progress-current]');
    const title = root.querySelector('[data-progress-title]');
    const description = root.querySelector('[data-progress-description]');
    const update = value => {
      const current = Math.max(1, Math.min(steps.length, value));
      steps.forEach((step, index) => {
        const number = index + 1;
        step.classList.toggle('is-complete', number < current);
        step.classList.toggle('is-current', number === current);
        if (number === current) step.setAttribute('aria-current', 'step');
        else step.removeAttribute('aria-current');
      });
      const source = steps[current - 1].querySelector('.progress-indicator__copy');
      currentText.textContent = String(current);
      title.textContent = source.querySelector('strong').textContent;
      description.textContent = source.querySelector('span').textContent;
      return {current, total: steps.length, title: title.textContent};
    };
    const instance = {update};
    mounted.set(root, instance);
    return instance;
  }
  window.PlatformProgressIndicator = {mount};
})();
