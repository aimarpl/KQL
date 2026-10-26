# Identity - MFA

Queries for analysing multifactor authentication usage in Microsoft Entra ID.

**Platform:** Microsoft Sentinel / Log Analytics
**Data source:** `SigninLogs`

## Queries

| Query                                                                    | Purpose                                                             |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| [authentication-method-usage.kql](authentication-method-usage.kql)       | Which methods are in use tenant-wide, and by how many users         |
| [users-relying-on-sms-or-voice.kql](users-relying-on-sms-or-voice.kql)   | Migration worklist: users with no stronger method than SMS or voice |
| [users-by-authentication-method.kql](users-by-authentication-method.kql) | Drill into one method group and list its users                      |

Typical order: start with the usage summary to see the shape of the tenant,
use the SMS/voice query to build the migration list, then drill into any
individual method with the third query.

## Reading `AuthenticationDetails`

Every row in `SigninLogs` carries an `AuthenticationDetails` array with one
entry per authentication **step**. A single sign-in can contain several steps —
a password, then an MFA prompt — so the array must be expanded with `mv-expand`
before methods can be counted.

Four details decide whether the numbers mean anything:

**Filter on `succeeded`.** Each step records its own result. Without
`where tobool(AuthStep.succeeded) == true`, a user who failed an SMS prompt and
then completed the sign-in with an authenticator app is counted as an SMS user.

**`ResultType == "0"` is the sign-in result.** It is separate from the per-step
`succeeded` flag. Use both when reporting on real-world usage: the step
succeeded *and* the overall sign-in succeeded.

**Count users by `UserId`, never by `Identity`.** `Identity` is the display
name. Two people called the same thing collapse into one row, and a renamed
user splits into two. `UserId` is the directory object ID and is stable.

**`Password` and `Previously satisfied` are not MFA methods.** The first is the
primary factor. The second means Entra accepted an MFA claim the session
already held — a real sign-in, but no method was exercised, so counting it as
method usage overstates adoption.

## Method names

Entra reports method names as display strings, and they change as features
ship. The documented list has been incomplete in the past, so treat any
classification list as something to verify against your own tenant:

```kusto
SigninLogs
| where TimeGenerated > ago(30d)
| mv-expand AuthStep = parse_json(AuthenticationDetails)
| extend RawMethod = tostring(AuthStep.authenticationMethod)
| summarize Steps = count() by RawMethod
| order by Steps desc
```

Run that first. Any name it returns that does not appear in a query's `case()`
block is a gap in that query.

`users-relying-on-sms-or-voice.kql` reports unmatched names in an
`UnclassifiedMethods` column for exactly this reason: an unrecognised method
must not be allowed to look like weak authentication.

## Known limitations

- **Interactive sign-ins only.** `SigninLogs` holds interactive sign-ins.
  Non-interactive sign-ins live in `AADNonInteractiveUserSignInLogs` and are
  not covered here; they rarely carry a user-exercised MFA method.
- **`dcount` is approximate.** Fine for adoption trends. For an exact figure in
  a small result set, use `dcount(..., 4)` or `count_distinct()`.
- **Guests and service accounts are included.** Filter by
  `UserType`, `UserPrincipalName` suffix or group membership if your report
  should cover employees only.
- **Retention bounds the window.** A 30-day lookback needs at least 30 days of
  `SigninLogs` retention in the workspace.
