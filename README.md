# KQL Query Library

Reusable Kusto Query Language (KQL) queries for multiple Microsoft platforms.

## Supported platforms

- Microsoft Sentinel and Log Analytics
- Microsoft Defender XDR Advanced Hunting
- Azure Data Explorer

Every `.kql` file must identify its target platform in a `// Platform:` header. Queries that work on more than one platform should list each supported platform.

## Suggested layout

- `sentinel/` — Microsoft Sentinel and Log Analytics queries
- `defender-xdr/` — Microsoft Defender XDR Advanced Hunting queries
- `azure-data-explorer/` — Azure Data Explorer queries
- `shared/` — queries verified on multiple platforms

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required query header and publishing workflow.
