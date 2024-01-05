import argparse
import sys
from dataclasses import dataclass

sys.path.append("..")
import aoc

@dataclass(frozen=True)
class Point:
    x: int
    y: int

class Image:
    def __init__(self, points):
        self.points = points
        self.xmax = 0
        self.ymax = 0
        for p in points:
            if p.x > self.xmax:
                self.xmax = p.x
            if p.y > self.ymax:
                self.ymax = p.y

    def show(self):
        out = ""
        for j in range(self.ymax+1):
            out += "\n"
            for i in range(self.xmax+1):
                if Point(i, j) in self.points:
                    out += "#"
                else:
                    out += "."
        return out

    def distances(self):
        totaldist = 0
        for i, pi in enumerate(self.points):
            for pj in self.points[i+1:]:
                dist = abs(pj.x - pi.x) + abs(pj.y - pi.y)
                #print(f"{pi} {pj} {dist}")
                totaldist += dist
        return totaldist

    def expand(self, n=2):
        expanded = {p: p for p in self.points}
        for x in range(self.xmax+1):
            xlt, xeq, xgt = self.partition(x, self.points, lambda p: p.x)
            if len(xeq) == 0:
                for p in xgt:
                    pe = expanded[p]
                    expanded[p] = Point(pe.x+n-1, pe.y)
        for y in range(self.ymax+1):
            ylt, yeq, ygt = self.partition(y, self.points, lambda p: p.y)
            if len(yeq) == 0:
                for p in ygt:
                    pe = expanded[p]
                    expanded[p] = Point(pe.x, pe.y+n-1)
        return Image(list(expanded.values()))

    def partition(self, pivot, points, func):
        lt, eq, gt = [], [], []
        for p in points:
            value = func(p)
            if value < pivot:
                lt.append(p)
            elif value == pivot:
                eq.append(p)
            else:
                gt.append(p)
        return lt, eq, gt

    @classmethod
    def fromfile(cls, filename):
        points = []
        with open(filename, "r") as fh:
            for y, line in enumerate(fh):
                for x, c in enumerate(line.strip()):
                    if c == "#":
                        points.append(Point(x, y))
        return Image(points)

def main(args):
    image = Image.fromfile(args.filename)
    #print(image.points)
    #print(image.xmax)
    #print(image.ymax)
    #print(image.show())
    expimage = image.expand(1000000)
    #print(expimage.show())
    print(expimage.distances())

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args("-f input.txt".split())

    main(args)