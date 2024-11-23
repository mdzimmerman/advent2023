import argparse
from dataclasses import dataclass
import logging
import re
import sys

sys.path.append("..")
import aoc

@dataclass
class Rule:
    prop: str
    op: str
    value: int
    dest: str

    PATTERN = re.compile(r"(\w+)([<>])(\d+):(.+)")

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            return cls(m.group(1), m.group(2), int(m.group(3)), m.group(4))

@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    altdest: str

    PATTERN = re.compile(r"(\w+){(.+),(\w+)}")

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            name = m.group(1)
            rules = [Rule.parse(r) for r in m.group(2).split(",")]
            altdest = m.group(3)
            return cls(name, rules, altdest)

class Part:
    PATTERN_BASE = re.compile(r"{(.+)}")
    PATTERN_ELEM = re.compile(r"(\w+)=(\d+)")

    @classmethod
    def parse(cls, s):
        mb = cls.PATTERN_BASE.match(s)
        if mb:
            out = dict()
            for xs in mb.group(1).split(","):
                mx = cls.PATTERN_ELEM.match(xs)
                if mx:
                    out[mx.group(1)] = int(mx.group(2))
            return out
def main(args):
    print(args)

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
    logging.basicConfig(level=loglevel, stream=sys.stdout)

    main(args)