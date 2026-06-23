# Plan-T Safe Release Contract

Required checks:
- Repository path: `C:\Users\NatalieK\dev\monthly-registration`.
- Release branch: `main`.
- Work remote: `work`, pointing at `natali6582/monthly-registration`.
- Run status and diff checks before staging.
- Stage only intended files.
- Do not stage `backups`, `outputs`, or `.codex-remote-attachments` by default.
- Do not use destructive git commands.
- Push to the work remote, not old `origin`, unless the user explicitly changes target.

Verification command:

```powershell
py skills\plan-t-safe-release\scripts\validate_contract.py
```
