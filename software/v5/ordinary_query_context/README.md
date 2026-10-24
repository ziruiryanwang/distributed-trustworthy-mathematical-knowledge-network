# Prepare a formal search using your checked local context

This adapter removes manual symbol-ID entry from the existing formal-query
workflow. It is a development component, not a new mathematical acceptance rule.
The selected integrated package and current evidence are listed in
[CURRENT](../ordinary_distribution/CURRENT.md).

First produce the desired formal type with the existing `OwnerQueryCommand`
in an approved local Lean project. No proof or result name is required; see
[the original query interface](../ordinary_query_package/README.md).

Then call the selected package's `query.py` with its existing runtime/profile,
finite resource and fresh-output arguments, using:

```text
--native-type <saved type JSON>
--context-root <exact checked local context ID>
--catalog <existing catalog directory>
--custody <existing custody directory>
--store-id <existing store ID>
--custody-limits <selected limits JSON>
```

Do not supply `--bindings` in this mode. Manual bindings remain supported as
the alternative; the context/store arguments are then omitted. The adapter
does not initialize a store, fetch data, run Lean, or accept a theorem.

For each referenced name, the adapter obtains its exact portable symbol ID
from the selected local context. It writes `BINDINGS.json`, `QUERY.json`,
`SPECS.json`, and finally `RESULT.json`. Pass the resulting specs to the existing
bounded `peer.py find` operation. Search candidates still require acquisition
and independent mathematical checking before use.

If references are absent, the response lists all absent names and emits no
usable query directory. It does not guess identities or automatically import
dependencies. Invalid context identity, limits, or uncertain closure fails
without a success marker. A failed final publication can report `UNKNOWN`
with the exact attempted result hash; preserve partial output for inspection.

The selected context determines the query's interpretation. Matching names
alone do **not** prove that an unrelated author's project has the same meanings.
This remains syntactic exact-type search, not arbitrary mathematical equivalence
or a guarantee that every useful theorem will be found.

The operation opens the existing owner and custody handles and closes both
before publishing success. Opening can recover abandoned reservations as
interrupted, so this is not a database-read-only promise. Owner operations must
respect the existing exclusive lock. Process/resource supervision and the
trusted local storage/runtime assumptions remain unchanged.

The eleven focused controls cover the actual pure binding helpers and explicitly
inert lifecycle doubles. Actual one-call owner integration has a separate
checkpoint; neither test category establishes search recall or useful growth.
