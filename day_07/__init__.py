import re
from collections import defaultdict, deque
import heapq

with open('day_07/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

REGEX = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')

data = []

for line in data_input:
    m = re.match(REGEX, line)
    if m:
        data.append(m.group(1, 2))

class Node:

    def __init__(self):
        self.step = None
        self.prereqs = set()
        self.postreqs = set()

    def __repr__(self):
        return "Node(step={}, prereqs={}, postreqs={})".format(self.step, self.prereqs, self.postreqs)

steps = defaultdict(Node)

for pre, post in data:
    node = steps[pre]
    node.step = pre
    node.postreqs.add(post)

    node = steps[post]
    node.step = post
    node.prereqs.add(pre)

# available_steps = [(s, n) for s, n in steps.items() if not n.prereqs]

# heapq.heapify(available_steps)

# order = []

# while available_steps:
#     s, n = heapq.heappop(available_steps)
#     order.append(s)
#     for postreq in n.postreqs:
#         steps[postreq].prereqs.remove(s)
#         if not steps[postreq].prereqs:
#             heapq.heappush(available_steps, (postreq, steps[postreq]))

# print(''.join(order))

def duration(step):
    return 60 + ord(step) - 64

available_steps = [(s, n) for s, n in steps.items() if not n.prereqs]

heapq.heapify(available_steps)

WORKER_COUNT = 5

available_workers = WORKER_COUNT
busy_workers = []

order = []

time = 0

while available_steps or busy_workers:
    if available_steps and available_workers:
        # start the next step
        next_step, n = heapq.heappop(available_steps)
        available_workers -= 1
        heapq.heappush(busy_workers, (time + duration(next_step), next_step))
        # print('start   :', time, next_step, available_workers, len(available_steps))
    else:
        # complete a step
        time, completed_step = heapq.heappop(busy_workers)
        available_workers += 1
        order.append(completed_step)
        n = steps[completed_step]
        for postreq in n.postreqs:
            steps[postreq].prereqs.remove(completed_step)
            if not steps[postreq].prereqs:
                heapq.heappush(available_steps, (postreq, steps[postreq]))
        # print('complete:', time, completed_step, available_workers, len(available_steps))

print(time)
