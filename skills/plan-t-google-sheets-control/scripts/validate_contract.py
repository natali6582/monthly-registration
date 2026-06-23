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
        "1KVnCH206v5Bq4LT-cuTncBrvJwD5TcV1_zQwP2sOkeE",
        "הדרכה פעילה",
        "הרשמה לוובינר",
        "תאריך ההדרכה",
        "קישור להדרכה",
        "פעיל",
        "DD/MM/YYYY HH:mm:ss",
        "Do not publish registrant personal data",
    ]
    for token in required:
        require(token in text, f"Missing required sheet contract token: {token}", failures)

    require("Do not change sharing permissions" in text, "Missing sharing-permission safety rule", failures)
    require("Do not delete sheet tabs" in text, "Missing no-delete safety rule", failures)
    require("one active row" in text.lower(), "Missing single-active-row rule", failures)

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OK: plan-t-google-sheets-control contract is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
