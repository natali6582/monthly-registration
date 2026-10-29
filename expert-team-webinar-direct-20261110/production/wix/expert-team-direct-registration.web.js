import { Permissions, webMethod } from "wix-web-module";
import { fetch } from "wix-fetch";
import { getSecret } from "wix-secrets-backend";
import { randomBytes, createHash } from "crypto";

const INTAKE_SECRET = "PLAN_T_EXPERTS_DIRECT_INTAKE_URL";
const CANCEL_SECRET = "PLAN_T_EXPERTS_DIRECT_CANCEL_URL";
const JOIN_URL = "https://zoom.us/j/REPLACE_WITH_WEBINAR_ID";
const EVENT_TITLE = "חשיפת נבחרת המומחים של PLAN T";
const DEADLINE_MS = 35000;

function normalize(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) return null;
  if (Object.keys(payload).sort().join(",") !== "email,name,phone") return null;
  if ([payload.name, payload.phone, payload.email].some(value => typeof value !== "string")) return null;
  const name = payload.name.trim().replace(/\s+/g, " ");
  const phone = payload.phone.trim().replace(/[\s()+.\-]/g, "");
  const email = payload.email.trim().toLowerCase();
  if (name.length < 2 || name.length > 100 || !/^\d{9,15}$/.test(phone)) return null;
  if (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return null;
  return { name, phone, email };
}

async function post(secretName, payload) {
  const url = await getSecret(secretName);
  if (!/^https:\/\/hook\.us2\.make\.com\/[a-z0-9]+$/.test(url)) return { status: "error" };
  let timer;
  try {
    const response = await Promise.race([
      fetch(url, { method: "post", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }),
      new Promise((resolve, reject) => { timer = setTimeout(() => reject(new Error("DEADLINE")), DEADLINE_MS); })
    ]);
    const data = await response.json();
    if (!data || typeof data.status !== "string") return { status: "unknown" };
    if (response.status !== 200) return { status: data.status === "email_error" ? "email_error" : data.status === "invalid" ? "invalid" : "error" };
    return data;
  } catch (error) {
    // A lost response may follow a completed request. Never retry automatically.
    return { status: "unknown" };
  } finally { if (timer !== undefined) clearTimeout(timer); }
}

function escapeIcs(value) {
  return value.replace(/\\/g, "\\\\").replace(/\r?\n/g, "\\n").replace(/;/g, "\\;").replace(/,/g, "\\,");
}

function calendar(uid) {
  const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z");
  const lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PLAN T//Experts Webinar//HE", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT", `UID:${uid}`, `DTSTAMP:${stamp}`, "DTSTART:20261110T090000Z", "DTEND:20261110T094500Z", `SUMMARY:${escapeIcs(EVENT_TITLE)}`, `DESCRIPTION:${escapeIcs("קישור להצטרפות לוובינר: " + JOIN_URL)}`, `LOCATION:${escapeIcs(JOIN_URL)}`, "ORGANIZER:mailto:sales@plan-t.org.il", "STATUS:CONFIRMED", "SEQUENCE:0", "END:VEVENT", "END:VCALENDAR"];
  // Fold by UTF-8 octets, preserving complete Unicode code points (RFC 5545).
  return lines.map(line => {
    const result = []; let part = ""; let size = 0;
    for (const character of line) {
      const bytes = Buffer.byteLength(character, "utf8");
      if (size + bytes > 75) { result.push(part); part = " "; size = 1; }
      part += character; size += bytes;
    }
    result.push(part); return result.join("\r\n");
  }).join("\r\n") + "\r\n";
}

export const submitDirectExpertRegistration = webMethod(Permissions.Anyone, async payload => {
  const registration = normalize(payload);
  if (!registration) return { status: "invalid" };
  const cancelToken = randomBytes(32).toString("hex");
  const result = await post(INTAKE_SECRET, { ...registration, cancelToken, source: "experts-webinar-direct" });
  if (result.status === "registered" && result.deliveryMode === "outlook" && Object.keys(result).sort().join(",") === "deliveryMode,status") {
    return { status: "registered", deliveryMode: "outlook", joinUrl: JOIN_URL };
  }
  if (result.status === "registered" && result.deliveryMode === undefined && /^plan-t-experts-20261110-\d+@plan-t\.org\.il$/.test(result.calendarUid || "")) {
    return { status: "registered", joinUrl: JOIN_URL, calendarIcs: calendar(result.calendarUid) };
  }
  return { status: ["already_received", "invalid", "email_error", "error", "unknown"].includes(result.status) ? result.status : "unknown" };
});

export const cancelDirectExpertRegistration = webMethod(Permissions.Anyone, async token => {
  if (typeof token !== "string" || !/^[a-f0-9]{64}$/.test(token)) return { status: "invalid" };
  const tokenHash = createHash("sha256").update(token, "utf8").digest("hex");
  const result = await post(CANCEL_SECRET, { tokenHash });
  return { status: ["cancelled", "invalid", "error", "unknown"].includes(result.status) ? result.status : "unknown" };
});
