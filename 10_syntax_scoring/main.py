import sys
import re
from queue import PriorityQueue


pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)
