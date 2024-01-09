import argparse
import logging
import re
import sys

sys.path.append("..")
import aoc

class Record:
    def __init__(self, template, counts):
        self.template = template
        self.counts = [int(x) for x in counts.split(",")]
        self.unknown = len(list(filter(lambda x: x == "?", template)))
        self.total = sum(self.counts)

    def __repr__(self, ):
        cls = self.__class__.__name__
        return f"{cls}(template={self.template} counts={self.counts})"

    def gen_candidates(self):
        pass

    def fill_template(self, smissing):
        out = ""
        missing = iter(smissing)
        for c in self.template:
            if c == "?":
                out += next(missing)
            else:
                out += c
        return out

    @classmethod
    def fromfile(cls, filename):
        with open(filename, "r") as fh:
            for l in fh:
                l = l.strip()
                yield cls(*(l.split()))

def permute(npos, nneg):
    def p(s, l=""):
        if (len(s) < 1):
            #print(l+s)
            yield l+s
        else:
            uset = set()

        for i in range(len(s)):
            if s[i] in uset:
                continue
            else:
                uset.add(s[i])

            temp = ""
            if (i < len(s) - 1):
                temp = s[:i] + s[i+1:]
            else:
                temp = s[:i]

            yield from p(temp, l + s[i])

    s = ("#" * npos) + ("." * nneg)
    return p(s, "")




def main(args):
    rs = list(Record.fromfile(args.filename))

    #max_unknown = 0
    #for r in rs:
    #    print(r)
    #    if max_unknown < r.unknown:
    #        max_unknown = r.unknown
    #print(max_unknown)

    print(rs[0])

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args()

    main(args)