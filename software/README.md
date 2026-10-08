# Mathematical commons software — v1 in development

This is the product source tree, separate from preserved research experiments.
It is not a qualified release yet. The active goal is deployable, usable software:
independent Lean 4 agents can discover, locally verify, reuse and contribute
mathematical knowledge without a mandatory central server or shared research agenda.

The first extraction targets Windows x64, Lean 4.34.0 and the qualified
Python/SQLite profile. It preserves the canonical reconstruction, native checking,
source capture, inverse export and fresh replay gates. Local Lean source is
owner-authorized executable input; peer exchange accepts inert bounded data only.

`py/` holds the local core and transport components; `native/` contains the
support sources to rebuild; `assets/` contains immutable foundation/common
packages; `tests/` contains independent tests. Installed code/assets, node data,
and inspection/evaluation scratch occupy separate configured domains. No runtime
configuration should refer to an old experiment or its precompiled outputs.

Start with `QUICKSTART.md` in an extracted package (the development source-tree
copy is `drafts/OPERATOR-QUICKSTART.md`). The [agent quickstart](AGENT-QUICKSTART.md)
shows how to create exact source requests without hand-escaping JSON. The
[local-agent API](API.md) leaves research strategy outside the node. The
[core contract](CORE.md), [peer boundary](PEER.md), [recovery rules](RECOVERY.md)
and [continued hosting](HOSTING.md) document guarantees and limits. Packaging
does not certify these features; qualification evidence is maintained separately.

Before v1: actual fresh builds and independently initialized exchange; reliable
offline reciprocal use; bounded hostile-data/failure tests; safe capacity growth,
bounded context selection and pending-work recovery; meaningful use/cost evidence;
independent audits and release documentation. Same-host tests will not be called
independent-host deployment. Useful or exponential growth is not established by
adding a theorem or transferring a file. No public deployment or release has occurred.

The project license remains undecided by explicit owner choice. No permission
for public redistribution is asserted by the development source package. No
second independently operated host is available for the current qualification;
same-host and loopback results do not establish independent-host operation.
