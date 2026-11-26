from pathlib import Path

target = Path("WebKitty/includes/js/utilities.js")
source = target.read_text(encoding="utf-8")
marker = "// JOSDANY92: record successful GoldHEN payload completion."
if marker in source:
    print("JOSDANY92 success hook already applied.")
    raise SystemExit(0)

anchor = "function jailbreakSuccess(statusMessage) {\n    var isBinLoader = storage.session.getBoolean('binloader', false);"
replacement = """function jailbreakSuccess(statusMessage) {
    // JOSDANY92: record successful GoldHEN payload completion.
    // This callback runs after WebKitty's selected payload loader returns.
    try {
        var j92PayloadPath = storage.session.getString('payload_path', '');
        var j92IsGoldHEN = typeof user !== 'undefined'
            && user.currentJbFlavor === 'GoldHEN'
            && /goldhen_v2\\.4b18\\.14\\.bin$/i.test(j92PayloadPath);
        if (j92IsGoldHEN) {
            localStorage.setItem('j92-goldhen-last-success', JSON.stringify({
                result: 'WebKitty reported GoldHEN payload completion',
                version: '2.4b18.14',
                firmware: user.ps4Fw || getPs4FwVersion(),
                exploitChain: user.exploitChain,
                payload: j92PayloadPath,
                timestamp: Date.now()
            }));
        }
    } catch (e) {
        console.warn('JOSDANY92 success marker could not be saved:', e);
    }

    var isBinLoader = storage.session.getBoolean('binloader', false);"""
if anchor not in source:
    raise SystemExit("Expected upstream jailbreakSuccess anchor was not found; refusing to patch.")
target.write_text(source.replace(anchor, replacement, 1), encoding="utf-8")
print("Applied JOSDANY92 GoldHEN success marker.")
