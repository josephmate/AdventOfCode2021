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
