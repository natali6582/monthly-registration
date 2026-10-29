# Direct-registration confirmation emails

Source snapshot of the approved monthly-training and experts-webinar confirmation emails, dated 29 October 2026. Existing Wix and legacy registration source files are preserved.

Both headers use the approved transparent logo centered above the heading: 56 x 56 pixels on desktop, 48 x 48 on mobile, with a 14-pixel gap. The emails preserve the registration wording, Zoom links, calendar attachment and cancellation mappings. Outlook desktop uses a VML gradient fallback and Arial fonts.

The Make intake snapshots correspond to scenarios 6824104 (monthly) and 6823179 (webinar). This commit stores source only; it does not deploy, activate or execute a scenario.

The public webinar event input and blueprint use `https://zoom.us/j/REPLACE_WITH_WEBINAR_ID`. Supply the approved private Zoom URL before deployment. Private Make webhook endpoints, rendered customer messages, personal cancellation links and test data are not included. The logo is already hosted on Wix and referenced by its HTTPS URL in each builder.

## Build and verify

Run from the repository root, choosing fresh output directories:

```sh
python -B monthly-training-direct/production/make/intake-assets/build_assets.py --output out_monthly_1
python -B monthly-training-direct/production/make/intake-assets/build_assets.py --output out_monthly_2
python -B monthly-training-direct/production/make/intake-assets/verify_assets.py --first out_monthly_1 --second out_monthly_2 --output out_monthly_proof
python -B expert-team-webinar-direct-20261110/production/make/intake/build_assets.py --event expert-team-webinar-direct-20261110/event-preview.json --row-module 6 --output out_webinar_1
python -B expert-team-webinar-direct-20261110/production/make/intake/build_assets.py --event expert-team-webinar-direct-20261110/event-preview.json --row-module 6 --output out_webinar_2
```

The header-layout scripts record image size, centering, title spacing and overflow at 900px and 390px. They currently use the local Windows Playwright runtime path. Browser rendering does not prove identical rendering in every email client.
