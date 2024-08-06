# Overview
**python-process** is a Python package that provides a simple and intuitive interface for spawning, managing, and interacting with processes.

## Install
To install **python-process**, simply use pip:

```console
$ pip install python-process
```

## Usage

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with Process("echo 'Hello World!'") as process:
            print(process.output())  #  b'Hello World!\n'


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        async with Process("echo 'Hello World!'") as process:
            print(await process.output())  # b'Hello World!\n'


    if __name__ == "__main__":
        asyncio.run(main())
    ```