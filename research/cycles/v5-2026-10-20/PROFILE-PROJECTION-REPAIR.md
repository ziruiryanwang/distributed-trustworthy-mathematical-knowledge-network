# Projection controls 02: harness-only repair

2026-10-20, core_release. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source-only root assignment; no Python import, control run, build, process,
network, mathematical operation or Git mutation was performed by this author.

## Actual defect and preserved predecessor

The root-reported first run completed its eight assertions, but independent
raw-stderr review found asynchronous Proactor callback `TypeError`s. The test
guard replaced the **class** `socket.socket` with a Mock. Windows' already-created
event-loop infrastructure still uses that class in `isinstance` checks after
test setup, so the guard itself broke those callbacks. Eight passing unittest
cases alone do not establish a clean run. The original attempt is noisy/held,
not silently relabeled or erased; root owns its exact saved outcome audit.

Frozen predecessor `software/v5/base_projection/controls.py` remains SHA-256
`ddbfaa67a375d2289f6fcf0e352386090ac0137df8f2cade49d02127f3860aa7`.
No product implementation change follows from this harness diagnosis.

## Exact fresh successor

`software/v5/base_projection/controls02.py`, SHA-256
`814863a6fa778ae431f36178ba080071f8c434024bbd17a78a0144512b768b1b`.

Created from the frozen predecessor using `apply_patch`. Only these source
changes are selected:

1. Guard `socket.socket.__init__`, preserving the real class and existing socket
   instances used by the event loop. Do not introduce a subclass, metaclass,
   replacement class or fake type test. The already-created loop infrastructure
   retains its normal receive/send methods. Existing subprocess and asynchronous
   network-start guards remain unchanged.
2. Install a per-loop exception handler during each selected test and teardown.
   Keep a total exception count plus at most sixteen bounded context records;
   delegate to the previous/default handler to preserve ordinary stderr evidence.
   Teardown drains resources, yields once to queued callbacks, records the count
   and contexts, and fails if any unexpected exception was observed. Restore the
   previous handler afterward. This is not an exhaustive monitor after restoration.
3. Correct the successor's self-provenance field to hash `controls02.py`, rather
   than claiming the frozen predecessor was the executed source.

Exactly the same eight selected groups, fixtures, product sources, assertions,
resource/cleanup scenarios and exclusions remain. No new mathematical, peer or
service workload is added. The independent actual review must still inspect raw
stderr as well as the per-test zero-exception records and enclosing closure;
the new local handler is not a substitute for that audit.

Root explicitly confirmed the constructor-method guard after coordinating the
reviewer's earlier alternative network-method suggestion. No further guard
variation or retry is selected by this note. The successor has not been executed
by its author; root owns a fresh finite selector and any subsequent launch.
