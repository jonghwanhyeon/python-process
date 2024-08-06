import sys


def is_windows() -> bool:
    """
    Check if the operating system is Windows.

    Returns:
        `True` if the operating system is Windows, `False` otherwise.
    """
    return sys.platform == "win32"
