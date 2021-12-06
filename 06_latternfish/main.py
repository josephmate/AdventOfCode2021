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

fish_timers = []
for i in range(0, 8+1):
    fish_timers.append(0)

for fish_timer in input:
    fish_timers[fish_timer] += 1
print(fish_timers)


for day in range(1, 80+1):
    new_fish_timers = []
    for i in range(0, 8+1):
        new_fish_timers.append(0)
    
    for i in range(1, 8+1):
        new_fish_timers[i-1] = fish_timers[i]
    
    new_fish_timers[8] = fish_timers[0]
    new_fish_timers[6] += fish_timers[0]

    fish_timers = new_fish_timers

print(sum(fish_timers))
