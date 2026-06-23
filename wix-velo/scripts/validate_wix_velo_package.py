from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    backend = read("backend/registration.web.js")
    page_code = read("page-code/registration-page.js")
    html = read("html-component/registration-form.html")
    readme = read("README.md")

    client_text = "\n".join([page_code, html])
    all_text = "\n".join([backend, page_code, html, readme])

    for field in ["name", "company", "email", "phone", "selected_topics", "source"]:
        require(field in backend or field in html, f"Missing required field: {field}", failures)

    require("MAKE_WEBHOOK_URL" in backend, "Backend must read MAKE_WEBHOOK_URL", failures)
    require("MAKE_WEBHOOK_API_KEY" in backend, "Backend must read MAKE_WEBHOOK_API_KEY", failures)
    require("x-api-key" in backend, "Backend must send x-api-key header", failures)
    require("wix-secrets-backend.v2" in backend, "Backend must use Wix Secrets Backend v2", failures)
    require("elevate(secrets.getSecretValue)" in backend, "Backend must elevate getSecretValue", failures)
    require("Permissions.Anyone" in backend, "Backend web method must allow public form submission", failures)
    require("application/x-www-form-urlencoded" in backend, "Backend should preserve current Make form field mapping", failures)

    require("submitRegistration" in page_code, "Page code must call submitRegistration", failures)
    require("#registrationHtml" in page_code, "Page code must target #registrationHtml", failures)
    require("plan-t-registration-submit" in html and "plan-t-registration-submit" in page_code, "HTML and page code message names must match", failures)

    require("hook.us2.make.com/" not in client_text, "Client-side code must not expose Make webhook URL", failures)
    require("hook.us2.make.com/" not in all_text, "Do not commit the Make webhook URL in this package", failures)
    require("MAKE_WEBHOOK_API_KEY" not in html, "HTML must not reference secret names or keys", failures)
    require("x-api-key" not in html, "HTML must not send x-api-key directly", failures)

    require("YOUR_LOGO_FILE.jpg" in html, "HTML component should keep logo URL as an explicit Wix placeholder", failures)
    require("scenario `5458320`" in readme, "README should identify the allowed Make scenario without storing the webhook URL", failures)

    if failures:
      for failure in failures:
          print(f"FAIL: {failure}")
      raise SystemExit(1)

    print("OK: Wix/Velo secure registration package is valid")


if __name__ == "__main__":
    main()
