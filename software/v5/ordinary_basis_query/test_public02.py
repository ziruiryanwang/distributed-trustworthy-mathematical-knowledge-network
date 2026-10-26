"""One fresh public check with a corrected 1024-MiB child envelope.

The used test and query sources remain unchanged. This is not a retry loop and
does not run the native-free controls. Root selects this entry separately.
"""
from pathlib import Path
import hashlib
import importlib.util
import sys

PRIOR_SHA = "c2fb010137343b3324181476e5bc2ad972085fc9fc2f38231871c4f4891194ad"


def main():
    if sys.argv[1:3] != ["--mode", "public"] or sys.argv.count("--mode") != 1:
        raise ValueError("BASIS_PUBLIC02_FIXED_PUBLIC_MODE")
    source = Path(__file__).resolve().with_name("test_query.py")
    with source.open("rb") as stream:
        raw = stream.read(65537)
    if not 0 < len(raw) <= 65536 or hashlib.sha256(raw).hexdigest() != PRIOR_SHA:
        raise ValueError("BASIS_PUBLIC02_PRIOR_TEST_PIN")
    spec = importlib.util.spec_from_file_location("_basis_public02_prior", source)
    prior = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = prior
    exec(compile(raw, str(source), "exec"), prior.__dict__)
    if prior.LIMITS["memory_mib"] != 768:
        raise ValueError("BASIS_PUBLIC02_PRIOR_ALLOWANCE")
    prior.LIMITS = dict(prior.LIMITS, memory_mib=1024)
    return prior.main()


if __name__ == "__main__":
    raise SystemExit(main())
