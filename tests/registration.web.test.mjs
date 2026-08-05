import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath, pathToFileURL } from 'node:url';

const REPOSITORY_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REGISTRATION_BACKEND_PATH = path.join(
  REPOSITORY_ROOT,
  'wix-velo',
  'backend',
  'registration.web.js'
);

const VALID_REGISTRATION = {
  name: 'נטלי כהן',
  role: 'מנהלת הדרכה',
  company: 'חברת בדיקה',
  email: 'registration-test@example.com',
  phone: '0501234567',
  training_focus: 'נושא לבדיקה',
  selected_topics: 'נושא ההדרכה נקבע על ידי החברה'
};

async function loadRegistrationBackend() {
  const source = await readFile(REGISTRATION_BACKEND_PATH, 'utf8');
  const fetchCalls = [];
  const context = vm.createContext({ console });

  const wixWebModule = new vm.SyntheticModule(
    ['Permissions', 'webMethod'],
    function initializeWixWebModule() {
      this.setExport('Permissions', { Anyone: 'Anyone' });
      this.setExport('webMethod', (_permission, handler) => handler);
    },
    { context }
  );

  const wixSecretsModule = new vm.SyntheticModule(
    ['secrets'],
    function initializeWixSecrets() {
      this.setExport('secrets', {
        async getSecretValue(name) {
          return name === 'MAKE_WEBHOOK_URL'
            ? 'https://example.test/registration'
            : 'test-api-key';
        }
      });
    },
    { context }
  );

  const wixAuthModule = new vm.SyntheticModule(
    ['elevate'],
    function initializeWixAuth() {
      this.setExport('elevate', (fn) => (...args) => fn(...args));
    },
    { context }
  );

  const wixFetchModule = new vm.SyntheticModule(
    ['fetch'],
    function initializeWixFetch() {
      this.setExport('fetch', async (url, options) => {
        fetchCalls.push({ url, options });
        return { ok: true };
      });
    },
    { context }
  );

  const backendModule = new vm.SourceTextModule(source, {
    context,
    identifier: pathToFileURL(REGISTRATION_BACKEND_PATH).href
  });

  await backendModule.link(async (specifier) => {
    if (specifier === 'wix-web-module') return wixWebModule;
    if (specifier === 'wix-secrets-backend.v2') return wixSecretsModule;
    if (specifier === 'wix-auth') return wixAuthModule;
    if (specifier === 'wix-fetch') return wixFetchModule;
    throw new Error(`Unexpected backend import: ${specifier}`);
  });
  await backendModule.evaluate();

  return { backend: backendModule.namespace, fetchCalls };
}

test('submits a registration when training_focus is empty', async () => {
  const { backend, fetchCalls } = await loadRegistrationBackend();
  const registration = { ...VALID_REGISTRATION, training_focus: '   ' };

  const result = await backend.submitRegistration(registration);

  assert.equal(result.ok, true);
  assert.deepEqual(Object.keys(result), ['ok']);
  assert.equal(fetchCalls.length, 1);
  const submittedForm = new URLSearchParams(fetchCalls[0].options.body);
  assert.equal(submittedForm.get('training_focus'), '');
  assert.equal(submittedForm.get('name'), VALID_REGISTRATION.name);
  assert.equal(submittedForm.get('email'), VALID_REGISTRATION.email);
});
