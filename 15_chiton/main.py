import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

input = list(
    map(lambda line : list(map(lambda c: int(c), line)),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)