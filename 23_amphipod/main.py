import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy
from collections import deque
from typing import OrderedDict
import math

# on x=10..12,y=10..12,z=10..12
# off x=9..11,y=9..11,z=9..11
pattern = r'(\w+) x=([0-9-]+)..([0-9-]+),y=([0-9-]+)..([0-9-]+),z=([0-9-]+)..([0-9-]+)'
def parse_file(filename):
    cave_map = {}
    with open(filename) as reader:
        r = 0
        for line in reader:
            line = line.rstrip()
            for c in range(0, len(line)):
                if line[c] in ['.', 'A', 'B', 'C', 'D']:
                    cave_map[(r,c)] = line[c]
            r+=1
    return cave_map

sample = parse_file('sample.txt')
input = parse_file('input.txt')
print("\n".join(map(lambda pair: str(pair), sample.items())))
print()
print("\n".join(map(lambda pair: str(pair), input.items())))

