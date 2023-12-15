import argparse
from collections import namedtuple
from functools import total_ordering
import logging
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

    JOKER_CARDRANKS = CARDRANKS.copy()
    JOKER_CARDRANKS["J"] = 1

    def __init__(self, hand, joker=False):
        self.hand     = hand
        self.joker    = joker
        self.typecode = self._build_typecode()
        self.rank     = self._calc_rank()

    def _build_typecode(self):
        d = dict()
        jokers = 0
        for c in self.hand:
            if self.joker and c == 'J':
                jokers += 1
            else:
                if c not in d:
                    d[c] = 0
                d[c] += 1
        counts = sorted(d.values(), reverse=True)
        if jokers == 5:
            return "5"
        else:
            counts[0] += jokers
            return "".join(str(i) for i in counts)

    def _calc_rank(self):
        cls = self.__class__
        cardranks = None
        if self.joker:
            cardranks = cls.JOKER_CARDRANKS
        else:
            cardranks = cls.CARDRANKS
        rank = 0
        rank += cls.TYPERANKS[self.typecode] * (10**10)
        for i in range(5):
            rank += cardranks[self.hand[i]] * (10**(2*(4-i)))
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

def play_game(filename, joker=False):
    lines = aoc.read_lines(filename)
    inputs = []
    for l in lines:
        ls = l.split()
        inputs.append(Input(Hand(ls[0], joker=joker), int(ls[1])))

    #for i, x in enumerate(inputs):
    #    for j, y in enumerate(inputs[i:]):
    #        logging.debug(f"{x.hand} < {y.hand}: {x.hand < y.hand}")

    total = 0
    for i, inp in enumerate(sorted(inputs, key=lambda x: x.hand)):
        logging.debug(inp)
        total += (i+1) * inp.bid
    return total

def main(args):
    print(f"part1 = {play_game(args.filename, joker=False)}")
    print(f"part2 = {play_game(args.filename, joker=True)}")


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