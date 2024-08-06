from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Generator

import pytest

from process.utils import is_windows

tests_path = Path(__file__).parent.absolute()
sys.path.append(str(tests_path))


@pytest.fixture
def assets_path() -> Path:
    return tests_path / "assets"


if (sys.version_info.major, sys.version_info.minor) == (3, 7):

    @pytest.fixture(scope="module")
    def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
        policy = asyncio.get_event_loop_policy()
        if is_windows():
            policy = asyncio.WindowsProactorEventLoopPolicy()  # type: ignore

        loop = policy.new_event_loop()
        yield loop
        loop.close()


@pytest.fixture
def cat() -> list[Path]:
    return [
        Path(sys.executable).absolute(),
        tests_path / "utils" / "cat.py",
    ]


@pytest.fixture
def echo() -> list[Path]:
    return [
        Path(sys.executable).absolute(),
        tests_path / "utils" / "echo.py",
    ]


@pytest.fixture
def echo_error() -> list[Path]:
    return [
        Path(sys.executable).absolute(),
        tests_path / "utils" / "echo-error.py",
    ]


@pytest.fixture
def lazy_echo() -> list[Path]:
    return [
        Path(sys.executable).absolute(),
        tests_path / "utils" / "lazy-echo.py",
    ]


@pytest.fixture
def ls() -> list[Path]:
    return [
        Path(sys.executable).absolute(),
        tests_path / "utils" / "ls.py",
    ]


@pytest.fixture
def sleep() -> list[Path]:
    return [
        Path(sys.executable).absolute(),
        tests_path / "utils" / "sleep.py",
    ]
