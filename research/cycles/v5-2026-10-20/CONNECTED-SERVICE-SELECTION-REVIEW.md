# Installed public service: exact selector review

2026-10-20, `core_release`. Source-only review; selector not executed here.

**Clear** `Select-InstalledService.ps1`, SHA-256
`0684e783dc8e11bb758d7fd90b7c8fbefaa5a2b840dd521cceabf31d9e52acb4`,
when root supplies the adopted release
`69d9456eb53135061bc68a8d657ae0f25bc71013cd9c8d2cd5f571c4c7996ef5`
and reviewed adapter
`93ceb7e13afc6cef0fd9f95775051498b14bd8513bfd6ea629dbbef706cc4a76`.

The selector checks exact release role/schema/input and prior advertised-control
basis. It snapshots only adapter and existing runner. It retains the 19 old
runtime/input pins, maps precisely the 18 retained Python rows to their installed
counterparts with matching manifest lengths/hashes, and adds release plus entry
pins: 39 runtime/input pins in total. Actual argv uses installed Python with
`-I -S -B`; the surrounding runner retains its original adopted runtime.

Installed Python presence is required; missing/mismatched rows fail before a
selection is created. The selector accepts exact root-approved SHA parameters,
not an arbitrary unpinned adapter/release. It creates only one fresh plan and
rejects an existing plan/evidence directory. Output is a fresh evidence child
under the original finite runner allocation, not the immutable installation.

The 600 wall / 120 CPU seconds / 512 MiB / six-process envelope is within the
existing runner's limits and contains the adapter's original 570-second deadline.
No Node runtime scan, runtime launch, download or proof operation occurs in the
selector. The public launcher and concrete controllers retain their existing
runtime checks during actual use. The source review
`CONNECTED-INSTALLED-SERVICE-REVIEW.md` governs the adapter's finite behavior.

Generated-plan identity must still be recorded by root at selection. A passing
source review is not execution evidence or final-v5 acceptance.
