# Release-owned producer: independent core source review

2026-10-22, storage_launch_review. Canonical project root only.

**PASS_SOURCE_REVIEW_WITH_SELECTED_CONTROLS_STILL_REQUIRED.** The three new core
sources implement the accepted compact adoption design without changing the
existing mathematical relation, generic snapshot, scheduler or allowance rules.
This is source review, not executed construction, installed portability,
cryptographic acceptance or final-v5 qualification. No code was imported or run.

The earlier `RELEASE-PRODUCER-DESIGN-REVIEW.md` remains unchanged at SHA-256
`343c6a91ef102f09c5a1017750eded5740facc8eb8519006d8f6d364b54a3c99`.
This separately pinned source addendum avoids rewriting that delivered review.

## Exact reviewed sources

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/release_production/__init__.py` |169|`56653258ec5e2b9e8d6abffa55e4f889b979daae05c81282a36cf65453b60717`|
| `software/v5/release_production/producer.py` |7617|`4396de095caf214559674e0fdd5188fcc52d10c3e4c8fe32e1d5b63259f397ce`|
| `software/v5/release_production/adoption.py` |10675|`62255a98879ed7162eb1a3414c937a29a70258b7396ae070d32fac1253ec5710`|
| `software/v5/release_production/README.md` |8134|`844108cac908c46f798a37f9420741aec8d0fd970c8d0620bb76aad7529cde36`|

I read all three core files and README, rechecked the relevant inherited source,
and traced every `_install` use in production, aggregate-small and generic
lifecycle/snapshot. Entry has a separate independent review.

## Resolved finding: protect the whole immutable release

The first constructor version copied `_support._install`, which is the nested
supervisor-manifest directory. The inherited output-overlap guards would then
allow a fresh output elsewhere inside the release. Individual pinned-file
protection does not protect unused directories of an immutable installation.
I reported this concrete defect before any launch.

The reviewed correction sets **only the aggregate owner's** `_install` to the
adopted full release root and binds it in `_check`. The support owner retains
its own base directory. All relevant inherited aggregate/snapshot uses are:

- output-overlap exclusion;
- the explicitly recorded host working directory;
- supervisory invocation with that working directory;
- exact adoption of the resulting snapshot command/cwd.

No inherited aggregate operation uses this field to locate support loader
files. Host executable, guest, input and output arguments are absolute. Thus
the correction strengthens the public class boundary without a duplicate
request parser or forked scheduler. New evidence commits to the new cwd;
old snapshot/profile identity is not relabeled. Actual binary behavior from
this cwd remains a later real snapshot integration obligation, not a source
proof or reason to repeat an old proof campaign.

## Adoption and immutability checks

`adoption.load` accepts exactly `{root,manifest,descriptor}`. It binds the
externally pinned `ROOT/V5-RELEASE.json`, bounds its file map, rejects self-entry,
case/directory aliases, file-as-parent paths and malformed relative components.
The descriptor must be one exact member of that map. Its exact field grammar
contains no reverse manifest hash, so the manifest/descriptor commitment graph
is acyclic. The materialized owner profile is separately supplied; an assembly
must not add it to the manifest that it itself pins.

The descriptor has exact foundation/policy/I/A identities, exact three selected
artifact byte counts/hashes and27 exact logical core module paths under
`sdk/v5`. Those core pins must equal both the supplied source set and the support
runtime membership. Every bound file is ordinary, contained within the release,
hash matched, and conflict checked. The support manifest and its three actual
loaded helper files are independently matched to the same outer release map.
The two authority-carrying documents are reread/rebound after payload reads.

This validates the operative component subset of a V3 manifest, not all fields
or payloads of an entire reader/distribution installation. Unselected map entries
are bounded metadata, not automatically opened dependencies. The static design
count56 remains a prospective exact-layout count; source enforces64 installation
pins and512MiB and refuses rather than expands those limits.

No peer or descriptor becomes publisher authority by naming its own digest.
The current source pins the selected host/guest artifact tuple explicitly;
guest-file hash and execution-image ID remain different. Correct compiler/checker
correspondence and local software adoption remain external assurance premises.
The returned adoption namespace is not a theorem, receipt or funding handle.

## Explicit construction, reuse and cleanup

The class initializes all scheduler and lifecycle state explicitly, copies and
binds new outer/inner profile schemas and the new hash domain, and validates
source origins before it constructs the unchanged support owner. It never calls
an old S/L/T constructor. The three inherited historical adoption hooks are
explicitly overridden to refuse, so no fallback reopens old build records.

After support construction it binds the real supervisor and Job, checks the
selected memory ceiling against the actual supervisor, unions exact pins,
requires that union to equal the adoption closure, and binds image/snapshot
roles. Readiness is set only after its immutable installation map is recorded;
the final `_check` executes inside constructor failure cleanup.

`super()._check` preserves aggregate/support raw-profile checks and all lifecycle
equalities,24-source origins and snapshot-map finalization checks. The successor
also checks all27 origins, the installation pin-map serialization, full release
root, cached image/snapshot host/snapshot map, file count/bytes and stage/image
failure markers. These cached operative values cannot silently diverge from
their committed profiles. The support `_check` rehashes supplied pins normally.

On a failure after the support constructor returned, cleanup calls its close.
If close also fails, `BaseExceptionGroup` retains both primary and cleanup
errors. No successful owner is returned. A support constructor that never
returned is not falsely claimed to have been separately closed. No worker is
created by these new constructors or adoption helpers.

The inherited generic snapshot dispatch/adoption, preparation, preflight,
production-request construction and finite scheduler remain unchanged. Prior
attempts still require exact profile/session/allowance/budget/prior-prefix/cost
identity. A newly materialized or relocated profile cannot reset or migrate the
live U allowance. A genuine U receipt can later support distinct mathematical
reuse, not retrospective reinterpretation of U's producer history.

## Remaining gates, not source defects

The separately selected minimal controls should cover changed adoption/paths,
origin/immutability, failure cleanup, no automatic dispatch and whole-release
output containment, plus one actual fresh relocated construction/close. This
needs neither host execution nor another proof. The test must report the actual
closed pin union rather than promoting56 into an observed count in advance.

The full production package, descriptor/manifest assembly, imported source
compatibility, actual host-cwd behavior, explicit public installed-launch
evidence adapter, genuine new snapshot/renewal and final release obligations
remain. Ordinary filesystem stability and trusted runtime/OS assumptions remain;
this source is not a hostile-source sandbox or hermetic-loader proof. No tests,
syntax checks, installation, host calls or proof operations were performed in
this review, and the retained heavy worker was untouched.
