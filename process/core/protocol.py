from __future__ import annotations

import asyncio
import subprocess
import sys
from typing import TYPE_CHECKING, Optional, Sequence, TypeVar, Union

from typing_extensions import Protocol, Self, overload

from process.core.constants import PIPE
from process.core.types import File, Returns, StrOrPath

if TYPE_CHECKING:
    from process.asyncio.types import StreamReader as AsyncStreamReader
    from process.asyncio.types import StreamWriter as AsyncStreamWriter
    from process.types import StreamReader, StreamWriter


W_co = TypeVar("W_co", "StreamWriter", "AsyncStreamWriter", covariant=True)
R_co = TypeVar("R_co", "StreamReader", "AsyncStreamReader", covariant=True)


class ProcessProtocol(Protocol[W_co, R_co]):
    """A protocol that defines the interface for spawning and managing a process."""

    @overload
    def __init__(
        self,
        arguments: StrOrPath,
        stdin: Optional[Union[bytes, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        arguments: Sequence[StrOrPath],
        stdin: Optional[Union[bytes, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None: ...

    def __init__(
        self,
        arguments: Union[StrOrPath, Sequence[StrOrPath]],
        stdin: Optional[Union[bytes, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None:
        """Initialize a new `Process` instance with the given `arguments`.

        Args:
            arguments: The command and its arguments for the process.
            stdin: A [`bytes`][bytes] object containing the input data, an existing file descriptor, an existing file object with a valid file descriptor, or special value ([`None`][None], [`PIPE`][process.PIPE], and [`DEVNULL`][process.DEVNULL]) to use as the standard input.
            stdout: An existing file descriptor, an existing file object with a valid file descriptor, or special value ([`None`][None], [`PIPE`][process.PIPE], and [`DEVNULL`][process.DEVNULL]) to use as the standard output.
            stderr: An existing file descriptor, an existing file object with a valid file descriptor, or special value ([`None`][None], [`PIPE`][process.PIPE], [`DEVNULL`][process.DEVNULL], and [`STDOUT`][process.STDOUT]) to use as the standard error.
            buffer_size: The buffer size for the stream operations. If `None`, the default buffer size will be used. If `0`, all operations will be unbuffered.

        Notes:
            If `arguments` is an instance of [`str`][str], it will be split into a list of arguments using [`shlex.split()`][shlex.split].

        Warning:
            A file-like object without a valid file descriptor, such as [`BytesIO`][io.BytesIO], cannot be used as `stdin`, `stdout`, or `stderr`.
        """
        ...

    def __del__(self) -> None:
        """Clean up resources used by the process."""
        ...

    @property
    def arguments(self) -> list[str]:
        """Return the command-line arguments provided to create this `Process` instance.

        Returns:
            The command-line arguments provided to create this `Process` instance.
        """
        ...

    if sys.version_info >= (3, 9):

        @property
        def process(self) -> Union[subprocess.Popen[bytes], asyncio.subprocess.Process]:
            """Return the underlying process instance.

            Returns:
                An instance of either [`subprocess.Popen`][subprocess.Popen] or [`asyncio.subprocess.Process`][asyncio.subprocess.Process].

            Raises:
                ProcessNotRunError: If the process has not been run.
            """
            ...
    else:

        @property
        def process(self) -> Union[subprocess.Popen, asyncio.subprocess.Process]:
            """Return the underlying process instance.

            Returns:
                An instance of either [`subprocess.Popen`][subprocess.Popen] or [`asyncio.subprocess.Process`][asyncio.subprocess.Process].

            Raises:
                ProcessNotRunError: If the process has not been run.
            """
            ...

    @property
    def id(self) -> int:
        """Return the process identifier.

        Returns:
            The process identifier.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    @property
    def running(self) -> bool:
        """Check if the process is currently running.

        Returns:
            `True` if the process is running, `False` otherwise.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    @property
    def exit_code(self) -> Optional[int]:
        """Return the exit code of the process.

        Returns:
            The exit code of the process. If the process is still running, it returns `None`.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    def run(self) -> Returns[Self]:
        """Run the process.

        Returns:
            The current `Process` instance itself.

        Raises:
            ProcessAlreadyRunError: If the process has already been run.
            ProcessError: If the process fails to run.
        """
        ...

    def output(self, join: bool = True) -> Returns[bytes]:
        """Return the output from the standard output stream of the process if the process was created with `stdout=PIPE`.

        Args:
            join: Whether to wait for the process to complete before returning the output.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        ...

    def error(self, join: bool = True) -> Returns[bytes]:
        """Return the output from the standard error stream of the process if the process was created with `stderr=PIPE`.

        Args:
            join: Whether to wait for the process to complete before returning the output.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        ...

    def join(self, timeout: Optional[float] = None) -> Returns[None]:
        """Wait for the process to complete.

        Args:
            timeout: Maximum time to wait for the process to complete, in seconds. If `None`, wait indefinitely.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessTimeoutError: If the process does not complete within the specified timeout.
        """
        ...

    def signal(self, signal: int) -> None:
        """Send a signal to the process.

        Args:
            signal: The signal number to send.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    def terminate(self) -> None:
        """Gracefully terminate the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    def kill(self) -> None:
        """Forcefully kill the process.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        ...

    def close(self) -> Returns[None]:
        """Close the process and release its resources.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """

    @property
    def stdin(self) -> W_co:
        """Return the standard input stream of the process.

        Returns:
            The standard input stream of the process if the process was created with `stdin=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdin=PIPE`.
        """
        ...

    @property
    def stdout(self) -> R_co:
        """Return the standard output stream of the process.

        Returns:
            The standard output stream of the process if the process was created with `stdout=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        ...

    @property
    def stderr(self) -> R_co:
        """Return the standard error stream of the process.

        Returns:
            The standard error stream of the process if the process was created with `stderr=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        ...
