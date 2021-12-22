import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy
from collections import deque

# on x=10..12,y=10..12,z=10..12
# off x=9..11,y=9..11,z=9..11
pattern = r'(\w+) x=([0-9-]+)..([0-9-]+),y=([0-9-]+)..([0-9-]+),z=([0-9-]+)..([0-9-]+)'
def parse_file(filename):
    lines = []
    with open(filename) as r:
        for line in r:
            line = line.rstrip()
            match = re.search(pattern, line)
            lines.append((match.group(1),
                match.group(2), match.group(3),
                match.group(4), match.group(5),
                match.group(6), match.group(7)
                ))
    return lines

sample_small = parse_file('sample_small.txt')
sample_large = parse_file('sample_large.txt')
input = parse_file('input.txt')

print(sample_small)
