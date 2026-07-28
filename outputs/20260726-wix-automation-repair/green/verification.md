# Step 4 — GREEN verification

Date: 2026-07-26

## Contract implemented

- Input: Wix form trigger payload containing the documented `field:*` keys.
- Output on success: an empty object.
- Secrets:
  - `MONDAY_API_TOKEN`
  - `MONDAY_REGISTRATION_CONFIG`
- Side effect: one Monday `create_item` GraphQL request when validation succeeds.

## Minimal implementation

- Exports the Wix-required `invoke(payload, context)` entry point.
- Validates the required full-name field before reading secrets.
- Reads the Monday token and account mapping from Wix Secrets.
- Sends user-controlled values through GraphQL variables.
- Rejects HTTP and GraphQL errors without logging secrets or response bodies.

## Verification

```powershell
node --check tests/MONDAY-HJ.test.mjs
node --check wix-velo/automation-actions/MONDAY-HJ.js
node --experimental-vm-modules --test tests/MONDAY-HJ.test.mjs
```

Result:

- Syntax checks: passed.
- Tests: 7 passed, 0 failed, 0 skipped.
- Network, email, Wix, Monday, deployment, and push actions: none.

The success-result assertion was adjusted to validate an object with zero keys
across Node VM realms. The expected behavior was not weakened.
