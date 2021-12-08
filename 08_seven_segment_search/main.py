import sys
import re

pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda line : line.split(" | "),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)