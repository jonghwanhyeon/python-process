# python-process
![Build status](https://github.com/jonghwanhyeon/python-process/actions/workflows/publish.yml/badge.svg)

A Python package that provides a simple and intuitive interface for spawning, managing, and interacting with processes.

## Help
See [documentation](https://python-process.readthedocs.io) for more details

## Install
To install **python-process**, simply use pip:

```console
$ pip install python-process
```

## Usage
You can find more examples in [the documentation](https://python-process.readthedocs.io/examples/running-command/).

### Synchronous API
```python
from process import Process


def main() -> None:
    with Process("echo 'Hello World!'") as process:
        print(process.output())  #  b'Hello World!\n'


if __name__ == "__main__":
    main()
```

### Asynchronous API
```python
import asyncio

from process.asyncio import Process


async def main() -> None:
    async with Process("echo 'Hello World!'") as process:
        print(await process.output())  # b'Hello World!\n'


if __name__ == "__main__":
    asyncio.run(main())
```