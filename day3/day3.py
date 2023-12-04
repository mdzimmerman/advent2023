import argparse
import logging
import re
import sys

sys.path.append("..")
import aoc


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

    def get(self, i, j):
        if i >= 0 and i < self.width and j >= 0 and j < self.height:
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
                        numbers[-1]['number'] += c
                    else:
                        numbers.append({"pos": (i, j), "number": c})
                        in_number = True
                else:
                    if in_number:
                        in_number = False
            in_number = False
        return numbers

    def is_part(self, number):
        ni = number["pos"][0]
        nj = number["pos"][1]
        for j in range(nj-1, nj+2):
            for i in range(ni-1, ni+len(number["number"])+1):
                char = self.get(i, j)
                logging.debug(f"pos={i, j}, char={self.get(i, j)}")
                if char != "." and not Grid.digitpatt.match(char):
                    return True
        return False

    def part1(self):
        total = 0
        for number in self.find_numbers():
            number_is_part = self.is_part(number)
            logging.info(f"{number['number']} {number_is_part}")
            if number_is_part:
                total += int(number['number'])
        return total

    def print_grid(self):
        for l in self.data:
            print(l)

def main(args):
    grid = Grid(args.filename)
    #grid.print_grid()
    #print(grid.width)
    #print(grid.height)
    print(grid.part1())


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