import argparse
from functools import reduce
import logging
import math
import sys


sys.path.append("..")
import aoc

def read_input(filename):
    lines = aoc.read_lines(filename)
    ts = [int(t) for t in (lines[0].split())[1:]]
    ds = [int(d) for d in (lines[1].split())[1:]]
    return ts, ds

def read_input2(filename):
    lines = aoc.read_lines(filename)
    t = int("".join((lines[0].split())[1:]))
    d = int("".join((lines[1].split())[1:]))
    return t, d

def part1_wins(tmax: int, distance_record: int):
    wins = 0
    for t in range(tmax):
        tleft = tmax - t
        dist = tleft * t
        logging.debug(f"{t} {dist}")
        if dist > distance_record:
            wins += 1
    return wins

def part2_wins(T: int, D: int):
    pred = math.sqrt(T*T - 4 * D)
    logging.info(pred)
    wmin = (T - pred)/2
    wmax = (T + pred)/2
    logging.info(f"{wmin} {wmax}")

    return math.floor(wmax) - math.ceil(wmin) + 1

def product(xs):
    return reduce(lambda a, b: a * b, xs, 1)

def main(args):
    ts, ds = read_input(args.filename)

    print("-- part 1 --")
    logging.info(f"{ts}")
    logging.info(f"{ds}")
    nwins = []
    for t, d in zip(ts, ds):
        nwins.append(part1_wins(t, d))
    logging.info(f"{nwins}")
    print(f"{product(nwins)}")

    print("-- part 2 --")
    t, d = read_input2(args.filename)
    logging.info(f"{t} {d}")
    print(f"{part2_wins(t, d)}")


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