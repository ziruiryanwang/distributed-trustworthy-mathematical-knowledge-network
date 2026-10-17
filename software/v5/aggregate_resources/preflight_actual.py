"""Private real-adoption/request preflight. Never run a proof or native host.

Run only under a separately selected outer Job with every existing read pinned.
The prospective request is a quote, not funding. No mathematical authority is
created by Python record validation or by inspecting an untrusted capsule.
"""
from pathlib import Path
import argparse
import hashlib
import os
import stat
import sys
import time
from subprocess import list2cmdline  # Pure quoting only; no subprocess launch.

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
MIB = 1024**2
SOURCE_SHA = {
    "production/producer.py": "5555e944d7473731e3e9095e85c5c57ce89c5f59187f78c5b248b4c1227532f3",
    "production/__init__.py": "c66f4ce32e6a929bf3d0a178fb9c62e6aaaebe45b441a98e4d2bc10b68d916ae",
    "aggregate_resources/producer.py": "1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09",
    "aggregate_resources/__init__.py": "0ca27c691b5afe5ad93086251afb3259491f2ebcaf6e2a9b7ff7b209d4489bb2",
}
RECORDS = {
    "module-base-production-01/profile.json": "71af83f7c4822d8d2a322e93dda5f08a59311614d434ab887cc5c33c318d84d0",
    "module-base-production-01/RESULT.json": "1ccfa4835ce7cf8ef62386bd2fc82a548d7e9b82db948a879ab9809f36027749",
    "aggregate-stage-host-build-01/RESULT.json": "10cbdd0cc233aefb6797c0d8d7756f2bd79030fa7e3f9619208006b11a1dd8db",
    "aggregate-stage-host-build-01-attempt.json": "c812af324580f9227b42cc09f07cdd9a918fd9928444d1fe19d68247434f3050",
    "aggregate-stage-host-build-01-selection.json": "fde4496bea48c5682116c5f2bf7e37bf7834fb422a4abef04b43867dee709326",
    "aggregate-stage-host-build-01/source-map.json": "834a3eb0a9547b235d8ea4ff3440f9536b2d0d0a15e753f1739837bc078455fe",
    "aggregate-stage-host-build-01/compile-command.json": "9d98335db2e8364e2fe0099e71113812162f75c44b111d6ebb9717afe47b259a",
    "proof-memo-image-assembly-01/assembly/RESULT.json": "8a2174ad097333a54f3a314d63f0e646607a639aa5755efdd31c2ee1d08d43ea",
    "proof-memo-image-assembly-01/RESULT.json": "50de313fbc8f20b3f48d971f3183bf66f1079cafe18af460538b414d715a2f4e",
    "proof-memo-image-assembly-01/selection.json": "60b1955f8b7f70b9238693ffb9c31018dc19a2089d6aec13b3238d2810f33600",
    "proof-memo-guest-build-01/RESULT.json": "993233231a722bcfdb4709def236d452a0bbded935bde2a66022ab1780bd8dac",
    "proof-memo-guest-build-01/selection.json": "16730dce90438a8ee83215af842babfc0def7ef1ef89a6a8bf901c8e05b855b9",
    "proof-memo-guest-build-01/SOURCE-MAP.json": "3ba8ee6781f249d9a49e9d1befb4d1becb8f899fd6f1a70270a8fa36eed76829",
    "proof-memo-guest-build-01/ARTIFACT.json": "164c8be3ebe2a1a68a7eeac8439283f3e30a918a0d40f4b37d5087b752c3c683",
    "frontier-capability-execution-01/evidence/RESULT.json": "5d21cb1966dc4dee52d59faf8e68f92aad92907522bb041faf078c53a39f44c6",
    "frontier-capability-execution-01/RESULT.json": "4a08f6eb3a711105aaee1409c84c43260288ece99929cee7a978b541a55a4382",
    "frontier-capability-execution-01/selection.json": "85555faa0313c26919800a8974c81f55e3add29f7d8892cd095314b0b94c02ef",
    "frontier-capability-execution-01/evidence/configuration.json": "d4d9751b155bc4b04e9d110ca23bfe31a8adc34e267d86fd00003da6c64004bd",
    "frontier-capability-execution-01/evidence/COMMAND.json": "655501f4ca0644e6974f22607df29d013acc69b9533f512cfc53c30dbbbc04ad",
}
ASSETS = {
    "stage_host": ("aggregate-stage-host-build-01/aggregate_stage_host.exe", 67992064,
                   "1266b6c990fc21f04f80f88c714a22d7841e4819c64bee0746992a47858a32ac"),
    "snapshot_host": ("aggregate-host-build-01/aggregate_host.exe", 6626304,
                      "b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1"),
    "image": ("proof-memo-image-assembly-01/assembly/aggregate_image.bin", 1745920,
              "98686ced7979d55685c648f441f7ffbe40712e327a1311f9cb076a0c7250e773"),
    "wire": ("frontier-capability-execution-01/evidence/wire.bin", 215540,
             "2aea63ff488a4c012233742306c71526aea37c67d9f8d214e94c0d95d1200cb4"),
    "expected": ("frontier-capability-execution-01/evidence/header.bin", 192,
                 "2bec7b73408dda33c1490360ea34330a846861283a5a5ee6ec6b7632bc5211e4"),
    "capsule": ("frontier-capability-execution-01/evidence/aggregate.snapshot", 37187089,
                "7996306944a51e0eec597266819871115f4bdea1f799c944442e472869465ffd"),
    "parent": ("module-base-production-01/finish-0/receipt.bin", 223594,
               "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path, *, fresh=False):
    need(path.is_absolute() and path.resolve(strict=not fresh) == path, "CANONICAL_PATH")
    for ancestor in [*path.parents, *([] if fresh else [path])]:
        info = ancestor.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400, "NO_REPARSE_INPUT")
    if fresh:
        need(not path.exists() and not path.is_symlink(), "FRESH_PATH")
    else:
        need(stat.S_ISREG(path.stat().st_mode), "ORDINARY_FILE")


def raw_pin(path, expected=None):
    ordinary(path)
    size = path.stat().st_size
    need(0 < size <= 128*MIB, "PIN_BYTES")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == size and (expected is None or digest == expected), "EXACT_PIN")
    return {"path": str(path), "bytes": size, "sha256": digest}


def main():
    started, cpu = time.monotonic(), time.process_time()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated
         and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "CANONICAL_ISOLATED_PREFLIGHT")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    ordinary(output, fresh=True)
    need(output.is_relative_to(HERE) and output.parent.is_dir(), "FRESH_LOCAL_EVIDENCE")
    source_root = Path(__file__).resolve().parents[1]
    need(source_root == output.parent/"sources/software/v5", "ACTUAL_OUTER_SOURCE_SNAPSHOT")
    source_pins = {relative: raw_pin(source_root/relative, digest)
                   for relative, digest in SOURCE_SHA.items()}
    sys.path.insert(0, str(source_root))
    from production import producer as P
    from aggregate_resources import producer as R
    need(Path(P.__file__).resolve() == source_root/"production/producer.py"
         and Path(R.__file__).resolve() == source_root/"aggregate_resources/producer.py"
         and Path(sys.modules["production"].__file__).resolve() == source_root/"production/__init__.py"
         and Path(sys.modules["aggregate_resources"].__file__).resolve() == source_root/"aggregate_resources/__init__.py"
         and R.P is P,
         "ACTUAL_SELECTED_IMPORTS")
    # The enclosing runner creates this exact selection before invoking us.
    selection_path = output.parent/"selection.json"
    selection_pin = raw_pin(selection_path)
    selection = P.parse(selection_path.read_bytes())
    P.fields(selection, ("schema", "name", "sources", "runtime_pins", "argv", "limits"))
    need(selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1"
         and type(selection["runtime_pins"]) is dict, "OUTER_SELECTION")
    for relative, pin in source_pins.items():
        need(selection["sources"].get("software/v5/"+relative) ==
             pin["sha256"], "OUTER_SOURCE_PIN")
    own = raw_pin(Path(__file__).resolve())
    need(selection["sources"].get("software/v5/aggregate_resources/preflight_actual.py") ==
         own["sha256"], "OUTER_ADAPTER_PIN")
    existing = {}

    def bind(path, digest=None, expected_bytes=None):
        pin = raw_pin(path, digest)
        need(expected_bytes is None or pin["bytes"] == expected_bytes, "BOUND_INPUT_BYTES")
        need(selection["runtime_pins"].get(str(path)) == pin["sha256"], "OUTER_RUNTIME_PIN:"+str(path))
        need(str(path) not in existing or existing[str(path)] == pin, "PIN_ROLE_CONFLICT")
        existing[str(path)] = pin
        return pin

    def bind_record(relative):
        return bind(HERE/relative, RECORDS[relative])

    def save(path, value):
        raw = P.encoded(value)
        need(len(raw) <= 2*MIB, "PREFLIGHT_RECORD_BOUND")
        with path.open("xb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        return raw_pin(path)

    def census(reserve=0, reserve_entries=0):
        total, entries = 0, 0
        for parent, dirs, names in os.walk(output, followlinks=False):
            for name in dirs+names:
                path = Path(parent)/name
                need(not path.is_symlink() and not path.is_junction(), "ORDINARY_EVIDENCE")
                entries += 1
                if name in names:
                    total += path.stat().st_size
        need(total+reserve <= 12*MIB and entries+reserve_entries <= 64, "PREFLIGHT_OUTPUT_ENVELOPE")
        return {"bytes": total, "entries": entries}

    output.mkdir()
    owner, planned = None, HERE/"aggregate-production-planned-01"
    report = {"schema": "DMKN_V5_REAL_PRODUCER_PREFLIGHT_V1", "status": "FAIL",
              "authority": "PRIVATE_REAL_RECORD_ADOPTION_AND_REQUEST_ONLY",
              "private_api_test": True, "proof_funding": False, "host_calls": 0,
              "guest_calls": 0, "proof_calls": 0, "mathematical_admission": False,
              "phase": "bind_inputs", "error": None, "final_binding_error": None,
              "memory_sufficiency_established": False, "production_directory_created": False}
    generated = []
    try:
        pins = {relative: bind_record(relative) for relative in RECORDS}
        data = {relative: P.parse(Path(pin["path"]).read_bytes()) for relative, pin in pins.items()}
        assets = {name: bind(HERE/relative, digest, size)
                  for name, (relative, size, digest) in ASSETS.items()}
        template = data["module-base-production-01/profile.json"]
        manifest_pin = template["supervisor_manifest"]
        bind(Path(manifest_pin["path"]), manifest_pin["sha256"], manifest_pin["bytes"])
        manifest = P.parse(Path(manifest_pin["path"]).read_bytes())
        install = Path(manifest_pin["path"]).parent
        for relative in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py"):
            row = manifest["files"][relative]
            bind(install/relative, row["sha256"], row["bytes"])
        for pin in [template["python"], template["python_dll"], *template["runtime_pins"]]:
            bind(Path(pin["path"]), pin["sha256"], pin["bytes"])
        build_root = HERE/"aggregate-stage-host-build-01"
        for relative, row in data["aggregate-stage-host-build-01/source-map.json"].items():
            bind(build_root/"source"/relative, row["sha256"], row["bytes"])
        support = P.parse(P.encoded(template))
        support["host"] = assets["stage_host"]
        support["image_id"] = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"
        support["source_pins"] = [source_pins["production/"+name] for name in P.SOURCE_NAMES]
        profile = {"schema": R.PREFIX+"PROFILE_V2", "support_profile": support,
                   "stage_memory_ceiling_mib": 8192,
                   "source_pins": [source_pins["aggregate_resources/"+name] for name in R.SOURCE_NAMES],
                   "relation_image": "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e",
                   "host_build": {name: pins[path] for name, path in {
                       "result": "aggregate-stage-host-build-01/RESULT.json",
                       "attempt": "aggregate-stage-host-build-01-attempt.json",
                       "selection": "aggregate-stage-host-build-01-selection.json",
                       "source_map": "aggregate-stage-host-build-01/source-map.json",
                       "command": "aggregate-stage-host-build-01/compile-command.json"}.items()},
                   "image_adoption": {name: pins[path] for name, path in {
                       "result": "proof-memo-image-assembly-01/assembly/RESULT.json",
                       "outer": "proof-memo-image-assembly-01/RESULT.json",
                       "selection": "proof-memo-image-assembly-01/selection.json",
                       "guest_build": "proof-memo-guest-build-01/RESULT.json",
                       "guest_selection": "proof-memo-guest-build-01/selection.json",
                       "guest_source_map": "proof-memo-guest-build-01/SOURCE-MAP.json",
                       "artifact": "proof-memo-guest-build-01/ARTIFACT.json"}.items()}}
        snapshot = data["frontier-capability-execution-01/evidence/RESULT.json"]
        actual = snapshot["actual_result"]
        session = {name: assets[name] for name in ("image", "wire", "expected", "capsule")}
        session.update(parents=[assets["parent"]], session_binding=actual["session_binding"],
                       capsule_binding=actual["capsule_binding"], cycles=snapshot["cycles"],
                       po2=snapshot["segment_po2"], segments=actual["segments"], assumptions=actual["assumptions"],
                       snapshot_evidence={name: pins[path] for name, path in {
                           "result": "frontier-capability-execution-01/evidence/RESULT.json",
                           "outer": "frontier-capability-execution-01/RESULT.json",
                           "selection": "frontier-capability-execution-01/selection.json",
                           "configuration": "frontier-capability-execution-01/evidence/configuration.json",
                           "command": "frontier-capability-execution-01/evidence/COMMAND.json"}.items()})
        need((session["segments"], session["assumptions"], session["cycles"], session["po2"]) ==
             (113, 1, 67108864, 19), "EXACT_RETAINED_GEOMETRY")
        caps = {"segment": 1700, "lift": 250, "join": 250, "resolve": 600, "finish": 300}
        walls = {"segment": 420, "lift": 150, "join": 150, "resolve": 600, "finish": 120}
        budget = {"worker_cpu_seconds": 250000, "controller_cpu_seconds": 3600,
                  "wall_seconds": 86400, "output_bytes": 2048*MIB, "output_entries": 8192,
                  "stages": {kind: {"cpu_seconds": cap, "wall_seconds": walls[kind],
                                    "memory_mib": 8192 if kind == "segment" else 4096,
                                    "active_processes": 2, "stdout_bytes": 65536,
                                    "stderr_bytes": 65536, "output_bytes": 524288}
                             for kind, cap in caps.items()}}
        base = data["module-base-production-01/RESULT.json"]
        build = data["aggregate-stage-host-build-01/RESULT.json"]
        acquisition = data["frontier-capability-execution-01/RESULT.json"]
        old = base["carried_external_costs"]
        carried = {
            "worker_cpu_seconds": P.number(base["worker_cpu_charge_this_attempt"])+P.number(base["prior_allowance_worker_charge"])
                +P.number(old["worker_cpu_seconds"])+P.number(build["job"]["cpu_seconds"])
                +P.number(acquisition["result"]["final_job"]["cpu_seconds"]),
            "controller_cpu_seconds": P.number(base["controller_cpu_seconds"])+P.number(base["prior_allowance_controller_cpu"])
                +P.number(old["controller_cpu_seconds"])+P.number(build["controller_cpu_seconds"])
                +P.number(acquisition["wrapper_cpu_seconds"]),
            "wall_seconds": P.number(base["wall_seconds"])+P.number(base["prior_allowance_wall"])
                +P.number(old["wall_seconds"])+P.number(build["wall_seconds"])+P.number(acquisition["wall_seconds"]),
            "scope": "Known base-I production including carried prefix, this aggregate stage-host build and retained capability acquisition only. Active wall sums, not calendar time. Earlier guest/image builds, failed runs, tests and research remain preserved/excluded, not zero; startup/exit tails are not exhaustive. Planning-only subtotal, not funding or full-cost benefit."}
        ordinary(planned, fresh=True)
        request = {"schema": R.PREFIX+"REQUEST_V1",
                   "allowance_id": P.hash_bytes(P.encoded(["NOT_A_PROOF_ALLOWANCE", str(output)])),
                   "session": session, "checkpoints": [], "output_directory": str(planned),
                   "stage_limit": 340, "budget": budget, "prior_attempts": [], "carried_external_costs": carried}
        generated += [save(output/"profile.json", profile), save(output/"prospective-request.json", request)]
        report["phase"] = "real_constructor"
        owner = R.AggregateProducer(profile)
        report["phase"] = "real_private_request"
        sid, inputs, inventory, nodes, chosen_output, prior, envelope = owner._request(request)
        need(chosen_output == planned and inventory == {} and prior == [0, 0, 0, 0, 0]
             and len(nodes) == 340 and nodes[-1][0] == "finish:0", "REAL_RETURNED_PLAN")
        for table in (owner._pins, inputs):
            for path, pin in table.items():
                known = existing.get(path)
                if known is None:
                    known = next((p for p in source_pins.values() if p["path"] == path), None)
                need(known == pin, "UNSELECTED_PRODUCER_READ:"+path)
        counts = {kind: sum(key.startswith(kind+":") for key, _ in nodes) for kind in P.KINDS}
        need(counts == {"segment": 113, "lift": 113, "join": 112, "resolve": 1, "finish": 1}, "EXACT_GRAPH_COUNTS")
        stage_wall_sum = sum(counts[kind]*budget["stages"][kind]["wall_seconds"] for kind in P.KINDS)
        total_wall_slack = budget["wall_seconds"]-stage_wall_sum
        need(stage_wall_sum == 81930 and total_wall_slack == 4470, "HYPOTHETICAL_WALL_CAP_ENVELOPE")
        need(envelope["missing_host_calls"] == 340 and envelope["missing_prover_stages"] == 339
             and envelope["selected_worker_cpu_envelope"] == 249250
             and envelope["new_output_envelope"] == 940048384 and envelope["new_entry_envelope"] == 2724
             and envelope["maximum_host_read_envelope"] == 99141167
             and envelope["full_path_fits_requested_envelopes"] is True, "EXACT_HYPOTHETICAL_ENVELOPE")
        rows, prospective = [], {}
        for key, dependencies in nodes:
            kind, index = key.split(":")
            artifact = planned/(kind+"-"+index)/("receipt.bin" if kind == "finish" else "proof.checkpoint")
            argv = R.stage_argv(support["host"]["path"], support["image_id"], session, key, artifact,
                                [{"path": str(prospective[d])} for d in dependencies])
            units = len(list2cmdline(argv).encode("utf-16-le"))//2+1
            need(units <= 32767, "PROSPECTIVE_WINDOWS_ARGV_LIMIT")
            rows.append({"stage": key, "utf16_units_including_nul": units, "argument_count": len(argv)})
            prospective[key] = artifact
        composite_bound = session["segments"]*budget["stages"]["segment"]["output_bytes"]+assets["parent"]["bytes"]+48
        need(composite_bound == 59468186 and composite_bound < 64*MIB, "CONDITIONAL_COMPOSITE_SERIALIZATION_BOUND")
        generated.append(save(output/"argv-envelope.json", rows))
        report.update(status="PASS_REAL_ADOPTION_AND_REQUEST_PREFLIGHT_ONLY", phase="preflight_complete",
                      profile_id=owner.profile_id, session_id=sid, full_path_envelope=envelope,
                      graph_counts=counts, actual_installation_pin_bytes=sum(p["bytes"] for p in owner._pins.values()),
                      actual_request_input_bytes=sum(p["bytes"] for p in inputs.values()),
                      maximum_argv=max(rows, key=lambda r: r["utf16_units_including_nul"]),
                      conditional_composite_byte_bound=composite_bound,
                      hypothetical_stage_wall_cap_sum_seconds=stage_wall_sum,
                      hypothetical_total_wall_slack_seconds=total_wall_slack,
                      wall_scope="CAP_SUM_SLACK_FOR_CONTROLLER_TRANSITIONS_AND_FINALIZATION_NOT_COMPLETION_GUARANTEE",
                      feasibility_scope="STATIC_QUOTE_UNDER_ARTIFACT_CAPS_NOT_ACTUAL_PROOF_SIZE_CPU_OR_MEMORY_GUARANTEE",
                      carried_external_costs=carried, quote_output_path=str(planned))
    except BaseException as error:
        report.update(status="FAIL", error=type(error).__name__+": "+str(error)[:2000])
    try:
        if owner is not None:
            owner.close()
            need(owner.report()["closed"] is True, "OWNER_CLOSED")
        for pin in [*existing.values(), *source_pins.values(), own, selection_pin, *generated]:
            need(raw_pin(Path(pin["path"])) == pin, "FINAL_INPUT_OR_CONTROL_CHANGED")
        ordinary(planned, fresh=True)
        report["final_binding_validated"] = True
    except BaseException as error:
        report.update(status="FAIL", final_binding_validated=False,
                      final_binding_error=type(error).__name__+": "+str(error)[:2000])
    generated.append(save(output/"input-map.json", {"existing_inputs": existing, "source_pins": source_pins,
                                                    "adapter": own, "outer_selection": selection_pin,
                                                    "trust_scope": "EXPLICIT_PINS_NOT_HERMETIC_OR_MATHEMATICAL_AUTHORITY"}))
    report["output_census_before_result"] = census(4*MIB, 2)
    report.update(controller_cpu_seconds_before_final_report=time.process_time()-cpu,
                  wall_seconds_before_final_report=time.monotonic()-started,
                  accounting="OUTER_JOB_IS_INCLUSIVE;DO_NOT_ADD_INNER_CONTROLLER_AGAIN;FINAL_EXIT_TAIL_EXCLUDED")
    generated.append(save(output/"RESULT.json", report))
    try:
        for pin in [*existing.values(), *source_pins.values(), own, selection_pin, *generated]:
            need(raw_pin(Path(pin["path"])) == pin, "POST_RESULT_BINDING_CHANGED")
        ordinary(planned, fresh=True)
        census(2*MIB, 1)
    except BaseException as error:
        report.update(status="FAIL", final_binding_validated=False,
                      final_binding_error=type(error).__name__+": "+str(error)[:2000])
        save(output/"FINALIZATION-FAILED.json", {"status": "FINALIZATION_FAILED", "overrides_result": True,
                                                "error": report["final_binding_error"]})
    print(P.encoded(report).decode(), end="", flush=True)
    return 0 if report["status"] == "PASS_REAL_ADOPTION_AND_REQUEST_PREFLIGHT_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
