# Sending Inputs

You can interact with a process that expects input data, like the `cat` command, by writing to its standard input stream.

Simply, you can send input directly from a memory buffer to a process by creating the [`Process`][process.Process] with `stdin=inputs`.

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with Process(["cat"], stdin=b"Hello, stdin from buffer!") as process:
            print(process.output())  # b'Hello, stdin from buffer!'


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        async with Process(["cat"], stdin=b"Hello, stdin from buffer!") as process:
            print(async process.output())  # b'Hello, stdin from buffer!'


    if __name__ == "__main__":
        asyncio.run(main())
    ```

You can also create a [`Process`][process.Process] with `stdin=PIPE` (which is the default) and write inputs to the stream.

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with Process(["cat"]) as process:
            process.stdin.write(b"Hello, stdin from stream!")
        # Use `output()` outside the context manager to ensure the standard input stream is closed
        print(process.output())  # b'Hello, stdin from stream!'


    if __name__ == "__main__":
        main()

    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        async with Process(["cat"]) as process:
            process.stdin.write(b"Hello, stdin from stream!")
            await process.stdin.drain()
        # Use `output()` outside the context manager to ensure the standard input stream is closed
        print(await process.output())  # b'Hello, stdin from stream!'


    if __name__ == "__main__":
        asyncio.run(main())
    ```

For a more complicated case, you can send input to a process from a file by creating a [`Process`][process.Process] with `stdin=file`.

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with open("assets/lorem-ipsum.txt", "rb") as input_file:
            with Process(["cat"], stdin=input_file) as process:
                print(process.output())  # b'Lorem ipsum odor amet, consectetuer adipiscing elit.'


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        with open("assets/lorem-ipsum.txt", "rb") as input_file:
            async with Process(["cat"], stdin=input_file) as process:
                print(await process.output())  # b'Lorem ipsum odor amet, consectetuer adipiscing elit.'


    if __name__ == "__main__":
        asyncio.run(main())
    ```