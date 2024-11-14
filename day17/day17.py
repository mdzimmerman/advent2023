import argparse
from dataclasses import dataclass, field
import queue
import sys

import numpy as np

sys.path.append("..")
import aoc
from aoc import Point

@dataclass(frozen=True)
class State:
    loss: int
    point: Point = field(compare=False)
    dir: str = field(compare=False)
    n: int = field(compare=False)

class Grid:
    def __init__(self, data):
        self.data = data
        self.width = data.shape[0]
        self.height = data.shape[1]

    def neighbors(self, state: State):
        nextdirs = []
        if state.dir == 'E' or state.dir == 'W':
            nextdirs.append('N')
            nextdirs.append('S')
        elif state.dir == 'N' or state.dir == 'S':
            nextdirs.append('E')
            nextdirs.append('S')
        if state.n < 3:
            nextdirs.append(state.dir)
        for ndir in nextdirs:
            npoint = state.point.move(ndir)
            if npoint.x < 0 or npoint.y < 0 or npoint.x >= self.width or npoint.y >= self.height:
                continue
            nn = 1
            if ndir == dir:
                nn = state.n + 1
            nloss = state.loss + self.data[npoint.y, npoint.x]
            yield State(nloss, npoint, ndir, nn)

    def dijkstra(self):
        start = State(0, Point(0, 0), 'E', 0)

        visited = set()
        visited.add(start.point)

        pq = queue.PriorityQueue()
        pq.put(start)

        while not pq.empty():
            pass

    @classmethod
    def fromfile(cls, filename):
        data = []
        with open(filename, "r") as fh:
            for l in fh:
                l = l.strip()
                data.append([int(x) for x in l])
        return Grid(np.array(data))


def main(args):
    grid = Grid.fromfile(args.filename)
    print(grid.data)
    print(grid.width)
    print(grid.height)

    s1 = State(0, Point(0, 0), 'E', 0)
    print(list(grid.neighbors(s1)))


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="test.txt")
    args = parser.parse_args()

    main(args)
