from collections import defaultdict, deque
from itertools import count
from more_itertools import partition

with open('day_15/input.txt', 'r') as input_file:
    data_input = input_file.readlines()

data = [line.strip() for line in data_input]

DEBUG = False

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wall(Cell):
    cell_type = 'Wall'

    def __str__(self):
        return '#'

def adjacent(x, y, game_data):
    for vx, vy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        cell = game_data[(x + vx, y + vy)]
        if not isinstance(cell, Wall):
            yield x + vx, y + vy, cell

class Player(Cell):
    ap = 3

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 200

    def __repr__(self):
        return "{}(x={}, y={}, hp={})".format(self.__class__.__name__, self.x, self.y, self.hp)

    def adjacent(self, game_data):
        yield from adjacent(self.x, self.y, game_data)

    def move(self, targets, game_data):
        dist_grid = defaultdict(lambda: -1)
        queue = deque([(self.x, self.y, 0)])
        seen = set()

        while queue:
            next_x, next_y, d = queue.popleft()

            if (next_x, next_y) in seen:
                continue
            seen.add((next_x, next_y))
            dist_grid[(next_x, next_y)] = d

            for adj_x, adj_y, c in adjacent(next_x, next_y, game_data):
                if c is None:
                    queue.append((adj_x, adj_y, d + 1))


        targets = sorted(
            (dist_grid[(x, y)], y, x, c) for d, y, x, c in targets 
            if dist_grid[(x, y)] > -1
        )

        if not targets:
            return

        target = targets[0]
        if DEBUG: print('Move Target:', (target[2], target[1]))

        # shortest path(s)
        d, y, x, c = target

        target_grid = defaultdict(lambda: -1)
        queue = deque([(x, y, 0)])
        seen = set()

        while queue:
            next_x, next_y, d = queue.popleft()
            if (next_x, next_y) in seen:
                continue
            seen.add((next_x, next_y))
            target_grid[(next_x, next_y)] = d

            for adj_x, adj_y, c in adjacent(next_x, next_y, game_data):
                adj_d = dist_grid[(adj_x, adj_y)]
                if adj_d > 0 and adj_d == dist_grid[(next_x, next_y)] - 1:
                    queue.append((adj_x, adj_y, d + 1))

        del game_data[(self.x, self.y)]
        
        _, self.y, self.x = sorted((target_grid[(x, y)], y, x) for x, y, c in self.adjacent(game_data) if target_grid[(x, y)] > -1)[0]
        
        game_data[(self.x, self.y)] = self

        if DEBUG: print('Move To:', (self.x, self.y))

    def attack(self, enemy, game_data):
        assert not isinstance(enemy, type(self))
        enemy.hp -= self.ap
        if enemy.hp <= 0:
            del game_data[(enemy.x, enemy.y)]

class Elf(Player):
    player_type = 'Elf'
    ap = 3

    def __str__(self):
        return 'E'

class Goblin(Player):
    player_type = 'Goblin'

    def __str__(self):
        return 'G'

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def pretty_print(turn_count, width, height, game_data):
    print('After {} rounds:'.format(turn_count + 1))
    if DEBUG:
        if width > 10:
            print((' ' if height <= 10 else '  ') + ''.join(str(x // 10) if x % 10 == 0 else ' ' for x in range(width)))
        print((' ' if height <= 10 else '  ') + ''.join(str(x % 10) for x in range(width)))
    for y in range(width):
        players = []
        row = []
        if DEBUG:
            if height > 10:
                row.append(str(y // 10) if y % 10 == 0 else ' ')
            row.append(str(y % 10))
        for x in range(height):
            c = game_data[(x, y)]
            if isinstance(c, Player):
                players.append(c)
            if c is None:
                row.append('.')
            else:
                row.append(str(c))
        print(''.join(row) + '   ' + ', '.join('{}({})'.format(str(p), p.hp) for p in players))
    print('')

def simulate(data, stop_on_elf_death=False, elf_ap=3):
    players = []
    game_data = defaultdict(lambda: None)

    elves_count = 0

    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c == '#':
                game_data[(x, y)] = Wall(x, y)
            elif c == 'G':
                game_data[(x, y)] = g = Goblin(x, y)
                players.append(g)
            elif c == 'E':
                game_data[(x, y)] = e = Elf(x, y)
                players.append(e)
                elves_count += 1

    width = y + 1
    height = x + 1

    def turn():
        nonlocal players, game_data

        players = sorted(
            (player for player in players if player.hp > 0),
            key=lambda p: (p.y, p.x)
        )
        goblins, elves = partition(lambda x: isinstance(x, Elf), players)

        if not elves or not goblins:
            # game over
            return True

        elves = set(elves)
        goblins = set(goblins)

        enemy_lookup = {
            Elf: goblins,
            Goblin: elves,
        }
        
        for player in players:
            # 1. identify targets
            # 2. can attack? skip move and attack
            # 3. move
            # 4. attack
            if player.hp <= 0:
                continue
            
            if DEBUG: print('Player:', repr(player))
            enemies = enemy_lookup[type(player)]
            # if DEBUG: print('Enemies:', enemies)

            if not enemies:
                return True

            targets = sorted(set(
                (dist((player.x, player.y), (x, y)), y, x, c)
                for enemy in enemies
                for x, y, c in enemy.adjacent(game_data)
                if c is player or c is None
            ))

            # if DEBUG: print('Targets:', targets)

            if not targets:
                continue

            if targets[0][0] > 0:
                # movement
                player.move(targets, game_data)

            adj_enemies = sorted(
                (c.hp, y, x, c) 
                for x, y, c in player.adjacent(game_data) 
                if c in enemies
            )

            if adj_enemies:
                # attack
                enemy = adj_enemies[0][3]
                if DEBUG: print('Attack:', repr(enemy))
                player.attack(enemy, game_data)
                if enemy.hp <= 0:
                    enemy_lookup[type(player)].remove(enemy)
            
            if DEBUG: print('')

    Elf.ap = elf_ap

    if not DEBUG:
        for i in count(0):
            if turn():
                break
            if sum(1 for p in players if isinstance(p, Elf)) < elves_count:
                if stop_on_elf_death:
                    return True
    else:
        pretty_print(-1, width, height, game_data)
        counter = count(0)

        turn()
        i = next(counter)
        pretty_print(i, width, height, game_data)

    # pretty_print(i, width, height, game_data)
    hp_sum = sum(player.hp for player in players if player.hp > 0)
    print(i, '*', hp_sum, '=', hp_sum * i)

# part 1
simulate(data)

# part 2
curr_ap = 3
step = 256

while step > 0:
    step //= 2
    print(curr_ap, step)
    elf_death = simulate(data, stop_on_elf_death=True, elf_ap=curr_ap)
    if elf_death:
        curr_ap += step
    else:
        curr_ap -= step
