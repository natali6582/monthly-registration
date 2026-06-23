---
name: plan-t-landing-page
description: Maintain the Plan-T monthly registration landing page and GitHub Pages build output. Use when Codex needs to update Wix-compatible HTML, dist/index.html, Plan-T assets, form fields, Make webhook form action, or publish landing page changes to the natali6582/monthly-registration repository.
---

# Plan-T Landing Page

Use this skill for the static registration landing page in this repository.

## Contract

Inputs:
- Source file: `wix-training-landing.html`
- Build output: `dist/index.html`
- Logo asset: `assets/plan-t-logo.jpg`
- Public site: `https://natali6582.github.io/monthly-registration/`

Expected output:
- Source and `dist/index.html` stay in sync.
- `dist` changes are included when committing/pushing public site changes.
- The form posts to the existing Make webhook configured in the source.
- Form fields keep the names Make expects: `name`, `company`, `email`, `phone`, `selected_topics`, and `source`.

Assumptions:
- This is a static GitHub Pages deployment, not a server-rendered app.
- Full webhook URLs are implementation details and should not be unnecessarily repeated.

## Safety Rules

- Make a backup before editing source or `dist`.
- Do not rotate/change the webhook URL unless the Make scenario was updated and verified.
- Do not remove `dist` from commits when the public site depends on it.
- Do not add a fake training-entry link.
- Do not expose registrant data in test pages or examples.
- Do not change branding assets without user-provided approval.

## Workflow

1. Read both `wix-training-landing.html` and `dist/index.html`.
2. Make the same user-facing change in source and dist.
3. Verify logo references and form field names.
4. Verify the form action still points at the intended Make webhook.
5. Run static checks.
6. Commit and push only after the user confirms release scope.

## Verification

Run:

```powershell
py skills\plan-t-landing-page\scripts\validate_contract.py
```

The test checks required file paths, form fields, logo contract, `dist` inclusion, and safety constraints.

For detailed checks, read `references/contract.md`.
