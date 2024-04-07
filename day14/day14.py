import argparse
import sys

sys.path.append("..")
import aoc
from aoc import Point

class Dish:
    def __init__(self, rounds, cubes, width, height):
        self.rounds = rounds
        self.cubes  = cubes
        self.width  = width
        self.height = height

    def show(self):
        out = ""
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p in self.cubes:
                    out += "#"
                elif p in self.rounds:
                    out += "O"
                else:
                    out += "."
            out += "\n"
        return out

    def load(self):
        for y in range(self.height)

    @classmethod
    def from_file(cls, filename):
        rounds = set()
        cubes = set()
        lines = aoc.read_lines(filename)
        height = len(lines)
        width = len(lines[0])
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    cubes.add(Point(x, y))
                elif c == "O":
                    rounds.add(Point(x, y))
        return cls(rounds, cubes, width, height)

    def slide_north(self):
        ndish = Dish(set(), self.cubes, self.width, self.height)
        for r in sorted(self.rounds, key=lambda p: p.y):
            stopped = False
            rcurr = Point(r.x, r.y)
            while not stopped:
                rnext = Point(rcurr.x, rcurr.y-1)
                if rcurr.y > 0 and rnext not in ndish.rounds and rnext not in ndish.cubes:
                    rcurr = rnext
                else:
                    stopped = True
            ndish.rounds.add(rcurr)
        return ndish
def main(args):
    dish = Dish.from_file(args.filename)
    print(dish.show())
    print()
    print(dish.slide_north().show())

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args("-f test.txt".split())

    # parse logging level
    main(args)