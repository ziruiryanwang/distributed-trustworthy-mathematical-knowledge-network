"""Three retained, native-free socket checks; synthetic bytes are not mathematics.

Run only under the root's bounded supervisor with an explicit DTMKN_TEST_ROOT.
Inherited fixture helpers are reused, but load_tests excludes inherited tests.
"""
import json
from pathlib import Path
import socket
import subprocess
import sys
import threading
import time
import unittest

from test_peer_wire import PeerWireTests, P, W, wire_json


class LocalNetworkSmokeTests(PeerWireTests):
    def start_supplier(self, name, offer):
        folder = self.root / name
        folder.mkdir()
        view, ready = folder / "view", folder / "ready.json"
        self.assertEqual(W.build_view(view, self.foundation, [offer]), self.catalog)
        command = [sys.executable, "-B", "-E", "-s", "-S", str(Path(__file__).resolve()),
                   "--serve-fixture", str(view), str(ready)]
        (folder / "command.json").write_bytes(wire_json(command))
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd=self.root, shell=False,
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        child = {"process": process, "folder": folder, "finished": False}
        self.addCleanup(self.cleanup_supplier, child)
        deadline = time.monotonic() + 5
        while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(ready.exists(), "supplier did not become ready within five seconds")
        info = json.loads(ready.read_bytes())
        self.assertEqual(info["host"], "127.0.0.1")
        child["port"] = info["port"]
        return child

    @staticmethod
    def retain_child(child, stdout, stderr, *, cleanup, forced):
        folder, process = child["folder"], child["process"]
        (folder / "stdout.bin").write_bytes(stdout)
        (folder / "stderr.bin").write_bytes(stderr)
        (folder / "lifecycle.json").write_bytes(wire_json({
            "pid": process.pid, "exit_code": process.returncode,
            "cleanup_path_used": cleanup, "forced_termination": forced}))
        child["finished"] = True

    def cleanup_supplier(self, child):
        if child["finished"]:
            return
        process = child["process"]
        forced = process.poll() is None
        if forced:
            process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            forced = True
            process.kill()
            stdout, stderr = process.communicate(timeout=3)
        self.retain_child(child, stdout, stderr, cleanup=True, forced=forced)

    def finish_supplier(self, child, responses):
        try:
            stdout, stderr = child["process"].communicate(timeout=15)
        except subprocess.TimeoutExpired:
            self.fail("supplier did not exit naturally; cleanup is not a successful stop")
        self.retain_child(child, stdout, stderr, cleanup=False, forced=False)
        self.assertEqual(child["process"].returncode, 0, stderr.decode(errors="replace"))
        self.assertEqual(stderr, b"")
        report = json.loads(stdout)
        (child["folder"] / "report.json").write_bytes(wire_json(report))
        self.assertEqual(report["connections"], 2)
        self.assertEqual(report["responses"], responses)
        self.assertEqual(report["stop_reason"], "SESSION_LIMIT")
        self.assertEqual(report["native_stages"], 0)
        self.assertIs(report["checker_loaded"], False)
        self.assertIs(report["mathematicalAcceptance"], False)
        self.assertEqual(report["bind_host"], "127.0.0.1")
        return report

    def acquire_exact(self, child):
        found = P.fetch_catalog(child["port"], self.foundation)
        self.assertEqual(found["catalog"], self.catalog)
        received = P.acquire(child["port"], found["catalog"]["entries"][0],
                             self.foundation, self.destination())
        self.assertIs(received["mathematicalAcceptance"], False)
        self.assertEqual(received["native_stages"], 0)
        self.assertEqual(received["basis"], "TRANSPORT_AND_OBJECT_IDENTITIES_ONLY")
        package = Path(received["package"]["path"])
        self.assertEqual(W.make_bundle(package), self.bundle)
        self.assertEqual((package / "manifest.json").read_bytes(), self.manifest_raw)
        self.assertFalse((package / "accepted.json").exists())
        return received

    def test_separate_process_supplier_turnover(self):
        first = self.start_supplier("supplier-a", self.offer())
        received = self.acquire_exact(first)
        self.finish_supplier(first, responses=2)
        with self.assertRaises(W.WireError) as unavailable:
            P.fetch_catalog(first["port"], self.foundation)
        # A closed Windows listener can refuse immediately or hit connect timeout.
        # Natural process exit above establishes that our original supplier ended.
        self.assertIn(unavailable.exception.code, ("PEER_UNAVAILABLE", "TRANSFER_TIMEOUT"))
        (first["folder"] / "offline-probe.json").write_bytes(wire_json({
            "code": unavailable.exception.code, "returned_catalog": False,
            "supplier_exit_code": first["process"].returncode}))
        offer = dict(self.offer(), package=received["package"])
        second = self.start_supplier("supplier-b", offer)
        self.acquire_exact(second)
        self.finish_supplier(second, responses=2)
        self.assertIsNotNone(first["process"].poll())

    def test_real_socket_truncated_bundle_is_not_acceptance(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addCleanup(server.close)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server.settimeout(5)
        port = server.getsockname()[1]
        raw = (b"HTTP/1.1 200 OK\r\nContent-Length: " + str(len(self.bundle)).encode() +
               b"\r\nContent-Type: application/octet-stream\r\nConnection: close\r\n\r\n" +
               self.bundle[:-1])
        (self.root / "truncated-response.bin").write_bytes(raw)
        observations, failures = {}, []

        def reply():
            try:
                connection, _ = server.accept()
                with connection:
                    connection.settimeout(5)
                    request = b""
                    while b"\r\n\r\n" not in request:
                        chunk = connection.recv(1024)
                        if not chunk or len(request) + len(chunk) > P.HEADER_MAX:
                            raise AssertionError("client request missing or oversized")
                        request += chunk
                    (self.root / "truncation-request.bin").write_bytes(request)
                    connection.sendall(raw)
                    connection.shutdown(socket.SHUT_WR)
                    observations["client_closed"] = connection.recv(1) == b""
            except BaseException as error:
                failures.append(repr(error))
            finally:
                server.close()

        worker = threading.Thread(target=reply)
        worker.start()
        destination = self.destination()
        try:
            self.expect("BUNDLE_FRAMING_REFUSED", P.acquire, port, self.entry,
                        self.foundation, destination)
        finally:
            worker.join(6)
            (self.root / "truncation-observations.json").write_bytes(wire_json({
                "observations": observations, "failures": failures, "thread_alive": worker.is_alive()}))
        self.assertFalse(worker.is_alive())
        self.assertEqual(failures, [])
        self.assertIs(observations["client_closed"], True)
        self.assertFalse((destination / "accepted.json").exists())

    def test_hostile_host_rejected_then_valid_discovery(self):
        child = self.start_supplier("host-check", self.offer())
        request = b"GET /v1/catalog HTTP/1.1\r\nHost: hostile.invalid\r\nConnection: close\r\n\r\n"
        (self.root / "hostile-request.bin").write_bytes(request)
        with socket.create_connection(("127.0.0.1", child["port"]), timeout=2) as connection:
            connection.settimeout(5)
            connection.sendall(request)
            response = connection.recv(1)
        (self.root / "hostile-response.bin").write_bytes(response)
        self.assertEqual(response, b"")
        self.assertEqual(P.fetch_catalog(child["port"], self.foundation)["catalog"], self.catalog)
        report = self.finish_supplier(child, responses=1)
        self.assertEqual(report["last_error"], "HTTP_PROFILE_REFUSED")


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(LocalNetworkSmokeTests(name) for name in (
        "test_separate_process_supplier_turnover",
        "test_real_socket_truncated_bundle_is_not_acceptance",
        "test_hostile_host_rejected_then_valid_discovery"))


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--serve-fixture":
        print(json.dumps(P.serve(Path(sys.argv[2]), 0, Path(sys.argv[3]),
                                 session_seconds=10, max_requests=2), sort_keys=True))
    else:
        unittest.main()
