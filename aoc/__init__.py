from dataclasses import dataclass
from collections import namedtuple
from enum import Enum

class Dir(Enum):
    U = 0
    R = 1
    D = 2
    L = 3

    @classmethod
    def fromstr(cls, s):
        return cls[s]        

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError
        return Point(self.x + other.x, self.y + other.y)

    def movedir(self, dir: Dir):
        if dir == Dir.U:
            return Point(self.x, self.y-1)
        elif dir == Dir.R:
            return Point(self.x+1, self.y)
        elif dir == Dir.D:
            return Point(self.x, self.y+1)
        elif dir == Dir.L:
            return Point(self.x-1, self.y)
        else:
            raise Exception(f"bad direction {dir}")
    
    def move(self, dir):
        if dir == 'N':
            return Point(self.x, self.y-1)
        elif dir == 'E':
            return Point(self.x+1, self.y)
        elif dir == 'S':
            return Point(self.x, self.y+1)
        elif dir == 'W':
            return Point(self.x-1, self.y)
        else:
            raise Exception(f"bad direction {dir}")

@dataclass
class Interval:
    start: int
    end: int

    def __repr__(self):
        return f"{self.start}-{self.end}"

    def __len__(self):
        return self.end - self.start

    def count(self):
        return self.end - self.start + 1

    def split(self, at):
        if at <= self.start:
            return None, Interval(self.start, self.end)
        elif self.start < at <= self.end:
            return Interval(self.start, at-1), Interval(at, self.end)
        else:
            return Interval(self.start, self.end), None

    def intersect(self, other):
        if self.end <= other.start or other.end <= self.start:
            return None
        else:
            start = max(self.start, other.start)
            end = min(self.end, other.end)
            return Interval(start, end)

@dataclass
class IntervalSeq:
    intervals: list[Interval]

    @classmethod
    def build(cls, xs):
        out = []
        it = iter(xs)
        for x, y in zip(it, it):
            out.append(Interval(x, y))
        return IntervalSeq(out)

    def __repr__(self):
        return f"[{','.join(str(x) for x in self.intervals)}]"

    def append(self, x: Interval):
        self.intervals.append(x)

    def count(self):
        return sum(x.count() for x in self.intervals)

    def split(self, at: int):
        a = IntervalSeq([])
        b = IntervalSeq([])
        for x in self.intervals:
            xa, xb = x.split(at)
            if xa is not None:
                a.append(xa)
            if xb is not None:
                b.append(xb)
        return a, b

def read_lines(filename):
    """Read in each line of a file as an element in a list"""

    lines = []
    with open(filename, "r") as fh:
        for l in fh:
            lines.append(l.rstrip())
    return lines

def read_string(filename):
    return "".join(read_lines(filename))

def split_xs(xs, sep):
    """Split the iterable xs on the separator sep"""
    out = [[]]
    for x in xs:
        if x == sep:
            out.append([])
        else:
            out[-1].append(x)
    return out


