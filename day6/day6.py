import argparse
from functools import reduce
import logging
import sys

sys.path.append("..")
import aoc

def read_input(filename):
    lines = aoc.read_lines(filename)
    ts = [int(t) for t in (lines[0].split())[1:]]
    ds = [int(d) for d in (lines[1].split())[1:]]
    return ts, ds

def max_distance(tmax: int, distance_record: int):
    wins = 0
    for t in range(tmax):
        tleft = tmax - t
        dist = tleft * t
        logging.debug(f"{t} {dist}")
        if dist > distance_record:
            wins += 1
    return wins

def product(xs):
    return reduce(lambda a, b: a * b, xs, 1)

def main(args):
    ts, ds = read_input(args.filename)


    logging.info(f"{ts}")
    logging.info(f"{ds}")
    nwins = []
    for t, d in zip(ts, ds):
        nwins.append(max_distance(t, d))
    logging.info(f"{nwins}")
    print(f"part1 = {product(nwins)}")


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args(["-f", "input.txt"])

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel, stream=sys.stdout)

    main(args)