import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
import copy

input = list(
    map(lambda line : list(map(lambda col: int(col), line)),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)
num_rows = len(input)
num_cols = len(input[0])

def handle_flashes(octopus_map):
    num_of_flashes = 0
    flashed = []
    for r in range(0, num_rows):
        current_row = []
        for c in range(0, num_cols):
            current_row.append(False)
        flashed.append(current_row)

    something_flashed = True
    while something_flashed:
        something_flashed = False
        for r in range(0, num_rows):
            for c in range(0, num_rows):
                if octopus_map[r][c] > 9 and not flashed[r][c]:
                    flashed[r][c] = True
                    num_of_flashes += 1
                    something_flashed = True
                    if r - 1 >= 0:
                        octopus_map[r-1][c] = octopus_map[r-1][c] + 1
                    if r + 1 < num_rows:
                        octopus_map[r+1][c] = octopus_map[r+1][c] + 1
                    if c - 1 >= 0:
                        octopus_map[r][c-1] = octopus_map[r][c-1] + 1
                    if c + 1 < num_cols:
                        octopus_map[r][c+1] = octopus_map[r][c+1] + 1
                    # diagonals
                    if r - 1 >= 0 and c - 1 >= 0:
                        octopus_map[r-1][c-1] = octopus_map[r-1][c-1] + 1
                    if r - 1 >= 0 and c + 1 < num_rows:
                        octopus_map[r-1][c+1] = octopus_map[r-1][c+1] + 1
                    if r + 1 < num_rows and c - 1 >= 0:
                        octopus_map[r+1][c-1] = octopus_map[r+1][c-1] + 1
                    if r + 1 < num_rows and c + 1 < num_rows:
                        octopus_map[r+1][c+1] = octopus_map[r+1][c+1] + 1

    # reset all values > 9 to 0
    for r in range(0, num_rows):
        for c in range(0, num_rows):
            if octopus_map[r][c] > 9:
                octopus_map[r][c] = 0

    return num_of_flashes

def simulate(steps, octopus_map):
    num_of_flashes = 0
    for step in range(1, steps+1):
        # increment everything
        for r in range(0, num_rows):
            for c in range(0, num_cols):
                octopus_map[r][c] = octopus_map[r][c]+1
        
        num_of_flashes += handle_flashes(octopus_map)
    
    
    for r in range(0, num_rows):
        for c in range(0, num_cols):
            print(octopus_map[r][c], end="")
        print("")

    return num_of_flashes

print('sample.txt 1656')
print(simulate(100, copy.deepcopy(input)))

def all_flash_step(octopus_map):
    flashed = []
    for r in range(0, num_rows):
        current_row = []
        for c in range(0, num_cols):
            current_row.append(False)
        flashed.append(current_row)

    something_flashed = True
    while something_flashed:
        something_flashed = False
        for r in range(0, num_rows):
            for c in range(0, num_rows):
                if octopus_map[r][c] > 9 and not flashed[r][c]:
                    flashed[r][c] = True
                    something_flashed = True
                    if r - 1 >= 0:
                        octopus_map[r-1][c] = octopus_map[r-1][c] + 1
                    if r + 1 < num_rows:
                        octopus_map[r+1][c] = octopus_map[r+1][c] + 1
                    if c - 1 >= 0:
                        octopus_map[r][c-1] = octopus_map[r][c-1] + 1
                    if c + 1 < num_cols:
                        octopus_map[r][c+1] = octopus_map[r][c+1] + 1
                    # diagonals
                    if r - 1 >= 0 and c - 1 >= 0:
                        octopus_map[r-1][c-1] = octopus_map[r-1][c-1] + 1
                    if r - 1 >= 0 and c + 1 < num_rows:
                        octopus_map[r-1][c+1] = octopus_map[r-1][c+1] + 1
                    if r + 1 < num_rows and c - 1 >= 0:
                        octopus_map[r+1][c-1] = octopus_map[r+1][c-1] + 1
                    if r + 1 < num_rows and c + 1 < num_rows:
                        octopus_map[r+1][c+1] = octopus_map[r+1][c+1] + 1

    # reset all values > 9 to 0
    for r in range(0, num_rows):
        for c in range(0, num_rows):
            if octopus_map[r][c] > 9:
                octopus_map[r][c] = 0

    for r in range(0, num_rows):
        for c in range(0, num_rows):
            if not flashed[r][c]:
                return False
    return True
    

def all_flash(octopus_map):
    for step in range(1, 1_000_000_000):
        # increment everything
        for r in range(0, num_rows):
            for c in range(0, num_cols):
                octopus_map[r][c] = octopus_map[r][c]+1
        
        if all_flash_step(octopus_map):
            return step

print("sample.txt 195")
print(all_flash(copy.deepcopy(input)))