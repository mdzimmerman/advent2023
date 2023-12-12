import argparse
from dataclasses import dataclass
import re
import sys

sys.path.append("..")
import aoc
from aoc import Interval

@dataclass
class Function:
    source: Interval
    offset: int
    dest: Interval

@dataclass
class AlmanacEntry:
    dest_start: int
    source_start: int
    range_length: int

    def in_range(self, x):
        return self.source_start <= x < self.source_start + self.range_length

def indent(levels=0):
    return "  " * levels

class AlmanacMap:
    header_patt = re.compile(r"(.+)-to-(.+) map:")

    def __init__(self, lines):
        self.intype, self.outtype = self._parse_header(lines[0])
        self.entries = self._parse_entries(lines[1:])

    def _parse_header(self, header):
        m = self.__class__.header_patt.match(header)
        if m:
            return m.group(1), m.group(2)
        else:
            return None, None

    def _parse_entries(self, lines):
        out = []
        for l in lines:
            out.append(AlmanacEntry(*(int(x) for x in l.split())))
        return sorted(out, key=lambda e: e.source_start)

    def __repr__(self):
        return f"{self.__class__.__name__}(" \
               f"intype={self.intype} " \
               f"outtype={self.outtype} " \
               f"entries={self.entries})"

    def pretty_print(self, n=0):
        print(f"{indent(n)}{self.__class__.__name__}(")
        print(f"{indent(n+1)}intype={self.intype}")
        print(f"{indent(n+1)}outtype={self.outtype}")
        print(f"{indent(n+1)}entries=[")
        for entry in self.entries:
            print(f"{indent(n+2)}{entry}")
        print(f"{indent(n+1)}])")

    def lookup(self, source):
        for e in self.entries:
            if e.source_start <= source < e.source_start+e.range_length:
                diff = source - e.source_start
                return e.dest_start + diff
        return source

class Almanac:
    seedpatt = re.compile(r'seeds: (.+)')

    def __init__(self, filename):
        self.filename = filename
        lines = aoc.read_lines(filename)
        paragraphs = aoc.split_xs(lines, "")
        self.seeds = self._parse_seeds(paragraphs[0][0])
        self.maps = {}
        for para in paragraphs[1:]:
            map = AlmanacMap(para)
            self.maps[map.intype] = map
            #AlmanacMap(para).pretty_print()

    def _parse_seeds(self, s):
        m = self.__class__.seedpatt.match(s)
        if m:
            return [int(n) for n in m.group(1).split()]
        else:
            return []

    def __repr__(self):
        return f"{self.__class__.name}(seeds={self.seeds} maps={self.maps})"

    def pretty_print(self, n=0):
        print(f"{indent(n)}{self.__class__.__name__}(")
        print(f"{indent(n+1)}seeds={self.seeds}")
        print(f"{indent(n+1)}maps=[")
        for key, e in self.maps.items():
            print(f"{indent(n+2)}'{key}':")
            e.pretty_print(n+2)
        print(f"{indent(n)}])")

    def to_location(self, seed):
        currtype = "seed"
        currid = seed
        while currtype != "location":
            map = self.maps[currtype]
            newtype = map.outtype
            newid = map.lookup(currid)
            #print(f"{currtype} {currid} -> {newtype} {newid}")
            currtype = newtype
            currid = newid
        return currid

    def build_functions(self, outtype, xmin, xmax):
        map = self.maps[outtype]
        print(xmin, xmax)
        fs = []
        x0 = 0
        for e in map.entries:
            source_range = Interval(e.source_start, e.source_start + e.range_length)
            dest_range = Interval(e.dest_start, e.dest_start + e.range_length)
            offset = e.dest_start - e.source_start
            if x0 < source_range.start:
                fs.append(Function(Interval(x0, source_range.start), 0, Interval(x0, source_range.start)))
            fs.append(Function(source_range, offset, dest_range))
            x0 = source_range.end
        if x0 < xmax:
            fs.append(Function(Interval(x0, xmax), 0, Interval(x0, xmax)))
        for f in fs:
            print(f)
        return fs


def main(args):
    almanac = Almanac(args.filename)
    locations = []
    for seed in almanac.seeds:
        location = almanac.to_location(seed)
        locations.append(location)
        #print(seed, location)

    print(f"part1 = {min(locations)}")

    #almanac.to_location(79)
    #almanac.pretty_print()
    #for n in range(100):
    #    print(n, almanac.maps["seed"].lookup(n))

    #print(almanac.seeds)
    #for k, v in almanac.maps.items():
    #    print(k, v)

    def apply_piecewise(fs, gtype):
        xmin = 0
        xmax = max(x.dest.end for x in fs)
        gs = almanac.build_functions(gtype, xmin, xmax)
        print()
        for f in fs:
            # print(f)
            for g in gs:
                inter = f.dest.intersect(g.source)
                if inter is not None:
                    inter_offset = inter.start - f.dest.start
                    inter_len = len(inter)
                    source = Interval(f.source.start + inter_offset, f.source.start + inter_offset + inter_len)
                    offset = f.offset + g.offset
                    dest = Interval(source.start + offset, source.end + offset)
                    fg = Function(source, offset, dest)
                    print(fg)

    print('seed')
    fseed = almanac.build_functions('seed', 0, 100)
    #print('soil')
    #functs_soil = almanac.build_functions('soil')
    apply_piecewise(fseed, 'soil')



    # i = 0
    # j = 0
    # x0 = 0
    # for _ in range(20):
    #     if functs_seed[i].end == functs_soil[j].end:
    #         x1 = functs_seed[i].end
    #         i += 1
    #         j += 1
    #     elif functs_seed[i].end < functs_soil[j].end:
    #         x1 = functs_seed[i].end
    #         i += 1
    #     else:
    #         x1 = functs_soil[j].end
    #         j += 1
    #
    #     x1 = min(functs_seed[i].end, functs_soil[j].end)
    #     if functs_seed[i].end < functs_soil[j]:




if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")

    # parse logging level
    args = parser.parse_args(['-f', 'test.txt'])
    main(args)