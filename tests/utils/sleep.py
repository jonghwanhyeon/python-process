import argparse
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("time", type=float)

    arguments = parser.parse_args()

    time.sleep(arguments.time)
