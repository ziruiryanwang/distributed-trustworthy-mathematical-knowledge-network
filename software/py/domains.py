"""Explicit operator-local path domains; never supplied by peer requests."""
from __future__ import annotations

import os
from pathlib import Path
import sys

PYTHON_FLAGS = ["-B", "-E", "-s", "-S"]
DOMAIN_KEYS = {"install", "state", "scratch", "lean_runtime"}


def require(value, code):
    if not value:
        raise ValueError(code)


def require_python_profile():
    require(sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_user_site and sys.flags.no_site, "PYTHON_ISOLATED_STARTUP_REQUIRED")


def absolute_directory(value, *, existing):
    require(type(value) is str and value and len(value) <= 32767, "DOMAIN_PATH_TYPE")
    path = Path(value)
    require(path.is_absolute(), "DOMAIN_ABSOLUTE_PATH_REQUIRED")
    # No broad drive/UNC-share root or alternate-stream/reserved spelling.
    require(path != Path(path.anchor) and len(path.parts) >= 2, "DOMAIN_ROOT_FORBIDDEN")
    require(all(":" not in part and not part.endswith((".", " "))
                and not os.path.isreserved(part) and part not in (".", "..")
                for part in path.parts[1:]), "DOMAIN_PATH_COMPONENT")
    resolved = path.resolve(strict=existing)
    require(resolved != Path(resolved.anchor), "DOMAIN_ROOT_FORBIDDEN")
    require(not resolved.exists() or resolved.is_dir(), "DOMAIN_NOT_DIRECTORY")
    return resolved


def overlap(left, right):
    return left.is_relative_to(right) or right.is_relative_to(left)


class Domains:
    def __init__(self, record):
        require(type(record) is dict and set(record) == DOMAIN_KEYS, "DOMAIN_FIELDS")
        self.install = absolute_directory(record["install"], existing=True)
        self.lean_runtime = absolute_directory(record["lean_runtime"], existing=True)
        self.state = absolute_directory(record["state"], existing=False)
        self.scratch = absolute_directory(record["scratch"], existing=False)
        require((self.install / "py").is_dir(), "INSTALL_PY_DIRECTORY_REQUIRED")
        require(self.install != self.lean_runtime and not self.install.is_relative_to(self.lean_runtime), "RUNTIME_MUST_NOT_CONTAIN_INSTALL")
        require(not overlap(self.state, self.scratch), "STATE_SCRATCH_OVERLAP")
        for writable in (self.state, self.scratch):
            require(not overlap(writable, self.install) and not overlap(writable, self.lean_runtime), "WRITABLE_IMMUTABLE_DOMAIN_OVERLAP")

    @classmethod
    def from_config(cls, config):
        require(type(config) is dict and type(config.get("schema")) is int
                and config["schema"] == 3, "CONFIG_DOMAIN_SCHEMA")
        return cls(config["domains"])

    @classmethod
    def from_stage_plan(cls, plan):
        require(type(plan) is dict and type(plan.get("schema")) is int
                and plan["schema"] == 2, "STAGE_DOMAIN_SCHEMA")
        return cls(plan["domains"])

    @classmethod
    def from_record(cls, record):
        return cls(record)

    def as_dict(self):
        return {key: str(getattr(self, key)) for key in sorted(DOMAIN_KEYS)}

    def require_state(self, path):
        path = Path(path)
        require(path.is_absolute() and path.resolve() == self.state, "CONFIG_STATE_PATH_MISMATCH")
        return self.state

    def require_read(self, path):
        path = Path(path)
        require(path.is_absolute(), "READ_ABSOLUTE_PATH_REQUIRED")
        path = path.resolve(strict=True)
        require(any(path.is_relative_to(root) for root in
                    (self.install, self.state, self.scratch, self.lean_runtime)), "READ_DOMAIN")
        return path

    def require_work(self, path):
        path = Path(path)
        require(path.is_absolute(), "WORK_ABSOLUTE_PATH_REQUIRED")
        path = path.resolve()
        require((path != self.state / "work" and path.is_relative_to(self.state / "work"))
                or (path != self.scratch and path.is_relative_to(self.scratch)), "SELECTED_WORK_DOMAIN")
        return path

    def require_write(self, path):
        # Exactly the operator's state/work and scratch trees, never install/runtime.
        return self.require_work(path)

    def require_stage(self, path, request_directory):
        request_directory = self.require_work(request_directory)
        path = self.require_work(path)
        require(path != request_directory and path.is_relative_to(request_directory), "SELECTED_REQUEST_STAGE_DOMAIN")
        return path

    def require_package(self, path):
        path = self.require_read(path)
        require(path.is_dir() and (path.is_relative_to(self.install / "assets")
                or path.is_relative_to(self.state) or path.is_relative_to(self.scratch)), "CANONICAL_PACKAGE_DOMAIN")
        return path

    def require_lean(self, path):
        path = self.require_read(path)
        require(path == (self.lean_runtime / "bin" / "lean.exe").resolve(strict=True)
                and path.is_file(), "EXACT_LEAN_RUNTIME_EXECUTABLE")
        return path
