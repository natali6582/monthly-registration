import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath, pathToFileURL } from 'node:url';

const REPOSITORY_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ACTION_PATH = path.join(
  REPOSITORY_ROOT,
  'wix-velo',
  'automation-actions',
  'MONDAY-HJ.js'
);

const MONDAY_ENDPOINT = 'https://api.monday.com/v2';
const TOKEN_SECRET_NAME = 'MONDAY_API_TOKEN';
const CONFIG_SECRET_NAME = 'MONDAY_REGISTRATION_CONFIG';
const FIXED_NOW = '2026-07-26T08:00:00.000Z';

const REGISTRATION_CONFIG = {
  boardId: '5099813594',
  groupId: 'group_mm50r2qx',
  columns: {
    phone: 'phone_mm50904s',
    email: 'email_mm50jkhy',
    company: 'text_mm50vwsm',
    registrationDate: 'date_mm50szvs',
    status: 'color_mm50rkbq'
  },
  statusIndex: 7,
  countryShortName: 'IL'
};

const VALID_PAYLOAD = {
  'field:fullName': 'נטלי "בדיקה"\nקו שני',
  'field:role': 'מנהלת',
  'field:company': 'חברת בדיקה',
  'field:phone': '0501234567',
  'field:email': 'registration-test@example.com',
  'field:topics': 'טעינת קבצים'
};

function mondayResponse({
  ok = true,
  status = 200,
  jsonBody = { data: { create_item: { id: '12345', name: VALID_PAYLOAD['field:fullName'] } } },
  textBody = ''
} = {}) {
  return {
    ok,
    status,
    async json() {
      return jsonBody;
    },
    async text() {
      return textBody;
    }
  };
}

async function loadAction({
  fetchResponse = mondayResponse(),
  secretsByName = {
    [TOKEN_SECRET_NAME]: 'rotated-test-token',
    [CONFIG_SECRET_NAME]: JSON.stringify(REGISTRATION_CONFIG)
  }
} = {}) {
  const source = await readFile(ACTION_PATH, 'utf8');
  const fetchCalls = [];
  const secretReads = [];
  const logs = [];
  const NativeDate = Date;

  class FixedDate extends NativeDate {
    constructor(...args) {
      super(...(args.length ? args : [FIXED_NOW]));
    }

    static now() {
      return NativeDate.parse(FIXED_NOW);
    }
  }

  const context = vm.createContext({
    console: {
      log: (...args) => logs.push({ level: 'log', args }),
      error: (...args) => logs.push({ level: 'error', args })
    },
    Date: FixedDate
  });

  const wixFetchModule = new vm.SyntheticModule(
    ['fetch'],
    function initializeWixFetch() {
      this.setExport('fetch', async (url, options) => {
        fetchCalls.push({ url, options });
        return fetchResponse;
      });
    },
    { context }
  );

  const wixSecretsModule = new vm.SyntheticModule(
    ['secrets'],
    function initializeWixSecrets() {
      this.setExport('secrets', {
        async getSecretValue(name) {
          secretReads.push(name);
          return secretsByName[name];
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

  const actionModule = new vm.SourceTextModule(source, {
    context,
    identifier: pathToFileURL(ACTION_PATH).href
  });

  await actionModule.link(async (specifier) => {
    if (specifier === 'wix-fetch') {
      return wixFetchModule;
    }
    if (specifier === 'wix-secrets-backend.v2') {
      return wixSecretsModule;
    }
    if (specifier === 'wix-auth') {
      return wixAuthModule;
    }
    throw new Error(`Unexpected import in action under test: ${specifier}`);
  });
  await actionModule.evaluate();

  return {
    action: actionModule.namespace,
    fetchCalls,
    logs,
    secretReads
  };
}

function requireInvoke(action) {
  assert.equal(
    typeof action.invoke,
    'function',
    'Wix Run Velo Code requires an exported invoke(payload, context) entry point'
  );
  return action.invoke;
}

test('exports invoke as the Wix Run Velo Code entry point', async () => {
  const { action } = await loadAction();

  requireInvoke(action);
});

test('maps the Wix form payload through GraphQL variables and returns an empty object', async () => {
  const { action, fetchCalls, secretReads } = await loadAction();
  const invoke = requireInvoke(action);

  const result = await invoke(VALID_PAYLOAD, { invocationId: 'test-invocation' });

  assert.deepEqual(result, {});
  assert.deepEqual(secretReads, [TOKEN_SECRET_NAME, CONFIG_SECRET_NAME]);
  assert.equal(fetchCalls.length, 1);
  assert.equal(fetchCalls[0].url, MONDAY_ENDPOINT);

  const request = JSON.parse(fetchCalls[0].options.body);
  assert.match(request.query, /mutation\s+CreateRegistrationItem/);
  assert.equal(request.query.includes(VALID_PAYLOAD['field:fullName']), false);
  assert.equal(request.variables.itemName, VALID_PAYLOAD['field:fullName']);
  assert.equal(request.variables.boardId, REGISTRATION_CONFIG.boardId);
  assert.equal(request.variables.groupId, REGISTRATION_CONFIG.groupId);

  const columnValues = JSON.parse(request.variables.columnValues);
  assert.deepEqual(columnValues, {
    [REGISTRATION_CONFIG.columns.phone]: {
      phone: VALID_PAYLOAD['field:phone'],
      countryShortName: REGISTRATION_CONFIG.countryShortName
    },
    [REGISTRATION_CONFIG.columns.email]: {
      email: VALID_PAYLOAD['field:email'],
      text: VALID_PAYLOAD['field:email']
    },
    [REGISTRATION_CONFIG.columns.company]: VALID_PAYLOAD['field:company'],
    [REGISTRATION_CONFIG.columns.registrationDate]: { date: '2026-07-26' },
    [REGISTRATION_CONFIG.columns.status]: { index: REGISTRATION_CONFIG.statusIndex }
  });
});

test('rejects a missing required form field before reading secrets or calling Monday', async () => {
  const { action, fetchCalls, secretReads } = await loadAction();
  const invoke = requireInvoke(action);
  const invalidPayload = { ...VALID_PAYLOAD, 'field:fullName': '   ' };

  await assert.rejects(
    () => invoke(invalidPayload, {}),
    /field:fullName.*required/i
  );
  assert.equal(secretReads.length, 0);
  assert.equal(fetchCalls.length, 0);
});

test('rejects a missing Monday token before making a network request', async () => {
  const { action, fetchCalls } = await loadAction({
    secretsByName: {
      [TOKEN_SECRET_NAME]: '',
      [CONFIG_SECRET_NAME]: JSON.stringify(REGISTRATION_CONFIG)
    }
  });
  const invoke = requireInvoke(action);

  await assert.rejects(
    () => invoke(VALID_PAYLOAD, {}),
    /MONDAY_API_TOKEN.*missing/i
  );
  assert.equal(fetchCalls.length, 0);
});

test('rejects invalid registration configuration before making a network request', async () => {
  const { action, fetchCalls } = await loadAction({
    secretsByName: {
      [TOKEN_SECRET_NAME]: 'rotated-test-token',
      [CONFIG_SECRET_NAME]: '{not-json'
    }
  });
  const invoke = requireInvoke(action);

  await assert.rejects(
    () => invoke(VALID_PAYLOAD, {}),
    /MONDAY_REGISTRATION_CONFIG.*invalid/i
  );
  assert.equal(fetchCalls.length, 0);
});

test('rejects an HTTP failure without logging the token or upstream response body', async () => {
  const upstreamBody = 'upstream body that must not be logged';
  const { action, logs } = await loadAction({
    fetchResponse: mondayResponse({
      ok: false,
      status: 401,
      jsonBody: {},
      textBody: upstreamBody
    })
  });
  const invoke = requireInvoke(action);

  await assert.rejects(
    () => invoke(VALID_PAYLOAD, {}),
    /Monday request failed.*HTTP 401/i
  );
  const renderedLogs = JSON.stringify(logs);
  assert.equal(renderedLogs.includes('rotated-test-token'), false);
  assert.equal(renderedLogs.includes(upstreamBody), false);
});

test('rejects Monday GraphQL errors instead of reporting success', async () => {
  const { action } = await loadAction({
    fetchResponse: mondayResponse({
      jsonBody: {
        errors: [{ message: 'Invalid column value' }]
      }
    })
  });
  const invoke = requireInvoke(action);

  await assert.rejects(
    () => invoke(VALID_PAYLOAD, {}),
    /Monday GraphQL error.*Invalid column value/i
  );
});
