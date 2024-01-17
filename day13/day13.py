import argparse
import logging
import re
import sys

sys.path.append("..")
import aoc

import numpy as np

class Grid():
    def __init__(self, rows, loglevel=0):
        self.width = max(len(x) for x in rows)
        self.height = len(rows)
        self.data = np.array(list(map(list, rows)))
        self.loglevel = loglevel

    def warn(self, *args):
        print(*args)

    def info(self, *args):
        if (self.loglevel >= 1):
            print(*args)

    def debug(self, *args):
        if (self.loglevel >= 2):
            print(*args)

    def pretty(self):
        out = ""
        for row in self.data:
            out += f'{"".join(row)}\n'
        return out

    @classmethod
    def fromfile(cls, filename, **kwargs):
        out = []
        for rows in aoc.split_xs(aoc.read_lines(filename), ""):
            out.append(cls(rows, **kwargs))
        return out

    def get_row(self, r):
        return "".join(self.data[r,:])

    def get_col(self, c):
        return "".join(self.data[:,c])

    def similarity(self, a, b):
        out = len(a)
        for i in range(len(a)):
            if a[i] == b[i]:
                out -= 1
        return out

    def row_similarity(self):
        out = np.full((self.height, self.height), 0)
        for i in range(self.height):
            ri = self.get_row(i)
            for j in range(i+1, self.height):
                rj = self.get_row(j)
                out[i,j] = self.similarity(ri, rj)
        return out

    def col_similarity(self):
        out = np.full((self.width, self.width), 0)
        for i in range(self.width):
            ci = self.get_col(i)
            for j in range(i+1, self.width):
                cj = self.get_col(j)
                out[i,j] = self.similarity(ci, cj)
        return out

    def find_mirror(self, simmatrix, smudges=0):
        #colsim = self.col_similarity()
        n = simmatrix.shape[0]
        #totalsim = 0
        for i in range(n-1):
            total = 0
            aj = i
            bj = i+1
            while aj >= 0 and bj < n:
                total += simmatrix[aj, bj]
                aj = aj-1
                bj = bj+1
            if total == smudges:
                return i+1
        return None

    def find_and_score(self, smudges=0):
        simcol = self.col_similarity()
        vmirror = self.find_mirror(simcol, smudges=smudges)
        self.debug()
        self.debug(simcol)
        self.debug(vmirror)

        simrow = self.row_similarity()
        hmirror = self.find_mirror(simrow, smudges=smudges)
        self.debug()
        self.debug(simrow)
        self.debug(hmirror)

        score = 0
        if vmirror is not None:
            score += vmirror
        if hmirror is not None:
            score += (hmirror) * 100

        return score

def p1test():
    gs = Grid.fromfile("test.txt", loglevel=2)
    print(sum(g.find_and_score() for g in gs))

def p1():
    gs = Grid.fromfile("input.txt")
    print("part1 =", sum(g.find_and_score() for g in gs))

def p2test():
    gs = Grid.fromfile("test.txt", loglevel=2)
    print(sum(g.find_and_score(smudges=1) for g in gs))

def p2():
    gs = Grid.fromfile("input.txt")
    print("part1 =", sum(g.find_and_score(smudges=1) for g in gs))

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    p1test()
    p1()
    p2test()
    p2()