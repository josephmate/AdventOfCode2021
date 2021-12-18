import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json

input = list(
    map(lambda line : json.loads(line),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)


