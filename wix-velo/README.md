# Plan-T Wix/Velo Secure Registration Flow

This package moves Plan-T registration submission away from direct static HTML-to-Make posting.

## Files

- `backend/registration.web.js` - Wix backend web module. Stores all Make access behind Wix Secrets Manager.
- `page-code/registration-page.js` - Wix page code that receives messages from the HTML component and calls the backend.
- `html-component/registration-form.html` - HTML Component markup for the registration form. It does not contain the Make webhook URL or API key.
- `automation-actions/MONDAY-HJ.js` - Custom action for the separate native Wix Form automation. Creates one Monday item without embedding credentials or account-specific IDs in source.
- `scripts/validate_wix_velo_package.py` - Local safety checks for this package.

## Wix Secrets

Create these secrets in Wix Secrets Manager:

- `MAKE_WEBHOOK_URL` - the Make webhook URL for scenario `5458320`.
- `MAKE_WEBHOOK_API_KEY` - a long random shared key. Use the same value in the Make filter.
- `MONDAY_API_TOKEN` - a newly rotated Monday API token. Never reuse a token that has appeared in source code.
- `MONDAY_REGISTRATION_CONFIG` - the JSON configuration for the native Wix Form automation action.

Do not put any of these values in the HTML component, frontend page code, or
automation source.

Use this shape for `MONDAY_REGISTRATION_CONFIG`, replacing every placeholder
with the matching value from the target Monday board and replacing the example
`statusIndex` value with the board's actual integer status index:

```json
{
  "boardId": "<BOARD_ID>",
  "groupId": "<GROUP_ID>",
  "columns": {
    "phone": "<PHONE_COLUMN_ID>",
    "email": "<EMAIL_COLUMN_ID>",
    "company": "<COMPANY_COLUMN_ID>",
    "registrationDate": "<REGISTRATION_DATE_COLUMN_ID>",
    "status": "<STATUS_COLUMN_ID>"
  },
  "statusIndex": 0,
  "countryShortName": "IL"
}
```

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

## Native Wix Form Automation

This is a separate, currently inactive flow. It must not replace or modify the
verified live HTML Component → Make scenario `5595814` flow.

1. Open automation `193c589f-1b2f-4d22-a105-e2d475c7b71f`.
2. Keep the trigger attached to the intended native Wix Form.
3. Open the **Run Velo Code** action.
4. Replace the action code with `automation-actions/MONDAY-HJ.js`.
5. Add the two Monday secrets before running the action.
6. Save the action.
7. Use a controlled test submission before activating the automation.

Running the custom action test is a live Monday mutation. Use a clearly marked
test registration and remove the resulting test item after verification.

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
