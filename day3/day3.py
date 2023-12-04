import argparse
from dataclasses import dataclass
from functools import reduce
import logging
import re
import sys

sys.path.append("..")
import aoc

@dataclass
class Number:
    i: int
    j: int
    numbertext: str


class Grid:
    digitpatt = re.compile(r'^\d$')

    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.width = None
        self.height = None
        with open(filename, 'r') as fh:
            for l in fh:
                self.data.append(l.strip())
            self.height = len(self.data)
            if self.height > 0:
                self.width = len(self.data[0])
        self.numbers = self.find_numbers()

    def get(self, i, j):
        if 0 <= i < self.width and 0 <= j < self.height:
            return self.data[j][i]
        else:
            return '.'

    def find_numbers(self):
        in_number = False
        numbers = []
        for j in range(self.height):
            for i in range(self.width):
                c = self.get(i, j)
                if Grid.digitpatt.match(c):
                    if in_number:
                        numbers[-1].numbertext += c
                    else:
                        numbers.append(Number(i=i, j=j, numbertext=c))
                        in_number = True
                else:
                    if in_number:
                        in_number = False
            in_number = False
        return numbers

    def is_part(self, number):
        for j in range(number.j-1, number.j+2):
            for i in range(number.i-1, number.i+len(number.numbertext)+1):
                char = self.get(i, j)
                #print(f"{number} char={self.get(i, j)}")
                if char != "." and not Grid.digitpatt.match(char):
                    return True
        return False

    def part1(self):
        total = 0
        for number in self.numbers:
            number_is_part = self.is_part(number)
            print(f"{number} {number_is_part}")
            if number_is_part:
                total += int(number.numbertext)
        return total

    def part2(self):
        totalratio = 0
        numbers = self.find_numbers()
        for j in range(self.height):
            for i in range(self.width):
                c = self.get(i, j)
                if c == '*':
                    gears = self.find_gears(i, j, numbers)
                    print(gears)
                    if len(gears) == 2:
                        ratio = reduce(lambda a, b: a * b, gears)
                        #print(gears, ratio)
                        totalratio += ratio
        return totalratio

    def find_gears(self, i, j, numbers):
        gears = []
        for num in numbers:
            if i >= num.i-1 and i <= num.i+len(num.numbertext) and j >= num.j-1 and j <= num.j+1:
                gears.append(int(num.numbertext))
        return gears

    def print_grid(self):
        for l in self.data:
            print(l)

def main(args):
    grid = Grid(args.filename)
    #grid.print_grid()
    #print(grid.width)
    #print(grid.height)
    print(f"part1 = {grid.part1()}")
    print(f"part2 = {grid.part2()}")


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args()

    # parse logging level
    loglevel = logging.INFO
    if args.log == "debug":
        loglevel = logging.DEBUG
    elif args.log == "warning":
        loglevel = logging.WARNING
    logging.basicConfig(level=loglevel)

    main(args)