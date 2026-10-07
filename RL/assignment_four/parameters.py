# ==============================================================
# PARAMETERS TO EXPERIMENT WITH
# ==============================================================

EPISODES = 500

# Which episodes should be shown in detail?
# Examples:
#     "1,2,goal,500"
#     "1,10,100"
WATCH = f"1,2,goal,{EPISODES}"

# Q-learning parameters
ALPHA = 0.1       # learning rate
GAMMA = 0.9       # importance of future rewards
EPSILON = 0.3     # probability of exploring

# Maximum number of steps in one episode
MAXSTEPS = 100

# Seconds between displayed steps
DELAY = 0.3


# Controls the random choices, making experiments
# easier to reproduce.
SEED = 5
