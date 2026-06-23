from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "SKILL.md", ROOT / "references" / "contract.md"]


def read_all() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in FILES)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    text = read_all()
    failures: list[str] = []
    required = [
        "{{4.`0`}}",
        "calendar.google.com/calendar/render",
        "outlook.office.com/calendar/0/deeplink/compose",
        "DD/MM/YYYY HH:mm:ss",
        "assets/plan-t-logo.jpg",
        "white/light-blue",
        "UTF-8",
    ]
    for token in required:
        require(token in text, f"Missing required email contract token: {token}", failures)

    lower_text = text.lower()
    require("no fake" in lower_text or "do not include a fake" in lower_text, "Missing fake-link wording", failures)
    require("Do not hard-code a webinar date" in text, "Missing no-hard-coded-date rule", failures)
    require("Do not include a fake Zoom/training URL." in text, "Missing fake-link safety rule", failures)
    require("{{4.`1`}}` must not be used" in text, "Missing training-link-field rule", failures)
    require("yellow" in text.lower(), "Missing yellow-removal contract", failures)

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: plan-t-webinar-email contract is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
