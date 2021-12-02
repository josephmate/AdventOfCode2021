import sys

input = list(
    map(lambda line : int(line),
        map(lambda line : line.rstrip(),
            sys.stdin.readlines())
    )
)

increments = 0
prev_depth = input[0]
for current_depth in input:
    if current_depth > prev_depth:
        increments += 1
    prev_depth = current_depth
print(increments)
