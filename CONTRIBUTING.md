# Contributing

## Query organization

Queries are grouped by **purpose**, under `queries/<category>/`:

```text
queries/
  identity-mfa/        Multifactor authentication usage and adoption
```

Platform is recorded in each file's header rather than in the folder path, so a
query is found by what it answers and still says where to run it.

Current categories:

| Directory               | Category value   |
| ----------------------- | ---------------- |
| `queries/identity-mfa/` | `Identity - MFA` |

Adding a category:

1. Create `queries/<name>/` with a `README.md` describing the data source, the
   queries in it, and the traps specific to that data.
2. Add the category value to `ALLOWED_CATEGORIES` in
   `tools/validate-kql-metadata.py`.
3. Add a row to the table in the root [README](README.md).

CI fails on a category that is not registered, which keeps the folders, the
validator and the README in step.

Use lowercase kebab-case filenames, for example `users-relying-on-sms-or-voice.kql`.

## Required query header

Begin every query with this metadata block:

```kusto
// Title: Users relying only on SMS or voice
// Platform: Microsoft Sentinel / Log Analytics
// Category: Identity - MFA
// Tags: entra-id, mfa, sms, voice, migration
// Description: Lists users who completed MFA with SMS or voice and never used
//   a stronger method in the period.
// Data sources: SigninLogs
// Parameters: StartTime, EndTime
// Notes: Optional. Anything a reader must know before trusting the output.
```

All of `Title`, `Platform`, `Category`, `Tags`, `Description` and
`Data sources` are required. Continuation lines are indented under their field.

Allowed `Platform` values are:

- `Microsoft Sentinel / Log Analytics`
- `Microsoft Defender XDR / Advanced Hunting`
- `Azure Data Explorer`
- `Multiple` — list the verified platforms in a following comment

### Tags

Lowercase kebab-case, comma separated. Tags cross-cut categories, so a reader
can find every `entra-id` query regardless of where it lives. Use them for:

- the solution or product: `entra-id`, `defender-for-endpoint`, `intune`
- the subject: `mfa`, `sms`, `passkey`, `sign-in-risk`
- the intent: `adoption`, `migration`, `hunting`, `troubleshooting`

## Style

- Declare parameters with `let` at the top, each with a comment explaining it.
  A reader should be able to adapt a query without reading its body.
- Format pipelines one operator per line when it improves readability.
- Use descriptive projected column names: `SuccessfulSteps`, not `c`.
- Comments explain **why** a filter or classification exists. The operator
  itself is already readable; the reason it is there is not.
- Prefer one parameterised query over several near-identical copies. A `let`
  that selects the method beats five files differing by one string.
- Do not include tenant-specific or sensitive values.

## Correctness

These queries get used to make decisions about real users, so:

- Filter authentication steps on `succeeded` as well as the sign-in
  `ResultType`. A failed prompt is not evidence that a method is in use.
- Identify users by `UserId`, never by display name. Display names are neither
  unique nor stable.
- Classify every value before filtering it. Narrowing the rows first and
  aggregating second is how a user with a strong method ends up on a
  weak-method report.
- Surface unmatched values in a column rather than letting them fall into a
  bucket silently. Microsoft adds method names over time.
- State the limitations in the category README: what the data source excludes,
  where an approximation is used, and who is in scope.

## No environment-specific values

Use placeholders: `contoso.com`, `jdoe@contoso.com`,
`00000000-0000-0000-0000-000000000000`. Never commit tenant or subscription
identifiers, workspace names, internal host names, real user names, or sample
output containing them. Sanitise pasted results as carefully as query text.

## Validation

```bash
python3 tools/validate-kql-metadata.py queries
npx --yes markdownlint-cli2 "**/*.md"
```

Both run in CI on every push and pull request.

Syntax is not checked in CI, since that needs the Kusto language service. Run a
query in the target console before publishing it, and say in the header whether
it was verified against real data or only reviewed.

## Commits and pull requests

Use Conventional Commits, such as:

- `feat(identity-mfa): add passkey adoption query`
- `fix(identity-mfa): count users by object ID`
- `docs: clarify tag conventions`

Small corrections may be committed directly to `main`. Use a pull request for
larger additions or structural changes. Pull requests are squash-merged after
approval.
