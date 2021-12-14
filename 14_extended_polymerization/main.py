import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)
print(input[0])
print(input[2:len(input)])

pattern = r'(\w+) -> (\w+)'
polymer_template = input[0]
insertion_rules = list(
    map(lambda match: (match.group(1), match.group(2)),
    map(lambda line: re.search(pattern, line),
    input[2:len(input)])))

print(pattern)
print(insertion_rules)