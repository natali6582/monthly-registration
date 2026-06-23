# Plan-T Landing Page Contract

Required checks:
- Source file: `wix-training-landing.html`.
- Public output: `dist/index.html`.
- Logo asset: `assets/plan-t-logo.jpg`.
- Public GitHub Pages URL: `https://natali6582.github.io/monthly-registration/`.
- Required form field names: `name`, `company`, `email`, `phone`, `selected_topics`, `source`.
- `dist` must be included for public site updates.
- The webhook URL is read from source and not unnecessarily repeated in notes.

Verification command:

```powershell
py skills\plan-t-landing-page\scripts\validate_contract.py
```
