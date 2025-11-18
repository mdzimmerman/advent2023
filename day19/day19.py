from collections import deque
from dataclasses import dataclass
import re
import sys

sys.path.append("..")
import aoc
from aoc import AocLogging

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

    def evalrange(self, part):
        out = []
        curr = part
        for rule in self.rules:
            yes, no = curr.split(rule.prop, rule.op, rule.value)
            out.append((rule.dest, yes))
            curr = no
        out.append((self.altdest, curr))
        return out

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

    def split(self, key, op, value):
        yes = PartRange()
        no  = PartRange()
        for k in self.__class__.KEYS:
            if k == key:
                yes[k] = []
                no[k]  = []
                it = iter(self.data[k])
                if op == '<':
                    for xmin, xmax in zip(it, it):
                        if value <= xmin:
                            yes[k].extend([xmin, xmax])
                        elif xmin < value <= xmax:
                            yes[k].extend([xmin, value-1])
                            no[k].extend([value, xmax])
                        else:
                            no[k].extend([xmin, xmax])
                elif op == '>':
                    for xmin, xmax in zip(it, it):
                        if value < xmin:
                            no[k].extend([xmin, xmax])
                        elif xmin <= value < xmax:
                            yes[k].extend([value+1, xmax])
                            no[k].extend([xmin, value])
                        else:
                            yes[k].extend([xmin, xmax])
            else:
                yes[k] = self.data[k][:]
                no[k] = self.data[k][:]
        return yes, no

class System(AocLogging):
    def __init__(self, workflows, parts, level=AocLogging.WARN):
        super().__init__(level=level)
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

    def part2(self):
        allpart = PartRange(x=[1,4000], m=[1,4000], a=[1,4000], s=[1,4000])

        queue = deque()
        queue.append(("in", allpart))

        accept = []
        reject = []
        while queue:
            flow, part = queue.popleft()
            self.debug(flow, part)
            if flow == 'A':
                accept.append(part)
            elif flow == 'R':
                reject.append(part)
            else:
                workflow = self.workflows[flow]
                for f, p in workflow.evalrange(part):
                    queue.append((f, p))

        self.debug("rejected:")
        cr = 0
        for r in reject:
            cr += r.ncombos()
            self.debug(f"  {r} {r.ncombos()}")

        ca = 0
        self.debug("accepted:")
        for a in accept:
            ca += a.ncombos()
            self.debug(f"  {a} {a.ncombos()}")

        cmax = allpart.ncombos()
        #print(cmax)
        #print(ca + cr)
        #print(cmax - (ca+cr))
        #print(ca + (cmax-(ca+cr)))

        #print()
        return ca

    @classmethod
    def read_file(cls, filename, level=aoc.AocLogging.WARN):
        ws, ps = aoc.split_xs(aoc.read_lines(filename), "")
        workflows = [Workflow.parse(w) for w in ws]
        parts = [Part.parse(p) for p in ps]
        return cls(workflows, parts, level=level)

if __name__ == '__main__':
    logger = AocLogging(level=AocLogging.WARN)
    part = PartRange(x=[1,4000], m=[1,4000], a=[1,4000], s=[1, 4000])
    for v in [1, 2000, 4000, 4001]:
        logger.debug(v)
        a, b = part.split('a', '<', v)
        an = 0
        if a is not None:
            an = a.ncombos()
        bn = 0
        if b is not None:
            bn = b.ncombos()
        logger.debug(f"    {a} {an}")
        logger.debug(f"    {b} {bn}")

    logger.debug()
    workflow = Workflow.parse("in{a>1000:out1,m<1000:out2,x>4000:out3,out4}")
    logger.debug(workflow)
    for k, v in workflow.evalrange(part):
        logger.debug(k, v)

    test = System.read_file("test.txt", level=AocLogging.WARN)
    inp  = System.read_file("input.txt", level=AocLogging.WARN)

    print("-- part #1 --")
    print("test =", test.part1())
    print("inp  =", inp.part1())

    print()
    print("-- part #2 --")
    print("test =", test.part2())
    print("inp  =", inp.part2())

    print()
