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
            is_on = match.group(1) == "on"
            lines.append((is_on,
                int(match.group(2)), int(match.group(3)),
                int(match.group(4)), int(match.group(5)),
                int(match.group(6)), int(match.group(7))
                ))
    return lines

sample_small = parse_file('sample_small.txt')
sample_large = parse_file('sample_large.txt')
input = parse_file('input.txt')

def solve_small(steps):
    on_cubes = set()

    for is_on, x1, x2, y1, y2, z1, z2 in steps:
        if (
            x1 >= -50 and x1 <= 50 and
            x2 >= -50 and x2 <= 50 and
            y1 >= -50 and y1 <= 50 and
            y2 >= -50 and y2 <= 50 and
            z1 >= -50 and z1 <= 50 and
            z2 >= -50 and z2 <= 50
        ):
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    for z in range(z1, z2+1):
                        if is_on:
                            on_cubes.add((x,y,z))
                        elif (x,y,z) in on_cubes:
                            on_cubes.remove((x,y,z))

    return len(on_cubes)

print("39")
print(solve_small(sample_small))
print("590784")
print(solve_small(sample_large))
print("input soln")
print(solve_small(input))