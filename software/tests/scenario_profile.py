"""Explicit test-only outer-sixteen grant; installed product profiles stay fixed.

The driver must authenticate this file and the original run_stage/supervise
files before import, check their loaded origins, and bind all three in pins.
Construction creates no process. Never use this module as a product runner.
"""
from pathlib import Path
import sys

import run_stage
import supervise


ACTIVE_PROCESSES = 16


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def structure_values(value):
    """Compare every declared field, including nested fields, without padding."""
    return tuple((name, structure_values(item) if isinstance(item, run_stage.C.Structure)
                  else item) for name, _ in type(value)._fields_
                 for item in (getattr(value, name),))


class Job(run_stage.Job):
    """Set the reviewed sixteen-process grant while the new Job is empty."""

    def __init__(self, seconds, memory_mib, active_processes):
        require(type(active_processes) is int and active_processes == ACTIVE_PROCESSES,
                "SCENARIO_EXPLICIT_SIXTEEN_REQUIRED")
        require(type(seconds) is int and 1 <= seconds <= 450, "SCENARIO_CPU_GRANT")
        require(type(memory_mib) is int and 1 <= memory_mib <= 6144,
                "SCENARIO_MEMORY_GRANT")
        try:
            super().__init__(seconds, memory_mib, active_processes=8)
            initial = self.stats()
            require(initial["active_processes"] == 0 and initial["total_processes"] == 0,
                    "SCENARIO_JOB_MUST_BE_UNASSIGNED")
            limits = self.extended_limits()
            basic = limits.BasicLimitInformation
            require(basic.ActiveProcessLimit == 8
                    and basic.PerJobUserTimeLimit == seconds * 10_000_000
                    and basic.LimitFlags == (0x4 | 0x8 | 0x200 | 0x2000)
                    and limits.JobMemoryLimit == memory_mib * 1024 * 1024,
                    "SCENARIO_BASE_LIMITS_CHANGED")
            # This is the sole changed field of the complete queried structure.
            basic.ActiveProcessLimit = ACTIVE_PROCESSES
            expected = structure_values(limits)
            if not self.k.SetInformationJobObject(
                    self.handle, 9, run_stage.C.byref(limits), run_stage.C.sizeof(limits)):
                raise run_stage.C.WinError(run_stage.C.get_last_error())
            require(structure_values(self.extended_limits()) == expected,
                    "SCENARIO_LIMIT_READBACK_CHANGED")
            final = self.stats()
            require(final["active_processes"] == 0 and final["total_processes"] == 0,
                    "SCENARIO_JOB_NOT_EMPTY_AFTER_CONFIGURATION")
        except BaseException:
            self.close()
            raise

    def extended_limits(self):
        limits = run_stage.ExtendedLimits()
        if not self.k.QueryInformationJobObject(
                self.handle, 9, run_stage.C.byref(limits), run_stage.C.sizeof(limits), None):
            raise run_stage.C.WinError(run_stage.C.get_last_error())
        return limits


class Transport(supervise.Transport):
    """Reuse common validation/containment with one explicit outer grant change."""

    def __init__(self, python, node, config, state, evidence_root, runner_module, limits):
        require(type(limits) is dict
                and type(limits.get("active_processes")) is int
                and limits["active_processes"] == ACTIVE_PROCESSES,
                "SCENARIO_EXPLICIT_SIXTEEN_REQUIRED")
        require(runner_module is sys.modules[__name__], "SCENARIO_RUNNER_MODULE_REQUIRED")
        # The base constructor validates paths/pins and other grants; it neither
        # creates a Job nor launches a process. Its eight is only a local input.
        common_limits = dict(limits, active_processes=8)
        super().__init__(python, node, config, state, evidence_root, runner_module, common_limits)
        bound_paths = {Path(pin["path"]).resolve(strict=True) for pin in self.pins}
        require({Path(run_stage.__file__).resolve(strict=True),
                 Path(supervise.__file__).resolve(strict=True)} <= bound_paths,
                "SCENARIO_ORIGINAL_MODULE_PINS_REQUIRED")
        self.limits = dict(self.limits, active_processes=ACTIVE_PROCESSES)

    def verify_pins(self, record):
        super().verify_pins(record)
        record["scope"] = ("reviewed test-only outer-sixteen scenario process tree; "
                           "requested OS limit and polled aggregate count; "
                           "no mathematical authority or exact auxiliary-PID maximum")
