from collections import defaultdict, deque


with open('day_20/input.txt', 'r') as input_file:
    data_input = input_file.read().rstrip()

data = deque(data_input)
# data = deque(r'^ENWWW(NEEE|SSE(EE|N))$')  # 10
# data = deque(r'^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')  # 18
# data = deque(r'^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')  # 23
# data = deque(r'^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')  # 31
# data = deque(r'^WWWW(SSSSS|)WWWWW$')  # 14

rooms = defaultdict(lambda: float('inf'))


# def find_closing_paren(regex_deque: deque):
#     res = deque()
#     paren_count = 1
#     while paren_count > 0:
#         token = regex_deque.popleft()
#         res.append(token)
#         if token == '(':
#             paren_count += 1
#         elif token == ')':
#             paren_count -= 1
#     res.pop()  # drop closing paren
#     return res


# def parse(start_room, rooms, regex_deque: deque, after_branch: deque, depth=0):
#     curr_room = start_room
#     while regex_deque:
#         token = regex_deque.popleft()
#         if token in '^$':
#             continue
#         if token == '(':
#             # find closing paren
#             enclosed = find_closing_paren(regex_deque)
#             parse(curr_room, rooms, enclosed, regex_deque, depth + 1)
#         elif token == '|':
#             # branch
#             parse(curr_room, rooms, deque(after_branch), deque(), depth + 1)
#             curr_room = start_room
#         else:
#             x, y = curr_room
#             d = rooms[curr_room]
#             if token == 'N':
#                 y += 1
#             elif token == 'E':
#                 x += 1
#             elif token == 'S':
#                 y -= 1
#             elif token == 'W':
#                 x -= 1
#             curr_room = (x, y)
#             rooms[curr_room] = min(rooms[curr_room], d + 1)
#     return curr_room


# def parse_bfs(queue: deque, rooms):
#     while queue:
#         print(len(queue))
#         start_room, branch, rest = queue.popleft()
#         curr_room = start_room
#         while branch:
#             token = branch.popleft()
#             if token in '^$':
#                 continue
#             if token == '(':
#                 # find closing paren
#                 enclosed = find_closing_paren(branch)
#                 queue.append((curr_room, enclosed, [branch] + rest))
#             elif token == '|':
#                 # branch
#                 if rest:
#                     next_branch, *rest_branches = rest
#                     queue.append((curr_room, deque(next_branch), rest_branches))
#                 curr_room = start_room
#             else:
#                 x, y = curr_room
#                 d = rooms[curr_room]
#                 if token == 'N':
#                     y += 1
#                 elif token == 'E':
#                     x += 1
#                 elif token == 'S':
#                     y -= 1
#                 elif token == 'W':
#                     x -= 1
#                 curr_room = (x, y)
#                 rooms[curr_room] = min(rooms[curr_room], d + 1)


def parse_other(input_regex, rooms, points):
    curr_points = points
    res_points = set()
    while input_regex:
        token = input_regex.popleft()
        if token in '^$':
            continue
        if token == '(':
            curr_points = parse_other(input_regex, rooms, curr_points)
        elif token == '|':
            if input_regex[0] == ')':
                res_points |= points
            res_points |= curr_points
            curr_points = points
        elif token == ')':
            return res_points
        else:
            new_points = set()
            for x, y in curr_points:
                d = rooms[(x, y)]
                if token == 'N':
                    y += 1
                elif token == 'E':
                    x += 1
                elif token == 'S':
                    y -= 1
                elif token == 'W':
                    x -= 1
                new_points.add((x, y))
                rooms[(x, y)] = min(rooms[(x, y)], d + 1)

            curr_points = new_points
    return res_points


start_room = (0, 0)
rooms[start_room] = 0
parse_other(data, rooms, {start_room})
# parse(start_room, rooms, data, deque(), 0)
# parse_bfs(deque([(start_room, data, [])]), rooms)
print(max(rooms.values()))
print(sum(1 for d in rooms.values() if d >= 1000))
