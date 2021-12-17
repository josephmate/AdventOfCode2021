import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import math

sample = "target area: x=20..30, y=-10..-5"
input = "target area: x=94..151, y=-156..-103"

pattern = r'target area: x=([0-9-]+)..([0-9-]+), y=([0-9-]+)..([0-9-]+)'
def parse(desc):
    match = re.search(pattern, desc)
    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)), )

sample = parse(sample)
input = parse(input)
print(sample)
print(input)

def print_trajectory(x1,x2,y1,y2,trajectory):
    trajectory_set = set(trajectory)
    values = trajectory.copy()
    values.append((x1,y1))
    values.append((x2,y2))
    values.append((0,0))
    min_x = min(map(lambda xy: xy[0], values))
    max_x = max(map(lambda xy: xy[0], values))
    min_y = min(map(lambda xy: xy[1], values))
    max_y = max(map(lambda xy: xy[1], values))

    for y in range(max_y, min_y-1, -1):
        for x in range(min_x, max_x+1):
            if (x,y) in trajectory_set:
                print("#", end="")
            elif (x,y) == (0,0):
                print("S", end="")
            elif x >= x1 and x <= x2 and y >= y1 and y <= y2:
                print("T", end="")
            else:
                print(".", end="")
        print("")

print_trajectory(sample[0], sample[1], sample[2], sample[3], [])

