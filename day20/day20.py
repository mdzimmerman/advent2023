import re
import sys
from collections import deque

sys.path.append("..")
import aoc

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
            return None
        elif pulse == 0:
            if self.state == 0:
                self.state = 1
                return [(self.name, out, Module.HIGH) for out in self.outputs]
            else:
                self.state = 0
                return [(self.name, out, Module.LOW) for out in self.outputs]
        else:
            return None

class Conjunction(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.last_inputs: dict[str, int] = dict()

    def handle_pulse(self, inp, pulse):
        self.last_inputs[inp] = pulse
        pulse_out = None
        if sum(self.last_inputs.values()) == len(self.outputs):
            pulse_out = Module.LOW
        else:
            pulse_out = Module.HIGH
        return [(self.name, out, pulse_out) for out in self.outputs]

class Broadcaster(Module):
    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)

    def handle_pulse(self, inp, pulse):
        return [(self.name, out, pulse) for out in self.outputs]

class System:
    def __init__(self, instructions: list[str]):
        self.instructions: list[str] = instructions
        self.modules: dict[str, Module] = self._build_modules(self.instructions)

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

    def evaluate(self, inp0, out0, pulse0):
        queue = deque()
        queue.append((inp0, out0, pulse0))

        while queue:
            inp, out, pulse = queue.popleft()
            print(f"{inp} -{pulse}-> {out}")
            for i, o, p in self.modules[out].handle_pulse(inp, pulse):
                queue.append((i, o, p))


    @classmethod
    def from_file(cls, filename):
        return cls(aoc.read_lines(filename))


if __name__ == '__main__':
    test1 = System.from_file("test1.txt")
    for k, m in test1.modules.items():
        print(k, m)
    print()
    test1.evaluate("button", "broadcaster", Module.LOW)