// Native <details> owns pointer and Enter/Space behavior. Escape is an enhancement.
const digitalStampInstances = new WeakMap();
export function initDigitalStamps(scope = document) {
  const roots = [...(scope.matches?.('.digital-stamp') ? [scope] : []), ...scope.querySelectorAll('.digital-stamp')];
  const cleanups = roots.map(root => {
    if (digitalStampInstances.has(root)) return digitalStampInstances.get(root);
    const onKeydown = event => {
      if (event.key !== 'Escape' || !root.open) return;
      event.preventDefault();
      root.open = false;
      root.querySelector(':scope > summary').focus();
    };
    root.addEventListener('keydown', onKeydown);
    const cleanup = () => { root.removeEventListener('keydown', onKeydown); digitalStampInstances.delete(root); };
    digitalStampInstances.set(root, cleanup);
    return cleanup;
  });
  return () => cleanups.forEach(cleanup => cleanup());
}
