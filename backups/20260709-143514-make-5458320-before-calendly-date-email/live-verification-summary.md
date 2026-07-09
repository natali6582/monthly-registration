# Live Make verification - 2026-07-09

Scenario: `5458320`

Repository artifact scope: copied Make blueprints, email preview, and verification notes only.

## Verified live in Make

- Scenario name: `הרשמה להדרכה עם לינק קלנדלי דינאמי`
- Scenario state: `Inactive`
- Schedule: `Immediately as data arrives`
- Queue: 2 records still waiting, not processed during this verification.
- No `Run once` was triggered during verification.
- No scenario activation was performed during verification.
- No unsaved-changes prompt was visible after inspection.

## Module checks

- Monday create-item module targets board `הרשמות להדרכות`.
- Monday `תאריך הרשמה` is mapped to `formatDate(now; "YYYY-MM-DDTHH:mm:ss")`.
- Monday module had no Google Sheets reference.
- First Calendly availability module starts at `formatDate(addMinutes(now; 5); "YYYY-MM-DDTHH:mm:ss[Z]"; "UTC")`.
- Calendly invite module uses `POST /invitees` through `sales@plan-t.org.il`.
- Calendly invite body uses `31.collection` through `37.collection` `start_time` tokens, plus webhook `1.name` and `1.email`.
- Email module sends through `sales@plan-t.org.il`.
- Email subject is `פרטי ההדרכה שלך במערכת PLAN-T`.
- Email content type is HTML.
- Email body references Set variable module 12, not plain text.
- Set variable module 12 contains the approved HTML email body with:
  - PLAN-T logo URL `https://natali6582.github.io/monthly-registration/assets/plan-t-logo.jpg`
  - logo width `72px`
  - dynamic training time from Calendly availability modules `31` through `37`
  - no Google Sheets token
  - no Zoom link
  - no Calendly scheduling-selection link
  - text that no additional date selection is needed

## Found, not fixed

- Two old queued records are still waiting in Make.
- The right-side history still shows old failed runs from before this fix, including `start_time must be in the future`.
- A separate top Tools module with a warning remains visible on the scenario canvas; it was not changed because it was outside this requested scope.
