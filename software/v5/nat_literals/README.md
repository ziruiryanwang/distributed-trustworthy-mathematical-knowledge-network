# Bounded native-Nat literal importer

Source successor only. Replace logical `modules/source_rows.py` explicitly with
this directory's `source_rows.py`; keep its package-relative codec/model imports.
The predecessor is `software/v5/modules/source_rows.py` SHA-256 `60c7255d...`.
No installed product, frontend, canonical syntax, checker, policy or receipt image
is changed by placing this file here. Root owns runtime selection and adoption.

## Changed boundary

`SourceRows.expression` now lowers an actual `natVal` decimal row to the captured
local `Nat.succ`/`Nat.zero` constructors. The API and every nonliteral branch are
unchanged. Unsupported strings/literals still refuse. OfNat applications are
preserved, not replaced or interpreted as privileged arithmetic.

The lazy guard requires exactly one complete original local Nat group: exact
Type0 and constructor shapes, zero/succ ordering, safe metadata, and Nat.rec's
universe/owner/arity/rule census. Integer metadata differs from booleans. The
actual recursor type and rule bodies remain untouched for the independent checker;
the structural guard does not claim their mathematical validity. Empty-role
census readers still work until actual expression lowering is requested.

## Prospective resource bounds

Canonical decimal spelling and length/value bounds precede integer conversion.
Each expanded occurrence charges `3*k+2` work visits, including references;
the original dispatcher has already charged one. Maximum depth is `d+k+1`.
This deliberately conservative extra reference charge applies only to literals;
it does not relabel the old ordinary-constant counter as full codec accounting.

Before first expansion, reserve surrounding metadata once: four times original
row bytes, expanded metadata-name bytes, and fixed declaration/rule/digest slack.
A syntax unit bounds one source node's largest raw header plus a full structured
reference, including external relative names larger than their source aliases.
Prior source visits and every subsequent visit pay that unit. Each
literal then reserves its exact constructor JSON size `Z+k*(S+9)` before building
the chain. Repeated DAG occurrences pay again. This is conservative and can refuse
some otherwise encodable inputs; it never raises existing caps. No growing subtree
is repeatedly serialized. Existing full body/group/spec validation still applies.

## Trust and evidence

Raw exports remain unchanged. The specified homomorphic lowering gives original
native literal/constructor correspondence; the later mathematical relation checks
normalized canonical descriptors against rebuilt rows and freshly checks the
relocated extension. Those are different obligations. Neither source hashes nor
this importer prove source execution or grant mathematical acceptance.

Small literals do not bound recursive arithmetic conversion. Relocated Nat is not
a later author's built-in Nat. No automatic numeric bridge or growth advantage is
claimed. `controls.py` is independently owned synthetic structure testing; a real
frontend/fresh-checker case is separately selected. No tests were run by the author.

Implementation selection and theory are under
`research/cycles/v5-2026-10-20/NAT-LITERAL-{IMPLEMENTATION,SEMANTICS,SOURCE-SEAM}.md`.
