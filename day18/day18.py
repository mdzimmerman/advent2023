import argparse
from collections import deque
from dataclasses import dataclass
import numpy as np
import re
import sys

sys.path.append("..")
from aoc import Dir, Point
import shapely

@dataclass
class DigEntry:
    dir: Dir
    dist: int
    color: str

    pattern = re.compile(r"(.) (\d+) \((.+)\)")
    
    @classmethod
    def from_string(cls, s):
        m = cls.pattern.match(s)
        if m:
            return cls(Dir.fromstr(m.group(1)), int(m.group(2)), m.group(3))

class DigPlan:
    def __init__(self, entries: list[DigEntry]):
        self.entries = entries
        self._build_trench()

    def _build_trench(self):
        points = list()
        currpoint = Point(0.5, 0.5)
        points.append((currpoint.x, currpoint.y))
        segments = list()
        
        for e in self.entries:
            oldpoint = currpoint
            currpoint = currpoint.movedir(dir=e.dir, d=e.dist)
            l = shapely.geometry.LineString([(oldpoint.x, oldpoint.y), (currpoint.x, currpoint.y)])
            segments.append(shapely.buffer(l, 0.5, cap_style="square"))
            #print(e, currpoint)
            points.append((currpoint.x, currpoint.y))

    
        self.trench = shapely.union_all(segments)
        self.trencharea = shapely.geometry.Polygon(self.trench.exterior)

    def print_trench(self):
        for y in range(self.ymin, self.ymax+1):
            for x in range(self.xmin, self.xmax+1):
                p = Point(x, y)
                if p in self.trench:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def to_array(self):
        out = []
        for y in range(self.ymin-1, self.ymax+2):
            out.append([])
            for x in range(self.xmin-1, self.xmax+2):
                p = Point(x, y)
                if p in self.trench:
                    out[-1].append(1)
                else:
                    out[-1].append(0)
        return np.array(out)
    
    @classmethod
    def from_file(cls, filename):
        entries = []
        with open(filename, "r") as fh:
            for l in fh:
                e = DigEntry.from_string(l.strip())
                if e is not None:
                    entries.append(e)
        return cls(entries)

    def part1(self):
        grid = self.to_array()
        array_ymax, array_xmax = grid.shape
        print(array_ymax * array_xmax)
        #print(array_ymax, array_xmax)

        queue = deque()
        queue.append(Point(array_xmax//2, array_ymax//2))

        i = 0
        while len(queue):
            p = queue.popleft()
            if grid[p.y, p.x] == 2:
                continue
            grid[p.y, p.x] = 2
            #print(p)
            i += 1
            #if (i % 100) == 0:
            #    print(i)
            for d in Dir.U, Dir.R, Dir.D, Dir.L:
                pn = p.movedir(d)
                if 0 <= pn.x < array_xmax \
                    and 0 <= pn.y < array_ymax \
                    and grid[pn.y, pn.x] == 0:
                    queue.append(pn)

        print(np.count_nonzero(grid > 0))
        return grid

        #n_tot = array_xmax * array_ymax
        #n_ext = len(visited)
        #n_int = n_tot - n_ext
        #print(n_tot, n_ext, n_int)


def main(args):
    #print(args)
    plan = DigPlan.from_file("input.txt")
    #for e in plan.entries:
    #    print(e)
    print(f"x = {plan.xmin}..{plan.xmax}")
    print(f"y = {plan.ymin}..{plan.ymax}")
    #plan.print_trench()
    plan.part1()

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="test.txt")
    args = parser.parse_args()

    # parse logging level
    main(args)