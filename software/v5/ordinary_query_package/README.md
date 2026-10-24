# Ordinary formal-query package successor

Development integration adopted, 2026-10-23. The selected package is identified by
[ordinary_distribution/CURRENT.md](../ordinary_distribution/CURRENT.md).

Independent saved-output review passes the public type-query, loopback find,
returned-target module export and clean ordinary Lean consumer workflow. It used
the already accepted local owner, not a fresh receiver, and required no certificate
or support rebuild. See the
[outcome](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-QUERY-PUBLIC-OUTCOME.md).

This successor combines exact installed-theorem module reuse with a type-only
query interface. It does not change mathematical admission or require
certificates. Only the search feature namespace changes; old indexes must not
be silently opened as new ones. Re-publication into a new index is explicit.

## Intended workflow

1. In an approved local Lean project, import `OwnerQueryCommand` from the
   package's authoring helpers. Write the desired formal type using
   `#ordinary_type_query [u, v] "C:/fresh/query-type.json" : ...`.
   You do not need a theorem name or a proof. This is normal trusted local
   elaboration, not execution of downloaded peer code.
2. Supply canonical JSON bindings `[originalLeanName, portableSymbolID]` for
   exactly the type's referenced symbols, in `formal_query.reference_names`
   order. Use already known basis/acquired-symbol identities. Do not guess IDs
   from names or traverse proof ancestry merely to ask a query. This first mode
   refuses unknown vocabulary. These are search inputs, not mathematical warrants.
3. Run `query.py` from the assembled package using selected runtimes/profile,
   `--native-type`, `--bindings`, `--output`, and explicit `--wall-seconds`,
   `--cpu-seconds`, `--memory-mib`. It writes `QUERY.json`, `SPECS.json` and
   `RESULT.json` in the fresh output. No owner state, Lean process, provider
   connection or index is opened. Process checks are cooperative; an outer
   supervisor is required for hard process limits.
4. Put the returned `specs` into the existing `peer.py find` configuration,
   with your selected providers and finite budgets. Only new-profile providers
   are compatible. Empty or incomplete results do not establish global absence.
5. Inspect candidates, acquire exact evidence and independently check missing
   mathematics through existing owner operations. Query-key agreement is not
   acceptance. A warranted result may be exported to an ordinary Lean module;
   the selected exact installed singleton theorem matches are reused safely.

The SDK also exposes `loaded.formal_query` through the approved package loader;
ordinary source/package sharing can use the identical search facility.

## Meaning and limits

The key ignores binder names, universe labels and DAG sharing but preserves
ordered universe positions, exact portable symbols and other expression fields.
This is a precise syntactic lookup mode, not general mathematical equivalence,
premise reordering, specialization, unfolding or a claim to outperform Loogle.
Common exact-type buckets can still be huge. Native elaboration may be expensive;
the pure key pass never traverses theorem proofs. No sustained useful-growth
advantage, broad library compatibility or final-v5 release follows from this seam.

The source/build recipe, file-only assembly and coherent public-use boundary have
separate reviewed evidence. Existing native/pure controls were reused, not rerun
as a package-wide campaign. No full source build was repeated for this integration:
unchanged generated support and the separately validated command were reused.
