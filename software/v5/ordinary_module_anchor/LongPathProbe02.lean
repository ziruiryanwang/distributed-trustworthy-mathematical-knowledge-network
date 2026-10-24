import Lean.Environment
import Lean.Util.Path
import Lean.Data.Json

/- Read-only diagnostic of a selected, already locally registered module.
   One mode per process: no old proof checking, artifact production, plugins,
   extension loading or owner access. The launcher authenticates all five parts.
   Successful imports expose only whether the expected definition is present. -/

open Lean

def probe (args : List String) : IO Json := do
  let [sysroot, directory, moduleText, spelling, visibility] := args
    | throw <| IO.userError "expected sysroot directory module spelling visibility"
  unless spelling == "raw" || spelling == "extended" do
    throw <| IO.userError "invalid spelling"
  unless visibility == "private" || visibility == "exported" do
    throw <| IO.userError "invalid visibility"
  let suffixes := #[".olean", ".olean.server", ".olean.private", ".ir.sig", ".ir"]
  let pathsFor (mode : String) := suffixes.map fun suffix =>
    let pathPrefix := if mode == "extended" then "\\\\?\\" else ""
    System.FilePath.mk (pathPrefix ++ directory ++ "\\" ++ moduleText ++ suffix)
  let paths := pathsFor spelling
  let mut metadata : Array Json := #[]
  for mode in #["raw", "extended"] do
    for path in pathsFor mode do
      let entry ← try
        let value ← path.symlinkMetadata
        pure <| Json.mkObj [
          ("spelling", toJson mode), ("path", toJson path.toString), ("ok", toJson true),
          ("is_file", toJson (value.type == .file)),
          ("bytes", toJson value.byteSize.toNat), ("links", toJson value.numLinks)]
      catch error =>
        pure <| Json.mkObj [
          ("spelling", toJson mode), ("path", toJson path.toString), ("ok", toJson false),
          ("error", toJson error.toString)]
      metadata := metadata.push entry
  searchPathRef.set [System.FilePath.mk sysroot / "lib" / "lean"]
  let moduleName := Name.mkSimple moduleText
  let artifacts := ({} : NameMap ImportArtifacts).insert moduleName
    (ImportArtifacts.ofArrays #[#[paths[0]!, paths[1]!, paths[2]!], #[paths[3]!, paths[4]!]])
  let imported ← try
    let level := if visibility == "private" then OLeanLevel.private else OLeanLevel.exported
    let env ← importModules
      #[{ module := moduleName, importAll := false, isExported := true, isMeta := false }]
      {} 0 (plugins := #[]) (leakEnv := false) (loadExts := false)
      (level := level) (arts := artifacts)
    let expectedDefinition := match env.find? `CommonsPackageExample.applyTwice with
      | some (.defnInfo _) => true
      | _ => false
    pure <| Json.mkObj [("ok", toJson true), ("expected_definition", toJson expectedDefinition)]
  catch error =>
    pure <| Json.mkObj [("ok", toJson false), ("error", toJson error.toString)]
  return Json.mkObj [
    ("schema", toJson "DMKN_LONG_PATH_NATIVE_PROBE_V1"),
    ("spelling", toJson spelling), ("visibility", toJson visibility),
    ("metadata", .arr metadata), ("import", imported)]

def main (args : List String) : IO UInt32 := do
  let report ← probe args
  IO.println report.compress
  return 0
