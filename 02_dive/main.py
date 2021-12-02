import sys

input = list(
    map(lambda pair : [pair[0], int(pair[1])],
    map(lambda line : line.split(" "),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))))

current_posn = 0
current_depth = 0
for (direction, magnitude) in input:
    if direction == "forward":
        current_posn += magnitude
    elif direction == "down":
        current_depth += magnitude
    elif direction == "up":
        current_depth -= magnitude
print(f"current_posn={current_posn} current_depth={current_depth} current_posn*current_depth={current_posn*current_depth}")

aim = 0
current_posn = 0
current_depth = 0
for (direction, magnitude) in input:
    if direction == "forward":
        current_posn += magnitude
        current_depth += aim*magnitude
    elif direction == "down":
        aim += magnitude
    elif direction == "up":
        aim -= magnitude
print(f"aim={aim} current_posn={current_posn} current_depth={current_depth} current_posn*current_depth={current_posn*current_depth}")