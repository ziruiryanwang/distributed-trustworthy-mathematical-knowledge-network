# D17 continuation: retain positional struct arrays

The original structural run01 FAILED at the fourth extra (`const: [0, []]`):
old outer flatten/Content accepted ExprConst, but direct Value enum decoding
refused positional struct arrays. This is a genuine acceptance-domain issue,
not a fixture error. Preserve every used source, build and failed run.

The selected one-line guard restricts the direct path to objects with NO array
value. Thus positional struct payloads and ordinary level max/imax tuple arrays
use the unchanged general decoder. The original decoder, inner enum, checker,
relation and compiled foundation are otherwise unchanged; current dev parser is
the fresh successor, earlier exact source snapshots remain preserved.

For the new guard domain (array payloads), old and new paths are literally the
same original function. For all other inputs, previous fast-path behavior is
unchanged. This is a source argument, reinforced by one small continuation;
do not repeat all five held mathematical examples or their foundation checks.

Actual run01 failure location follows all five held row-equivalence cases,
compiled foundation reconstruction/equality, 421 foundation refusals and first
three extra successes in straight-line source. Independent saved-source/control-
flow review adopts those scoped successes; run01 remains FAILED overall. Its
23,313-byte reconstructed foundation survives and is independently checked for
raw SHA256 736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c
and framed FoundationID d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481.
No native/VM/proof calls have occurred.

New structural_frontend_continuation.rs runs the remaining nine accepted extras
(including the failing const case), six targeted array payloads (both legitimate
tuple variants and positional structs), and all 21 previously unreached irregular
boundary cases. Old/new successful decoded objects must match; otherwise both
must refuse. The build keeps retained fat LTO/embed-bitcode flags and the same
180CPU/300wall/4096MiB owner Job lifecycle. Runtime remains 30CPU/60wall/768MiB.

Runtime wrapper pins actual prior failure/source/binary/foundation evidence,
binds reused successes without rerunning them, verifies both foundation digests,
and invokes only the fresh continuation binary. Root owns exact selections.
Prospective guest05 selection must be refreshed to the successor parser after
independent review and actual continuation adoption. No cap change, new host
link, mathematical admission or measured speedup follows from this continuation.
