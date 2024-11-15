import argparse
from dataclasses import dataclass
import logging
import numpy as np
import re
import sys

sys.path.append("..")
from aoc import Dir, Point

@dataclass
class DigEntry:
    dir: Dir
    dist: int
    color: str

    pattern = re.compile(r"(.) (\d) \((.+)\)")
    
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
        self.trench = set()
        currpoint = Point(0, 0)
        self.trench.add(currpoint)
        
        for e in self.entries:
            for _ in range(e.dist):
                currpoint = currpoint.movedir(e.dir)
                self.trench.add(currpoint)

        self.xmin = min(p.x for p in self.trench)
        self.xmax = max(p.x for p in self.trench)
        self.ymin = min(p.y for p in self.trench)
        self.ymax = max(p.y for p in self.trench)

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

def main(args):
    #print(args)
    plan = DigPlan.from_file(args.filename)
    #for e in plan.entries:
    #    print(e)
    print(f"x = {plan.xmin}..{plan.xmax}")
    print(f"y = {plan.ymin}..{plan.ymax}")
    plan.print_trench()

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args()

    # parse logging level
    main(args)