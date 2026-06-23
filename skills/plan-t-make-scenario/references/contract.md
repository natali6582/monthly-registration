# Plan-T Make Scenario Contract

Required checks:
- Scope is only Make scenario `5458320`.
- Scenario URL is `https://us2.make.com/1621766/scenarios/5458320/edit`.
- Post-import schedule must be `Immediately as data arrives`.
- Local blueprint backup must exist before import.
- The agent must inspect the live module after import.
- The agent must not run `Run once` without explicit approval.
- The agent must not send test emails without explicit recipient and payload approval.
- The skill must not store full Make webhook URLs.

Verification command:

```powershell
py skills\plan-t-make-scenario\scripts\validate_contract.py
```
