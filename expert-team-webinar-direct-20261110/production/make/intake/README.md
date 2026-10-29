# Webinar registration entry point

Scenario **6823179** retains its existing Wix webhook. Module **16** selects the delivery mode: `outlook` is the production default; `ics` restores the preserved email-and-calendar-file route.

The Outlook route calls worker **6828265**, which processes registrations in order, validates the form, checks for an existing non-cancelled email registration, and creates a pending Monday item. It stores the Outlook mode before creating a private invitation with one attendee, then saves the returned event ID before sending the styled Sales confirmation without an ICS attachment. A successful response is `{"status":"registered","deliveryMode":"outlook"}`.

The authorized calendar account is the visible invitation organizer. The event remains 10 November 2026, 11:00–11:45 Asia/Jerusalem; public copy displays the start time only. No Calendly step or individual Zoom registration is involved.

Unknown or partial results must not be retried automatically. An Outlook-mode record without an event ID requires reconciliation with Make history and its deterministic `plan-t-webinar-20261110-<itemId>` transaction ID before another invitation is attempted.

For rollback, set only module 16's value to `ics`. Keep cancellation scenario **6823178** and worker **6828325** active for invitations already sent. Do not restore old registration data or assume a Git revert cancels invitations.

See [deployment and verification](../../../../docs/webinar-outlook-invitations.md). Public snapshots use placeholders for the private Zoom URL and organizer identity; supply the approved values before deployment.
