import re
from operator import itemgetter
from heapq import heappush, heappop
from itertools import product


with open('day_23/input.txt', 'r') as input_file:
    data_input = iter(input_file.readlines())


def dist(x1, y1, z1, x2, y2, z2):
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


data = [tuple(map(int, re.findall(r'[-0-9]+', line))) for line in data_input]
max_x, max_y, max_z, max_r = max(data, key=itemgetter(3))

print(sum(1 for x, y, z, r in data if dist(x, y, z, max_x, max_y, max_z) <= max_r))


def intersect(x, y, z, r, box_min_x, box_max_x, box_min_y, box_max_y, box_min_z, box_max_z):
    """
    https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection#Sphere_vs._AABB
    """
    bx = max(box_min_x, min(x, box_max_x))
    by = max(box_min_y, min(y, box_max_y))
    bz = max(box_min_z, min(z, box_max_z))

    return dist(x, y, z, bx, by, bz) <= r


def find_best_distance(queue):
    # best points (there may be more than one) sorted by count and distance from origin
    points = []
    seen = set()

    while queue:
        # count is stored negative so the heap sorts largest first
        neg_count, box_min_x, box_max_x, box_min_y, box_max_y, box_min_z, box_max_z = heappop(queue)

        if (box_min_x, box_max_x, box_min_y, box_max_y, box_min_z, box_max_z) in seen:
            continue

        seen.add((box_min_x, box_max_x, box_min_y, box_max_y, box_min_z, box_max_z))

        # skip boxes where the count smaller than the best
        if points and -neg_count < -points[0][0]:
            continue

        # we have a point
        if box_min_x == box_max_x and box_min_y == box_max_y and box_min_z == box_max_z:
            dist_from_origin = dist(box_min_x, box_min_y, box_min_z, 0, 0, 0)
            heappush(points, (neg_count, dist_from_origin,
                              box_min_x, box_max_x,
                              box_min_y, box_max_y,
                              box_min_z, box_max_z))

        x_mid = box_min_x + ((box_max_x - box_min_x) // 2)
        y_mid = box_min_y + ((box_max_y - box_min_y) // 2)
        z_mid = box_min_z + ((box_max_z - box_min_z) // 2)

        permutations = product(
            ((box_min_x, x_mid), (x_mid + 1, box_max_x)),
            ((box_min_y, y_mid), (y_mid + 1, box_max_y)),
            ((box_min_z, z_mid), (z_mid + 1, box_max_z))
        )

        for (min_x, max_x), (min_y, max_y), (min_z, max_z) in permutations:
            count = sum(1 for x, y, z, r in data
                        if intersect(x, y, z, r,
                                     min_x, max_x,
                                     min_y, max_y,
                                     min_z, max_z))

            heappush(queue, (-count,
                             min_x, max_x,
                             min_y, max_y,
                             min_z, max_z))

    return heappop(points)[1]


# make sure (0, 0, 0) is in the ranges
min_x = min(x for x, y, z, r in data + [(0, 0, 0, 0)])
max_x = max(x for x, y, z, r in data + [(0, 0, 0, 0)])
min_y = min(y for x, y, z, r in data + [(0, 0, 0, 0)])
max_y = max(y for x, y, z, r in data + [(0, 0, 0, 0)])
min_z = min(z for x, y, z, r in data + [(0, 0, 0, 0)])
max_z = max(z for x, y, z, r in data + [(0, 0, 0, 0)])

queue = [(-len(data), min_x, max_x, min_y, max_y, min_z, max_z)]

print(find_best_distance(queue))
