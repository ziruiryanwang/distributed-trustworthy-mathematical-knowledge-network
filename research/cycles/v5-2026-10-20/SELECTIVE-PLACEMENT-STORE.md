# Guarded index commit seam

2026-10-21, root. Source-only implementation selected by
SELECTIVE-PLACEMENT-SELECTION. No imports/tests/runtime/build performed.

Basis: software/v5/instantiation_discovery/discovery/discovery_store.py,
32df0e1d5be03b9bb0ac3c57f3df367857e608e4678c8ede262593ea9f65b884.
Successor: software/v5/selective_placement/discovery/discovery_store.py,
1c8543d4903754174b80d107ee923116ddb402d41a3b5af3f1d255abdfc6a328.

Only three source seams change: optional keyword-only before_commit argument,
callback before duplicate COMMIT, callback before fresh COMMIT. Both remain
inside the original exception/rollback region, after the existing internal
deadline check. No callback is called when the argument is omitted; existing
workspace/caller behavior and storage bytes/schemas stay unchanged. This mirrors
the existing ModuleStore before_commit contract instead of adding another store.

The callback is trusted owner code, not a downloaded function or a mathematical
verifier. It checks the owner's exact live service grant and deadline before
commit. It is not a preemptive sandbox or a new guarantee for unchecked callers.
Root inspected the full line diff; independent review/controls remain pending.
