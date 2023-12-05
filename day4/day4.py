import argparse
import re
import sys

sys.path.append("..")
import aoc

class Card:
    pattern = re.compile(r"Card +(\d+): (.+) \| (.+)")

    def __init__(self, line):
        m = self.__class__.pattern.match(line)
        if not m:
            raise Exception(f"bad input: {line}")
        self.n = int(m.group(1))
        self.allwinners = set(int(x) for x in m.group(2).strip().split())
        self.assigned = set(int(x) for x in m.group(3).strip().split())
        self.winners = self.assigned.intersection(self.allwinners)
        self.nwinners = len(self.winners)

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
            f"n={self.n} allwinners={self.allwinners} " \
            f"assigned={self.assigned} winners={self.winners} " \
            f"nwinners={self.nwinners})"

    def score(self):
        if self.nwinners > 0:
            return 2 ** (self.nwinners-1)
        else:
            return 0

    @classmethod
    def read_file(cls, filename):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                out.append(Card(l))
        return out


def main(args):
    part1 = 0
    cards = Card.read_file(args.filename)
    for c in cards:
        score = c.score()
        #print(card, score)
        part1 += score
    print(f"part1 = {part1}")

    ncards = dict()
    for c in cards:
        ncards[c.n] = 1
    for i in sorted(ncards.keys()):
        nwinners = cards[i-1].nwinners
        for j in range(i+1, i+nwinners+1):
            ncards[j] += ncards[i]
    #print(ncards)
    print(f"part2 = {sum(ncards.values())}")

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")

    args = parser.parse_args(["-f", "input.txt"])
    main(args)