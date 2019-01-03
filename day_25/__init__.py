from itertools import combinations
from collections import defaultdict, deque

with open('day_25/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

data = [tuple(map(int, line.split(','))) for line in data_input]


def dist(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


results = defaultdict(set)

for a, b in combinations(range(len(data)), 2):
    results[a].add(a)
    results[b].add(b)
    if dist(data[a], data[b]) <= 3:
        results[a].add(b)
        results[b].add(a)

queue = deque([next(iter(results.keys()))])

constellations = []
constellation = set()
seen = set()

while results:
    if queue:
        next_key = queue.popleft()
    else:
        constellations.append(constellation)
        constellation = set()
        next_key = next(iter(results.keys()))
        assert next_key not in seen

    if next_key in seen:
        continue

    seen.add(next_key)
    constellation.add(next_key)

    queue.extend(results[next_key] - seen)
    del results[next_key]

constellations.append(constellation)


print(len(constellations))
