import argparse
import logging
import re
import sys

sys.path.append("..")
import aoc

class Record:
    def __init__(self, template, counts):
        self.template = template
        self.pos_counts = [int(x) for x in counts.split(",")]
        self.pos_counts_str = counts
        self.tmpl_unk = len(list(filter(lambda x: x == "?", self.template)))
        self.tmpl_pos = len(list(filter(lambda x: x == "#", self.template)))
        self.pos_total = sum(self.pos_counts)

    def __repr__(self, ):
        cls = self.__class__.__name__
        return f"{cls}(template={self.template} pos_counts={self.pos_counts})"

    def count_candidates(self):
        return sum(1 for _ in self.gen_candidates())

    def gen_candidates(self):
        pos_needed = self.pos_total - self.tmpl_pos
        neg_needed = self.tmpl_unk - pos_needed
        for p in permute(pos_needed, neg_needed):
            #print(p)
            cand = self.fill_template(p)
            cand_counts_str = ",".join(str(x) for x in self.count(cand))
            if cand_counts_str == self.pos_counts_str:
                yield cand
                #print(cand)

    def fill_template(self, smissing):
        out = ""
        missing = iter(smissing)
        for c in self.template:
            if c == "?":
                out += next(missing)
            else:
                out += c
        return out

    def count(self, candidate):
        counts = []
        ingroup = False
        for c in candidate:
            if ingroup:
                if c == "#":
                    counts[-1] += 1
                else:
                    ingroup = False
            else:
                if c == "#":
                    counts.append(1)
                    ingroup = True
        return counts

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

    ntotal = 0
    for r in rs:
        ncand = r.count_candidates()
        ntotal += ncand
        print(r, ncand)
    print(ntotal)

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default="input.txt")
    args = parser.parse_args()

    main(args)