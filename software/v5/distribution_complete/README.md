# Complete authoring support, projected client distribution

This is a fresh successor to `distribution_efficient`, not an edit to an
installed release. Public `build`, `verify`, and `launch` command syntax is
unchanged; the input and release schemas are explicitly version 2.

The change repairs an actual installed AuthorLean failure: `Init.olean` alone
is not Lean's Init library. Private imports in the retained Lean 4.34 loader
need every reachable module's `.olean`, `.olean.server`, `.olean.private`,
`.ir.sig`, and `.ir` artifacts.

## Exact package contracts

`base_role` must be `mathematical-client-v1`. The full pinned predecessor
manifest remains a catalogue. The installed base must contain exactly all of
its `receiver/runtime/python/` files and the three selected supervisor helpers,
plus the catalogue itself. No arbitrary subset is allowed. This is not a
complete v4 installation: its historical CLI and Node/location roles are not
included or advertised as operational. Optional location needs its own adopted
runtime.

The new `lean_support` input has:

```text
profile: LEAN_4_34_INIT_PRIVATE_V1
modules: module name -> list of direct imported module names
files: original-Lean-root-relative artifact path -> {path, bytes, sha256}
```

All module names belong to Init; every edge must have a selected target, every
module must be reachable from Init, and every module must have exactly the five
required artifacts. The source selector derives this graph from the retained
toolchain's headers and records its assumptions/provenance separately. Structural
graph closure is not proof that arbitrary binary files encode that graph.

All support artifacts enter the release file map and exact filesystem census.
They are copied and independently hash-checked, and launch hashes them again.
An overlap with the existing short runtime-pin list must agree in both source
path and expected bytes/hash. No undeclared extra `assets/lean/` payload is
accepted.

The six worker runtime pins remain minimum explicit dependencies, not a claim
of a hermetic Lean runtime. The installed closure is checked by the enclosing
trusted release launcher, under the stable owner-controlled filesystem
assumption. This does not add a hostile-code sandbox or secure OS loader.
Authoring still produces untrusted output; the ordinary contributor must
actually admit that output before publication.

## Efficient validation

Reused directory-only path caching retains fresh file type/size/hash checks.
The complete Init closure is streamed, not loaded wholly into RAM. Omitting
unrelated base roles reduces file traversal while supplying necessary authoring
dependencies. This is a source-supported cost argument, not an assumed measured
speedup or a completed-v5 claim.

The independent path/copy tests need not be repeated. The new small controls
exercise only role projection, graph/header parsing, exact artifact closure,
overlap and release-file binding. A separately selected installed contributor
operation must demonstrate the actual loader/authoring path.
