"""
The Bellman equation, solved by value iteration.

Same spirit as the earlier Markov chain code -- states, and a rule for
moving between them -- but now there are ACTIONS to choose and REWARDS to
collect, so we compute each state's VALUE instead of just simulating a walk.

    V(s) = max_a  sum_s' P(s'|s,a) [ R(s,a,s') + gamma * V(s') ]

Here the world is a 5-cell line: [0] [1] [2] [3] [4*]
State 4 is the goal -- stepping into it pays a reward of 1.0.
"""

states = [0, 1, 2, 3, 4]
actions = ["left", "right"]
gamma = 0.9  # how much future reward is worth, compared to reward right now - we often have lower gamma when fewer states, and gamma closer to 1.0 when more states.


def step(s, a):
    """Return (next_state, reward) for taking action a in state s.
    This plays the role of P(s'|s,a) and R(s,a,s') combined -- the
    world here is deterministic, so each action leads to exactly one s'.
    State 4 is absorbing: once you're there, you stay, with no further
    reward -- so the payoff is only for *reaching* the goal, once."""
    if s == 4:
        return 4, 0.0
    s_next = max(0, s - 1) if a == "left" else min(4, s + 1)
    reward = 1.0 if s_next == 4 else 0.0
    return s_next, reward


def bellman_update(V):
    """Apply the Bellman equation once to every state."""
    new_V = {}
    for s in states:
        # try every action, keep the best (reward now + discounted future)
        new_V[s] = max(
            step(s, a)[1] + gamma * V[step(s, a)[0]]
            for a in actions
        )
    return new_V


if __name__ == "__main__":
    V = {s: 0.0 for s in states}  # start: every state worth nothing

    for iteration in range(20):
        V = bellman_update(V)
        print(f"iteration {iteration + 1:2d}: " +
              "  ".join(f"V({s})={V[s]:.3f}" for s in states))

    print("\nFinal values:", V)
