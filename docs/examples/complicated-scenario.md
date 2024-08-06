# Complicated Scenario

Let's explore a complicated scenario where you can use the [`Process`][process.Process] class to manage and interact with a process.

For this scenario, create a simple Python script named `greedy_cat.py` similar to `cat`, but it outputs its inputs to both the standard output and standard error.

```python title="greedy_cat.py"
import fileinput
import sys

if __name__ == "__main__":
    for line in fileinput.input():
        print(line, end="", file=sys.stdout)
        print(line, end="", file=sys.stderr)
```

Assume you have an input file `lorem-ipsum.txt` with the following content:

``` title="lorem-ipsum.txt"
Lorem ipsum odor amet, consectetuer adipiscing elit.
```

Then, you can create a [`Process`][process.Process] instance that reads from this file as `stdin` and uses the `greedy_cat.py` script as follows:

=== "Synchronous API"

    ```python
    import sys

    from process import Process


    def main() -> None:
        with open("lorem-ipsum.txt", "rb") as input_file:
            with Process([sys.executable, "greedy_cat.py"], stdin=input_file) as process:
                print(process.output())  # b'Lorem ipsum odor amet, consectetuer adipiscing elit.'
                print(process.error())  # b'Lorem ipsum odor amet, consectetuer adipiscing elit.'


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio
    import sys

    from process.asyncio import Process


    async def main() -> None:
        with open("lorem-ipsum.txt", "rb") as input_file:
            async with Process([sys.executable, "greedy_cat.py"], stdin=input_file) as process:
                print(await process.output())  # b'Lorem ipsum odor amet, consectetuer adipiscing elit.'
                print(await process.error())  # b'Lorem ipsum odor amet, consectetuer adipiscing elit.'


    if __name__ == "__main__":
        asyncio.run(main())
    ```

Next, let's redirect the standard error to the standard output by creating a [`Process`][process.Process] instance with `stderr=STDOUT`.

=== "Synchronous API"

    ```python
    import sys

    from process import STDOUT, Process


    def main() -> None:
        with open("lorem-ipsum.txt", "rb") as input_file:
            with Process([sys.executable, "greedy_cat.py"], stdin=input_file, stderr=STDOUT) as process:
                # b'Lorem ipsum odor amet, consectetuer adipiscing elit.Lorem ipsum odor amet, consectetuer adipiscing elit.'
                print(process.output())


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio
    import sys

    from process import STDOUT
    from process.asyncio import Process


    async def main() -> None:
        with open("lorem-ipsum.txt", "rb") as input_file:
            async with Process([sys.executable, "greedy_cat.py"], stdin=input_file, stderr=STDOUT) as process:
                # b'Lorem ipsum odor amet, consectetuer adipiscing elit.Lorem ipsum odor amet, consectetuer adipiscing elit.'
                print(await process.output())


    if __name__ == "__main__":
        asyncio.run(main())
    ```

Lastly, let's redirect the standard output to a file by creating a [`Process`][process.Process] instance with `stdout=file`.

=== "Synchronous API"

    ```python
    import sys

    from process import STDOUT, Process


    def main() -> None:
        with open("lorem-ipsum.txt", "rb") as input_file:
            with open("output.txt", "w+b") as output_file:
                with Process([sys.executable, "greedy_cat.py"], stdin=input_file, stdout=output_file, stderr=STDOUT):
                    pass

                output_file.seek(0)
                # b'Lorem ipsum odor amet, consectetuer adipiscing elit.Lorem ipsum odor amet, consectetuer adipiscing elit.'
                print(output_file.read())


    if __name__ == "__main__":
        main()
    ```

=== "Asynchronous API"

    ```python
    import asyncio
    import sys

    from process import STDOUT
    from process.asyncio import Process


    async def main() -> None:
        with open("lorem-ipsum.txt", "rb") as input_file:
            with open("output.txt", "w+b") as output_file:
                async with Process([sys.executable, "greedy_cat.py"], stdin=input_file, stdout=output_file, stderr=STDOUT):
                    pass

                output_file.seek(0)
                # b'Lorem ipsum odor amet, consectetuer adipiscing elit.Lorem ipsum odor amet, consectetuer adipiscing elit.'
                print(output_file.read())


    if __name__ == "__main__":
        asyncio.run(main())
    ```