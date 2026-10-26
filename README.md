# KQL Query Library

Reusable Kusto Query Language (KQL) queries for Microsoft security and
monitoring platforms.

## Supported platforms

- Microsoft Sentinel and Log Analytics
- Microsoft Defender XDR Advanced Hunting
- Azure Data Explorer

Every `.kql` file identifies its target platform in a `// Platform:` header.
Queries verified on more than one platform use `Multiple` and list each one.

## Organization

Queries are grouped by **purpose**, not by platform, because that is how they
are looked for: you know what you want to find out before you know which
console you will run it in. Each query declares its platform in its header, and
each category folder has a README explaining the data source and its pitfalls.

```text
queries/
  identity-mfa/        Multifactor authentication usage and adoption
tools/
  validate-kql-metadata.py
```

| Category                              | Scope                                           | Platform                 |
| ------------------------------------- | ----------------------------------------------- | ------------------------ |
| [identity-mfa](queries/identity-mfa/) | MFA method usage, adoption, migration worklists | Sentinel / Log Analytics |

New categories are added as the library grows. The allowed category values live
in `tools/validate-kql-metadata.py` and are enforced in CI, so a typo cannot
quietly create a stray category.

## Query metadata

Every `.kql` file begins with a header that makes it findable:

```kusto
// Title: Users relying only on SMS or voice
// Platform: Microsoft Sentinel / Log Analytics
// Category: Identity - MFA
// Tags: entra-id, mfa, sms, voice, migration
// Description: Lists users who completed MFA with SMS or voice and never used
//   a stronger method in the period.
// Data sources: SigninLogs
// Parameters: StartTime, EndTime
```

`Platform` says where it runs, `Category` says what it is for, and `Tags`
describe the solution and subject so related queries can be found across
categories.

## Using a query

1. Read the category README for the data source and its caveats.
2. Copy the `.kql` file into the query window for the platform named in its
   header.
3. Adjust the parameters at the top — they are declared with `let` in the first
   few lines.
4. Replace placeholder values such as `contoso.com` with your own.

## Validation

```bash
python3 tools/validate-kql-metadata.py queries
```

CI runs this on every push and pull request, alongside Markdown linting.

## Conventions

- Lowercase kebab-case filenames: `users-relying-on-sms-or-voice.kql`.
- Parameters declared with `let` at the top of the file, each with a comment
  explaining what it does.
- Placeholders only: `contoso.com`, `jdoe@contoso.com`, zero GUIDs. No tenant
  identifiers, internal host names or real user data.
- Comments explain **why** a filter or classification exists, not what the
  operator does.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full header specification and
publishing workflow.

## License

[MIT](LICENSE)
