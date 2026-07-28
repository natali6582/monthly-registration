# Repository Working Rules

These rules apply to every task in this repository.

1. Plan before implementation.
   - State inputs, outputs, assumptions, files to touch, and the definition of done.
   - Wait for explicit approval before writing implementation code.

2. Work in small, reviewable steps.
   - Execute one approved step at a time.
   - Show the result and verification evidence before continuing.

3. Preserve rollback.
   - Do not overwrite source or baseline artifacts.
   - Create dated backups or redacted snapshots before changing external systems.
   - Keep work on a dedicated local branch until publication is explicitly approved.

4. Lock scope.
   - Change only the approved Wix automation repair.
   - Do not change the verified live Wix/Make flow or Make scenario `5595814`.
   - Record unrelated findings as "found, not fixed".

5. Use behavior-first TDD.
   - RED: add a meaningful failing test that proves the missing behavior.
   - GREEN: implement only enough to pass.
   - REFACTOR: improve clarity while keeping tests green.
   - Run relevant tests, then the full suite. Do not weaken or delete tests.

6. Require evidence.
   - Verify every change with tests, diffs, hashes, counts, or end-to-end evidence.
   - Run deterministic local checks twice and compare their outputs.
   - A claim without proof is not complete.

7. Prevent state leakage.
   - Use fresh dated output directories.
   - Overwrite generated outputs unless intentional append behavior is approved.
   - Avoid mutable global state and make dependencies explicit.
   - Ensure every requested change is wired into the main execution path.

8. Protect secrets and production systems.
   - Never hard-code, commit, print, or copy API tokens.
   - Read the Monday token from Wix Secrets Manager.
   - Treat the previously embedded Monday token as compromised.
   - Do not run Wix "Run Code", activate an automation, publish the site, send email,
     or create a Monday item without explicit approval for the live-test stage.
   - If a live email test is approved, use only `natali.koifman@gmail.com`.

9. Prefer safe, generic logic.
   - Validate required inputs and meaningful error paths.
   - Do not hard-code task-specific user data to satisfy a test.
   - Use GraphQL variables rather than interpolating user input into query text.

10. Stop on conflicting evidence.
    - If Wix state, repository state, or the request conflicts with this baseline,
      report the conflict and ask before proceeding.
