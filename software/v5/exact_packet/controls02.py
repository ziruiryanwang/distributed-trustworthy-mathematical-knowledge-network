"""Fresh fixture-only successor for failed exact-packet groups 04 and 05.

Imports the frozen original controls from this operation's source snapshot.
No test body or product implementation is replaced. Root selects execution.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SELF = Path("software/v5/exact_packet/controls02.py")
ORIGINAL = Path("software/v5/exact_packet/controls.py")
ORIGINAL_BYTES = 34036
ORIGINAL_SHA = "bd9a48119a3ae428e343a2d6061256026fc530cf0b281bf33e49e554214f2883"
SELECTED = (
    "test_04_budget_contact_and_commit_expiry",
    "test_05_actual_placement_exact_and_duplicate_accounting",
)


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction()
        for item in (path, *path.parents)), "CONTROL02_ORDINARY_PATH")
    return path


def main():
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "CONTROL02_OUTPUT_REQUIRED")
    output = ordinary(Path(sys.argv[2]))
    need(output.is_dir() and output.is_relative_to(PROJECT) and os.name == "nt"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "CONTROL02_ISOLATED_WINDOWS")
    source = ordinary(output/"sources"/SELF)
    need(Path(__file__).resolve() == source, "CONTROL02_SNAPSHOT_EXECUTION_REQUIRED")
    selection = json.loads((output/"selection.json").read_bytes())
    pins = selection["sources"]
    need(type(pins) is dict and len(pins) == 138, "CONTROL02_SOURCE_CENSUS")
    need(pins.get(SELF.as_posix()) == hashlib.sha256(source.read_bytes()).hexdigest(),
         "CONTROL02_SELF_PIN")
    original = ordinary(output/"sources"/ORIGINAL)
    need(original.is_file() and original.stat().st_size == ORIGINAL_BYTES,
         "CONTROL02_ORIGINAL_SIZE")
    need(pins.get(ORIGINAL.as_posix()) == ORIGINAL_SHA
         and hashlib.sha256(original.read_bytes()).hexdigest() == ORIGINAL_SHA,
         "CONTROL02_ORIGINAL_PIN")
    spec = importlib.util.spec_from_file_location("exact_packet_controls01_frozen", original)
    need(spec is not None and spec.loader is not None, "CONTROL02_ORIGINAL_LOADER")
    base = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = base
    spec.loader.exec_module(base)
    need(all(name in base.SELECTED for name in SELECTED), "CONTROL02_ORIGINAL_METHODS")

    class Controls02(base.Controls):
        async def fixture(self, terminal=True):
            # The parent fixture supplies 8 MiB. Adapt only constructor config;
            # invoke the real selected provider with all its guards unchanged.
            # Patch lifetime ends before the test sends any request.
            provider_type = base.ET.CompositeProvider
            def provider(*args, **kwargs):
                need(kwargs.get("max_reply_bytes") == 8*base.MIB,
                     "CONTROL02_ORIGINAL_PROVIDER_CAP")
                kwargs["max_reply_bytes"] = 32*base.MIB
                return provider_type(*args, **kwargs)
            with patch.object(base.ET, "CompositeProvider", provider):
                fixture = await super().fixture(terminal)
            need(type(fixture.provider) is provider_type
                 and fixture.provider.max_reply_bytes == 32*base.MIB,
                 "CONTROL02_REAL_PROVIDER_CONFIG")
            # The HTTP server returns http_provider_receipts.Endpoint. Contacts
            # validate against http_provider.Endpoint. Preserve every field,
            # but construct the endpoint with the actual policy's public API.
            policy = base.LP.OwnerEgressPolicy(self.egress(fixture))
            contact = {key: getattr(fixture.endpoint, key)
                       for key in ("host", "port", "tls", "server_name")}
            endpoint = policy.endpoint(contact)
            need(base.asdict(endpoint) == base.asdict(fixture.endpoint),
                 "CONTROL02_ENDPOINT_FIELDS")
            fixture.endpoint = endpoint
            return fixture

    # unittest receives these two explicit names only. The six passing groups
    # remain in the frozen module but cannot be selected by this entry point.
    base.SELECTED = SELECTED
    base.Controls = Controls02
    original_writer = base.write_new
    def write_report(path, raw):
        if path == output/"exact-packet-controls-result.json":
            report = json.loads(raw)
            need(report["selected"] == list(SELECTED)
                 and report["tests_run"] == 2, "CONTROL02_EXACT_TWO_TESTS")
            report.update(
                schema="DMKN_V5_EXACT_PACKET_CONTROLS_V2",
                scope="REAL_LOOPBACK_HTTP_BUDGET_CONTACT_COMMIT_AND_PLACEMENT_ONLY",
                predecessor_source_sha256=ORIGINAL_SHA,
                predecessor_outcome="FAILED_TWO_FIXTURE_ERRORS_PRESERVED",
                fixture_corrections={
                    "endpoint": "OwnerEgressPolicy.endpoint_PRESERVES_ALL_FIELDS",
                    "provider_max_reply_bytes": 32*base.MIB,
                    "provider_configuration_only": True,
                },
                passing_predecessor_groups_rerun=False,
            )
            report.pop("higher_facade_scope")
            raw = json.dumps(report, sort_keys=True, separators=(",", ":"),
                             allow_nan=False).encode()+b"\n"
        return original_writer(path, raw)
    base.write_new = write_report
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
