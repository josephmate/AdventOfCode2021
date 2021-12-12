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

incomplete_uncorrupted_lines = []
score = 0
for line in input:
    braces_stack = Stack()
    uncorrupted = True
    for char in line:
        if char in braces_lookup:
            braces_stack.put(char)
        else:
            char_to_match = braces_stack.get()
            if char != braces_lookup[char_to_match]:
                print(f"Expected {braces_lookup[char_to_match]}, but found {char} instead")
                score += score_lookup[char]
                uncorrupted = False
                break
    if uncorrupted:
        incomplete_uncorrupted_lines.append(line)

print(incomplete_uncorrupted_lines)
print(score)

score_lookup = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

scores = []
for line in incomplete_uncorrupted_lines:
    braces_stack = Stack()
    uncorrupted = True
    for char in line:
        if char in braces_lookup:
            braces_stack.put(char)
        else:
            char_to_match = braces_stack.get()
    score = 0
    # what ever is left in the stack
    while not braces_stack.empty():
        char_to_match = braces_stack.get()
        score = score * 5 + score_lookup[char_to_match]
    print(score)
    scores.append(score)

scores.sort()
# len(3)
# 3//2 = 1
# 0 1 2
mid_point = len(scores) // 2
print("median score")
print(scores[mid_point])
