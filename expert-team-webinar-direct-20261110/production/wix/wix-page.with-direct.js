import wixLocationFrontend from "wix-location-frontend";
import { submitDirectExpertRegistration, cancelDirectExpertRegistration } from "backend/expert-team-direct-registration.web";

$w.onReady(() => {
  initializeDirectFlow($w("#expertsRegistrationHtml"), wixLocationFrontend.query);
});

function initializeDirectFlow(html, query) {
  const cancelToken = typeof query.cancel === "string" && /^[a-f0-9]{64}$/.test(query.cancel) ? query.cancel : null;
  const invalidCancel = Object.prototype.hasOwnProperty.call(query, "cancel") && !cancelToken;
  let inFlight = false;
  html.onMessage(async event => {
    const message = event.data;
    if (!message || typeof message !== "object" || Array.isArray(message)) return;
    if (message.type === "plan-t:experts:ready" || message.type === "plan-t:experts-direct:ready") {
      html.postMessage({ type: "plan-t:experts-direct:mode", mode: "direct", cancellation: Boolean(cancelToken), invalidCancel });
      return;
    }
    if (!["plan-t:experts-direct:submit", "plan-t:experts-direct:cancel"].includes(message.type)) return;
    if (typeof message.requestId !== "string" || !/^[A-Za-z0-9][A-Za-z0-9_.:\-]{0,99}$/.test(message.requestId) || inFlight) return;
    inFlight = true;
    let result = { status: "unknown" };
    try {
      if (message.type === "plan-t:experts-direct:cancel") {
        result = cancelToken ? await cancelDirectExpertRegistration(cancelToken) : { status: "invalid" };
      } else if (cancelToken || invalidCancel) {
        result = { status: "invalid" };
      } else {
        result = await submitDirectExpertRegistration({ name: message.name, phone: message.phone, email: message.email });
      }
    } catch (error) { result = { status: "unknown" }; }
    finally { inFlight = false; }
    html.postMessage({ type: "plan-t:experts-direct:result", requestId: message.requestId, ...result });
  });
}
