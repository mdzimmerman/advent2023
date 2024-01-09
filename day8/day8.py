import argparse
from functools import reduce
import itertools
import logging
from math import gcd
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

def is_start_part1(node):
    return (node == 'AAA')

def is_end_part1(node):
    return (node == 'ZZZ')

def traverse(dirs, nodes, start, end_func, times):
    currnode = start
    steps = 0
    diriter = itertools.cycle(dirs)
    t = 0
    steps0 = 0
    while t < times:
        dir = next(diriter)
        nextnode = nodes[currnode].get(dir)
        steps += 1
        logging.debug(f"{currnode} ({dir}) -> {nextnode}")
        if end_func(nextnode):
            t += 1
            print(steps, steps-steps0, factors(steps))
            steps0 = steps
        currnode = nextnode
    return steps

def traverse2(dirs, nodes):
    currnodes = list(filter(lambda s: s[-1] == 'A', nodes))
    for c in currnodes:
        print(c)
        traverse(dirs, nodes, c, lambda e: e[-1] == 'Z', 3)
    steps = [traverse(dirs, nodes, c, lambda e: e[-1] == 'Z', 1) for c in currnodes]
    print(lcm(steps))

def lcm(xs):
    return reduce(lambda a, b: a * b // gcd(a, b), xs)

def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def main(args):
    inp = aoc.split_xs(aoc.read_lines(args.filename), "")
    dirs = inp[0][0]
    nodes = dict()
    for s in inp[1]:
        key, node = Node.parse(s)
        nodes[key] = node
    traverse2(dirs, nodes)
    #print(f"{traverse(dirs, nodes, lambda s: s[-1] == 'A', lambda e: e[-1] == 'Z')}")

    #for k, v in nodes.items():
    #    if re.match("..[AZ]", k):
    #        print(k)


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