import argparse
import logging
import re
import sys
from dataclasses import dataclass

sys.path.append("..")
import aoc

class Grid:
    @classmethod
    def from_file(cls, filename):
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

    def show(self):
        out = ""
        for j, row in enumerate(self.grid):
            for i, c in enumerate(row):
                out += c
            out += "\n"
        return out

    def inbounds(self, x, y):
        pass

    def get(self, x, y):
        return self.grid[y][x]

@dataclass(frozen=True)
class Beam:
    x: int
    y: int
    dir: str

    def move(self, dir):
        if dir == 'N':
            return Beam(self.x, self.y-1, dir)
        elif dir == 'E':
            return Beam(self.x+1, self.y, dir)
        elif dir == 'S':
            return Beam(self.x, self.y+1, dir)
        elif dir == 'W':
            return Beam(self.x-1, self.y, dir)

def passthrough(b):
    """Keep moving in the same direction"""
    return b.move(b.dir)

def get_next(grid, b):
    tile = grid.get(b.x, b.y)
    out = ""
    if tile == '|':
        if b.dir == 'E' or b.dir == 'W':
            out = "NS"
        else:
            out = b.dir
    elif tile == '-':
        if b.dir == 'N' or b.dir == 'S':
            out = "EW"
        else:
            out = b.dir
    elif tile == '/':
        if b.dir == 'N':
            out = 'E'
        elif b.dir == 'E':
            out = 'N'
        elif b.dir == 'S':
            out = 'W'
        elif b.dir == 'W':
            out = 'S'
    elif tile == '\\':
        if b.dir == 'N':
            out = 'W'
        elif b.dir == 'E':
            out = 'S'
        elif b.dir == 'S':
            out = 'E'
        elif b.dir == 'W':
            out = 'N'
    else:
        out = b.dir
    return filter(lambda n: grid.inbounds(n.x, n.y), b.move(d))

def bfs(self, grid, start):
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

def main(args):
    grid = Grid.from_file(args.filename)
    print(grid.show())

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args("-f test.txt".split())

    main(args)