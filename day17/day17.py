import argparse
from dataclasses import dataclass, field
import queue
import sys

import numpy as np

sys.path.append("..")
import aoc
from aoc import Point

@dataclass(frozen=True, order=True)
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
    
    def neighbors(self, state: State, minsteps=0, maxsteps=3):
        nextdirs = []
        if state.n < maxsteps:
            nextdirs.append(state.dir)
        if state.n >= minsteps:
            if state.dir == 'E' or state.dir == 'W':
                nextdirs.append('N')
                nextdirs.append('S')
            elif state.dir == 'N' or state.dir == 'S':
                nextdirs.append('E')
                nextdirs.append('W')
        
        for ndir in nextdirs:
            npoint = state.point.move(ndir)
            if npoint.x < 0 or npoint.y < 0 or npoint.x >= self.width or npoint.y >= self.height:
                continue
            nloss = state.loss + self.data[npoint.y, npoint.x]                
            nn = None
            if ndir == state.dir:
                nn = state.n + 1
            else:
                nn = 1
            yield State(nloss, npoint, ndir, nn)

    def dijkstra(self, start=None, end=None, minsteps=0, maxsteps=3):
        if start == None:
            start = Point(0, 0)
        if end == None:
            end = Point(self.width-1, self.height-1)
        
        visited = set()
        pq = queue.PriorityQueue()
        pq.put(State(0, start, 'E', 0))
        pq.put(State(0, start, 'S', 0))

        while not pq.empty():
            state = pq.get()
            #print(state)

            if state.point == end and state.n >= minsteps:
                return state

            if (state.point, state.dir, state.n) in visited:
                continue
            visited.add((state.point, state.dir, state.n))
            
            for nstate in self.neighbors(state, minsteps=minsteps, maxsteps=maxsteps):
                pq.put(nstate)

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
    #print(grid.data)
    #print(grid.width)
    #print(grid.height)

    #s1 = State(0, Point(0, 0), 'E', 0)
    #print(list(grid.neighbors(s1)))
    
    print(grid.dijkstra())
    print(grid.dijkstra(minsteps=4, maxsteps=10))

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="test.txt")
    args = parser.parse_args()

    main(args)
