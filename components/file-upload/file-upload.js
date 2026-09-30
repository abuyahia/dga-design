/* Single-file selection UI. Validation policy and submission remain consumer-owned. */
(() => {
  const mounted = new WeakMap();
  function mount(root, {validate = () => '', onError = () => {}} = {}) {
    if (mounted.has(root)) return mounted.get(root);
    const input = root.querySelector('input[type=file]');
    const browse = root.querySelector('[data-file-browse]');
    const remove = root.querySelector('[data-file-remove]');
    const name = root.querySelector('[data-file-name]');
    const clear = () => {
      input.value = '';
      root.classList.remove('is-uploaded');
      name.textContent = '';
      onError('');
    };
    browse.addEventListener('click', () => input.click());
    remove.addEventListener('click', () => { clear(); browse.focus(); });
    input.addEventListener('change', () => {
      const error = validate(input.files[0]);
      onError(error);
      root.classList.toggle('is-uploaded', Boolean(input.files[0]));
      name.textContent = input.files[0]?.name || '';
      root.querySelector('.file-item').classList.toggle('file-item--error', Boolean(error));
    });
    const instance = {clear};
    mounted.set(root, instance);
    return instance;
  }
  window.PlatformFileUpload = {mount};
})();
