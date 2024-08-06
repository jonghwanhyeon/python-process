# Running a Command

In **python-process**, you can simply run a command like `echo` using [`Process`][process.Process] class.

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        process = Process("echo 'Hello, World!'").run()
        print(process.exit_code)  # 66071 True None
        process.join()
        print(process.exit_code)  # 66071 False 0


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        process = await Process("echo 'Hello, World!'").run()
        print(process.exit_code)  # 66333 True None
        await process.join()
        print(process.exit_code)  # 66333 False 0


    if __name__ == "__main__":
        asyncio.run(main())
    ```

Even simpler, you can use [`Process`][process.Process] class as a context manager to handle the execution of the process and to clean up resources automatically:

=== "Synchronous API"

    ```python
    from process import Process


    def main() -> None:
        with Process("echo 'Hello, World!'") as process:
            print(process.id, process.running, process.exit_code)  # 64165 True None
        print(process.id, process.running, process.exit_code)  # 64165 False 0


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio

    from process.asyncio import Process


    async def main() -> None:
        async with Process("echo 'Hello, World!'") as process:
            print(process.id, process.running, process.exit_code)  # 64395 True None
        print(process.id, process.running, process.exit_code)  # 64395 False 0


    if __name__ == "__main__":
        asyncio.run(main())
    ```

If you need to run a command with complex arguments, you can provide them as a [`list`][list] of [`str`][str] or [`Path`][pathlib.Path].

=== "Synchronous API"

    ```python
    from pathlib import Path

    from process import Process


    def main() -> None:
        with Process(["ls", Path.cwd()]) as process:
            print(process.id, process.running, process.exit_code)  # 67129 True None
        print(process.id, process.running, process.exit_code)  # 67129 False 0


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio
    from pathlib import Path

    from process.asyncio import Process


    async def main() -> None:
        async with Process(["ls", Path.cwd()]) as process:
            print(process.id, process.running, process.exit_code)  # 67381 True None
        print(process.id, process.running, process.exit_code)  # 67381 False 0


    if __name__ == "__main__":
        asyncio.run(main())
    ```