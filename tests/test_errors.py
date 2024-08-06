from __future__ import annotations

from pathlib import Path

import pytest

from process import (
    STDOUT,
    Process,
    ProcessAlreadyRunError,
    ProcessError,
    ProcessInvalidStreamError,
    ProcessNotRunError,
    ProcessTimeoutError,
)


def test_process_error_invalid_command() -> None:
    with pytest.raises(ProcessError):
        Process(["invalid-command"]).run()


def test_process_not_run_error(sleep: list[Path]) -> None:
    process = Process([*sleep, "1"])
    with pytest.raises(ProcessNotRunError):
        process.join(timeout=1)


def test_process_already_run_error(sleep: list[Path]) -> None:
    process = Process([*sleep, "1"]).run()
    with pytest.raises(ProcessAlreadyRunError):
        process.run()

    with Process([*sleep, "1"]) as process:
        with pytest.raises(ProcessAlreadyRunError):
            process.run()


def test_process_invalid_stream_error(echo: list[Path]) -> None:
    with Process([*echo, "Hello, World!"], stdout=None) as process:
        with pytest.raises(ProcessInvalidStreamError):
            process.output()

    with Process([*echo, "Hello, World!"], stderr=None) as process:
        with pytest.raises(ProcessInvalidStreamError):
            process.error()

    with Process([*echo, "Hello, World!"], stderr=STDOUT) as process:
        with pytest.raises(ProcessInvalidStreamError):
            process.error()

    with Process([*echo, "Hello, World!"], stdout=None, stderr=None) as process:
        with pytest.raises(ProcessInvalidStreamError):
            process.output()

        with pytest.raises(ProcessInvalidStreamError):
            process.error()


def test_process_timeout_error(sleep: list[Path]) -> None:
    process = Process([*sleep, "1"]).run()
    with pytest.raises(ProcessTimeoutError):
        process.join(timeout=0.5)

    process.join()
