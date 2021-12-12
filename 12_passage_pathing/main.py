import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack


input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)

