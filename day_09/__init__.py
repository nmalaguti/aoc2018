import re
from collections import deque

with open('day_09/input.txt', 'r') as input_file:
    data_input = input_file.read()

m = re.match(r'(\d+) players; last marble is worth (\d+) points', data_input)

num_players = int(m.group(1))
last_marble = int(m.group(2)) * 100

# class Marble:

#     def __init__(self, value):
#         self.nextt = self
#         self.prev = self
#         self.value = value


# class Circle:
#     def __init__(self):
#         self.curr_marble = Marble(0)
#         self.marble_count = 1
#         self.curr_player = 0
#         self.scores = [0] * num_players
    
#     def next_turn(self):
#         if self.marble_count % 23 == 0:
#             self.scores[self.curr_player] += self.marble_count
#             self.move_counterclockwise(7)
#             self.scores[self.curr_player] += self.curr_marble.value
#             self.remove_curr_marble()
#         else:
#             self.move_clockwise(2)
#             self.insert_marble(self.marble_count)

#         self.marble_count += 1
#         self.curr_player += 1
#         self.curr_player %= num_players

#     def move_counterclockwise(self, steps):
#         for i in range(steps):
#             self.curr_marble = self.curr_marble.prev

#     def move_clockwise(self, steps):
#         for i in range(steps):
#             self.curr_marble = self.curr_marble.nextt

#     def remove_curr_marble(self):
#         self.curr_marble.prev.nextt = self.curr_marble.nextt
#         self.curr_marble.nextt.prev = self.curr_marble.prev
#         self.curr_marble = self.curr_marble.nextt

#     def insert_marble(self, value):
#         m = Marble(value)

#         m.prev = self.curr_marble.prev
#         m.nextt = self.curr_marble
#         m.prev.nextt = m
#         m.nextt.prev = m

#         self.curr_marble = m

# circle = Circle()

# while circle.marble_count < last_marble:
#     circle.next_turn()

# print(max(circle.scores))

scores = [0] * num_players
marble_count = 1
curr_player = 0
circle = deque([0])


while marble_count < last_marble:
    if marble_count % 23 == 0:
        circle.rotate(7)
        scores[curr_player] += marble_count + circle.pop()
        circle.rotate(-1)
    else:
        circle.rotate(-1)
        circle.append(marble_count)
    
    marble_count += 1
    curr_player += 1
    curr_player %= num_players

print(max(scores))