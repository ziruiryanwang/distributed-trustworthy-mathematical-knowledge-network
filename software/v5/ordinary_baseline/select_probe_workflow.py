"""Pin one saved-snapshot diagnostic, never launch or accept mathematics."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_baseline/"
MIB = 1024**2


def need(ok,code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("workflow-sha256","probe-sha256","build-sha256","build-result-sha256","build-selection-sha256"):
        parser.add_argument("--"+name,required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PROBE_SELECTOR_PROCESS")
    need(all(len(value) == 64 and all(c in "0123456789abcdef" for c in value)
             for value in vars(args).values()), "PROBE_SELECTOR_HASHES")
    path = ROOT/PREFIX/"probe_workflow.py"
    with path.open("rb") as stream:
        raw = stream.read(MIB+1)
    need(len(raw) <= MIB and hashlib.sha256(raw).hexdigest() == args.workflow_sha256, "PROBE_SELECTOR_WORKFLOW_PIN")
    spec = importlib.util.spec_from_file_location("_selected_view_probe",path)
    W = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = W
    exec(compile(raw,str(path),"exec"),W.__dict__)
    H = W.utility(ROOT/PREFIX/"native_workflow02.py")
    B = H.helper()
    deadline = time.monotonic()+60
    runtime = {}
    def check():
        need(time.monotonic() < deadline,"PROBE_SELECTOR_DEADLINE")
    def pin(path,expected=None,maximum=128*MIB):
        value = B.pin(B.ordinary(path),check,maximum)["sha256"]
        need(expected is None or value == expected,"PROBE_SELECTOR_PIN:"+str(path))
        need(str(path) not in runtime or runtime[str(path)] == value,"PROBE_SELECTOR_CONFLICT")
        runtime[str(path)] = value
        return value
    authorized = {"build":args.build_sha256,"result":args.build_result_sha256,"selection":args.build_selection_sha256}
    _, selected_build = W.inspect_build(H,B,authorized,args.probe_sha256,check)
    for name,value in selected_build.items():
        pin(Path(name),value["sha256"],512*MIB)
    template = H.LOCAL/"ordinary-preview-public-01.selection.json"
    pin(template,"613e28c8da5fde5d5e570e46d52bfe94cb56b6fa2b0c6037f26592095796c5c7")
    template_raw = H.read(template)
    need(H.sha(template_raw) == runtime[str(template)],"PROBE_SELECTOR_TEMPLATE_CHANGED")
    for name,digest in json.loads(template_raw)["runtime_pins"].items():
        if any(Path(name).is_relative_to(root) for root in (H.PACKAGE,H.PYTHON,H.LEAN)):
            pin(Path(name),digest)
    for relative,digest in W.FIXED.items():
        pin(W.OLD/relative,digest,2*MIB)
    sources = {PREFIX+name:pin(ROOT/PREFIX/name,digest,MIB) for name,digest in W.SOURCES.items()}
    sources[PREFIX+"probe_workflow.py"] = pin(ROOT/PREFIX/"probe_workflow.py",args.workflow_sha256,MIB)
    sources[PREFIX+"ReferenceViewProbe.lean"] = pin(ROOT/PREFIX/"ReferenceViewProbe.lean",args.probe_sha256,MIB)
    for name in (PREFIX+"select_probe_workflow.py","tools/Run-V5-Check.py"):
        sources[name] = pin(ROOT/name,maximum=MIB)
    pin(ROOT/H.BUILDER,H.BUILDER_SHA,MIB)
    need(len(runtime) <= 256 and str(H.PYTHON/"python.exe") in runtime,"PROBE_SELECTOR_RUNTIME_BOUND")
    destination = W.LOCAL/(W.NAME+".selection.json")
    B.ordinary(destination,fresh=True)
    B.ordinary(W.LOCAL/W.NAME,directory=True,fresh=True)
    selection = {"schema":"DMKN_V5_LOCAL_CHECK_V1","name":W.NAME,"sources":sources,"runtime_pins":runtime,
        "argv":[str(H.PYTHON/"python.exe"),"-I","-S","-B","{snapshot}/"+PREFIX+"probe_workflow.py",
            "--source-root","{snapshot}","--output","{output}/probe","--probe-sha256",args.probe_sha256,
            "--build-sha256",args.build_sha256,"--build-result-sha256",args.build_result_sha256,
            "--build-selection-sha256",args.build_selection_sha256],
        "limits":{"wall_seconds":90,"cpu_seconds":45,"memory_mib":1536,"active_processes":4,
                  "stdout_bytes":MIB,"stderr_bytes":MIB}}
    raw = H.encoded(selection)
    need(len(raw) <= MIB,"PROBE_SELECTOR_BYTES")
    B.fresh_bytes(destination,raw)
    need(B.pin(destination,check,MIB) == {"bytes":len(raw),"sha256":H.sha(raw)},"PROBE_SELECTOR_READBACK")
    print(json.dumps({"selection":str(destination),"sha256":H.sha(raw),"runtime_pin_count":len(runtime),
                      "runtime":"NOT_STARTED"}),flush=True)


if __name__ == "__main__":
    main()
