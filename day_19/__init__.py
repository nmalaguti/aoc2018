import re

with open('day_19/input.txt', 'r') as input_file:
    data_input = input_file.readlines()


class Instructions:
    @staticmethod
    def addr(r, a, b, c): r[c] = r[a] + r[b]

    @staticmethod
    def addi(r, a, b, c): r[c] = r[a] + b

    @staticmethod
    def mulr(r, a, b, c): r[c] = r[a] * r[b]

    @staticmethod
    def muli(r, a, b, c): r[c] = r[a] * b

    @staticmethod
    def banr(r, a, b, c): r[c] = r[a] & r[b]

    @staticmethod
    def bani(r, a, b, c): r[c] = r[a] & b

    @staticmethod
    def borr(r, a, b, c): r[c] = r[a] | r[b]

    @staticmethod
    def bori(r, a, b, c): r[c] = r[a] | b

    @staticmethod
    def setr(r, a, b, c): r[c] = r[a]

    @staticmethod
    def seti(r, a, b, c): r[c] = a

    @staticmethod
    def gtir(r, a, b, c): r[c] = int(a > r[b])

    @staticmethod
    def gtri(r, a, b, c): r[c] = int(r[a] > b)

    @staticmethod
    def gtrr(r, a, b, c): r[c] = int(r[a] > r[b])

    @staticmethod
    def eqir(r, a, b, c): r[c] = int(a == r[b])

    @staticmethod
    def eqri(r, a, b, c): r[c] = int(r[a] == b)

    @staticmethod
    def eqrr(r, a, b, c): r[c] = int(r[a] == r[b])


def execute(ip, ipr, state, instruction, debug=False):
    state[ipr] = ip
    op_code, a, b, c = instruction
    if debug: print('ip={}'.format(ip), state, op_code, a, b, c, '', end='')
    getattr(Instructions, op_code)(state, a, b, c)
    if debug: print(state)
    ip = state[ipr]
    ip += 1

    return ip, state


def run(state, ipr, program, steps=None):
    ip = 0
    counter = 0

    while 0 <= ip <= len(program):
        ip, state = execute(ip, ipr, state, program[ip])
        counter += 1
        yield state
        if steps is not None and counter >= steps:
            break


data = []
ipr = 0

for line in data_input:
    if line.startswith('#'):
        ipr = int(re.findall(r'\d', line)[0])
    else:
        op_code, *rest = line.rstrip().split()
        data.append((op_code,) + tuple(map(int, rest)))

for state in run([0] * 6, ipr, data):
    pass

print(state[0])

n = 0
for state in run([1] + [0] * 5, ipr, data, steps=1000):
    n = max(n, state[2])

total = 0
for i in range(1, n + 1):
    if n % i == 0:
        total += i
print(total)
