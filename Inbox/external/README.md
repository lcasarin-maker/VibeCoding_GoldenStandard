# Inbox / External

Place community or issue/PR-derived findings here.

Use `../templates/external_contribution.md` as the source of truth and name files with the canonical pattern:

```text
YYYY-MM-DD_gh<issue-or-pr>_<slug>.md
```

External submissions are triaged by maintainers before they are promoted to the Golden Standard catalogs.
Submissions that depend on retired `00 audit` artifacts, stale snapshots, or pre-purge states are not valid external evidence; they must be reworked against the active baseline and include fresh purge proof when they claim cleanup, completeness, or repo hygiene.
If the submission only shows that an old test suite passes, the maintainer must reject it or return it as `NEEDS_INFO` until it is re-targeted to the current Cerberus baseline and backed by functional evidence.
