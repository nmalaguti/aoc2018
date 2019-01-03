import re

with open('day_10/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

data = [tuple(map(int, re.findall('[-0-9]+', line))) for line in data_input]

def after_time(seconds):
    new_data = []
    for x, y, vx, vy in data:
        new_data.append((x + vx * seconds, y + vy * seconds, vx, vy))

    return new_data

def get_dims(new_data):
    x_min = min(x for x, y, vx, vy in new_data)
    x_max = max(x for x, y, vx, vy in new_data)
    y_min = min(y for x, y, vx, vy in new_data)
    y_max = max(y for x, y, vx, vy in new_data)

    return x_max - x_min + y_max - y_min

def find_smallest_dims(start=0, inital_step=1000):
    step = inital_step
    curr = start
    smallest = get_dims(after_time(curr))
    while step != 0:
        new_dims = get_dims(after_time(curr + step))
        if new_dims < smallest:
            curr += step
            smallest = new_dims
        else:
            step = step // -2

    return curr

def pretty_print(new_data):
    x_min = min(x for x, y, vx, vy in new_data)
    x_max = max(x for x, y, vx, vy in new_data)
    y_min = min(y for x, y, vx, vy in new_data)
    y_max = max(y for x, y, vx, vy in new_data)

    grid = []
    for i in range(y_max - y_min + 1):
        grid.append(['.'] * (x_max - x_min + 1))
    
    for x, y, vx, vy, in new_data:
        grid[y - y_min][x - x_min] = '#'

    for row in grid:
        print(''.join(row))

wait_time = find_smallest_dims()
pretty_print(after_time(wait_time))
print(wait_time)