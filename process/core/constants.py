import subprocess

PIPE = subprocess.PIPE
"""Special value that can be used as the `stdin`, `stdout`, or `stderr` argument to indicate that a pipe to the standard stream should be opened."""

STDOUT = subprocess.STDOUT
"""Special value that can be used as the `stderr` argument to indicate that standard error should be redirected to standard output."""

DEVNULL = subprocess.DEVNULL
"""Special value that can be used as the `stdin`, `stdout`, or `stderr` argument to indicate that the special file [`os.devnull`][os.devnull] should be used."""
