import argparse
import logging
import re
import sys

sys.path.append("..")
import aoc

import numpy as np

class Grid:
    def __init__(self, rows):
        self.width = max(len(x) for x in rows)
        self.height = len(rows)
        self.data = np.array(list(map(list, rows)))

    def pretty(self):
        out = ""
        for row in self.data:
            out += f'{"".join(row)}\n'
        return out

    @classmethod
    def fromfile(cls, filename):
        out = []
        for rows in aoc.split_xs(aoc.read_lines(filename), ""):
            out.append(cls(rows))
        return out

    def get_row(self, r):
        return "".join(self.data[r,:])

    def get_col(self, c):
        return "".join(self.data[:,c])

def main(args):
    gs = Grid.fromfile(args.filename)
    g0 = gs[0]
    print(g0.pretty())
    print(g0.get_row(0))
    print(g0.get_col(0))
    print(g0.data)

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args("-f test.txt".split())

    main(args)