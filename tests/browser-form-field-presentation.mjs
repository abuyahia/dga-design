// Focused F10 computed-style comparison; Node 22+, no package dependency.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const before = path.resolve(process.argv[2]);
const after = path.resolve(process.argv[3]);
const output = process.argv[4] || '/tmp/f10-browser.json';
const port = process.argv[5] || '9342';
const target = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: 'PUT'})).json();
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
let sequence = 0;
const pending = new Map();
const loaded = new Set();
socket.onmessage = event => {
  const message = JSON.parse(event.data);
  if (message.method === 'Page.lifecycleEvent' && message.params.name === 'load') loaded.add(message.params.loaderId);
  if (!message.id) return;
  const request = pending.get(message.id);
  pending.delete(message.id);
  message.error ? request.reject(new Error(JSON.stringify(message.error))) : request.resolve(message.result);
};
const raw = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++sequence;
  pending.set(id, {resolve, reject});
  socket.send(JSON.stringify({id, method, params}));
});
async function send(method, params = {}) {
  const result = await raw(method, params);
  if (method === 'Page.navigate') {
    const deadline = Date.now() + 15000;
    while (result.loaderId && !loaded.has(result.loaderId)) {
      if (Date.now() > deadline) throw new Error('Page load timeout');
      await new Promise(resolve => setTimeout(resolve, 20));
    }
    await raw('Runtime.evaluate', {expression: 'document.fonts.ready.then(() => true)', awaitPromise: true});
  }
  return result;
}
async function evaluate(expression) {
  const result = await raw('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
async function snapshot(root, page) {
  await send('Page.navigate', {url: pathToFileURL(path.join(root, page)).href});
  return evaluate(`(() => {
    const label = document.querySelector('.text-input__label');
    const marker = label.querySelector('[aria-hidden="true"]');
    const style = element => getComputedStyle(element);
    const result = {
      fits: document.documentElement.scrollWidth <= innerWidth,
      stylesLoaded: [...document.querySelectorAll('link[rel=stylesheet]')].every(link => link.sheet),
      labelsAssociated: [...document.querySelectorAll('label[for]')].every(item => document.getElementById(item.htmlFor)),
      label: [style(label).fontSize, style(label).fontWeight, style(label).lineHeight],
      marker: marker ? style(marker).color : null,
      markerText: marker?.textContent,
      contactCSS: [...document.styleSheets].some(sheet => sheet.href?.includes('templates/contact/contact.css')),
    };
    const affix = document.querySelector('.input-affix');
    if (affix) {
      const field = affix.closest('.text-input__field');
      result.affix = [style(affix).height, style(affix).alignSelf, style(affix).flexGrow,
        style(affix).flexShrink, style(affix).borderRadius, style(field).height];
    }
    const upload = document.querySelector('.file-upload');
    if (upload) {
      upload.classList.add('is-uploaded');
      const name = upload.querySelector('.file-item__name');
      name.textContent = 'a-very-long-file-name-that-must-wrap-without-overflowing-the-contact-column-document.pdf';
      const file = upload.querySelector('.file-upload__file');
      const item = upload.querySelector('.file-item');
      const row = upload.querySelector('.file-item__row');
      result.upload = [style(upload).minWidth, style(file).width, style(item).width,
        style(name).overflowWrap, style(name).whiteSpace, style(row).justifyContent,
        item.getBoundingClientRect().right <= upload.getBoundingClientRect().right + 0.5];
    }
    return result;
  })()`);
}

const results = [];
try {
  await send('Page.enable');
  await send('Page.setLifecycleEventsEnabled', {enabled: true});
  await send('Network.enable');
  await send('Network.setBlockedURLs', {urls: ['http://*', 'https://*']});
  await send('Emulation.setDeviceMetricsOverride', {width: 430, height: 1000, deviceScaleFactor: 1, mobile: false});
  for (const page of ['contact.html', 'form.html']) {
    const oldState = await snapshot(before, page);
    const newState = await snapshot(after, page);
    const stable = JSON.stringify({...oldState, contactCSS: undefined}) === JSON.stringify({...newState, contactCSS: undefined});
    const pass = stable && newState.fits && newState.stylesLoaded && newState.labelsAssociated &&
      newState.markerText === '*' && (page === 'contact.html' ? newState.contactCSS : !newState.contactCSS);
    results.push({page, pass, oldState, newState});
  }
  if (results.some(result => !result.pass)) process.exitCode = 1;
  console.log(JSON.stringify(results));
} finally {
  fs.writeFileSync(output, JSON.stringify(results, null, 2));
  socket.close();
}
