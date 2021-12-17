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
print("")

def simulate(vx, vy, x1, x2, y1, y2):
    trajectory = [(vx, vy)]
    current_x = vx
    current_y = vy
    while True:
        #Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater than 0, increases by 1 if it is less than 0, or does not change if it is already 0.
        if vx > 0:
            vx = vx - 1
        #Due to gravity, the probe's y velocity decreases by 1.
        vy = vy - 1
        
        #The probe's x position increases by its x velocity.
        current_x += vx
        #The probe's y position increases by its y velocity.
        current_y += vy
        trajectory.append((current_x, current_y))

        if current_x > x2 or current_y < y1:
            break;
    return trajectory

print_trajectory(sample[0], sample[1], sample[2], sample[3], 
    simulate(7, 2, sample[0], sample[1], sample[2], sample[3]))
print("")
print_trajectory(sample[0], sample[1], sample[2], sample[3], 
    simulate(6, 3, sample[0], sample[1], sample[2], sample[3]))
print("")
print_trajectory(sample[0], sample[1], sample[2], sample[3], 
    simulate(9, 0, sample[0], sample[1], sample[2], sample[3]))
print("")
print_trajectory(sample[0], sample[1], sample[2], sample[3], 
    simulate(17, -4, sample[0], sample[1], sample[2], sample[3]))
print("")

def hit(trajectory, x1, x2, y1, y2):
    for (x,y) in trajectory:
        if x >= x1 and x <= x2 and y <= y2 and y >= y1:
            return True
    return False

def find_highest(x1, x2, y1, y2):
    highest = 0
    for x in range(0, x2+1):
        for y in range(0, abs(y1)+1):
            trajectory = simulate(x,y, x1,x2,y1,y2)
            if hit(trajectory, x1,x2,y1,y2):
                current_max_height = max(map(lambda xy: xy[1], trajectory))
                if current_max_height > highest:
                    highest = current_max_height
    return highest

print(hit(simulate(7, 2, sample[0], sample[1], sample[2], sample[3]), sample[0], sample[1], sample[2], sample[3]))
print("45")
print(find_highest(sample[0], sample[1], sample[2], sample[3]))
print("")
print(find_highest(input[0], input[1], input[2], input[3]))