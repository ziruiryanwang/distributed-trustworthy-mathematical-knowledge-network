"""Six finite transport-lifecycle controls; root selects execution separately.

Real loopback sockets/TLS and one ordinary inert preview read. No Lean, proof,
mathematical admission, old database, external host or reused private key.
The selected package supplies unchanged verified support; only the separately
pinned candidate Provider is loaded as a fresh sibling module.
"""
from __future__ import annotations

import time
START_WALL, START_CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import ssl
import subprocess
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START_WALL + 50
CPU_CAP = 25
PROFILE = "97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834"
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

# Same offline .NET CertificateRequest mechanism as the historical test helper,
# but a fresh output-local identity, not that helper's fixed old target/key.
# No certificate-store access. The test key is never printed or adopted by a peer.
TLS_SCRIPT = r'''
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -lt 7) { throw 'TEST_TLS_PWSH7_REQUIRED' }
$fixtureRoot = [Environment]::GetEnvironmentVariable('DMKN_BOUNDED_TRANSPORT_TLS')
if (-not [IO.Directory]::Exists($fixtureRoot)) { throw 'TEST_TLS_PARENT' }
$certPath = [IO.Path]::Combine($fixtureRoot, 'test-cert.pem')
$keyPath = [IO.Path]::Combine($fixtureRoot, 'test-key.pem')
if ([IO.File]::Exists($certPath) -or [IO.File]::Exists($keyPath)) { throw 'TEST_TLS_FRESH' }
$rsa = $null
$cert = $null
try {
    $rsa = [Security.Cryptography.RSA]::Create(2048)
    $request = [Security.Cryptography.X509Certificates.CertificateRequest]::new(
        'CN=DMKN disposable loopback transport test', $rsa,
        [Security.Cryptography.HashAlgorithmName]::SHA256,
        [Security.Cryptography.RSASignaturePadding]::Pkcs1)
    $request.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509BasicConstraintsExtension]::new($true,$true,0,$true))
    $usage = [Security.Cryptography.X509Certificates.X509KeyUsageFlags]::DigitalSignature -bor
             [Security.Cryptography.X509Certificates.X509KeyUsageFlags]::KeyCertSign -bor
             [Security.Cryptography.X509Certificates.X509KeyUsageFlags]::KeyEncipherment
    $request.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509KeyUsageExtension]::new($usage,$true))
    $request.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509SubjectKeyIdentifierExtension]::new($request.PublicKey,$false))
    $purposes = [Security.Cryptography.OidCollection]::new()
    [void]$purposes.Add([Security.Cryptography.Oid]::new('1.3.6.1.5.5.7.3.1'))
    $request.CertificateExtensions.Add(
        [Security.Cryptography.X509Certificates.X509EnhancedKeyUsageExtension]::new($purposes,$false))
    $san = [Security.Cryptography.X509Certificates.SubjectAlternativeNameBuilder]::new()
    $san.AddIpAddress([Net.IPAddress]::Parse('127.0.0.1'))
    $san.AddDnsName('localhost')
    $request.CertificateExtensions.Add($san.Build())
    $now = [DateTimeOffset]::UtcNow
    $cert = $request.CreateSelfSigned($now.AddMinutes(-5), $now.AddDays(1))
    $utf8 = [Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText($certPath,$cert.ExportCertificatePem(),$utf8)
    [IO.File]::WriteAllText($keyPath,$rsa.ExportPkcs8PrivateKeyPem(),$utf8)
    [Console]::WriteLine('DISPOSABLE_LOOPBACK_TEST_TLS_CREATED')
} finally {
    if ($null -ne $cert) { $cert.Dispose() }
    if ($null -ne $rsa) { $rsa.Dispose() }
}
'''


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-START_CPU < CPU_CAP,
         "TRANSPORT_TEST_ORIGINAL_ENVELOPE")


def read(path, maximum=2*MIB):
    check()
    need(path.is_file() and not path.is_symlink(), "TRANSPORT_TEST_INPUT_FILE")
    size = path.stat().st_size
    need(0 < size <= maximum, "TRANSPORT_TEST_INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "TRANSPORT_TEST_INPUT_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= MIB, "TRANSPORT_TEST_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw+b"\n")


def load(args):
    root = Path(args.package)
    need(root.is_absolute() and root.resolve(strict=True) == root,
         "TRANSPORT_TEST_PACKAGE_PATH")
    raw = read(root/"PROFILE.json")
    need(args.profile_sha256 == PROFILE and hashlib.sha256(raw).hexdigest() == PROFILE,
         "TRANSPORT_TEST_PROFILE_PIN")
    profile = json.loads(raw)
    installation_raw = read(root/"installation/INSTALLATION.json")
    need(hashlib.sha256(installation_raw).hexdigest() == profile["installation_manifest_sha256"],
         "TRANSPORT_TEST_INSTALLATION_MANIFEST_PIN")
    installation = json.loads(installation_raw)
    candidate = Path(args.candidate)
    need(candidate.is_absolute() and candidate.resolve(strict=True) == candidate,
         "TRANSPORT_TEST_CANDIDATE_PATH")
    # No package/native loader. Empty namespace paths prevent an unlisted lazy
    # import from silently pulling another product module from disk.
    for name in ("discovery", "transport", "custody"):
        need(name not in sys.modules, "TRANSPORT_TEST_PACKAGE_PRELOADED")
        package = ModuleType(name)
        package.__path__ = []
        sys.modules[name] = package
    modules = {}
    for name, relative in SUPPORT:
        need(name not in sys.modules, "TRANSPORT_TEST_SUPPORT_PRELOADED")
        path = candidate if relative is None else root/relative
        source = read(path)
        if relative is None:
            need(hashlib.sha256(source).hexdigest() == args.candidate_sha256,
                 "TRANSPORT_TEST_CANDIDATE_PIN")
        else:
            row = installation["files"][relative.removeprefix("installation/")] if relative.startswith(
                "installation/") else profile["files"][relative]
            need(len(source) == row["bytes"] and hashlib.sha256(source).hexdigest() == row["sha256"],
                 "TRANSPORT_TEST_SUPPORT_PIN:"+relative)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        exec(compile(source, str(path), "exec"), module.__dict__)
        modules[name] = module
        if "." in name:
            parent, child = name.rsplit(".", 1)
            setattr(sys.modules[parent], child, module)
    support = SimpleNamespace(O=modules["transport.ordinary_acquisition"],
        PP=modules["portable_preview"], F=modules["discovery.formal_features"],
        E=modules["ordinary_evidence"], semantic_id=modules["ordinary_semantics"].semantic_id())
    return support, modules["transport.http_provider"]


def generate_tls(args, output, report):
    pwsh = Path(args.pwsh)
    raw = read(pwsh, 32*MIB)
    need(pwsh.is_absolute() and hashlib.sha256(raw).hexdigest() == args.pwsh_sha256,
         "TRANSPORT_TEST_PWSH_PIN")
    tls = output/"disposable-tls"
    tls.mkdir()
    env = dict(os.environ, DMKN_BOUNDED_TRANSPORT_TLS=str(tls))
    command = [str(pwsh), "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", TLS_SCRIPT]
    started = time.monotonic()
    with (tls/"stdout.txt").open("xb") as stdout, (tls/"stderr.txt").open("xb") as stderr:
        child = subprocess.run(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
            stdout=stdout, stderr=stderr, timeout=min(12, DEADLINE-time.monotonic()),
            creationflags=subprocess.CREATE_NO_WINDOW)
    check()
    need(child.returncode == 0 and (tls/"stderr.txt").stat().st_size == 0 and
         read(tls/"stdout.txt", 1024).strip() == b"DISPOSABLE_LOOPBACK_TEST_TLS_CREATED",
         "TRANSPORT_TEST_TLS_GENERATOR")
    cert = tls/"test-cert.pem"
    key = tls/"test-key.pem"
    cert_raw = read(cert, 16384)
    need(0 < key.stat().st_size <= 16384, "TRANSPORT_TEST_TLS_KEY_BOUND")
    report["test_tls"] = dict(scope="FRESH_DISPOSABLE_LOOPBACK_ONLY_NOT_OPERATOR_IDENTITY",
        certificate_sha256=hashlib.sha256(cert_raw).hexdigest(),
        script_sha256=hashlib.sha256(TLS_SCRIPT.encode("utf-8")).hexdigest(),
        generator_exit=child.returncode, generator_reaped=True,
        generator_wall_seconds=time.monotonic()-started,
        private_key_published=False, certificate_store_modified=False)
    return cert, key


async def until(predicate, code, seconds=2):
    end = min(DEADLINE-2, time.monotonic()+seconds)
    while not predicate():
        check()
        need(time.monotonic() < end, code)
        await asyncio.sleep(0.01)


async def close_client(writer):
    writer.close()
    try:
        async with asyncio.timeout(1):
            await writer.wait_closed()
    except (ConnectionError, ssl.SSLError):
        pass


class Observations:
    """Wrap the REAL transport conversion, never simulate acceptance or TLS."""
    def __init__(self, maximum):
        self.maximum, self.sockets, self.events = maximum, [], []

    @contextmanager
    def install(self):
        loop = asyncio.get_running_loop()
        original = loop.connect_accepted_socket

        async def observed(factory, sock, **kwargs):
            existing = sum(old.fileno() != -1 for old in self.sockets)
            need(existing < self.maximum, "TRANSPORT_TEST_REAL_RAW_SLOT_OVERLAP")
            need(len(self.events) < 16, "TRANSPORT_TEST_OBSERVATION_BOUND")
            self.sockets.append(sock)
            row = dict(sequence=len(self.sockets), prior_open_raw_sockets=existing,
                initial_fileno=sock.fileno(), tls=kwargs.get("ssl") is not None,
                returned=False, error_type=None)
            self.events.append(row)
            try:
                value = await original(factory, sock, **kwargs)
                row["returned"] = True
                return value
            except BaseException as caught:
                row["error_type"] = type(caught).__name__
                raise

        with patch.object(loop, "connect_accepted_socket", new=observed):
            yield self

    def all_closed(self):
        return all(sock.fileno() == -1 for sock in self.sockets)

    def report(self):
        return dict(events=self.events, accepted_raw_socket_count=len(self.sockets),
                    raw_socket_filenos=[sock.fileno() for sock in self.sockets],
                    all_raw_sockets_closed=self.all_closed())


async def stop_observed(provider, observation, seconds=2):
    started = time.monotonic()
    async with asyncio.timeout(min(seconds, DEADLINE-time.monotonic())):
        await provider.stop()
    need(time.monotonic()-started < seconds, "TRANSPORT_TEST_STOP_NOT_PROMPT")
    need(provider.server is None and not provider.tasks and observation.all_closed(),
         "TRANSPORT_TEST_REAL_CLOSURE_NOT_OBSERVED")
    state = provider.status()
    need(state["active"] == 0 and state["reserved_reply_bytes"] == 0,
         "TRANSPORT_TEST_UNSETTLED_STATUS")
    return dict(stop_wall_seconds=time.monotonic()-started, status=state,
                observation=observation.report())


async def cases(loaded, H, output, cert, key, report):
    api = loaded
    store = None
    groups, all_providers, all_writers, cleanup_errors = report["groups"], [], [], []
    stop_attempted = set()

    async def start(*, encrypted, attempts=8):
        provider = H.Provider(ordinary=store, max_connections=1,
            max_requests=attempts, max_reply_bytes=65536, operation_ms=60000)
        all_providers.append(provider)
        endpoint = await provider.start("127.0.0.1", 0, tls_context=tls if encrypted else None)
        return provider, endpoint

    async def client(endpoint, *, encrypted=False):
        kwargs = dict(ssl=client_tls, server_hostname="127.0.0.1",
            ssl_handshake_timeout=2, ssl_shutdown_timeout=1) if encrypted else {}
        async with asyncio.timeout(2):
            reader, writer = await asyncio.open_connection(endpoint.host, endpoint.port, **kwargs)
        all_writers.append(writer)
        return reader, writer

    async def stop(provider, observation):
        stop_attempted.add(provider)
        return await stop_observed(provider, observation)

    try:
        store = api.O.OrdinaryStore(output/"fresh-inert-custody", api.semantic_id,
            dict(objects=1, exports=1, logical_bytes=65536, db_pages=256), create=True)
        name = [[0, {"$bytes": list(b"SyntheticTransportUnprovedClaim")}]]
        raw = api.F.compact(dict(schema=api.PP.SCHEMA, semantic_id=api.semantic_id,
            unit_id=hashlib.sha256(b"synthetic-transport-unproved-unit").hexdigest(),
            export_name=name, header=[2, [], [api.E.EXPR_FORMAT, [[0]], [[1, 0]], 0]],
            type_bindings=[]))
        stored = store.put_preview(raw, before_commit=check)
        need(stored["mathematical_acceptance"] is False, "TRANSPORT_TEST_INERT_ONLY")
        save(output/"SYNTHETIC-PREVIEW.json", json.loads(raw))
        tls = H.server_tls(str(cert), str(key))
        client_tls = ssl.create_default_context(cafile=str(cert))
        client_tls.minimum_version = ssl.TLSVersion.TLSv1_2
        # K=1 means the second TCP connection can be queued by the OS, but must
        # not become a second TLS conversion while the first is still owned.
        observation = Observations(1)
        with observation.install():
            provider, endpoint = await start(encrypted=True, attempts=3)
            _, first = await client(endpoint)
            await until(lambda: len(observation.sockets) == 1, "TRANSPORT_TEST_FIRST_HANDSHAKE")
            _, second = await client(endpoint)
            await asyncio.sleep(0.15)
            need(len(observation.sockets) == 1 and not observation.all_closed(),
                 "TRANSPORT_TEST_STALLED_TLS_CAP")
            before = provider.status()
            need(before["accepted_attempts"] == 1 and before["requests"] == 0,
                 "TRANSPORT_TEST_PREHANDSHAKE_ACCOUNTING")
            await close_client(first)
            await until(lambda: len(observation.sockets) == 2, "TRANSPORT_TEST_SLOT_NOT_REUSED_AFTER_CLOSE")
            need(observation.sockets[0].fileno() == -1 and not observation.events[1]["returned"],
                 "TRANSPORT_TEST_RAW_CLOSURE_BEFORE_REFILL")
            result = await stop(provider, observation)
            await close_client(second)
            groups.append(dict(name="pending_tls_slot_and_real_close_before_refill", before=before, **result))

        observation = Observations(1)
        with observation.install():
            provider, endpoint = await start(encrypted=True, attempts=2)
            for index in range(2):
                _, writer = await client(endpoint)
                writer.write(b"not a TLS record\n")
                try:
                    await writer.drain()
                except ConnectionError:
                    pass  # A prompt real TLS refusal can race this test write.
                await until(lambda: len(observation.sockets) == index+1 and observation.all_closed(),
                            "TRANSPORT_TEST_FAILED_TLS_NOT_CLOSED")
                await close_client(writer)
            await until(lambda: provider.status()["admission_exhausted"],
                        "TRANSPORT_TEST_ATTEMPT_EXHAUSTION")
            state = provider.status()
            need(state["accepted_attempts"] == 2 and state["requests"] == 0 and
                 state["handshake_failures"] == 2 and not state["accepting"],
                 "TRANSPORT_TEST_FAILED_TLS_NOT_PAID")
            # A closed listener must not silently accept a third attempt.
            try:
                async with asyncio.timeout(0.5):
                    _, writer = await asyncio.open_connection(endpoint.host, endpoint.port)
            except (ConnectionError, OSError, TimeoutError):
                refused = True
            else:
                all_writers.append(writer)
                await close_client(writer)
                refused = False
            need(refused and len(observation.sockets) == 2, "TRANSPORT_TEST_THIRD_ATTEMPT_ACCEPTED")
            groups.append(dict(name="failed_handshakes_consume_finite_attempts",
                before_stop=state, **await stop(provider, observation)))

        for encrypted in (False, True):
            observation = Observations(1)
            with observation.install():
                provider, endpoint = await start(encrypted=encrypted)
                reader, writer = await client(endpoint, encrypted=encrypted)
                writer.write(b"POST /v5/ordinary/preview HTTP/1.1\r\n")
                await writer.drain()
                await until(lambda: provider.status()["requests"] == 1,
                            "TRANSPORT_TEST_HEADER_HANDLER_NOT_ENTERED")
                result = await stop(provider, observation)
                # An actual EOF/reset must follow, not merely a zero counter.
                try:
                    async with asyncio.timeout(1):
                        eof = await reader.read(1)
                    need(eof == b"", "TRANSPORT_TEST_CLIENT_NOT_CLOSED")
                except (ConnectionError, ssl.SSLError):
                    pass
                await close_client(writer)
                groups.append(dict(name=("tls" if encrypted else "http")+"_incomplete_header_prompt_stop",
                    original_operation_ms=60000, **result))

        observation = Observations(1)
        with observation.install():
            provider, endpoint = await start(encrypted=True)
            verified = H.Endpoint(endpoint.host, endpoint.port, tls=True,
                server_name="127.0.0.1", ca_file=str(cert))
            response = await H.exchange(verified, H.ORDINARY_PREVIEW_ROUTE,
                dict(schema=api.O.PREVIEW_REQUEST, object_sha256=hashlib.sha256(raw).hexdigest(),
                     object_bytes=len(raw)), len(raw), 2000)
            need(response["status"] == 200 and response["raw"] == raw and
                 response["reply_bytes"] == len(raw), "TRANSPORT_TEST_ORDINARY_EXACT_REPLY")
            parsed = api.PP.read_preview(response["raw"])
            need(parsed.mathematical_acceptance is False, "TRANSPORT_TEST_REPLY_IS_NOT_WARRANT")
            await until(observation.all_closed, "TRANSPORT_TEST_POSITIVE_CONNECTION_NOT_CLOSED")
            state = provider.status()
            need(state["requests"] == 1 and state["reply_bytes"] == len(raw),
                 "TRANSPORT_TEST_POSITIVE_ACCOUNTING")
            groups.append(dict(name="verified_tls_ordinary_inert_preview_unchanged",
                reply_sha256=hashlib.sha256(raw).hexdigest(), reply_bytes=len(raw),
                before_stop=state, **await stop(provider, observation)))

        observation = Observations(1)
        with observation.install():
            provider, _ = await start(encrypted=True)
            await asyncio.sleep(0.03)
            need(not observation.sockets, "TRANSPORT_TEST_IDLE_UNEXPECTED_ACCEPT")
            groups.append(dict(name="idle_pending_accept_prompt_stop",
                **await stop(provider, observation)))
        need(len(groups) == 6, "TRANSPORT_TEST_GROUP_CENSUS")
    finally:
        failure_in_flight = sys.exception()
        for writer in all_writers:
            try:
                await close_client(writer)
            except BaseException as caught:
                cleanup_errors.append(dict(phase="client", type=type(caught).__name__))
        for provider in reversed(all_providers):
            if provider not in stop_attempted:
                stop_attempted.add(provider)
                try:
                    async with asyncio.timeout(2):
                        await provider.stop()
                except BaseException as caught:
                    cleanup_errors.append(dict(phase="provider", type=type(caught).__name__))
            if provider.server is not None or provider.tasks:
                cleanup_errors.append(dict(phase="provider_not_quiescent"))
        if store is not None:
            try:
                store.close()
            except BaseException as caught:
                cleanup_errors.append(dict(phase="store", type=type(caught).__name__))
        report["cleanup_errors"] = cleanup_errors
        if failure_in_flight is None:
            need(not cleanup_errors, "TRANSPORT_TEST_CLEANUP_UNCERTAIN")


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for key in ("package", "profile-sha256", "candidate",
                "candidate-sha256", "pwsh", "pwsh-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
         "TRANSPORT_TEST_SUPPORTED_RUNTIME")
    need(output.is_absolute() and not output.exists() and output.parent.is_dir() and
         output.parent.resolve(strict=True) == output.parent,
         "TRANSPORT_TEST_FRESH_OUTPUT")
    output.mkdir()
    report = dict(schema="DMKN_BOUNDED_TRANSPORT_CONTROLS_V1", ok=False, groups=[],
        source_only_until_root_selection=True, mathematical_acceptance=False,
        python=sys.version, openssl=ssl.OPENSSL_VERSION,
        profile_sha256=args.profile_sha256, candidate_sha256=args.candidate_sha256,
        cleanup_errors=[], scope="LOOPBACK_TRANSPORT_AND_INERT_PREVIEW_NOT_NATIVE_OR_PUBLIC_READINESS")
    error = None
    try:
        loaded, candidate = load(args)
        cert, key = generate_tls(args, output, report)
        asyncio.run(cases(loaded, candidate, output, cert, key, report))
        check()
        report["ok"] = True
    except BaseException as caught:
        error = caught
        report["error"] = dict(type=type(caught).__name__, message=str(caught)[:300])
    finally:
        report["wall_seconds"] = time.monotonic()-START_WALL
        report["harness_cpu_seconds"] = time.process_time()-START_CPU
        save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if error is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
