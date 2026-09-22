"""
Simple Markov chain simulation: word autocomplete (same idea as the
Sunny / Rainy weather example, just with words as the states).
"""
import random

states = ["i", "love", "want", "to", "eat", "pizza", ""]
transition = {
    "i":     {"love": 1/3, "want": 1/3, "need": 1/3},
    "love":  {"to": 1.0},
    "want":  {"to": 1.0},
    "need":  {"to": 1.0},
    "to":    {"eat": 0.5, "go": 0.5},
    "eat":   {"pizza": 1.0},
    "go":    {"home": 0.5, "to sleep": 0.5},
    "pizza": {"": 1.0},
    "home":  {"": 1.0},
    "to sleep": {"": 1.0},
}

def next_state(current):
    choices = list(transition[current].keys())
    weights = list(transition[current].values())
    return random.choices(choices, weights=weights)[0]

if __name__ == "__main__":
    state = "i"
    history = [state]
    for _ in range(5):
        state = next_state(state)
        history.append(state)

    print(" ".join(history))