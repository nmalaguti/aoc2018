from itertools import count

with open('day_13/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

data = [list(line.rstrip()) for line in data_input]

turns = {
    '>': ['^', '>', 'v', '-'],
    'v': ['>', 'v', '<', '|'],
    '<': ['v', '<', '^', '-'],
    '^': ['<', '^', '>', '|'],
}

movement = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1),
}

tracks = {
    '-': {
        '>': '>',
        '<': '<',
    },
    '\\': {
        '>': 'v',
        '^': '<',
        '<': '^',
        'v': '>'
    },
    '|': {
        'v': 'v',
        '^': '^',
    },
    '/': {
        '>': '^',
        '<': 'v',
        '^': '>',
        'v': '<',
    },
}

class Cart:
    def __init__(self, s, x, y):
        self.s = s
        self.under = turns[self.s][3]
        self.x = x
        self.y = y
        self.crashed = False
        self.tick_count = count()

    def __str__(self):
        return self.s

    def tick(self, state):
        if self.crashed:
            return

        state[self.y][self.x] = self.under

        vx, vy = movement[self.s]
        self.x, self.y = self.x + vx, self.y + vy
        
        self.under = state[self.y][self.x]

        if isinstance(self.under, Cart):
            self.crashed = True
            self.under.crashed = True
            state[self.y][self.x] = self.under.under
            return

        if self.under == '+':
            self.s = turns[self.s][next(self.tick_count) % 3]
        else:
            self.s = tracks[self.under][self.s]
        
        state[self.y][self.x] = self

carts = []

for y, row in enumerate(data):
    for x in range(len(row)):
        if row[x] in turns:
            row[x] = Cart(row[x], x, y)
            carts.append(row[x])

def pretty_print(d):
    for row in d:
        print(''.join(str(c) for c in row))
    print('')

first_crash = None

def tick(carts, state):
    global first_crash

    carts = sorted(carts, key=lambda c: (c.y, c.x))
    for cart in carts:
        cart.tick(state)
        if first_crash is None and cart.crashed:
            first_crash = (cart.x, cart.y)
    carts = [cart for cart in carts if not cart.crashed]
    return carts, state

state = data
# pretty_print(state)
while len(carts) > 1:
    carts, state = tick(carts, state)
    # pretty_print(state)

print('%s,%s' % first_crash)
print('%s,%s' % (carts[0].x, carts[0].y))