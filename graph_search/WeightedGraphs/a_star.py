import heapq
from helpers import reconstruct_path

def a_star(graph, start, goal, h):
    """
    A* search. Same signature and return type as dijkstra(), so the two
    can be swapped for each other directly.

    visited is returned as a list, in the order nodes were expanded (not
    a set), so the visualization can show a "wavefront" of the search.
    """
    frontier = [(h(start), start)]
    g_score = {start: 0}
    came_from = {}
    visited = []
    seen = set()

    while frontier:
        _, node = heapq.heappop(frontier)
        if node not in seen:
            seen.add(node)
            visited.append(node)

        if node == goal:
            break

        for neighbour, weight in graph[node]:
            tentative_g = g_score[node] + weight

            if neighbour not in g_score or tentative_g < g_score[neighbour]:
                g_score[neighbour] = tentative_g
                came_from[neighbour] = node
                f_score = tentative_g + h(neighbour)
                heapq.heappush(frontier, (f_score, neighbour))

    path = reconstruct_path(came_from, start, goal)

    return path, visited