import re


with open('day_21/input.txt', 'r') as input_file:
    data_input = input_file.readlines()


mapping = {
    'addr': 'r[{2}] = r[{0}] + r[{1}]',
    'addi': 'r[{2}] = r[{0}] + {1}',
    'mulr': 'r[{2}] = r[{0}] * r[{1}]',
    'muli': 'r[{2}] = r[{0}] * {1}',
    'banr': 'r[{2}] = r[{0}] & r[{1}]',
    'bani': 'r[{2}] = r[{0}] & {1}',
    'borr': 'r[{2}] = r[{0}] | r[{1}]',
    'bori': 'r[{2}] = r[{0}] | {1}',
    'setr': 'r[{2}] = r[{0}]',
    'seti': 'r[{2}] = {0}',
    'gtir': 'r[{2}] = int({0} > r[{1}])',
    'gtri': 'r[{2}] = int(r[{0}] > {1})',
    'gtrr': 'r[{2}] = int(r[{0}] > r[{1}])',
    'eqir': 'r[{2}] = int({0} == r[{1}])',
    'eqri': 'r[{2}] = int(r[{0}] == {1})',
    'eqrr': 'r[{2}] = int(r[{0}] == r[{1}])',
}

data = []
ipr = 0

output = """
r = [0] * 6
numbers = set()
last = -1

while True:
""".splitlines()

for line in data_input:
    if line.startswith('#'):
        ipr = int(re.findall(r'\d', line)[0])
    else:
        op_code, *rest = line.rstrip().split()
        data.append((op_code,) + tuple(map(int, rest)))

for i, line in enumerate(data):
    if_statement = 'if' if i == 0 else 'elif'
    op_code, a, b, c = line
    extra = ''

    if i == 18:  # optimize division
        extra = f"""
        r[3] = r[2] = r[3] // 256
        r[{ipr}] = 8
        continue
        """
    elif i == 28:  # handle exit case
        extra = """
        if last == -1:
            print(r[4])
        if r[4] in numbers:
            print(last)
            exit()
        last = r[4]
        numbers.add(last)
        """

    block = f"""
    {if_statement} r[{ipr}] == {i}:
        {extra}
        {mapping[op_code].format(a, b, c)}
        r[{ipr}] += 1
    """
    output.extend(block.splitlines())


block = f"""
    else:
        exit()
"""

output.extend(block.splitlines())


with open('day_21/output.py', 'w') as output_file:
    output_file.write('\n'.join(output))
