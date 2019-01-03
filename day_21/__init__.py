# import re
#
# with open('day_21/input.txt', 'r') as input_file:
#     data_input = input_file.readlines()
#
#
# class Instructions:
#     @staticmethod
#     def addr(r, a, b, c): r[c] = r[a] + r[b]
#
#     @staticmethod
#     def addi(r, a, b, c): r[c] = r[a] + b
#
#     @staticmethod
#     def mulr(r, a, b, c): r[c] = r[a] * r[b]
#
#     @staticmethod
#     def muli(r, a, b, c): r[c] = r[a] * b
#
#     @staticmethod
#     def banr(r, a, b, c): r[c] = r[a] & r[b]
#
#     @staticmethod
#     def bani(r, a, b, c): r[c] = r[a] & b
#
#     @staticmethod
#     def borr(r, a, b, c): r[c] = r[a] | r[b]
#
#     @staticmethod
#     def bori(r, a, b, c): r[c] = r[a] | b
#
#     @staticmethod
#     def setr(r, a, b, c): r[c] = r[a]
#
#     @staticmethod
#     def seti(r, a, b, c): r[c] = a
#
#     @staticmethod
#     def gtir(r, a, b, c): r[c] = int(a > r[b])
#
#     @staticmethod
#     def gtri(r, a, b, c): r[c] = int(r[a] > b)
#
#     @staticmethod
#     def gtrr(r, a, b, c): r[c] = int(r[a] > r[b])
#
#     @staticmethod
#     def eqir(r, a, b, c): r[c] = int(a == r[b])
#
#     @staticmethod
#     def eqri(r, a, b, c): r[c] = int(r[a] == b)
#
#     @staticmethod
#     def eqrr(r, a, b, c): r[c] = int(r[a] == r[b])
#
#
# def execute(ip, ipr, state, instruction, debug=False):
#     state[ipr] = ip
#     op_code, a, b, c = instruction
#     if debug: print('ip={}'.format(ip), state, op_code, a, b, c, '', end='')
#     getattr(Instructions, op_code)(state, a, b, c)
#     if debug: print(state)
#     do_print = state[ipr] >= 25
#     ip = state[ipr]
#     ip += 1
#
#     # if do_print:
#     #     print(ip, state)
#
#     return ip, state
#
#
# def run(state, ipr, program):
#     ip = 0
#     counter = 0
#
#     while 0 <= ip <= len(program):
#         ip, state = execute(ip, ipr, state, program[ip], debug=True)
#         if ip < 0 or ip >= len(program):
#             break
#         # if ip == 28:
#         #     print(counter, state)
#         counter += 1
#         if counter > 1900:
#             break
#     return counter
#
# # 0 16337778
# # 1 15727270
# # 2 15624546
# # 3 7433718
# # 4 13429714
# # 5 6578886
# # 6 1969858
# # 7 6352150
# # 8 8793650
#
# data = []
# ipr = 0
#
# for line in data_input:
#     if line.startswith('#'):
#         ipr = int(re.findall(r'\d', line)[0])
#     else:
#         op_code, *rest = line.rstrip().split()
#         data.append((op_code,) + tuple(map(int, rest)))
#
# steps = run([0] + [0] * 5, ipr, data)
#
# print(steps)


# Manually Transpiled

while 123 & 456 != 72:
    pass

r0, r1, r2, r3, r4, r5 = [0] * 6
# r0 = 15690445

numbers = set()
last = -1

while True:  # 6
    r3 = r4 | 65536  # 6
    r4 = 12670166  # 7

    while True:  # 8
        r2 = r3 & 255 # 8
        r4 = r4 + r2  # 9
        r4 = r4 & 16777215  # 10
        r4 = r4 * 65899  # 11
        r4 = r4 & 16777215  # 12

        if 256 > r3:  # 14
            r2 = 1  # 13
            if r4 == r0:  # 29
                r2 = 1  # 28
                exit()
            else:
                r2 = 0  # 28
                if last == -1:
                    print(r4)
                if r4 in numbers:
                    print(last)
                    print(len(numbers))
                    exit()
                last = r4
                numbers.add(last)
                break  # 30 goto 6
        else:  # 15
            # r2 = 0  # 13
            r3 = r2 = r3 // 256  # rewrite loop below as division
            # while True:  # 18
            #     r5 = r2 + 1  # 18
            #     r5 = r5 * 256  # 19
            #     if r5 > r3:
            #         r5 = 1  # 20
            #         r3 = r2  # 26
            #         break  # 27 goto 8
            #     else:
            #         r5 = 0  # 20
            #         r2 = r2 + 1  # 24
            #         # 25 goto 18


