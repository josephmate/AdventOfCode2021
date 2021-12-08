import sys
import re

pattern = r'(\d+),(\d+)\s->\s(\d+),(\d+)'

input = list(
    map(lambda columns : [columns[0].split(" "), columns[1].split(" ")],
    map(lambda line : line.split(" | "),
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))))

print(input)

seven_segment_display = [
    set(['a', 'b', 'c', 'e', 'f', 'g']),      # 0
    set(['c', 'f']),                          # 1
    set(['a', 'c', 'd', 'e', 'g']),           # 2
    set(['a', 'c', 'd', 'f', 'g']),           # 3
    set(['b', 'c', 'd', 'f']),                # 4
    set(['a', 'b', 'd', 'f', 'g']),           # 5
    set(['a', 'b', 'd', 'e', 'f', 'g']),      # 6
    set(['a', 'c', 'f']),                     # 7
    set(['a', 'b', 'c', 'd', 'e', 'f', 'g']), # 8
    set(['a', 'b', 'c', 'd', 'f', 'g']),      # 9
]

group_by_num_of_segments = {}
for i in range(0, len(seven_segment_display)):
    num_segments = len(seven_segment_display[i])
    if num_segments in group_by_num_of_segments:
        group_by_num_of_segments[num_segments].append(i)
    else:
        group_by_num_of_segments[num_segments] = [i]

print(group_by_num_of_segments)

num_of_uniq = 0
for (_, displays) in input:
    for display in displays:
        if len(group_by_num_of_segments[len(display)]) == 1:
            num_of_uniq += 1
print(num_of_uniq)

def set_to_str(s):
    s_list = list(s)
    s_list.sort()
    return f"{''.join(map(lambda i: str(i), s_list))}"

def print_num_to_signals(num_to_signals):
    for (num, signals) in num_to_signals.items():
        print(num, end="")
        for signal in signals:
            print(f" {set_to_str(signal)}", end="")
        print("")

def print_signals_to_num(signals_to_num):
    for (signal, options) in signals_to_num.items():
        print(f"{set_to_str(signal)} {set_to_str(options)}")

def not_done(num_to_signals) :
    for (num, signals) in num_to_signals.items():
        if len(signals) > 1:
            return False
    return True

def solve_display(signals, displays):
    signals_to_num = {}
    for signal in signals:
        signal_set = set()
        for c in signal:
            signal_set.add(c)
        options = set()
        for i in range(0, 10):
            options.add(i)
        signals_to_num[frozenset(signal_set)] = options
    num_to_signals = {}
    for i in range(0, 10):
        set_of_signals = set()
        for signal in signals:
            signal_set = set()
            for c in signal:
                signal_set.add(c)
            set_of_signals.add(frozenset(signal_set))
        num_to_signals[i] = set_of_signals
    group_by_num_of_segments_set = {}
    for (count, options) in group_by_num_of_segments.items():
        group_by_num_of_segments_set[count] = set(options)

    # solve the easy cases
    for signal in signals:
        if len(group_by_num_of_segments[len(signal)]) == 1:
            matched_val = group_by_num_of_segments[len(signal)][0]
            set_to_clear = signals_to_num[frozenset(signal)]
            # update signals_to_num
            for i in range(0, 10):
                if i != matched_val:
                    if i in set_to_clear:
                        set_to_clear.remove(i)
            for signal_to_update in signals:
                if frozenset(signal_to_update) != (signal):
                    set_to_update = signals_to_num[frozenset(signal_to_update)]
                    if matched_val in set_to_update:
                        set_to_update.remove(matched_val)

            # update num_to_signals
            for i in range(0, 10):
                if frozenset(signal) in num_to_signals[i]:
                    num_to_signals[i].remove(frozenset(signal))
            num_to_signals[matched_val] = frozenset(signal)

            # update group_by_num_of_segments_set
            for (signal_len, options) in group_by_num_of_segments_set.items():
                if matched_val in options:
                    options.remove(matched_val)
            
    
    print_signals_to_num(signals_to_num)
    print_num_to_signals(num_to_signals)
    print("\n".join(map(lambda pair: str(pair), group_by_num_of_segments_set.items())))
        

    return 0

sum = 0
for (signals, displays) in input:
    sum += solve_display(signals, displays)
print(sum)