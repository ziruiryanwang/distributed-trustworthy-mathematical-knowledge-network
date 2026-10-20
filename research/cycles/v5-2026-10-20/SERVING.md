# Ordinary retained-workspace service

Source-only checkpoint, 2026-10-20. Canonical workspace guard passed.

Added `software/v5/client/serve_workspace.py` and `client/SERVING.md` under
root's selected ordinary-service scope. One trusted `main(context)` / async
`serve(context)` opens an existing exact-mode workspace, exposes its unchanged
typed CompositeProvider, writes READY while live, stops within a finite
original deadline with cleanup reserve, attempts shutdown, and reports outcome.
No fixture IDs, new server, math owner, location planner or proof is introduced.

The small composition closes the publication-to-serving product gap. Read-only
means remote routes; workspace/index metadata can change. Inputs must therefore
be mutable ordinary working data, never frozen evidence. Existing store/profile
checks stay authoritative, with no fallback. Constructor-internal failure is
not mislabeled complete cleanup; unsuccessful close gets bounded remaining
component attempts and cannot become PASS.

Root owns exact selections/runtime/Git. `core_growth` owns focused source
controls; `core_release` independently reviews. No source has been executed
by this author. Further changes await their concrete findings; no repeated
proof or memory campaign is requested.
