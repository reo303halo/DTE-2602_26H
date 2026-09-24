"""
Turning the word Markov chain into an MDP: same states, but now there
are ACTIONS to choose and REWARDS to collect.

  Markov chain:  transition[state]            -> {next_state: prob}
  MDP:           transition[state][action]     -> {next_state: prob}
                 reward[state][action]          -> payoff for choosing that action

The agent no longer just drifts with random.choices() -- it follows a
POLICY (its steering wheel) and racks up a SCORE (the scoreboard).
"""
import random

states = ["i", "love", "want", "need", "to", "eat", "go", "pizza", "home", "sleep", "END"]

# --- NEW: actions available in each state (the agent's choices) ---
actions = {
    "i":    ["love", "want", "need"],  # which word to say next
    "love": ["to"], "want": ["to"], "need": ["to"],  # forced -- only one option
    "to":   ["eat", "go"],             # the interesting choice: eat, or go?
    "eat":  ["pizza"],
    "go":   ["home_or_sleep"],         # one action, but the OUTCOME is uncertain
    "pizza": ["end"], "home": ["end"], "sleep": ["end"],
    "END":  [],
}

# --- transition now keyed by (state, action) -> {next_state: probability} ---
# Compare to the old version: transition["to"] = {"eat": 0.5, "go": 0.5}
# That 0.5/0.5 was random DRIFT. Now "eat" and "go" are actions the agent
# picks on purpose -- the only leftover randomness is what "go" leads to.
transition = {
    ("i", "love"): {"love": 1.0},
    ("i", "want"): {"want": 1.0},
    ("i", "need"): {"need": 1.0},
    ("love", "to"): {"to": 1.0},
    ("want", "to"): {"to": 1.0},
    ("need", "to"): {"to": 1.0},
    ("to", "eat"): {"eat": 1.0},
    ("to", "go"): {"go": 1.0},
    ("eat", "pizza"): {"pizza": 1.0},
    ("go", "home_or_sleep"): {"home": 0.5, "sleep": 0.5},  # still risky!
    ("pizza", "end"): {"END": 1.0},
    ("home", "end"): {"END": 1.0},
    ("sleep", "end"): {"END": 1.0},
}

# --- NEW: reward for taking an action in a state (the scoreboard) ---
reward = {
    ("i", "love"): 0.2,     # "I love..." -- a nice opener
    ("i", "want"): 0.0,
    ("i", "need"): -0.1,    # "I need..." sounds a bit desperate
    ("to", "eat"): 0.0,
    ("to", "go"): 0.0,
    ("eat", "pizza"): 1.0,  # pizza is guaranteed and reliably good
    ("go", "home_or_sleep"): 0.0,  # the payoff here depends on next_state below
}
# some transitions pay off based on where you LAND, not just the action:
landing_bonus = {"pizza": 5.0, "home": 1.0, "sleep": -1.0}


def next_state(state, action):
    """Same sampling logic as before -- just looks up (state, action) now."""
    outcomes = transition[(state, action)]
    choices = list(outcomes.keys())
    weights = list(outcomes.values())
    return random.choices(choices, weights=weights)[0]


def run_episode(policy):
    """Follow a policy (the agent's chosen action per state) and total the reward."""
    state = "i"
    history = [state]
    total_reward = 0.0

    while state != "END" and actions[state]:
        action = policy[state]
        total_reward += reward.get((state, action), 0.0)
        state = next_state(state, action)
        total_reward += landing_bonus.get(state, 0.0)
        history.append(state)

    return history, total_reward


if __name__ == "__main__":
    # The agent's policy: what it chooses to do in each state.
    # This is the "steering wheel" -- swap these and behavior changes.
    policy = {
        "i": "love",   # say "I love..."
        "love": "to", "want": "to", "need": "to",
        "to": "eat",   # <- try changing this to "go" and rerun
        "go": "home_or_sleep",  # only used if "to" is set to "go"
        "eat": "pizza",
        "pizza": "end", "home": "end", "sleep": "end",
    }

    for _ in range(3):
        history, total_reward = run_episode(policy)
        print(f"{' '.join(history):45s}  total reward = {total_reward:+.1f}")