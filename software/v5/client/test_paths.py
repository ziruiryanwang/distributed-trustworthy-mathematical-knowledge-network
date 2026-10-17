"""Pure portable-location path/class controls; never starts Node or a verifier.

Runtime directories here are empty test directories, NOT adopted installations.
These controls exercise constructor policy, not runtime verification or routing.
"""
import argparse
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import sys
import time
import unittest

V5 = Path(__file__).resolve().parents[1]
OVERLAY = V5/"portable_runtime"
if __name__ == "__main__": sys.path[:0] = [str(OVERLAY), str(V5)]
from location import controller as B
from location import controller_services as S
from delta import transport as D
from frontier_network.transport import FrontierLocatedHandoff

EVIDENCE = None
EXPECTED_OVERLAY = OVERLAY


class PortablePathControls(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.root = EVIDENCE/self._testMethodName; self.root.mkdir()
        self.source, self.install, self.work = (self.root/name for name in ("source", "install", "work"))
        for path in (self.source, self.install, self.work): path.mkdir()
        self.pins = {name: "00"*32 for name in B.SOURCE_NAMES}
        self.roles = {name: "11"*32 for name in S.ROLE_NAMES}
        self.adopted = B.AdoptedLocationRuntime(self.source, self.pins,
            installation_root=self.install, workspace_root=self.work)

    def config(self, state=None):
        return {"schema": "DMKN_V5_MAINTAINED_LOCATION_ROLES_V1", "role": "reader",
                "state": str(state or self.work/"state")}

    async def test_one_canonical_location_identity(self):
        self.assertEqual(Path(B.__file__).resolve(), EXPECTED_OVERLAY/"location"/"controller.py")
        self.assertEqual(Path(S.__file__).resolve(), EXPECTED_OVERLAY/"location"/"controller_services.py")
        self.assertIs(D.ServiceLocationProcess, S.ServiceLocationProcess)
        self.assertIs(FrontierLocatedHandoff, D.DeltaLocatedHandoff)

    async def test_adoption_has_immutable_copied_selection_and_v2_map(self):
        self.pins[next(iter(self.pins))] = "22"*32
        self.assertEqual(set(self.adopted.source_pins.values()), {"00"*32})
        with self.assertRaises(TypeError): self.adopted.source_pins["protocol.mjs"] = "33"*32
        with self.assertRaises(FrozenInstanceError): self.adopted.workspace = self.install
        mapping = self.adopted.source_map(self.roles)
        self.assertEqual(mapping["schema"], "DMKN_V5_LOCAL_NODE_SOURCE_MAP_V2")
        self.assertEqual(set(mapping), {"schema", "root", "installation_root", "workspace_root", "files", "manifest_sha256"})
        self.assertEqual(set(mapping["files"]), B.SOURCE_NAMES | S.ROLE_NAMES)
        self.assertEqual(self.adopted.node, self.install/"runtime"/"node"/"node.exe")

    async def test_overlapping_or_noncanonical_roots_refuse(self):
        for work in (self.root, self.source, self.install):
            with self.assertRaisesRegex(ValueError, "IMMUTABLE_ROOT_OVERLAP"):
                B.AdoptedLocationRuntime(self.source, self.pins,
                    installation_root=self.install, workspace_root=work)
        with self.assertRaisesRegex(ValueError, "CANONICAL"):
            B.AdoptedLocationRuntime("relative", self.pins,
                installation_root=self.install, workspace_root=self.work)

    async def test_fresh_state_and_evidence_must_be_disjoint_inside_workspace(self):
        for state, evidence in ((self.install/"state", self.work/"evidence"),
                                (self.work/"state", self.source/"evidence"),
                                (self.work/"same", self.work/"same"),
                                (self.work, self.work/"evidence")):
            with self.assertRaises(ValueError):
                S.ServiceLocationProcess(self.adopted, self.roles, self.config(state), evidence,
                                         deadline=time.monotonic()+10)
        held = S.ServiceLocationProcess(self.adopted, self.roles, self.config(), self.work/"evidence",
                                        deadline=time.monotonic()+10)
        self.assertEqual(held.state, self.work/"state")
        self.assertFalse(held.evidence.exists())
        self.assertIsNone(held.process)
        (self.work/"state").mkdir()
        with self.assertRaisesRegex(ValueError, "FRESH_WORKSPACE_PATH"):
            S.ServiceLocationProcess(self.adopted, self.roles, self.config(), self.work/"evidence2",
                                     deadline=time.monotonic()+10)

    async def test_legacy_bare_launch_refuses_without_runtime(self):
        bare = B.LocationProcess(self.adopted, {}, self.work/"evidence", deadline=time.monotonic()+10)
        with self.assertRaises(ValueError): await bare._start_core()
        self.assertIsNone(bare.process)
        self.assertFalse(bare.evidence.exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--output", required=True)
    EVIDENCE = Path(parser.parse_args().output); EVIDENCE.mkdir(parents=True, exist_ok=False)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PortablePathControls))
    report = {"status": "PASS_PORTABLE_PATH_CONTROLS" if result.wasSuccessful() else "FAIL",
              "tests": result.testsRun, "errors": len(result.errors), "failures": len(result.failures),
              "node_launches": 0, "runtime_adoptions": 0, "mathematical_authority": False}
    with (EVIDENCE/"RESULT.json").open("x", encoding="utf-8") as stream: json.dump(report, stream, sort_keys=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)
