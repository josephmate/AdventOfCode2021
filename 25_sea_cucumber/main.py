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
            map.append(line)
    return map

sample1 = parse_file("sample1.txt")
sample2 = parse_file("sample2.txt")
input = parse_file("input.txt")

print("\n".join(sample1))
print()
print("\n".join(sample2))