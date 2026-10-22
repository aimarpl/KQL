# Contributing

## Query organization

Place each `.kql` query in the directory matching its target platform:

- `sentinel/`
- `defender-xdr/`
- `azure-data-explorer/`
- `shared/`

Use lowercase kebab-case filenames, for example `failed-sign-ins-by-country.kql`.

## Required query header

Begin every query with this metadata block:

```kusto
// Title: Failed sign-ins by country
// Platform: Microsoft Sentinel / Log Analytics
// Description: Summarizes failed sign-ins by source country.
// Data sources: SigninLogs
// Parameters: Update the time range when needed.
```

Allowed `Platform` values are:

- `Microsoft Sentinel / Log Analytics`
- `Microsoft Defender XDR / Advanced Hunting`
- `Azure Data Explorer`
- `Multiple` — list the verified platforms in a following comment

## Style

- Format pipelines one operator per line when it improves readability.
- Put environment-specific constants near the top and explain them.
- Use descriptive projected column names.
- Add comments for unusual joins, parsing expressions, or performance tradeoffs.
- Do not include tenant-specific or sensitive values.

## Commits and pull requests

Use Conventional Commits, such as:

- `feat(sentinel): add risky sign-in query`
- `fix(defender-xdr): correct device join key`
- `docs: clarify query metadata requirements`

Small corrections may be committed directly to `main`. Use a pull request for larger additions or structural changes. Pull requests are squash-merged after approval.
