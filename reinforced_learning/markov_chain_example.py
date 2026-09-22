"""
Simple Markov chain simulation: a two-state weather model (Sunny / Rainy).
"""
import random

states = ["Sunny", "Rainy"]
transition = {
    "Sunny": {"Sunny": 0.7, "Rainy": 0.3},
    "Rainy": {"Sunny": 0.4, "Rainy": 0.6},
}

def next_state(current):
    choices = list(transition[current].keys())
    weights = list(transition[current].values())
    return random.choices(choices, weights=weights)[0]

if __name__ == "__main__":
    state = "Sunny"
    history = [state]
    for _ in range(10):
        state = next_state(state)
        history.append(state)

    print(" -> ".join(history))