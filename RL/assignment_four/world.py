from collections import deque


# ==============================================================
# WORLD
# ==============================================================
SIZE = 5

START = (0, 0)
GOAL = (4, 4)

PITS = [
    (1, 3),
    (2, 2),
    (3, 1),
]

REWARDS = {
    GOAL: 10.0, **{pit: -10.0 for pit in PITS},
}

# Up, right, down, left
MOVES = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
]


def step(state, action):
    """
    Move the agent and return:
        next_state
        reward
        done
    """
    row, col = state
    dr, dc = MOVES[action]
    next_state = (
        min(max(row + dr, 0), SIZE - 1),
        min(max(col + dc, 0), SIZE - 1),
    )
    reward = REWARDS.get(next_state, 0.0)

    # The episode ends when we reach the goal or a pit.
    done = next_state in REWARDS

    return next_state, reward, done


def shortest_path_len():
    """
    Find the shortest path from START to GOAL
    without entering any pits.
    This is only used when displaying the final result.
    """
    distances = {START: 0}
    queue = deque([START])

    while queue:
        state = queue.popleft()

        if state == GOAL:
            return distances[state]

        for action in range(4):
            next_state, _, _ = step(state, action)

            if next_state not in distances and next_state not in PITS:
                distances[next_state] = distances[state] + 1
                queue.append(next_state)

    return None
