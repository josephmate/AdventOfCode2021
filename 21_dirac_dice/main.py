import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json
import copy
from collections import deque

sample = [4,8]
input = [8,9]
# translated to 0 index the input becomes
sample = [3,7]
input = [7,8]

def roll_dice(dice):
    dice = dice + 1
    if dice > 100:
        dice = 1
    return dice

def simulate(players):
    last_roll = 100
    scores = [0, 0]
    roll_count = 0
    current_position = players.copy()
    while True:
        for i in range(0, len(players)):
            roll1 = roll_dice(last_roll)
            roll_count+=1
            roll2 = roll_dice(roll1)
            roll_count+=1
            roll3 = roll_dice(roll2)
            roll_count+=1
            last_roll = roll3
            current_position[i] = (current_position[i] + roll1 + roll2 + roll3) % 10
            scores[i] += current_position[i] + 1
            #print(f"Player {i+1} rolls {roll1}+{roll2}+{roll3} and moves to space {current_position[i]+1} for a total score of {scores[i]}")
            if scores[i] >= 1000:
                return (scores[ (i+1)%2 ], roll_count)

(loser_score, roll_count) = simulate(sample)
print(f"loser_score={loser_score} roll_count={roll_count} product={loser_score*roll_count}")
(loser_score, roll_count) = simulate(input)
print(f"loser_score={loser_score} roll_count={roll_count} product={loser_score*roll_count}")