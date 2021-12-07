import sys
import re

pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

input = list (
    map(
        lambda column: int(column),
        input[0].split(",")
    )
)
print(input)

min_posn = min(input)
max_posn = max(input)

def calc_fuel(target_posn, posns) :
    sum = 0
    for posn in posns:
        sum += abs(posn - target_posn)
    return sum

min_fuel = 1000000000
target_posn = -1
for posn in range(min_posn, max_posn+1):
    fuel = calc_fuel(posn, input)
    if fuel < min_fuel:
        min_fuel = fuel
        target_posn = posn
print(f"min_fuel={min_fuel} target_posn={target_posn}")

def calc_movement(posn, target_posn):
    delta = abs(posn - target_posn)
    sum = 0
    for i in range(1, delta+1):
        sum += i
    return sum

def calc_expensive_fuel(target_posn, posns) :
    sum = 0
    for posn in posns:
        sum += calc_movement(posn, target_posn)
    return sum

min_fuel = 1000000000
target_posn = -1
for posn in range(min_posn, max_posn+1):
    fuel = calc_expensive_fuel(posn, input)
    if fuel < min_fuel:
        min_fuel = fuel
        target_posn = posn
print(f"min_fuel={min_fuel} target_posn={target_posn}")

