"""Changed-boundary controls: real parser, provider dispatch and scratch custody.

StreamReader inputs and bounded writer doubles make write races deterministic.
No sockets, native workers, mathematical admission or existing database is opened.
Root selects execution and exact source/package/evidence pins separately.
"""
from __future__ import annotations

import argparse
import asyncio
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from types import ModuleType
from unittest.mock import patch

START, CPU = time.monotonic(), time.process_time()
ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
SUPPORT = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py"),
    ("portable_evidence", "installation/py/portable_evidence.py"),
    ("ordinary_preview", "authoring/py/ordinary_preview.py"),
    ("portable_preview", "authoring/py/portable_preview.py"),
    ("discovery.formal_features", "support/discovery/formal_features.py"),
    ("discovery.authenticated_index", "support/discovery/authenticated_index.py"),
    ("discovery.summary_wire", "support/discovery/summary_wire.py"),
    ("discovery.pair_access", "support/discovery/pair_access.py"),
    ("discovery.discovery_store", "support/discovery/discovery_store.py"),
    ("custody.module_store", "support/custody/module_store.py"),
    ("transport.http_provider", None),
    ("transport.clients", "support/transport/clients.py"),
    ("transport.ordinary_acquisition", "support/transport/ordinary_acquisition.py"),
)


def need(ok, code):
    if not ok:
        raise AssertionError("CAPACITY_CONTROL_"+code)


def check():
    need(time.monotonic()-START < 40 and time.process_time()-CPU < 15, "ALLOWANCE")


def read(path, expected=None):
    check()
    need(path.is_absolute() and path.is_file() and not path.is_symlink() and
         0 < path.stat().st_size <= 2*MIB, "INPUT")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(len(raw) <= 2*MIB and (expected is None or
         hashlib.sha256(raw).hexdigest() == expected), "PIN")
    return raw


def load(args):
    package = Path(args.package)
    profile_raw = read(package/"PROFILE.json", args.profile_sha256)
    profile = json.loads(profile_raw)
    installation = json.loads(read(package/"installation/INSTALLATION.json",
                                  profile["installation_manifest_sha256"]))
    pins = {}
    for name in ("discovery", "transport", "custody"):
        need(name not in sys.modules, "PRELOADED")
        module = ModuleType(name)
        module.__path__ = []
        sys.modules[name] = module
    modules = {}
    for name, relative in SUPPORT:
        path = Path(args.candidate) if relative is None else package/relative
        pin = ({"sha256": args.candidate_sha256} if relative is None else
               installation["files"][relative.removeprefix("installation/")]
               if relative.startswith("installation/") else profile["files"][relative])
        raw = read(path, pin["sha256"])
        need("bytes" not in pin or len(raw) == pin["bytes"], "SOURCE_SIZE")
        need(name not in sys.modules, "PRELOADED_MODULE")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        exec(compile(raw, str(path), "exec"), module.__dict__)
        if "." in name:
            parent, child = name.rsplit(".", 1)
            setattr(sys.modules[parent], child, module)
        modules[name] = module
        pins[str(path)] = hashlib.sha256(raw).hexdigest()
    return modules, pins


class Writer:
    def __init__(self, *, hold=False):
        self.data = bytearray()
        self.hold = hold
        self.entered, self.release = asyncio.Event(), asyncio.Event()
        self.closed = False

    def write(self, raw):
        need(len(self.data)+len(raw) <= 128*1024, "WRITER_BOUND")
        self.data.extend(raw)

    async def drain(self):
        self.entered.set()
        if self.hold:
            await self.release.wait()

    def close(self):
        self.closed = True

    def body(self):
        if not self.data:
            return None
        header, body = bytes(self.data).split(b"\r\n\r\n", 1)
        need(header.startswith(b"HTTP/1.1 200 OK"), "HTTP_STATUS")
        fields = dict(line.split(b":", 1) for line in header.split(b"\r\n")[1:])
        need(int(fields[b"Content-Length"].strip()) == len(body), "CONTENT_LENGTH")
        return body


def request_reader(F, route, request):
    raw = F.compact(request)
    header = ("POST "+route+" HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Length: "+
              str(len(raw))+"\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n").encode("ascii")
    reader = asyncio.StreamReader()
    reader.feed_data(header+raw)
    reader.feed_eof()
    return reader


async def controls(modules, output, evidence):
    H = modules["transport.http_provider"]
    O = modules["transport.ordinary_acquisition"]
    F = modules["discovery.formal_features"]
    PE = modules["portable_evidence"]
    parsed = PE.read_evidence(evidence)
    semantic, unit = parsed.document["semantic_id"], parsed.unit_id
    export = PE.export_id(semantic, unit, parsed.document["unit"][2][0][0])
    store = O.OrdinaryStore(output/"custody", semantic,
        dict(objects=8, exports=64, logical_bytes=MIB, db_pages=256), create=True)
    cases = []
    try:
        store.put_evidence(evidence)
        locator_request = dict(schema=O.LOCATOR_REQUEST, semantic_id=semantic,
                               export_id=export, max_bytes=MIB)
        evidence_request = dict(schema=O.EVIDENCE_REQUEST, semantic_id=semantic,
                                unit_id=unit, max_bytes=8*MIB)
        original = deepcopy((locator_request, evidence_request))

        def provider(cap):
            return H.Provider(ordinary=store, max_reply_bytes=cap, max_requests=16,
                              operation_ms=2000)

        async def call(p, route, request, writer=None):
            check()
            writer = Writer() if writer is None else writer
            await p._serve(request_reader(F, route, request), writer)
            need(p.reserved_reply_bytes == 0 and p.reply_bytes <= p.max_reply_bytes,
                 "SETTLED_BUDGET")
            return writer

        # Both original maxima exceed the whole grant, but exact objects fit.
        p = provider(30000)
        first = await call(p, H.ORDINARY_LOCATOR_ROUTE, locator_request)
        locator = first.body()
        need(locator is not None, "LOCATOR")
        second = await call(p, H.ORDINARY_EVIDENCE_ROUTE, evidence_request)
        need(second.body() == evidence and p.failures == 0 and
             p.reply_bytes == len(locator)+len(evidence), "UNKNOWN_SMALL_OBJECT")
        need((locator_request, evidence_request) == original, "REQUEST_INPUT_CHANGED")
        cases.append("oversized-client-maxima-complete-real-locator-and-evidence")

        # Real SQLite refuses before the evidence BLOB SELECT on a too-small cap.
        p = provider(len(evidence)-1)
        sql = []
        store.db.set_trace_callback(sql.append)
        denied = await call(p, H.ORDINARY_EVIDENCE_ROUTE, evidence_request)
        store.db.set_trace_callback(None)
        need(denied.body() is None and p.failures == 1 and p.reply_bytes == 0 and
             any("SELECT length(raw),raw_sha256 FROM objects" in stmt for stmt in sql) and
             not any("SELECT raw FROM objects" in stmt for stmt in sql), "LENGTH_FIRST")
        cases.append("oversized-object-refused-before-blob-read-no-truncation")

        p = provider(30000)
        missing = dict(evidence_request, unit_id="0"*64)
        need((await call(p, H.ORDINARY_EVIDENCE_ROUTE, missing)).body() is None and
             p.failures == 1 and p.reply_bytes == 0, "UNAVAILABLE")
        malformed = dict(evidence_request, max_bytes=True)
        need((await call(p, H.ORDINARY_EVIDENCE_ROUTE, malformed)).body() is None and
             p.failures == 2 and p.reply_bytes == 0, "ORIGINAL_VALIDATION")
        cases.append("missing-object-and-invalid-original-cap-refuse")

        p = provider(len(evidence))
        need((await call(p, H.ORDINARY_EVIDENCE_ROUTE, evidence_request)).body() == evidence,
             "EXACT_GRANT")
        need((await call(p, H.ORDINARY_LOCATOR_ROUTE, locator_request)).body() is None and
             p.failures == 1 and p.reply_bytes == len(evidence), "EXHAUSTED")
        cases.append("exact-budget-exhaustion-no-extra-body")

        # Preserve conservative admission while already-charged writes are live.
        p = provider(40000)
        holding = Writer(hold=True)
        task = asyncio.create_task(p._serve(request_reader(F, H.ORDINARY_EVIDENCE_ROUTE,
                                                         evidence_request), holding))
        try:
            await asyncio.wait_for(holding.entered.wait(), 1)
            need(p.reply_bytes == len(evidence) and p.reserved_reply_bytes == 40000,
                 "CHARGED_WRITE_STILL_RESERVED")
            denied = Writer()
            await p._serve(request_reader(F, H.ORDINARY_LOCATOR_ROUTE, locator_request), denied)
            need(denied.body() is None and p.failures == 1 and
                 p.reserved_reply_bytes == 40000, "CONCURRENT_CONSERVATIVE_REFUSAL")
        finally:
            holding.release.set()
            await task
        need(holding.body() == evidence and p.reserved_reply_bytes == 0, "WRITE_FINISHED")
        need((await call(p, H.ORDINARY_LOCATOR_ROUTE, locator_request)).body() == locator,
             "REMAINDER_AFTER_WRITE")
        cases.append("live-write-reservation-retained-and-released")

        p = provider(40000)
        interrupted = Writer(hold=True)
        task = asyncio.create_task(p._serve(request_reader(F, H.ORDINARY_EVIDENCE_ROUTE,
                                                         evidence_request), interrupted))
        try:
            await asyncio.wait_for(interrupted.entered.wait(), 1)
        finally:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        need(p.reply_bytes == len(evidence) and p.reserved_reply_bytes == 0,
             "INTERRUPTION_RETAINS_CHARGE")
        cases.append("cancelled-write-keeps-charge-and-releases-reservation")

        p = provider(30000)
        preview = dict(schema=O.PREVIEW_REQUEST, object_sha256="1"*64, object_bytes=MIB)
        sql = []
        store.db.set_trace_callback(sql.append)
        need((await call(p, H.ORDINARY_PREVIEW_ROUTE, preview)).body() is None and
             p.reply_bytes == 0 and p.failures == 1 and not sql, "PREVIEW_UNCHANGED")
        store.db.set_trace_callback(None)
        offer = dict(namespace="2"*64, features=["3"*64], max_bytes=MIB,
                     max_expanded_bytes=MIB)
        need((await call(p, H.OFFER_ROUTE, offer)).body() is None and
             p.reply_bytes == 0 and p.failures == 2, "OFFER_UNCHANGED")
        cases.append("exact-preview-and-discovery-offer-quotas-unchanged")
    finally:
        store.close()
    need(store.db is None, "CUSTODY_CLOSED")
    return cases


def forbidden(*args, **kwargs):
    raise AssertionError("CAPACITY_CONTROL_UNSELECTED_EXECUTION")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for key in ("package", "profile-sha256", "candidate", "candidate-sha256",
                "evidence", "evidence-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON")
    output = Path(args.output)
    need(output.is_absolute() and output.parent.is_dir() and not output.exists() and
         output.resolve().is_relative_to(ROOT/"experiments/v5-local-checks"), "FRESH_OUTPUT")
    evidence_path = Path(args.evidence)
    evidence = read(evidence_path, args.evidence_sha256)
    with ExitStack() as stack:
        for target in ("subprocess.Popen", "socket.create_connection", "asyncio.open_connection",
                       "asyncio.start_server", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        modules, pins = load(args)
        output.mkdir()
        cases = asyncio.run(controls(modules, output, evidence))
    check()
    for path, digest in pins.items():
        read(Path(path), digest)
    need(read(evidence_path, args.evidence_sha256) == evidence, "EVIDENCE_CHANGED")
    result = dict(status="PASS_REPLY_CAPACITY_CONTROLS", groups=len(cases), cases=cases,
        profile_sha256=args.profile_sha256, candidate_sha256=args.candidate_sha256,
        evidence_sha256=args.evidence_sha256, support_pins=pins,
        mathematical_acceptance=False, custody_closed=True,
        scope="REAL_HTTP_PARSE_DISPATCH_AND_SQLITE_CUSTODY_WITH_CONTROLLED_WRITERS_NO_SOCKETS",
        wall_seconds=time.monotonic()-START, cpu_seconds=time.process_time()-CPU)
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    with (output/"RESULT.json").open("xb") as stream:
        stream.write(raw)
    print(raw.decode(), flush=True)


if __name__ == "__main__":
    main()
