from collections import defaultdict, deque
from bisect import bisect_right, bisect_left

with open('day_17/input.txt', 'r') as input_file:
    data_input = input_file.readlines()


def parse(coord):
    var, val = coord.split('=')
    if '..' in val:
        low, high = map(int, val.split('..'))
        return range(low, high+1)
    else:
        val = int(val)
        return range(val, val + 1)


grid = defaultdict(lambda: '.')

x_min = y_min = 1_000_000
x_max = y_max = -1

y_list = []

for line in data_input:
    xs, ys = line.split(', ')
    if 'x' in ys:
        xs, ys = ys, xs
    for x in parse(xs):
        x_min = min(x, x_min)
        x_max = max(x, x_max)
        for y in parse(ys):
            y_min = min(y, y_min)
            y_max = max(y, y_max)
            y_list.append((y, x))
            grid[(x, y)] = '#'

x_range = range(x_min, x_max + 1)
y_range = range(y_min, y_max + 1)

y_list.sort()
x_list = sorted(grid.keys())


def pretty_print(start=None, end=None):
    y_num_width = len(str(max(y_range)))
    x_num_height = len(str(max(x_range)))

    if start is None:
        start = min(y_range)
    if end is None:
        end = max(y_range)

    # if start < min(y_range):
    #     start = min(y_range)
    # if end > max(y_range):
    #     end = max(y_range)

    row_format = '%' + str(y_num_width) + 'd '
    for i in range(x_num_height):
        row = [' ' * (y_num_width + 1)]
        for x in x_range:
            div = (10 ** (x_num_height - 1 - i))
            row.append(str(x // div % 10))
        print(''.join(row))

    for y in range(start, end + 1):
        row = [row_format % y]
        for x in x_range:
            row.append(grid[(x, y)])
        print(''.join(row))

    print('')


spring = 500


def find_gt(a, x):
    """Find leftmost value greater than x"""
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError


def find_lt(a, x):
    """Find rightmost value less than x"""
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError


def find_left_right(a, x):
    i = bisect_left(a, x)
    if i:
        return a[i-1], a[i]
    raise ValueError


falling_queue = deque([(500, y_min)])
seen = set()
counter = 0

while falling_queue:
    curr_x, curr_y = falling_queue.popleft()

    # if (curr_x, curr_y) in seen:
    #     continue

    seen.add((curr_x, curr_y))

    if grid[(curr_x, curr_y)] == '~':
        continue

    if grid[(curr_x, curr_y + 1)] not in ('#', '~'):
        next_x, next_y = find_gt(x_list, (curr_x, curr_y))
        if next_x != curr_x:
            # fell off the bottom
            for vy in range(curr_y, y_max + 1):
                grid[(curr_x, vy)] = '|'
            continue

        for vy in range(curr_y, next_y):
            grid[(curr_x, vy)] = '|'
    else:
        next_y = curr_y
        next_x = curr_x

    (left_y, left_x), (right_y, right_x) = find_left_right(y_list, (next_y - 1, next_x))
    if left_y != next_y - 1:
        # went off the left side
        print('off left', (left_x, left_y), (next_x, next_y))
        break

    if right_y != next_y - 1:
        # went off the right side
        print('off right', right_y, next_y)
        break

    # is this a bowl?
    if not all(grid[(vx, next_y)] in ('#', '~') for vx in range(left_x, right_x + 1)):
        # find the gaps

        # left gap
        for sx in range(curr_x - 1, left_x, - 1):
            if grid[(sx, next_y)] in ('#', '~'):
                grid[(sx, next_y - 1)] = '|'
            else:
                if grid[(sx, next_y - 1)] not in ('#', '~'):
                    falling_queue.append((sx, next_y - 1))
                break

        # right gap
        for sx in range(curr_x + 1, right_x):
            if grid[(sx, next_y)] in ('#', '~'):
                grid[(sx, next_y - 1)] = '|'
            else:
                if grid[(sx, next_y - 1)] not in ('#', '~'):
                    falling_queue.append((sx, next_y - 1))
                break

        continue

    curr_y = next_y - 1

    # fill up
    while True:
        (nleft_y, nleft_x), (nright_y, nright_x) = find_left_right(y_list, (curr_y, next_x))
        if nleft_y != curr_y or nright_y != curr_y:
            # wrap around
            # print('wrap around')
            break

        if nleft_x < left_x or nright_x > right_x:
            # print('bounds wrong')
            break

        for vx in range(nleft_x + 1, nright_x):
            grid[(vx, curr_y)] = '~'

        left_x = nleft_x
        right_x = nright_x

        curr_y -= 1

    # fill in running water above
    for vx in range(left_x + 1, right_x):
        grid[(vx, curr_y)] = '|'

    if nleft_y != curr_y or nleft_x < left_x:
        # fall off the left side
        grid[(left_x, curr_y)] = '|'
        falling_queue.append((left_x - 1, curr_y))

    if nright_y != curr_y or nright_x > right_x:
        # fall off the right side
        grid[(right_x, curr_y)] = '|'
        falling_queue.append((right_x + 1, curr_y))


    # if nleft_y == curr_y and nleft_x == left_x:
    #     # fill in to the left
    #     for vx in range(left_x + 1, curr_x):
    #         grid[(vx, curr_y)] = '|'
    # if nright_y == curr_y and nright_x == right_x:
    #     # fill in to the right
    #     for vx in range(curr_x + 1, right_x):
    #         grid[(vx, curr_y)] = '|'
    #
    # if

    # pretty_print(start=52, end=70)

    counter += 1
    if counter > 500:
        print('too far')
        break

for x, y in falling_queue:
    grid[(x, y)] = '@'

for (x, y), v in list(grid.items()):
    if v == '|':
        if grid[(x, y - 1)] == '~' or grid[(x - 1, y)] == '~' or grid[(x + 1)] == '~':
            grid[(x, y)] = '~'

pretty_print()

print(sum(1 for k, v in grid.items() if v in ('|', '~')))
print(sum(1 for k, v in grid.items() if v == '~'))
