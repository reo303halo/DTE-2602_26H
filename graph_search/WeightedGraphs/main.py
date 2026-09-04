import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from helpers import manhattan_heuristic, make_grid_graph
from dijkstra import dijkstra
from a_star import a_star


# Use this value in a grid to mark a cell as a wall (not traversable).
# Any other value is treated as the cost of moving INTO that cell.
WALL = -1


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def _draw_grid(ax, grid, path = None, visited = None, start = None, goal = None, show_weights = False):
    """
    Draws one grid (walls, weight shading if enabled, visited gradient,
    path outline, start/goal) onto a given matplotlib axis. Shared by
    visualize_grid() (one grid) and visualize_comparison() (several
    grids side by side), so both stay visually consistent.

    Returns (min_weight, max_weight, cmap) if show_weights is True, so
    the caller can draw a matching colorbar - otherwise returns None.
    """
    rows = len(grid)
    cols = len(grid[0])

    weight_info = None
    if show_weights:
        weights = [grid[r][c] for r in range(rows) for c in range(cols) if grid[r][c] != WALL]
        min_w, max_w = (min(weights), max(weights)) if weights else (1, 1)
        weight_cmap = plt.get_cmap("YlOrRd")
        weight_info = (min_w, max_w, weight_cmap)

    # Grid cells: plain white/black, or shaded by weight if enabled
    for r in range(rows):
        for c in range(cols):
            value = grid[r][c]

            if value == WALL:
                color = "black"
            elif show_weights:
                min_w, max_w, weight_cmap = weight_info
                norm = 0.0 if max_w == min_w else (value - min_w) / (max_w - min_w)
                color = weight_cmap(0.15 + 0.55 * norm)
            else:
                color = "white"

            ax.add_patch(patches.Rectangle(
                (c, rows - r - 1), 1, 1,
                facecolor=color, edgecolor="gray"
            ))

            if show_weights and value != WALL:
                ax.text(c + 0.5, rows - r - 1 + 0.5, 
                        str(value), ha = "center", va = "center", fontsize = 8, color = "black")

    # Visited nodes as a gradient showing the order they were expanded in
    # (light = expanded early, dark = expanded late) - a "wavefront" you
    # can read the search's progress from, and compare between algorithms.
    if visited:
        visited_seq = list(visited)
        n = len(visited_seq)
        visited_cmap = plt.get_cmap("Blues")
        for i, (r, c) in enumerate(visited_seq):
            norm = i / max(n - 1, 1)
            color = visited_cmap(0.15 + 0.8 * norm)
            ax.add_patch(patches.Rectangle(
                (c, rows - r - 1), 1, 1,
                facecolor = color, alpha = 0.75, edgecolor = "none"
            ))

    # Path as an outline, so it never hides what's underneath
    if path:
        for (r, c) in path:
            ax.add_patch(patches.Rectangle(
                (c, rows - r - 1), 1, 1,
                facecolor = "none", edgecolor = "gold", linewidth = 3
            ))

    # Start and goal as circles rather than full-cell fills
    if start:
        r, c = start
        ax.add_patch(patches.Circle(
            (c + 0.5, rows - r - 1 + 0.5), 0.3,
            facecolor = "green", edgecolor = "black", zorder = 5
        ))
    if goal:
        r, c = goal
        ax.add_patch(patches.Circle(
            (c + 0.5, rows - r - 1 + 0.5), 0.3,
            facecolor = "red", edgecolor = "black", zorder = 5
        ))

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    return weight_info


def _legend_handles():
    return [
        patches.Patch(facecolor = "black", label = "Wall"),
        patches.Patch(facecolor = "steelblue", alpha = 0.6, label = "Visited (darker = later)"),
        patches.Patch(facecolor = "none", edgecolor = "gold", linewidth = 2, label = "Path"),
        patches.Patch(facecolor = "green", label = "Start"),
        patches.Patch(facecolor = "red", label = "Goal"),
    ]


def visualize_grid(grid, path = None, visited = None, start = None, goal = None,
                    title = "Search on a grid", show_weights = False):
    """
    Simple visualization of a single grid: the path found by a search
    algorithm, and (optionally) which nodes were expanded during the
    search, shown as a light-to-dark gradient in the order they were
    visited.

    grid:    2D list, WALL = wall, any other value = cell weight (cost)
    path:    list of (row, col) tuples, in order from start to goal
    visited: sequence of (row, col) tuples, in the order they were
             expanded during search (as returned by dijkstra()/a_star())
    start:   (row, col) tuple
    goal:    (row, col) tuple
    show_weights: if True, shade cells by weight and print the weight in
                  each cell. Off by default, so the focus stays on
                  comparing *how the algorithms search*, not on terrain
                  cost - turn it on if you want to see both at once.
    """
    rows = len(grid)
    cols = len(grid[0])

    fig, ax = plt.subplots(figsize = (cols / 2, rows / 2))
    weight_info = _draw_grid(ax, grid, path, visited, start, goal, show_weights)
    ax.set_title(title)

    if show_weights and weight_info:
        min_w, max_w, weight_cmap = weight_info
        sm = cm.ScalarMappable(cmap = weight_cmap, norm = mcolors.Normalize(vmin = min_w, vmax = max_w))
        sm.set_array([])
        fig.colorbar(sm, ax = ax, label = "Cell weight (movement cost)", fraction = 0.046, pad = 0.04)

    ax.legend(handles = _legend_handles(), loc = "upper center",
              bbox_to_anchor = (0.5, -0.05), ncol = 5, fontsize = 8, frameon = False)

    plt.show()


def visualize_comparison(grid, start, goal, results, show_weights = False):
    """
    Side-by-side comparison of several search runs on the SAME grid.

    results: list of (label, path, visited) tuples, e.g.

        visualize_comparison(grid, start, goal, [
            ("Dijkstra", dijkstra_path, dijkstra_visited),
            ("A*",       astar_path,    astar_visited),
        ])

    Each panel gets its own title showing the label, path cost, and
    number of nodes visited, so the numbers and the picture back each
    other up.
    """
    n = len(results)
    rows = len(grid)
    cols = len(grid[0])

    fig, axes = plt.subplots(1, n, figsize = (cols / 2 * n, rows / 2 + 1))
    if n == 1:
        axes = [axes]

    for ax, (label, path, visited) in zip(axes, results):
        _draw_grid(ax, grid, path, visited, start, goal, show_weights)

        cost = sum(grid[r][c] for (r, c) in path[1:]) if path else None
        n_visited = len(visited) if visited else 0
        subtitle = label
        if cost is not None:
            subtitle += f"\ncost = {cost}, visited = {n_visited}"
        ax.set_title(subtitle)

    fig.legend(handles = _legend_handles(), loc = "lower center",
               ncol = 5, fontsize = 8, frameon = False)
    plt.tight_layout(rect = (0, 0.05, 1, 1))
    plt.show()



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    W = WALL
    rows, cols = 16, 16

    # Open grid (uniform weight 1 everywhere)...
    example_grid = [[1 for _ in range(cols)] for _ in range(rows)]

    example_grid[5] = [W] * cols
    example_grid[5][3] = 1

    example_grid[11] = [W] * cols
    example_grid[11][12] = 1

    start = (0, 0)
    goal = (15, 15)

    graph = make_grid_graph(example_grid, W)
    h = manhattan_heuristic(goal)

    dijkstra_path, dijkstra_visited = dijkstra(graph, start, goal)
    astar_path, astar_visited = a_star(graph, start, goal, h)

    # Side by side, so the difference between the two is easy to see
    results = [
        ("Dijkstra", dijkstra_path, dijkstra_visited),
        ("A*", astar_path, astar_visited),
    ]

    visualize_comparison(example_grid, start, goal, results)
    