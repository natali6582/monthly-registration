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

function parseRegistrationConfig(rawConfig) {
  try {
    return JSON.parse(rawConfig);
  } catch {
    throw new Error(`${CONFIG_SECRET_NAME} is invalid JSON`);
  }
}

export async function invoke(payload, context) {
  const itemName = requireFullName(payload);
  const mondayToken = await getSecretValue(TOKEN_SECRET_NAME);
  if (typeof mondayToken !== 'string' || mondayToken.trim() === '') {
    throw new Error(`${TOKEN_SECRET_NAME} is missing`);
  }

  const rawConfig = await getSecretValue(CONFIG_SECRET_NAME);
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

  return {};
}
