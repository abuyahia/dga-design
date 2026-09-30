(() => {
  function init(root = document) {
    root.querySelectorAll('[data-form-template]').forEach(section => {
      if (section.dataset.initialized) return;
      section.dataset.initialized = 'true';
      const indicator = PlatformProgressIndicator.mount(section.querySelector('[data-progress-indicator]'));
      const previous = section.querySelector('[data-form-previous]');
      const next = section.querySelector('[data-form-next]');
      const status = section.querySelector('[data-form-step-status]');
      let current = Number(section.dataset.currentStep);

      const update = value => {
        const state = indicator.update(value);
        current = state.current;
        section.dataset.currentStep = String(current);
        previous.disabled = current === 1;
        next.disabled = current === state.total;
        status.textContent = `الخطوة ${current} من ${state.total}: ${state.title}`;
      };

      previous.addEventListener('click', () => update(current - 1));
      next.addEventListener('click', () => update(current + 1));
      update(current);
    });
  }

  window.PlatformFormTemplate = { init };
  init();
})();
