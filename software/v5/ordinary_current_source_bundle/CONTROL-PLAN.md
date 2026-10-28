# Current source bundle: focused file-only controls

Source-only plan, 2026-10-28. Root selects execution separately after independent
review. No pack, extraction, verification child or native build has run yet.

Run one actual source pack and controlled extraction of only its independently
expected 96 archive members. Invoke the public verifier once from that relocated
tree with the manifest hash from the actual external receipt. Then check fresh
wrong-manifest/missing-source/extra-source/changed-map fixtures and a stale
overlay-entrypoint manifest. Seven grouped outcomes are required. The expected
95 payload paths come from the reviewed map's 87 entries plus eight explicit
additions in the test, not from the utility's private selection helpers.

The public verification child runs only the exact approved bundle utility and
stdlib under isolated Python; it does not import product code or start a
compiler. It inherits the outer Job and has one remaining-time subprocess
timeout. There is no native build, owner/database operation, network request,
old-workspace traversal, deletion or retry. Only fresh controlled test outputs
are written. The original and successful relocated source trees stay unchanged;
refusal fixtures are separate fresh trees with their alterations present before
verification. All outcomes and child logs are retained.

Suggested selected inputs: the 95 payloads as external exact pins, plus the
test/runner source snapshots. Keep the existing runner's `software/v5/` source
allowlist unchanged; it intentionally does not snapshot foundation assets. Pass
the canonical root explicitly as read-only `--source-root` and a fresh selected
control directory as `--output`. Use approved Windows Python with `-I -S -B`
and one enclosing bounded Job. The suite checks one 60-second cooperative
deadline across the workflow; root supplies the actual outer limits.

Do not repeat the predecessor's broad path/ZIP tests: those algorithms were not
changed. This run should also produce the exact extraction for a later separately
selected native build, avoiding a duplicate intermediate build from canonical
source. A passing source bundle does not qualify that native build or complete
v5.
