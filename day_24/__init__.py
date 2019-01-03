import re
from collections import defaultdict
from typing import Set

with open('day_24/input.txt', 'r') as input_file:
    data_input = input_file.readlines()


PATTERN = re.compile(r'^(\d+) units each with (\d+) hit points( \(.+\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)$')

boost = 0


class Group:
    team_name: str
    num_units: int
    hit_points: int
    weaknesses: Set[str]
    immunities: Set[str]
    attack_damage: int
    attack_type: str
    initiative: int

    def __init__(self, team_name, num_units, hit_points, weaknesses, immunities, attack_damage, attack_type, initiative):
        self.team_name = team_name
        self.num_units = num_units
        self.hit_points = hit_points
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative

    def __repr__(self):
        return (
                "Group(num_units={}, hit_points={}, weaknesses={}, "
                "immunities={}, attack_damage={}, attack_type={}, initiative={})"
                "".format(self.num_units, self.hit_points, self.weaknesses, self.immunities,
                          self.attack_damage, self.attack_type, self.initiative)
        )

    @property
    def effective_power(self):
        global boost
        return self.num_units * (self.attack_damage + (boost if self.team_name == 'Immune System' else 0))

    def damage(self, defender):
        return damage(self, defender)


def parse_weak_immunity(value):
    if value is None:
        return ([], [])

    weaknesses = []
    immunities = []

    value = value.strip().strip('()')
    for part in value.split('; '):
        if 'weak' in part:
            weaknesses.extend(part.split('to ')[1].split(', '))
        elif 'immune' in part:
            immunities.extend(part.split('to ')[1].split(', '))
        else:
            assert False

    return set(weaknesses), set(immunities)


def parse(data_input):
    teams = defaultdict(list)

    for line in data_input:
        if line.rstrip().endswith(':'):
            curr_team = line.rstrip().split(':')[0]
        else:
            m = re.match(PATTERN, line.rstrip())
            if m:
                num_units, hit_points, weak_immune, attack_damage, attack_type, initiative = m.groups()
                weaknesses, immunities = parse_weak_immunity(weak_immune)
                teams[curr_team].append(Group(curr_team,
                                              int(num_units), int(hit_points),
                                              weaknesses, immunities,
                                              int(attack_damage), attack_type,
                                              int(initiative)))

    return teams


def damage(attacker: Group, defender: Group):
    if attacker.attack_type in defender.immunities:
        return 0

    damage = attacker.effective_power
    if attacker.attack_type in defender.weaknesses:
        damage *= 2

    return damage


def fight(teams: dict):
    # target selection
    team_names = teams.keys()
    enemies = {team_name: next(iter(team_names - {team_name})) for team_name in team_names}

    fights = []

    for team_name, team in teams.items():
        defenders = list(teams[enemies[team_name]])
        for attacker in sorted(team, key=lambda t: (t.effective_power, t.initiative), reverse=True):
            targets = [(attacker.damage(defender), defender.effective_power, defender.initiative, defender)
                       for defender in defenders if attacker.damage(defender) > 0]
            if targets:
                target = max(targets)
                fights.append((attacker, target[3]))
                defenders.remove(target[3])

    units_eliminated = False

    # attacking
    for attacker, defender in sorted(fights, key=lambda t: t[0].initiative, reverse=True):
        if attacker.num_units <= 0:
            continue

        possible_damage = attacker.damage(defender)
        num_dead_units = possible_damage // defender.hit_points
        if num_dead_units > 0:
            units_eliminated = True
        defender.num_units -= num_dead_units
        if defender.num_units <= 0:
            teams[defender.team_name].remove(defender)

    return units_eliminated


teams = parse(data_input)

while all(teams.values()):
    fight(teams)

for team in teams.values():
    if team:
        print(sum(group.num_units for group in team))


# part 2
for i in range(100):
    boost = i
    teams = parse(data_input)
    while all(teams.values()):
        if not fight(teams):
            break

    if all(teams.values()) or not teams['Immune System']:
        continue
    else:
        break

print(sum(group.num_units for group in teams['Immune System']))
