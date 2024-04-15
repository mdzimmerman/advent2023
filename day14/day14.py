import argparse
import sys
from collections import defaultdict

sys.path.append("..")
import aoc
from aoc import Point

class Dish:
    def __init__(self, rounds, cubes, width, height):
        self.rounds = frozenset(rounds)
        self.cubes  = frozenset(cubes)
        self.width  = width
        self.height = height

    def show(self):
        out = ""
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p in self.cubes:
                    out += "#"
                elif p in self.rounds:
                    out += "O"
                else:
                    out += "."
            out += "\n"
        return out

    def load(self):
        return sum(self.height-r.y for r in self.rounds)

    @classmethod
    def from_file(cls, filename):
        rounds = set()
        cubes = set()
        lines = aoc.read_lines(filename)
        height = len(lines)
        width = len(lines[0])
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    cubes.add(Point(x, y))
                elif c == "O":
                    rounds.add(Point(x, y))
        return cls(rounds, cubes, width, height)

    def get_sorted_rounds(self, dir):
        if dir == "n":
            return sorted(self.rounds, key=lambda p: p.y)
        elif dir == "s":
            return sorted(self.rounds, key=lambda p: p.y, reverse=True)
        elif dir == "w":
            return sorted(self.rounds, key=lambda p: p.x)
        elif dir == "e":
            return sorted(self.rounds, key=lambda p: p.x, reverse=True)
        else:
            return None

    def get_next_pos(self, rock, dir):
        if dir == "n":
            return Point(rock.x, rock.y-1)
        elif dir == "s":
            return Point(rock.x, rock.y+1)
        elif dir == "e":
            return Point(rock.x+1, rock.y)
        elif dir == "w":
            return Point(rock.x-1, rock.y)
        else:
            return None

    def in_bounds(self, rock):
        return 0 <= rock.x < self.width and 0 <= rock.y < self.height

    def slide(self, dir):
        nrocks = set()
        for r in self.get_sorted_rounds(dir):
            stopped = False
            rcurr = Point(r.x, r.y)
            while not stopped:
                rnext = self.get_next_pos(rcurr, dir)
                if self.in_bounds(rnext) and rnext not in nrocks and rnext not in self.cubes:
                    rcurr = rnext
                else:
                    stopped = True
            nrocks.add(rcurr)
        return Dish(nrocks, self.cubes, self.width, self.height)

    def cycle(self):
        return self.slide("n").slide("w").slide("s").slide("e")

    def cycle_n_times(self, n):
        cycles = dict()
        dishes = list()

        dish = self
        cycles[dish.gethash()] = 0
        dishes.append(dish)
        i = 1
        found = False
        c1, c2 = None, None
        while not found:
            dish = dish.cycle()
            hash = dish.gethash()
            if hash in cycles:
                c1, c2 = cycles[hash], i
                print(c1, c2)
                found = True
            else:
                cycles[hash] = i
                dishes.append(dish)
                i += 1

        if n >= len(dishes):
            return dishes[c1 + (n - c1) % (c2 - c1)]
        else:
            return dishes[n]

    def gethash(self):
        return self.rounds.__hash__()

def main(args):
    print("-- part 1 test --")

    cycles = defaultdict(list)
    tdish0 = Dish.from_file("input.txt")

    tdish = tdish0.cycle_n_times(1_000_000_000)
    #print(tdish.show())
    print(tdish.load())

    #print(tdish0.show())
    #cycles[tdish0.gethash()].append(0)

    #cycles = defaultdict(list)
    #tdish = tdish0
    #for i in range(1, 1000):
    #    tdish = tdish.cycle()
    #    cycles[tdish.gethash()].append(i)

    #for k, v in cycles.items():
    #    print(k, v)

    #print()
    #tdish1 = tdish.cycle()
    #print(tdish1.show())
    #tdish2 = tdish1.cycle()
    #print(tdish2.show())
    #tdish3 = tdish2.cycle()
    #print(tdish3.show())
    #print(tdish.slide("e").show())
    #print(tdish.slide("s").show())
    #print(tdish.slide("w").show())
    #print(tdish1.show())
    #print(tdish1.load())

    #print()
    #print("-- part 1 --")
    #dish = Dish.from_file("input.txt")
    #print(dish.slide_north().load())
    #print(dish.rounds.__hash__())


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args("-f test.txt".split())

    # parse logging level
    main(args)
