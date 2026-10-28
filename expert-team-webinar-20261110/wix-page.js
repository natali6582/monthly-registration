import { submitExpertRegistration } from "backend/expert-team-registration.web";

const READY_TYPE = "plan-t:experts:ready";
const READY_ACK_TYPE = "plan-t:experts:ready-ack";
const SUBMIT_TYPE = "plan-t:experts:submit";
const RESULT_TYPE = "plan-t:experts:result";
const CALENDLY_URL = "https://calendly.com/supportclient-plan-t/plan-t-10-11-2026-11-00";

function normalizeRegistration(message) {
  if (typeof message.name !== "string" || typeof message.phone !== "string" || typeof message.email !== "string") return null;
  const name = message.name.trim().replace(/\s+/g, " ");
  const phone = message.phone.trim().replace(/[\s()+.\-]/g, "");
  const email = message.email.trim().toLowerCase();
  if (name.length < 2 || name.length > 100) return null;
  if (!/^\d{9,15}$/.test(phone)) return null;
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return null;
  return { name, phone, email };
}

$w.onReady(() => {
  const html = $w("#expertsRegistrationHtml");
  let inFlightRequestId = null;

  function reply(requestId, status) {
    const message = { type: RESULT_TYPE, requestId, status };
    if (status === "queued") message.calendlyUrl = CALENDLY_URL;
    html.postMessage(message);
  }

  html.onMessage(async (event) => {
    const message = event.data;
    if (!message || typeof message !== "object" || Array.isArray(message)) return;

    if (message.type === READY_TYPE) {
      html.postMessage({ type: READY_ACK_TYPE });
      return;
    }
    if (message.type !== SUBMIT_TYPE) return;
    if (typeof message.requestId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9_.:\-]{0,99}$/.test(message.requestId)) return;

    const requestId = message.requestId;
    if (inFlightRequestId === requestId) return;
    if (inFlightRequestId !== null) {
      reply(requestId, "error");
      return;
    }

    const registration = normalizeRegistration(message);
    if (!registration) {
      reply(requestId, "invalid");
      return;
    }

    inFlightRequestId = requestId;
    try {
      const result = await submitExpertRegistration(registration);
      if (result && result.status === "queued" && result.calendlyUrl === CALENDLY_URL) {
        reply(requestId, "queued");
      } else if (result && ["invalid", "error", "unknown"].includes(result.status)) {
        reply(requestId, result.status);
      } else {
        reply(requestId, "unknown");
      }
    } catch (error) {
      // The backend may have completed despite a lost response. Do not retry here.
      reply(requestId, "unknown");
    } finally {
      inFlightRequestId = null;
    }
  });
});
