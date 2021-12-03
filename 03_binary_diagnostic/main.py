import sys

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

# all bianry numbers are the same length
binary_length = len(input[0])
counts = []
for i in range(0, binary_length):
    counts.append([0, 0])
for binary in input:
    for i in range(0, binary_length):
        # '0' -> 0
        # '1' -> 1
        # which lets us index into the array of counts
        counts[i][int(binary[i])] += 1

def binary_array_to_int(binary_array):
    # binary number is most significant to least significant N-i the power
    result = 0
    for i in range(0, len(binary_array)):
        result += binary_array[i]*2**(len(binary_array)-i-1)
    return result

gamma_binary = []
epsilon_binary = []
for i in range(0, binary_length):
    if counts[i][0] > counts[i][1]:
        gamma_binary.append(0)
        epsilon_binary.append(1)
    else:
        gamma_binary.append(1)
        epsilon_binary.append(0)

print(gamma_binary)
print(epsilon_binary)

gamma = binary_array_to_int(gamma_binary)
epsilon = binary_array_to_int(epsilon_binary)
power = gamma*epsilon
print(f"gamma={gamma} epsilon={epsilon} power={power}")


potential_generator_rating = input.copy()
current_posn = 0
while len(potential_generator_rating) > 1:
    counts = [0, 0]
    for binary_number in potential_generator_rating:
        counts[int(binary_number[current_posn])] += 1
    
    criteria = '0'
    if counts[1] >= counts[0]:
        criteria = '1'
    
    potential_generator_rating = list(
        filter(
            lambda binary_number: binary_number[current_posn] == criteria,
            potential_generator_rating
        )
    )
    current_posn += 1
potential_scrubber_rating = input.copy()
current_posn = 0
while len(potential_scrubber_rating) > 1:
    counts = [0, 0]
    for binary_number in potential_scrubber_rating:
        counts[int(binary_number[current_posn])] += 1
    
    criteria = '1'
    if counts[0] <= counts[1]:
        criteria = '0'
    
    potential_scrubber_rating = list(
        filter(
            lambda binary_number: binary_number[current_posn] == criteria,
            potential_scrubber_rating
        )
    )
    current_posn += 1

def binary_str_to_int(binary_str):
    binary_array = []
    for binary_digit_str in binary_str:
        binary_array.append(int(binary_digit_str))
    return binary_array_to_int(binary_array)

print(potential_generator_rating)
print(binary_str_to_int(potential_generator_rating[0]))
generator_rating = binary_str_to_int(potential_generator_rating[0])
print(potential_scrubber_rating)
print(binary_str_to_int(potential_scrubber_rating[0]))
scrubber_rating = binary_str_to_int(potential_scrubber_rating[0])

life_support_rating = generator_rating * scrubber_rating
print(f"generator_rating={generator_rating} scrubber_rating={scrubber_rating} life_support_rating={life_support_rating}")
