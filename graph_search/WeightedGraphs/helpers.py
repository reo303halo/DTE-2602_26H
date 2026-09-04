def manhattan_heuristic(goal, min_weight=1):
    """
    Returns a heuristic function h(node) estimating the remaining cost to
    `goal`, using Manhattan distance.

    min_weight should be the cheapest possible cell weight in the grid
    (1 if unweighted). Multiplying by min_weight keeps the heuristic
    admissible when cells have weights greater than 1 - without it, the
    heuristic could overestimate the true remaining cost on expensive
    terrain and A* would no longer be guaranteed optimal.
    """
    goal_r, goal_c = goal

    def h(node):
        r, c = node
        return (abs(r - goal_r) + abs(c - goal_c)) * min_weight

    return h


def reconstruct_path(came_from, start, goal):
    """Walk backwards through came_from to rebuild the path start -> goal."""
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def make_grid_graph(grid, wall):
    """
    Convert a grid (list of lists) into a graph with the same format as
    the weighted graph from class: graph[node] -> [(neighbour, weight), ...]

    grid[row][col] == WALL   ->  wall (not traversable)
    grid[row][col] == w > 0  ->  free cell with movement cost w

    Each node is a (row, col) tuple. Movement is allowed in 4 directions
    (up, down, left, right). The cost of moving into a cell is that
    cell's own weight (i.e. entering an expensive cell costs more,
    regardless of which direction you entered it from).
    """
    rows = len(grid)
    cols = len(grid[0])
    graph = {}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == wall:
                continue  # walls are not nodes

            neighbours = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != wall:
                    neighbours.append(((nr, nc), grid[nr][nc]))

            graph[(r, c)] = neighbours

    return graph