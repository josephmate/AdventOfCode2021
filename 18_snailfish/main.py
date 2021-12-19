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

# [[[[[9,8],1],2],3],4]
#        / \
#       / \ 4
#      / \ 3
#    / \  2
#  / \  1
#  9 8
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

def copy_stack(stack):
    vals = []
    while not stack.empty():
        vals.append(stack.get())
    vals.reverse()
    result = Stack()
    for val in vals:
        stack.put(val)
        result.put(val)
    return result

def sn_explode(sn, parent_stack):
    (parent, direction) = parent_stack.get()
    if direction == 'left':
        parent[0] = 0
    else:
        parent[1] = 0
    parent_stack.put((parent, direction))
    parent_stack_for_right = copy_stack(parent_stack)
    explode_to_left(sn[0], parent_stack)
    explode_to_right(sn[1], parent_stack_for_right)

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
            parent_stack.get()
        if isinstance(sn[1], list):
            parent_stack.put((sn, 'right'))
            if sn_try_explode_impl(sn[1], count, parent_stack):
                return True
            parent_stack.get()
        return False
    

def sn_try_explode(sn):
    return sn_try_explode_impl(sn, 0, Stack())

def sn_try_split_impl(sn, parent, direction):
    if isinstance(sn, int):
        # If any regular number is 10 or greater, the leftmost such regular number splits.
        if sn > 9:
            # the left element of the pair should be the regular number divided by two and rounded down
            left = sn // 2
            # the right element of the pair should be the regular number divided by two and rounded up
            right = (sn // 2) + (sn % 2)
            pair = [left, right]
            if direction == "right":
                parent[1] = pair
            else:
                parent[0] = pair
            return True
        else:
            return False
    else:
        if sn_try_split_impl(sn[0], sn, "left"):
            return True
        if sn_try_split_impl(sn[1], sn, "right"):
            return True
        return False

def sn_try_split(sn):
    return sn_try_split_impl(sn, None, None)

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
    return added

print([[1, 2], [[3, 4], 5]])
print(sn_add([1,2], [[3,4],5]))
print("")

print(f"Expected: {[[[[0,9],2],3],4]} True")
sn = [[[[[9,8],1],2],3],4]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
assert(reduced == True)
assert(f"{[[[[0,9],2],3],4]}" == f"{sn}")
print("")

print(f"Expected: {[7,[6,[5,[7,0]]]]} True")
sn = [7,[6,[5,[4,[3,2]]]]]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
assert(reduced == True)
assert(f"{[7,[6,[5,[7,0]]]]}" == f"{sn}")
print("")

print(f"Expected: {[[6,[5,[7,0]]],3]} True")
sn = [[6,[5,[4,[3,2]]]],1]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
assert(reduced == True)
assert(f"{[[6,[5,[7,0]]],3]}" == f"{sn}")
print("")

print(f"Expected: {[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]} True")
sn = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
assert(reduced == True)
assert(f"{[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]}" == f"{sn}")
print("")

print(f"Expected: {[[3,[2,[8,0]]],[9,[5,[7,0]]]]} True")
sn = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
reduced = sn_try_explode(sn)
print(f"Actual:   {sn} {reduced}")
assert(reduced == True)
assert(f"{[[3,[2,[8,0]]],[9,[5,[7,0]]]]}" == f"{sn}")
print("")

expected = [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
actual = sn_add( [[[[4,3],4],4],[7,[[8,4],9]]] , [1,1] )
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

def sn_sum(sns):
    sum = sns[0]
    for i in range(1, len(sns)):
        sum = sn_add(sum, sns[i])
    return sum


expected = [[[[1,1],[2,2]],[3,3]],[4,4]]
actual = sn_sum([
    [1,1],
    [2,2],
    [3,3],
    [4,4],
])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = [[[[3,0],[5,3]],[4,4]],[5,5]]
actual = sn_sum([
    [1,1],
    [2,2],
    [3,3],
    [4,4],
    [5,5],
])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")


expected = [[[[5,0],[7,4]],[5,5]],[6,6]]
actual = sn_sum([
    [1,1],
    [2,2],
    [3,3],
    [4,4],
    [5,5],
    [6,6],
])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
actual = sn_sum([
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
    [7,[5,[[3,8],[1,4]]]],
    [[2,[2,2]],[8,[8,1]]],
    [2,9],
    [1,[[[9,3],9],[[9,0],[0,7]]]],
    [[[5,[7,4]],7],1],
    [[[[4,2],2],6],[8,7]],
])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

def sn_magnitude(sn):
    if isinstance(sn, int):
        return sn
    else:
        # The magnitude of a pair is 
        # 3 times the magnitude of its left element
        # plus 2 times the magnitude of its right element.
        return (3 * sn_magnitude(sn[0])) + (2 * sn_magnitude(sn[1]))

expected = 143
actual = sn_magnitude([[1,2],[[3,4],5]])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = 1384
actual = sn_magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = 445
actual = sn_magnitude([[[[1,1],[2,2]],[3,3]],[4,4]])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = 791
actual = sn_magnitude([[[[3,0],[5,3]],[4,4]],[5,5]])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = 1137
actual = sn_magnitude([[[[5,0],[7,4]],[5,5]],[6,6]])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = 3488
actual = sn_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

expected = 4140
actual = sn_magnitude(sn_sum([
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
    [[[5,[2,8]],4],[5,[[9,9],0]]],
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
    [[[[5,4],[7,7]],8],[[8,3],8]],
    [[9,3],[[9,9],[6,[4,9]]]],
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]],
]))
print(f"Expected: {expected}")
print(f"Actual:   {actual}")
assert(f"{expected}" == f"{actual}")
print("")

print(sn_magnitude(sn_sum(input)))