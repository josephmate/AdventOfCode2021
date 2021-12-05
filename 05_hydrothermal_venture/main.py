import sys

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print(input)