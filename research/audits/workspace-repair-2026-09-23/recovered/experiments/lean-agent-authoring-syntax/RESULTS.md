# Lean agent authoring syntax probe

This separate probe used only trivial reflexivity goals. It did not run the U1 product or check the U1 theorem.

## Runtime and invocation

- Executable: `E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin\lean.exe`
- Working directory: `E:\Distributed Verifiable Mathematical Knowledge Network\experiments\lean-agent-authoring-syntax`
- Invocation: `System.Diagnostics.ProcessStartInfo` with `UseShellExecute=false`, `CreateNoWindow=true`, UTF-8 redirected stdout/stderr, and `WaitForExit(15000)`; a timed-out process would have been killed. All five calls completed before the timeout.
- Effective executable and exact arguments (each line is one separate invocation):

```text
"E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin\lean.exe" --version
"E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin\lean.exe" "E:\Distributed Verifiable Mathematical Knowledge Network\experiments\lean-agent-authoring-syntax\01-term.lean"
"E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin\lean.exe" "E:\Distributed Verifiable Mathematical Knowledge Network\experiments\lean-agent-authoring-syntax\02-same-line-by-exact.lean"
"E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin\lean.exe" "E:\Distributed Verifiable Mathematical Knowledge Network\experiments\lean-agent-authoring-syntax\03-multiline-by-exact.lean"
"E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows\bin\lean.exe" "E:\Distributed Verifiable Mathematical Knowledge Network\experiments\lean-agent-authoring-syntax\04-multiline-by-let.lean"
```

## Observed results

| Invocation | Exit code | Timed out | stdout | stderr / diagnostics |
| --- | ---: | --- | --- | --- |
| `--version` | 0 | no | `Lean (version 4.34.0, x86_64-w64-windows-gnu, commit 293d5d0c0c3f3dded4688b3ccd6a33939ac5102b, Release)` | empty |
| [01-term.lean](01-term.lean) | 0 | no | empty | empty |
| [02-same-line-by-exact.lean](02-same-line-by-exact.lean) | 0 | no | empty | empty |
| [03-multiline-by-exact.lean](03-multiline-by-exact.lean) | 0 | no | empty | empty |
| [04-multiline-by-let.lean](04-multiline-by-let.lean) | 0 | no | empty | empty |

The multiline files put `by` at column 20 (zero-based) and the following proof line at column 2. Ordinary Lean 4.34.0 accepts both `exact` and `let` in that layout. This falsifies a general Lean indentation or `let`-tactic explanation for the frozen U1 source rejection. The U1 product elaborated source against a reconstructed environment and a larger nested theorem statement; this standalone runtime probe does not isolate the product-specific cause or establish mathematical acceptance of any U1 result.
