# Step 3 — RED verification

Date: 2026-07-26

## Scope

- Added an isolated, redacted working copy of the current Wix automation action.
- Added behavior-focused tests for the proposed Wix `invoke(payload, context)` contract.
- Used mocked Wix Secrets and Monday API dependencies only.
- Performed no network request, email send, Wix update, Monday mutation, push, or deployment.

## Commands

```powershell
node --check tests/MONDAY-HJ.test.mjs
node --check wix-velo/automation-actions/MONDAY-HJ.js
node --experimental-vm-modules --test tests/MONDAY-HJ.test.mjs
```

## Evidence

- Both JavaScript syntax checks completed successfully.
- Test result: 7 tests, 0 passed, 7 failed, 0 skipped, 0 cancelled.
- The test command exited with code 1, as required for RED.
- Every test failed at the same missing public contract:

```text
Wix Run Velo Code requires an exported invoke(payload, context) entry point
actual: undefined
expected: function
```

This is a meaningful failure: the current action exports `createMondayItem(formData)`, while the Wix automation runtime requires an exported `invoke(payload, context)` entry point. The production behavior has not been implemented in this step.

## Behaviors specified for GREEN

1. Export the Wix automation entry point `invoke(payload, context)`.
2. Map the real colon-prefixed Wix form keys into Monday column values.
3. Pass GraphQL data through variables so quotes and newlines remain valid.
4. Read the Monday token and account-specific mapping from Wix Secrets.
5. Reject missing required form data, missing secrets, invalid configuration, HTTP errors, and Monday GraphQL errors.
6. Avoid logging secret tokens or upstream response bodies on failure.
7. Return an empty object after a successful custom action.

## Safety verification

- Compromised Monday token prefix matches in the work copy: `0`.
- Original external Velo source SHA-256 remains:
  `5773db957fadd3eb5d29397a14adf548de2e114f206cd275d058297203399fde`.
- Live GitHub `main` remains:
  `972ee41c8ca2ec704af2e8485f0514ef748ecbc5`.
- Local rollback tag `codex-baseline-20260726` still points to the same live `main` commit.
