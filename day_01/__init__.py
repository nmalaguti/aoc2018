
with open('day_01/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

total = 0
totals = set()
repeat = False

while not repeat:
    for line in data_input:
        [sign, *num] = line
        value = int(''.join(num))
        if sign == '+':
            total += value
        else:
            total -= value
        
        if total in totals:
            print('seen:', total)
            repeat = True
            break

        totals.add(total)

print(total)