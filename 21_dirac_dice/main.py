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
print()

dice_roll_count_map = {}
for i in range(1, 3+1):
    for j in range(1, 3+1):
        for k in range(1,3+1):
            sum = i+k+j
            dice_roll_count_map[sum] = dice_roll_count_map.get(sum, 0) + 1
print(dice_roll_count_map)
dice_roll_counts = []
for (roll, count) in dice_roll_count_map.items():
    dice_roll_counts.append((roll,count))

def simulate_dirac_dice_impl(turn, p1, p2, s1, s2, memoization_map, winning_score):
    if turn == 2 and s1 >= winning_score:
        return (1,0)
    if turn == 1 and s2 >= winning_score:
        return (0,1)
    if (turn, p1, p2, s1, s2) in memoization_map:
        return memoization_map[(turn, p1, p2, s1, s2)]

    p1_wins = 0
    p2_wins = 0
    for (roll, count) in dice_roll_counts:
        if turn == 1:
            next = p1 + roll
            if next > 10:
                next = next - 10
            (sub_p1_wins, sub_p2_wins) = simulate_dirac_dice_impl(
                2,
                next,
                p2,
                s1 + next,
                s2,
                memoization_map,
                winning_score
            )
            p1_wins += count*sub_p1_wins
            p2_wins += count*sub_p2_wins
        else:
            next = p2 + roll
            if next > 10:
                next = next - 10
            (sub_p1_wins, sub_p2_wins) = simulate_dirac_dice_impl(
                1,
                p1,
                next,
                s1,
                s2 + next,
                memoization_map,
                winning_score
            )
            p1_wins += count*sub_p1_wins
            p2_wins += count*sub_p2_wins
    memoization_map[(turn, p1, p2, s1, s2)] = (p1_wins, p2_wins)
    return (p1_wins, p2_wins)



def simulate_dirac_dice(players, winning_score):
    return simulate_dirac_dice_impl(1, players[0], players[1], 0, 0, {}, winning_score)

# translated positions back to 1 to 10 index for convenience
sample = [4,8]
input = [8,9]

# player1=4 , player2=8
# winning score 1
# player 1 rolls 1 2 3 
#                5 6 7
# so that means for score 1 to 5, we expect players one to win in 1 roll
# for 6 is when the chances start opening up for players 2
# Player 1     Player 2       Player 1          Result
#    5            9              X                2
#                10              X                2
#                 1              6                1
#                                7                1
#                                8                1
#    6           X                                1
#    7           X                                1
#
# winning score = 7
# Player 1     Player 2       Player 1    Player 2      Result
#    5            9              X                        2
#                10              X                        2
#                 1              11                       1
#                                12                       1
#                                13                       1
#    6           9               X                        2
#               10               X                        2
#                1               13                       1
#                                14                       1
#                                15                       1
#    7           X                                        1
# AHHHH this was all wrong! i'm suppose to roll 3 dice per turn :(
for i in range(1, 11):
    print(f"{i} {simulate_dirac_dice(sample, i)}")
print()
print(simulate_dirac_dice(sample, 21))
print((444356092776315, 341960390180808))
print(simulate_dirac_dice(input, 21))