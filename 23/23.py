"""
this is just a bfs/dfs i think

maybe save "middle" hallway parts as separate list
treat whole area as grid, add walls where " ", treat some coords special

rules:
- never stop outside the room
- only go inside if correct destination and no other "wrong" in there
- once in hallway, stay there until it can mve inside room
"""
import sys
from copy import deepcopy

COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
DONE_STATE = ({0: ['A', 'A'], 1: ['B', 'B'], 2: ['C', 'C'], 3: ['D', 'D']}, list('.' * 11))
DONE_STATE_PART2 = (
    {0: ['A', 'A', 'A', 'A'], 1: ['B', 'B', 'B', 'B'], 2: ['C', 'C', 'C', 'C'], 3: ['D', 'D', 'D', 'D']},
    list('.' * 11))
START_STATE_EX = ({0: ['B', 'A'], 1: ['C', 'D'], 2: ['B', 'C'], 3: ['D', 'A']}, list('.' * 11))
START_STATE_MY = ({0: ['D', 'C'], 1: ['D', 'A'], 2: ['B', 'B'], 3: ['A', 'C']}, list('.' * 11))
START_STATE_EX_PART2 = (
    {0: ['B', 'D', 'D', 'A'], 1: ['C', 'C', 'B', 'D'], 2: ['B', 'B', 'A', 'C'], 3: ['D', 'A', 'C', 'A']},
    list('.' * 11))
START_STATE_MY_PART2 = (
    {0: ['D', 'D', 'D', 'C'], 1: ['D', 'C', 'B', 'A'], 2: ['B', 'B', 'A', 'B'], 3: ['A', 'A', 'C', 'C']},
    list('.' * 11))

GOALS = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

# range(lower_col + 2, lower_col + 2 + (3 + ((diff_cols)) - 1) * 2))
CHECK_HALLWAY = {frozenset({0, 1}): [2, 3, 4],
                 frozenset({0, 2}): [2, 3, 4, 5, 6],
                 frozenset({0, 3}): [2, 3, 4, 5, 6, 7, 8],
                 frozenset({1, 2}): [4, 5, 6],
                 frozenset({1, 3}): [4, 5, 6, 7, 8],
                 frozenset({2, 3}): [6, 7, 8]}

HALLWAY_POS = [0, 1, 3, 5, 7, 9, 10]


def can_move_goal(state, col, row, pod):
    already_done = GOALS[pod] == col
    if already_done:
        return None, None, False
    goal = GOALS[pod]
    to_check = CHECK_HALLWAY[frozenset({col, goal})]
    hallway_free = all([True if v == '.' else False for (i, v) in enumerate(state[1]) if i in to_check])
    new_state = deepcopy(state)
    col_to_check = [True if state[0][col][i] == '.' else False for i in range(0, row)]
    free_col = (len(col_to_check) > 0 and all(col_to_check)) or row == 0
    if not PART2:
        if hallway_free and free_col and state[0][goal][1] == '.' and state[0][goal][0] == '.':
            new_state[0][col][row] = '.'
            new_state[0][goal][1] = pod
            cost = (len(to_check) + row + 2) * COST[pod]
            return new_state, cost, True
        if hallway_free and free_col and state[0][goal][1] == pod and state[0][goal][0] == '.':
            new_state[0][col][row] = '.'
            new_state[0][goal][0] = pod
            cost = (len(to_check) + row + 1) * COST[pod]
            return new_state, cost, True
    else:
        if hallway_free and free_col and state[0][goal][3] == '.' and state[0][goal][2] == '.' and state[0][goal][
            1] == '.' and state[0][goal][0] == '.':
            new_state[0][col][row] = '.'
            new_state[0][goal][3] = pod
            cost = (len(to_check) + row + 4) * COST[pod]
            return new_state, cost, True
        if hallway_free and free_col and state[0][goal][3] == pod and state[0][goal][2] == '.' and state[0][goal][
            1] == '.' and state[0][goal][0] == '.':
            new_state[0][col][row] = '.'
            new_state[0][goal][2] = pod
            cost = (len(to_check) + row + 3) * COST[pod]
            return new_state, cost, True
        if hallway_free and free_col and state[0][goal][3] == pod and state[0][goal][2] == pod and state[0][goal][
            1] == '.' and state[0][goal][0] == '.':
            new_state[0][col][row] = '.'
            new_state[0][goal][1] = pod
            cost = (len(to_check) + row + 2) * COST[pod]
            return new_state, cost, True
        if hallway_free and free_col and state[0][goal][3] == pod and state[0][goal][2] == pod and state[0][goal][
            1] == pod and state[0][goal][0] == '.':
            new_state[0][col][row] = '.'
            new_state[0][goal][0] = pod
            cost = (len(to_check) + row + 1) * COST[pod]
            return new_state, cost, True
    return None, None, False


# one of possible positions HALLWAY_POS
# they can also move in the middle hallway
def can_move_hallway(state, col, row, pod, goal_idx):
    already_done = GOALS[pod] == col
    below = 2 if not PART2 else 4
    others_below_done = all([True if state[0][col][i] == pod else False for i in range(row, below)])
    if already_done and others_below_done:
        return None, None, False

    new_state = deepcopy(state)
    start, end = min(goal_idx, 2 + (col * 2)), max(goal_idx, 2 + (col * 2))
    highway_to_check = range(start, end + 1)
    free_way = all([True if state[1][i] == '.' else False for i in highway_to_check])
    col_to_check = [True if state[0][col][i] == '.' else False for i in range(0, row)]
    free_col = (len(col_to_check) > 0 and all(col_to_check)) or row == 0
    if free_way and free_col:
        new_state[1][goal_idx] = pod
        new_state[0][col][row] = '.'
        cost = (len(highway_to_check) + row) * COST[pod]
        return new_state, cost, True
    return None, None, False


def can_move_hallway_goal(state, way_idx):
    pod = state[1][way_idx]
    goal = GOALS[pod]
    offset = 2 + (goal * 2)
    if way_idx < offset:
        start, end = way_idx + 1, offset
    else:
        start, end = offset, way_idx - 1
    to_check = [i for i in range(start, end + 1)]
    hallway_free = all([True if state[1][i] == '.' else False for i in to_check])
    new_state = deepcopy(state)
    if not PART2:
        if hallway_free and state[0][goal][1] == '.' and state[0][goal][0] == '.':
            new_state[1][way_idx] = '.'
            new_state[0][goal][1] = pod
            cost = (len(to_check) + 2) * COST[pod]
            return new_state, cost, True
        if hallway_free and state[0][goal][1] == pod and state[0][goal][0] == '.':
            new_state[1][way_idx] = '.'
            new_state[0][goal][0] = pod
            cost = (len(to_check) + 1) * COST[pod]
            return new_state, cost, True
    else:
        if hallway_free and state[0][goal][3] == '.' and state[0][goal][2] == '.' and state[0][goal][1] == '.' and \
                state[0][goal][0] == '.':
            new_state[1][way_idx] = '.'
            new_state[0][goal][3] = pod
            cost = (len(to_check) + 4) * COST[pod]
            return new_state, cost, True
        if hallway_free and state[0][goal][3] == pod and state[0][goal][2] == '.' and state[0][goal][1] == '.' and \
                state[0][goal][0] == '.':
            new_state[1][way_idx] = '.'
            new_state[0][goal][2] = pod
            cost = (len(to_check) + 3) * COST[pod]
            return new_state, cost, True
        if hallway_free and state[0][goal][3] == pod and state[0][goal][2] == pod and state[0][goal][1] == '.' and \
                state[0][goal][0] == '.':
            new_state[1][way_idx] = '.'
            new_state[0][goal][1] = pod
            cost = (len(to_check) + 2) * COST[pod]
            return new_state, cost, True
        if hallway_free and state[0][goal][3] == pod and state[0][goal][2] == pod and state[0][goal][1] == pod and \
                state[0][goal][0] == '.':
            new_state[1][way_idx] = '.'
            new_state[0][goal][0] = pod
            cost = (len(to_check) + 1) * COST[pod]
            return new_state, cost, True
    return None, None, False


def solve(state):
    (bot, top) = state
    key = (tuple((k, tuple(v)) for k, v in bot.items()), tuple(top))
    if (PART2 and state == DONE_STATE_PART2) or state == DONE_STATE:
        return 0
    if key in DP:
        return DP[key]

    possibilities = []
    # check move from cols to goal or hallway
    for col, pods in bot.items():  #
        for pos, pod in enumerate(pods):
            if pod in GOALS.keys():  # is a pod and not already correct
                # check move to goal
                (new_state, cost, moved) = can_move_goal(state, col, pos, pod)
                if moved:
                    possibilities.append((new_state, cost))
                # check move to hallway
                free = [idx for idx in HALLWAY_POS if top[idx] == '.']
                for hallway_goal in free:
                    (new_state, cost, moved) = can_move_hallway(state, col, pos, pod, hallway_goal)
                    if moved:
                        possibilities.append((new_state, cost))

    # check moves from hallway to goal
    for idx, pod in enumerate(top):
        if pod in GOALS.keys():
            (new_state, cost, moved) = can_move_hallway_goal(state, idx)
            if moved:
                possibilities.append((new_state, cost))

    costs = [cost + solve(new_state) for (new_state, cost) in possibilities]
    if len(costs) == 0:
        cost = 1e9
    else:
        cost = min(costs)
    DP[key] = cost
    return cost


DP = {}
PART2 = False
print(f"part1: {solve(START_STATE_MY)}")

DP = {}
PART2 = True
print(f"part2: {solve(START_STATE_MY_PART2)}")
