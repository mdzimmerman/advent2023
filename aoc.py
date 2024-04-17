from dataclasses import dataclass
from collections import namedtuple

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError
        return Point(self.x + other.x, self.y + other.y)

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


