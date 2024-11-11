import argparse
import sys

import numpy as np

sys.path.append("..")
import aoc

class Grid:
    def __init__(self, data):
        self.data = data
        self.width = data.shape[0]
        self.height = data.shape[1]

    def get_next(self, n, dir):
        pass

    def bfs(self, start):
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

    @classmethod
    def fromfile(cls, filename):
        data = []
        with open(filename,"r") as fh:
            for l in fh:
                l = l.strip()
                data.append([int(x) for x in l])
        return Grid(np.array(data))
def main(args):
    grid = Grid.fromfile(args.filename)
    print(grid.data)
    print(grid.width)
    print(grid.height)


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="test.txt")
    args = parser.parse_args()

    main(args)