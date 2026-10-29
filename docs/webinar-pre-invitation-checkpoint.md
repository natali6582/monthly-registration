# Webinar checkpoint before Outlook invitations

This checkpoint preserves the deployed direct-registration flow on 29 October 2026, before implementing real Outlook meeting invitations.

## Preserved behavior

- Page: `/experts-webinar`, Wix HTML component `expertsRegistrationHtml`.
- Displayed start time: **11:00**, 10 November 2026. The calendar remains **11:00–11:45 Asia/Jerusalem**.
- Full-width calendar button, 19px text and blue border; the redundant registration footnote is removed.
- Intake scenario **6823179** and cancellation scenario **6823178** remain active.
- Intake sends a confirmation email from Sales with a `METHOD:PUBLISH` calendar attachment. No Outlook invitation mode has been enabled.
- Cancellation changes the registration record. It does not delete an already imported calendar entry.

## Recovery sources

`expert-team-webinar-direct-20261110/production/wix/` contains the form, page bridge, backend, and builder inputs. `production/make/intake/` and `production/make/cancellation/` contain the scenario snapshots. The existing monthly-training source is unchanged.

Public files replace the live Zoom join URL with `https://zoom.us/j/REPLACE_WITH_WEBINAR_ID`. Do not deploy that placeholder. Exact private Make snapshots and Wix artifacts are retained locally under `out_20261029_calendar_invitation_baseline/`, outside this commit. They contain the existing server-side webhook references; Wix secrets stay in Wix.

## Rollback procedure after a future invitation-mode rollout

1. Stop creating invitations for new registrations; preserve registration data and the invitation/event ledger.
2. Restore the current intake email/ICS configuration from the exact private snapshot, keeping the current webhook endpoint and connections. Read back all edited module fields and activation state.
3. Restore the verified form HTML, page bridge and backend if they were changed; save and publish. Compare the public form source with the checkpoint.
4. Verify a single authorized test registration, the received confirmation email and the calendar date/time. Do not restore old Monday records over newer registrations.
5. Preserve cancellation handling for invitations already sent. A Git/configuration rollback cannot unsend them; cancelling those events would send separate cancellation notices.

The invitation rollout must retain the old mode until calendar authorization, invitation delivery, duplicate prevention and cancellation are tested. A user declining in Outlook does not currently update Monday.

## Verification at checkpoint

The published form matches the approved local HTML after newline normalization. Both Make scenarios were read live, and exact private snapshots were saved. Source exports are deterministic and exclude webhook URLs, personal cancellation tokens, private credentials and rendered test messages. Sales calendar-list discovery failed; authorization is still required before an invitation rollout.
