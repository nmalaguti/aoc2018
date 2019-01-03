data_input = 360781
# data_input = 92510

state = [3, 7]

elf1 = 0
elf2 = 1

NUM_AFTER = 10

digits = list(map(int, str(data_input)))

while True:
    elf1_value, elf2_value = state[elf1], state[elf2]
    new_value = elf1_value + elf2_value
    if new_value >= 10:
        state.append(1)
        if state[-len(digits):] == digits:
            break
    state.append(new_value % 10)
    if state[-len(digits):] == digits:
            break

    if len(state) % 100000 == 0:
        print(len(state))

    elf1 = (elf1 + elf1_value + 1) % len(state)
    elf2 = (elf2 + elf2_value + 1) % len(state)


print(''.join(str(i) for i in state[data_input:data_input+NUM_AFTER]))
print(len(state) - len(digits))