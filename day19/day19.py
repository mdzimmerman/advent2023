from dataclasses import dataclass
import re
import sys

sys.path.append("..")
import aoc

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

    def evalrange(self, partrange: PartRange):
        //x = partrange.copy()
        for rule in self.rules:
            if rule.op == '<':
                a, b = partrange
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

class PartRange:
    KEYS = ['x', 'm', 'a', 's']

    def __init__(self, **kwargs):
        self.data = dict()
        for k, v in kwargs.items():
            if k in self.__class__.KEYS:
                self.data[k] = v

    def __getitem__(self, key):
        if key in self.__class__.KEYS:
            return dict.__getitem__(self.data, key)

    def __setitem__(self, key, val):
        if key in self.__class__.KEYS:
            return dict.__setitem__(self.data, key, val)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"

    def _filter_bad_range(self, pr):
        for k in self.__class__.KEYS:
            if not pr[k]:
                return None
        return pr

    def ncombos(self):
        out = 1
        for k in self.__class__.KEYS:
            it = iter(self.data[k])
            count = 0
            for xmin, xmax in zip(it, it):
                count += (xmax-xmin+1)
            out *= count
        return out

    def split(self, key, value):
        a = PartRange()
        b = PartRange()
        for k in self.__class__.KEYS:
            if k == key:
                a[k] = []
                b[k] = []
                it = iter(self.data[k])
                for xmin, xmax in zip(it, it):
                    if value <= xmin:
                        a[k].extend([xmin, xmax])
                    elif xmin < value <= xmax:
                        a[k].extend([xmin, value-1])
                        b[k].extend([value, xmax])
                    else:
                        b[k].extend([xmin, xmax])
            else:
                a[k] = self.data[k][:]
                b[k] = self.data[k][:]
        return self._filter_bad_range(a), self._filter_bad_range(b)

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
    part = PartRange(x=[1,4000], m=[1,4000], a=[1,4000], s=[1, 4000])
    for v in [1, 2000, 4000, 4001]:
        print(v)
        a, b = part.split('a', v)
        an = 0
        if a is not None:
            an = a.ncombos()
        bn = 0
        if b is not None:
            bn = b.ncombos()
        print(f"    {a} {an}")
        print(f"    {b} {bn}")