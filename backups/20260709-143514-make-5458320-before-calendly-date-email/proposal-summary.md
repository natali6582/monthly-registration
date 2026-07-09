# Make 5458320 proposal - Calendly date email

Scope: local proposal only. No live Make changes were saved.

Planned changes in this copied blueprint:
- Module 31 Calendly availability starts at addMinutes(now; 5) to avoid booking a slot that is already in the past.
- Module 32 still creates the Calendly invitee using the first available start_time returned by Calendly.
- Email body shows the same selected Calendly start_time, formatted as DD/MM/YYYY HH:mm in Asia/Jerusalem.
- Email uses a small PLAN-T logo: 72px wide.
- Email contains no Calendly selection link, no fake Zoom link, and no Google Sheets date token.
- Monday mapping remains unchanged: date_mm50szvs is תאריך הרשמה and receives now.

Files:
- scenario-blueprint-proposal-calendly-date-email.json
- email-preview-calendly-date.html
