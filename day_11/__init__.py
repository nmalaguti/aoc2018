data_input = 3463

def power_level(grid_serial, x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += grid_serial
    power_level *= rack_id
    hunds_digit = power_level // 100 % 10
    return hunds_digit - 5

grid = []
for y in range(1, 301):
    row = []
    grid.append(row)
    for x in range(1, 301):
        row.append(power_level(data_input, x, y))

summed_area_table = []
for y in range(0, 300):
    row = []
    summed_area_table.append(row)
    for x in range(0, 300):
        row.append(
            grid[y][x] +
            (0 if y == 0 else summed_area_table[y - 1][x]) +
            (0 if x == 0 else summed_area_table[y][x - 1]) -
            (0 if (x == 0 or y == 0) else summed_area_table[y - 1][x - 1])
        )

def square_power(summed_area_table, x, y, size):
    return (
        (0 if x == 0 or y == 0 else summed_area_table[y - 1][x - 1]) +
        summed_area_table[y + size - 1][x + size - 1] - 
        (0 if y == 0 else summed_area_table[y - 1][x + size - 1]) - 
        (0 if x == 0 else summed_area_table[y + size - 1][x - 1])
    )

def square_power_grid(grid, x, y, size):
    return sum(grid[y + i][x + j] for i in range(size) for j in range(size))

def find_max_square_power(grid, size):
    max_square_power = (None, None, size, 300 * 300 * -5)
    for y in range(len(grid) - size):
        for x in range(len(grid[y]) - size):
            sp = square_power(summed_area_table, x, y, size)
            if sp > max_square_power[3]:
                max_square_power = (x + 1, y + 1, size, sp)

    return max_square_power

def find_size_max_square_power(grid):
    max_square_power = (None, None, -1, 300 * 300 * -5)
    for size in range(1, len(grid) - 1):
        sp = find_max_square_power(grid, size)
        if sp[3] > max_square_power[3]:
            max_square_power = sp

    return max_square_power

msp3 = find_max_square_power(grid, 3)

print("{},{}".format(msp3[0], msp3[1]))

msp = find_size_max_square_power(grid)

print("{},{},{}".format(msp[0], msp[1], msp[2]))
