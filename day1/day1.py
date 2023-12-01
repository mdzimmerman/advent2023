import argparse
import re

word2digit = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9}

def to_digit(s):
    if s in word2digit:
        return word2digit[s]
    else:
        return int(s)

def get_digitpatt(part):
    if part == 1:
        return re.compile(r'(\d)')
    else:
        return re.compile(r'(\d|one|two|three|four|five|six|seven|eight|nine)')

def main(args):
    digitpatt = get_digitpatt(args.part)

    with open(args.filename, "r") as fh:
        total = 0
        for l in fh:
            l = l.strip()
            n = []
            for i in range(len(l)):
                m = digitpatt.match(l[i:])
                if m:
                    n.append(to_digit(m.group(0)))
            number = int(str(n[0])+str(n[-1]))
            print(f"{l:70s} {str(n):30s} {number}")
            total += number
        print(total)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--part', '-p', type=int, default=1)
    args = parser.parse_args()

    main(args)