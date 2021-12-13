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

coords_set = set(coords)

def print_coords_set(coords_set):
    min_y = min(map(lambda coords: coords[1], coords_set))
    max_y = max(map(lambda coords: coords[1], coords_set))
    min_x = min(map(lambda coords: coords[0], coords_set))
    max_x = max(map(lambda coords: coords[0], coords_set))

    print(f"{min_x},{min_y}")
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in coords_set:
                print("#", end="")
            else:
                print(".", end="")
        print("")

    for x in range(min_x, max_x+1):
        print(" ", end="")
    print(f"{max_x},{max_y}")

print_coords_set(coords_set)

def fold_up(coords_set, posn):
    # remove the yth row
    coords_to_process = []
    for (x,y) in coords_set:
        if y == posn:
            coords_to_process.append((x,y))
    for (x,y) in coords_to_process:
        coords_set.remove((x,y))
    
    # process anything higher than 7th row
    coords_to_process = []
    for (x,y) in coords_set:
        if y > posn:
            coords_to_process.append((x,y))
    for (x,y) in coords_to_process:
        coords_set.remove((x,y))

    # translate to flipped y point
    for (x,y) in coords_to_process:
        new_y = posn - (y-posn)
        coords_set.add((x,new_y))

def fold_left(coords_set, posn):
    # remove the yth row
    coords_to_process = []
    for (x,y) in coords_set:
        if x == posn:
            coords_to_process.append((x,y))
    for (x,y) in coords_to_process:
        coords_set.remove((x,y))
    
    # process anything higher than 7th row
    coords_to_process = []
    for (x,y) in coords_set:
        if x > posn:
            coords_to_process.append((x,y))
    for (x,y) in coords_to_process:
        coords_set.remove((x,y))

    # translate to flipped y point
    for (x,y) in coords_to_process:
        new_x = posn - (x-posn)
        coords_set.add((new_x, y))

def apply_fold(coords_set, fold):
    (direction, posn) = fold
    if direction == 'y':
        fold_up(coords_set, posn)
    if direction == 'x':
        fold_left(coords_set, posn)


apply_fold(coords_set, folds[0])
print_coords_set(coords_set)


print("sample.txt 17")
print(len(coords_set))

coords_set = set(coords)
for fold in folds:
    apply_fold(coords_set, fold)
print_coords_set(coords_set)