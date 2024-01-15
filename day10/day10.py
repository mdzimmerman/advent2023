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

    LOOPCHARS = {"-", "|", "F", "7", "L", "J", "S"}

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
        self.loop_max_steps, self.loop = self.bfs(self.findstart(), get_next_impl="loop")

    def expand(self):
        expandx = []
        for j in range(len(self.grid)):
            expandx.append("")
            expandx[j] += self.grid[j][0]
            for i in range(len(self.grid[j]) - 1):
                pa = Point(i, j)
                pb = Point(i+1, j)
                ca = self.get(pa)
                cb = self.get(pb)
                if (pa in self.loop and pb in self.loop and
                        'E' in Grid.BYCHAR[ca] and 'W' in Grid.BYCHAR[cb]):
                    expandx[j] += "-"
                else:
                    expandx[j] += " "
                expandx[j] += cb

        expandxy = []
        expandxy.append(expandx[0])
        for j in range(len(self.grid)-1):
            fill = []
            for i in range(len(self.grid[j])):
                pa = Point(i, j)
                pb = Point(i, j+1)
                ca = self.get(pa)
                cb = self.get(pb)
                if (pa in self.loop and pb in self.loop and
                        'S' in Grid.BYCHAR[ca] and 'N' in Grid.BYCHAR[cb]):
                    fill += "|"
                else:
                    fill += " "
            expandxy.append(" ".join(fill))
            expandxy.append(expandx[j + 1])
        return Grid(expandxy)

    def prettyprint(self, outregions=None, inregions=None):
        if outregions is None:
            outregions = []
        if inregions is None:
            inregions = []
        for j, row in enumerate(self.grid):
            for i, c in enumerate(self.grid[j]):
                p = Point(i, j)
                if p in outregions:
                    print("O", end="")
                elif p in inregions:
                    print("I", end="")
                else:
                    print(c, end="")
            print()

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

    def get_next_loop(self, p):
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

    def get_next_ground(self, p):
        out = []
        for d, dp in Grid.DIRS.items():
            np = p + dp
            nc = self.get(np)
            if 0 <= np.x < self.width and 0 <= np.y < self.height and np not in self.loop:
                out.append(np)
        return out

    def bfs(self, start, get_next_impl="loop"):
        get_next = None
        if get_next_impl == "loop":
            get_next = lambda p: self.get_next_loop(p)
        elif get_next_impl == "ground":
            get_next = lambda p: self.get_next_ground(p)

        maxsteps = 0
        visited = set()
        queue = []

        visited.add(start)
        queue.append((start, 0))

        while queue:  # Creating loop to visit each node
            p, steps = queue.pop(0)
            # print(p, steps)
            if steps > maxsteps:
                maxsteps = steps

            for np in get_next(p):
                if np not in visited:
                    visited.add(np)
                    queue.append((np, steps + 1))

        return maxsteps, visited

    def bounds(self, region):
        xmin = None
        xmax = None
        ymin = None
        ymax = None
        for p in region:
            if xmin is None or xmin > p.x:
                xmin = p.x
            if xmax is None or xmax < p.x:
                xmax = p.x
            if ymin is None or ymin > p.y:
                ymin = p.y
            if ymax is None or ymax < p.y:
                ymax = p.y
        return xmin, xmax, ymin, ymax

    def part1(self):
        return self.loop_max_steps

    def find_ground_regions(self):
        regions = list()
        for j, row in enumerate(self.grid):
            for i, c in enumerate(self.grid[j]):
                p = Point(i, j)
                if p not in self.loop and not any(p in r for r in regions):
                    _, rnew = self.bfs(p, get_next_impl="ground")
                    regions.append(rnew)
        inset, outset = set(), set()
        for r in regions:
            xmin, xmax, ymin, ymax = self.bounds(r)
            enclosed = True
            if xmin == 0 or ymin == 0 or xmax == (self.width-1) or ymax == (self.height-1):
                enclosed = False
            for p in r:
                if self.get(p) != ' ':
                    if enclosed:
                        inset.add(p)
                    else:
                        outset.add(p)
        return inset, outset

    def part2(self):
        #self.prettyprint()
        #print()
        gridexp = self.expand()
        #gridexp.prettyprint()
        #print()
        inset, outset = gridexp.find_ground_regions()
        #gridexp.prettyprint(outregions=outset, inregions=inset)
        #print()
        return len(inset)

def main(args):
    grid = Grid.fromfile(args.filename)
    #grid.prettyprint()
    print()
    print(grid.part1())

    #print()
    #start = grid.findstart()
    #print(start, grid.next(start))
    #p00 = Point(0, 0)
    #print(p00, grid.next(p00))
    #p11 = Point(1, 1)
    #print(p11, grid.next(p11))

    print(grid.part2())

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args("-f input.txt".split())

    main(args)
