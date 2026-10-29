"""Build deterministic monthly-training Make templates from module IDs only.

Event dates and Zoom location are Make mappings, never build-time constants.
Output directories must be new so earlier files cannot leak into a build.
"""

import argparse
import hashlib
import json
from pathlib import Path


def iml(expression):
    return "{{" + expression + "}}"


def event_timestamp(base, field):
    # Modules16/17 parse Monday's raw DateValue.value JSON. DateValue.time is
    # user-timezone-adjusted and must never be interpreted as UTC.
    parsed = "16" if field == "start" else "17"
    return (
        f'parseDate(join(add(emptyarray; {parsed}.date; '
        f'{parsed}.time); " "); "YYYY-MM-DD HH:mm:ss"; "UTC")'
    )


def format_event(base, field, pattern, timezone):
    return iml(f'formatDate({event_timestamp(base, field)}; "{pattern}"; "{timezone}")')


def fold_static(line):
    """RFC 5545 folding, counting UTF-8 octets including continuation space."""
    parts = []
    current = ""
    for character in line:
        if len((current + character).encode("utf-8")) > 75:
            parts.append(current)
            current = " "
        current += character
    return "\r\n".join(parts + [current])


def url_property(name, reference):
    # Production validation limits the URL to 480 ASCII characters and excludes
    # TEXT delimiters/backslash/newlines. Empty tail segments are valid folds:
    # unfolding each CRLF+space removes them without changing the URL value.
    segments = [iml(f"substring({reference}; {start}; {start + 60})") for start in range(0, 480, 60)]
    return name + ":" + "\r\n ".join(segments)


def make_templates(query_module, row_module, trigger_module):
    base = f"{query_module}.body.data.items[1]"
    zoom_reference = base + ".zoom[1].url"
    uid = "plan-t-monthly-" + iml(base + ".id") + "-" + iml(f"{row_module}.id") + "@plan-t.org.il"
    stamp = iml('formatDate(now; "YYYYMMDD[T]HHmmss[Z]"; "UTC")')
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//PLAN T//Monthly Training//HE",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "BEGIN:VEVENT",
        "UID:" + uid, "DTSTAMP:" + stamp,
        "DTSTART:" + format_event(base, "start", "YYYYMMDD[T]HHmmss[Z]", "UTC"),
        "DTEND:" + format_event(base, "end", "YYYYMMDD[T]HHmmss[Z]", "UTC"),
        fold_static("SUMMARY:הדרכה חודשית PLAN T"),
        fold_static("DESCRIPTION:הדרכה מקצועית במערכת PLAN T"),
        "ORGANIZER:mailto:sales@plan-t.org.il",
        url_property("LOCATION", zoom_reference), url_property("URL", zoom_reference),
        "STATUS:CONFIRMED", "SEQUENCE:0", "TRANSP:OPAQUE", "END:VEVENT", "END:VCALENDAR",
    ]
    calendar = "\r\n".join(lines) + "\r\n"
    date = format_event(base, "start", "DD.MM.YYYY", "Asia/Jerusalem")
    start = format_event(base, "start", "HH:mm", "Asia/Jerusalem")
    end = format_event(base, "end", "HH:mm", "Asia/Jerusalem")
    zoom = iml(f"escapeHTML({zoom_reference})")
    cancel = "https://www.plan-t.org.il/monthlyregistration?cancel=" + iml(f"{trigger_module}.cancelToken")
    email = f'''<!doctype html>
<html lang="he" dir="rtl" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">
<title>אישור הרשמה להדרכה החודשית של PLAN-T</title>
<style>table,td{{mso-table-lspace:0pt;mso-table-rspace:0pt;}}table{{border-spacing:0;}}img{{-ms-interpolation-mode:bicubic;}}a{{text-decoration:none;}}@media only screen and (max-width:600px){{.outer-pad{{padding:16px 10px!important;}}.content-pad{{padding:26px 22px!important;}}.header-pad{{padding:26px 18px!important;}}.header-title{{font-size:23px!important;line-height:32px!important;}}.logo-table{{width:48px!important;}}.logo-image{{width:48px!important;height:48px!important;}} }}</style>
<!--[if mso]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><style>body,table,td,h1,p,a,strong,span{{font-family:Arial,sans-serif!important;}}table{{border-collapse:collapse;}}a{{text-decoration:none;}}</style><![endif]-->
</head>
<body dir="rtl" style="margin:0;padding:0;background-color:#f4f8fc;color:#27425b;font-family:Arial,sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f4f8fc" style="width:100%;background-color:#f4f8fc;font-family:Arial,sans-serif;">
<tr><td class="outer-pad" align="center" style="padding:32px 12px;font-family:Arial,sans-serif;">
<!--[if mso]><table role="presentation" width="640" align="center" cellspacing="0" cellpadding="0" border="0"><tr><td width="640" style="font-family:Arial,sans-serif;"><![endif]-->
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" style="width:100%;max-width:640px;background-color:#ffffff;border:1px solid #e4edf4;border-radius:20px;box-shadow:0 8px 28px rgba(42,84,118,0.08);overflow:hidden;font-family:Arial,sans-serif;">
<tr><td align="center" bgcolor="#b4d2ca" style="background-color:#b4d2ca;background-image:linear-gradient(100deg,#a7c9e2 0%,#acd19c 100%);border-radius:20px 20px 0 0;font-family:Arial,sans-serif;">
<!--[if mso]><v:rect fill="true" stroke="false" style="width:640px;height:240px;"><v:fill type="gradient" color="#a7c9e2" color2="#acd19c" angle="0"/><v:textbox inset="0,0,0,0" style="mso-fit-shape-to-text:true;"><![endif]-->
<table role="presentation" width="100%" align="center" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td class="header-pad" align="center" style="padding:24px 26px;text-align:center;font-family:Arial,sans-serif;">
<table role="presentation" width="100%" align="center" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;">
<tr><td align="center" style="text-align:center;font-family:Arial,sans-serif;">
<table class="logo-table" role="presentation" width="56" align="center" cellspacing="0" cellpadding="0" border="0" style="width:56px;margin:0 auto;font-family:Arial,sans-serif;"><tr><td align="center" style="text-align:center;font-family:Arial,sans-serif;"><img class="logo-image" src="https://static.wixstatic.com/media/88ee62_4361485f42f94da89c506f97f9a109e4~mv2.png" alt="PLAN-T" width="56" height="56" style="display:block;margin:0 auto;border:0;outline:none;width:56px;height:56px;"></td></tr></table>
</td></tr>
<tr><td height="14" align="center" style="height:14px;font-family:Arial,sans-serif;font-size:1px;line-height:14px;mso-line-height-rule:exactly;">&nbsp;</td></tr>
<tr><td dir="rtl" align="center" style="text-align:center;font-family:Arial,sans-serif;color:#ffffff;">
<h1 class="header-title" style="margin:0;font-family:Arial,sans-serif;font-size:26px;line-height:36px;font-weight:700;color:#ffffff;mso-line-height-rule:exactly;">אישור הרשמה להדרכה החודשית של&nbsp;&nbsp;PLAN-T</h1>
<p style="margin:10px 0 0;font-family:Arial,sans-serif;font-size:14px;line-height:22px;font-weight:400;color:#ffffff;mso-line-height-rule:exactly;">כל הפרטים למפגש הקרוב — במקום אחד</p>
</td></tr></table></td></tr></table>
<!--[if mso]></v:textbox></v:rect><![endif]-->
</td></tr>
<tr><td class="content-pad" dir="rtl" align="center" style="padding:32px 38px 28px;text-align:center;font-family:Arial,sans-serif;color:#27425b;">
<p style="margin:0 0 12px;font-family:Arial,sans-serif;font-size:22px;line-height:30px;font-weight:700;color:#24455f;mso-line-height-rule:exactly;">ההרשמה שלך נקלטה בהצלחה</p>
<p style="margin:0 0 24px;font-family:Arial,sans-serif;font-size:16px;line-height:26px;color:#64788b;mso-line-height-rule:exactly;">נשמח לראותך בהדרכה החודשית של PLAN-T.</p>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td align="center" style="padding:0 0 25px;text-align:center;font-family:Arial,sans-serif;">
<p style="margin:0 0 6px;font-family:Arial,sans-serif;font-size:14px;line-height:22px;color:#6d8092;mso-line-height-rule:exactly;">מועד ההדרכה</p>
<p style="margin:0;font-family:Arial,sans-serif;font-size:20px;line-height:30px;font-weight:700;color:#24455f;mso-line-height-rule:exactly;"><strong style="font-family:Arial,sans-serif;font-size:20px;line-height:30px;color:#24455f;">{date}&nbsp;&nbsp;|&nbsp;&nbsp;<span dir="ltr" style="font-family:Arial,sans-serif;white-space:nowrap;">{start}–{end}</span></strong></p>
<p style="margin:3px 0 0;font-family:Arial,sans-serif;font-size:13px;line-height:20px;color:#8091a1;mso-line-height-rule:exactly;">לפי שעון ישראל</p>
</td></tr></table>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td align="center" bgcolor="#0ba3bd" style="background-color:#0ba3bd;border-radius:8px;text-align:center;font-family:Arial,sans-serif;">
<a href="{zoom}" style="display:block;padding:16px 16px;border:1px solid #0ba3bd;border-radius:8px;font-family:Arial,sans-serif;font-size:18px;line-height:24px;font-weight:700;color:#ffffff;text-align:center;text-decoration:none;mso-padding-alt:0;"><!--[if mso]><i style="letter-spacing:16px;mso-font-width:-100%;mso-text-raise:24pt;">&nbsp;</i><![endif]--><span style="font-family:Arial,sans-serif;color:#ffffff;mso-text-raise:12pt;">לכניסה להדרכה ב־Zoom</span><!--[if mso]><i style="letter-spacing:16px;mso-font-width:-100%;">&nbsp;</i><![endif]--></a>
</td></tr></table>
<p style="margin:12px 0 25px;font-family:Arial,sans-serif;font-size:13px;line-height:21px;color:#8091a1;mso-line-height-rule:exactly;">אפשר לשמור את המייל ולחזור לקישור ביום ההדרכה.</p>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#edf7fd" style="width:100%;background-color:#edf7fd;border:1px solid #dcecf7;border-radius:10px;font-family:Arial,sans-serif;"><tr><td align="center" dir="rtl" style="padding:22px 18px;text-align:center;font-family:Arial,sans-serif;color:#385c78;">
<p style="margin:0 0 9px;font-family:Arial,sans-serif;font-size:17px;line-height:25px;font-weight:700;color:#385c78;mso-line-height-rule:exactly;"><strong style="font-family:Arial,sans-serif;font-size:17px;line-height:25px;color:#385c78;">הוספה ליומן Outlook או Google</strong></p>
<p style="margin:0;font-family:Arial,sans-serif;font-size:15px;line-height:25px;color:#526f87;mso-line-height-rule:exactly;">פתחו את קובץ היומן המצורף למייל.</p>
<p style="margin:4px 0 0;font-family:Arial,sans-serif;font-size:13px;line-height:22px;color:#7890a3;mso-line-height-rule:exactly;">ייתכן שיידרש אישור להוספת ההדרכה ביומן שלכם.</p>
</td></tr></table>
<p style="margin:24px 0 5px;font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#8294a3;mso-line-height-rule:exactly;">אם הכפתור אינו נפתח, אפשר להשתמש בקישור:</p>
<p dir="ltr" style="margin:0;font-family:Arial,sans-serif;font-size:12px;line-height:20px;word-break:break-all;mso-line-height-rule:exactly;"><a dir="ltr" href="{zoom}" style="font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#1899b4;text-decoration:underline;word-break:break-all;">{zoom}</a></p>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;font-family:Arial,sans-serif;"><tr><td align="center" style="padding:24px 0 0;font-family:Arial,sans-serif;"><table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:100%;border-top:1px solid #e8eff4;font-family:Arial,sans-serif;"><tr><td align="center" style="padding:19px 0 0;font-family:Arial,sans-serif;">
<p style="margin:0 0 10px;font-family:Arial,sans-serif;font-size:13px;line-height:22px;color:#71879a;mso-line-height-rule:exactly;">לשאלות: <a href="mailto:supportclient@plan-t.org.il" style="font-family:Arial,sans-serif;font-size:13px;line-height:22px;color:#1899b4;text-decoration:none;">supportclient@plan-t.org.il</a></p>
<p style="margin:0 0 8px;font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#8294a3;mso-line-height-rule:exactly;"><a href="{cancel}" style="font-family:Arial,sans-serif;font-size:12px;line-height:20px;color:#71879a;text-decoration:underline;">לביטול ההרשמה</a></p>
<p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:11px;line-height:18px;color:#97a6b3;mso-line-height-rule:exactly;">אם הוספתם את ההדרכה ליומן, לאחר ביטול ההרשמה יש להסיר אותה גם מהיומן.</p>
<p style="margin:0;font-family:Arial,sans-serif;font-size:14px;line-height:23px;font-weight:700;color:#55718a;mso-line-height-rule:exactly;">נתראה בהדרכה,<br>צוות PLAN-T</p>
</td></tr></table></td></tr></table>
</td></tr></table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr></table></body></html>
'''
    return {"templateemail.html": email.encode("utf-8"), "calendar-template.ics.txt": calendar.encode("utf-8")}


def build(query_module, row_module, trigger_module, output):
    if any(value < 1 for value in (query_module, row_module, trigger_module)):
        raise ValueError("Make module IDs must be positive integers")
    templates = make_templates(query_module, row_module, trigger_module)
    output.mkdir(parents=True, exist_ok=False)
    for name, content in templates.items():
        (output / name).write_bytes(content)
    manifest = {
        "query_module": query_module, "row_module": row_module, "trigger_module": trigger_module,
        "files": {name: {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()} for name, content in sorted(templates.items())},
        "calendar_method": "PUBLISH", "sender": "sales@plan-t.org.il",
        "timezone_in_email": "Asia/Jerusalem", "timezone_in_calendar": "UTC",
        "dynamic_event_fields": ["3.body.data.items[1].id", "16.date", "16.time", "17.date", "17.time", "3.body.data.items[1].zoom[1].url"],
        "parsed_date_modules": {"start": 16, "end": 17, "source": "Monday DateValue.value raw UTC JSON"},
        "url_precondition": "HTTPS Zoom URL, ASCII, 1..480 characters, no CR/LF, backslash, comma or semicolon",
        "id_precondition": "Numeric Monday item IDs, each at most 20 digits",
        "cancel_token_precondition": "URL-safe opaque token generated by the Wix backend",
        "runtime_validation": "Fixture tests do not execute Make expressions or send email",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query-module", type=int, default=3)
    parser.add_argument("--row-module", type=int, default=6)
    parser.add_argument("--trigger-module", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.query_module, args.row_module, args.trigger_module, args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()
