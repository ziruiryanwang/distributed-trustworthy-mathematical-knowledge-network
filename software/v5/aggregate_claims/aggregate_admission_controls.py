"""UNRUN synthetic owner/membership controls; ZERO real receipt verification.

Tests deliberately construct exact-class fake owners/registries, mock base
installation checks, and use an in-memory fake supervisor for receive plumbing.
Valid-looking headers/journals and fabricated stdout are not proofs. No host,
guest, kernel, subprocess, network, file write or ordinary-source worker runs.
"""
from pathlib import Path
import sys
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from admission.verifier import ReceiptVerifier, VerifiedModule
from modules import codec as C
from aggregate_claims import bindings as B
from aggregate_claims import aggregate_admission as A

FAKE_IMAGE = "07"*32


def fixture():
    specs = [{"schema":C.SPEC_SCHEMA,"foundation":B.FOUNDATION,"policy":B.POLICY,
        "groups":[{"kind":"ordinary","declarations":[{"kind":"theorem",
            "name":[["s",name]],"universes":0,"type":["sort",["zero"]],
            "value_hash":None,"meta":{}}]}]} for name in ("left","right")]
    pairs = []
    for spec in specs:
        summary = C.summarize(spec)
        exact = (b"DMKNM002"+(2).to_bytes(4,"little")+bytes.fromhex(B.RELATION_IMAGE)
            +bytes.fromhex(B.FOUNDATION+B.POLICY+C.summary_id(summary)+summary["group_root"])
            +summary["group_count"].to_bytes(4,"little")+(0).to_bytes(8,"little"))
        pairs.append((exact,spec))
    pairs.sort(key=lambda pair:pair[0]); journals = [pair[0] for pair in pairs]
    header = (B.MAGIC+B.VERSION.to_bytes(4,"little")+bytes.fromhex(FAKE_IMAGE+B.RELATION_IMAGE
        +B.FOUNDATION+B.POLICY)+B.commitment(journals)+len(journals).to_bytes(4,"little")
        +(0).to_bytes(8,"little")+(1).to_bytes(8,"little"))
    return header,pairs,[B.opening(journals,index) for index in range(len(journals))]


def fake_owner():
    """TEST ONLY: fabricate a registry; NEVER call this mathematical admission."""
    owner = object.__new__(A.AggregateReceiptVerifier)
    owner._aggregate_initialized = True
    owner._members,owner._member_cache,owner._handles = {},{},{}
    owner._member_used,owner._used,owner._output_reserved = [0,0],[0,0,0],[0,0]
    owner._member_caps,owner._caps = (4096,4096,64*A.MIB),(8,64*A.MIB,240)
    owner._output_caps = 128*A.MIB,1024
    owner._controller_started,owner._controller_cpu_cap = time.process_time(),60
    owner._closed = owner._busy = False
    owner._deadline = time.monotonic()+300
    owner._image = owner._adopted_aggregate_image = FAKE_IMAGE
    owner._foundation,owner._policy = B.FOUNDATION,B.POLICY
    owner._profile_id = owner._origin_profile = "08"*32
    owner._check_install = lambda:owner._active() # Deliberately fake source/runtime check.
    owner._required_origins = {name:Path(sys.modules[name].__file__).resolve() for name in (
        "aggregate_claims.aggregate_admission","aggregate_claims","aggregate_claims.admission_binding",
        "aggregate_claims.bindings","admission","admission.verifier","admission.bindings",
        "modules","modules.codec")}
    header,pairs,openings = fixture()
    batch = A.VerifiedAggregate()
    owner._handles[batch] = header,"09"*32,len(b"NOT-A-RECEIPT")
    return owner,batch,header,pairs,openings


def mocked_receipt_owner(mode="ok"):
    """TEST ONLY in-memory call plumbing, with NO actual verifier or files."""
    owner,batch,header,_,_ = fake_owner()
    owner._deadline = 10000
    owner._install = ROOT/"TEST-ONLY-NONEXISTENT-INSTALL"
    owner._manifest = owner._install/"manifest.json"
    owner._executable = owner._install/"NO-SUCH-VERIFIER.exe"
    owner._pins = {}
    owner._job = object() # Only forwarded to the deliberately fake supervisor.
    output = ROOT/"TEST-ONLY-NONEXISTENT-OUTPUT"
    receipt = b"NOT-A-RECEIPT"
    clock,checks,censuses = [100.0],[0],[]

    class FakeSupervisor:
        def __init__(self): self.files,self.calls,self.saves = {},[],[]
        def limits_checked(self,limits): return dict(limits)
        def absolute(self,path,**kwargs): return Path(path)
        def overlap(self,left,right): return False
        def write(self,path,raw):
            assert path not in self.files
            self.files[path] = raw
        def save_new(self,path,value):
            self.saves.append(path.name); self.write(path,C.canonical(value))
            if mode == "final_deadline" and path.name == "binding.json": clock[0] = 161.0
        def bounded_read(self,path,cap):
            raw = self.files[path]
            assert len(raw) <= cap
            return raw
        def supervise(self,argv,cwd,prefix,limits,job,*,started):
            self.calls.append((list(argv),cwd,prefix,dict(limits),job,started))
            statement = list(header)
            if mode == "wrong_statement": statement[-1] ^= 1
            self.write(prefix/"stdout.txt",C.canonical({
                "schema":"DMKN_AGGREGATE_VERIFY_RESULT_V1",
                "status":"VERIFIED_RESOLVED_AGGREGATE_RECEIPT",
                "aggregate_image":FAKE_IMAGE,"header":statement,
                "receipt_sha256":A._sha(receipt),"receipt_bytes":len(receipt)}))
            if mode == "changed_receipt": self.files[output/"receipt.bin"] = b"ALTERED"
            if mode == "changed_header": self.files[output/"header.bin"] = b"\0"*B.HEADER_BYTES
            return {"status":"COMMAND_EXITED_ZERO_AND_CLOSED","child_exit_code":0,
                "direct_child_reaped":True,"job_closed":True,"cleanup_errors":[],
                "termination_requested":False,"wall_seconds_through_cleanup":4.0,
                "final_job":{"active_processes":1 if mode == "unclean" else 0,
                    "terminated_processes":0,"cpu_seconds":1.0}}

    supervisor = FakeSupervisor()
    owner._supervisor,owner._write = supervisor,supervisor.write
    def check_install():
        checks[0] += 1
        if checks[0] == 1: clock[0] = 103.0 # Deliberate preflight cost; wall budget remains60.
        if mode == "final_pins" and checks[0] == 3:
            raise C.StructureError("TEST_ONLY_FINAL_RECEIVE_PIN_CHANGE")
        owner._active()
    owner._check_install = check_install
    def census(directory,byte_cap,entry_cap):
        assert directory == output
        censuses.append((byte_cap,entry_cap))
        C.require(len(supervisor.files) <= entry_cap
            and sum(map(len,supervisor.files.values())) <= byte_cap,"TEST_ONLY_CENSUS")
    owner._census = census
    return owner,batch,header,receipt,output,supervisor,clock,checks,censuses


class AggregateOwnerControls(unittest.TestCase):
    def test_distinct_classes_and_all_statement_methods_override(self):
        self.assertFalse(issubclass(A.VerifiedAggregate,VerifiedModule))
        self.assertFalse(issubclass(A.VerifiedAggregateMember,VerifiedModule))
        for name in ("receive","describe","open_group","report","close"):
            self.assertIn(name,A.AggregateReceiptVerifier.__dict__)
        owner,batch,*_ = fake_owner()
        fact = owner.describe(batch)
        self.assertIn("header",fact); self.assertNotIn("module",fact)

    def test_base_constructor_virtual_liveness_hook_is_initialized_first(self):
        # Pure mocked constructor control: no files, loaded supervisor or process.
        root = Path(A.__file__).resolve().parents[1]
        names = ("aggregate_claims/aggregate_admission.py","aggregate_claims/__init__.py",
            "aggregate_claims/admission_binding.py","aggregate_claims/bindings.py",
            "admission/__init__.py","admission/verifier.py","admission/bindings.py",
            "modules/__init__.py","modules/codec.py")
        executable = root/"NO-SUCH-TEST-ONLY-EXECUTABLE.exe"
        pins = {path:{"sha256":"10"*32,"bytes":1} for path in [executable,*[root/name for name in names]]}
        observed = []
        def base(instance,**kwargs):
            instance._closed = instance._busy = False
            instance._deadline = time.monotonic()+60
            instance._handles,instance._used,instance._caps = {},[0,0,0],(1,1024,30)
            instance._image,instance._foundation,instance._policy = kwargs["image_id"],kwargs["foundation"],kwargs["policy"]
            instance._pins,instance._executable = pins,executable
            observed.append(instance._aggregate_initialized)
            instance._check_install()
        with patch.object(ReceiptVerifier,"__init__",base), \
             patch.object(ReceiptVerifier,"_check_install",lambda instance:instance._active()):
            owner = A.AggregateReceiptVerifier(supervisor_manifest="TEST-ONLY",supervisor_manifest_sha256="11"*32,
                executable=str(executable),runtime_pins={},aggregate_image=FAKE_IMAGE,operations=1,
                submitted_bytes=1024,reserved_cpu_seconds=30,wall_seconds=60)
        self.assertEqual(observed,[False]); self.assertTrue(owner._aggregate_initialized)
        self.assertEqual(owner._origin_profile,owner._profile_id)
        self.assertEqual(owner.report()["live_aggregates"],0)

    def test_member_selection_requires_same_owner_registry_not_copied_facts(self):
        owner,batch,_,pairs,openings = fake_owner()
        other,other_batch,*_ = fake_owner()
        for bad in (other_batch,A.VerifiedAggregate(),owner.describe(batch),VerifiedModule()):
            with self.assertRaises(C.StructureError): owner.select_member(bad,pairs[0][0],0,openings[0])
        member = owner.select_member(batch,pairs[0][0],0,openings[0])
        with self.assertRaises(C.StructureError): other.describe_member(member)

    def test_membership_exactness_no_false_handle_on_wrong_path_index_or_journal(self):
        owner,batch,_,pairs,openings = fake_owner()
        for exact,index,path in ((pairs[0][0],1,openings[0]),
            (pairs[0][0],0,[b"\0"*32]),(pairs[1][0],0,openings[0]),
            (pairs[0][0],True,openings[0]),(pairs[0][0],0,[])):
            with self.assertRaises(C.StructureError): owner.select_member(batch,exact,index,path)
        self.assertEqual(owner._members,{})
        self.assertEqual(len(owner._handles),1)

    def test_duplicate_member_selection_charges_before_cache_and_stores_once(self):
        owner,batch,_,pairs,openings = fake_owner()
        first = owner.select_member(batch,pairs[0][0],0,openings[0])
        second = owner.select_member(batch,pairs[0][0],0,openings[0])
        self.assertIs(first,second)
        self.assertEqual(owner.report()["live_members"],1)
        self.assertEqual(owner._member_used,[2,2*(184+32*len(openings[0]))])

    def test_member_byte_refusal_has_charge_but_no_partial_handle(self):
        owner,batch,_,pairs,openings = fake_owner()
        owner._member_caps = 4096,4096,1
        with self.assertRaisesRegex(C.StructureError,"MEMBER_BYTE_ALLOWANCE"):
            owner.select_member(batch,pairs[0][0],0,openings[0])
        self.assertEqual(owner._members,{})
        self.assertEqual(owner._member_used,[1,216])

    def test_member_call_and_storage_caps_do_not_create_handles(self):
        owner,batch,_,pairs,openings = fake_owner()
        owner._member_caps = 2,1,64*A.MIB
        member = owner.select_member(batch,pairs[0][0],0,openings[0])
        with self.assertRaisesRegex(C.StructureError,"MEMBER_STORAGE"):
            owner.select_member(batch,pairs[1][0],1,openings[1])
        with self.assertRaisesRegex(C.StructureError,"MEMBER_CALL_ALLOWANCE"):
            owner.describe_member(member)
        self.assertEqual(len(owner._members),1)

    def test_returned_facts_and_group_are_copies_not_mutable_authority(self):
        owner,batch,_,pairs,openings = fake_owner()
        member = owner.select_member(batch,pairs[0][0],0,openings[0])
        facts = owner.describe_member(member); facts["summary"]["foundation"] = "00"*32
        facts["siblings"][0] = b"\0"*32
        group = owner.open_group(member,C.group_opening(pairs[0][1],0))
        group["declarations"][0]["name"] = [["s","changed"]]
        self.assertEqual(owner.describe_member(member)["summary"]["foundation"],B.FOUNDATION)
        self.assertNotEqual(owner.open_group(member,C.group_opening(pairs[0][1],0)),group)

    def test_group_opening_must_match_selected_exact_member(self):
        owner,batch,_,pairs,openings = fake_owner()
        member = owner.select_member(batch,pairs[0][0],0,openings[0])
        with self.assertRaises(C.StructureError): owner.open_group(member,C.group_opening(pairs[1][1],0))
        with self.assertRaises(C.StructureError): owner.open_group(batch,C.group_opening(pairs[0][1],0))

    def test_every_handle_use_rechecks_install_and_failed_pin_check_revokes(self):
        owner,batch,_,pairs,openings = fake_owner()
        member = owner.select_member(batch,pairs[0][0],0,openings[0])
        def changed(): raise C.StructureError("TEST_ONLY_PIN_CHANGED")
        owner._check_install = changed
        with self.assertRaisesRegex(C.StructureError,"TEST_ONLY_PIN_CHANGED"): owner.describe_member(member)
        self.assertTrue(owner._closed); self.assertEqual(owner._handles,{})
        self.assertEqual(owner._members,{})
        owner._check_install = lambda:owner._active()
        with self.assertRaises(C.StructureError): owner.describe_aggregate(batch)

    def test_origin_close_expiry_and_profile_change_revoke_members(self):
        for change in (lambda owner:owner.close(),
                       lambda owner:setattr(owner,"_deadline",time.monotonic()-1),
                       lambda owner:setattr(owner,"_profile_id","ff"*32)):
            owner,batch,_,pairs,openings = fake_owner()
            member = owner.select_member(batch,pairs[0][0],0,openings[0])
            change(owner)
            with self.assertRaises(C.StructureError): owner.describe_member(member)
            self.assertTrue(owner._closed); self.assertEqual(owner._members,{})

    def test_wrong_loaded_origin_revokes_even_if_matching_files_exist_elsewhere(self):
        owner,batch,*_ = fake_owner()
        owner._required_origins["admission.verifier"] = ROOT/"another-installation"/"verifier.py"
        with self.assertRaisesRegex(C.StructureError,"LOADED_SOURCE_ORIGIN"):
            owner.describe_aggregate(batch)
        self.assertTrue(owner._closed); self.assertEqual(owner._handles,{})

    def test_imported_symbol_replacement_is_not_accepted_from_matching_path(self):
        owner,batch,*_ = fake_owner()
        # Different function under the same module pathname is not this imported
        # bind_output. Pure identity control, not arbitrary monkeypatch security.
        with patch.object(sys.modules["aggregate_claims.admission_binding"],"bind_output",lambda *args:None):
            with self.assertRaisesRegex(C.StructureError,"IMPORTED_SYMBOL_ORIGIN"):
                owner.describe_aggregate(batch)
        self.assertTrue(owner._closed)

    def test_final_member_liveness_failure_prevents_promotion(self):
        owner,batch,_,pairs,openings = fake_owner(); calls = 0
        def final_fail():
            nonlocal calls
            calls += 1
            if calls == 2: raise C.StructureError("TEST_ONLY_FINAL_PINS_CHANGED")
            owner._active()
        owner._check_install = final_fail
        with self.assertRaisesRegex(C.StructureError,"TEST_ONLY_FINAL_PINS_CHANGED"):
            owner.select_member(batch,pairs[0][0],0,openings[0])
        self.assertEqual(owner._members,{})

    def test_entered_receipt_header_refusal_revokes_and_preserves_reservations(self):
        owner,batch,_,pairs,openings = fake_owner()
        member = owner.select_member(batch,pairs[0][0],0,openings[0])
        # There is deliberately no _supervisor/executable. Header rejects before
        # any worker/path access; no successful receipt admission is simulated.
        with self.assertRaises(C.StructureError):
            owner.receive(b"NOT-A-RECEIPT",b"\0"*B.HEADER_BYTES,"NOT-A-REAL-OUTPUT")
        self.assertEqual(owner._used,[1,len(b"NOT-A-RECEIPT"),30])
        self.assertEqual(owner._output_reserved,[len(b"NOT-A-RECEIPT")+B.HEADER_BYTES+A.MIB,32])
        self.assertTrue(owner._closed); self.assertFalse(owner._busy)
        self.assertEqual(owner._handles,{}); self.assertEqual(owner._members,{})

    def test_mocked_receive_exact_command_statement_report_and_finalization(self):
        # This fabricates verifier output and intercepts ALL writes/worker calls.
        # Only the Python adapter is exercised; the resulting handle is fake.
        owner,batch,header,receipt,output,supervisor,clock,checks,censuses = mocked_receipt_owner()
        with patch.object(A.time,"monotonic",lambda:clock[0]), \
             patch.object(Path,"mkdir",return_value=None) as mkdir:
            handle = owner.receive(receipt,header,output)
        mkdir.assert_called_once_with()
        self.assertEqual(len(supervisor.calls),1)
        argv,cwd,prefix,limits,job,started = supervisor.calls[0]
        self.assertEqual(argv,[str(owner._executable),"verify",FAKE_IMAGE,
            str(output/"receipt.bin"),str(output/"header.bin")])
        self.assertEqual((cwd,prefix,job,started),(owner._install,output/"command",owner._job,100.0))
        self.assertEqual(limits["wall_seconds"],60) # Not57: no double preflight subtraction.
        self.assertEqual(supervisor.files[output/"receipt.bin"],receipt)
        self.assertEqual(supervisor.files[output/"header.bin"],header)
        self.assertEqual(supervisor.saves,["request.json","process.json","binding.json"])
        self.assertEqual(checks,[3]); self.assertEqual(len(censuses),2)
        self.assertIs(type(handle),A.VerifiedAggregate)
        self.assertEqual(owner._handles[handle],(header,A._sha(receipt),len(receipt)))
        self.assertIn(batch,owner._handles)
        self.assertFalse(owner._closed); self.assertFalse(owner._busy)
        self.assertEqual(owner._used,[1,len(receipt),30])

    def test_mocked_receive_failures_never_promote_and_revoke_entered_authority(self):
        cases = (("wrong_statement","EXACT_STATEMENT"),("unclean","REFUSED_OR_UNCLOSED"),
            ("changed_receipt","EXACT_INPUT_CHANGED"),("changed_header","EXACT_INPUT_CHANGED"),
            ("final_pins","FINAL_RECEIVE_PIN_CHANGE"),("final_deadline","AGGREGATE_TOTAL_WALL"))
        for mode,reason in cases:
            with self.subTest(mode=mode):
                owner,_,header,receipt,output,supervisor,clock,_,_ = mocked_receipt_owner(mode)
                with patch.object(A.time,"monotonic",lambda:clock[0]), \
                     patch.object(Path,"mkdir",return_value=None):
                    with self.assertRaisesRegex(C.StructureError,reason):
                        owner.receive(receipt,header,output)
                self.assertEqual(len(supervisor.calls),1)
                self.assertTrue(owner._closed); self.assertFalse(owner._busy)
                self.assertEqual(owner._handles,{}); self.assertEqual(owner._members,{})
                self.assertEqual(owner._used,[1,len(receipt),30])
                self.assertEqual(owner._output_reserved,[len(receipt)+B.HEADER_BYTES+A.MIB,32])
                self.assertIn("process.json",supervisor.saves)
                if mode in ("final_pins","final_deadline"):
                    self.assertIn("binding.json",supervisor.saves)


if __name__ == "__main__":
    unittest.main(verbosity=2)
