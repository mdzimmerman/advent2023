import argparse
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
        " ": {},
        "-": {"E", "W"},
        "|": {"N", "S"},
        "F": {"E", "S"},
        "7": {"W", "S"},
        "L": {"N", "E"},
        "J": {"N", "W"},
        "S": {"N", "E", "S", "W"}
    }

    @classmethod
    def fromfile(cls, filename):
        grid = list()
        with open(filename, "r") as fh:
            for l in fh:
                grid.append(l.strip())
        return cls(grid)

    def __init__(self, grid):
        if not len(grid):
            raise ValueError("Input grid is empty")
        self.grid = list(grid)
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def expand(self):
        expandx = []
        for j in range(len(self.grid)):
            expandx.append("")
            expandx[j] += self.grid[j][0]
            for i in range(len(self.grid[j])-1):
                ca = self.grid[j][i]
                cb = self.grid[j][i+1]
                if 'E' in Grid.BYCHAR[ca] and 'W' in Grid.BYCHAR[cb]:
                    expandx[j] += "-"
                else:
                    expandx[j] += " "
                expandx[j] += cb

        expandxy = []
        expandxy.append(expandx[0])
        for j in range(len(expandx)-1):
            fill = ""
            for i in range(len(expandx[j])):
                ca = expandx[j][i]
                cb = expandx[j+1][i]
                if 'S' in Grid.BYCHAR[ca] and 'N' in Grid.BYCHAR[cb]:
                    fill += "|"
                else:
                    fill += " "
            expandxy.append(fill)
            expandxy.append(expandx[j+1])
        return Grid(expandxy)

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
            #print(p, steps)
            if steps > maxsteps:
                maxsteps = steps

            for np in self.next(p):
                if np not in visited:
                    visited.add(np)
                    queue.append((np, steps+1))

        return maxsteps, visited

def main(args):
    grid = Grid.fromfile(args.filename)
    grid.prettyprint()

    print()
    start = grid.findstart()
    print(start, grid.next(start))
    p00 = Point(0, 0)
    print(p00, grid.next(p00))
    p11 = Point(1, 1)
    print(p11, grid.next(p11))

    #grid.bfs()
    gridexp = grid.expand()
    gridexp.prettyprint()

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args("-f test5.txt".split())

    main(args)