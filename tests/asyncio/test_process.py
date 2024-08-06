from __future__ import annotations

import signal
from pathlib import Path
from tempfile import TemporaryFile

import pytest

from process import PIPE, STDOUT
from process.asyncio import Process


@pytest.mark.asyncio
async def test_init() -> None:
    process = Process("echo Hello, World!")
    assert process.arguments == ["echo", "Hello,", "World!"]

    process = Process("echo 'Hello, World!'")
    assert process.arguments == ["echo", "Hello, World!"]

    process = Process(["echo", "Hello,", "World!"])
    assert process.arguments == ["echo", "Hello,", "World!"]


@pytest.mark.asyncio
async def test_run(echo: list[Path]) -> None:
    process = await Process([*echo, "Hello, World!"]).run()
    assert process._process is not None
    await process.join()


@pytest.mark.asyncio
async def test_context_manager(lazy_echo: list[Path]) -> None:
    async with Process([*lazy_echo, "Hello, World!"]) as process:
        assert process.exit_code is None

    assert process.exit_code == 0
    assert (await process.output()).strip() == b"Hello, World!"


@pytest.mark.asyncio
async def test_output(echo: list[Path]) -> None:
    async with Process([*echo, "Hello, stdout!"]) as process:
        assert (await process.output()).strip() == b"Hello, stdout!"

    assert (await process.output()).strip() == b"Hello, stdout!"


@pytest.mark.asyncio
async def test_output_consumed_by_others(echo: list[Path]) -> None:
    async with Process([*echo, "Hello, stdout!"]) as process:
        assert await process.stdout.read(7) == b"Hello, "
        assert (await process.output()).strip() == b"stdout!"

    assert (await process.output()).strip() == b"stdout!"


@pytest.mark.asyncio
async def test_error(echo_error: list[Path]) -> None:
    async with Process([*echo_error, "Hello, stderr!"]) as process:
        assert (await process.error()).strip() == b"Hello, stderr!"

    assert (await process.error()).strip() == b"Hello, stderr!"


@pytest.mark.asyncio
async def test_error_consumed_by_others(echo_error: list[Path]) -> None:
    async with Process([*echo_error, "Hello, stderr!"]) as process:
        assert await process.stderr.read(7) == b"Hello, "
        assert (await process.error()).strip() == b"stderr!"

    assert (await process.error()).strip() == b"stderr!"


@pytest.mark.asyncio
async def test_stdin_from_buffer(cat: list[Path]) -> None:
    async with Process(cat, stdin=b"Hello, stdin!") as process:
        assert (await process.output()).strip() == b"Hello, stdin!"


@pytest.mark.asyncio
async def test_stdin_from_file(assets_path: Path, cat: list[Path]) -> None:
    with open(assets_path / "lorem-ipsum.txt", "rb") as input_file:  # noqa: ASYNC230
        async with Process(cat, stdin=input_file) as process:
            assert (await process.output()).strip() == b"Lorem ipsum odor amet, consectetuer adipiscing elit."


@pytest.mark.asyncio
async def test_stdout_as_file(echo: list[Path]) -> None:
    with TemporaryFile("w+b") as output_file:
        async with Process([*echo, "Hello, stdout!"], stdout=output_file):
            pass

        output_file.seek(0)
        assert output_file.read().strip() == b"Hello, stdout!"


@pytest.mark.asyncio
async def test_stderr_as_file(echo_error: list[Path]) -> None:
    with TemporaryFile("w+b") as output_file:
        async with Process([*echo_error, "Hello, stderr!"], stderr=output_file):
            pass

        output_file.seek(0)
        assert output_file.read().strip() == b"Hello, stderr!"


@pytest.mark.asyncio
async def test_stdout_from_stdout_as_buffer(echo_error: list[Path]) -> None:
    async with Process([*echo_error, "Hello, stdout!"], stderr=STDOUT) as process:
        assert (await process.output()).strip() == b"Hello, stdout!"


@pytest.mark.asyncio
async def test_stderr_from_stdout_as_file(echo_error: list[Path]) -> None:
    with TemporaryFile("w+b") as output_file:
        async with Process([*echo_error, "Hello, stdout!"], stdout=output_file, stderr=STDOUT):
            pass

        output_file.seek(0)
        assert output_file.read().strip() == b"Hello, stdout!"


@pytest.mark.asyncio
async def test_stdout_from_file_as_file(assets_path: Path, cat: list[Path]) -> None:
    with open(assets_path / "lorem-ipsum.txt", "rb") as input_file:  # noqa: ASYNC230
        with TemporaryFile("w+b") as output_file:
            async with Process(cat, stdin=input_file, stdout=output_file):
                pass

            output_file.seek(0)
            assert output_file.read().strip() == b"Lorem ipsum odor amet, consectetuer adipiscing elit."


@pytest.mark.asyncio
async def test_process_join(sleep: list[Path]) -> None:
    process = await Process([*sleep, "0.5"]).run()
    assert process.exit_code is None

    await process.join()
    assert process.exit_code == 0


@pytest.mark.asyncio
async def test_process_signal(sleep: list[Path]) -> None:
    async with Process([*sleep, "3"]) as process:
        assert process.exit_code is None
        process.signal(signal.SIGTERM)

    assert process.exit_code is not None


@pytest.mark.asyncio
async def test_process_termination(sleep: list[Path]) -> None:
    async with Process([*sleep, "3"]) as process:
        assert process.exit_code is None
        process.terminate()

    assert process.exit_code is not None


@pytest.mark.asyncio
async def test_process_kill(sleep: list[Path]) -> None:
    async with Process([*sleep, "3"]) as process:
        assert process.exit_code is None
        process.kill()

    assert process.exit_code is not None


@pytest.mark.asyncio
async def test_process_close(sleep: list[Path]) -> None:
    process = await Process([*sleep, "3"], stdin=PIPE).run()
    assert process.stdin is not None
    assert process.stdout is not None
    assert process.stderr is not None
    assert process.exit_code is None
    await process.close()

    assert process.stdin.is_closing()
    assert process.exit_code is not None


@pytest.mark.asyncio
async def test_running(sleep: list[Path]) -> None:
    async with Process([*sleep, "0.5"]) as process:
        assert process.running

    assert not process.running


@pytest.mark.asyncio
async def test_exit_code(sleep: list[Path]) -> None:
    async with Process([*sleep, "0.5"]) as process:
        assert process.exit_code is None

    assert process.exit_code == 0
