"""One prospective native-free suite against a coherent selected package.

Real immutable contact maps, egress, HTTP, finite directory service, ordinary
search, index and shared budget. The single indexed claim is synthetic metadata,
not mathematics. No native checker, source execution, external network, retained
knowledge state or subprocess. Root selects this finite run before execution.
"""
from __future__ import annotations

import time
START, CPU = time.monotonic(), time.process_time()
import argparse
import asyncio
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB = 1024**2
DEADLINE = START + 70
CASES = []


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def check():
    need(time.monotonic() < DEADLINE and time.process_time()-CPU < 35,
         "DIRECTORY_CONTROL_ORIGINAL_ENVELOPE")


def passed(name):
    check()
    CASES.append({"case": name, "status": "PASS"})


def refusal(call):
    try:
        call()
    except ValueError as error:
        return str(error)
    raise AssertionError("DIRECTORY_CONTROL_EXPECTED_REFUSAL")


def read(path, maximum=2*MIB):
    check()
    size = path.stat().st_size
    need(0 < size <= maximum, "DIRECTORY_CONTROL_READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "DIRECTORY_CONTROL_READ_CHANGED")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    need(len(raw) <= 2*MIB, "DIRECTORY_CONTROL_REPORT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw+b"\n")


def load_package(args):
    package = Path(args.package)
    need(package.is_absolute() and package.resolve(strict=True) == package,
         "DIRECTORY_CONTROL_PACKAGE")
    raw = read(package/"PROFILE.json")
    need(hashlib.sha256(raw).hexdigest() == args.profile_sha256,
         "DIRECTORY_CONTROL_PROFILE_PIN")
    descriptor = json.loads(raw)
    loader_raw = read(package/"profile.py")
    pin = descriptor["files"]["profile.py"]
    need(len(loader_raw) == pin["bytes"] and hashlib.sha256(loader_raw).hexdigest() == pin["sha256"],
         "DIRECTORY_CONTROL_LOADER_PIN")
    spec = importlib.util.spec_from_file_location("_directory_control_profile", package/"profile.py")
    loader = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loader
    exec(compile(loader_raw, str(package/"profile.py"), "exec"), loader.__dict__)
    return loader.load(package, args.profile_sha256,
        {"python_runtime": args.python_runtime, "lean_runtime": args.lean_runtime},
        DEADLINE, check_parent=check)


def endpoint(host="127.0.0.1", port=40001, tls=False, server_name=None):
    return dict(host=host, port=port, tls=tls, server_name=server_name)


def policy_config(*ports):
    return dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="loopback-test", public_ports=[],
                test_endpoints=[dict(host="127.0.0.1", port=p) for p in sorted(set(ports))])


PUBLIC_POLICY = dict(schema="DMKN_V5_OWNER_EGRESS_V1", mode="public-ipv4",
                     public_ports=[443], test_endpoints=[])


def pure_controls(api):
    C, H, F = api.CD, api.H, api.F
    namespace, features = "1"*64, ["2"*64]
    hints = [endpoint(port=40001), endpoint(port=40002)]
    doc = dict(schema=C.MAP_SCHEMA, namespace=namespace,
               entries=[dict(features=features, endpoints=hints)])
    req = dict(schema=C.REQUEST_SCHEMA, namespace=namespace, features=features,
               nonce="3"*64, max_contacts=8, max_bytes=C.REPLY_MAX)
    index = C.ContactMap.from_bytes(F.compact(doc), check_budget=check)
    result = C.read_reply(index.reply(req, check_budget=check), req)
    need(result["contacts"] == hints and result["truncated"] is False and
         result["global_complete"] is False and result["mathematical_acceptance"] is False,
         "DIRECTORY_CONTROL_EXACT_ADVISORY_REPLY")
    result["contacts"][0]["port"] = 1
    need(C.read_reply(index.reply(req), req)["contacts"] == hints,
         "DIRECTORY_CONTROL_IMMUTABLE_MAP")
    passed("immutable-map-exact-advisory-reply")

    count = dict(req, max_contacts=1)
    limited = C.read_reply(index.reply(count), count)
    need(limited["contacts"] == hints[:1] and limited["truncated"] is True,
         "DIRECTORY_CONTROL_COUNT_PREFIX")
    absent = dict(req, features=["4"*64])
    absent_result = C.read_reply(index.reply(absent), absent)
    need(absent_result["contacts"] == [] and absent_result["global_complete"] is False,
         "DIRECTORY_CONTROL_ABSENCE_NOT_GLOBAL")
    wrong_ns = dict(req, namespace="5"*64)
    need(C.read_reply(index.reply(wrong_ns), wrong_ns)["contacts"] == [],
         "DIRECTORY_CONTROL_NAMESPACE_ABSENCE")
    tiny = dict(req, max_bytes=len(F.compact(dict(absent_result,
        features=features, truncated=True))))
    tiny_result = C.read_reply(index.reply(tiny), tiny)
    need(tiny_result["contacts"] == [] and tiny_result["truncated"] is True,
         "DIRECTORY_CONTROL_BYTE_PREFIX")
    refusal(lambda: index.reply(dict(req, max_bytes=1)))
    passed("count-byte-truncation-and-local-absence")

    for key, value in (("namespace", "5"*64), ("nonce", "5"*64),
                       ("features", ["5"*64]), ("global_complete", True),
                       ("mathematical_acceptance", True), ("truncated", 1),
                       ("status", "CHECKED")):
        bad = C.read_reply(index.reply(req), req)
        bad[key] = value
        refusal(lambda b=bad: C.read_reply(F.compact(b), req))
    refusal(lambda: C.read_reply(index.reply(req)+b"\n", req))
    passed("reply-binding-assurance-and-canonical-json-refusals")

    for malformed in (dict(req, nonce="not-a-nonce"), dict(req, max_contacts=True),
                      dict(req, features=[features[0], features[0]]),
                      dict(req, max_bytes=C.REPLY_MAX+1), dict(req, extra=True)):
        refusal(lambda r=malformed: C.request_limit(r))
    duplicate = deepcopy(doc); duplicate["entries"].append(deepcopy(doc["entries"][0]))
    refusal(lambda: C.ContactMap.from_bytes(F.compact(duplicate)))
    duplicate = deepcopy(doc); duplicate["entries"][0]["endpoints"] = [hints[0], hints[0]]
    refusal(lambda: C.ContactMap.from_bytes(F.compact(duplicate)))
    refusal(lambda: C.ContactMap.from_bytes(F.compact(doc)+b"\n"))
    refusal(lambda: C.ContactMap.from_bytes(b" "*(C.MAP_MAX+1)))
    passed("malformed-duplicate-and-overbudget-input-refusals")

    public = C.OwnerEgressPolicy(deepcopy(PUBLIC_POLICY))
    accepted = public.endpoint(endpoint("8.8.8.8", 443, True, "example.invalid"))
    need(type(accepted) is H.Endpoint and accepted.ca_file is None,
         "DIRECTORY_CONTROL_SYSTEM_CA_ONLY")
    for host in ("127.0.0.1", "10.0.0.1", "172.16.0.1", "192.168.1.1", "169.254.1.1",
                 "100.64.0.1", "0.0.0.0", "224.0.0.1", "255.255.255.255", "192.0.2.1",
                 "::1", "::ffff:8.8.8.8", "8.008.8.8", "example.invalid"):
        refusal(lambda h=host: public.endpoint(endpoint(h, 443, True, "example.invalid")))
    passed("public-policy-excludes-private-special-mapped-and-dns-dials")

    for row in (endpoint("8.8.8.8", 80, True, "example.invalid"),
                endpoint("8.8.8.8", 443, False),
                endpoint("8.8.8.8", 443, True, "Bad.Example"),
                endpoint("8.8.8.8", 443, True, "bad/name"),
                dict(endpoint("8.8.8.8", 443, True, "example.invalid"), ca_file="peer.pem"),
                dict(endpoint("8.8.8.8", 443, True, "example.invalid"), mode="loopback-test")):
        refusal(lambda r=row: public.endpoint(r))
    passed("no-port-tls-name-ca-or-policy-escalation")

    config = policy_config(40001)
    local = C.OwnerEgressPolicy(config)
    config["test_endpoints"].append(dict(host="127.0.0.1", port=40002))
    exposed = local.report(); exposed["config"]["test_endpoints"].append(dict(host="127.0.0.1", port=40002))
    need(type(local.endpoint(hints[0])) is H.Endpoint, "DIRECTORY_CONTROL_EXACT_LOOPBACK")
    refusal(lambda: local.endpoint(hints[1]))
    refusal(lambda: C.OwnerEgressPolicy(dict(PUBLIC_POLICY, test_endpoints=[dict(host="127.0.0.1", port=40001)])))
    passed("owner-policy-is-immutable-and-loopback-is-explicit")

    provider = H.Provider(contact_directory=index)
    need(C.read_reply(provider.dispatch(C.ROUTE, req), req)["contacts"] == hints,
         "DIRECTORY_CONTROL_REAL_PROVIDER_DISPATCH")
    absent_offer = F.strict(provider.dispatch(H.OFFER_ROUTE,
        dict(namespace=namespace, features=features, max_bytes=1024, max_expanded_bytes=1024)), 1024)
    need(absent_offer["status"] == "NO_OFFER" and absent_offer["reason"] == "ROLE_NOT_SERVED" and
         absent_offer["global_complete"] is False, "DIRECTORY_CONTROL_NO_INDEX_OFFER")
    passed("directory-only-provider-has-no-index-role")
    return dict(helper_source="selected-package", pure_groups=8)


async def async_controls(loaded, output, report):
    api = loaded.peer_api
    C, H, F, X, O = api.CD, api.H, api.F, api.X, api.O
    allowance = SimpleNamespace(deadline=DEADLINE-4, check=check)
    adapter = api.OrdinaryExportAdapter(loaded.installation.semantic_id)
    specs = [{"tag": "declaration-kind", "value": "theorem"},
             {"tag": "result-head", "head": {"tag": "sort"}}]
    features = api.compile_query(adapter.namespace, specs)
    name = [[0, {"$bytes": list(b"DirectorySyntheticClaim")}]]
    raw = F.compact(dict(schema=api.PP.SCHEMA, semantic_id=loaded.installation.semantic_id,
        unit_id=hashlib.sha256(b"directory-control-no-proof-or-evidence").hexdigest(),
        export_name=name, header=[2, [], [loaded.A.E.EXPR_FORMAT, [[0]], [[1, 0]], 0]],
        type_bindings=[]))
    expected = adapter.extract(raw)
    need(set(features) <= set(expected["features"]), "DIRECTORY_CONTROL_SYNTHETIC_RECORD")
    save(output/"SYNTHETIC-RECORD.json", expected)
    index, provider, service = None, None, None
    extras, dials, cleanup_errors = [], [], []
    original_dial = asyncio.open_connection

    # Deterministic source-boundary controls: no real delay, DNS, TLS handshake
    # or socket. Only local clock/setup are injected; expiry must stop transport
    # before the forbidden connection callback is reached.
    fake_clock, forbidden_dials = [10.0], []

    async def forbidden_dial(*args, **kwargs):
        forbidden_dials.append((args, kwargs))
        raise AssertionError("DIRECTORY_CONTROL_EXPIRED_DIAL")

    def consume_tls_setup(**kwargs):
        fake_clock[0] = 12.0
        return SimpleNamespace(minimum_version=None)

    request = dict(namespace=adapter.namespace, features=features,
                   max_bytes=1024, max_expanded_bytes=1024)
    with patch.object(X, "time", SimpleNamespace(monotonic=lambda: fake_clock[0])), \
            patch.object(asyncio, "open_connection", new=forbidden_dial):
        for setup, horizon, expected_error in (
                (False, 9.0, "FAIR_ABSOLUTE_DEADLINE_EXHAUSTED"),
                (True, 11.0, "FAIR_LOCAL_ATTEMPT_SETUP_EXHAUSTED")):
            fake_clock[0] = 10.0
            try:
                with patch.object(X.ssl, "create_default_context", new=consume_tls_setup):
                    await X.exchange(H.Endpoint("127.0.0.1", 40001, setup),
                        H.OFFER_ROUTE, request, 1024, 5000, absolute_deadline=horizon)
            except ValueError as error:
                need(str(error) == expected_error, "DIRECTORY_CONTROL_EXPIRY_REFUSAL_CLASS")
            else:
                raise AssertionError("DIRECTORY_CONTROL_EXPIRED_EXCHANGE_NOT_REFUSED")
    need(forbidden_dials == [], "DIRECTORY_CONTROL_ABSOLUTE_DEADLINE_NO_DIAL")
    passed("absolute-horizon-refuses-late-entry-and-local-tls-setup-before-dial")

    async def observe_dial(host, port, **kwargs):
        # Observation only; the real selected transport and sockets run unchanged.
        need(host == "127.0.0.1", "DIRECTORY_CONTROL_EXTERNAL_DIAL_FORBIDDEN")
        dials.append(dict(host=host, port=port, tls=kwargs.get("ssl") is not None))
        return await original_dial(host, port, **kwargs)

    def contact(ep):
        return dict(host=ep.host, port=ep.port, tls=ep.tls, server_name=ep.server_name,
                    ca_file=None, ca_sha256=None)

    def find_config(seed, egress):
        return dict(contacts={"seed": contact(seed)}, directories=["seed"],
            specs=deepcopy(specs), routes=[deepcopy(specs)], egress=egress,
            directory=dict(requests=1, reply_bytes=C.REPLY_MAX, max_contacts=1,
                max_bytes=C.REPLY_MAX, max_age_ms=20000, attempt_timeout_ms=3000),
            search=dict(limits=dict(providers=2, snapshots=4, requests=4, pages=2,
                examined=32, candidates=8, bytes=MIB, wall_ms=12000, inflight=1),
                offer=dict(max_bytes=65536, max_expanded_bytes=MIB, max_age_ms=12000),
                page=dict(scanned=8, matches=4, bytes=65536, timeout_ms=1000,
                    record_probes=64, node_reads=100000, hash_calls=2000000, sql_vm_steps=1000000)))

    async def expect_failure(config, *, ledger=None):
        try:
            await api.directory_find(loaded, config, allowance, network_budget=ledger)
        except api.PeerFailure as error:
            need(error.report["status"] == "FAILED", "DIRECTORY_CONTROL_FAILURE_STATUS")
            return error.report
        raise AssertionError("DIRECTORY_CONTROL_EXPECTED_API_FAILURE")

    try:
        index = api.DS.Store(output/"fresh-index", adapter,
            dict(max_objects=1, max_postings=64, max_features=64, max_snapshots=2,
                 max_logical_bytes=2*MIB, max_db_pages=256), create=True)
        admitted = index.admit(raw, expected_id=expected["object_id"])
        provider = H.Provider(index=index, max_connections=2, max_requests=8,
                              max_reply_bytes=4*MIB, operation_ms=3000)
        provider_endpoint = await provider.start("127.0.0.1", 0)
        hint = endpoint(port=provider_endpoint.port)
        # The egress allowlist is test harness permission, not a provider input
        # to search. The actual search contacts must come from the directory.
        egress = policy_config(provider_endpoint.port)
        unused_port = 40001 if provider_endpoint.port != 40001 else 40002
        service_config = dict(entries=[dict(specs=deepcopy(specs),
            endpoints=[hint, endpoint(port=unused_port)])], host="127.0.0.1", port=0,
            tls=None, lease_seconds=4, cleanup_seconds=10,
            limits=dict(max_connections=2, max_requests=8, max_reply_bytes=MIB, operation_ms=3000))
        ready = asyncio.get_running_loop().create_future()
        service = asyncio.create_task(api.directory_serve(loaded, service_config, allowance,
            ready=lambda value: ready.set_result(value)))
        done, _ = await asyncio.wait((ready, service), timeout=5, return_when=asyncio.FIRST_COMPLETED)
        if service in done:
            await service
        need(ready.done(), "DIRECTORY_CONTROL_SERVICE_NOT_READY")
        ready_value = ready.result()
        seed = H.Endpoint(ready_value["host"], ready_value["port"])
        config = find_config(seed, egress)
        need(all(row["port"] != provider_endpoint.port for row in config["contacts"].values()),
             "DIRECTORY_CONTROL_PROVIDER_NOT_A_CONFIGURED_CONTACT")

        with patch.object(asyncio, "open_connection", new=observe_dial):
            ledger = O.OrdinaryBudget(deadline=allowance.deadline-3,
                requests=5, reply_bytes=MIB+C.REPLY_MAX)
            before_deadline = ledger.deadline
            original_find, seen_ledgers = api.find, []

            async def observe_find(*args, **kwargs):
                seen_ledgers.append(kwargs.get("network_budget"))
                return await original_find(*args, **kwargs)

            with patch.object(api, "find", new=observe_find):
                result = await api.directory_find(loaded, config, allowance, network_budget=ledger)
            report["discovery"] = result
            need(seen_ledgers == [ledger] and ledger.sequence == 0 and ledger.pending is None and
                 ledger.deadline <= before_deadline and not ledger.closed,
                 "DIRECTORY_CONTROL_SAME_NONRENEWING_LEDGER")
            need(ledger.external == [dict(label="directory-find", requests=1, reply_bytes=C.REPLY_MAX),
                dict(label="peer-find", requests=4, reply_bytes=MIB)] and ledger.requests == 5 and
                ledger.reply_bytes == MIB+C.REPLY_MAX, "DIRECTORY_CONTROL_COMBINED_PREPAYMENT")
            ledger.close()
            need(result["matches"] == [dict(provider=result["learned_contacts"][0]["contact"],
                snapshot_id=admitted["snapshot_id"], record=expected)],
                "DIRECTORY_CONTROL_LEARNED_PROVIDER_REAL_MATCH")
            need(result["learned_contacts"][0]["endpoint"] == hint and
                 result["directory"]["truncated"] is True and result["directory"]["requests"] == 1 and
                 result["global_complete"] is False and result["mathematical_acceptance"] is False and
                 result["verified_scan_coverage"] is False,
                 "DIRECTORY_CONTROL_UNKNOWN_ENDPOINT_TRUNCATION_ASSURANCE")
            need([row["port"] for row in dials] == [seed.port, provider_endpoint.port, provider_endpoint.port],
                 "DIRECTORY_CONTROL_REAL_DIRECTORY_OFFER_PAGE")
            need(result["search"]["search"]["session"]["pending_requests"] == 0 and
                 result["cleanup_errors"] == [], "DIRECTORY_CONTROL_SEARCH_SETTLED")
            passed("real-finite-directory-to-unknown-provider-to-ordinary-record")
            passed("one-original-ledger-two-prepaid-slices-and-one-real-find")

            no_contact = deepcopy(config); no_contact["routes"] = [[deepcopy(specs[0])]]
            before = len(dials)
            empty = await api.directory_find(loaded, no_contact, allowance)
            report["no_contact"] = empty
            need(len(dials) == before+1 and empty["matches"] == [] and empty["search"] is None and
                 empty["learned_contacts"] == [] and empty["global_complete"] is False and
                 empty["network"]["closed"] is True, "DIRECTORY_CONTROL_NO_CONTACT_NO_SEARCH")
            passed("empty-route-is-incomplete-without-provider-dial")

            denied = deepcopy(config); denied["egress"] = deepcopy(PUBLIC_POLICY)
            before = len(dials)
            refused = await api.directory_find(loaded, denied, allowance)
            report["denied"] = refused
            need(len(dials) == before+1 and refused["search"] is None and
                 refused["lookups"][0]["rejected"] == 1 and refused["learned_contacts"] == [],
                 "DIRECTORY_CONTROL_EGRESS_REJECTION_BEFORE_DIAL")
            passed("peer-cannot-enable-loopback-or-bypass-owner-egress")

            short_ledger = O.OrdinaryBudget(deadline=allowance.deadline-3,
                requests=4, reply_bytes=MIB+C.REPLY_MAX)
            before = len(dials)
            failed = await expect_failure(config, ledger=short_ledger)
            need(len(dials) == before and short_ledger.sequence == 0 and short_ledger.requests == 0,
                 "DIRECTORY_CONTROL_CAPACITY_BEFORE_IO")
            short_ledger.close(); report["short_ledger"] = failed
            invalid_route = deepcopy(config)
            invalid_route["routes"] = [[dict(tag="object-kind", value=adapter.extract(raw)["kind"])]]
            failed = await expect_failure(invalid_route)
            need(len(dials) == before and failed["error"]["code"] == "DIRECTORY_ROUTE_QUERY_SUBSET",
                 "DIRECTORY_CONTROL_ROUTE_SUBSET_BEFORE_IO")
            passed("combined-capacity-and-route-subset-refuse-before-io")

            expired = deepcopy(config); expired["directory"]["max_age_ms"] = 1
            before = len(dials)
            expired_result = await api.directory_find(loaded, expired, allowance)
            report["short_horizon"] = expired_result
            need(len(dials) == before and expired_result["directory"]["requests"] == 0 and
                 expired_result["termination"] == "DIRECTORY_NO_LEGAL_ATTEMPT_SLICE",
                 "DIRECTORY_CONTROL_NO_LEGAL_EXPIRY_SLICE")
            passed("insufficient-original-horizon-never-dials")

            # The real transport carries malformed directory metadata. No index,
            # source or proof acceptance is mocked by this adversarial provider.
            directory_map = C.ContactMap.from_bytes(F.compact(dict(schema=C.MAP_SCHEMA,
                namespace=adapter.namespace, entries=[dict(features=features, endpoints=[hint])])))

            class BadNonceProvider(H.Provider):
                def dispatch(self, route, request, *, check_budget=None):
                    reply = super().dispatch(route, request, check_budget=check_budget)
                    if route == C.ROUTE:
                        value = F.strict(reply, C.REPLY_MAX)
                        value["nonce"] = "e"*64 if request["nonce"] == "f"*64 else "f"*64
                        return F.compact(value)
                    return reply

            bad = BadNonceProvider(contact_directory=directory_map, max_connections=1,
                                   max_requests=2, max_reply_bytes=2*C.REPLY_MAX, operation_ms=1000)
            extras.append(bad)
            bad_endpoint = await bad.start("127.0.0.1", 0)
            malformed = find_config(bad_endpoint, egress)
            before = len(dials)
            malformed_result = await api.directory_find(loaded, malformed, allowance)
            report["malformed"] = malformed_result
            need(len(dials) == before+1 and malformed_result["search"] is None and
                 malformed_result["lookups"][0]["status"] == "INVALID_DIRECTORY_METADATA" and
                 malformed_result["directory"]["charged_reply_bytes"] == C.REPLY_MAX,
                 "DIRECTORY_CONTROL_BAD_METADATA_CHARGED_WITHOUT_FOLLOW")
            passed("real-http-nonce-mismatch-charged-and-not-followed")

            terminal = deepcopy(config)
            terminal["contacts"]["second"] = contact(seed)
            terminal["directories"].append("second")
            terminal["directory"].update(requests=2, reply_bytes=2*C.REPLY_MAX)
            attempts = []

            async def uncertain(*args, **kwargs):
                attempts.append(args[0])
                raise X.UnsettledTransportError("FAIR_SOCKET_CLOSURE_UNCERTAIN")

            before = len(dials)
            with patch.object(X, "exchange", new=uncertain):
                failed = await expect_failure(terminal)
            report["uncertain_cleanup"] = failed
            need(len(attempts) == 1 and len(dials) == before and
                 failed["error"]["code"] == "FAIR_SOCKET_CLOSURE_UNCERTAIN" and
                 failed["directory"]["charged_reply_bytes"] == C.REPLY_MAX,
                 "DIRECTORY_CONTROL_UNCERTAIN_CLEANUP_IS_TERMINAL")
            passed("injected-unsettled-transport-stops-before-next-directory")

        async with asyncio.timeout(6):
            service_result = await service
        report["service"] = service_result
        need(service_result["status"] == "LEASE_FINISHED" and service_result["quiescent"] is True and
             service_result["cleanup_errors"] == [] and service_result["provider"]["active"] == 0 and
             service_result["provider"]["reserved_reply_bytes"] == 0 and
             service_result["mathematical_acceptance"] is False,
             "DIRECTORY_CONTROL_FINITE_STATE_FREE_SERVICE_CLOSED")
        passed("finite-state-free-directory-service-closes-cleanly")
    finally:
        if service is not None and not service.done():
            service.cancel()
            try:
                async with asyncio.timeout(max(0.001, min(4, DEADLINE-time.monotonic()))):
                    await service
            except asyncio.CancelledError:
                pass
            except BaseException as error:
                # A failing service may report its cancellation after completing
                # cleanup; retain it rather than silently treating it as clean.
                cleanup_errors.append("service:"+type(error).__name__)
        for owned in [*extras, *([provider] if provider is not None else [])]:
            try:
                async with asyncio.timeout(max(0.001, min(3, DEADLINE-time.monotonic()))):
                    await owned.stop()
                need(owned.server is None and not owned.tasks and owned.reserved_reply_bytes == 0,
                     "DIRECTORY_CONTROL_PROVIDER_CLEANUP")
            except BaseException as error:
                cleanup_errors.append("provider:"+type(error).__name__)
        report["providers"] = [owned.status() for owned in extras]
        if provider is not None:
            report["record_provider"] = provider.status()
        if index is not None:
            try:
                index.close()
            except BaseException as error:
                cleanup_errors.append("index:"+type(error).__name__)
        report.update(dials=dials, cleanup_errors=cleanup_errors,
                      index_closed=index is None or index.db is None,
                      service_task_finished=service is None or service.done())
    need(not cleanup_errors and report["index_closed"] and report["service_task_finished"],
         "DIRECTORY_CONTROL_CLEANUP_UNCERTAIN")
    passed("all-owned-listeners-handlers-and-fresh-index-closed")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "DIRECTORY_CONTROL_ISOLATED_PROCESS")
    need(output.is_absolute() and output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         output.parent.is_dir() and output.parent.resolve(strict=True) == output.parent and
         not os.path.lexists(output), "DIRECTORY_CONTROL_FRESH_OUTPUT")
    for selected in (args.package, args.python_runtime, args.lean_runtime):
        path = Path(selected)
        need(path.is_absolute() and not output.is_relative_to(path) and not path.is_relative_to(output),
             "DIRECTORY_CONTROL_PROTECTED_OUTPUT")
    output.mkdir()
    report = dict(passed=False, cases=CASES, profile_sha256=args.profile_sha256,
        authority="NATIVE_FREE_REAL_PACKAGE_API_LOOPBACK_SYNTHETIC_METADATA_NOT_MATHEMATICS_OR_TLS")
    try:
        loaded = load_package(args)
        report["pure"] = pure_controls(loaded.peer_api)
        asyncio.run(async_controls(loaded, output, report))
        report["passed"] = True
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error)[:1000])
    report.update(wall_seconds=time.monotonic()-START, harness_cpu_seconds=time.process_time()-CPU,
                  completed_groups=len(CASES))
    save(output/"RESULT.json", report)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
