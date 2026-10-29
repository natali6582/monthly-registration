"""Verify emitted Make-template fixtures, not the live Make expression engine."""

import argparse
from datetime import datetime, timezone
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo


def split_arguments(text):
    parts, start, depth, quoted = [], 0, 0, False
    for index, character in enumerate(text):
        if character == '"':
            quoted = not quoted
        elif not quoted:
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
            elif character == ";" and depth == 0:
                parts.append(text[start:index].strip())
                start = index + 1
    if depth or quoted:
        raise ValueError("Unbalanced template expression")
    return parts + [text[start:].strip()]


def evaluate(expression, values):
    expression = expression.strip()
    if expression in values:
        return values[expression]
    if expression == "emptyarray":
        return []
    if expression.startswith('"') and expression.endswith('"'):
        return json.loads(expression)
    if expression.isdigit():
        return int(expression)
    match = re.fullmatch(r"([a-zA-Z]+)\((.*)\)", expression)
    if not match:
        raise ValueError("Unexpected mapping or expression: " + expression)
    function = match.group(1)
    args = [evaluate(arg, values) for arg in split_arguments(match.group(2))]
    if function == "add":
        return args[0] + args[1:]
    if function == "join":
        return args[1].join(args[0])
    if function == "substring":
        return args[0][args[1]:args[2]]
    if function == "escapeHTML":
        return html.escape(args[0], quote=True)
    if function == "parseDate":
        assert args[1:] == ["YYYY-MM-DD HH:mm:ss", "UTC"]
        return datetime.strptime(args[0], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    if function == "formatDate":
        patterns = {"YYYYMMDD[T]HHmmss[Z]": "%Y%m%dT%H%M%SZ", "DD.MM.YYYY": "%d.%m.%Y", "HH:mm": "%H:%M"}
        return args[0].astimezone(ZoneInfo(args[2])).strftime(patterns[args[1]])
    raise ValueError("Unsupported fixture function: " + function)


def render(template, values):
    return re.sub(r"\{\{(.*?)\}\}", lambda match: str(evaluate(match.group(1), values)), template)


class EmailLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attributes):
        if tag == "a":
            self.links.append(dict(attributes).get("href"))

    def handle_data(self, data):
        self.text.append(data)


def verify_fixture(templates, query_module, row_module, trigger_module, date, start, end, expected_date, expected_times, url_length, long_ids=False):
    base = f"{query_module}.body.data.items[1]"
    prefix = "https://us05web.zoom.us/j/00000000000?pwd="
    # A nonexistent meeting ID, containing an ampersand to exercise HTML escaping.
    url = prefix + "a" * (url_length - len(prefix) - 4) + "&x=1"
    assert len(url) == url_length and url.isascii()
    training_id = "12345678901234567890" if long_ids else "3302411216"
    row_id = "98765432109876543210" if long_ids else "3318000000"
    values = {
        base + ".id": training_id,
        "16.date": date, "16.time": start,
        "17.date": date, "17.time": end,
        base + ".zoom[1].url": url, f"{row_module}.id": row_id,
        f"{trigger_module}.cancelToken": "fixture-opaque_token-123",
        "now": datetime(2026, 10, 29, 12, 0, tzinfo=timezone.utc),
    }
    calendar = render(templates["calendar-template.ics.txt"], values)
    email = render(templates["templateemail.html"], values)
    assert "{{" not in calendar + email and "}}" not in calendar + email
    assert calendar.endswith("\r\n")
    assert "\n" not in calendar.replace("\r\n", "")
    line_lengths = [len(line.encode("utf-8")) for line in calendar.split("\r\n")]
    assert max(line_lengths) <= 75, line_lengths
    unfolded = re.sub(r"\r\n[ \t]", "", calendar)
    properties = dict(line.split(":", 1) for line in unfolded.split("\r\n") if ":" in line)
    assert properties["LOCATION"] == url
    assert properties["URL"] == url
    assert properties["METHOD"] == "PUBLISH"
    assert properties["ORGANIZER"] == "mailto:sales@plan-t.org.il"
    assert properties["SUMMARY"] == "הדרכה חודשית PLAN T"
    assert properties["UID"] == f"plan-t-monthly-{training_id}-{row_id}@plan-t.org.il"
    assert properties["DTSTAMP"] == "20261029T120000Z"
    assert properties["DTSTART"] == date.replace("-", "") + "T" + start.replace(":", "") + "Z"
    assert properties["DTEND"] == date.replace("-", "") + "T" + end.replace(":", "") + "Z"
    assert "ATTENDEE:" not in calendar
    parsed = EmailLinks()
    parsed.feed(email)
    assert parsed.links.count(url) == 2
    assert "https://www.plan-t.org.il/monthlyregistration?cancel=fixture-opaque_token-123" in parsed.links
    text = "".join(parsed.text)
    assert expected_date in text and expected_times in text
    for forbidden in ("Calendly", "calendly", "וובינר", "בדיקה", "שלום"):
        assert forbidden not in email
    return {"url_length": url_length, "date": date, "expected_local_time": expected_times, "max_ics_line_bytes": max(line_lengths), "long_ids": long_ids}, calendar, email


def verify(first, second, output):
    names = ["templateemail.html", "calendar-template.ics.txt", "manifest.json"]
    hashes = {}
    for name in names:
        a, b = (first / name).read_bytes(), (second / name).read_bytes()
        assert a == b, name + " differs between clean builds"
        hashes[name] = hashlib.sha256(a).hexdigest()
    manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
    templates = {name: (first / name).read_bytes().decode("utf-8") for name in names[:2]}
    assert "20261105" not in templates["calendar-template.ics.txt"]
    assert "05.11.2026" not in templates["templateemail.html"]
    modules = (manifest["query_module"], manifest["row_module"], manifest["trigger_module"])
    cases = []
    representative = None
    for length in (59, 60, 61, 119, 120, 121, 479, 480):
        case, calendar, email = verify_fixture(templates, *modules, "2026-11-05", "08:00:00", "08:45:00", "05.11.2026", "10:00–10:45", length, length == 480)
        cases.append(case)
        if length == 119:
            representative = (calendar, email)
    for args in (("2026-12-10", "09:30:00", "10:15:00", "10.12.2026", "11:30–12:15"), ("2026-07-15", "07:00:00", "07:45:00", "15.07.2026", "10:00–10:45")):
        case, _, _ = verify_fixture(templates, *modules, *args, 119)
        cases.append(case)
    output.mkdir(parents=True, exist_ok=False)
    (output / "fixture-calendar.ics").write_bytes(representative[0].encode("utf-8"))
    (output / "fixture-email.html").write_bytes(representative[1].encode("utf-8"))
    report = {
        "status": "passed", "clean_builds_byte_identical": True,
        "sha256": hashes, "fixture_count": len(cases), "cases": cases,
        "verified": ["RFC 5545 CRLF and UTF-8 line lengths", "lossless folding at 60-character boundaries and 480-character maximum", "empty continuation segments unfold without changing URL", "HTML-escaped Zoom link reconstructs original URL", "UID matches backend contract including 20-digit IDs", "UTC ICS date/time and Israel email time from same dynamic source", "future date and summer DST are dynamic", "direct cancellation link", "no personalized greeting or test/Calendly/webinar wording"],
        "not_verified": ["Live Make expression evaluation", "Live email sending and delivery", "Calendar-client import"],
    }
    (output / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.first, args.second, args.output), ensure_ascii=False))


if __name__ == "__main__":
    main()
