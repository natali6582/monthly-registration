# Verification report - Wix, Make, Monday, Calendly

Date: 2026-07-13 (Asia/Jerusalem)

## Scope

- Scenario: `5595814` (`הרשמה להדרכה חודשית (נטלי) - Wix-Monday-Calendly`)
- Monday board: `5099813594`
- Existing unrelated scenarios and flows were not changed.
- API tokens and webhook URLs are not stored in this report.

## Root cause and fix

- The Calendly scheduling-link code was extracted from URL segment 5.
- Make removes the empty segment after `https://`, so segment 5 was `one-off-meeting` instead of the link code.
- The extraction now uses segment 4.
- HTTP modules 40, 41, and 42 now treat non-2xx/3xx responses as errors, so a `404` cannot silently create a row with an empty training date.

## Reproducibility

- Final blueprint SHA-256: `BBA722CAF641374829BA1162A2698E068E26BFB8208735D11FB5FF3ED11AF6D9`
- Final patch request SHA-256: `C10760FC1E59CAD79841D6F67A22607CF8335706086635F52002413DBFEFD56F`
- Each artifact was generated twice and produced the same hash.

## Direct Make verification

- Test item: `FINAL-OK-20260713175717`
- Webhook response: HTTP 200, `Accepted`, 726 ms.
- Make execution: `196d8a6b170a46af832af18662a1b9d7`
- Result: success, 10 of 10 modules completed, 4.737 seconds.
- Monday training date: `Aug 6, 11:00 AM`.
- Monday registration date and customer name were populated.
- Outlook email module completed successfully.

## Wix end-to-end verification

- Test item: `WIX-FINAL-20260713180129`
- Wix displayed: `ההרשמה נשלחה.`
- Make execution: `132a200feb2543759456b758b4ba9a19`
- Result: success, 10 of 10 modules completed, 5.532 seconds.
- Monday row contains the exact Wix name, phone, company, registration date, and training date `Aug 6, 11:00 AM`.
- Email recipient is read from Monday column `email_mm50jkhy`.
- Email greeting uses the created Monday item name (`{{43.name}}`).

## Live scenario state

- Active: `true`
- Invalid: `false`
- Module order: `1,39,40,41,42,30,44,43,12,2`
- Email logo width: 72 px.

## Found, not changed

- The Wix form still requires the free-text field `training_focus`. The successful test used `נושא ההדרכה נקבע על ידי החברה`. This is a Wix form UX issue, not part of the Make mapping fix.
