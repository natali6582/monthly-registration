---
name: plan-t-webinar-email
description: Build and validate Plan-T webinar registration email templates for Make/Outlook. Use when Codex needs to update the confirmation email HTML, add Plan-T branding, keep the webinar date dynamic from Google Sheets, restore calendar links, or remove inactive training-entry links safely.
---

# Plan-T Webinar Email

Use this skill for the HTML email body sent by the Plan-T Make scenario.

## Contract

Inputs:
- Existing Make blueprint or module content.
- Plan-T logo URL already hosted by the landing page.
- Dynamic date field from the active training row: `{{4.`0`}}`.

Expected output:
- Email body uses white and Plan-T light-blue styling.
- Plan-T logo appears at the top and signature area.
- Date/time remains dynamic from the Google Sheet field.
- Google Calendar and Outlook / Apple links are present.
- Training-entry link/button is not present until the user provides a real URL.
- Email body is HTML-safe for Make formulas.

Assumptions:
- Calendar links depend on the sheet date format `DD/MM/YYYY HH:mm:ss`.
- The entry link is intentionally unavailable unless the user supplies one.

## Safety Rules

- Do not hard-code a webinar date inside the template.
- Do not include a fake Zoom/training URL.
- Do not remove working calendar links unless the user explicitly requests it.
- Do not send an actual email for testing without approval of recipient and payload.
- Keep all user-facing Hebrew text in UTF-8; reject templates that turn Hebrew into question marks.
- Use a new backup blueprint for every imported email change.

## Workflow

1. Extract the active email module from the blueprint or Make UI.
2. Prepare the HTML template locally first.
3. Validate these tokens before import:
   - `{{4.`0`}}`
   - `calendar.google.com/calendar/render`
   - `outlook.office.com/calendar/0/deeplink/compose`
   - `assets/plan-t-logo.jpg`
4. Confirm no yellow background remains.
5. Confirm no `{{4.`1`}}` training-entry link is used unless approved.
6. Import or update Make.
7. Inspect the live Make module after saving.

## Verification

Run:

```powershell
py skills\plan-t-webinar-email\scripts\validate_contract.py
```

The test checks the required dynamic-date, calendar-link, branding, no-fake-link, UTF-8, and safety rules.

For detailed checks, read `references/contract.md`.
