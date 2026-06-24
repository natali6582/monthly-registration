import { Permissions, webMethod } from 'wix-web-module';
import { secrets } from 'wix-secrets-backend.v2';
import { elevate } from 'wix-auth';
import { fetch } from 'wix-fetch';

const elevatedGetSecretValue = elevate(secrets.getSecretValue);

const SECRET_WEBHOOK_URL = 'MAKE_WEBHOOK_URL';
const SECRET_API_KEY = 'MAKE_WEBHOOK_API_KEY';
const SOURCE = 'wix-velo-secure-form';

function cleanText(value, maxLength = 500) {
  return String(value || '').trim().replace(/\s+/g, ' ').slice(0, maxLength);
}

function assertField(name, value) {
  if (!value) {
    throw new Error(`${name} is required`);
  }
}

function assertEmail(email) {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new Error('email is invalid');
  }
}

function encodeForm(payload) {
  return Object.entries(payload)
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&');
}

function normalizeRegistration(form) {
  const payload = {
    name: cleanText(form?.name, 120),
    company: cleanText(form?.company, 160),
    email: cleanText(form?.email, 180).toLowerCase(),
    phone: cleanText(form?.phone, 60),
    selected_topics: cleanText(form?.selected_topics, 1000),
    source: SOURCE
  };

  assertField('name', payload.name);
  assertField('company', payload.company);
  assertField('email', payload.email);
  assertField('phone', payload.phone);
  assertField('selected_topics', payload.selected_topics);
  assertEmail(payload.email);

  return payload;
}

async function getRequiredSecret(name) {
  const secret = await elevatedGetSecretValue(name);
  const value = cleanText(
    typeof secret === 'string' ? secret : secret?.value,
    2000
  );

  if (!value) {
    throw new Error(`${name} is missing`);
  }

  return value;
}

function requireAbsoluteHttpsUrl(url, name) {
  if (!/^https:\/\//i.test(url)) {
    throw new Error(`${name} must be a full https:// URL`);
  }

  return url;
}

export const submitRegistration = webMethod(Permissions.Anyone, async (form) => {
  const payload = normalizeRegistration(form);
  const webhookUrl = requireAbsoluteHttpsUrl(
    await getRequiredSecret(SECRET_WEBHOOK_URL),
    SECRET_WEBHOOK_URL
  );
  const apiKey = await getRequiredSecret(SECRET_API_KEY);

  const response = await fetch(webhookUrl, {
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'x-make-apikey': apiKey
    },
    body: encodeForm(payload)
  });

  if (!response.ok) {
    const body = await response.text();
    console.error('Make registration webhook failed', {
      status: response.status,
      body: body?.slice(0, 500)
    });
    throw new Error('Registration failed');
  }

  return { ok: true };
});
