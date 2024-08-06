import sys
import time

if __name__ == "__main__":
    arguments = sys.argv[1:]

    time.sleep(1.0)
    print(*arguments)
