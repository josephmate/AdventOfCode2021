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
from heapq import *
import time
from collections import deque

def parse_file(filename):
    map = []
    with open(filename) as reader:
        for line in reader:
            line = line.rstrip()
            map.append(list(line))
    return map

sample1 = parse_file("sample1.txt")
sample2 = parse_file("sample2.txt")
input = parse_file("input.txt")

print("\n".join(map(lambda l: ''.join(l), sample1)))
print()
print("\n".join(map(lambda l: ''.join(l), sample2)))



def simulate_steps(map, steps = None):
    step = 0
    while True:
        if steps != None:
            if step >= steps:
                break
        step += 1

        noone_moved = True

        next_map = copy.deepcopy(map)
        # move east herd
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == '>' and map[i][(j+1)%len(map[i])] == '.':
                    noone_moved = False
                    next_map[i][j] = '.'
                    next_map[i][(j+1)%len(map[i])] = '>'
        map = next_map
        next_map = copy.deepcopy(map)
        # move south herd
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 'v' and map[(i+1)%len(map)][j] == '.':
                    noone_moved = False
                    next_map[i][j] = '.'
                    next_map[(i+1)%len(map)][j] = 'v'
        map = next_map
        if noone_moved:
            break
    return (step, map)




print()
expected = """>......
..v....
..>.v..
.>.v...
...>...
.......
v......"""
print("Expected:")
print(expected)
print()
(_, actual) = simulate_steps(sample1, 4)
actual = "\n".join(map(lambda l: ''.join(l), actual))
print("Actual:")
print(actual)
assert expected == actual

(steps, actual) = simulate_steps(sample2)
print(f"Expected: {58}")
print(f"Actual:   {steps}")
print()
(steps, actual) = simulate_steps(input)
print(steps)