from io import BufferedReader, BufferedWriter, FileIO
from typing import Union

from typing_extensions import TypeAlias

# According to the documentation for [`Popen.stdin`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/subprocess.rst?plain=1#L892)
# > If the *stdin* argument was :data:`PIPE`, this attribute is a writeable stream object as returned by :func:`open`.
# According to the documentation for [`open`](https://github.com/python/cpython/blob/8f19be47b6a50059924e1d7b64277ad3cef4dac7/Doc/library/functions.rst?plain=1#L1418)
# > When used to open a file in a binary mode with buffering, the returned class is a subclass of :class:`io.BufferedIOBase`.
# > The exact class varies: in read binary mode, it returns an :class:`io.BufferedReader`;
# > in write binary and append binary modes, it returns an :class:`io.BufferedWriter`, and
# > in read/write mode, it returns an :class:`io.BufferedRandom`.
# > When buffering is disabled, the raw stream, a subclass of :class:`io.RawIOBase`, :class:`io.FileIO`, is returned.
StreamWriter: TypeAlias = Union[FileIO, BufferedWriter]
StreamReader: TypeAlias = Union[FileIO, BufferedReader]
