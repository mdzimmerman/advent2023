import argparse
import logging
import re
import sys
from dataclasses import dataclass

sys.path.append("..")
import aoc


def hash(s):
    current = 0
    for c in s:
        current += ord(c)
        current *= 17
        current %= 256
    return current

@dataclass(frozen=True)
class Step:
    label: str
    op: str
    focal_length: int

    PATT_DASH = re.compile(r"^([a-z]+)-$")
    PATT_EQUALS = re.compile(r"^([a-z]+)=(\d+)")

    @classmethod
    def parse(cls, s):
        m = cls.PATT_DASH.match(s)
        if m:
            return cls(m.group(1), '-', None)

        m = cls.PATT_EQUALS.match(s)
        if m:
            return cls(m.group(1), '=', int(m.group(2)))

@dataclass(frozen=True)
class Lens:
    label: str
    focal_length: int

class Hashmap:
    def __init__(self, s):
        self.steps = s.split(",")
        #self.boxes = [[] for _ in range(256)]


    def part1(self):
        return sum(hash(s) for s in self.steps)

    def part2(self, debug=True):
        boxes = [[] for _ in range(256)]
        for step in (Step.parse(s) for s in self.steps):
            b = hash(step.label)
            if step.op == '-':
                for lens in boxes[b]:
                    if lens.label == step.label:
                        boxes[b].remove(lens)
                        break
            elif step.op == '=':
                found = False
                for i, lens in enumerate(boxes[b]):
                    if lens.label == step.label:
                        found = True
                        boxes[b][i] = Lens(step.label, step.focal_length)
                        break
                if not found:
                    boxes[b].append(Lens(step.label, step.focal_length))

        if debug:
            for i, box in enumerate(boxes):
                if len(box) > 0:
                    print(f"{i}: {box}")
        power = 0
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                power += (i+1) * (j+1) * lens.focal_length
        return power

    @classmethod
    def from_file(cls, filename):
        return cls(aoc.read_string(filename))

def main(args):
    #print(hash("HASH"))

    test = Hashmap.from_file("test.txt")
    print(test.part1())
    #print(test.boxes)

    inp = Hashmap.from_file("input.txt")
    print(inp.part1())

    print(test.part2())

    print(inp.part2(debug=False))



if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args()

    # parse logging level
    main(args)