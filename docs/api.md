# API Reference

## ::: process
    options:
      members:
        - Process

### ::: process.types
    options:
      members:
        - StreamReader
        - StreamWriter

## ::: process.asyncio
    options:
      show_root_full_path: true
      members:
        - Process

### ::: process.asyncio.types
    options:
      members:
        - StreamReader
        - StreamWriter

## ::: process.core
    options:
      members:
        - AbstractProcess
        - ProcessProtocol

### ::: process.core.types
    options:
      members:
        - StrOrPath
        - Buffer
        - File

## ⚠️ Errors
### ::: process.core.errors
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members:
        - ProcessError
        - ProcessNotRunError
        - ProcessAlreadyRunError
        - ProcessInvalidStreamError
        - ProcessTimeoutError

## 🔢 Constants
### ::: process.core.constants
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members:
        - PIPE
        - STDOUT
        - DEVNULL

### ::: process.constants
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members:
        - DEFAULT_BUFFER_SIZE

### ::: process.asyncio
    options:
      members:
        - DEFAULT_BUFFER_SIZE