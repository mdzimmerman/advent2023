import argparse
from dataclasses import dataclass
import re
import sys

sys.path.append("..")
import aoc
from aoc import IntervalSeq, Interval

@dataclass
class Rule:
    prop: str
    op: str
    value: int
    dest: str

    PATTERN = re.compile(r"(\w+)([<>])(\d+):(.+)")

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            return cls(m.group(1), m.group(2), int(m.group(3)), m.group(4))

@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    altdest: str

    PATTERN = re.compile(r"(\w+){(.+),(\w+)}")

    def eval(self, part):
        for rule in self.rules:
            if rule.op == '>':
                if part[rule.prop] > rule.value:
                    return rule.dest
            elif rule.op == '<':
                if part[rule.prop] < rule.value:
                    return rule.dest
        return self.altdest

    def evalrange(self, partrange: dict[str, IntervalSeq]):
        x = partrange.copy()
        for rule in self.rules:
            if rule.op == '<':
                a, b = partrange[rule.prop].split(rule.value)
                if a.count():
                    pass

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            name = m.group(1)
            rules = [Rule.parse(r) for r in m.group(2).split(",")]
            altdest = m.group(3)
            return cls(name, rules, altdest)

class Part:
    PATTERN_BASE = re.compile(r"{(.+)}")
    PATTERN_ELEM = re.compile(r"(\w+)=(\d+)")

    @classmethod
    def parse(cls, s):
        mb = cls.PATTERN_BASE.match(s)
        if mb:
            out = dict()
            for xs in mb.group(1).split(","):
                mx = cls.PATTERN_ELEM.match(xs)
                if mx:
                    out[mx.group(1)] = int(mx.group(2))
            return out

@dataclass
class PartRange:
    data: dict[str, list[int]]

    def split(self, prop: str, at: int):
        pass

class System:
    def __init__(self, workflows, parts):
        self.workflows = {w.name: w for w in workflows}
        self.parts = parts

    def part1(self):
        accept = []
        reject = []

        for p in self.parts:
            current = 'in'
            while current != 'A' and current != 'R':
                workflow = self.workflows[current]
                current = workflow.eval(p)
                #print(current)
            #print(p)
            if current == 'A':
                accept.append(p)
            elif current == 'R':
                reject.append(p)

        return sum(sum(p.values()) for p in accept)

    @classmethod
    def read_file(cls, filename):
        ws, ps = aoc.split_xs(aoc.read_lines(filename), "")
        workflows = [Workflow.parse(w) for w in ws]
        parts = [Part.parse(p) for p in ps]
        return cls(workflows, parts)

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    from aoc import IntervalSeq
    inter = IntervalSeq.build([1, 10, 15, 20])
    for i in range(0, 22):
        a, b = inter.split(i)
        print(a, a.count(), b, b.count())

    test = System.read_file("input.txt")
    print(test.part1())

