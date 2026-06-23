---
name: plan-t-google-sheets-control
description: Validate and maintain the Google Sheets control contract for Plan-T training registration. Use when Codex needs to explain or update how Make reads the active webinar date, training link placeholder, active row, registration rows, or date format from the shared Google Sheet.
---

# Plan-T Google Sheets Control

Use this skill for the spreadsheet that controls the active Plan-T training date and registration output.

Read `references/contract.md` for the exact Hebrew tab names and column labels. Keep this file ASCII so the system skill validator works reliably in Windows PowerShell.

## Contract

Inputs:
- Spreadsheet ID: `1KVnCH206v5Bq4LT-cuTncBrvJwD5TcV1_zQwP2sOkeE`
- Control tab: exact Hebrew name in `references/contract.md`
- Registration tab: exact Hebrew name in `references/contract.md`

Expected output:
- Make reads one active row from the control tab.
- Column A stores the training date.
- Column B may store the training-entry link, but it must not be used in public emails until real.
- Column C stores the active flag.
- Registration rows append to the registration tab.

Assumptions:
- Calendar links require the exact date format `DD/MM/YYYY HH:mm:ss`, for example `25/06/2026 10:00:00`.
- User-facing phrasing like "next Thursday" is not safe for Make calendar parsing.

## Safety Rules

- Do not change sharing permissions without explicit approval.
- Do not delete sheet tabs, rows, or historical registrations.
- Do not create Apps Script alternatives unless the user explicitly asks.
- Do not use multiple active training rows.
- Do not publish registrant personal data in final answers.
- When editing sheet values, state the exact tab, row, column, and value before making the change.

## Workflow

1. Identify the exact spreadsheet and tabs.
2. Read headers before editing any cell.
3. Verify there is one active row in the control tab.
4. Validate date format before relying on calendar links.
5. If updating date/time, write only the control cell and report the new value.
6. Do not modify registration history except through the registration flow.

## Verification

Run:

```powershell
py skills\plan-t-google-sheets-control\scripts\validate_contract.py
```

The test checks the tab names, required columns, active-row rule, date format rule, and privacy/security constraints.

For detailed checks, read `references/contract.md`.
