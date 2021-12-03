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