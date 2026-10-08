"""Transport-only tests; synthetic CBOR is deliberately not accepted mathematics.

Root executes after review. Tests import no checker/codec/native experiment.
"""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "py"))
import peer_wire as W
import peer_service as P


def wire_json(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def cid(tag, schema, raw):
    digest = hashlib.sha256(b"DTMKN-CAS\0" + tag.to_bytes(2, "big") + schema.to_bytes(2, "big") +
                            len(raw).to_bytes(8, "big") + raw).digest()
    return [1, tag, schema, {"$bytes": list(digest)}]


def small_uint(number):
    if number < 24:
        return bytes([number])
    if number < 256:
        return b"\x18" + bytes([number])
    return b"\x19" + number.to_bytes(2, "big")


def own_filename(identifier):
    return (b"\x84\x01" + small_uint(identifier[1]) + small_uint(identifier[2]) +
            b"\x58\x20" + bytes(identifier[3]["$bytes"])).hex() + ".cbor"


class PeerWireTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = os.environ.get("DTMKN_TEST_ROOT")
        W.require(type(parent) is str and parent and Path(parent).is_absolute(), "TEST_ROOT_REQUIRED")
        cls.test_parent = W.safe_path(parent, directory=True)

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="peer-" + self._testMethodName[5:29] + "-",
                                         dir=self.test_parent))
        (self.root / "test-case.json").write_bytes(wire_json({"test": self._testMethodName,
                                                           "retained": True}))
        self.payloads = [b"\x80", b"\x81\x00"]
        self.foundation = cid(1, 2, self.payloads[0])
        self.replay = cid(0x15, 3, self.payloads[1])
        self.descriptor = cid(0x8111, 3, b"\x80")
        self.manifest = {"foundation": self.foundation, "root": self.replay,
                         "objects": [self.foundation, self.replay], "inventories": []}
        self.manifest_raw = wire_json(self.manifest)
        self.bundle = self.framed(self.manifest_raw, self.payloads)
        self.formal = {"replay": self.replay, "native_ref": [], "semantic_target": [],
                       "universe_arity": 0, "type_dag": [], "descriptor": [],
                       "descriptor_id": self.descriptor, "symbols": [], "trace": []}
        self.entry = {"descriptor_id": self.descriptor, "root": self.replay,
                      "manifest_sha256": hashlib.sha256(self.manifest_raw).hexdigest(),
                      "bundle_sha256": hashlib.sha256(self.bundle).hexdigest(), "bundle_bytes": len(self.bundle),
                      "formal_metadata": self.formal}
        self.catalog = {"schema": 1, "foundation": self.foundation, "entries": [self.entry]}
        self.package = self.root / "package"
        self.package.mkdir()
        (self.package / "objects").mkdir()
        (self.package / "manifest.json").write_bytes(self.manifest_raw)
        for identifier, raw in zip(self.manifest["objects"], self.payloads):
            (self.package / "objects" / own_filename(identifier)).write_bytes(raw)
        self.serial = 0

    @staticmethod
    def framed(manifest, payloads):
        return (b"DTMKN-PEER-BUNDLE-1\n" + len(manifest).to_bytes(4, "big") + manifest +
                b"".join(len(raw).to_bytes(8, "big") + raw for raw in payloads))

    def destination(self):
        self.serial += 1
        return self.root / ("incoming-" + str(self.serial))

    def expect(self, code, function, *args):
        with self.assertRaises(W.WireError) as captured:
            function(*args)
        self.assertEqual(captured.exception.code, code)

    def selected(self, bundle):
        return dict(self.entry, bundle_sha256=hashlib.sha256(bundle).hexdigest(), bundle_bytes=len(bundle))

    def receive(self, raw, entry=None):
        return W.receive_bundle(io.BytesIO(raw), self.entry if entry is None else entry,
                                self.foundation, self.destination())

    def test_independent_bundle_and_filename(self):
        self.assertEqual(W.make_bundle(self.package), self.bundle)
        for identifier in self.manifest["objects"]:
            self.assertEqual(W.object_name(identifier), own_filename(identifier))

    def test_receive_is_not_acceptance_and_preserves_bytes(self):
        result = self.receive(self.bundle)
        self.assertIs(result["mathematicalAcceptance"], False)
        self.assertEqual(result["native_stages"], 0)
        self.assertEqual(result["basis"], "TRANSPORT_AND_OBJECT_IDENTITIES_ONLY")
        installed = Path(result["package"]["path"])
        self.assertEqual((installed / "manifest.json").read_bytes(), self.manifest_raw)
        self.assertEqual(W.make_bundle(installed), self.bundle)
        self.assertFalse((installed / "accepted.json").exists())

    def test_catalog_exact_schema(self):
        self.assertEqual(W.parse_catalog(wire_json(self.catalog), self.foundation), self.catalog)
        for field in ("source", "path", "context", "receipt", "accepted"):
            bad = copy.deepcopy(self.catalog)
            bad["entries"][0][field] = True
            self.expect("PEER_SCHEMA_REFUSED", W.parse_catalog, wire_json(bad), self.foundation)
        self.expect("PEER_SCHEMA_REFUSED", W.parse_catalog, b'{"schema":1,"schema":1}', self.foundation)

    def test_malformed_id_and_noninteger_json(self):
        bad = copy.deepcopy(self.catalog)
        bad["entries"][0]["root"][3]["$bytes"][0] = True
        self.expect("PEER_SCHEMA_REFUSED", W.parse_catalog, wire_json(bad), self.foundation)
        for raw in (b'{"schema":1.0}', b'{"schema":NaN}', b"[" * 65 + b"0" + b"]" * 65):
            self.expect("PEER_SCHEMA_REFUSED", W.parse_catalog, raw, self.foundation)

    def test_foundation_mismatch_before_destination(self):
        other = cid(1, 2, b"\x81\x00")
        target = self.destination()
        self.expect("FOUNDATION_MISMATCH", W.receive_bundle, io.BytesIO(self.bundle), self.entry, other, target)
        self.assertFalse(target.exists())

    def test_declared_bundle_over_limit_before_read(self):
        class NoRead:
            def read(self, _):
                raise AssertionError("oversized advertised bundle must refuse without reading")
        self.expect("TRANSFER_LIMIT", W.receive_bundle, NoRead(), dict(self.entry, bundle_bytes=W.BUNDLE_MAX + 1),
                    self.foundation, self.destination())

    def test_manifest_and_object_frame_limits(self):
        over_manifest = W.MAGIC + (W.MANIFEST_MAX + 1).to_bytes(4, "big")
        self.expect("TRANSFER_LIMIT", self.receive, over_manifest, self.selected(over_manifest))
        over_object = W.MAGIC + len(self.manifest_raw).to_bytes(4, "big") + self.manifest_raw + (W.OBJECT_MAX + 1).to_bytes(8, "big")
        self.expect("TRANSFER_LIMIT", self.receive, over_object, self.selected(over_object))

    def test_truncation_and_trailing_frame(self):
        self.expect("BUNDLE_FRAMING_REFUSED", self.receive, self.bundle[:-1])
        extra = self.bundle + b"X"
        self.expect("BUNDLE_FRAMING_REFUSED", self.receive, extra, self.selected(extra))
        self.expect("BUNDLE_FRAMING_REFUSED", self.receive, self.bundle + b"X")

    def test_transport_digest_precedes_object_error(self):
        altered = self.bundle[:-1] + b"\x01"
        self.expect("BUNDLE_DIGEST_MISMATCH", self.receive, altered)

    def test_canonical_id_is_independent_of_transport_digest(self):
        altered = self.bundle[:-1] + b"\x01"
        self.expect("OBJECT_ID_MISMATCH", self.receive, altered, self.selected(altered))

    def test_noncanonical_cbor_rejected(self):
        altered = self.framed(self.manifest_raw, [self.payloads[0], b"\x18\x00"])
        self.expect("OBJECT_ENCODING_REFUSED", self.receive, altered, self.selected(altered))
        for payload in (b"\xff", b"\xa0", b"\x80\x00", b"\x58\x01x"):
            self.expect("OBJECT_ENCODING_REFUSED", W.canonical_payload, payload)

    def test_sender_filenames_never_accepted(self):
        bad = dict(self.manifest, path="../../outside")
        bundle = self.framed(wire_json(bad), self.payloads)
        self.expect("PEER_SCHEMA_REFUSED", self.receive, bundle, self.selected(bundle))
        bad = copy.deepcopy(self.manifest)
        bad["objects"][0] = "../../outside"
        bundle = self.framed(wire_json(bad), self.payloads)
        self.expect("PEER_SCHEMA_REFUSED", self.receive, bundle, self.selected(bundle))
        self.assertFalse((self.root / "outside").exists())

    def test_no_overwrite_and_duplicate_manifest_members(self):
        target = self.destination()
        target.mkdir()
        self.expect("LOCAL_PATH_REFUSED", W.receive_bundle, io.BytesIO(self.bundle), self.entry, self.foundation, target)
        bad = copy.deepcopy(self.manifest)
        bad["objects"].append(self.foundation)
        altered = self.framed(wire_json(bad), self.payloads + self.payloads[:1])
        self.expect("BUNDLE_FRAMING_REFUSED", self.receive, altered, self.selected(altered))

    def test_manifest_digest_is_checked(self):
        bad = dict(self.entry, manifest_sha256="0" * 64)
        self.expect("MANIFEST_DIGEST_MISMATCH", self.receive, self.bundle, bad)

    def test_metadata_coherence_is_not_semantic_check(self):
        bad = copy.deepcopy(self.entry)
        bad["formal_metadata"]["descriptor_id"] = cid(0x8111, 3, b"\x81\x01")
        self.expect("ADVERTISED_METADATA_MISMATCH", self.receive, self.bundle, bad)
        # Internally coherent false type metadata must still be rederived by root.
        result = self.receive(self.bundle)
        self.assertEqual(result["advertised_metadata"]["type_dag"], [])
        self.assertIs(result["mathematicalAcceptance"], False)

    def offer(self):
        return {"package": {"path": str(self.package), "manifest_sha256": self.entry["manifest_sha256"]},
                "descriptor_id": self.descriptor, "formal_metadata": self.formal}

    def test_view_requires_manifest_pin_and_completion(self):
        bad = self.offer()
        bad["package"]["manifest_sha256"] = "0" * 64
        target = self.root / "bad-view"
        self.expect("MANIFEST_DIGEST_MISMATCH", W.build_view, target, self.foundation, [bad])
        self.assertFalse((target / "complete.json").exists())
        view = self.root / "view"
        self.assertEqual(W.build_view(view, self.foundation, [self.offer()]), self.catalog)
        loaded = W.load_view(view)
        self.assertEqual(loaded["catalog"], self.catalog)
        (view / "bundles" / (self.entry["bundle_sha256"] + ".bundle")).write_bytes(self.bundle[:-1] + b"\x01")
        self.expect("BUNDLE_DIGEST_MISMATCH", W.load_view, view)

    def test_real_loopback_discovery_acquisition_and_private_route(self):
        view, ready = self.root / "http-view", self.root / "ready.json"
        W.build_view(view, self.foundation, [self.offer()])
        stop, outcomes, failures = threading.Event(), [], []

        def worker():
            try:
                outcomes.append(P.serve(view, 0, ready, stop=stop, session_seconds=15, max_requests=8))
            except BaseException as error:
                failures.append(error)

        thread = threading.Thread(target=worker)
        thread.start()
        try:
            deadline = time.monotonic() + 5
            while not ready.exists() and thread.is_alive() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(ready.exists(), str(failures))
            info = json.loads(ready.read_bytes())
            port = info["port"]
            self.assertEqual(info["host"], "127.0.0.1")
            found = P.fetch_catalog(port, self.foundation)
            self.assertEqual(found["catalog"], self.catalog)
            received = P.acquire(port, found["catalog"]["entries"][0], self.foundation, self.destination())
            self.assertIs(received["mathematicalAcceptance"], False)
            self.expect("PEER_NOT_FOUND", P._get, port, "/control.sqlite3", 4096, b"application/json", lambda *_: None)
            self.expect("PEER_NOT_FOUND", P._get, port, "/v1/bundle/" + "0" * 64, W.BUNDLE_MAX,
                        b"application/octet-stream", lambda *_: None)
        finally:
            stop.set()
            thread.join(6)
        self.assertFalse(thread.is_alive())
        self.assertFalse(failures, str(failures))
        self.assertEqual(outcomes[0]["connections"], 4)
        self.assertEqual(outcomes[0]["native_stages"], 0)
        self.assertIs(outcomes[0]["checker_loaded"], False)

    def test_http_parser_rejects_oversize_redirect_and_ambiguous_length(self):
        bodies = [
            (b"HTTP/1.1 200 OK\r\nContent-Length: 999999\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n", "TRANSFER_LIMIT"),
            (b"HTTP/1.1 302 Found\r\nLocation: http://example.invalid/\r\nContent-Length: 0\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n", "HTTP_PROFILE_REFUSED"),
            (b"HTTP/1.1 200 OK\r\nContent-Length: 1\r\nContent-Length: 2\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n", "HTTP_PROFILE_REFUSED"),
            (b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\nTransfer-Encoding: chunked\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n", "HTTP_PROFILE_REFUSED"),
        ]
        for raw, code in bodies:
            with self.subTest(code=code, raw=raw[:60]):
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind(("127.0.0.1", 0))
                server.listen(1)
                server.settimeout(5)

                def reply():
                    try:
                        connection, _ = server.accept()
                        with connection:
                            connection.settimeout(5)
                            request = b""
                            while b"\r\n\r\n" not in request:
                                chunk = connection.recv(4096)
                                if not chunk:
                                    return
                                request += chunk
                            connection.sendall(raw)
                    finally:
                        server.close()

                thread = threading.Thread(target=reply)
                thread.start()
                try:
                    self.expect(code, P.fetch_catalog, server.getsockname()[1], self.foundation)
                finally:
                    thread.join(6)
                self.assertFalse(thread.is_alive())


if __name__ == "__main__":
    unittest.main()
