# Diagnosis: Wix Run Velo Code Action

Date: 2026-07-26

## Confirmed failure

Automation `193c589f-1b2f-4d22-a105-e2d475c7b71f` is inactive and uses a Wix
Forms `Form submitted` trigger followed by `Send an email` and `Run Velo code`.
The selected Velo file is `MONDAY-HJ.js`.

The action currently exports:

```javascript
export async function createMondayItem(formData)
```

Wix Run Velo Code custom actions call the service plugin's `invoke()` method.
The current action therefore does not expose the entry point Wix invokes.
Passing `node --check` only proves JavaScript syntax; it does not validate the
Wix service-plugin contract.

Official references:

- https://dev.wix.com/docs/develop-websites/articles/coding-with-velo/automations/about-custom-actions
- https://dev.wix.com/docs/velo/events-service-plugins/automations/service-plugins/automations-actions/invoke

## Confirmed payload

The Wix Payload view includes the dynamic keys:

- `field:fullName`
- `field:role`
- `field:company`
- `field:phone`
- `field:email`
- `field:topics`

Bracket notation is required for these colon-containing keys. The earlier
change from `formData.name` to `formData['field:fullName']` was directionally
correct but did not fix the missing `invoke()` entry point.

## Additional blocking risks

1. A real Monday token is hard-coded in both the local handoff file and the Wix
   action. It must be revoked and replaced with a Wix Secrets Manager value.
2. The action interpolates the submitted name directly into GraphQL source,
   allowing quotes, backslashes, or line breaks to break the mutation.
3. HTTP errors are not checked.
4. Monday GraphQL can return an `errors` array in a successful HTTP response;
   the current action logs and returns it as if item creation succeeded.
5. Required payload fields are not validated.
6. The Wix sample data contains field-name placeholders rather than realistic,
   unique test values.
7. The email action precedes Monday creation, so a downstream Monday failure
   can occur after the registrant email step.

## Scope lock

- No Wix code, automation configuration, Make scenario, Monday item, email, or
  GitHub branch was changed.
- The verified live flow using Make scenario `5595814` remains out of scope.
- The next approved step is RED only: behavioral tests that reproduce the
  missing entry point and the unsafe/error-handling cases before implementation.

## Found, not fixed

The direct Wix-to-Monday action duplicates integration logic already present in
Make. A later architecture decision should consider routing the native Wix Form
through an isolated clone of the working Make flow. This is not part of the
current repair.
