#!/usr/bin/env python3

import random, sys, argparse, string


class Shuf:
    def __init__(self, sources, head_count, repeat=False, echo=False):
        self.lines = []
        self.head_count = head_count
        self.sources = sources
        self.repeat = repeat
        self.echo = echo

    def getline(self, source):
        for line in source:
            self.lines.append(line)
        random.shuffle(self.lines) 
        if self.head_count == float('inf') and not self.repeat:
            for line in self.lines:
                sys.stdout.write(str(line) + "\n")
        elif self.head_count == float('inf'):
            while True:
                r = random.choice(self.lines) 
                sys.stdout.write(str(r) + "\n") # caused pipe error for -h used to say print
        else:
            if self.repeat:
                x = range(0, self.head_count)
                for i in x:
                    r = random.choice(self.lines) 
                    sys.stdout.write(str(r) + "\n") # caused pipe error for -h used to say print
            else:
                i = 0
                for line in self.lines:
                    if (i < self.head_count):
                        sys.stdout.write(str(line) + "\n")
                        i += 1
                    else:
                        break

def parse_arguments():
    usage_msg = """Usage: shuf [OPTION]... [FILE]
  or:  shuf -e [OPTION]... [ARG]...
  or:  shuf -i LO-HI [OPTION]...
Write a random permutation of the input lines to standard output."""
    description_msg = """shuf shuffles its input by outputting a random permutation of its input lines. Each output permutation is equally likely."""
    
    parser = argparse.ArgumentParser(usage=usage_msg, description=description_msg)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--echo', action='store_true', help='treat each source file as a separate argument and print the corresponding lines together separated by the sources delimiter')
    group.add_argument('-i', '--input-range', metavar='LO-HI', help='treat each number LO through HI as an input line')
    parser.add_argument('-n', '--head-count', metavar='COUNT', type=int, default=float('inf'), help='output at most COUNT lines')
    parser.add_argument('-r', '--repeat', action='store_true', help='output lines can be repeated')
    parser.add_argument('sources', metavar='SOURCE', nargs='*', default=['-'], help='input sources')

    args = parser.parse_args()

    # Check the input_range validity
    if args.input_range:
        try:
            lo, hi = map(int, args.input_range.split('-'))
        except ValueError:
            parser.error('invalid input range: {0}'.format(args.input_range))
        sequence = list(range(lo, hi+1))
    
    shuffer=Shuf(args.sources, args.head_count, args.repeat, args.echo)

    match (args.sources, args.echo, args.input_range is not None):
        # -e
        case (sources, True, input_range):
            shuffer.getline(sources)
        # -i 
        case (sources, False, True):
            shuffer.getline(sequence)
        # read from standard input
        case (["-"], False, False):
            shuffer.getline(sys.stdin.read().splitlines())
        # read from file
        case ([filename], False, False):
            try:
                with open(filename, encoding="UTF-8") as file:
                    shuffer.getline(file.read().splitlines()) #used to say file
                                #f = open(filename, 'r')
                #shuffer.getline(f.readlines())
                #f.close()
            except FileNotFoundError:
                parser.error(f"Error: file '{filename}' not found.")
        case _:
            parser.error(f"extra operand: '{args.sources[1]}'")    

if __name__ == "__main__":
    parse_arguments()