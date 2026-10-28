# Exact symbol-query successor: independent source review

2026-10-28. **PASS for root's finite controls and file-only integration
selection.** Reviewed source/data only: no imports of product modules, control
execution, native calls, owner-state access, index query, assembly or Git action.
The final operator-companion delta is included below. Runtime and real-owner
outcomes remain unqualified here.

| Selected source | SHA-256 |
|---|---|
| query.py | 5db6c0b12258b37cf2704b7003108fe23ff23085656290eb01e09bfab40d5ecb |
| CONTRACT.md | c3fb64aa9eb4aad1aad230ab5b9679507b18063eb51fb712215f4de3306ef9c1 |
| run.py | 77de8ed046273b6eec3ab4fc8c1f779fb31d662072176562313068a432f9ccc9 |
| LAUNCHER.md | f438e90a3076b7eccbeada316d62d6e2fd500ca9f022cf3775de146797ecbc6c |
| assemble.py | ceee7a5a5d2b439cd3680c2f8b3e6b1ddcfa2f2cf07aa41135a84c2334df21d2 |
| PAYLOADS.json | 27d2c1d74ead5d22c13aa7ae282f8af6d48c057b9883209b8019a615f65d6856 |
| build.py | 55e5618d610e0d24f9d7526fce5a267d1dcb214c40261afd6ffd0ae96688564e |
| source-map.json | f6eb20aaced69765dadac3d52f6f41f369cea09e34a541e9cffb04e8cdec4f1c |

The new input is precisely a canonical list of 1..8 unique structured names,
at most 65536 bytes. The existing name codec validates components, UTF-8 and
semantic-name restrictions; strings/Lean syntax, invalid tags, duplicate exact
keys and noncanonical encodings refuse. Numeric and string components are
distinct, not ambiguously reinterpreted. This entry does no shorthand or alias
resolution. Parsing finishes before owner opening. Symbol input requires the
complete contextual argument tuple and excludes manual bindings/native-type
input; programmatic dispatch validates those modes too.

Names resolve only in the explicitly selected `catalog.context(root)` binding
map, after root/semantic/foundation/implementation identity checks. The existing
catalog rejects duplicate/shadowed original-name bindings: equal spellings in
different contexts select their respective identities, with no cross-context
search or ambiguous-name fallback. Every selected ID is validated. Any missing
name makes `resolve_names` return no binding bytes; the controller then returns
`UNMAPPED_REFERENCES` without specs/features or an output directory. There is
no query from a mapped subset. Complete success emits one existing `type-symbol`
spec per requested name and uses the unchanged adapter's conjunctive compiler.
Feature deduplication for equal identities is legitimate conjunction idempotence;
all requested names remain in the binding rows and specs.

The diff against frozen `ordinary_query_context/query.py` preserves input and
profile revalidation, owner-then-custody closure, refusal on failed closure, and
success publication only after both handles close. Symbol mode writes
BINDINGS/SYMBOL-NAMES/SPECS before the final fresh RESULT rename. Uncertain rename
retains its attempted result hash and failure disposition. Current exact-type
manual/context modes keep their native binding/key/feature algorithms and output
filenames; report additions identify the input kind and contextual closures.
The shared resolver's extraction preserves old zero-reference behavior.

`run.py` differs from `run_frontier.py` only by adding `symbol-names` to the query
option allowlist and input-path treatment. It inherits the existing input/output
separation and child-tree supervision; no wrapper-containment expansion follows.
The appended guidance accurately distinguishes search inputs from admission.

The file-only assembler pins the existing helper, compatibility map, caller-
selected base receipt/PROFILE and every one of its 154 payload files. Its final
payload-map constant is bound. It requires exactly three replacement sources,
regenerates PROFILE for query/run, then verifies that exactly LAUNCHER/PROFILE/
query/run changed and 150 files remain identical. Fresh destination separation,
source/destination readbacks and final census are retained. No native build or
owner operation occurs. This reviews the assembly transformation; actual source
and output identities still require its saved result audit.

Independent JSON comparison confirms the portable source-map successor changes
only the query/run/LAUNCHER source paths and their pins, including LAUNCHER's
documentation reference. Counts, 87 selected inputs, 72 copy roles, native lanes,
runtime pins and other fields are unchanged. `build.py` changes only PREFIX and
MAP_SHA. This preserves a reproducible future source-build path without selecting
another native build. A changed PROFILE must be used explicitly for new reports;
unchanged implementation/storage identity permits normal B-context checks, not
relabeling old reports under the new PROFILE.

Five small control groups were authored separately as `control_tests.py`
(`98343d81db4b17f74b3f7cec5c4499c3735f9282de0efa6c5aa84fac89f40708`),
with CONTROL-PLAN.md
(`9db8811d8dafdde729d4d57ce682c6d7a34817343f4466879961f8e6e3df855a`).
They have not run. Real inert codecs/features test new parsing/projection and
old type projection; two explicit owner doubles check new success and partial
missing output/closure. This reviewer authored those controls, so this report
does not count as an independent test-source review. Root should use the
separate source-author check and select exact test/package/query pins.

Correctness is conditional on the checked-context invariant already enforced
by the owner. This operation prepares faithful search constraints; it proves
neither relevance nor coverage nor mathematical acceptance. Its incremental
projection is small, but cold context loading still walks selected local lineage
and retained metadata. CONTRACT discloses that cost; no constant-time whole-owner
lookup, global speedup, autonomy or final-v5 claim is warranted.

## Operator companion delta

Reviewed final `operator/prepare.py`
`f426dd563cae1fa5d82b9824e1793d5a2b8cd3042542abaf0704d77c945d8323`,
`prepare_selected.py`
`95805eb58baf607d39e536c5502a4b6d4181610b193c39d686c8d4b0a5b1902a`
and `compatibility.json`
`9abcb9cfdec62f2e8fbd2447b7895b05ee35f8174c7fc8d625e6d3067930e980`.
No blocker found in their diff against the adopted current operator kit.

The new action requires exactly one explicit context root or matching-profile
parent report and exactly one dotted or structured name list. Dotted shorthand
uses a documented restricted component grammar; digit components stay strings,
never guessed numeric Name components. Empty/duplicate/oversized lists and
unsupported shorthand refuse. Structured names retain the conservative existing
kit validator; the product still performs authoritative semantic validation.
An explicit root is a user-selected input checked by the real owner, not a way
to relabel an old report under the successor PROFILE.

Successful symbol-query report intake requires the exact selected PROFILE,
symbol query kind, both CLOSED fields, exact input-pin fields, matching name
hash, 1..8 matching reference/spec counts, valid type-symbol specs and canonical
feature order. A failure/missing result cannot seed `find`. Feature bytes are
convenience report fields; the existing search uses/validates the specs anew.
Exact-type report intake remains supported. The compatibility delta changes
only schema plus query/run direct-source pins; all other 43 direct roles and
72 generated roles remain unchanged. This is a source review, not an assertion
that a future actual preparation/find has succeeded.
