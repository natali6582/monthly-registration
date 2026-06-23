# Plan-T Webinar Email Contract

Required checks:
- Date/time must stay dynamic through `{{4.`0`}}`.
- Calendar links must support Google Calendar and Outlook / Apple.
- Calendar formulas must parse `DD/MM/YYYY HH:mm:ss`.
- Training-entry link field `{{4.`1`}}` must not be used unless a real link is approved.
- No fake Zoom or placeholder entry link is allowed.
- Styling must avoid yellow and use Plan-T white/light-blue colors.
- Logo must use the hosted Plan-T landing page asset.
- Hebrew must remain UTF-8, not question marks.

Verification command:

```powershell
py skills\plan-t-webinar-email\scripts\validate_contract.py
```
