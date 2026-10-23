import OriginalExpr

open Lean OrdinaryLean.ExprCodec

namespace OrdinaryLean.CodecChecks

def ensure (label : String) (condition : Bool) : IO Unit := do
  unless condition do throw <| IO.userError s!"CHECK_FAILED {label}"

def refuses (label expected : String) (action : IO α) : IO Unit := do
  let caught ← try
    discard <| action
    pure false
  catch error =>
    pure ((error.toString.splitOn expected).length > 1)
  ensure label caught

def allowed : Std.HashSet Name := (({} : Std.HashSet Name).insert ``Nat).insert ``String

def roundtrip (label : String) (expr : Expr) (params : List Name := []) : IO Unit := do
  let encoded ← encode params expr
  let decoded ← decode params allowed encoded
  ensure label (expr.equal decoded)

def packet (levels expressions : Array Json) (root : Nat) : Json :=
  arr #[Json.str format, arr levels, arr expressions, num root]

def run : IO Unit := do
  let nat := mkConst ``Nat
  let x := Expr.lam `x nat (.bvar 0) .default
  let y := Expr.lam `y nat (.bvar 0) .default
  roundtrip "named-binders-and-distinct-sharing" (.app x y)
  let xJson ← encode [] x
  let yJson ← encode [] y
  ensure "binder-label-identity" (xJson != yJson)
  let implicitX := Expr.lam `x nat (.bvar 0) .implicit
  ensure "annotation-identity" ((← encode [] implicitX) != xJson)
  roundtrip "anonymous-binder" (.lam .anonymous nat (.bvar 0) .strictImplicit)
  roundtrip "original-universe" (.forallE `a (.sort (.param `universe_name)) (.bvar 0) .instImplicit)
    [`universe_name]
  let letFalse := Expr.letE `bound nat (.lit (.natVal 9)) (.bvar 0) false
  let letTrue := Expr.letE `bound nat (.lit (.natVal 9)) (.bvar 0) true
  roundtrip "let-false" letFalse
  roundtrip "let-true" letTrue
  ensure "nondep-identity" ((← encode [] letFalse) != (← encode [] letTrue))
  ensure "erase-only-mdata" ((← encode [] (.mdata {} x)) == xJson)
  roundtrip "large-native-nat" (.lit (.natVal (2^160 + 17)))
  roundtrip "native-utf8-string" (.lit (.strVal "mathematics λ 数学"))
  roundtrip "zero-native-nat" (.lit (.natVal 0))
  let singleDot := Name.str .anonymous "a.b"
  let splitDot := Name.str (.str .anonymous "a") "b"
  ensure "component-names" ((← encodeName singleDot) != (← encodeName splitDot))
  ensure "anonymous-name" ((← decodeName (arr #[])).isAnonymous)
  let mut shared := nat
  for _ in [:100] do shared := .app shared shared
  let sharing ← encode [] shared { maxExprs := 128, maxDepth := 256 }
  let fields ← arrayOf sharing
  ensure "linear-dag-nodes" ((← arrayOf fields[2]!).size == 101)
  ensure "shared-roundtrip" (shared.equal (← decode [] allowed sharing { maxExprs := 128, maxDepth := 256 }))
  refuses "free-root" "OPEN_EXPRESSION" (encode [] (.bvar 0))
  refuses "undeclared-level" "UNDECLARED_LEVEL_PARAMETER" (encode [] (.sort (.param `missing)))
  refuses "duplicate-params" "PARAMETER_NAME" (encode [`u, `u] nat)
  refuses "wrong-allowed-context" "UNBOUND_REFERENCE" (decode [] {} (← encode [] nat))
  refuses "name-byte-limit" "BYTES_BOUND" (decode [] allowed xJson { maxNameBytes := 0 })
  refuses "node-limit" "EXPRESSION_NODE_BOUND" (decode [] allowed xJson { maxExprs := 1 })
  refuses "depth-limit" "DEPTH_BOUND" (decode [] allowed xJson { maxDepth := 1 })
  let stringJson ← encode [] (.lit (.strVal "abc"))
  refuses "literal-limit" "BYTES_BOUND" (decode [] allowed stringJson { maxLiteralBytes := 2 })
  refuses "aggregate-literal-limit" "BYTES_BOUND" (decode [] allowed stringJson { maxTotalLiteralBytes := 2 })
  refuses "forward-reference" "BACKWARD_INDEX"
    (decode [] allowed (packet #[] #[arr #[num 3, num 0, num 0]] 0))
  refuses "open-decoded-root" "ROOT_OR_SCOPE"
    (decode [] allowed (packet #[] #[arr #[num 0, num 0]] 0))
  refuses "leading-zero-natural" "NAT_MAGNITUDE_CANONICAL"
    (decode [] allowed (packet #[] #[arr #[num 7, bytesJson ⟨#[0, 1]⟩]] 0))
  refuses "invalid-utf8" "STRING_UTF8"
    (decode [] allowed (packet #[] #[arr #[num 9, bytesJson ⟨#[255]⟩]] 0))
  refuses "duplicate-or-orphan-node" "NONCANONICAL_DAG"
    (decode [] allowed (packet #[] #[arr #[num 7, bytesJson ⟨#[]⟩],
      arr #[num 7, bytesJson ⟨#[]⟩]] 1))
  refuses "forbidden-evaluation" "FORBIDDEN_SEMANTIC_NAME" (encode [] (mkConst ``Lean.reduceNat))
  IO.println "ORDINARY_CODEC_CHECKS_PASS syntax_only=true mathematical_acceptance=false"

end OrdinaryLean.CodecChecks

def main : IO Unit := OrdinaryLean.CodecChecks.run
