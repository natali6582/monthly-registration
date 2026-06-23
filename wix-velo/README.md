# Plan-T Wix/Velo Secure Registration Flow

This package moves Plan-T registration submission away from direct static HTML-to-Make posting.

## Files

- `backend/registration.web.js` - Wix backend web module. Stores all Make access behind Wix Secrets Manager.
- `page-code/registration-page.js` - Wix page code that receives messages from the HTML component and calls the backend.
- `html-component/registration-form.html` - HTML Component markup for the registration form. It does not contain the Make webhook URL or API key.
- `scripts/validate_wix_velo_package.py` - Local safety checks for this package.

## Wix Secrets

Create these secrets in Wix Secrets Manager:

- `MAKE_WEBHOOK_URL` - the Make webhook URL for scenario `5458320`.
- `MAKE_WEBHOOK_API_KEY` - a long random shared key. Use the same value in the Make filter.

Do not put either value in the HTML component or frontend page code.

## Wix Setup

1. Enable Velo in the Wix site.
2. Add an HTML Component to the registration page.
3. Set the HTML Component element ID to `registrationHtml`.
4. Paste `html-component/registration-form.html` into the HTML Component.
5. Replace the placeholder logo URL in the HTML component with the uploaded Wix media URL for the Plan-T logo.
6. Add `backend/registration.web.js` as `backend/registration.web.js`.
7. Paste `page-code/registration-page.js` into the registration page code.
8. Add the two Wix secrets listed above.
9. Publish the Wix site.

## Make Setup

Keep scenario `5458320` as the only Make scenario changed for this flow.

After Wix is published and a test submission reaches Make, add a filter immediately after the webhook:

- Header/key source: `x-api-key` from the incoming webhook bundle.
- Expected value: the same value stored in Wix secret `MAKE_WEBHOOK_API_KEY`.

Only enable this filter after the Wix page is live. Enabling it before Wix is live will intentionally block the current direct GitHub Pages form because that form cannot send a secret header safely.

## Verification

Run locally:

```powershell
py wix-velo\scripts\validate_wix_velo_package.py
```

Then verify in Wix/Make:

1. Submit a registration from the Wix page with a selected topic.
2. Confirm a new row appears in the Google Sheet.
3. Confirm the confirmation email is received.
4. Submit a request without the correct `x-api-key` directly to Make and confirm the scenario stops at the filter.
