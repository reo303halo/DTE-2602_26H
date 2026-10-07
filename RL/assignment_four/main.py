import shutil

from q_learning import QLearningAgent
from display import DemoDisplay


def main():
    # ----------------------------------------------------------
    # Check terminal size
    # ---------------------------------------------------------
    cols, rows = shutil.get_terminal_size()
    if cols < 100 or rows < 24:
        print(
            f"Your terminal window is "
            f"{cols}x{rows}; "
            f"this demo needs about 100x24.\n"
        )

        print(
            "Make the window bigger or zoom out, "
            "then press Enter to start "
            "(Ctrl+C quits)."
        )
        input()


    # ----------------------------------------------------------
    # Setting up agent, display and run the program
    # ----------------------------------------------------------
    agent = QLearningAgent()
    display = DemoDisplay(agent)
    display.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
