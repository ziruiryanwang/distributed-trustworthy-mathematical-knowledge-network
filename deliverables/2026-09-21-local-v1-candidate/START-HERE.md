# Mathematical commons: local v1 candidate

2026-09-21. This is a locally usable, tested source candidate, **not a completed
global-network v1 or a public release**. Project licensing remains undecided.
The ZIP is an immutable source cut; qualification is separate from packaging.
No runtime, user database, experimental state, credential or automatic agent is
inside the ZIP. Nothing has been published externally.

## The artifact

`math-commons-source.zip`: 3,637,844 bytes, 112 source/document/asset payloads
plus a manifest. SHA-256:

```text
22e673620aa3a6cdba6aa21ef7e56a9dcafa4c1ed296c149f2c8ab24c0f01ff5
```

`SOURCE-MANIFEST.json` lists every payload length/hash. Its SHA-256 is
`8cf79c3283fb51342039a02e8876b06a59c0f563f8a2746da903b283b4848c87`.
These are integrity identifiers, not a publisher signature or license grant.

## Start a fresh node

Supported qualification environment: Windows x64 on local NTFS, Lean 4.34.0,
Python 3.14.6 with standard-library SQLite **3.50.4**. The complete Lean runtime
and selected Python distribution are prerequisites, not included dependencies.
The current machine's qualified Python is `D:\Python314\python.exe`; Lean is
under the project's `software\runtime\lean-4.34.0-windows` directory. Do not
assume another Python build contains the same SQLite version.

1. Check the archive hash, extract into a new empty installation, and retain
   the manifest. Do not overlay a used installation or copy an experimental DB.
2. Open the extracted `QUICKSTART.md`. It gives actual build, configure,
   initialize, submit, publish, expose, acquire and locally admit commands.
   Choose distinct fresh state/scratch/build-work paths on the same fixed
   NTFS volume; provide the documented free-space margin.
3. Use `AGENT-QUICKSTART.md` to create source-request JSON with `make_request.py`.
   An agent chooses its own problem and proof. The node does not impose a task
   queue, common research goal or natural-language intention field.
4. Use `HOSTING.md` for finite continued hosting. A grant explicitly reserves
   sessions and resources. Expiry never silently renews itself. No service
   remains running from the qualification tests.

For convenience, an already extracted and successfully built installation is
retained at `product-local\integrated-release-01\install` beneath the project.
It is qualification evidence, not a mutable working copy. Start from a fresh
extraction for your own node; leave qualification state and receipts untouched.

## What the system does

A contribution is checked relative to an explicit Lean foundation, converted
to canonical content-addressed objects, replayed locally and inversely exported
and replayed before publication. Another node acquires inert packages and
performs its own fresh admission; a sender's success is not inherited trust.
Verified knowledge can be used to build and publish a further contribution.
Custody, availability, discovery and mathematical acceptance are distinct.

Peer serving has no indispensable central endpoint. This candidate's transport
binds **127.0.0.1 only**; configured aliases can be connected through separately
managed authenticated forwarding. No independent-host deployment has been tested.
Discovery is bounded catalog enumeration, not a global mathematical search engine.

Owner-supplied Lean source is executable local input and must be authorized by
that owner. This is not a sandbox for arbitrary hostile source. Peers supply
inert bounded canonical data, never executable checking plans or acceptance
credentials. The OS, local filesystem owner, selected runtimes, implementation
and allowed foundational axioms remain trusted.

## Qualification and limitations

Fresh archive extraction/build, initialization, exact-source request generation,
checked submission/publication/exposure, two real timed hosting sessions and
exhausted-grant reinvocation passed independent evidence audit. Focused request,
hosting and packaging contracts also passed. Prior preserved source cuts have
separate reciprocal-use, replica-custody and bounded recovery evidence.

See [RESULTS.md](RESULTS.md) for the authoritative independent-agent results,
support limits and remaining gates, and the [two-host profile](TWO-HOST-PROFILE.md)
for the proposed unexecuted deployment workflow. The results supersede dated
pending qualification labels inside the immutable archive; they do not change
its code or authorize mutation of old installations. Do not infer scalable useful growth, general
Lean/mathlib compatibility, indefinite storage, arbitrary crash recovery,
independent-host operation or public redistribution permission from this package.
