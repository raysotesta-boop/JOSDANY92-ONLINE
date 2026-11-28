const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');

const language = fs.readFileSync('WebKitty/includes/js/language.js', 'utf8');
const patch = fs.readFileSync('patches/webkitty/apply-josdany92-patches.py', 'utf8');

test('firmware 12.00-12.02 is not presented as hardware-verified', () => {
  assert.match(language, /j92HardwarePending/);
  assert.match(language, /Cadena disponible · prueba en hardware pendiente/);
  assert.match(language, /j92FwNum >= 12\.00 && j92FwNum <= 12\.02/);
});

test('firmware validation label survives upstream WebKitty synchronization', () => {
  assert.match(patch, /firmware 12\.00-12\.02 status is honest about pending hardware validation/);
  assert.match(patch, /Cadena disponible · prueba en hardware pendiente/);
});
