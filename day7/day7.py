import argparse
from collections import namedtuple
from functools import total_ordering
import logging
import re
import sys

sys.path.append("..")
import aoc

@total_ordering
class Hand:
    TYPERANKS = {
        "11111": 1, "2111": 2, "221": 3,
        "311":   4, "32":   5, "41":  6, "5": 7}

    CARDRANKS = {
        "2": 2,  "3": 3,  "4": 4, "5": 5,  "6": 6,
        "7": 7,  "8": 8,  "9": 9, "T": 10, "J": 11,
        "Q": 12, "K": 13, "A": 14}

    def __init__(self, hand):
        self.hand     = hand
        self.typecode = self._build_typecode()
        self.rank     = self._calc_rank()

    def _build_typecode(self):
        d = dict()
        for c in self.hand:
            if c not in d:
                d[c] = 0
            d[c] += 1
        return "".join(str(i) for i in sorted(d.values(), reverse=True))

    def _calc_rank(self):
        cls = self.__class__
        rank = 0
        rank += cls.TYPERANKS[self.typecode] * (10**10)
        for i in range(5):
            rank += cls.CARDRANKS[self.hand[i]] * (10**(2*(4-i)))
        return rank

    def __repr__(self):
        return f"{self.__class__.__name__}(hand={self.hand} typecode={self.typecode})"

    def _is_valid_operand(self, other):
        return hasattr(other, "rank")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.rank == other.rank

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.rank < other.rank

Input = namedtuple("Input", "hand bid")

def part1(inputs):
    for inp in sorted(inputs, key=lambda x: x.hand):
        pass

def main(args):
    lines = aoc.read_lines(args.filename)
    inputs = []
    for l in lines:
        ls = l.split()
        inputs.append(Input(Hand(ls[0]), int(ls[1])))

    #for i, x in enumerate(inputs):
    #    for j, y in enumerate(inputs[i:]):
    #        logging.debug(f"{x.hand} < {y.hand}: {x.hand < y.hand}")

    total = 0
    for i, inp in enumerate(sorted(inputs, key=lambda x: x.hand)):
        logging.debug(inp)
        total += (i+1) * inp.bid
    print(f"part1 = {total}")


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args(["-f", "input.txt", "-l", "info"])

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel, stream=sys.stdout)

    main(args)