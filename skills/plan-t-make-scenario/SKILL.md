---
name: plan-t-make-scenario
description: Safely maintain the Plan-T Make scenario used by the monthly registration landing page. Use when Codex needs to inspect, back up, import a blueprint into, configure scheduling for, or verify only Make scenario 5458320 in us2.make.com without touching other Make projects.
---

# Plan-T Make Scenario

Use this skill for the Make scenario behind Plan-T webinar registrations.

## Contract

Inputs:
- Make scenario URL: `https://us2.make.com/1621766/scenarios/5458320/edit`
- A local blueprint JSON file when importing changes.
- User approval before importing, saving, or running anything in Make.

Expected output:
- Scenario 5458320 is the only scenario changed.
- Scenario scheduling is `Immediately as data arrives`.
- The scenario is saved and verified in the UI.
- Evidence is reported: imported filename, scheduling text, save confirmation, and the specific module checked.

Assumptions:
- The user is already logged in to Make in the in-app browser.
- File upload from the browser may require the user to choose the JSON file manually.

## Safety Rules

- Do not change any Make scenario except `5458320`.
- Do not click `Run once` unless the user explicitly approves a real test run.
- Do not send test emails unless the user approves the recipient and test payload.
- Do not expose full webhook URLs in final notes. Refer to them as the scenario webhook.
- Always create or identify a local blueprint backup before import.
- After import, always re-check scheduling because Make can reset it to `Every 15 minutes`.
- If the browser UI behaves inconsistently, verify with the visible module contents before claiming success.

## Workflow

1. Confirm the browser is on scenario `5458320`.
2. Confirm the intended local blueprint path.
3. Verify the blueprint locally before asking the user to choose it.
4. Ask the user to choose the JSON file if the browser cannot upload it directly.
5. Import the blueprint.
6. Reopen and fix schedule to `Immediately as data arrives`.
7. Save the scenario.
8. Inspect the changed module content and report proof.

## Verification

Run the local contract test:

```powershell
py skills\plan-t-make-scenario\scripts\validate_contract.py
```

The test checks that this skill keeps the scenario scoped, requires backup and explicit approval, prevents accidental run/test email actions, and requires post-import scheduling verification.

For detailed checks, read `references/contract.md`.
