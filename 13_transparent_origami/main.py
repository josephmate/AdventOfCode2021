import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

# 1,2
coord_pattern = r'(\d+),(\d+)'
# fold along y=7
fold_pattern = r'fold along (\w+)=(\d+)'
input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)

coords = list(
    map(lambda match: ( int(match.group(1)), int(match.group(2))),
    filter(lambda match: not match == None,
    map(lambda line: re.search(coord_pattern, line),
    input))))
print(coords)
folds = list(
    map(lambda match: (match.group(1), int(match.group(2))),
    filter(lambda match: not match == None,
    map(lambda line : re.search(fold_pattern, line),
    input))))
print(folds)