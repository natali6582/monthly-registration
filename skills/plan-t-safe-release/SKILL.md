---
name: plan-t-safe-release
description: Release Plan-T registration changes safely through local validation, git checks, commits, and pushes. Use when Codex needs to stage, commit, push, or summarize changes for the monthly-registration repository without overwriting unrelated user work.
---

# Plan-T Safe Release

Use this skill before publishing changes from the `monthly-registration` repository.

## Contract

Inputs:
- Current repository: `C:\Users\NatalieK\dev\monthly-registration`
- Git branch expected for site work: `main`
- Work GitHub remote expected for push: `work` / `natali6582/monthly-registration`

Expected output:
- Only requested files are staged.
- Generated/public files such as `dist/index.html` are included when needed.
- Commit message describes the change.
- Push goes to the work GitHub account/repository, not the old source repository.
- Final answer reports what changed and what was verified.

Assumptions:
- The checkout may contain untracked local backups and outputs.
- The old `origin` remote may point at a different or unavailable repository.

## Safety Rules

- Do not run `git reset --hard`, `git checkout --`, or destructive cleanup unless explicitly requested.
- Do not stage broad untracked directories like `backups`, `outputs`, or `.codex-remote-attachments` unless the user asks.
- Do not push to `origin` when the release target is the work account.
- Do not hide failing validations.
- Do not commit unrelated user changes.
- Always report any files intentionally left uncommitted.

## Workflow

1. Run `git status --short --branch`.
2. Review changed files and separate requested files from unrelated files.
3. Run skill-specific validators.
4. Stage only the intended files.
5. Commit with a concise message.
6. Push to the correct remote/branch.
7. Report validation evidence and remaining untracked files.

## Verification

Run:

```powershell
py skills\plan-t-safe-release\scripts\validate_contract.py
```

The test checks release safety rules, expected repository targets, and no-destructive-git constraints.

For detailed checks, read `references/contract.md`.
