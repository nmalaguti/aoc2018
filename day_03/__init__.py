with open('day_03/input.txt', 'r') as input_file:
    data_input = input_file.readlines()


bitmap = []
for i in range(1000):
    bitmap.append([0] * 1000)

# for row in bitmap:
#     print(''.join(row))

def fill(x, y, w, h):
    for i in range(h):
        for j in range(w):
            bitmap[y + i][x + j] += 1

def check(x, y, w, h):
    for i in range(h):
        for j in range(w):
            if bitmap[y + i][x + j] != 1:
                return False
    return True

for line in data_input:
    [claim_id, value] = line.strip().split(' @ ')
    [coords, size] = value.strip().split(': ')
    [x, y] = coords.strip().split(',')
    [w, h] = size.split('x')
    
    fill(int(x), int(y), int(w), int(h))

for line in data_input:
    [claim_id, value] = line.strip().split(' @ ')
    [coords, size] = value.strip().split(': ')
    [x, y] = coords.strip().split(',')
    [w, h] = size.split('x')
    
    if check(int(x), int(y), int(w), int(h)):
        print(claim_id)

# print(bitmap)

total = 0

for row in bitmap:
    for col in row:
        if col > 1:
            total += 1

print(total)