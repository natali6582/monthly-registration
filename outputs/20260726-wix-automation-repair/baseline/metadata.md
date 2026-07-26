# Wix Automation Repair Baseline

Captured: 2026-07-26, Asia/Jerusalem

## Rollback anchors

- Repository: `natali6582/monthly-registration`
- Upstream branch: `main`
- Upstream and cloned HEAD: `972ee41c8ca2ec704af2e8485f0514ef748ecbc5`
- Local rollback tag: `codex-baseline-20260726`
- Local work branch: `codex/wix-automation-repair-20260726`
- Wix automation: `193c589f-1b2f-4d22-a105-e2d475c7b71f`
- Wix automation status when inspected: `INACTIVE`
- Redacted code snapshot: `MONDAY-HJ.redacted.js`

The GitHub default branch and the live Wix/Make flow were not changed. No branch,
tag, commit, or file from this work copy was pushed to GitHub.

## Secret handling

The source `MONDAY-HJ.js` contains a real Monday token. The token was not copied
into this repository. The redacted snapshot preserves the surrounding code for
comparison while replacing the token. The original source file is identified by
hash only:

- Original local Velo file SHA-256:
  `5773db957fadd3eb5d29397a14adf548de2e114f206cd275d058297203399fde`
- A current-branch GitHub code search for the observed JWT prefix returned zero
  matches.

The exposed token must be revoked and replaced before any live test.

## Input hashes

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `PROJECTSUMMARY.md` | 7,437 | `b6b686ce4396c1e0fd5a3b6ccf54b8adce8bcc248ce020e6da37c91b31b470dc` |
| Local Velo source | 1,684 | `5773db957fadd3eb5d29397a14adf548de2e114f206cd275d058297203399fde` |
| `sample data.txt` | 2,365 | `20b9fab91004920598546059938fa7d51f339fb1ddb61c82a6f8b1342cd17146` |
| `SearchWixAPISpec.txt` | 25,126 | `f7cf77a401d0582e634ed49d9a078e2781495c57a0fedf9578fa351fa14ce7cc` |
| `ExecuteWixAPI.txt` | 5,375 | `fdde75c4765bb4f77a4b8d5ce11579d2bdb2c6c9d4b538af2a57447b476ca285` |
| `SearchWixRESTDocumentation.txt` | 34,711 | `cef7ab1e40ff8b71847f99d95e3d2aa67613ead78209c26aafde3deff11e8060` |
| `ReadFullDocsArticle.txt` | 14,736 | `729f2b48ebc255e1e098755deff4e1b865d88a94acae20b75a4c6bef62af9d69` |
| `wixredme.txt` | 37,519 | `fd113c8b6c684886b0c43a99eee9c564ed56dab01adeed149624a6172a11713b` |

## Approved future test recipient

If the user separately approves a live test, the only approved recipient is
`natali.koifman@gmail.com`. No email was sent during baseline capture.
