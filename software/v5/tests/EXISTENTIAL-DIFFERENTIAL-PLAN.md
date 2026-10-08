# Profile2 existential conclusion: focused changed-boundary plan

Status: SOURCE ONLY, no build or test has run. Root owns finite selection and
launch. Preserve all profile1 images, diagnostics, failed snapshots and traces.

## Selected change

The mutable receipt relation uses DMKN_CERTIFIED_MODULES_V2; its public journal
is DMKNM002/profile2/184bytes. The witness field and whole-input canonical hash
disappear. All semantic commitments, checker calls, exact parent journals and
rank constraints remain. Host capsule/checkpoint versions become3/5; session
and snapshot binding domains becomeV2. Input hashes remain in local host
bindings and do not create a transferable provenance assertion.

The claim is existence of SOME checked witness for the committed module. It
does not attest an arbitrary proof supplied alongside a certificate. See
research/cycles/v5-2026-10-07/REPRESENTATION-COST-DECISION.md and independent
ASSURANCE.md for the source-level reduction and its assumptions.

## Size-validation equivalence

New canonical_size counts exactly the length that the unchanged canonical
emitter would produce, with identical MAX_BYTES/MAX_NODES/depth/numeric guards.
Strings contribute two quotes and one byte per UTF8 byte, except quote,
backslash and b/f/n/r/t controls contribute2; other ASCII controls contribute6.
Keys obey the same string rule but do not count as Value nodes or add depth.
Null/bool/u64 decimal lengths and container punctuation are exact. Permuting
object keys changes no length, so sorting is unnecessary. Induction on Value
establishes exact size equality; early refusal may have different error ordering
when several bounds fail, but accepted domain is unchanged. The strict parser
still rejects duplicates, negatives, floats, trailing input, oversize input and
default serde recursion overflow. No raw-length/canonical-length shortcut is
assumed. Public parse, canonical and hash APIs remain unchanged.

## Fresh focused Rust harness

software/v5/tests/existential_differential.rs links the real retained native
checker and RISC0 SHA; no mocked hash, guest, network or parent-proof execution.
Its exact source and actual retained runtime map must be selected before build.

Five previously held native inputs are read without modifying their bytes.
Inside this TEST ONLY harness, schema and parent journals are projected to the
new profile. Those parent statements remain synthetic unverified conditions,
NOT upgraded receipts. The new relation's output must equal the old actual
216B journal projected to184B with magic/profile updated, including exact
ModuleID/summary/rank and pending parent statements. Old journals must refuse.
There is no second old native campaign: held actual outputs are the comparison.

The base runs once through each new public entry. A distinct local theorem
proof is constructed as `(fun h:T => h) p` for retained closed proof p:T.
The real native checker must accept it with the exact same new conclusion;
different serialized witnesses alone are not a pass. A corresponding invalid
local proof using T as its own proof must fail closed.

Six relation refusals: old schema, wrong rank, changed foundation, changed
body opening, extra input field and invalid local proof. Five old journal
layouts plus profile/magic/trailing/short mutations refuse. Calls total13,
of which8 reach the native checker if all source expectations hold; exact
actual results, including any failure, must be retained. This is not13 proofs.

Size tests cover every ASCII scalar as both object key and string value,
Unicode boundaries/2028/2029, all u64 decimal transitions, nested/empty
containers, direct256/257depth boundary,1Mnode boundary, exact16MiB canonical
boundary and escaped-key overflow. Raw parser comparisons cover whitespace,
Unicode escapes, duplicates, trailing input, numbers, malformed UTF8/surrogate,
empty input, serde recursion, raw-byte overflow and global-node overflow.

Passing establishes the selected profile projection and validation boundaries,
not a cryptographic certificate, completed guest, throughput or useful growth.
A new guest image and host binary are required because old image/profile bytes
cannot become profile2 by editing journals. No budget/cap increase is selected.

## Bounded adapters prepared for independent review

build_existential_test.py is a fresh narrow adaptation of the already reviewed
one-link frontend harness adapter: new paths/status/source names and the exact
guest03 frozen canonical source989c2695... replace predecessor inputs. It retains
the same native link recipe/compiler/runtime map, finite limits, process Job,
source snapshots, exact owned telemetry cleanup and final binding checks. It
builds only the harness, without running it or rebuilding the checker/backend.

run_existential_test.py pins the actual fresh executable plus ten exact held
input/result fixtures and validates the new report: five projected cases,
13relation calls,8native-reaching calls,6relation refusals,9journal-layout
refusals and183size/parser controls. Root's outer supervisor must bind the
actual successful executable/build sources and provide whole-tree containment.
The exact runtime selection cannot exist until a successful reviewed build.
No old experiment output, parent receipt or mathematical module is rewritten.
