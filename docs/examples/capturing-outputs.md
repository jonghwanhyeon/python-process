# Capturing Outputs

You can capture the standard output of a process by creating the [`Process`][process.Process] with `stdout=PIPE` (which is the default) and using the [`output()`][process.Process.output] method.

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with Process(["echo", "Hello, stdout!"]) as process:
            print(process.output())  # b'Hello, stdout!\n'


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        async with Process(["echo", "Hello, stdout!"]) as process:
            print(await process.output())  # b'Hello, stdout!\n'


    if __name__ == "__main__":
        asyncio.run(main())
    ```

Similarly, you can capture the standard error of a process by creating the [`Process`][process.Process] with `stderr=PIPE` (which is also the default) and using the [`error()`][process.Process.error] method.

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with Process(["ls", "non-existent-file"]) as process:
            print(process.output())  # b''
            print(process.error())  # b'ls: non-existent-file: No such file or directory\n'


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        async with Process(["ls", "non-existent-file"]) as process:
            print(await process.output())  # b''
            print(await process.error())  # b'ls: non-existent-file: No such file or directory\n'


    if __name__ == "__main__":
        asyncio.run(main())
    ```