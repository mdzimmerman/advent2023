import argparse
import logging
import sys

sys.path.append("..")
from aoc import Point

class Grid:
    DIRS = {
        "N": Point(0, -1),
        "E": Point(1, 0),
        "S": Point(0, 1),
        "W": Point(-1, 0)}

    BYCHAR = {
        ".": {},
        "-": {"E", "W"},
        "|": {"N", "S"},
        "F": {"E", "S"},
        "7": {"W", "S"},
        "L": {"N", "E"},
        "J": {"N", "W"},
        "S": {"N", "E", "S", "W"}
    }

    def __init__(self, filename):
        self.grid = []
        self.height = 0
        self.width = 0
        with open(filename, "r") as fh:
            for l in fh:
                self.grid.append(l.strip())
            self.width = len(self.grid[0])
            self.height = len(self.grid)

    def prettyprint(self):
        for l in self.grid:
            print(l)

    def get(self, p):
        if 0 <= p.x < self.width and 0 <= p.y < self.height:
            return self.grid[p.y][p.x]
        else:
            return "."

    def findstart(self):
        for j, line in enumerate(self.grid):
            for i, c in enumerate(self.grid[j]):
                if c == 'S':
                    return Point(i, j)

    def next(self, p):
        out = []
        c = self.get(p)
        for d in Grid.BYCHAR[c]:
            np = p + Grid.DIRS[d]
            nc = self.get(np)
            if d == "N" and "S" in Grid.BYCHAR[nc]:
                out.append(np)
            elif d == "S" and "N" in Grid.BYCHAR[nc]:
                out.append(np)
            elif d == "E" and "W" in Grid.BYCHAR[nc]:
                out.append(np)
            elif d == "W" and "E" in Grid.BYCHAR[nc]:
                out.append(np)
        return out

    def bfs(self, start=None):
        if start is None:
            start = self.findstart()

        maxsteps = 0
        visited = set()
        queue = []

        visited.add(start)
        queue.append((start, 0))

        while queue:  # Creating loop to visit each node
            p, steps = queue.pop(0)
            print(p, steps)
            if steps > maxsteps:
                maxsteps = steps

            for np in self.next(p):
                if np not in visited:
                    visited.add(np)
                    queue.append((np, steps+1))

        return maxsteps

def main(args):
    grid = Grid(args.filename)
    grid.prettyprint()

    print()
    start = grid.findstart()
    print(start, grid.next(start))
    p00 = Point(0, 0)
    print(p00, grid.next(p00))
    p11 = Point(1, 1)
    print(p11, grid.next(p11))

    grid.bfs()

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args("-f test2.txt".split())

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel, stream=sys.stdout)

    main(args)