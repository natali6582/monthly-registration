import { Permissions, webMethod } from "wix-web-module";
import { fetch } from "wix-fetch";

const MAKE_WEBHOOK_URL = "<SET_PRIVATELY_IN_WIX_BACKEND>"; // Live webhook omitted from this public repository.
const CALENDLY_URL = "https://calendly.com/supportclient-plan-t/plan-t-10-11-2026-11-00";
const REQUEST_TIMEOUT_MS = 25000;

function normalizeRegistration(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) return null;
  const keys = Object.keys(payload).sort();
  if (keys.length !== 3 || keys.join(",") !== "email,name,phone") return null;
  if (typeof payload.name !== "string" || typeof payload.phone !== "string" || typeof payload.email !== "string") return null;

  const name = payload.name.trim().replace(/\s+/g, " ");
  const phone = payload.phone.trim().replace(/[\s()+.\-]/g, "");
  const email = payload.email.trim().toLowerCase();
  if (name.length < 2 || name.length > 100) return null;
  if (!/^\d{9,15}$/.test(phone)) return null;
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return null;
  return { name, phone, email };
}

export const submitExpertRegistration = webMethod(Permissions.Anyone, async (payload) => {
  const registration = normalizeRegistration(payload);
  if (!registration) return { status: "invalid" };

  let timeoutId;
  try {
    // The local deadline does not cancel a POST that Make may already have received.
    const response = await Promise.race([
      fetch(MAKE_WEBHOOK_URL, {
        method: "post",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registration)
      }),
      new Promise((resolve, reject) => {
        timeoutId = setTimeout(() => reject(new Error("REQUEST_TIMEOUT")), REQUEST_TIMEOUT_MS);
      })
    ]);

    if (response.status !== 200 && response.status !== 202) return { status: "error" };
    return { status: "queued", calendlyUrl: CALENDLY_URL };
  } catch (error) {
    // A network failure or deadline leaves the receipt status uncertain. Do not retry here.
    return { status: "unknown" };
  } finally {
    if (timeoutId !== undefined) clearTimeout(timeoutId);
  }
});
