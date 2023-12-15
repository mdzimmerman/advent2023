import argparse
import itertools
import logging
import re
import sys
from dataclasses import dataclass

sys.path.append("..")
import aoc

@dataclass
class Node:
    left: str
    right: str

    pattern = re.compile(r"(.+) = \((.+), (.+)\)")

    def get(self, dir):
        if dir == 'L':
            return self.left
        elif dir == 'R':
            return self.right
        else:
            return None

    @classmethod
    def parse(cls, s):
        m = cls.pattern.match(s)
        if m:
            key = m.group(1)
            node = cls(m.group(2), m.group(3))
            return key, node
        else:
            return None

def traverse(dirs, nodes, start="AAA", end="ZZZ"):
    currnode = start
    steps = 0
    diriter = itertools.cycle(dirs)
    while currnode != end:
        dir = next(diriter)
        nextnode = nodes[currnode].get(dir)
        steps += 1
        logging.debug(f"{currnode} ({dir}) -> {nextnode}")
        currnode = nextnode
    return steps

def main(args):
    inp = aoc.split_xs(aoc.read_lines(args.filename), "")
    dirs = inp[0][0]
    nodes = dict()
    for s in inp[1]:
        key, node = Node.parse(s)
        nodes[key] = node
    #print(f"part1 = {traverse(dirs, nodes, 'AAA', 'ZZZ')}")

    for k, v in nodes.items():
        if re.match("..[AZ]", k):
            print(k)


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args("-f input.txt -l info".split())

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel, stream=sys.stdout)

    main(args)