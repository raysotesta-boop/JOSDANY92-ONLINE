const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

class FakeElement {
  constructor(tag) {
    this.tagName = tag;
    this.children = [];
    this.attributes = {};
    this.style = {};
    this.className = '';
    this.id = '';
    this.textContent = '';
    this.parentNode = null;
  }
  appendChild(child) {
    child.parentNode = this;
    this.children.push(child);
    return child;
  }
  removeChild(child) {
    const i = this.children.indexOf(child);
    if (i >= 0) this.children.splice(i, 1);
    child.parentNode = null;
    return child;
  }
  setAttribute(name, value) {
    this.attributes[name] = String(value);
    if (name === 'id') this.id = String(value);
  }
  get firstChild() { return this.children[0] || null; }
}

function makeDocument() {
  const body = new FakeElement('body');
  return {
    body,
    readyState: 'complete',
    createElement: (tag) => new FakeElement(tag),
    createElementNS: (_ns, tag) => new FakeElement(tag),
    addEventListener() {},
    getElementById(id) {
      const walk = (el) => {
        if (el.id === id) return el;
        for (const child of el.children) {
          const found = walk(child);
          if (found) return found;
        }
        return null;
      };
      return walk(body);
    }
  };
}

function makeStorage(sessionData = {}) {
  const data = { ...sessionData };
  return {
    data,
    getString(key, fallback) {
      const value = data[key];
      return value == null || value === '' ? fallback : String(value);
    },
    getBoolean(key, fallback) {
      const value = data[key];
      if (value == null || value === '') return fallback;
      return value === true || value === 'true' || value === '1';
    },
    getNumber(key, fallback) {
      const value = data[key];
      return value == null ? fallback : Number(value);
    },
    set(key, value) { data[key] = String(value); return true; },
    remove(key) { delete data[key]; return true; }
  };
}

function makeLoaderContext() {
  const document = makeDocument();
  const session = {};
  const window = { sessionStorage: {
    getItem: (key) => Object.prototype.hasOwnProperty.call(session, key) ? session[key] : null,
    setItem: (key, value) => { session[key] = String(value); },
    removeItem: (key) => { delete session[key]; }
  }};
  let timerId = 0;
  const context = {
    document, window, console,
    setTimeout: () => ++timerId,
    clearTimeout: () => {},
    Math, String, Number, parseInt
  };
  vm.createContext(context);
  vm.runInContext(read('WebKitty/includes/js/neon-exploit-loader.js'), context);
  return { context, document, window, session };
}

test('NEON loader hides on start and shows correct retry/success/error states', () => {
  const { window, document } = makeLoaderContext();
  const loader = window.J92NeonLoader;
  assert.ok(loader);
  const overlay = document.getElementById('j92-neon-exploit-loader');
  assert.equal(overlay.className, 'j92-loader-hidden');

  loader.retry(5);
  assert.equal(overlay.className, 'j92-result-retry');
  assert.match(document.getElementById('j92-result-detail').textContent, /5 SEGUNDOS/);
  loader.updateRetry(4);
  assert.match(document.getElementById('j92-result-detail').textContent, /4 SEGUNDOS/);

  loader.start();
  assert.equal(overlay.className, 'j92-loader-hidden');
  assert.equal(loader.isRunning(), true);

  loader.finish('goldhen');
  assert.equal(overlay.className, 'j92-result-goldhen');
  assert.equal(document.getElementById('j92-result-title').textContent, 'GOLDHEN ACTIVADO');

  loader.alreadyActive(true);
  assert.equal(overlay.className, 'j92-result-goldhen');
  assert.equal(document.getElementById('j92-result-title').textContent, 'GOLDHEN YA ESTÁ ACTIVADO');

  loader.finish('error');
  assert.equal(overlay.className, 'j92-result-error');
  assert.equal(document.getElementById('j92-result-title').textContent, 'GOLDHEN NO ACTIVADO');
});

test('GoldHEN success marker recognizes supported 2.4b18 payload revisions', () => {
  const { context, window } = makeLoaderContext();
  const storage = makeStorage({ payload_path: './includes/payloads/HEN/goldhen_v2.4b18.13.bin' });
  const local = {};
  const finished = [];
  context.storage = {
    session: storage,
    getBoolean: () => false,
    getNumber: () => 0,
    remove() {},
    set() {}
  };
  context.localStorage = {
    setItem: (key, value) => { local[key] = value; }
  };
  context.user = { currentJbFlavor: 'GoldHEN', ps4Fw: '14.02', exploitChain: 1, blockJailbreak: true };
  context.ui = { exploitState: { textContent: '' } };
  context.window.J92NeonLoader = { finish: (state) => finished.push(state) };
  context.updateJbStats = () => {};
  context.reloadAfterJb = false;
  context.getReloadAfterJbValue = () => false;
  context.getPs4FwVersion = () => '14.02';
  vm.runInContext(read('WebKitty/includes/js/utilities.js'), context);

  context.jailbreakSuccess();
  assert.equal(storage.data.j92GoldHENActive, 'true');
  assert.equal(JSON.parse(local['j92-goldhen-last-success']).version, '2.4b18.13');
  assert.deepEqual(finished, ['goldhen']);
  assert.equal(context.user.blockJailbreak, false);
});

test('PS4HEN success does not set the GoldHEN active marker', () => {
  const { context, window } = makeLoaderContext();
  const storage = makeStorage({ payload_path: './includes/payloads/HEN/PS4HEN.bin' });
  const finished = [];
  context.storage = { session: storage, getBoolean: () => false, getNumber: () => 0, remove() {}, set() {} };
  context.localStorage = { setItem() {} };
  context.user = { currentJbFlavor: 'PS4HEN', ps4Fw: '9.00', exploitChain: 1, blockJailbreak: true };
  context.ui = { exploitState: { textContent: '' } };
  context.window.J92NeonLoader = { finish: (state) => finished.push(state) };
  context.updateJbStats = () => {};
  context.reloadAfterJb = false;
  context.getReloadAfterJbValue = () => false;
  context.getPs4FwVersion = () => '9.00';
  vm.runInContext(read('WebKitty/includes/js/utilities.js'), context);

  context.jailbreakSuccess();
  assert.equal(storage.data.j92GoldHENActive, undefined);
  assert.deepEqual(finished, ['success']);
});

test('second activation is blocked before any exploit work when GoldHEN is active', async () => {
  const calls = { already: 0, start: 0, handler: 0 };
  const storage = makeStorage({ j92GoldHENActive: 'true', payload_path: './goldhen.bin' });
  const context = {
    storage: { session: storage, getBoolean: (k, d) => storage.getBoolean(k, d) },
    user: { blockJailbreak: false, exploitChain: 1 },
    devMode: false,
    window: { J92NeonLoader: { start: () => calls.start++ } },
    jailbreakAlreadyActive: () => calls.already++,
    isPS4Console: () => { throw new Error('exploit platform check must not run'); },
    EXPLOIT_CHAINS: {
      PSFREE_MODULAR: 1, PSFREE_BUNDLE: 2, BADHOIST: 3, CSSFONTFACE_NETCTRL: 4,
      CSSFONTFACE_LAPSE: 5, SLOPKIT_LAPSE: 6, SLOPKIT_NETCTRL: 7, RELAPSE: 8,
      SLOPKIT_AFTERGLOW: 9, BPF_DOUBLE_FREE: 10, WOBKOT_LAPSE: 11
    },
    EXPLOIT_HANDLERS: { 1: () => calls.handler++ },
    console
  };
  vm.createContext(context);
  vm.runInContext(read('WebKitty/includes/js/jailbreak.js'), context);
  await context.jailbreak();
  assert.deepEqual(calls, { already: 1, start: 0, handler: 0 });
});

test('new exploit attempts clear retry/result overlay before running', async () => {
  const calls = { start: 0, handler: 0 };
  const storage = makeStorage({ payload_path: './test.bin' });
  storage.getBoolean = () => false;
  const context = {
    document: { getElementById: () => null },
    storage: {
      session: storage,
      getBoolean: () => false,
      getString: (k, d) => storage.getString(k, d),
      set: () => true
    },
    user: { blockJailbreak: false, exploitChain: 99, bareboneJB: false },
    devMode: false,
    autoJbInterval: null,
    window: { J92NeonLoader: { start: () => calls.start++ } },
    isPS4Console: () => true,
    ui: { consoleElement: { textContent: '' } },
    autoJbInterval: null,
    isRtl: () => false,
    cleanUp() {},
    log() {},
    updateJbStats() {},
    EXPLOIT_CHAINS: {
      PSFREE_MODULAR: 1, PSFREE_BUNDLE: 2, BADHOIST: 3, CSSFONTFACE_NETCTRL: 4,
      CSSFONTFACE_LAPSE: 5, SLOPKIT_LAPSE: 6, SLOPKIT_NETCTRL: 7, RELAPSE: 8,
      SLOPKIT_AFTERGLOW: 9, BPF_DOUBLE_FREE: 10, WOBKOT_LAPSE: 11
    },
    EXPLOIT_HANDLERS: { 99: () => calls.handler++ },
    console
  };
  vm.createContext(context);
  vm.runInContext(read('WebKitty/includes/js/jailbreak.js'), context);
  await context.jailbreak();
  assert.deepEqual(calls, { start: 1, handler: 1 });
});

test('firmware cache manifests invalidate the changed assets for PS4 14.02 and 12.00', () => {
  const fw140 = read('WebKitty/includes/caches/manifest/140x.manifest');
  const fw12 = read('WebKitty/includes/caches/manifest/12xx.manifest');
  assert.match(fw140, /^# v\d+$/m);
  assert.match(fw12, /^# v\d+$/m);
  assert.ok(fw140.includes('../../../../j92-goldhen-success.svg'));
  assert.ok(fw12.includes('../../../../j92-goldhen-success.svg'));
  for (const manifest of [fw140, fw12]) {
    assert.ok(manifest.includes('includes/css/neon-exploit-loader.css'));
    assert.ok(manifest.includes('includes/js/neon-exploit-loader.js'));
  }
});

test('full-screen approved artwork is loaded and cached for the three result states', () => {
  const css = read('WebKitty/includes/css/neon-exploit-loader.css');
  assert.ok(css.includes("url("../../../j92-goldhen-success.svg")"));
  assert.ok(fs.existsSync(path.join(root, 'j92-goldhen-success.svg')));
  assert.ok(css.includes('♛  JOSDANY92'));
  assert.ok(css.includes('GOLDHEN NO ESTÁ CARGADO'));
  assert.ok(css.includes('REINTENTO AUTOMÁTICO'));
  const patch = read('patches/webkitty/apply-josdany92-patches.py');
  assert.ok(patch.includes('"../../../../j92-goldhen-success.svg"'));
});

test('result title and detail are explicitly visible for legacy PS4 WebKit', () => {
  const loader = read('WebKitty/includes/js/neon-exploit-loader.js');
  assert.ok(loader.includes("title.style.visibility = 'visible'"));
  assert.ok(loader.includes("detail.style.visibility = 'visible'"));
  assert.ok(loader.includes("title.style.fontSize = '56px'"));
  const css = read('WebKitty/includes/css/neon-exploit-loader.css');
  assert.match(css, /\.j92-result-title\s*\{[^}]*display:block !important/s);
  assert.match(css, /\.j92-result-detail\s*\{[^}]*visibility:visible !important/s);
});

test('legacy PS4 browser build also clears the result overlay before a new attempt', () => {
  const legacy = read('WebKitty/includes/js/jailbreak-legacy.js');
  assert.ok(legacy.includes('JOSDANY92: hide retry/result overlay before every new exploit attempt'));
  assert.doesNotThrow(() => new vm.Script(legacy, { filename: 'jailbreak-legacy.js' }));
});

test('Barebone page routes JavaScript errors and red logs to the NEON error state', () => {
  const html = read('WebKitty/exploit.html');
  assert.match(html, /Barebone errors must reach the visible status layer/);
  assert.match(html, /color === 'red' && window\.J92NeonLoader/);
});

test('all modified JavaScript entry files parse successfully', () => {
  const files = [
    'WebKitty/includes/js/jailbreak.js',
    'WebKitty/includes/js/utilities.js',
    'WebKitty/includes/js/autoJbRetry.js',
    'WebKitty/includes/js/neon-exploit-loader.js'
  ];
  for (const file of files) {
    const source = read(file);
    assert.doesNotThrow(() => new vm.Script(source, { filename: file }), file);
  }
});

test('firmware 12.00-12.02 forcibly disables automatic jailbreak and retry preferences', () => {
  const source = read('WebKitty/includes/js/autoJbRetry.js');
  const values = { autoJbRetry: 'true', autoJb: 'true' };
  const sessionValues = { autoJbRetry: 'true', autoJb: 'true' };
  const calls = { intervalsCleared: 0, retryStopped: 0 };
  const ui = { autoJbRetry: { checked: true }, autoJb: { checked: true } };
  const storage = {
    set: (key, value) => { values[key] = String(value); },
    getBoolean: (key, fallback) => values[key] == null ? fallback : values[key] === 'true',
    session: {
      set: (key, value) => { sessionValues[key] = String(value); },
      getBoolean: (key, fallback) => sessionValues[key] == null ? fallback : sessionValues[key] === 'true',
      remove: (key) => { delete sessionValues[key]; }
    }
  };
  const context = {
    window: { ps4Fw: '12.00', J92NeonLoader: { stopRetry: () => calls.retryStopped++ } },
    storage, ui, autoJbInterval: 7,
    clearInterval: () => calls.intervalsCleared++,
    isFirmwareSupported: () => true,
    document: { getElementById: () => ({ innerText: '' }) },
    jailbreak: () => { throw new Error('automatic launch must not run'); },
    getAutoJbTimer: () => 5,
    toggleVisibility() {}, console
  };
  vm.createContext(context);
  vm.runInContext(source, context);
  context.setAutoJbRetry(true);
  context.setAutoJb(true);
  context.autoJailbreak();
  assert.equal(values.autoJbRetry, 'false');
  assert.equal(values.autoJb, 'false');
  assert.equal(sessionValues.autoJbRetry, 'false');
  assert.equal(sessionValues.autoJb, 'false');
  assert.equal(ui.autoJbRetry.checked, false);
  assert.equal(ui.autoJb.checked, false);
  assert.equal(calls.intervalsCleared, 1);
  assert.equal(calls.retryStopped, 3);
  assert.ok(read('patches/webkitty/apply-josdany92-patches.py')
    .includes('Firmware 12.00-12.02 gets manual-only launches'));
});


// Keep the firmware 12.00 manual-only guard covered in the pinned-source rebuild.
