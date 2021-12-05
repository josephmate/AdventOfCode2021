import sys
import re

pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda match : [
        [int(match.group(1)), int(match.group(2))],
        [int(match.group(3)), int(match.group(4))],
    ],
    map(lambda line : re.search(pattern, line),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))))

print(input)

collisions = {}
for ((x1, y1),(x2,y2)) in input:
    if x1 == x2:
        if y1 <= y2:
            lower_y = y1
            bigger_y = y2
        else:
            lower_y = y2
            bigger_y = y1

        for i in range(lower_y, bigger_y+1):
            collisions[(x1, i)] = collisions.get((x1, i), 0) + 1
    elif y1 == y2:

        if x1 <= x2:
            lower_x = x1
            bigger_x = x2
        else:
            lower_x = x2
            bigger_x = x1
        for i in range(lower_x, bigger_x+1):
            collisions[(i, y1)] = collisions.get((i, y1), 0) + 1

def print_collisions(collisions):
    max_x = 0
    max_y = 0
    for ((x,y), count) in collisions.items():
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
    for y in range(0, max_y+1):
        for x in range(0, max_x+1):
            if (x,y) in collisions:
                print(str(collisions[(x,y)]), end="")
            else:
                print(".", end = "")
        print("")


print_collisions(collisions)

too_many_collisions = 0
for ((x,y), count) in collisions.items():
    if (count >= 2):
        too_many_collisions += 1

print(too_many_collisions)

