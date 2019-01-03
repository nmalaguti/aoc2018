from collections import defaultdict, Counter

with open('day_18/input.txt', 'r') as input_file:
    data_input = input_file.readlines()


OPEN = '.'
TREES = '|'
LUMBERYARD = '#'

DIMS = len(data_input)

def create_grid():
    return defaultdict(lambda: None)

grid = create_grid()

for y, line in enumerate(data_input):
    for x, c in enumerate(line.rstrip()):
        grid[(x, y)] = c


def adjacent(x, y, grid):
    for vy in range(-1, 2):
        for vx in range(-1, 2):
            if y + vy >= DIMS or x + vx >= DIMS or y + vy < 0 or x + vx < 0:
                continue
            if vy == 0 and vx == 0:
                continue
            value = grid[(x + vx, y + vy)]
            if value is not None:
                yield value


def tick(grid):
    new_grid = create_grid()
    for y in range(DIMS):
        for x in range(DIMS):
            v = grid[(x, y)]
            if v is None:
                continue

            c = Counter(adjacent(x, y, grid))

            if v == OPEN and c[TREES] >= 3:
                new_grid[(x, y)] = TREES
            elif v == TREES and c[LUMBERYARD] >= 3:
                new_grid[(x, y)] = LUMBERYARD
            elif v == LUMBERYARD and (c[LUMBERYARD] < 1 or c[TREES] < 1):
                new_grid[(x, y)] = OPEN
            else:
                new_grid[(x, y)] = v

    return new_grid


def pretty_print(grid):
    for y in range(DIMS):
        row = []
        for x in range(DIMS):
            row.append(grid[(x, y)])
        print(' ' + ''.join(row))
    print('')


def calc_value(grid):
    c = Counter(grid.values())
    return c[TREES] * c[LUMBERYARD]


def find_cycle(grid):
    tortoise = tick(grid)
    hare = tick(tortoise)

    while tortoise.items() != hare.items():
        tortoise = tick(tortoise)
        hare = tick(tick(hare))

    mu = 0
    tortoise = grid
    while tortoise.items() != hare.items():
        tortoise = tick(tortoise)
        hare = tick(hare)
        mu += 1

    lam = 1
    hare = tick(tortoise)
    while tortoise.items() != hare.items():
        hare = tick(hare)
        lam += 1

    return mu, lam, tortoise


sim = grid
for i in range(10):
    sim = tick(sim)

print(calc_value(sim))

cycle_start, cycle_length, sim = find_cycle(grid)

iterations, remainder = divmod(1000000000 - cycle_start, cycle_length)

for i in range(remainder):
    sim = tick(sim)

print(calc_value(sim))
