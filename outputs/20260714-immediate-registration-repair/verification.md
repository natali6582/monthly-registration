# Immediate registration flow repair

Date: 2026-07-14 (Asia/Jerusalem)

## Scope

- Wix page: `https://www.plan-t.org.il/monthlyregistration`
- Make scenario: `5595814`
- Monday board: `5099813594`
- No unrelated Make scenarios or Monday flows were changed.
- No Wix source code was changed. The live HTML component already used the secure Velo `postMessage` flow.

## Root cause

Scenario `5595814` was active and valid, but its schedule was:

```json
{"type":"indefinitely","interval":900}
```

Webhook submissions were accepted into the Make queue and processed only on the 15-minute interval. Wix therefore showed success before Monday and email processing had completed.

## Change

Only the scenario schedule was changed to:

```json
{"type":"immediately","maximum_runs_per_minute":100}
```

The scenario remained active and valid. A flow-only SHA-256 comparison confirmed that the Make module blueprint did not change.

## Verification

- Queued submissions were processed successfully after the schedule change.
- Trigger queue after processing: `0`.
- End-to-end test submitted through the live Wix page: `בדיקת חיבור מיידי 14-07`.
- Test recipient: `sales@plan-t.org.il`.
- Make execution: `f44f9ddda1664390a8552cd2f990c56a`.
- Execution status: `SUCCESS`.
- Operations: `10`.
- Monday create-item module `30`: status `1`, one bundle.
- Microsoft email module `2`: status `1`, one bundle.
- Monday row was visible on board `5099813594` with status `נרשם`, registration time `2026-07-14 00:28`, and training time `2026-08-06 11:00`.
- Observed time from Wix submit to completed Make run: approximately 77 seconds.

## Backups

- `backups/20260714-002032-wix-live-form-before-repair/`
- `backups/20260714-002409-scenario-5595814-before-immediate-schedule/`

The second backup includes the scenario details, blueprint before and after the scheduling change, and the exact patch request.

## Found, not changed

- Multiple registrations had accumulated in the webhook queue and were processed together when immediate scheduling was restored.
- The test row `בדיקת חיבור מיידי 14-07` remains on the Monday board as end-to-end evidence.
- Module success proves that Make submitted the email successfully; mailbox placement is controlled by the recipient mail system.
