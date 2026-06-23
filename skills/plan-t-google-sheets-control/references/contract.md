# Plan-T Google Sheets Control Contract

Required checks:
- Spreadsheet ID: `1KVnCH206v5Bq4LT-cuTncBrvJwD5TcV1_zQwP2sOkeE`.
- Control tab: `הדרכה פעילה`.
- Registration tab: `הרשמה לוובינר`.
- Active flag value: `פעיל`.
- Required control fields: `תאריך ההדרכה`, `קישור להדרכה`, active flag.
- Calendar-safe date format: `DD/MM/YYYY HH:mm:ss`.
- Do not use free text such as "next Thursday" for the date cell.
- Do not publish registrant personal data.

Verification command:

```powershell
py skills\plan-t-google-sheets-control\scripts\validate_contract.py
```
