/-
  Source-only adapter for the exact dependency pins in DEPENDENCIES.json.
  No solver, subprocess or network import. Registration is explicit.
-/
module

public import LPTactic.Registry
public import LPBackendSoplexJSON.Contract

public section

namespace Commons.Witness

open LP

/-- Local operational limits, not mathematical acceptance rules. -/
structure Limits where
  maxPairs : Nat := 8
  maxFileBytes : Nat := 65536
  maxTotalBytes : Nat := 262144
  maxDimension : Nat := 128
  maxNonzeros : Nat := 2048
  maxDigits : Nat := 128
  maxCalls : Nat := 16
  deriving Repr

/-- Paths and labels are chosen by approved local code, never by a response. -/
structure FilePair where
  label : String
  requestPath : System.FilePath
  responsePath : System.FilePath
  deriving Repr

structure Config where
  name : String
  pairs : Array FilePair
  limits : Limits := {}
  deriving Repr

/-- Exact acquired UTF-8 contents. Labels/paths are not hashes or warrants. -/
structure Snapshot where
  files : FilePair
  request : String
  response : String
  requestBytes : Nat
  responseBytes : Nat
  deriving Repr

structure Registration where
  name : String
  limits : Limits
  snapshots : Array Snapshot
  totalFileBytes : Nat
  /-- Shared remaining funded callbacks; failed requests consume this too. -/
  remainingCalls : BaseIO Nat

private def checkLimits (c : Config) : Except String Unit := do
  let l := c.limits
  if c.name.isEmpty ∨ c.name.utf8ByteSize > 64 then
    throw "backend name must contain 1..64 UTF-8 bytes"
  if l.maxPairs = 0 ∨ l.maxPairs > 32 ∨ c.pairs.isEmpty ∨ c.pairs.size > l.maxPairs then
    throw "invalid or exceeded pair count (hard ceiling 32)"
  if l.maxFileBytes = 0 ∨ l.maxFileBytes > 1048576 ∨
      l.maxTotalBytes = 0 ∨ l.maxTotalBytes > 4194304 then
    throw "invalid file/aggregate byte limits (hard ceilings 1/4 MiB)"
  if l.maxDimension = 0 ∨ l.maxDimension > 512 ∨
      l.maxNonzeros = 0 ∨ l.maxNonzeros > 8192 then
    throw "invalid dimensions/nonzero limit (hard ceilings 512/8192)"
  if l.maxDigits = 0 ∨ l.maxDigits > 256 ∨ l.maxCalls = 0 ∨ l.maxCalls > 256 then
    throw "invalid numeral/callback limits (hard ceilings 256/256)"

private def liftCheck {α : Type} (result : Except String α) : IO α :=
  match result with
  | .ok value => pure value
  | .error message => throw <| IO.userError s!"offline witness: {message}"

/-- Open once, retain at most cap bytes, and read at most one rejection sentinel.
The bounded loop also handles partial reads. An outer process deadline is needed
for blocking IO; metadata is not a race-free filesystem sandbox. -/
private def readBounded (path : System.FilePath) (cap : Nat) : IO ByteArray := do
  if (← path.metadata).type != .file then
    throw <| IO.userError "offline witness: expected an approved ordinary file"
  IO.FS.withFile path .read fun handle => do
    let mut data := ByteArray.empty
    for _ in [0:cap + 1] do
      let chunk ← handle.read (min 4096 (cap + 1 - data.size)).toUSize
      if chunk.isEmpty then return data
      data := data ++ chunk
      if data.size > cap then
        throw <| IO.userError "offline witness: file/aggregate byte allowance exceeded"
    throw <| IO.userError "offline witness: bounded file read did not reach EOF"

private def strictUTF8 (data : ByteArray) : IO String :=
  match String.fromUTF8? data with
  | some text => pure text
  | none => throw <| IO.userError "offline witness: invalid UTF-8"

/-- Resource preflight, NOT a JSON or rational decoder. The deliberately narrow
response subset is ASCII, no string escapes, no JSON numbers, depth <= 8.
The maintained decoder supplies all actual JSON/rational semantics afterwards. -/
private def responsePreflight (bytes : ByteArray) (maxDigits : Nat) : Except String Unit := do
  let mut quoted := false
  let mut depth := 0
  let mut stringBytes := 0
  let mut digits := 0
  for byte in bytes do
    let b := byte.toNat
    if b > 127 then throw "response must use the supported ASCII subset"
    if quoted then
      if b = 34 then
        quoted := false
        digits := 0
      else
        if b = 92 ∨ b < 32 then throw "escaped/control response strings are unsupported"
        stringBytes := stringBytes + 1
        if stringBytes > 2 * maxDigits + 16 then throw "response string too long"
        digits := if 48 ≤ b ∧ b ≤ 57 then digits + 1 else 0
        if digits > maxDigits then throw "response numeral digit limit exceeded"
    else
      if b = 34 then
        quoted := true
        stringBytes := 0
        digits := 0
      else if b = 123 ∨ b = 91 then
        depth := depth + 1
        if depth > 8 then throw "response nesting limit exceeded"
      else if b = 125 ∨ b = 93 then
        if depth = 0 then throw "unbalanced response delimiters"
        depth := depth - 1
      else if 48 ≤ b ∧ b ≤ 57 then
        throw "numeric JSON tokens are unsupported; wire rationals must be strings"
  if quoted ∨ depth != 0 then throw "unterminated response string/container"

private def checkRat (bound : Nat) (q : Rat) : Except String Unit := do
  if q.num.natAbs ≥ bound ∨ q.den ≥ bound then
    throw "local request numeral digit limit exceeded"

/-- Bound the already-local problem before string conversion or JSON encoding.
Sparse array size is checked independently of the dimensions. -/
private def requestPreflight {m n : Nat} (l : Limits) (opts : Options)
    (p : Problem m n) : Except String Unit := do
  if m > l.maxDimension ∨ n > l.maxDimension ∨ p.a.size > l.maxNonzeros then
    throw "local request dimensions/sparse-entry limit exceeded"
  let bound := 10 ^ l.maxDigits
  if let some iterations := opts.iterLimit then
    if iterations ≥ bound then throw "local request option numeral limit exceeded"
  checkRat bound p.objOffset
  for q in p.c.toArray do checkRat bound q
  for (_, _, q) in p.a do checkRat bound q
  for (lo, hi) in p.rowBounds.toArray do
    if let some q := lo then checkRat bound q
    if let some q := hi then checkRat bound q
  for (lo, hi) in p.colBounds.toArray do
    if let some q := lo then checkRat bound q
    if let some q := hi then checkRat bound q

private def callback (limits : Limits) (snapshots : Array Snapshot)
    (remaining : IO.Ref Nat) {m n : Nat} (opts : Options) (p : Problem m n) :
    IO (Except SolveError (Solution m n)) := do
  -- No request encoding/decoding work before this atomic debit, including failures.
  let allowed ← remaining.modifyGet fun count =>
    if count = 0 then (false, 0) else (true, count - 1)
  if !allowed then return .error (.bridge "offline witness: callback allowance exhausted")
  match requestPreflight limits opts p with
  | .error message => return .error (.bridge s!"offline witness: {message}")
  | .ok () => pure ()
  let request := LP.Backend.SoplexJSON.encodeRequest opts p
  if request.utf8ByteSize > limits.maxFileBytes then
    return .error (.bridge "offline witness: encoded request exceeds file-byte limit")
  let some selected := snapshots.find? (fun snapshot => snapshot.request == request)
    | return .error (.bridge "offline witness: no exact retained encoded request")
  match LP.Backend.SoplexJSON.decodeResponse m n selected.response with
  | .error _ => return .error (.bridge s!"offline witness: malformed response for {selected.files.label}")
  | .ok (.wireError _) =>
      return .error (.bridge s!"offline witness: retained wire error for {selected.files.label}")
  | .ok (.solution solution) => return .ok solution

/-- Explicitly snapshot approved file pairs and register one opt-in backend.
There is no initializer in this module. The failing probe prevents automatic
selection; use the explicit backend name. Returned data is only proposed evidence.
The existing tactic must construct and kernel-check its actual target proof. -/
def register (config : Config) : IO Registration := do
  liftCheck (checkLimits config)
  let limits := config.limits
  let mut snapshots : Array Snapshot := #[]
  let mut total := 0
  for pair in config.pairs do
    if pair.label.isEmpty ∨ pair.label.utf8ByteSize > 64 then
      throw <| IO.userError "offline witness: pair labels must contain 1..64 UTF-8 bytes"
    if snapshots.any (fun snapshot => snapshot.files.label == pair.label) then
      throw <| IO.userError "offline witness: duplicate pair label"
    let requestData ← readBounded pair.requestPath (min limits.maxFileBytes (limits.maxTotalBytes - total))
    total := total + requestData.size
    let request ← strictUTF8 requestData
    if request.isEmpty then throw <| IO.userError "offline witness: empty retained request"
    if snapshots.any (fun snapshot => snapshot.request == request) then
      throw <| IO.userError "offline witness: duplicate encoded request"
    let responseData ← readBounded pair.responsePath (min limits.maxFileBytes (limits.maxTotalBytes - total))
    total := total + responseData.size
    let response ← strictUTF8 responseData
    liftCheck (responsePreflight responseData limits.maxDigits)
    snapshots := snapshots.push {
      files := pair, request, response,
      requestBytes := requestData.size, responseBytes := responseData.size }
  let remaining ← IO.mkRef limits.maxCalls
  LP.registerStaticBackend config.name 1000 (callback limits snapshots remaining)
    (pure (.error "offline witness backend requires explicit selection"))
  return { name := config.name, limits, snapshots, totalFileBytes := total,
    remainingCalls := remaining.get }

end Commons.Witness
