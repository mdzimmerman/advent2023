import argparse
import itertools
import logging
import re
import sys

sys.path.append("..")
import aoc

def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def predict(xs, dir=1):
    dxs = []
    dxs.append(xs)
    while any(x != 0 for x in dxs[-1]):
        dxs.append([b-a for a, b in pairwise(dxs[-1])])

    if dir == 1:
        dxs[-1].append(0)
        for j in reversed(range(len(dxs)-1)):
            i = len(dxs[j])
            dxs[j].append(dxs[j+1][i-1] + dxs[j][i-1])
    else:
        for dx in dxs:
            dx.reverse()
        dxs[-1].append(0)
        for j in reversed(range(len(dxs)-1)):
            i = len(dxs[j])
            dxs[j].append(dxs[j][i-1] - dxs[j+1][i-1])

    for dx in dxs:
        print(dx)
    print(dxs[0][-1])
    print()
    return (dxs[0][-1])

def main(args):
    data = []
    for l in aoc.read_lines(args.filename):
        data.append([int(x) for x in l.split()])

    print(sum(predict(xs, dir=-1) for xs in data))


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args("-f input.txt".split())

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel, stream=sys.stdout)

    main(args)