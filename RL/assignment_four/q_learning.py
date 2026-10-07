import random
import numpy as np
from parameters import (
    ALPHA,
    EPSILON,
    GAMMA,
    MAXSTEPS,
    SEED,
)
from world import (
    GOAL,
    START,
    SIZE,
    step,
)


class QLearningAgent:
    def __init__(self):
        self.q = np.zeros((5, 5, 4))

        # Random generator used for exploration.
        self.rng = random.Random(SEED)

        # Store the result of each episode.
        self.history = []


    # ==============================================================
    # ACTION SELECTION
    # ==============================================================
    def choose(self, state):
        """
        Choose an action using epsilon-greedy selection.
        With probability EPSILON:
            explore = choose a random action
        Otherwise:
            exploit = choose the best known action
        """

        # ----------------------------------------------------------
        # EXPLORE
        # ----------------------------------------------------------
        if self.rng.random() < EPSILON:
            return self.rng.randrange(4), True

        # ----------------------------------------------------------
        # EXPLOIT
        # ----------------------------------------------------------
        values = self.q[state]
        best_actions = [
            action
            for action in range(4)
            if values[action] == values.max()
        ]

        return self.rng.choice(best_actions), False


    def episode(self):
        """
        Run one episode of Q-learning.
        This is the central algorithm.
        """
        state = START
        step_number = 0
        done = False
        outcome = "step limit"

        # ----------------------------------------------------------
        # REPEAT UNTIL THE EPISODE ENDS
        # ----------------------------------------------------------
        while not done and step_number < MAXSTEPS:
            action, explored = self.choose(state)
            next_state, reward, done = step(
                state,
                action,
            )

            # ------------------------------------------------------
            # Q-LEARNING UPDATE
            # -----------------------------------------------------
            old = self.q[state][action]
            best_next = self.q[next_state].max()
            new = old + ALPHA * (
                reward
                + GAMMA * best_next
                - old
            )
            self.q[state][action] = new

            # ------------------------------------------------------
            # CHECK WHETHER THE EPISODE ENDED
            # ------------------------------------------------------
            step_number += 1
            if done:
                if next_state == GOAL:
                    outcome = "goal"
                else:
                    outcome = "pit"
            state = next_state
        self.history.append((step_number, outcome))

        return outcome


    # ==============================================================
    # TRAINING
    # ==============================================================
    def train(self, episodes):
        for _ in range(episodes):
            self.episode()

    # ==============================================================
    # TEST THE CURRENT POLICY
    # ==============================================================
    def will_reach_goal(self):
        """
        Test whether the next episode reaches the goal.
        Everything is restored afterwards, so this test does not
        change the actual learning.
        """
        saved_q = self.q.copy()
        saved_rng = self.rng.getstate()
        saved_history = list(self.history)

        outcome = self.episode()

        self.q = saved_q
        self.rng.setstate(saved_rng)
        self.history = saved_history

        return outcome == "goal"


    # ==============================================================
    # GREEDY PATH
    # ==============================================================
    def greedy_path(self):
        """
        Follow the best-known action from START.
        This shows what the agent has learned after training.
        """
        path = [START]
        state = START

        for _ in range(SIZE * SIZE):
            action = int(
                self.q[state].argmax()
            )
            state, _, done = step(
                state,
                action,
            )
            path.append(state)
            if done:
                break

        return path
    