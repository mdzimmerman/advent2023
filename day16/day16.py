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

    def show(self, mark=set()):
        out = ""
        for j, row in enumerate(self.grid):
            for i, c in enumerate(row):
                if (i, j) in mark:
                    out += '#'
                else:
                    out += c
            out += "\n"
        return out

    def inbounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

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

def get_next_dir(tile, b):
    if tile == '|':
        if b.dir == 'E' or b.dir == 'W': return "NS"
        else: return b.dir
    elif tile == '-':
        if b.dir == 'N' or b.dir == 'S': return "EW"
        else: return b.dir
    elif tile == '/':
        if   b.dir == 'N': return 'E'
        elif b.dir == 'E': return 'N'
        elif b.dir == 'S': return 'W'
        elif b.dir == 'W': return 'S'
    elif tile == '\\':
        if   b.dir == 'N': return 'W'
        elif b.dir == 'E': return 'S'
        elif b.dir == 'S': return 'E'
        elif b.dir == 'W': return 'N'
    elif tile == '.':
        return b.dir
    return ""

def get_next(grid, b):
    tile = grid.get(b.x, b.y)
    out = []
    for d in get_next_dir(tile, b):
        nb = b.move(d)
        if grid.inbounds(nb.x, nb.y):
            out.append(nb)
    #print(out)
    return out

def bfs(grid, start):
    visited = set()
    queue = []

    visited.add(start)
    queue.append((start, 0))
    energized = set()

    while queue:  # Creating loop to visit each node
        b, steps = queue.pop(0)
        #print(b, steps)
        energized.add((b.x, b.y))
        for nb in get_next(grid, b):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, steps + 1))

    return energized

def main(args):
    grid = Grid.from_file(args.filename)
    #print(grid.show())
    max_energized_len = 0
    max_energized = None
    #energized = bfs(grid, Beam(0, 0, 'E'))

    starts = []
    for x in range(grid.width):
        starts.append(Beam(x, 0, 'S'))
    for y in range(grid.height):
        starts.append(Beam(grid.width-1, y, 'W'))
    for x in range(grid.width):
        starts.append(Beam(x, grid.height-1, 'N'))
    for y in range(grid.height):
        starts.append(Beam(0, y, 'E'))

    for start in starts:
        energized = bfs(grid, start)
        energized_len = len(energized)
        if energized_len > max_energized_len:
            max_energized_len = energized_len
            max_energized = energized

    #print(grid.show(mark=max_energized))
    print(max_energized_len)


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args("-f input.txt".split())

    main(args)