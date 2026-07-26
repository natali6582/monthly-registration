import { fetch } from 'wix-fetch';
import { secrets } from 'wix-secrets-backend.v2';
import { elevate } from 'wix-auth';

const MONDAY_ENDPOINT = 'https://api.monday.com/v2';
const TOKEN_SECRET_NAME = 'MONDAY_API_TOKEN';
const CONFIG_SECRET_NAME = 'MONDAY_REGISTRATION_CONFIG';
const getSecretValue = elevate(secrets.getSecretValue);

const CREATE_REGISTRATION_ITEM = `
  mutation CreateRegistrationItem(
    $boardId: ID!
    $groupId: String!
    $itemName: String!
    $columnValues: JSON!
  ) {
    create_item(
      board_id: $boardId
      group_id: $groupId
      item_name: $itemName
      column_values: $columnValues
    ) {
      id
      name
    }
  }
`;

function requireFullName(payload) {
  const fullName = payload?.['field:fullName'];
  if (typeof fullName !== 'string' || fullName.trim() === '') {
    throw new Error('field:fullName is required');
  }
  return fullName;
}

function unwrapSecretValue(secretResponse) {
  if (typeof secretResponse === 'string') {
    return secretResponse;
  }
  if (typeof secretResponse?.value === 'string') {
    return secretResponse.value;
  }
  return '';
}

function requireConfigString(value, path) {
  if (typeof value !== 'string' || value.trim() === '') {
    throw new Error(`${CONFIG_SECRET_NAME} ${path} is required`);
  }
}

function parseRegistrationConfig(rawConfig) {
  let config;
  try {
    config = JSON.parse(rawConfig);
  } catch {
    throw new Error(`${CONFIG_SECRET_NAME} is invalid JSON`);
  }

  requireConfigString(config?.boardId, 'boardId');
  requireConfigString(config?.groupId, 'groupId');
  requireConfigString(config?.columns?.phone, 'columns.phone');
  requireConfigString(config?.columns?.email, 'columns.email');
  requireConfigString(config?.columns?.company, 'columns.company');
  requireConfigString(
    config?.columns?.registrationDate,
    'columns.registrationDate'
  );
  requireConfigString(config?.columns?.status, 'columns.status');
  requireConfigString(config?.countryShortName, 'countryShortName');
  if (!Number.isInteger(config?.statusIndex) || config.statusIndex < 0) {
    throw new Error(`${CONFIG_SECRET_NAME} statusIndex is required`);
  }

  return config;
}

export async function invoke(payload, context) {
  const itemName = requireFullName(payload);
  const tokenResponse = await getSecretValue(TOKEN_SECRET_NAME);
  const mondayToken = unwrapSecretValue(tokenResponse);
  if (typeof mondayToken !== 'string' || mondayToken.trim() === '') {
    throw new Error(`${TOKEN_SECRET_NAME} is missing`);
  }

  const configResponse = await getSecretValue(CONFIG_SECRET_NAME);
  const rawConfig = unwrapSecretValue(configResponse);
  const config = parseRegistrationConfig(rawConfig);
  const email = payload['field:email'] || '';
  const columnValues = {
    [config.columns.phone]: {
      phone: payload['field:phone'] || '',
      countryShortName: config.countryShortName
    },
    [config.columns.email]: {
      email,
      text: email
    },
    [config.columns.company]: payload['field:company'] || '',
    [config.columns.registrationDate]: {
      date: new Date().toISOString().split('T')[0]
    },
    [config.columns.status]: {
      index: config.statusIndex
    }
  };

  const response = await fetch(MONDAY_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: mondayToken
    },
    body: JSON.stringify({
      query: CREATE_REGISTRATION_ITEM,
      variables: {
        boardId: config.boardId,
        groupId: config.groupId,
        itemName,
        columnValues: JSON.stringify(columnValues)
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Monday request failed: HTTP ${response.status}`);
  }

  const result = await response.json();
  if (Array.isArray(result.errors) && result.errors.length > 0) {
    const messages = result.errors
      .map((error) => error?.message || 'Unknown error')
      .join('; ');
    throw new Error(`Monday GraphQL error: ${messages}`);
  }
  if (!result?.data?.create_item?.id) {
    throw new Error('Monday response did not return a created item');
  }

  return {};
}
