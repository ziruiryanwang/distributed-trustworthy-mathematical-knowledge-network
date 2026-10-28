# Advisory symbol-query preparation

Status: source-only successor for independent review, 2026-10-28. No operation,
performance measurement or deployment claim follows from this source. Root owns
package/profile selection and actual execution. Used predecessors are unchanged.

## The operation and its purpose

An agent knows one to eight exact names in a selected local context and wants
existing search specifications for declarations mentioning those symbols. The
name-to-symbol mapping comes from the owner's recorded checked context metadata.
Preparing this advisory search does not require opening the context's retained
Lean snapshots or its custody store. The separate mathematical use/admission
path still checks its required retained snapshots and dependencies normally.

This distinction removes a term proportional to retained snapshot bytes from
this operation's state reads. It does not make cold metadata lookup sublinear:
the selected catalog reader still validates complete bounded ancestry, names,
no-shadow rules, import audit and correspondence. Package/runtime verification
also remains. The source argument is in the predecessor's
[SCALING-AUDIT.md](../ordinary_symbol_query/SCALING-AUDIT.md); the private facade
and its validation obligations are specified in [CONTRACT.md](CONTRACT.md).

## Public arguments

The entry retains the package/runtime identities, finite CPU/wall/memory
arguments and fresh output path. Choose exactly one input kind:

| Input | Binding mode | Required state arguments |
|---|---|---|
| `--symbol-names PATH` | `--context-root HEX` only | `--catalog PATH`, `--store-id HEX` |
| `--native-type PATH` | `--context-root HEX` | Existing catalog, store ID, custody and custody-limit arguments |
| `--native-type PATH` | `--bindings PATH` | No state arguments |

Symbol mode rejects `--bindings`, `--custody` and `--custody-limits`. It does not
silently ignore custody arguments or import an old report as current evidence.
Exact-type inputs, admission semantics and their owner/custody lifecycle remain
unchanged. The root-owned next offline kit must reflect this argument difference.

The symbol input remains canonical JSON containing one to eight distinct exact
structured Lean names, at most 65,536 bytes. There is no new syntax, feature,
namespace, wire protocol, matching algorithm or database schema. All names must
resolve; an absent name yields `UNMAPPED_REFERENCES` and no query output directory,
never a weaker conjunction containing only the names that happened to resolve.

## Source selection and authority

The package's successor profile requires one added root auxiliary source role,
`advisory_context.py`. Installed core sources and their implementation identity
are unchanged. The package loader validates this role as part of the exact file
set before the caller can open state. The caller then reads that fixed file,
checks its captured bytes against the selected descriptor's exact size and
SHA-256, and executes only those bytes under a unique module name. It never
searches for a helper on an unselected path or extends `sys.path`.

The helper receives the exact already loaded `A.P` catalog module, the selected
installation, catalog path, store ID, root, names, recorded limits and operation
budget callback. It opens and closes its private query-only catalog internally.
It returns only identities, the requested binding projection, missing names and
explicit advisory status. It returns no state owner, module loading plan,
snapshot path or admission capability. The caller rejects additional returned
fields, unrequested bindings, inconsistent missing names and identity mismatch.
Final profile verification includes the helper before output publication.

The profile hash is explicit byte selection, not third-party authentication.
The existing entrypoint, runtime, OS and protected immutable local-record
premises remain. Native local roots do not independently authenticate arbitrary
binding maps. This operation reads the selected catalog through its retained
metadata checks; it does not accept an operator-supplied map as root evidence.

## State lifecycle

The caller validates input, output, selected catalog and installation/runtime
path separation, adoption marker and implementation/store identity. The helper
retains catalog exclusive locking, liveness, withdrawal, activation checks and
recovery. Opening may settle old reservations, so this is not database-read-only.
Only the symbol branch avoids opening custody and ordinary admission.

The helper returns after successful close. A failure to open, validate or close
raises and produces no ready query output. If a helper call fails, the caller
uses `owner_closure: NOT_CONFIRMED`; it does not invent a successful close or
assert that the catalog was never opened. Before the call the value is
`NOT_OPENED`. A successful projection has `owner_closure: CLOSED`.

Missing or damaged retained snapshots can coexist with a successful advisory
projection. The operation deliberately does not establish their current
integrity or availability. Selected metadata, audit or identity damage still
refuses. An actual downstream use remains subject to the ordinary full checks.

## Successful report and files

Output remains `BINDINGS.json`, `SYMBOL-NAMES.json`, `SPECS.json`, then the fresh
renamed `RESULT.json` success marker. The marker is published only after helper
closure, input recheck, final profile verification and the finite budget check.
Partial failed output remains retained without automatic retry. Success retains:

- `operation: prepare-symbol-query`, `query_kind: symbol-neighborhood` and
  `binding_mode: selected-local-context`;
- exact PROFILE, names and bindings hashes, selected identities/root/store and
  reference count, existing conjunction specs and features;
- `mathematical_acceptance: false` and the existing bounded-search claim.

The successor additionally reports:

```text
owner_closure: CLOSED
custody_closure: NOT_OPENED
snapshot_integrity: NOT_CHECKED
context_readiness: NOT_ASSERTED
interpretation: RECORDED_ROOT_SEARCH_BINDINGS_NOT_LOAD_READY_OR_PROJECT_EQUIVALENCE
input_pins: {names_sha256: <exact input hash>}
```

There is no custody-limit hash because no such input is selected. There is no
exact-type key or native-type hash. A new offline kit must validate this precise
success contract before preparing `find`; the frozen predecessor kit requires
custody closure and its limit hash and must not be weakened in place. The existing
find implementation and acceptance rules need no change.

This result means that the selected recorded root supplies the specified search
identities. It does not assert context load readiness, theorem truth from this
operation, useful results, global completeness, project equivalence or measured
speedup. Those properties have separate checking and evaluation boundaries.
