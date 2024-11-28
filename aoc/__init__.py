from dataclasses import dataclass
from collections import namedtuple
from enum import Enum

class AocLogging:
    WARN = 0
    INFO = 1
    DEBUG = 2
    def __init__(self, level=WARN):
        self.level = level

    def _print_logging(self, level, *args):
        if self.level >= level:
            print(*args)

    def warn(self, *args):
        self._print_logging(0, "WARN:", *args)

    def info(self, *args):
        self._print_logging(1, "INFO:", *args)

    def debug(self, *args):
        self._print_logging(2, "DEBUG:", *args)

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

    def __len__(self):
        return self.end - self.start

    def intersect(self, other):
        if self.end <= other.start or other.end <= self.start:
            return None
        else:
            start = max(self.start, other.start)
            end = min(self.end, other.end)
            return Interval(start, end)


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


