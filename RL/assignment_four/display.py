import re
import sys
import time

from parameters import ALPHA, DELAY, EPISODES, EPSILON, GAMMA, MAXSTEPS, WATCH
from world import GOAL, PITS, SIZE, START, shortest_path_len

# ==============================================================
# DISPLAY SETTINGS
# ==============================================================

ARROWS = "↑→↓←"
USE_COLOR = True
ANSI = re.compile(r"\x1b\[[0-9;]*m")

BOLD = "1"
GREEN = "1;32"
RED = "31"
YELLOW = "1;33"
DIM = "2"
REV = "7"
CYAN = "36"


# ==============================================================
# FORMATTING HELPERS
# ==============================================================

def col(text, code):
    """Add terminal colour if colours are enabled."""
    if USE_COLOR:
        return f"\033[{code}m{text}\033[0m"
    return text


def visible_length(text):
    """Length of text without ANSI colour codes."""
    return len(ANSI.sub("", text))


def fmt(value):
    """Format a Q-value."""
    if value < 0:
        return f"({value:.2f})"
    return f"{value:.2f}"


def side_by_side(left, right, gap=4):
    """Put two blocks of text next to each other."""
    width = max(visible_length(line) for line in left)
    output = []

    for i in range(max(len(left), len(right))):
        left_line = left[i] if i < len(left) else ""
        right_line = right[i] if i < len(right) else ""
        padding = " " * (width - visible_length(left_line) + gap)
        output.append(left_line + padding + right_line)

    return output


# ==============================================================
# BOARD
# ==============================================================

def board_lines(agent=None, trail=(), numbers=None):
    """Create the text representation of the board."""
    separator = "+" + "---+" * SIZE
    lines = [separator]

    for row in range(SIZE):
        line = "|"

        for col_number in range(SIZE):
            cell = (row, col_number)

            if cell == agent:
                character = col("A", GREEN)
            elif cell == GOAL:
                character = col("G", YELLOW)
            elif cell in PITS:
                character = col("X", RED)
            elif numbers and cell in numbers:
                character = col(str(numbers[cell] % 10), CYAN)
            elif cell == START:
                character = "S"
            elif cell in trail:
                character = col("·", DIM)
            else:
                character = " "

            line += f" {character} |"

        lines += [line, separator]

    return lines


# ==============================================================
# Q-TABLE
# ==============================================================

def qpanel(q, highlight=None):
    """Display the best action and Q-value for each cell."""
    separator = "+" + "-" * 9 + ("+" + "-" * 9) * (SIZE - 1) + "+"
    lines = [separator]

    for row in range(SIZE):
        line = "|"

        for col_number in range(SIZE):
            cell = (row, col_number)

            if cell == GOAL:
                text = col("G".center(9), YELLOW)
            elif cell in PITS:
                text = col("X".center(9), RED)
            else:
                values = q[row, col_number]

                if values.max() == values.min():
                    arrow = "·"
                else:
                    arrow = ARROWS[int(values.argmax())]

                text = f" {arrow}{values.max():6.2f} "

                if cell == highlight:
                    text = col(text, REV)

            line += text + "|"

        lines += [line, separator]

    return lines


# ==============================================================
# DEMO DISPLAY
# ==============================================================

class DemoDisplay:

    def __init__(self, agent):
        self.agent = agent
        self.first_frame = True

    # ----------------------------------------------------------
    # DRAW
    # ----------------------------------------------------------

    def show(self, agent_position, trail, info, highlight=None, numbers=None):
        left = [col("BOARD".center(21), BOLD)]
        left += board_lines(agent_position, trail, numbers)

        right = [
            col(
                "Q-TABLE (arrow = best action, number = best value)",
                BOLD,
            )
        ]
        right += qpanel(self.agent.q, highlight)

        lines = side_by_side(left, right) + [""] + info

        first = "\033[2J" if self.first_frame else ""
        self.first_frame = False

        body = "\n".join(line + "\033[K" for line in lines)
        sys.stdout.write(first + "\033[H" + body + "\n\033[J")
        sys.stdout.flush()

    # ----------------------------------------------------------
    # WAIT
    # ----------------------------------------------------------

    def wait(self, seconds=None):
        time.sleep(DELAY if seconds is None else seconds)

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------

    def header(self, episode, step):
        return col(
            f"Episode {episode}/{EPISODES}   "
            f"step {step}   "
            f"ε = {EPSILON}   "
            f"α = {ALPHA}   "
            f"γ = {GAMMA}",
            BOLD,
        )

    # ----------------------------------------------------------
    # ONE DISPLAYED EPISODE
    # ----------------------------------------------------------

    def show_episode(self, episode, note=""):
        state = START
        trail = set()
        step_number = 0
        done = False
        outcome = "step limit"

        info = [
            self.header(episode, 0),
            f"The agent starts at S. {note}",
            "All Q-values are updated with",
            "Q(s,a) ← Q(s,a) + α·(",
            "r + γ·max Q(s',·) − Q(s,a))",
        ]

        self.show(state, trail, info)
        self.wait()

        while not done and step_number < MAXSTEPS:
            action, explored = self.agent.choose(state)

            next_state, reward, done = self._take_step(state, action)

            old = self.agent.q[state][action]
            best_next = self.agent.q[next_state].max()
            new = old + ALPHA * (reward + GAMMA * best_next - old)
            self.agent.q[state][action] = new

            step_number += 1

            if done:
                outcome = "goal" if next_state == GOAL else "pit"

            trail.add(state)

            kind = (
                "random move (explore)"
                if explored
                else "best known move (exploit)"
            )

            values = "   ".join(
                col(f"{ARROWS[i]} {self.agent.q[state][i]:5.2f}", REV)
                if i == action
                else f"{ARROWS[i]} {self.agent.q[state][i]:5.2f}"
                for i in range(4)
            )

            tail = "  (terminal: nothing comes after it)" if done else ""

            info = [
                self.header(episode, step_number),
                (
                    f"Action {ARROWS[action]}  {kind}      "
                    f"reward {reward:+.0f}      "
                    f"new state {next_state}"
                ),
                (
                    f"Q{state}{ARROWS[action]} = "
                    f"{fmt(old)} + {ALPHA} · ("
                    f"{fmt(reward)} + {GAMMA} · {fmt(best_next)} − "
                    f"{fmt(old)}) = "
                    f"{col(f'{new:.2f}', YELLOW)}{tail}"
                ),
                f"Q{state} now:   {values}",
            ]

            if done:
                if outcome == "goal":
                    message = (
                        f"Episode {episode} ended: "
                        f"reached the GOAL in {step_number} steps."
                    )
                    colour = GREEN
                else:
                    message = (
                        f"Episode {episode} ended: "
                        f"fell into a PIT after {step_number} steps."
                    )
                    colour = RED

                info.append(col(message, colour))

            self.show(next_state, trail, info, highlight=state)
            self.wait(DELAY * (3 if done else 1))

            state = next_state

        if outcome == "step limit":
            print(
                col(
                    f"Episode {episode} hit the step limit ({MAXSTEPS}).",
                    RED,
                )
            )
            self.wait()

        return outcome

    def _take_step(self, state, action):
        """
        Let the environment handle the action.

        Kept here only so the display can run a detailed episode.
        """
        from world import step

        return step(state, action)

    # ----------------------------------------------------------
    # TRAINING SUMMARY
    # ----------------------------------------------------------

    def banner(self, first, last):
        chunk = self.agent.history[first - 1:last]

        goals = sum(outcome == "goal" for _, outcome in chunk)
        pits = sum(outcome == "pit" for _, outcome in chunk)
        average = sum(steps for steps, _ in chunk) / len(chunk)

        info = [
            col(
                f"Episodes {first}-{last} were trained without drawing.",
                BOLD,
            ),
            (
                f"{goals} reached the goal, {pits} fell into a pit, "
                f"{average:.1f} steps on average."
            ),
            "This is the Q-table the agent has now.",
        ]

        self.show(None, (), info)
        self.wait(1.5)

    # ----------------------------------------------------------
    # FINAL RESULT
    # ----------------------------------------------------------

    def finish(self):
        path = self.agent.greedy_path()
        reached = path[-1] == GOAL

        numbers = {cell: i for i, cell in enumerate(path)} if reached else None

        shortest = shortest_path_len()

        info = [col(f"Training finished after {EPISODES} episodes.", BOLD)]

        if reached:
            info.append(
                f"Greedy path from S: {len(path) - 1} moves "
                f"(the shortest possible is {shortest}).  "
                f"Digits show the order."
            )
        else:
            info.append(
                "The greedy path does not reach the goal yet: "
                "train longer or change the settings."
            )

        info.append(
            "Read the table: the arrows form the policy, the values grow "
            "toward G and drop next to the pits."
        )

        self.show(None, (), info, numbers=numbers)

    # ----------------------------------------------------------
    # MAIN DISPLAY LOOP
    # ----------------------------------------------------------

    def run(self):
        tokens = [
            token.strip().lower()
            for token in WATCH.split(",")
            if token.strip()
        ]
        numeric = {int(token) for token in tokens if token.isdigit()}
        want_goal = "goal" in tokens

        shown_until = 0

        for episode in range(1, EPISODES + 1):
            draw = episode in numeric
            note = ""

            if want_goal and self.agent.will_reach_goal():
                draw = True
                want_goal = False
                note = "This episode reaches the goal for the first time."

            if draw:
                if episode > shown_until + 1:
                    self.banner(shown_until + 1, episode - 1)

                self.show_episode(episode, note=note)
                shown_until = episode
            else:
                self.agent.episode()

        if shown_until < EPISODES:
            self.banner(shown_until + 1, EPISODES)

        self.finish()
        