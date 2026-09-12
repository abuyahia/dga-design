(() => {
  function init(root = document) {
    root.querySelectorAll('[data-form-template]').forEach(section => {
      if (section.dataset.initialized) return;
      section.dataset.initialized = 'true';
      const steps = [...section.querySelectorAll('[data-progress-step]')];
      const previous = section.querySelector('[data-form-previous]');
      const next = section.querySelector('[data-form-next]');
      const currentText = section.querySelector('[data-progress-current]');
      const title = section.querySelector('[data-progress-title]');
      const description = section.querySelector('[data-progress-description]');
      const status = section.querySelector('[data-form-step-status]');
      let current = Number(section.dataset.currentStep);

      const update = value => {
        current = Math.max(1, Math.min(steps.length, value));
        section.dataset.currentStep = String(current);
        steps.forEach((step, index) => {
          const number = index + 1;
          step.classList.toggle('is-complete', number < current);
          step.classList.toggle('is-current', number === current);
          if (number === current) step.setAttribute('aria-current', 'step');
          else step.removeAttribute('aria-current');
        });
        const active = steps[current - 1];
        const source = active.querySelector('.progress-indicator__copy');
        currentText.textContent = String(current);
        title.textContent = source.querySelector('strong').textContent;
        description.textContent = source.querySelector('span').textContent;
        previous.disabled = current === 1;
        next.disabled = current === steps.length;
        status.textContent = `الخطوة ${current} من ${steps.length}: ${title.textContent}`;
      };

      previous.addEventListener('click', () => update(current - 1));
      next.addEventListener('click', () => update(current + 1));
      update(current);
    });
  }

  window.PlatformFormTemplate = { init };
  init();
})();
