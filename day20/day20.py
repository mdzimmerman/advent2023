import re
import sys
from collections import deque

sys.path.append("..")
import aoc
from aoc import AocLogging

class Module:
    LOW = 0
    HIGH = 1

    PATTERN = re.compile(r"(.+) -> (.+)")

    def __init__(self, name: str, outputs: list[str]):
        self.name: str = name
        self.outputs: list[str] = outputs
        self.inputs: list[str] = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, out={self.outputs}, inp={self.inputs})"

    def handle_pulse(self, inp, pulse):
        return []

    @classmethod
    def parse(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            name = m.group(1)
            outputs = m.group(2).split(", ")
            if name == 'broadcaster':
                return Broadcaster(name, outputs)
            elif name[0] == '%':
                return FlipFlop(name[1:], outputs)
            elif name[0] == '&':
                return Conjunction(name[1:], outputs)

class FlipFlop(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.state: int = 0

    def handle_pulse(self, inp, pulse):
        if pulse == 1:
            return []
        elif pulse == 0:
            if self.state == 0:
                self.state = 1
                return [(self.name, out, 1) for out in self.outputs]
            else:
                self.state = 0
                return [(self.name, out, 0) for out in self.outputs]
        else:
            return []

class Conjunction(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.last_inputs: dict[str, int] = dict()

    def handle_pulse(self, inp, pulse):
        self.last_inputs[inp] = pulse
        pulse_out = None
        if sum(self.last_inputs.values()) == len(self.inputs):
            pulse_out = 0
        else:
            pulse_out = 1
        return [(self.name, out, pulse_out) for out in self.outputs]

class Broadcaster(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)

    def handle_pulse(self, inp, pulse):
        return [(self.name, out, pulse) for out in self.outputs]

class System(AocLogging):
    def __init__(self, instructions: list[str], level=AocLogging.WARN):
        super().__init__(level=level)
        self.instructions: list[str] = instructions
        self.modules: dict[str, Module] = self._build_modules(self.instructions)

    def state(self):
        out = dict()
        for k, m in self.modules.items():
            if isinstance(m, FlipFlop):
                out[k] = m.state
        return tuple(sorted(out.items()))

    def print_modules(self):
        for k, m in self.modules.items():
            print(f"{k} => {m}")

    def _build_modules(self, instructions: list[str]):
        modules: dict[str, Module] = dict()
        for inst in instructions:
            module = Module.parse(inst)
            if module is not None:
                modules[module.name] = module
        inputs = dict()
        for inp, m in modules.items():
            for out in m.outputs:
                if out not in inputs:
                    inputs[out] = []
                inputs[out].append(inp)
        for k, m in modules.items():
            if k in inputs:
                m.inputs = inputs[k]
        return modules

    def evaluate(self, inp0='button', out0='broadcaster', pulse0=0):
        queue = deque()
        queue.append((inp0, out0, pulse0))

        nlow, nhigh = 0, 0
        outputs = {}
        while queue:
            inp, out, pulse = queue.popleft()
            if pulse == 1:
                nhigh += 1
            else:
                nlow += 1
            self.debug(f"{inp} -{pulse}-> {out}")
            if out in self.modules:
                for i, o, p in self.modules[out].handle_pulse(inp, pulse):
                    queue.append((i, o, p))
            else:
                if out not in outputs:
                    outputs[out] = []
                outputs[out].append(pulse)
        return nlow, nhigh, outputs

    def part1(self):
        nlowtotal = 0
        nhightotal = 0
        for _ in range(1000):
            nlow, nhigh, _ = self.evaluate()
            nlowtotal += nlow
            nhightotal += nhigh
        self.info(nlowtotal, nhightotal)
        return nlowtotal * nhightotal

    @classmethod
    def from_file(cls, filename, level=AocLogging.WARN):
        return cls(aoc.read_lines(filename), level=level)


if __name__ == '__main__':
    print("-- test1 --")
    test1 = System.from_file("test1.txt", level=AocLogging.DEBUG)
    test1.print_modules()
    print()
    print(test1.evaluate())

    print()
    print("-- test2 --")
    test2 = System.from_file("test2.txt", level=AocLogging.DEBUG)
    test2.print_modules()
    print(test2.state())
    for _ in range(4):
        print()
        print(test2.evaluate())
        print(test2.state())

    test2b = System.from_file('test2.txt')
    print(test2b.part1())

    print()
    print("-- input --")
    inp = System.from_file("input.txt")
    #print(inp.part1())
    for i in range(10_000_000):
        if (i % 10_000) == 0:
            print(i)
        _, _, outputs = inp.evaluate()
        if outputs["rx"][0] == 0:
            print(i, outputs)
