# Exact-byte replica custody: independent implementation review

Reviewed 2026-09-21 by `feasibility_checkpoint_audit`.
**PASS at the source-review gate for the exact patch below; no concrete
correctness or operability blocker found.** The patch remains unapplied and
unexecuted by this reviewer. This is not integration, test, native-custody,
availability or usable-v1 qualification. Only this review note was authored;
no product import, test/process launch, SQL query, patch application or repair
was performed.

## Scope and immutable cut

The complete custody design, complete implementation note and complete patch
were read. Supporting inspection covered the existing acquisition/exposure
paths, both control-store interfaces, request dispatch/visibility/replay,
structural package validation and bundle construction, service import closure
and supervision, configuration pins, and ordinary/peer recovery boundaries.

| Reviewed proposal | Bytes | SHA-256 |
| --- | ---: | --- |
| `REPLICA-CUSTODY.md` | 17,995 | `6E17FC07C8340108154FC51F2981DDFAF41513A811F4D3191F19FEDF7EE4093C` |
| `REPLICA-IMPLEMENTATION.md` | 10,039 | `1F79AAD35477464D88BD8C9E38F0B20C15E5CD66E0BF4C7C626574AD49D2BE1D` |
| `REPLICA-IMPLEMENTATION.patch` | 22,216 | `5618AE27E3FF592C6D8F1BDD7EAD6DAB23DE81D8CE07103329D917CA6DD72EBA` |

All six installed base files match the patch author's declared base hashes:

| Base file, relative to `software` | SHA-256 |
| --- | --- |
| `py/peer_node.py` | `99B7F3AF3C4C4E0B66827157E743A75EAC320A54D04E90C1E4A9912991A90B18` |
| `py/service_worker.py` | `C94098CD5EE08ED8A4977843B138B3C0CFB905EE8A6F9D67CA9E39991ED21E86` |
| `py/peer_wire.py` | `B4AAD584E9F6F6D83872501D277C1F1CDE79E5A89618EFBF1260497BEB8D4946` |
| `py/node.py` | `DC0B2E20C27290270B595122C33385D51FF629B67EF52B94B97DD8A3990F6977` |
| `manage.py` | `DF319F00DBCF29702A04D6151564896AE4D040998AC5859CACE7CBE53580BB77` |
| `py/recovery_worker.py` | `EB574CEC2090CE3B337E289FCDF76C230B5C5BDB9E94E2DDB9CA39ABDB99C073` |

References below use **patch-file line numbers**, avoiding confusion between
old product lines and unintegrated proposed lines. An author-reported
`git apply --check` is only applicability evidence; this review did not rerun it.

## Ledger authority and read-only compatibility

The shared helper begins at patch line 26. Its complete call surface is
`record`, `cut`, `entry`, `rows`, and the already-initialized `root` attribute.
These are available on both `ControlStore` and `ReadOnlyControl`. The latter
inherits the keyed readers, supplies `root`, `config_id`, database and event
fields, and permits the helper's literal `SELECT` query. No helper call requires
`limits`, writable construction, authorization mutation or filesystem package
access. Default `rows(maximum=1)` bounds the original-request lookup; other reads
remain the existing indexed singleton readers and SQL progress budget.

`ReadOnlyControl` opens one query-only transaction, authenticates configuration,
initialization and absence of active work, and closes it after selection
validation but before the finite service. Moving validation into that transaction
provides one ledger snapshot rather than mixing separately opened ledger views.
No writer lock is manufactured by this read-only path.

The helper establishes the intended authority chain:

- Same-client, configuration-bound acquisition and remote records are
  authenticated by existing content-hashed record handles. Missing legacy
  custody is explicitly refused rather than reconstructed from directories.
- The advertised entry is validated; configured peer/endpoint, catalog digest,
  descriptor and bundle digest agree with the acquisition. Its historical
  snapshot must identify P1 and contain the exact positive integer sequence.
- The local offer's normalized package pin, descriptor and formal metadata
  agree with the acquisition and advertisement. The offer's symbols are checked
  against rederived symbols during new-view preparation, not trusted as theorem
  acceptance or read from source packages during serving.
- The original request key is 64 lowercase hex, and the indexed row binds that
  key to the same client/request ID. Bounded byte-valued request/response fields
  must describe a terminal `peer_acquire` for the exact remote handle.
- The terminal response's exact shape names this acquisition and a same-client
  authenticated candidate with the same snapshot, sequence and descriptor.
  Type-sensitive serialization prevents bool/integer aliases in these matches.

The received path is bound lexically to
`state/work/<original-acquisition-request-key>/incoming`. This deliberately does
not resolve a now-missing package while authenticating an old view. The stored
manifest digest must equal the original advertised digest. Neither supplied
paths nor an arbitrary candidate can replace the selected acquisition.

## Original representation and new-view preparation

The acquisition delta at patch lines 123-124 and 179-180 preserves
`received_package` separately from the normalized/reused `package`. The source
transport already checks manifest and bundle digests, framing and object IDs
and flushes incoming files. Existing normalization/reuse and candidate creation
remain unchanged; acquisition alone creates no publication, view or service.

`replica_expose` starts at patch line 133. It checks the current context's
foundation against the selected remote foundation, rejects reparse traversal
for incoming/manifest/selected objects, and requires the original raw manifest
digest. Existing `revalidate` calls `Checker.package` and `metadata` on the
received pin, not `Checker.offer` or `import_package`. `source_codec.read_package`
checks object identities, foundation, exact root closure, inventory completeness
and supported replay planning. Recomputed descriptor/formal metadata/symbols must
equal the selected local offer; its descriptor/formal metadata already agree
with the advertisement.

The existing builder preserves raw manifest bytes and its object-list order;
`make_bundle` rechecks canonical object payloads and uses the original framing.
The patch requires the one resulting entry to equal the original advertised
entry in all fields, including root, manifest digest, bundle digest and length.
Thus a normalized representation with different transport bytes cannot silently
substitute, even when mathematical IDs agree. Successful exact transport identity
remains conditional on the existing hash-security and stable-selected-file
premises, not proof of mathematical truth.

The builder flushes bundle/catalog/completion files; `load_view` then authenticates
the completed result. The new view remains under this operation's fresh request
work directory. Its only selected row names the custody basis and acquisition.
No export, admission, native proof execution or publication is introduced.

## Serving, publication compatibility and import closure

`validate_selection` begins at patch line 216. It pairs every selected row with
its corresponding catalog entry, requires P1, positive bounded integer and
nonduplicate sequence, and enforces the exact descriptor. The two row shapes
are disjoint: publication rows must satisfy the existing `require_published`
handle plus local descriptor/metadata/manifest correspondence; replica rows must
be the sole row, have `basis="replica-custody"`, pass the ledger helper and match
the original entry/foundation exactly. Unknown/extra/mixed fields refuse. A
failed publication check cannot fall through to custody. Existing exposure
build order matches selected-row order, and existing publication rows already
carry the required fields. Publication eligibility is strengthened, not bypassed.

At service startup the helper does not contact the original peer or open its
source, incoming, normalized or mathematical-evidence files. An intact frozen
view therefore does not require those separate copies. Installed implementation
modules, configuration, usable ledger and configured domain directories still
must exist: source-copy independence is not independence from the local runtime.
The unchanged `serve` path authenticates frozen bundles through `load_view` and
hashes the bytes actually returned for each bundle request. HTTP routes expose
only the selected catalog/bundles, not source packages or evidence directories.

The new service import of `peer_node` occurs only after configured peer-source
pins are checked; all three module paths are verified. Its top-level imports are
standard library, storage, wire and transport. Methods referencing a checker
are not executed by the helper. The existing `inspect_context`/`node` imports
also do not load the mathematical checker at module import. Service supervision
adds `peer_node.py`, giving eleven source files plus interpreter/configuration:
thirteen pins, within the sixteen-pin limit. Ordinary public calls and original
recovery receipts retain their existing twelve-pin closure.

## Visibility, grant and recovery boundaries

The commit branch at patch line 188 repeats immutable ledger bindings and the
exact prepared custody/selected-row/foundation match. It creates only the view
record through the existing branch. The enclosing dispatcher transaction commits
that record together with the terminal reply; no candidate, provider, snapshot,
publication, head, artifact or stage update is added. Orphan completion markers
cannot authorize a view. Exact request replay occurs before reservation and
preparation, so it returns historical bytes without reconstructing missing files.

Adding the operation to `PEER_OPS` consistently covers parser acceptance,
prepare/commit dispatch, peer file-census ceiling and the hard native-allocation
guard. It consumes one real request plus the existing 80-MiB exposure grant.
The wrapper selects the existing 120-wall/120-CPU-second, 1024-MiB/eight-process
peer envelope. No new grant, refund, schema, stage allocator or quota reset is
introduced. Structural work remains bounded by existing checker limits and the
worker supervisor; endpoint file observations are not transient disk quotas.

Recovery changes only the explicit peer operation set at patch line 376.
`replica_expose` is not added to ordinary recovery. Existing peer zero-stage
checks, source/command authentication, original-attempt and whole-Job quiescence,
existing owner lock, terminal-only mutation, counter retention and uncertainty
handling remain. A pending replica request cannot promote a staged view. Fresh
installation/configuration pins are required; old source-bound receipts do not
become recovery authority for a changed installation.

## Required next evidence, not additional mechanisms

Integration must be rehashed against this patch and followed by a separately
reviewed bounded test cut. In particular, the old eleven-contract suite asserts
the previous exact peer-mode set, so it cannot simply be rerun unchanged and
claimed to qualify this addition. The existing native qualification likewise
does not automatically cover the new operation.

The smallest discriminating controls are genuine private acquisition and
same-client custody; original-versus-normalized manifest identity; malformed
origin/candidate/membership bindings; missing or altered incoming bytes; exact
service row/catalog validation; unchanged unpublished `expose` refusal; serving
an intact committed view after source/incoming/normalized copies disappear;
changed bundle refusal; exact replay; finite quota and native-free pending
interruption with no refund or visibility promotion. They should exercise the
helper through both store interfaces and verify the checker-free service path.
The separately bounded A-offline/B-custody/C-fresh-check-and-substantive-use
scenario remains necessary. No source verdict here supplies those results,
multi-host fault tolerance, indefinite hosting or meaningful knowledge growth.
