from pathlib import Path
import re

ROOT = Path("WebKitty")


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, content):
    path.write_text(content, encoding="utf-8")


def replace_once(path, old, new, marker):
    content = read(path)
    if marker in content or new in content:
        print("Already applied:", marker)
        return
    if old not in content:
        raise SystemExit("Expected source anchor missing in %s: %s" % (path, marker))
    write(path, content.replace(old, new, 1))
    print("Applied:", marker)


# 1) WebKitty main page: default JOSDANY92 theme and NEON visual layer.
index = ROOT / "index.html"
content = read(index)
content = content.replace('<title>WebKitty</title>', '<title>WebKitty · JOSDANY92 Neon Edition</title>', 1)
theme_anchor = """                        <p id="catppuccinoColor">Catppuccino</p>
                    </label>"""
theme_replacement = theme_anchor + """
                    <label class="flex items-center text-white/80">
                        <input type="radio" name="colorTheme" value="josdany92-neon" onchange="setTheme(this.value);">
                        <p>JOSDANY92 Neon</p>
                    </label>"""
if 'value="josdany92-neon"' not in content and theme_anchor in content:
    content = content.replace(theme_anchor, theme_replacement, 1)
content = re.sub(
    r"(var savedTheme = localStorage\.getItem\('theme'\) \|\| )\"[^\"]+\";",
    r'\1"compact";',
    content,
    count=1
)
content = re.sub(
    r"(var savedColor = localStorage\.getItem\('color'\) \|\| )\"[^\"]+\";",
    r'\1"josdany92-neon";',
    content,
    count=1
)
if "isJOSDANY92Pages" not in content:
    redirect_anchor = """        var isCurrentHTTPS = window.location.protocol === 'https:';
        if (isThisPS4 && goToHttps && !isLocalServer && isCurrentHTTPS) {"""
    redirect_replacement = """        var isCurrentHTTPS = window.location.protocol === 'https:';
        // Keep GitHub Pages on the JOSDANY92 repository.
        var isJOSDANY92Pages = window.location.hostname.indexOf('github.io') !== -1;
        if (isThisPS4 && goToHttps && !isLocalServer && isCurrentHTTPS && !isJOSDANY92Pages) {"""
    if redirect_anchor not in content:
        raise SystemExit("index.html redirect anchor missing")
    content = content.replace(redirect_anchor, redirect_replacement, 1)

anchor = '    <script src="./includes/js/utilities.js"></script>'
insertion = anchor + '\n    <link rel="stylesheet" href="./includes/css/neon-exploit-loader.css">\n    <script src="./includes/js/neon-exploit-loader.js"></script>'
if 'includes/css/neon-exploit-loader.css' not in content:
    if anchor not in content:
        raise SystemExit("index.html utilities.js anchor missing")
    content = content.replace(anchor, insertion, 1)
if 'JOSDANY92: show NEON failure state for global errors' not in content:
    report_anchor = '    function reportGlobalError(title, details) {'
    report_replacement = report_anchor + '\n      // JOSDANY92: show NEON failure state for global errors.\n      if (window.J92NeonLoader) window.J92NeonLoader.finish("error");'
    if report_anchor not in content:
        raise SystemExit("index.html reportGlobalError anchor missing")
    content = content.replace(report_anchor, report_replacement, 1)
write(index, content)


# 2) Shared logging and success callback. Recognize the selected GoldHEN 2.4b18 revision.
utilities = ROOT / "includes/js/utilities.js"
replace_once(
    utilities,
    '    consoleEl.appendChild(span);',
    '''    consoleEl.appendChild(span);
    // JOSDANY92: drive the red failure animation from explicit error log entries.
    if (color === 'red') {
        if (typeof user !== 'undefined') user.blockJailbreak = false;
        if (window.J92NeonLoader) window.J92NeonLoader.finish('error');
    }''',
    'JOSDANY92: drive the red failure animation'
)
replace_once(
    utilities,
    '// Called by exploit implementations after a successful jailbreak.\nfunction jailbreakSuccess(statusMessage) {',
    '''// Report the state when a second activation is blocked.
function jailbreakAlreadyActive(goldhenReady) {
    if (typeof user !== 'undefined') user.blockJailbreak = false;
    if (window.J92NeonLoader && window.J92NeonLoader.alreadyActive) {
        window.J92NeonLoader.alreadyActive(!!goldhenReady);
    }
    var message = goldhenReady
        ? 'GoldHEN ya está activado. No se repetirá el exploit ni la carga.'
        : 'El jailbreak del kernel ya está activo. GoldHEN no quedó confirmado; no se repetirá la cadena.';
    if (typeof ui !== 'undefined' && ui.exploitState) {
        ui.exploitState.textContent = message;
    } else {
        var stateEl = document.getElementById('state');
        if (stateEl) stateEl.textContent = message;
    }
}

// Called by exploit implementations after a successful jailbreak.
function jailbreakSuccess(statusMessage) {
    if (typeof user !== 'undefined') user.blockJailbreak = false;
    var j92IsGoldHEN = false;
    var j92PayloadPath = '';
    try {
        j92PayloadPath = storage.session.getString('payload_path', '');
        var j92GoldHENVersionMatch = j92PayloadPath.match(/goldhen_v(2\.4b18\.\d+)\.bin$/i);
        j92IsGoldHEN = typeof user !== 'undefined'
            && user.currentJbFlavor === 'GoldHEN'
            && !!j92GoldHENVersionMatch;
        if (j92IsGoldHEN) {
            storage.session.set('j92GoldHENActive', true);
            localStorage.setItem('j92-goldhen-last-success', JSON.stringify({
                result: 'WebKitty reported GoldHEN payload completion',
                version: j92GoldHENVersionMatch[1],
                firmware: user.ps4Fw || getPs4FwVersion(),
                exploitChain: user.exploitChain,
                payload: j92PayloadPath,
                timestamp: Date.now()
            }));
        }
    } catch (e) {
        console.warn('JOSDANY92 GoldHEN success marker could not be saved:', e);
    }
    if (window.J92NeonLoader) {
        window.J92NeonLoader.finish(j92IsGoldHEN ? 'goldhen' : 'success');
    }''',
    'jailbreakAlreadyActive(goldhenReady)'
)


# 3) Prevent a second run before userland starts; respect the real retry switch.
jailbreak = ROOT / "includes/js/jailbreak.js"
replace_once(
    jailbreak,
    'async function jailbreak() {\n  if (!isPS4Console() && !devMode) return;',
    '''async function jailbreak() {
  if (storage.session.getBoolean('j92GoldHENActive', false)) {
    jailbreakAlreadyActive(true);
    return;
  }
  if (!isPS4Console() && !devMode) return;''',
    'j92GoldHENActive guard in jailbreak()'
)
replace_once(
    jailbreak,
    '  // Make it retry until success\n  storage.session.set(\'autoJbRetry\', true);',
    '''  // JOSDANY92: honor the persistent ON/OFF retry preference (OFF by default).
  storage.session.set('autoJbRetry', storage.getBoolean('autoJbRetry', false));''',
    'JOSDANY92 retry preference in jailbreak()'
)
replace_once(
    jailbreak,
    "  if (typeof handler === 'function') {\n    handler();",
    """  if (typeof handler === 'function') {
    var runResult = handler();
    if (runResult && typeof runResult.catch === 'function') {
      runResult.catch(function (error) { log(error, "red"); });
    }""",
    'catch asynchronous exploit handler failures'
)
replace_once(
    jailbreak,
    '  if (!isPS4Console() && !devMode) return;\n\n  // clear terminal',
    '''  if (!isPS4Console() && !devMode) return;

  // JOSDANY92: hide retry/result overlay before every new exploit attempt.
  if (window.J92NeonLoader) window.J92NeonLoader.start();

  // clear terminal''',
    'hide result overlay when a new exploit attempt starts'
)


# 4) Both launch controls check the success marker before setting the click lock.
events = ROOT / "includes/js/events.js"
events_source = read(events)
click_anchor = '    if (user.blockJailbreak) return;'
click_guard = """    // JOSDANY92: j92GoldHENActive click guard.\n    if (storage.session.getBoolean('j92GoldHENActive', false)) {
        jailbreakAlreadyActive(true);
        return;
    }
    if (user.blockJailbreak) return;"""
if 'j92GoldHENActive click guard' not in events_source:
    if events_source.count(click_anchor) != 2:
        raise SystemExit("Expected both WebKitty launch controls before patching events.js")
    events_source = events_source.replace(click_anchor, click_guard, 2)
    write(events, events_source)
    print("Applied GoldHEN guard to both launch controls.")

# Start the NEON overlay only when the user explicitly launches the exploit.
# Keep this in the patch source so upstream synchronization cannot erase it.
if 'JOSDANY92: start NEON animation' not in events_source:
    launch_anchor = "    user.blockJailbreak = true;" + chr(10) + "    chooseHEN();"
    if events_source.count(launch_anchor) != 2:
        raise SystemExit("Expected both launch handlers before adding NEON start hook")
    launch_replacement = "    user.blockJailbreak = true;" + chr(10) + "    // JOSDANY92: start NEON animation" + chr(10) + "    if (window.J92NeonLoader) window.J92NeonLoader.start();" + chr(10) + "    chooseHEN();"
    events_source = events_source.replace(launch_anchor, launch_replacement, 2)
    write(events, events_source)
    print("Applied NEON start hook to both launch controls.")

# 5) Automatic retry is a real opt-in switch. Toggling it never starts an exploit.
retry = ROOT / "includes/js/autoJbRetry.js"
replace_once(
    retry,
    '''function setAutoJbRetry(checked) {
    storage.set('autoJbRetry', checked);
    storage.session.set('autoJbRetry', checked);

    if (!checked) return;
    if (confirm(window.lang.autoJbRetryConfirm)) jailbreak();
}''',
    '''function setAutoJbRetry(checked) {
    storage.set('autoJbRetry', checked);
    storage.session.set('autoJbRetry', checked);

    if (!checked) {
        if (autoJbInterval) {
            clearInterval(autoJbInterval);
            autoJbInterval = null;
        }
        if (window.J92NeonLoader) window.J92NeonLoader.stopRetry();
        if (ui.stopAutoJbBtn) toggleVisibility(ui.stopAutoJbBtn.id, false);
    }
    // Enabling the switch only arms retries after a recoverable failed attempt.
    // It never launches a second exploit immediately when the user changes the setting.
}''',
    'JOSDANY92 non-launching retry switch'
)
replace_once(
    retry,
    "storage.getBoolean('autoJbRetry', true)",
    "storage.getBoolean('autoJbRetry', false)",
    'auto retry defaults OFF'
)
replace_once(
    retry,
    "if (timer <= 0 && storage.session.getBoolean('autoJbRetry', true)){",
    "if (timer <= 0 && (permanentJb || storage.session.getBoolean('autoJbRetry', false))){",
    'zero-delay auto jailbreak respects retry mode'
)
replace_once(
    retry,
    '            clearInterval(autoJbInterval);\n            jailbreak();',
    '            clearInterval(autoJbInterval);\n            autoJbInterval = null;\n            jailbreak();',
    'clear retry interval before execution'
)
replace_once(
    retry,
    '    // paste this again so it displays immediately on page load',
    '''    // JOSDANY92: show the retry state only during an automatic retry countdown.
    if (!permanentJb && window.J92NeonLoader) window.J92NeonLoader.retry(timer);

    // paste this again so it displays immediately on page load''',
    'show automatic retry countdown in NEON layer'
)
replace_once(
    retry,
    '        timer--;\n        if (ui.clickToStartText) {',
    '''        timer--;
        if (!permanentJb && window.J92NeonLoader && window.J92NeonLoader.updateRetry) {
            window.J92NeonLoader.updateRetry(timer);
        }
        if (ui.clickToStartText) {''',
    'update NEON retry countdown each second'
)


replace_once(
    ROOT / "includes/js/languages/es.js",
    '"autoJbRetryText": "Reintentar Jailbreak",',
    '"autoJbRetryText": "Reintentos automáticos",',
    'Spanish retry toggle label'
)
replace_once(
    ROOT / "includes/js/languages/en.js",
    '"autoJbRetryText": "Auto-Retry Jailbreak",',
    '"autoJbRetryText": "Automatic retries",',
    'English retry toggle label'
)


# 6) Keep the generic Wobkot toast suppressed. A session callback marker is
# specific to this GoldHEN payload; port 9090 is a generic Payload Loader probe.
kernel = ROOT / "src/wobkot/kernel.js"
kernel_source = read(kernel)
kernel_source = kernel_source.replace("    notify('Jailbroken !!');", "    // JOSDANY92: GoldHEN supplies its own notification; suppress generic Wobkot toast.")
old_kernel = '''async function kernel_main() {
  logger.info('===KERNEL===');

  await exploit();

  find_all_proc();

  // Avoid reapplying if already done
  if (fn.setuid.invoke(0) === -1) {
    jailbreak();

    // JOSDANY92: GoldHEN supplies its own notification; suppress generic Wobkot toast.

    await post_jailbreak();
  }else {
    await load_payload();
  }
  if (typeof jailbreakSuccess == "function"){
    jailbreakSuccess();
  }

  logger.info('===END===');
}'''
new_kernel = '''async function kernel_main() {
  logger.info('===KERNEL===');

  var goldhenReady = false;
  try {
    goldhenReady = sessionStorage.getItem('j92GoldHENActive') === 'true';
  } catch (_) {}

  // Do not rerun Wobkot or reload the payload after this session confirmed GoldHEN.
  if (goldhenReady) {
    logger.info('GoldHEN already active; skipping exploit and payload reinjection.');
    if (typeof jailbreakAlreadyActive === 'function') jailbreakAlreadyActive(true);
    logger.info('===END===');
    return;
  }

  // Secondary guard for an already-elevated process without a GoldHEN success marker.
  if (fn.setuid.invoke(0) !== -1) {
    logger.info('Kernel jailbreak already active; GoldHEN not confirmed in this session.');
    if (typeof jailbreakAlreadyActive === 'function') jailbreakAlreadyActive(false);
    logger.info('===END===');
    return;
  }

  await exploit();
  find_all_proc();

  if (fn.setuid.invoke(0) === -1) {
    jailbreak();
    // GoldHEN's own payload notification is preserved; generic Wobkot toast is omitted.
    await post_jailbreak();
  } else {
    await load_payload();
  }

  if (typeof jailbreakSuccess === 'function') jailbreakSuccess();
  logger.info('===END===');
}'''
if old_kernel in kernel_source:
    kernel_source = kernel_source.replace(old_kernel, new_kernel, 1)
elif new_kernel not in kernel_source:
    raise SystemExit("Expected Wobkot kernel_main anchor missing; refusing to patch.")
if "notify('Jailbroken !!')" in kernel_source:
    raise SystemExit("Generic Wobkot Jailbroken toast remains.")
write(kernel, kernel_source)


# 7) Wobkot global errors must drive the red visual state.
wobkot_main = ROOT / "src/wobkot/main.js"
replace_once(
    wobkot_main,
    '''  error(msg) {
    this.log('[-]', `${msg}`);
  },''',
    '''  error(msg) {
    if (window.J92NeonLoader) window.J92NeonLoader.finish('error');
    this.log('[-]', `${msg}`);
  },''',
    'Wobkot errors drive NEON failure state'
)


# 8) Barebone page gets the same animation and active-session guard.
exploit_page = ROOT / "exploit.html"
content = read(exploit_page)
if 'includes/css/neon-exploit-loader.css' not in content:
    title_anchor = '  <title>Barebone jailbreak Experience</title>'
    if title_anchor not in content:
        raise SystemExit("exploit.html title anchor missing")
    content = content.replace(title_anchor, title_anchor + '\n  <link rel="stylesheet" href="./includes/css/neon-exploit-loader.css">', 1)
if 'includes/js/neon-exploit-loader.js' not in content:
    util_anchor = '  <script src="./includes/js/utilities.js"></script>'
    if util_anchor not in content:
        raise SystemExit("exploit.html utilities.js anchor missing")
    content = content.replace(util_anchor, util_anchor + '\n  <script src="./includes/js/neon-exploit-loader.js"></script>', 1)
if "JOSDANY92: guard barebone flow against duplicate activation" not in content:
    onload_anchor = '    window.onload = function () {\n      user.ip = "127.0.0.1";'
    onload_replacement = '''    window.onload = function () {
      // JOSDANY92: guard barebone flow against duplicate activation.
      if (storage.session.getBoolean('j92GoldHENActive', false)) {
        jailbreakAlreadyActive(true);
        return;
      }
      if (window.J92NeonLoader) window.J92NeonLoader.start();
      user.ip = "127.0.0.1";'''
    if onload_anchor not in content:
        raise SystemExit("exploit.html onload anchor missing")
    content = content.replace(onload_anchor, onload_replacement, 1)
write(exploit_page, content)
replace_once(
    exploit_page,
    '    function reportGlobalError(title, details) {\n',
    '''    function reportGlobalError(title, details) {
      // JOSDANY92: Barebone errors must reach the visible status layer.
      if (window.J92NeonLoader) window.J92NeonLoader.finish('error');
''',
    'Barebone global errors drive NEON failure state'
)
replace_once(
    exploit_page,
    '      if (color) span.style.color = color;\n      consoleElement.appendChild(span);\n    }',
    '''      if (color) span.style.color = color;
      consoleElement.appendChild(span);
      if (color === 'red' && window.J92NeonLoader) window.J92NeonLoader.finish('error');
    }''',
    'Barebone red log entries drive NEON failure state'
)


# 9) Cache custom theme and animation assets in every firmware manifest.
manifest_dir = ROOT / "includes/caches/manifest"
assets = [
    "../../../includes/css/colors/josdany92-neon.css",
    "../../../includes/css/neon-exploit-loader.css",
    "../../../includes/js/neon-exploit-loader.js",
]
for manifest in manifest_dir.glob("*.manifest"):
    if manifest.name == "cachePayloads.manifest":
        continue
    content = read(manifest)
    if "NETWORK:" not in content:
        raise SystemExit("Manifest lacks NETWORK section: %s" % manifest)
    missing = [asset for asset in assets if asset not in content]
    if missing:
        content = content.replace("NETWORK:", "\n".join(missing) + "\n\nNETWORK:", 1)
        version_match = re.search(r"(?m)^# v([0-9]+)(?:\.([0-9]+))?$", content)
        if not version_match:
            raise SystemExit("Manifest version marker missing: %s" % manifest)
        major = int(version_match.group(1))
        minor = version_match.group(2)
        if manifest.name == "12xx.manifest":
            # v9 was already deployed; force v10 so PS4 12.00 refreshes the changed assets.
            next_version = str(max(major + 1, 10)) if minor is None else "%s.%s" % (major, max(int(minor) + 1, 10))
        elif minor is not None:
            next_version = "%s.%s" % (major, int(minor) + 1)
        else:
            next_version = str(major + 1)
        content = content[:version_match.start()] + "# v" + next_version + content[version_match.end():]
        write(manifest, content)
        print("Added JOSDANY92 assets and bumped cache version to v%s in %s" % (next_version, manifest.name))


print("JOSDANY92 WebKitty patches applied and verified.")
