from operator import mul, add, gt, and_, or_, eq
from functools import partial
from more_itertools import chunked
from collections import defaultdict

with open('day_16/input.txt', 'r') as input_file:
    data_input = iter(input_file.readlines())


data = []
program = []

for before, instruction, after, _ in chunked((line.rstrip() for line in data_input), 4):
    if not before:
        program.extend([after, _])
        break

    data.append(
        (
            eval(before.split(': ')[1]),
            tuple(map(int, instruction.split(' '))),
            eval(after.split(': ')[1])
        )
    )

program.extend(line.rstrip() for line in data_input)
program = [tuple(map(int, instruction.split(' '))) for instruction in program]


def addr(r, a, b, c): r[c] = r[a] + r[b]
def addi(r, a, b, c): r[c] = r[a] + b
def mulr(r, a, b, c): r[c] = r[a] * r[b]
def muli(r, a, b, c): r[c] = r[a] * b
def banr(r, a, b, c): r[c] = r[a] & r[b]
def bani(r, a, b, c): r[c] = r[a] & b
def borr(r, a, b, c): r[c] = r[a] | r[b]
def bori(r, a, b, c): r[c] = r[a] | b
def setr(r, a, b, c): r[c] = r[a]
def seti(r, a, b, c): r[c] = a
def gtir(r, a, b, c): r[c] = int(a > r[b])
def gtri(r, a, b, c): r[c] = int(r[a] > b)
def gtrr(r, a, b, c): r[c] = int(r[a] > r[b])
def eqir(r, a, b, c): r[c] = int(a == r[b])
def eqri(r, a, b, c): r[c] = int(r[a] == b)
def eqrr(r, a, b, c): r[c] = int(r[a] == r[b])


op_codes = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr,
]


def execute(state, instruction):
    state = state.copy()
    op_code, a, b, c = instruction
    op_codes[op_code](state, a, b, c)

    return state


def find_valid_op_codes(before, instruction, after):
    for i, op_code in enumerate(op_codes):
        if execute(before, (i,) + instruction[1:]) == after:
            yield i


# before = [3, 2, 1, 1]
# instruction = (9, 2, 1, 2)
# after = [3, 2, 2, 1]
# execute(before, instruction)

count = 0

results = []
possible_mappings = defaultdict(set)

for before, instruction, after in data:
    valid_op_codes = set(find_valid_op_codes(before, instruction, after))
    possible_mappings[instruction[0]] |= valid_op_codes
    if len(valid_op_codes) >= 3:
        count += 1

print(count)


op_code_mapping = [None] * len(op_codes)


while possible_mappings:
    op_code, [lookup, *rest] = min(possible_mappings.items(), key=lambda x: len(x[1]))
    assert not rest
    del possible_mappings[op_code]
    op_code_mapping[op_code] = op_codes[lookup]
    for k, v in possible_mappings.items():
        try:
            v.remove(lookup)
        except KeyError:
            pass

op_codes = op_code_mapping

state = [0] * 4
for instruction in program:
    state = execute(state, instruction)

print(state[0])
