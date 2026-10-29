"""Build webinar email assets without sending mail.

The default ``ics`` mode preserves the legacy email and calendar attachment.
The ``outlook`` mode emits only the styled email: Make must send the separate
Outlook calendar invitation before sending this confirmation. No ICS attachment
is generated in that mode, and cancellation must also cancel the invitation.
"""

import argparse
import html
import json
from pathlib import Path


def fold(line):
    parts = []
    current = ""
    for character in line:
        if len((current + character).encode("utf-8")) > 75:
            parts.append(current)
            current = " "
        current += character
    return "\r\n".join(parts + [current])


def build(event_path, module_id, output, delivery_mode="ics"):
    if delivery_mode not in ("ics", "outlook"):
        raise ValueError("delivery_mode must be 'ics' or 'outlook'")
    event = json.loads(event_path.read_text(encoding="utf-8"))
    row = "{{" + str(module_id) + ".id}}"
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PLAN T//Experts Webinar//HE",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT",
        "UID:plan-t-experts-20261110-" + row + "@plan-t.org.il", "DTSTAMP:__STAMP__",
        "DTSTART:20261110T090000Z", "DTEND:20261110T094500Z",
        "SUMMARY:" + event["title"], "DESCRIPTION:אירוע חשיפת נבחרת המומחים של PLAN T",
        "ORGANIZER:mailto:" + event["sender_email"],
        "LOCATION:" + event["join_url"], "URL:" + event["join_url"],
        "STATUS:CONFIRMED", "SEQUENCE:0", "TRANSP:OPAQUE", "END:VEVENT", "END:VCALENDAR",
    ]
    ics = ("\r\n".join(fold(line) for line in lines) + "\r\n").replace(
        "__STAMP__", '{{formatDate(now; "YYYYMMDD[T]HHmmss[Z]"; "UTC")}}')
    join_url = html.escape(event["join_url"], quote=True)
    cancel_url = "https://www.plan-t.org.il/experts-webinar?flow=direct&amp;cancel={{1.cancelToken}}"
    email = '''<!doctype html>
<html lang="he" dir="rtl" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">
<title>אישור הרשמה לאירוע חשיפת נבחרת המומחים של PLAN T</title>
<style>table,td{mso-table-lspace:0pt;mso-table-rspace:0pt;}table{border-spacing:0;}img{-ms-interpolation-mode:bicubic;}a{text-decoration:none;}@media only screen and (max-width:600px){.outer-pad{padding:16px 10px!important;}.content-pad{padding:26px 22px!important;}.header-pad{padding:26px 18px!important;}.header-title{font-size:23px!important;line-height:32px!important;}.logo-table{width:48px!important;}.logo-image{width:48px!important;height:48px!important;} }</style>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><style>body,table,td,h1,p,a,strong,span{font-family:Arial,sans-serif!important;}table{border-collapse:collapse;}a{text-decoration:none;}</style><![endif]-->
</head>
<body dir="rtl" style="margin:0;padding:0;background-color:#f4f8fc;color:#27425b;font-family:Arial,sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f4f8fc" style="width:100%;background-color:#f4f8fc;font-family:Arial,sans-serif;">
<tr><td class="outer-pad" align="center" style="padding:32px 12px;font-family:Arial,sans-serif;">
<!--[if mso]><table role="presentation" width="640" align="center" cellspacing="0" cellpadding="0" border="0"><tr><td width="640" style="font-family:Arial,sans-serif;"><![endif]-->
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" style="width:100%;max-width:640px;background-color:#ffffff;border:1px solid #e4edf4;border-radius:20px;box-shadow:0 8px 28px rgba(42,84,118,0.08);overflow:hidden;font-family:Arial,sans-serif;">
<tr><td align="center" bgcolor="#bfdccb" style="background-color:#bfdccb;background-image:linear-gradient(90deg,#bfdfe7 0%,#badb9d 100%);border-radius:20px 20px 0 0;font-family:Arial,sans-serif;">
<!--[if mso]><v:rect fill="true" stroke="false" style="width:640px;height:220px;"><v:fill type="gradient" color="#bfdfe7" color2="#badb9d" angle="90"/><v:textbox inset="0,0,0,0" style="mso-fit-shape-to-text:true;"><![endif]-->
<table role="presentation" width="100%" align="center" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td class="header-pad" align="center" style="padding:24px 26px;text-align:center;font-family:Arial,sans-serif;">
<table role="presentation" width="100%" align="center" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;">
<tr><td align="center" style="text-align:center;font-family:Arial,sans-serif;">
<table class="logo-table" role="presentation" width="56" align="center" cellspacing="0" cellpadding="0" border="0" style="width:56px;margin:0 auto;font-family:Arial,sans-serif;"><tr><td align="center" style="text-align:center;font-family:Arial,sans-serif;"><img class="logo-image" src="https://static.wixstatic.com/media/88ee62_4361485f42f94da89c506f97f9a109e4~mv2.png" alt="PLAN-T" width="56" height="56" style="display:block;margin:0 auto;border:0;outline:none;width:56px;height:56px;"></td></tr></table>
</td></tr>
<tr><td height="14" align="center" style="height:14px;font-family:Arial,sans-serif;font-size:1px;line-height:14px;mso-line-height-rule:exactly;">&nbsp;</td></tr>
<tr><td dir="rtl" align="center" style="text-align:center;font-family:Arial,sans-serif;color:#24455f;">
<h1 class="header-title" style="margin:0;font-family:Arial,sans-serif;font-size:26px;line-height:36px;font-weight:700;color:#24455f;mso-line-height-rule:exactly;">חשיפת נבחרת המומחים של <span dir="ltr" style="white-space:nowrap;font-family:Arial,sans-serif;">PLAN&nbsp;T</span></h1>
<p style="margin:10px 0 0;font-family:Arial,sans-serif;font-size:14px;line-height:22px;font-weight:400;color:#385c78;mso-line-height-rule:exactly;">אישור הרשמה לאירוע</p>
</td></tr></table></td></tr></table>
<!--[if mso]></v:textbox></v:rect><![endif]-->
</td></tr>
<tr><td class="content-pad" dir="rtl" align="center" style="padding:32px 38px 28px;text-align:center;font-family:Arial,sans-serif;color:#27425b;">
<p style="margin:0 0 12px;font-family:Arial,sans-serif;font-size:22px;line-height:30px;font-weight:700;color:#24455f;mso-line-height-rule:exactly;">ההרשמה הושלמה</p>
<p style="margin:0 0 24px;font-family:Arial,sans-serif;font-size:16px;line-height:26px;color:#64788b;mso-line-height-rule:exactly;">נשמח לראותך באירוע חשיפת נבחרת המומחים של PLAN T.</p>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td align="center" style="padding:0 0 25px;text-align:center;font-family:Arial,sans-serif;">
<p style="margin:0 0 6px;font-family:Arial,sans-serif;font-size:14px;line-height:22px;color:#6d8092;mso-line-height-rule:exactly;">יום שלישי</p>
<p style="margin:0;font-family:Arial,sans-serif;font-size:20px;line-height:30px;font-weight:700;color:#24455f;mso-line-height-rule:exactly;"><strong style="font-family:Arial,sans-serif;font-size:20px;line-height:30px;color:#24455f;">10.11.2026&nbsp;&nbsp;|&nbsp;&nbsp;<span dir="ltr" style="font-family:Arial,sans-serif;white-space:nowrap;">11:00</span></strong></p>
<p style="margin:3px 0 0;font-family:Arial,sans-serif;font-size:13px;line-height:20px;color:#8091a1;mso-line-height-rule:exactly;">לפי שעון ישראל</p>
</td></tr></table>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td align="center" bgcolor="#0879cf" style="background-color:#0879cf;border-radius:8px;text-align:center;font-family:Arial,sans-serif;">
<a href="''' + join_url + '''" style="display:block;padding:16px 16px;border:1px solid #0879cf;border-radius:8px;font-family:Arial,sans-serif;font-size:18px;line-height:24px;font-weight:700;color:#ffffff;text-align:center;text-decoration:none;mso-padding-alt:0;"><!--[if mso]><i style="letter-spacing:16px;mso-font-width:-100%;mso-text-raise:24pt;">&nbsp;</i><![endif]--><span style="font-family:Arial,sans-serif;color:#ffffff;mso-text-raise:12pt;">כניסה לוובינר ב־Zoom</span><!--[if mso]><i style="letter-spacing:16px;mso-font-width:-100%;">&nbsp;</i><![endif]--></a>
</td></tr></table>
<p style="margin:12px 0 25px;font-family:Arial,sans-serif;font-size:13px;line-height:21px;color:#8091a1;mso-line-height-rule:exactly;">אפשר לשמור את המייל ולחזור לקישור ביום האירוע.</p>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#edf7fd" style="width:100%;background-color:#edf7fd;border:1px solid #dcecf7;border-radius:10px;font-family:Arial,sans-serif;"><tr><td align="center" dir="rtl" style="padding:22px 18px;text-align:center;font-family:Arial,sans-serif;color:#385c78;">
<p style="margin:0 0 9px;font-family:Arial,sans-serif;font-size:17px;line-height:25px;font-weight:700;color:#385c78;mso-line-height-rule:exactly;"><strong style="font-family:Arial,sans-serif;font-size:17px;line-height:25px;color:#385c78;">הוספה ליומן Outlook או Google</strong></p>
<p style="margin:0;font-family:Arial,sans-serif;font-size:15px;line-height:25px;color:#526f87;mso-line-height-rule:exactly;">פתחו את קובץ היומן המצורף למייל.</p>
<p style="margin:4px 0 0;font-family:Arial,sans-serif;font-size:13px;line-height:22px;color:#7890a3;mso-line-height-rule:exactly;">ייתכן שיידרש אישור להוספת האירוע ביומן שלכם.</p>
</td></tr></table>
<p style="margin:24px 0 5px;font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#8294a3;mso-line-height-rule:exactly;">אם הכפתור אינו נפתח, אפשר להשתמש בקישור:</p>
<p dir="ltr" style="margin:0;font-family:Arial,sans-serif;font-size:12px;line-height:20px;word-break:break-all;mso-line-height-rule:exactly;"><a dir="ltr" href="''' + join_url + '''" style="font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#1899b4;text-decoration:underline;word-break:break-all;">''' + join_url + '''</a></p>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td align="center" style="padding:24px 0 0;font-family:Arial,sans-serif;"><table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;border-top:1px solid #e8eff4;font-family:Arial,sans-serif;"><tr><td align="center" style="padding:19px 0 0;font-family:Arial,sans-serif;">
<p style="margin:0 0 10px;font-family:Arial,sans-serif;font-size:13px;line-height:22px;color:#71879a;mso-line-height-rule:exactly;">לשאלות: <a href="mailto:supportclient@plan-t.org.il" style="font-family:Arial,sans-serif;font-size:13px;line-height:22px;color:#1899b4;text-decoration:none;">supportclient@plan-t.org.il</a></p>
<p style="margin:0 0 8px;font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#8294a3;mso-line-height-rule:exactly;"><a href="''' + cancel_url + '''" style="font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#71879a;text-decoration:underline;">לביטול ההרשמה</a></p>
<p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:11px;line-height:18px;color:#97a6b3;mso-line-height-rule:exactly;">אם הוספתם את האירוע ליומן, לאחר ביטול ההרשמה יש להסיר אותו גם מהיומן.</p>
<p style="margin:0;font-family:Arial,sans-serif;font-size:14px;line-height:23px;font-weight:700;color:#55718a;mso-line-height-rule:exactly;">נתראה באירוע,<br>צוות PLAN T</p>
</td></tr></table></td></tr></table>
</td></tr></table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table></body></html>
'''
    if delivery_mode == "outlook":
        calendar_copy = {
            "הוספה ליומן Outlook או Google": "הזמנה ליומן",
            "פתחו את קובץ היומן המצורף למייל.": "הזמנה ליומן נשלחה אליכם במייל נפרד.",
            "ייתכן שיידרש אישור להוספת האירוע ביומן שלכם.": "לאישור ההשתתפות ולהוספה ליומן, פתחו את ההזמנה ואשרו אותה.",
            "אם הוספתם את האירוע ליומן, לאחר ביטול ההרשמה יש להסיר אותו גם מהיומן.": "ביטול ההרשמה דרך הקישור ישלח אליכם גם הודעת ביטול להזמנה ביומן.",
        }
        for original, replacement in calendar_copy.items():
            if email.count(original) != 1:
                raise ValueError("Expected exactly one legacy calendar instruction")
            email = email.replace(original, replacement)
    output.mkdir(parents=True, exist_ok=False)
    if delivery_mode == "ics":
        (output / "calendar-template.ics.txt").write_bytes(ics.encode("utf-8"))
    (output / "email-template.html").write_bytes(email.encode("utf-8"))
    sample = ics.replace(row, "3317000000").replace('{{formatDate(now; "YYYYMMDD[T]HHmmss[Z]"; "UTC")}}', "20261029T110000Z")
    assert all(len(line.encode("utf-8")) <= 75 for line in sample.split("\r\n"))
    assert "ATTENDEE" not in sample and "ORGANIZER:mailto:sales@plan-t.org.il" in sample
    assert "Calendly" not in email and "calendly.com" not in email
    if delivery_mode == "ics":
        print(json.dumps({"files": 2, "calendar_bytes": len(ics.encode("utf-8")), "preview_markers": False}))
    else:
        print(json.dumps({"files": 1, "delivery_mode": "outlook", "calendar_attachment": False, "separate_calendar_invitation_required": True, "preview_markers": False}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--row-module", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--delivery-mode", choices=("ics", "outlook"), default="ics")
    args = parser.parse_args()
    build(args.event, args.row_module, args.output, args.delivery_mode)


if __name__ == "__main__":
    main()
