import BaselineArtifactCore02

def main (args : List String) : IO UInt32 := do
  try
    match args with
    | [sysroot, requestPath, reportPath] =>
        OrdinaryLean.BaselineArtifacts.run
          (← OrdinaryLean.BaselineArtifacts.absolutePath sysroot)
          (← OrdinaryLean.BaselineArtifacts.absolutePath requestPath)
          (← OrdinaryLean.BaselineArtifacts.absolutePath reportPath)
        return 0
    | _ => OrdinaryLean.BaselineArtifacts.fail "USAGE sysroot request report"
  catch error =>
    let stderr ← IO.getStderr
    stderr.putStrLn (String.ofList (error.toString.toList.take 2048))
    stderr.flush
    return 1
