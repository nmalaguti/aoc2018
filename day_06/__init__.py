from collections import deque, Counter

with open('day_06/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

# data_input = [
#     "1, 1",
#     "1, 6",
#     "8, 3",
#     "3, 4",
#     "5, 5",
#     "8, 9",
# ]

data = [tuple([int(x) for x in line.strip().split(', ')]) for line in data_input]

x_max = max(x for x, y in data) + 2
y_max = max(y for x, y in data) + 2

grid = []
queue = deque()

for i in range(y_max):
    grid.append([(-1, 0)] * x_max)

for i, (x, y) in enumerate(data):
    grid[y][x] = (i, 0)
    queue.append((x, y, i, 0))

def adjacent_points(x, y):
    if x > 0:
        yield x - 1, y
    if x + 1 < x_max:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y + 1 < y_max:
        yield x, y + 1

def to_chr(v, t):
    if v == -2:
        return '.'
    if v == -1:
        return '?'
    if t == 0:
        return chr(97 + v).upper()
    else:
        return chr(97 + v)

def display_grid():
    for row in grid:
        print(''.join(to_chr(v, t) for v, t in row))

tc = 0

while queue:
    x, y, value, turn = queue.popleft()

    # if tc != turn:
    #     display_grid()
    #     print('')
    #     tc = turn

    if grid[y][x][0] == -2:
        continue

    for next_x, next_y in adjacent_points(x, y):
        if grid[next_y][next_x][0] == -1:
            grid[next_y][next_x] = (value, turn + 1)
            queue.append((next_x, next_y, value, turn + 1))
        elif grid[next_y][next_x][0] != value and grid[next_y][next_x][1] == turn + 1:
            grid[next_y][next_x] = (-2, turn)
            queue.append((next_x, next_y, value, turn + 1))

counter = Counter()

for row in grid:
    counter.update(v for v, t in row)

del counter[-1]
del counter[-2]

for v, t in grid[0]:
    del counter[v]

for v, t in grid[-1]:
    del counter[v]

for row in grid:
    del counter[row[0][0]]
    del counter[row[-1][0]]

print(counter.most_common(1)[0][1])

grid = []

for i in range(y_max):
    grid.append([0] * x_max)

for g_y in range(y_max):
    for g_x in range(x_max):
        for p_x, p_y in data:
            grid[g_y][g_x] += abs(g_y - p_y) + abs(g_x - p_x)

def to_chr2(x, y, v):
    if (x, y) in data:
        i = data.index((x, y))
        return chr(97 + i).upper()
    if v >= 32:
        return '.'
    return '#'

def display_grid2():
    for y, row in enumerate(grid):
        print(''.join(to_chr2(x, y, v) for x, v in enumerate(row)))

size = 0

for row in grid:
    for item in row:
        if item < 10_000:
            size += 1

print(size)