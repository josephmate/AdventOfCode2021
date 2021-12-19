import sys
import re
from queue import PriorityQueue
from queue import LifoQueue as Stack
from queue import Queue
import json

input = list(
    map(lambda line : json.loads(line),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    )))

print(input)

# [[1,2], 3]
#    /  \ 
#   / \  3
#   1 2
#
#  [1, [2, 3]]
#    / \
#   1  / \
#     2   3
#
#
#   [[1,[2,3]],4]
#    / \
#   / \  4  
#  1 / \
#    2 3 
#
#  [1,[[2,3], 4]]]
#     / \
#    1 / \
#     / \ 4
#     2 3
#  [[1 ,2],[3,4]]
#        / \
#       /\ /\
#      1 2 3 4
#
#  [[[[[1,2],3],4],5],6]
#        /\
#       /\ 6
#      /\ 5
#     /\ 4
#    /\ 3
#   1  2

def go_left_until_int(val, sn):
    if isinstance(sn[0], int):
        sn[0] += val
    else:
        go_left_until_int(val, sn[0])

def explode_to_right(val, parent_stack):
    # go up until you can go to the right
    while not parent_stack.empty():
        (parent, direction) = parent_stack.get()
        if direction == "left":
            if isinstance(parent[1], int):
                parent[1] += val
            else:
                go_left_until_int(val, parent[1])
            return


def go_right_until_int(val, sn):
    if isinstance(sn[1], int):
        sn[1] += val
    else:
        go_right_until_int(val, sn[1])

def explode_to_left(val, parent_stack):
    # go up until you can go to the left
    while not parent_stack.empty():
        (parent, direction) = parent_stack.get()
        if direction == "right":
            if isinstance(parent[0], int):
                parent[0] += val
            else:
                go_right_until_int(val, parent[0])
            return

def sn_explode(sn, parent_stack):
    (parent, direction) = parent_stack.get()
    if direction == 'left':
        parent[0] = 0
    else:
        parent[1] = 0
    parent_stack.put((parent, direction))
    explode_to_left(sn[0], parent_stack)
    explode_to_right(sn[1], parent_stack)

def sn_try_explode_impl(sn, count, parent_stack):
    if isinstance(sn, int):
        return False
    else:
        count += 1
        if isinstance(sn[0], int) and isinstance(sn[1], int):
            if count > 4:
                sn_explode(sn, parent_stack)
                return True
            else:
                return False
        
        if isinstance(sn[0], list):
            parent_stack.put((sn, 'left'))
            if sn_try_explode_impl(sn[0], count, parent_stack):
                return True
        if isinstance(sn[1], list):
            parent_stack.put((sn, 'right'))
            if sn_try_explode_impl(sn[1], count, parent_stack):
                return True
            parent_stack.get()
        return False
    

def sn_try_explode(sn):
    return sn_try_explode_impl(sn, 0, Stack())

def sn_try_split(sn):
    return False

def sn_reduce(sn):
    while True:
        if sn_try_explode(sn):
            continue
        if sn_try_split(sn):
            continue
        break

def sn_add(sn1, sn2):
    added = [sn1, sn2]
    sn_reduce(added)

print([[1, 2], [[3, 4], 5]])
print(sn_add([1,2], [[3,4],5]))
print("")

print(f"Expected: {[[[[0,9],2],3],4]} True")
sn = [[[[[9,8],1],2],3],4]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
print("")

print(f"Expected: {[7,[6,[5,[7,0]]]]} True")
sn = [7,[6,[5,[4,[3,2]]]]]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
print("")

print(f"Expected: {[[6,[5,[7,0]]],3]} True")
sn = [[6,[5,[4,[3,2]]]],1]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
print("")

print(f"Expected: {[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]} True")
sn = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
print("")

print(f"Expected: {[[3,[2,[8,0]]],[9,[5,[7,0]]]]} True")
sn = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
print("")

exit()

print([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
print(sn_add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]))
print("")

def sn_sum(sns):
    sum = sns[0]
    for i in range(1, len(sns)):
        sum = sn_add(sum, sns[i])
    return sum

print([[[[1,1],[2,2]],[3,3]],[4,4]])
print(sn_sum([
[1,1],
[2,2],
[3,3],
[4,4],
]))
print("")
print([[[[3,0],[5,3]],[4,4]],[5,5]])
print(sn_sum([
[1,1],
[2,2],
[3,3],
[4,4],
[5,5],
]))
print("")
print([[[[5,0],[7,4]],[5,5]],[6,6]])
print(sn_sum([
[1,1],
[2,2],
[3,3],
[5,5],
[6,6],
]))
print("")
