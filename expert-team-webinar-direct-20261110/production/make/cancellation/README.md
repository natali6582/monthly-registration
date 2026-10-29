# Webinar registration cancellation

Scenario **6823178** keeps the existing private Wix cancellation webhook. Opening a link only displays a confirmation; cancellation requires the participant to confirm. The backend sends a SHA-256 token hash and the scenario requires exactly one matching item in board **5106887275**, group `topics`.

For an Outlook registration, worker **6828325** verifies the event ID, organizer, sole attendee and registration transaction ID before requesting cancellation. It confirms a cancelled event or an exact-event 404 following an accepted cancellation request. Only then does the parent update Monday to `בוטלה הרשמה` and return a verified result.

Legacy records with empty delivery mode and event ID keep their existing status-only cancellation behavior. Inconsistent or missing Outlook metadata fails closed. An initial 404, permission failure, or ambiguous result is not proof of cancellation. Already-cancelled Monday records return confirmation without sending another cancellation.

Keep this scenario and its worker active after switching new registrations back to ICS. Calendar RSVP responses such as Decline are separate from registration cancellation and do not automatically update Monday; the cancellation link is the supported action.

See [deployment and verification](../../../../docs/webinar-outlook-invitations.md). Never commit actual cancellation tokens, private webhook addresses or test event records.
