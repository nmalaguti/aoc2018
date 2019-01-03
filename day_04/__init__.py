import re
from collections import defaultdict
from operator import attrgetter, itemgetter

with open('day_04/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

def parse_line(line):
    # [1518-07-28 00:10]
    m = re.match(r'\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\] (.*)', line)
    return [int(x) for x in m.group(1, 2, 3, 4, 5)] + [m.group(6)]

data = sorted(parse_line(line) for line in data_input)

class GuardData:
    def __init__(self):
        self.guard_id = None
        self.last_sleep = None
        self.last_wake = None
        self.total_sleep = 0
        self.minutes = [0] * 60

    def __repr__(self):
        return 'GuardData(guard_id={}, total_sleep={})'.format(self.guard_id, self.total_sleep)

guards = defaultdict(GuardData)
curr_guard = None

for year, month, day, hour, minute, value in data:
    m = re.match(r'Guard #(\d+) begins shift', value)
    if m:
        curr_guard = m.group(1)
        guards[curr_guard].guard_id = curr_guard
    elif value == 'falls asleep':
        guards[curr_guard].last_sleep = minute
    elif value == 'wakes up':
        guards[curr_guard].last_wake = minute
        guards[curr_guard].total_sleep += minute - guards[curr_guard].last_sleep
        for i in range(guards[curr_guard].last_sleep, minute):
            guards[curr_guard].minutes[i] += 1
    else:
        assert False, 'Unexpected Input'

sleepiest_guard = sorted(guards.values(), key=attrgetter('total_sleep'))[-1]
sleepiest_minute = sorted(enumerate(sleepiest_guard.minutes), key=itemgetter(1))[-1][0]

print(int(sleepiest_guard.guard_id) * sleepiest_minute)

sleepiest_minute_guard = sorted(guards.values(), key=lambda g: max(g.minutes))[-1]
sleepiest_minute_guard_minute = sorted(enumerate(sleepiest_minute_guard.minutes), key=itemgetter(1))[-1][0]

print(int(sleepiest_minute_guard.guard_id) * sleepiest_minute_guard_minute)