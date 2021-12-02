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

increments = 0
prev_sum = input[0] + input[1] + input[2]
for i in range(3, len(input)):
    new_sum = prev_sum + input[i] - input[i-3]
    if new_sum > prev_sum:
        increments += 1
    prev_sum = new_sum
print(increments)