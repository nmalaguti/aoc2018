from functools import lru_cache
from collections import defaultdict
from heapq import heappush, heappop

with open('day_22/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

depth = int(data_input[0].split(': ')[1])
target = tuple(map(int, data_input[1].split(': ')[1].split(',')))


# depth = 510
# target = (10, 10)


@lru_cache(maxsize=None)
def erosion_level(x, y):
    return (geologic_index(x, y) + depth) % 20183


@lru_cache(maxsize=None)
def geologic_index(x, y):
    if (x, y) == (0, 0):
        return 0
    if target == (x, y):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    else:
        return erosion_level(x - 1, y) * erosion_level(x, y - 1)


# part 1
print(sum(erosion_level(x, y) % 3 for x in range(target[0] + 1) for y in range(target[1] + 1)))

# part 2

TORCH = 1
CLIMBING_GEAR = 2
NEITHER = 0

regions = {
    # rocky
    0: {TORCH, CLIMBING_GEAR},
    # wet
    1: {CLIMBING_GEAR, NEITHER},
    # narrow
    2: {TORCH, NEITHER},
}


def adjacent(x, y):
    if y > 0:
        yield x, y - 1
    if x > 0:
        yield x - 1, y
    yield x + 1, y
    yield x, y + 1


def dist(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


grid = defaultdict(lambda: float('inf'))

loc = (0, 0)
grid[(loc, TORCH)] = 0
queue = [(-1, 0, loc, TORCH)]
visited = set()


while queue:
    d, cost, (x, y), tool = heappop(queue)
    allowed_tools = regions[erosion_level(x, y) % 3]
    assert tool in allowed_tools

    # if we've already been here with this tool and it was cheaper
    if cost > grid[((x, y), tool)]:
        continue

    # it can't be cheaper if it is already more expensive than our target
    if cost + dist((x, y), target) > grid[(target, TORCH)]:
        continue

    grid[((x, y), tool)] = cost

    for other_tool in allowed_tools - {tool}:
        if ((x, y), other_tool, cost + 7) not in visited:
            visited.add(((x, y), other_tool, cost + 7))
            heappush(queue,
                     (
                         dist(target, (x, y)) + cost + 7,
                         cost + 7,
                         (x, y),
                         other_tool,
                     ))

    for next_x, next_y in adjacent(x, y):
        if tool in regions[erosion_level(next_x, next_y) % 3]:
            if ((next_x, next_y), tool, cost + 1) not in visited:
                visited.add(((next_x, next_y), tool, cost + 1))
                heappush(queue,
                         (
                             dist(target, (next_x, next_y)) + cost,
                             cost + 1,
                             (next_x, next_y),
                             tool,
                         ))

print(grid[(target, TORCH)])
