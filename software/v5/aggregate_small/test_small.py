"""Changed-boundary controls only: no native process, build, guest or proof.

Installation, build/image and snapshot adoption are explicitly synthetic.
The real controller constructor, request, graph, manifest and dispatch accounting
are exercised. No predecessor test module is imported or old suite repeated.
"""
from copy import deepcopy
import argparse
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch

SNAPSHOT_V5 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SNAPSHOT_V5))
from aggregate_small import producer as A
from production import producer as P

OUTPUT = None
TEST_COUNT = 12
DISPATCHES = []


def saved(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
    return P.file_pin(path)


def checkpoint(key, binding, count=100):
    kind, index = key.split(":")
    payload = b"X"*(count-64-len(kind))
    return (b"DMKNAP01"+struct.pack("<I",1)+bytes.fromhex(binding)
            +struct.pack("<Q",len(kind))+kind.encode()
            +struct.pack("<IQ",int(index),len(payload))+payload)


class InertSupervisor:
    CEILINGS = {"memory_mib": 8192}

    def absolute(self, value, *, directory=False, fresh=False):
        path = Path(value)
        P.require(path.is_absolute() and path.resolve() == path, "SYNTHETIC_ABSOLUTE")
        P.require(not path.exists() if fresh else
                  (path.is_dir() if directory else path.is_file()), "SYNTHETIC_EXISTENCE")
        return path

    def overlap(self, left, right):
        return left.is_relative_to(right) or right.is_relative_to(left)

    def save_new(self, path, value):
        saved(Path(path), P.encoded(value))

    def supervise(self, argv, cwd, evidence, limits, job):
        # Only inspect actual durable controller output. Never launch a process
        # or manufacture a successful checkpoint/receipt.
        manifest = P.file_pin(Path(argv[-3]))
        P.require(manifest["bytes"] == int(argv[-2]) and manifest["sha256"] == argv[-1],
                  "DURABLE_MANIFEST_MATCHES_ARGV")
        value = P.parse(Path(manifest["path"]).read_bytes())
        reservation = P.parse((Path(argv[10]).parent/"reservation.json").read_bytes())
        P.require(reservation["argv"] == argv and reservation["limits"] == limits,
                  "DURABLE_RESERVATION")
        P.require(value["stage"] == argv[8]+":"+argv[9] and value["dependencies"] == [],
                  "EXACT_FIRST_SEGMENT_MANIFEST")
        DISPATCHES.append({"manifest":manifest,"reservation":reservation,
                           "argv":argv,"scope":"INERT_NO_PROCESS"})
        return {"status":"COMMAND_FAILED","child_exit_code":1,
            "direct_child_reaped":True,"job_closed":True,"cleanup_errors":[],
            "termination_requested":False,"final_job":{"cpu_seconds":0,
                "active_processes":0,"terminated_processes":0}}


class SyntheticSupport:
    def __init__(self, install):
        self._A, self._Job, self._install, self._pins = InertSupervisor(), object, install, {}

    def _check(self, pins):
        for pin in pins.values():
            P.require(P.file_pin(Path(pin["path"])) == pin, "SYNTHETIC_PIN_CHANGED")

    def _read(self, pin, maximum):
        P.pin_fields(pin,maximum)
        self._check({pin["path"]:pin})
        return Path(pin["path"]).read_bytes()

    def close(self):
        pass


class Fixture:
    def __init__(self, name, segments=1, assumptions=0):
        self.path = OUTPUT/name
        self.path.mkdir()
        self.install = self.path/"inputs"
        self.install.mkdir()
        def put(name, raw):
            return saved(self.install/name,raw)
        support = {"schema":"SYNTHETIC_SUPPORT_NOT_ADOPTION",
            "host":put("host.fake",b"NOT_AN_EXECUTABLE"),
            "image_id":"01"*32,"foundation":"03"*32,"policy":"04"*32}
        self.image = put("image.fake",b"SYNTHETIC_IMAGE")
        self.profile = {"schema":A.PREFIX+"PROFILE_V1","support_profile":support,
            "source_pins":[P.file_pin(Path(A.__file__).resolve().parent/n) for n in A.SOURCE_NAMES],
            "relation_image":"02"*32,"host_build":{},"image_adoption":{},
            "stage_memory_ceiling_mib":4096}
        header = (b"DMKNA002"+struct.pack("<I",2)
            +bytes.fromhex(support["image_id"]+"02"*32+support["foundation"]+support["policy"])
            +bytes.fromhex("05"*32)+struct.pack("<IQQ",1,0,1))
        self.session = {"image":self.image,
            "wire":put("wire.bin",b"DMKNAI02"+struct.pack("<I",2)+bytes.fromhex(support["image_id"])),
            "expected":put("header.bin",header),
            "capsule":put("capsule.bin",b"DMKNAS01"+struct.pack("<I",1)+bytes.fromhex("06"*32)),
            "parents":[put("parent-"+str(i)+".bin",b"NOT_A_RECEIPT") for i in range(assumptions)],
            "session_binding":"06"*32,"capsule_binding":"07"*32,
            "cycles":1<<26,"po2":18,"segments":segments,"assumptions":assumptions,
            "snapshot_evidence":{"synthetic":put("snapshot.fake",b"NOT_SNAPSHOT_ADOPTION")}}
        stage = dict(cpu_seconds=1,wall_seconds=10,memory_mib=1,active_processes=1,
                     stdout_bytes=4096,stderr_bytes=4096,output_bytes=4096)
        self.request = {"schema":A.PREFIX+"REQUEST_V1","allowance_id":"08"*32,
            "session":self.session,"checkpoints":[],"output_directory":str(self.path/"attempt"),
            "stage_limit":1,"budget":dict(worker_cpu_seconds=500000,controller_cpu_seconds=60,
                wall_seconds=172800,output_bytes=2304*P.MIB,output_entries=8192,
                stages={kind:dict(stage) for kind in P.KINDS}),
            "prior_attempts":[],"carried_external_costs":dict(worker_cpu_seconds=0,
                controller_cpu_seconds=0,wall_seconds=0,scope="SYNTHETIC_CHANGED_BOUNDARY_CONTROL")}

    def owner(self, profile=None):
        with patch.object(P,"Producer",lambda p:SyntheticSupport(self.install)), \
             patch.object(A.AggregateProducer,"_adopt_build",lambda o:None), \
             patch.object(A.AggregateProducer,"_adopt_image",lambda o:setattr(o,"_image",self.image)):
            owner = A.AggregateProducer(deepcopy(self.profile if profile is None else profile))
        owner._snapshot = lambda s,e,i:None
        owner._snapshot_build_pins = {}
        return owner

    def rows(self, key):
        return [{"key":d,"file":{"path":str(self.install/(d.replace(":","-")+".checkpoint")),
                 "bytes":100,"sha256":"09"*32}}
                for d in dict(A.graph(self.session["segments"],self.session["assumptions"]))[key]]


class SmallControls(unittest.TestCase):
    def test_maximum_graph_and_iterative_missing_plan(self):
        nodes = A.graph(256,8)
        self.assertEqual(len(nodes),776)
        self.assertEqual(len(dict(nodes)),776)
        self.assertEqual(nodes[-1],("finish:0",tuple("segment:"+str(i) for i in range(256))+("resolve:7",)))
        seen = set()
        for key,deps in nodes:
            self.assertTrue(set(deps) <= seen)
            seen.add(key)
        self.assertEqual(A.missing_plan(256,8,{}),nodes)
        self.assertEqual(A.missing_plan(256,8,{k:None for k,_ in nodes[:-1]}),[nodes[-1]])
        cached = {"resolve:7":None}
        self.assertEqual(len(A.missing_plan(256,8,cached)),257)
        for n,m in ((257,0),(0,0),(256,9),(True,0),(256,False)):
            with self.subTest(n=n,m=m), self.assertRaises(ValueError): A.graph(n,m)

    def test_canonical_stage_keys_and_membership(self):
        for key in ("segment:255","lift:255","join:255","resolve:7","finish:0"):
            self.assertEqual(A.stage_key(*A.split_key(key)),key)
        for key in ("segment:256","segment:01","segment:+1","segment:-1","segment:１",
                    "finish:1","join:0","resolve:8","segment:1:2","bogus:0"):
            with self.subTest(key=key), self.assertRaises(ValueError): A.split_key(key)
        with self.assertRaises(ValueError): A.missing_plan(256,0,{"finish:0":None})

    def test_exact_manifest_order_missing_extra_and_duplicate(self):
        f = Fixture("ordered",3,2)
        for key in ("segment:2","lift:2","join:2","resolve:1","finish:0"):
            rows = f.rows(key)
            value = A.dependency_manifest(f.session,key,rows)
            self.assertEqual(value["dependencies"],rows)
            self.assertEqual(value["session_binding"],f.session["session_binding"])
            if rows:
                for invalid in (rows[:-1],rows+rows[:1]):
                    with self.assertRaises(ValueError): A.dependency_manifest(f.session,key,invalid)
            if len(rows)>1:
                with self.assertRaises(ValueError): A.dependency_manifest(f.session,key,list(reversed(rows)))

    def test_finish_257_rows_and_258_refusal(self):
        f = Fixture("finish-count",256,8)
        rows = f.rows("finish:0")
        self.assertEqual(len(rows),257)
        raw = A.encoded(A.dependency_manifest(f.session,"finish:0",rows))
        self.assertLessEqual(len(raw),256*1024)
        with self.assertRaises(ValueError): A.dependency_manifest(f.session,"finish:0",rows+rows[:1])

    def test_manifest_pin_bounds_and_session_digest(self):
        f = Fixture("pins",1,0)
        for field,value in (("bytes",True),("bytes",A.ARTIFACT_LIMIT+1),
                            ("sha256","A"*64),("path","relative"),("path","E:\\"+"x"*513)):
            rows = f.rows("lift:0"); rows[0]["file"][field] = value
            with self.subTest(field=field,value=str(value)[:25]), self.assertRaises(ValueError):
                A.dependency_manifest(f.session,"lift:0",rows)
        session = {**f.session,"capsule_binding":"not-a-digest"}
        with self.assertRaises(ValueError): A.dependency_manifest(session,"segment:0",[])

    def test_constant_argv_shape_and_windows_quoted_length(self):
        f = Fixture("argv",256,8)
        manifest = saved(f.path/"dependencies.json",A.encoded(A.dependency_manifest(f.session,"finish:0",f.rows("finish:0"))))
        argv = A.stage_argv(f.profile["support_profile"]["host"]["path"],"01"*32,
                            f.session,"finish:0",f.path/"receipt.bin",manifest)
        self.assertEqual(len(argv),24)
        self.assertEqual(argv[1],"stage-manifest")
        self.assertEqual(argv[-3:],[manifest["path"],str(manifest["bytes"]),manifest["sha256"]])
        with self.assertRaisesRegex(ValueError,"WINDOWS_COMMAND_LINE_LIMIT"):
            A.stage_argv("x"*32768,"01"*32,f.session,"finish:0",f.path/"receipt.bin",manifest)

    def test_new_profile_request_and_fixed_geometry(self):
        f = Fixture("request",256,8)
        owner = f.owner(); result = owner._request(deepcopy(f.request))
        self.assertEqual(result[-1]["missing_host_calls"],776)
        for field,value in (("po2",19),("cycles",(1<<26)+1),("segments",257)):
            req = deepcopy(f.request); req["session"][field]=value
            with self.subTest(field=field), self.assertRaises(ValueError): owner._request(req)
        legacy = deepcopy(f.profile); legacy["schema"]="DMKN_V5_AGGREGATE_PRODUCER_PROFILE_V2"
        with self.assertRaises(ValueError): f.owner(legacy)
        req = deepcopy(f.request); req["schema"]="DMKN_V5_AGGREGATE_PRODUCER_REQUEST_V1"
        with self.assertRaises(ValueError): owner._request(req)

    def test_new_capsule_parent_and_output_metadata_caps(self):
        f = Fixture("metadata",1,1); owner=f.owner()
        for field,limit in (("capsule",96*P.MIB),("parent",P.MIB),("artifact",P.MIB//2)):
            req=deepcopy(f.request)
            if field=="parent": req["session"]["parents"][0]["bytes"]=limit+1
            elif field=="artifact": req["budget"]["stages"]["segment"]["output_bytes"]=limit+1
            else: req["session"][field]["bytes"]=limit+1
            with self.subTest(field=field), self.assertRaisesRegex(ValueError,"INTEGER_LIMIT"):
                owner._request(req)

    def test_retained_checkpoint_cap_and_large_index(self):
        f=Fixture("checkpoint",256,0); owner=f.owner()
        path=f.path/"segment255.checkpoint"
        row={"key":"segment:255","file":saved(path,checkpoint("segment:255",f.session["capsule_binding"]))}
        owner._checkpoint(row,f.session)
        too_big=f.path/"oversize.checkpoint"
        large={"key":"segment:255","file":saved(too_big,checkpoint("segment:255",f.session["capsule_binding"],A.ARTIFACT_LIMIT+1))}
        with self.assertRaisesRegex(ValueError,"INTEGER_LIMIT"): owner._checkpoint(large,f.session)
        wrong=deepcopy(row); wrong["key"]="segment:254"
        with self.assertRaises(ValueError): owner._checkpoint(wrong,f.session)

    def test_fixed_input_remainder_is_enforced_before_checkpoints(self):
        f=Fixture("fixed"); owner=f.owner()
        # Metadata-only negative: no 20 MiB allocation or host call. The extra
        # fake pin stands in for a large adopted snapshot record inventory.
        def snapshot(s,e,inputs):
            inputs[str(f.path/"oversized-fixed.fake")]={"path":str(f.path/"oversized-fixed.fake"),
                "bytes":20*P.MIB+1,"sha256":"09"*32}
        owner._snapshot=snapshot
        with self.assertRaisesRegex(ValueError,"FIXED_SESSION_INPUT_ENVELOPE"):
            owner._request(deepcopy(f.request))

    def test_complete_path_quote_charges_manifest_and_admin_space(self):
        f=Fixture("quotes",256,8)
        budget=deepcopy(f.request["budget"])
        cpu={"segment":1200,"lift":250,"join":250,"resolve":600,"finish":300}
        wall={"segment":240,"lift":150,"join":150,"resolve":600,"finish":120}
        for kind in P.KINDS:
            budget["stages"][kind].update(cpu_seconds=cpu[kind],wall_seconds=wall[kind],
                output_bytes=512*1024,stdout_bytes=64*1024,stderr_bytes=64*1024)
        quote=A.AggregateProducer._envelope(f.session,budget,{},A.graph(256,8),[0,0,0,0,0])
        self.assertEqual(quote["selected_worker_cpu_envelope"],440050)
        self.assertEqual(quote["new_output_envelope"],int(776*2.875*P.MIB)+4*P.MIB)
        self.assertEqual(quote["new_entry_envelope"],776*9+4)
        base=sum(f.session[k]["bytes"] for k in ("image","wire","expected","capsule"))
        base+=sum(p["bytes"] for p in f.session["parents"])
        self.assertEqual(quote["maximum_host_read_envelope"],base+257*512*1024+256*1024)
        self.assertTrue(quote["full_path_fits_requested_envelopes"])
        exhausted=A.AggregateProducer._envelope(f.session,budget,{},A.graph(256,8),[500000,0,0,0,0])
        self.assertFalse(exhausted["full_path_fits_requested_envelopes"])

    def test_real_manifest_reservation_dispatch_without_a_native_process(self):
        f=Fixture("dispatch"); owner=f.owner(); before=len(DISPATCHES)
        result=owner.run(deepcopy(f.request))
        self.assertEqual(len(DISPATCHES),before+1)
        self.assertEqual(result["status"],"FAIL")
        self.assertTrue(result["closure_accounting_known"])
        self.assertTrue(result["final_binding_validated"])
        self.assertEqual(result["host_calls_attempted"],1)
        self.assertEqual(result["reported_proof_stage_calls"],0)
        self.assertFalse(result["application_receipt_created"])
        self.assertFalse(result["mathematical_admission"])
        self.assertEqual(DISPATCHES[-1]["reservation"]["output_entries_reserved"],9)


def main():
    global OUTPUT
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True)
    OUTPUT=Path(parser.parse_args().output)
    P.require(OUTPUT.is_absolute() and OUTPUT.resolve()==OUTPUT and not OUTPUT.exists(),"FRESH_CONTROL_OUTPUT")
    OUTPUT.mkdir()
    origins={}
    for name in ("aggregate_small","aggregate_small.producer","production","production.producer"):
        path=Path(sys.modules[name].__file__).resolve()
        P.require(path.is_relative_to(SNAPSHOT_V5),"SELECTED_IMPORT_ORIGIN")
        origins[name]=P.file_pin(path)
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(SmallControls)
    P.require(suite.countTestCases()==TEST_COUNT,"EXACT_CONTROL_COUNT")
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    success=result.wasSuccessful() and result.testsRun==TEST_COUNT and not result.skipped
    report={"schema":"DMKN_SMALL_PRODUCER_CONTROLS_V1","status":"PASS_SYNTHETIC_CONTROLS_ONLY" if success else "FAIL",
        "tests":result.testsRun,"errors":len(result.errors),"failures":len(result.failures),"skipped":len(result.skipped),
        "selected_imports":origins,"inert_dispatches":len(DISPATCHES),"native_calls":0,"proof_calls":0,
        "build_calls":0,"guest_calls":0,"mathematical_admission":False,
        "mocked_boundaries":["installation","supervisor","build_and_image_adoption","snapshot_adoption"],
        "scope":"PYTHON_CHANGED_BOUNDARIES_NOT_NATIVE_MANIFEST_PARSER_OR_REAL_PROOF"}
    saved(OUTPUT/"CONTROL-RESULT.json",P.encoded(report))
    saved(OUTPUT/"DISPATCHES.json",P.encoded(DISPATCHES))
    return 0 if success else 1


if __name__=="__main__":
    raise SystemExit(main())
