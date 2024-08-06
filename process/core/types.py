import os
import sys
from typing import IO, Any, Coroutine, TypeVar, Union

from typing_extensions import TypeAlias

T = TypeVar("T")

Returns: TypeAlias = Union[T, Coroutine[Any, Any, T]]

if sys.version_info >= (3, 9):
    PathLike = os.PathLike[str]
else:
    PathLike = os.PathLike

StrOrPath: TypeAlias = Union[str, PathLike]

# Reference: https://github.com/python/typeshed/blob/0fd6cd211f9f8b17d6b3960ff96051ec89fb908c/stdlib/subprocess.pyi#L65
File: TypeAlias = Union[int, IO[bytes]]
