from collections import Counter
from operator import itemgetter

with open('day_02/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

# twos = 0
# threes = 0

# for line in data_input:
#     c = Counter(line.strip())
#     value_set = set(c.values())
#     if 2 in value_set:
#         twos += 1
#     if 3 in value_set:
#         threes += 1

# print(twos * threes)

def find_close(sorted_list):
    first = sorted_list.pop().strip()

    for item in sorted_list:
        second = item.strip()
        
        count_diff = 0
        for f, s in zip(first, second):
            if f != s:
                count_diff += 1

        if count_diff == 1:
            print(first, second)

        first = second

input_len = len(data_input[0].strip())
for i in range(input_len):
    find_close(sorted(data_input, key=itemgetter(i)))