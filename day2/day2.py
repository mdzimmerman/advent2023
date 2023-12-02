import argparse
from collections import defaultdict
from functools import reduce
import logging
import re
import sys

sys.path.append("..")
import aoc

linepatt = re.compile(r'Game (\d+): (.+)');

def parse(s):
    d = defaultdict(int)
    for e in s.split(', '):
        n, color = e.split()
        d[color] = int(n)
    return d

def main(args):
    p1total = 0
    p2total = 0
    with open(args.filename, "r") as fh:
        for l in fh:
            l = l.strip()
            m = linepatt.match(l)
            if m:
                valid = True
                id = int(m.group(1))
                es = m.group(2)
                ds = [parse(e) for e in es.split('; ')]
                dmax = {'red': 0, 'green': 0, 'blue': 0}
                for d in ds:
                    if d['red'] > 12 or d['green'] > 13 or d['blue'] > 14:
                        valid = False
                    for c in ['red', 'green', 'blue']:
                        if d[c] > dmax[c]:
                            dmax[c] = d[c]
                power = reduce(lambda x, y: x * y, dmax.values())
                logging.debug(f"{id} {ds} {valid} {power}")
                if valid:
                    p1total += id
                p2total += power
    print(f"Part 1 = {p1total}")
    print(f"Part 2 = {p2total}")

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args()

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel)

    main(args)