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
        "C:\\Users\\NatalieK\\dev\\monthly-registration",
        "main",
        "work",
        "natali6582/monthly-registration",
        "git status --short --branch",
        "Stage only the intended files",
        "Do not push to `origin`",
        "Do not run `git reset --hard`",
        "backups",
        "outputs",
        ".codex-remote-attachments",
    ]
    for token in required:
        require(token in text, f"Missing required release token: {token}", failures)

    require("Do not stage broad untracked directories" in text, "Missing broad-untracked safety rule", failures)
    require("Do not hide failing validations." in text, "Missing validation safety rule", failures)
    require("Push to the work remote" in text, "Missing work-remote push rule", failures)

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: plan-t-safe-release contract is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
