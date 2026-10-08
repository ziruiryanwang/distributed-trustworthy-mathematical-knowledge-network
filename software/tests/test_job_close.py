"""Four in-memory controls for checked Job.close; no native stages or real Jobs.

Root executes only through a separately reviewed, bounded close-test worker.
This module opens no state, creates no fixture files and launches no process.
It constructs Job without __init__ and replaces kernel/error functions with
in-memory fakes. This is branch evidence, not an OS handle-release experiment.
"""
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, call, patch

if not (sys.dont_write_bytecode and sys.flags.ignore_environment
        and sys.flags.no_user_site and sys.flags.no_site):
    raise RuntimeError("CLOSE_TESTS_REQUIRE_PYTHON_B_E_s_S")

INSTALL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(INSTALL / "py"))

import run_stage as R

if Path(R.__file__).resolve() != INSTALL / "py" / "run_stage.py":
    raise RuntimeError("CLOSE_TEST_RUNNER_PATH")


class JobCloseTests(unittest.TestCase):
    HANDLE = 0x1234
    ERROR_CODE = 6

    def fixture(self, returns):
        job = R.Job.__new__(R.Job)
        job.handle = self.HANDLE
        kernel = SimpleNamespace(CloseHandle=Mock(side_effect=returns))
        job.k = kernel
        error = OSError(self.ERROR_CODE, "injected CloseHandle failure")
        errors = SimpleNamespace(get_last_error=Mock(return_value=self.ERROR_CODE),
                                 WinError=Mock(return_value=error))
        return job, kernel, errors, error

    def test_success_clears_handle(self):
        job, kernel, errors, _ = self.fixture([1])
        with patch.object(R, "C", errors):
            self.assertIsNone(job.close())
        self.assertIsNone(job.handle)
        kernel.CloseHandle.assert_called_once_with(self.HANDLE)
        errors.get_last_error.assert_not_called()
        errors.WinError.assert_not_called()

    def test_false_return_raises_and_retains_handle(self):
        job, kernel, errors, error = self.fixture([0])
        with patch.object(R, "C", errors):
            with self.assertRaises(OSError) as raised:
                job.close()
        self.assertIs(raised.exception, error)
        self.assertEqual(job.handle, self.HANDLE)
        kernel.CloseHandle.assert_called_once_with(self.HANDLE)
        errors.get_last_error.assert_called_once_with()
        errors.WinError.assert_called_once_with(self.ERROR_CODE)

    def test_successful_close_is_idempotent(self):
        job, kernel, errors, _ = self.fixture([1])
        with patch.object(R, "C", errors):
            self.assertIsNone(job.close())
            self.assertIsNone(job.close())
            self.assertIsNone(job.close())
        self.assertIsNone(job.handle)
        kernel.CloseHandle.assert_called_once_with(self.HANDLE)
        errors.get_last_error.assert_not_called()
        errors.WinError.assert_not_called()

    def test_explicit_retry_after_failure_closes_retained_handle(self):
        job, kernel, errors, error = self.fixture([0, 1])
        with patch.object(R, "C", errors):
            with self.assertRaises(OSError) as raised:
                job.close()
            self.assertIs(raised.exception, error)
            self.assertEqual(job.handle, self.HANDLE)
            self.assertIsNone(job.close())
        self.assertIsNone(job.handle)
        self.assertEqual(kernel.CloseHandle.call_args_list,
                         [call(self.HANDLE), call(self.HANDLE)])
        errors.get_last_error.assert_called_once_with()
        errors.WinError.assert_called_once_with(self.ERROR_CODE)


if __name__ == "__main__":
    unittest.main()
