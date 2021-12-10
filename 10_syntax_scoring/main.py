import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack

pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)

score_lookup = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

braces_lookup = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
braces_lookup_rev = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

score = 0
for line in input:
    braces_stack = Stack()
    for char in line:
        if char in braces_lookup:
            braces_stack.put(char)
        else:
            char_to_match = braces_stack.get()
            if char != braces_lookup[char_to_match]:
                print(f"Expected {braces_lookup[char_to_match]}, but found {char} instead")
                score += score_lookup[char]
                continue

print(score)