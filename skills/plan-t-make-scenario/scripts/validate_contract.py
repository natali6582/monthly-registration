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
        "scenario 5458320",
        "https://us2.make.com/1621766/scenarios/5458320/edit",
        "Immediately as data arrives",
        "backup",
        "explicit approval",
        "Run once",
        "test emails",
        "live module",
    ]
    for token in required:
        require(token in text, f"Missing required contract token: {token}", failures)

    require("hook.us2.make.com/" not in text, "Skill must not store a full webhook URL", failures)
    require("Do not change any Make scenario except `5458320`." in text, "Missing scenario scope rule", failures)
    require("After import, always re-check scheduling" in text, "Missing post-import schedule verification", failures)

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: plan-t-make-scenario contract is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
