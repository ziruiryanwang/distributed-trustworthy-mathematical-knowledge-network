# Managed storage profile binding review

2026-10-21, support_guest. Source-only review of selected127 input e0f0dc5d,
helper 3b535a33 and the adopted contract/runtime argument. No imports, tests,
database opens, process/network inspection, installation change or Git.

## Decision

PASS_DESIGN_CONDITIONAL: a fresh manager schema with immutable `storage_profile`
and `writer_profile_sha256`, checked by the installed owner before any manager
write, suffices without per-store adoption tokens, context variables or monkey
patches. This is identity plus an explicitly adopted trusted-code premise, not
proof that arbitrary bytes bearing that identity implement the envelope.

Root's selected writer digest is domain-separated over the fixed SP.PROFILE,
fixed base-manifest SHA and the complete installed SDK logical-name map of exact
`{bytes, sha256}` rows. Include the owner, new manager/session/composer/helpers,
all seven Python openers and inherited implementations, and the Node writer
closure through that exact map/base manifest. Omit installation/source paths
and whole mutable release identity from this persistent digest. All SDK changes
deliberately refuse reopen; there is no migration. The transient session profile
may still include its current full release identity. The two profiles serve
different purposes and must not be substituted for one another.

This complete map is the smallest low-risk implementation choice: a handpicked
list of the seven openers would omit inherited methods, imports and serializers.
The owner already authenticates all selected rows. Boot/source/runtime pins and
readbacks remain observations/engineering trust, not a reproducible-build proof.

## Mandatory order and closure

1. Fresh manager: validate exact new schema/profile, independently reconstructed
   writer digest, registry and both-slot reservation arithmetic before mkdir,
   lock creation or SQLite open. The caller's config digest is only an expected
   identity; it cannot authenticate itself.
2. Existing manager: check exact marker bytes, ordinary path/kind/no reparse or
   hardlink aliases, one-byte lock, fixed registry main/journal size bounds and
   allowed root grammar before writable registry open. A later SELECT/PRAGMA
   may already have performed hot-journal recovery. Never repair/delete an old
   journal, truncate a lock or adopt an old marker to obtain compatibility.
3. Every one of the seven Python opener successors runs shared fixed-path
   preopen checks before connect and SP.configure_connection before any existing
   PRAGMA/schema statement. Failure closes/refuses. Existing ordinary checks
   alone do not reject hardlink aliases, oversize locks or unknown WAL files.
4. Generation allocation validates all cap-bearing nested fields and computes
   SP.generation_envelope before the sequence/PROVISIONING transaction. Stored
   records repeat storage-cap validation; all configured runs remain charged.
5. Composer compares the current independently reconstructed writer digest to
   the manager, checks the exact derived generation marker and bounded grammar
   before service store opens, and launches the pinned Node successor with the
   same exact explicit metadata caps. Its runtime maps come from the verified
   installed owner, not request-provided adoption booleans.
6. Supervisor direct reopen is a real extra seam: sessions._open_launch is used
   for both suspended-worker binding and final exact-Job quiescence recovery.
   _Launch must retain the verified manager writer digest and pass it to the new
   required manager.open keyword. Reading a digest from config alone is not a
   substitute. Preserve original deadlines, identities and recovery semantics.

Generation identity already hashes the manager marker plus sequence/slot/config;
the generation marker contains that identity and config hash. Therefore the new
manager config transitively binds existing generation marker construction to
both profiles; a duplicate per-DB profile table or per-store token is unnecessary.
An explicit new generation marker version/profile field is optional clarity,
not required to close this identity chain. No other supported managed writer
path was found in this selected call graph.

## File grammar and recovery limitations

Use a bounded nonrecursive walk of the known layout, not a payload scan or
unbounded recursive inventory. Before stores open, reject unknown entries,
WAL/SHM, temporary/superjournals, unsupported kinds/aliases, any file over its
own cap and nonempty workspace/operations. Account for absent files in partial
PROVISIONING and interrupted runs; do not demand a completed fresh layout when
legitimate failed prefixes must remain charged. Reclaiming slots must retain
their separate deletion-prefix reconciliation rather than being made unreadable
by a full-present-layout requirement. R._info and R.layout are useful primitives,
but R.census alone checks a summed byte limit, not each database/journal cap.

For a normal service reopen, a matching marker under private-root continuity
establishes same-profile lineage. A bounded main/journal pair alone does not:
unknown hot journals must not be recovered merely because their lengths fit.
Metadata and path checks cannot exclude a hostile concurrent writer or prove
that copied/restored bytes are original. Existing no-external-writers/no-restores
premises and exact current ownership are substantive. Named alternate data
streams, filesystem metadata, snapshots/COW and other OS allocations are not
covered by an apparent default-data-stream sum.

Shared store guards outside this installed managed entrypoint establish only
their stated connection/file checks. They cannot claim a manager envelope or
retroactively establish old lineage. No serializable digest becomes execution,
mathematical, closure, deletion or migration authority.

## Conditional result, not physical adoption

Under the exact supported code/runtime closure, ordinary default Windows VFS,
no replacement VFS/extensions/chunk override, correct stated SQLite mechanisms,
custody-only operations and private-root/no-other-writers/no-restores premises,
the manager/composer can report the derived apparent-data-stream bound. The
Node pre-schema guard and pre-write identity/adoption byte caps are separate
necessary integration obligations owned by core_release. No RAM/pager campaign
is required by this review. Keep physical_envelope_adopted=false; this is not a
physical-allocation/free-space, cleanup-progress, all-owner-lifetime-output or
mathematical acceptance guarantee. Implementation and independent source review
remain separate from this design disposition.
