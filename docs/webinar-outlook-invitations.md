# Webinar registration with Outlook invitations

Source snapshot of the production webinar flow after the Outlook-invitation rollout on 29 October 2026. The earlier pre-invitation checkpoint document remains historical. Monthly-training files are outside this export.

## Production behavior

- The existing `/experts-webinar` form submits directly, without Calendly.
- The page and confirmation email display **10 November 2026 at 11:00 Israel time**. The calendar invitation is **11:00–11:45 Asia/Jerusalem**, or **09:00–09:45 UTC**.
- Intake parent **6823179**, module **16**, currently sets `deliveryMode` to `outlook`. Its Outlook branch calls registration worker **6828265**; the legacy ICS branch is retained for rollback.
- Registration worker **6828265** is serial (`sequential:true`, `dlq:false`). It creates the Outlook invitation, records the associated event information, then sends the separate styled Sales confirmation. The confirmation has no ICS attachment in Outlook mode.
- The invitation organizer is the user-approved personal Microsoft calendar account configured in the calendar connection. The styled confirmation is sent from Sales. These are separate messages and senders.
- Cancellation parent **6823178** calls worker **6828325** when the registration has an Outlook invitation. Cancellation of the linked event sends the calendar cancellation notice. Existing legacy registrations retain their original cancellation path.
- Declining or changing RSVP in a calendar client does **not** update Monday. Use the registration cancellation link for the application cancellation flow.

## Files and configuration

`production/wix/` contains the four builder inputs and the three current compiled Wix artifacts. The page uses the direct flow by default and recognizes both Outlook-invitation and legacy ICS responses. The backend reads webhook endpoints from Wix Secrets; their values are never exported.

The four `production/make/*/scenario-blueprint.json` files preserve the latest module wiring, guards, mappings and worker interfaces. Each export has `autoActivate:false`; storing or importing these files does not deploy or activate a scenario. The registration worker's serial settings and the intake parent's `sequential:false` are the only explicitly exported runtime settings. Metadata records the live snapshot status separately.

Before deployment, replace `https://zoom.us/j/REPLACE_WITH_WEBINAR_ID` with the approved private Zoom join URL. Replace every `REPLACE_WITH_ORGANIZER_EMAIL` guard with the exact email of the authorized calendar organizer; do not remove these identity checks. Preserve or remap the scenario, hook and connection IDs when importing into a different Make environment. Worker-call IDs must target the corresponding workers before activation.

The public event input omits the test recipient, preview UID and preview timestamp. Rendered customer messages, Outlook event IDs, registration rows, personal cancellation tokens, webhook URLs, execution logs and screenshots are excluded. The existing synthetic row `3317000000` in the asset builder is only a fixture constant.

## Build the two email modes

Run from the repository root with a fresh output directory on each run:

```sh
python -B expert-team-webinar-direct-20261110/production/make/intake/build_assets.py --event expert-team-webinar-direct-20261110/event-preview.json --row-module 6 --delivery-mode outlook --output out_webinar_outlook
python -B expert-team-webinar-direct-20261110/production/make/intake/build_assets.py --event expert-team-webinar-direct-20261110/event-preview.json --row-module 6 --delivery-mode ics --output out_webinar_ics
python -B expert-team-webinar-direct-20261110/production/wix/build_wix.py --default-direct --out out_webinar_wix
```

Outlook mode emits only `email-template.html`; Make must send the invitation before sending that confirmation. Default `ics` mode preserves the legacy email and calendar attachment. The public placeholder URL is not deployable until replaced with the real event configuration. The Wix builder also uses the existing `expert-team-webinar-20261110/form.html` and `wix-page.js` base sources already in the repository.

## Rollback for new registrations

1. Change only intake parent **6823179**, module **16**, `mapper.value` from `outlook` to `ics`, then save and read back that field and the active state. This selects the retained legacy branch for subsequent registrations.
2. Keep cancellation parent **6823178** and cancellation worker **6828325** active for invitations already sent. Preserve their event ledger and registration data. A configuration rollback cannot unsend an invitation.
3. Do not replace existing Monday rows or restore old event IDs over current records. Preserve the organizer identity checks and the worker interfaces.
4. Verify one authorized test of the selected registration mode and the existing invitation cancellation path before making further changes.

The Wix response handling supports both modes, so switching the parent delivery-mode field does not require restoring an old page that lacks invitation support.

## Verification and limits

Invitation delivery to Gmail, the separate Sales confirmation and the calendar cancellation notice were verified. The public form's duplicate-registration path and a repeated cancellation were also checked. These checks do not imply that every calendar client adds an event without recipient confirmation; RSVP-decline synchronization to Monday is not implemented.

The public export is generated twice from the same final private snapshots and source files. File manifests must match byte for byte, and the export is scanned for the private Zoom password, webhook endpoints, personal test emails, cancellation tokens and credentials. Private evidence remains outside this repository.
