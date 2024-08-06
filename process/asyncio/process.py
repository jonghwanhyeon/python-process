from __future__ import annotations

import asyncio
import subprocess
import sys
from contextlib import suppress
from types import TracebackType
from typing import Optional, Sequence, Union, cast

from typing_extensions import Self

from process.asyncio.constants import DEFAULT_BUFFER_SIZE
from process.asyncio.types import StreamReader, StreamWriter
from process.core.constants import PIPE
from process.core.errors import (
    ProcessAlreadyRunError,
    ProcessError,
    ProcessInvalidStreamError,
    ProcessNotRunError,
    ProcessTimeoutError,
)
from process.core.process import AbstractProcess
from process.core.types import File, StrOrPath
from process.utils import is_windows

if sys.version_info < (3, 11):
    from asyncio import TimeoutError as TimeoutError


class Process(AbstractProcess[StreamWriter, StreamReader]):
    """A class for spawning, managing, and interacting with a process asynchronously.

    This class provides a convenient interface for running a process, interacting with its standard input, output, and error streams, and managing its execution.
    """

    def __init__(
        self,
        arguments: Union[StrOrPath, Sequence[StrOrPath]],
        stdin: Optional[Union[bytes, File]] = None,
        stdout: Optional[File] = PIPE,
        stderr: Optional[File] = PIPE,
        buffer_size: Optional[int] = None,
    ) -> None:
        """Initialize a new [`Process`][process.asyncio.Process] instance with the given `arguments`.

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
        if buffer_size is None:
            buffer_size = DEFAULT_BUFFER_SIZE

        super().__init__(arguments, stdin=stdin, stdout=stdout, stderr=stderr, buffer_size=buffer_size)

    def __del__(self) -> None:
        """Clean up resources used by the process.

        This method cleans up resources as follows:

        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        - If the process is running, terminate the process.
        """
        if self._process is None:
            return

        with suppress(ProcessInvalidStreamError):
            # Since we are cleaning up, suppress errors from closing the standard input stream by following the approach in
            # https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Lib/subprocess.py#L1097
            with suppress(BrokenPipeError, ConnectionResetError):
                if not self.stdin.is_closing():
                    self.stdin.close()

        if self.running:
            self.terminate()

    @property
    def process(self) -> asyncio.subprocess.Process:
        """Return the underlying process object.

        Returns:
            An instance of [`asyncio.subprocess.Process`][asyncio.subprocess.Process].

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        if self._process is None:
            raise ProcessNotRunError("Process has not been run")

        return cast(asyncio.subprocess.Process, self._process)

    @property
    def running(self) -> bool:
        """Check if the process is currently running.

        Returns:
            `True` if the process is running, `False` otherwise.

        Raises:
            ProcessNotRunError: If the process has not been run.
        """
        return self.process.returncode is None

    async def run(self) -> Self:
        """Run the process.

        Returns:
            The current [`Process`][process.asyncio.Process] instance itself.

        Raises:
            ProcessAlreadyRunError: If the process has already been run.
            ProcessError: If the process fails to run.
        """
        if self._process is not None:
            raise ProcessAlreadyRunError("Process has already been run")

        creationflags = 0

        # According to the documentation for [`Popen.send_signal()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L864),
        # > On Windows, ... CTRL_C_EVENT and CTRL_BREAK_EVENT can be sent to processes
        # > started with a *creationflags* parameter which includes ``CREATE_NEW_PROCESS_GROUP``.
        if is_windows():
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore

        stdin = self._stdin
        should_feed_stdin = isinstance(stdin, bytes)

        try:
            self._process = await asyncio.subprocess.create_subprocess_exec(
                *self.arguments,
                stdin=cast(File, stdin) if not should_feed_stdin else PIPE,
                stdout=self._stdout,
                stderr=self._stderr,
                limit=self._buffer_size,
                creationflags=creationflags,
            )
        except Exception as exception:
            raise ProcessError(f"Failed to run process: {exception!r}")

        if should_feed_stdin:
            # Since `Popen.communicate()` requires the process to terminate, we feed the input ourselves.
            # If deadlock issues are reported, consider using a different approach, such as threading.
            self.stdin.write(cast(bytes, stdin))
            await self.stdin.drain()

            self.stdin.close()
            # Contrary to the documentation for [`StreamWriter.wait_closed()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/asyncio-stream.rst?plain=1#L383),
            # using `wait_closed()` in Python 3.7 raises `AttributeError: 'SubprocessStreamProtocol' object has no attribute '_closed'`.
            if sys.version_info >= (3, 8):
                await self.stdin.wait_closed()

        return self

    async def output(self, join: bool = True) -> bytes:
        r"""Return the output from the standard output stream of the process if the process was created with `stdout=PIPE`.

        Warning:
            If the standard output stream of the process is modified by others, the result of [`output()`][process.asyncio.Process.output] will be affected by those changes.

            ```python
            with Process("echo something") as process:
                print(process.stdout.read(4))  # b'some'
            print(process.output())  # b'thing\n'
            ```

        Args:
            join: Whether to wait for the process to complete before returning the output.

        Returns:
            The output from the standard output stream of the process if the process was created with `stdout=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        if join:
            await self.join()

        self._output += await self.stdout.read()

        return self._output

    async def error(self, join: bool = True) -> bytes:
        """Return the output from the standard error stream of the process if the process was created with `stderr=PIPE`.

        Warning:
            If the standard error stream of the process is modified by others, the result of [`error()`][process.asyncio.Process.error] will be affected by those changes.

        Args:
            join: Whether to wait for the process to complete before returning the output.

        Returns:
            The output from the standard error stream of the process if the process was created with `stderr=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        if join:
            await self.join()

        self._error += await self.stderr.read()

        return self._error

    async def join(self, timeout: Optional[float] = None) -> None:
        """Wait for the process to complete.

        Args:
            timeout: Maximum time to wait for the process to complete, in seconds. If `None`, wait indefinitely.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessTimeoutError: If the process does not complete within the specified timeout.
        """
        try:
            await asyncio.wait_for(self.process.wait(), timeout=timeout)
        except TimeoutError:
            raise ProcessTimeoutError(f"Process did not complete within {timeout} seconds")

    async def close(self) -> None:
        """Close the process and release its resources.

        This method cleans up the process execution as follows:

        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        - If the process is running, terminate it.
        - Wait for the process to complete.
        - Read the remaining output from the standard output stream if the process was created with `stdout=PIPE`.
        - Read the remaining error from the standard error stream if the process was created with `stderr=PIPE`.
        """
        with suppress(ProcessInvalidStreamError):
            # Since we are cleaning up, suppress errors from closing the standard input stream by following the approach in
            # https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Lib/subprocess.py#L1097
            with suppress(BrokenPipeError, ConnectionResetError):
                if not self.stdin.is_closing():
                    self.stdin.close()
                    # Contrary to the documentation for [`StreamWriter.wait_closed()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/asyncio-stream.rst?plain=1#L383),
                    # using `wait_closed()` in Python 3.7 raises `AttributeError: 'SubprocessStreamProtocol' object has no attribute '_closed'`.
                    if sys.version_info >= (3, 8):
                        await self.stdin.wait_closed()

        self.terminate()
        await self.join()

        with suppress(ProcessInvalidStreamError):
            self._output += await self.stdout.read()

        with suppress(ProcessInvalidStreamError):
            self._error += await self.stderr.read()

    async def __aenter__(self) -> Self:
        """Enter the runtime context for this [`Process`][process.asyncio.Process] instance.

        This method runs the process.

        Returns:
            The current [`Process`][process.asyncio.Process] instance itself.
        """
        return await self.run()

    async def __aexit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the runtime context for this [`Process`][process.asyncio.Process] instance.

        This method cleans up the process execution as follows:

        - Close the standard input stream if the process was created with `stdin=PIPE` and the stream is not closed.
        - Wait for the process to complete.
        - Read the remaining output from the standard output stream if the process was created with `stdout=PIPE`.
        - Read the remaining error from the standard error stream if the process was created with `stderr=PIPE`.
        """
        with suppress(ProcessInvalidStreamError):
            # Since we are cleaning up, suppress errors from closing the standard input stream by following the approach in
            # https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Lib/subprocess.py#L1097
            with suppress(BrokenPipeError, ConnectionResetError):
                if not self.stdin.is_closing():
                    self.stdin.close()
                    # Contrary to the documentation for [`StreamWriter.wait_closed()`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/asyncio-stream.rst?plain=1#L383),
                    # using `wait_closed()` in Python 3.7 raises `AttributeError: 'SubprocessStreamProtocol' object has no attribute '_closed'`.
                    if sys.version_info >= (3, 8):
                        await self.stdin.wait_closed()

        if exception_type is None:
            await self.join()

        with suppress(ProcessInvalidStreamError):
            if exception_type is None:
                self._output += await self.stdout.read()

        with suppress(ProcessInvalidStreamError):
            if exception_type is None:
                self._error += await self.stderr.read()

    @property
    def stdin(self) -> StreamWriter:
        """Return the standard input stream of the process if the process was created with `stdin=PIPE`.

        Returns:
            The standard input stream of the process if the process was created with `stdin=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdin=PIPE`.
        """
        stdin = self.process.stdin

        if stdin is None:
            raise ProcessInvalidStreamError("Process was not created with `stdin=PIPE`")

        return stdin

    @property
    def stdout(self) -> StreamReader:
        """Return the standard output stream of the process if the process was created with `stdout=PIPE`.

        Returns:
            The standard output stream of the process if the process was created with `stdout=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stdout=PIPE`.
        """
        stdout = self.process.stdout

        if stdout is None:
            raise ProcessInvalidStreamError("Process was not created with `stdout=PIPE`")

        return stdout

    @property
    def stderr(self) -> StreamReader:
        """Return the standard error stream of the process if the process was created with `stderr=PIPE`.

        Returns:
            The standard error stream of the process if the process was created with `stderr=PIPE`.

        Raises:
            ProcessNotRunError: If the process has not been run.
            ProcessInvalidStreamError: If the process was not created with `stderr=PIPE`.
        """
        stderr = self.process.stderr

        if stderr is None:
            raise ProcessInvalidStreamError("Process was not created with `stderr=PIPE`")

        return stderr
