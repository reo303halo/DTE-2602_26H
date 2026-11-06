"""
Perceptron with three features: apples vs oranges in 3D
=======================================================
Intro to ML & AI — the 3D picture from the slide "More features: w1, w2, w3, ...".

Run it from a terminal:
    python perceptron_3d.py

A window opens. Drag with the mouse to rotate the picture.
Keys:
    p   show / hide the plane (the decision boundary)
    r   start / stop automatic rotation
    q   close the window

In Jupyter, put  %matplotlib qt  (or  %matplotlib widget  with ipympl installed)
in a cell before running the code, so the plot opens in a window you can rotate.
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------- the data (same as on the slide)
rng = np.random.default_rng(5)
apples = np.column_stack([rng.normal(155, 14, 40),                    # weight (g)
                          rng.normal(11.0, 0.9, 40),                  # sweetness
                          np.clip(rng.normal(0.30, 0.15, 40), 0, 1)]) # colour: 0 = green, 1 = orange
oranges = np.column_stack([rng.normal(205, 16, 40),
                           rng.normal(8.2, 0.9, 40),
                           np.clip(rng.normal(0.85, 0.08, 40), 0, 1)])
X = np.vstack([apples, oranges])
y = np.array([0] * 40 + [1] * 40)                                    # 0 = apple, 1 = orange

# ---------------------------------------------------------------- train a perceptron (scaled features)
scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)

w = np.zeros(3)
b = 0.0
order_rng = np.random.default_rng(0)
for epoch in range(50):
    mistakes = 0
    for i in order_rng.permutation(len(Xs)):
        y_hat = 1 if Xs[i] @ w + b > 0 else 0
        if y_hat != y[i]:
            w = w + (y[i] - y_hat) * Xs[i]
            b = b + (y[i] - y_hat)
            mistakes += 1
    if mistakes == 0:
        break

print(f"Trained in {epoch + 1} epochs")
print(f"w = {np.round(w, 2)}  (weight, sweetness, colour),  b = {b}")

# ---------------------------------------------------------------- the plane where z = 0
# Solve w1*x1 + w2*x2 + w3*x3 + b = 0 for x3 (colour) on a grid, in scaled units,
# then convert back to the original units so the axes show grams, sweetness and colour.
g1, g2 = np.meshgrid(np.linspace(-2, 2, 20), np.linspace(-2, 2, 20))
g3 = -(w[0] * g1 + w[1] * g2 + b) / w[2]
plane = scaler.inverse_transform(np.column_stack([g1.ravel(), g2.ravel(), g3.ravel()]))
PX, PY, PZ = (plane[:, k].reshape(g1.shape) for k in range(3))
PZ = np.where((PZ > -0.15) & (PZ < 1.15), PZ, np.nan)                 # cut the plane to the box

# ---------------------------------------------------------------- draw
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(projection="3d")

surface = [ax.plot_surface(PX, PY, PZ, color="#7D5BA6", alpha=0.25, edgecolor="#7D5BA6", linewidth=0.3)]
ax.scatter(*apples.T, c="#FF6B4A", s=40, edgecolors="white", linewidths=0.5, depthshade=False, label="apple (0)")
ax.scatter(*oranges.T, c="#F3A712", s=40, edgecolors="white", linewidths=0.5, depthshade=False, label="orange (1)")

ax.set_xlabel("weight (g)")
ax.set_ylabel("sweetness")
ax.set_zlabel("colour (green → orange)")
ax.set_zlim(-0.1, 1.1)
ax.view_init(elev=8, azim=-28)
ax.legend(loc="upper left")
ax.set_title("Perceptron with 3 features: the boundary is a flat plane\n"
             "drag to rotate · p: plane on/off · r: auto-rotate · q: quit", fontsize=10)

# ---------------------------------------------------------------- keys: plane on/off, auto-rotate
state = {"rotating": False}
timer = fig.canvas.new_timer(interval=40)

def rotate_step():
    ax.view_init(elev=ax.elev, azim=ax.azim + 1)
    fig.canvas.draw_idle()

timer.add_callback(rotate_step)

def on_key(event):
    if event.key == "p":
        surface[0].set_visible(not surface[0].get_visible())
        fig.canvas.draw_idle()
    elif event.key == "r":
        state["rotating"] = not state["rotating"]
        timer.start() if state["rotating"] else timer.stop()

fig.canvas.mpl_connect("key_press_event", on_key)
plt.show()