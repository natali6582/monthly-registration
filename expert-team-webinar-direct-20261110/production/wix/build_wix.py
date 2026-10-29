"""Build the opt-in direct flow while proving the legacy source is preserved."""
import argparse
import hashlib
import json
from pathlib import Path


def build(destination: Path, default_direct: bool = False) -> dict:
    source = Path(__file__).resolve().parent
    event_root = source.parent.parent
    workspace = event_root.parent
    legacy = workspace / "expert-team-webinar-20261110"
    event = json.loads((event_root / "event-preview.json").read_text(encoding="utf-8-sig"))
    legacy_html = (legacy / "form.html").read_bytes()
    legacy_page = (legacy / "wix-page.js").read_bytes()
    direct_ui = (source / "direct-ui.fragment.html").read_bytes()
    assert legacy_html.count(b"</body>") == 1
    html = legacy_html.replace(b"</body>", direct_ui + b"\r\n</body>")
    assert html.replace(direct_ui + b"\r\n", b"", 1) == legacy_html
    entry = b'$w.onReady(() => {\r\n'
    if entry not in legacy_page:
        entry = b'$w.onReady(() => {\n'
    assert legacy_page.count(entry) == 1
    imports = b'import wixLocationFrontend from "wix-location-frontend";\r\nimport { submitDirectExpertRegistration, cancelDirectExpertRegistration } from "backend/expert-team-direct-registration.web";\r\n'
    conditional = b'  if (wixLocationFrontend.query.flow === "direct") {\r\n    initializeDirectFlow($w("#expertsRegistrationHtml"), wixLocationFrontend.query);\r\n    return;\r\n  }\r\n'
    fragment = (source / "direct-page.fragment.js").read_bytes()
    page = imports + legacy_page.replace(entry, entry + conditional, 1) + b"\r\n" + fragment
    assert page[len(imports):].replace(conditional, b"", 1).removesuffix(b"\r\n" + fragment) == legacy_page
    if default_direct:
        # The direct handler is unchanged. No query value can select the retired handler.
        page = imports + b'\r\n$w.onReady(() => {\r\n  initializeDirectFlow($w("#expertsRegistrationHtml"), wixLocationFrontend.query);\r\n});\r\n\r\n' + fragment
        assert b"Calendly" not in page and b"CALENDLY" not in page
        assert b"submitExpertRegistration" not in page
    backend = (source / "backend.template.js").read_text(encoding="utf-8")
    backend = backend.replace("__JOIN_URL__", json.dumps(event["join_url"], ensure_ascii=False)).replace("__EVENT_TITLE__", json.dumps(event["title"], ensure_ascii=False))
    files = {"form.with-direct.html": html, "wix-page.with-direct.js": page, "expert-team-direct-registration.web.js": backend.encode("utf-8")}
    destination.mkdir(parents=True, exist_ok=False)
    for name, content in files.items():
        (destination / name).write_bytes(content)
    manifest = {"files": {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}, "legacy_html_preserved": True, "legacy_page_preserved": not default_direct, "default_direct": default_direct, "flow": "direct", "same_page": "/experts-webinar"}
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--default-direct", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args.out, args.default_direct), indent=2))
