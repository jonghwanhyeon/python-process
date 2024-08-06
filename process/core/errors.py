class ProcessError(Exception):
    """Base class for exceptions related to process errors."""


class ProcessNotRunError(ProcessError):
    """Exception raised when a process has not been run."""


class ProcessAlreadyRunError(ProcessError):
    """Exception raised when the process has already been run."""


class ProcessInvalidStreamError(ProcessError):
    """Exception raised when an invalid stream is encountered in the process."""


class ProcessTimeoutError(ProcessError):
    """Exception raised when the process times out."""
