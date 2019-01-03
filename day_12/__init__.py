from collections import defaultdict
from more_itertools import windowed
from itertools import count

with open('day_12/input.txt', 'r') as input_file:
    data_input = iter(input_file.readlines())

initial_state = next(data_input).strip().split(': ')[1]
next(data_input)

patterns = defaultdict(lambda: '.')
for line in data_input:
    pattern, result = line.strip().split(' => ')
    patterns[pattern] = result

def generation(first, state):
    first_plant = state.index('#')
    if first_plant < 5:
        state = ('.' * (5 - first_plant)) + state
        first -= (5 - first_plant)
    if first_plant > 5:
        state = state[first_plant - 5:]
        first += first_plant - 5

    last_plant = state.rindex('#')
    if len(state) - last_plant < 5:
        state += ('.' * (5 - (len(state) - last_plant)))
    if len(state) - last_plant > 5:
        state = state[:last_plant + 6]

    return (first + 2, ''.join(patterns[''.join(window)] for window in windowed(state, 5)))

def state_value(first, state):
    for i, c in zip(count(first), state):
        if c == '#':
            yield i

state = initial_state
first = 0
# print(0, first, sum(state_value(first, state)), state)
for i in count(1):
    prev_state, prev_first = state, first
    first, state = generation(first, state)
    if i == 20:
        print(sum(state_value(first, state)))
    if state == prev_state:
        break
    # print(i + 1, first, sum(state_value(first, state)), state)

first = first - i + (50_000_000_000 * (first - prev_first))
print(sum(state_value(first, state)))



# print(list()