import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))
input = input[0]


print("sample.txt 16   sample2.txt 12   sample3.txt 23   sample4.txt 31")
