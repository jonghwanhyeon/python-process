from __future__ import annotations

from pathlib import Path

import pytest

from process import (
    STDOUT,
    ProcessAlreadyRunError,
    ProcessError,
    ProcessInvalidStreamError,
    ProcessNotRunError,
    ProcessTimeoutError,
)
from process.asyncio import Process


@pytest.mark.asyncio
async def test_process_error_invalid_command() -> None:
    with pytest.raises(ProcessError):
        await Process(["invalid-command"]).run()


@pytest.mark.asyncio
async def test_process_not_run_error(sleep: list[Path]) -> None:
    process = Process([*sleep, "1"])
    with pytest.raises(ProcessNotRunError):
        await process.join(timeout=1)


@pytest.mark.asyncio
async def test_process_already_run_error(sleep: list[Path]) -> None:
    process = await Process([*sleep, "1"]).run()
    with pytest.raises(ProcessAlreadyRunError):
        await process.run()

    async with Process([*sleep, "1"]) as process:
        with pytest.raises(ProcessAlreadyRunError):
            await process.run()


@pytest.mark.asyncio
async def test_process_invalid_stream_error(echo: list[Path]) -> None:
    async with Process([*echo, "Hello, World!"], stdout=None) as process:
        with pytest.raises(ProcessInvalidStreamError):
            await process.output()

    async with Process([*echo, "Hello, World!"], stderr=None) as process:
        with pytest.raises(ProcessInvalidStreamError):
            await process.error()

    async with Process([*echo, "Hello, World!"], stderr=STDOUT) as process:
        with pytest.raises(ProcessInvalidStreamError):
            await process.error()

    async with Process([*echo, "Hello, World!"], stdout=None, stderr=None) as process:
        with pytest.raises(ProcessInvalidStreamError):
            await process.output()

        with pytest.raises(ProcessInvalidStreamError):
            await process.error()


@pytest.mark.asyncio
async def test_process_timeout_error(sleep: list[Path]) -> None:
    process = await Process([*sleep, "1"]).run()
    with pytest.raises(ProcessTimeoutError):
        await process.join(timeout=0.5)

    await process.join()
