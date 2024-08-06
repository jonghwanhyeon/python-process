import sys

if __name__ == "__main__":
    arguments = sys.argv[1:]
    print(*arguments, file=sys.stderr)
