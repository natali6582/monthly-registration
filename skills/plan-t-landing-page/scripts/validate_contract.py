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
        "wix-training-landing.html",
        "dist/index.html",
        "assets/plan-t-logo.jpg",
        "https://natali6582.github.io/monthly-registration/",
        "name",
        "company",
        "email",
        "phone",
        "selected_topics",
        "source",
        "dist",
    ]
    for token in required:
        require(token in text, f"Missing required landing-page token: {token}", failures)

    require("Make a backup before editing source or `dist`." in text, "Missing backup rule", failures)
    require("Do not rotate/change the webhook URL" in text, "Missing webhook safety rule", failures)
    require("Do not add a fake training-entry link." in text, "Missing fake-link safety rule", failures)
    require("hook.us2.make.com/" not in text, "Skill must not store a full webhook URL", failures)

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: plan-t-landing-page contract is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
