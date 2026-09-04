import heapq
from helpers import reconstruct_path

def dijkstra(graph, start, goal):
    frontier = [(0, start)]
    cost_so_far = {start: 0}
    came_from = {}
    visited = []
    seen = set()

    while frontier:
        cost, node = heapq.heappop(frontier)
        if node not in seen:
            seen.add(node)
            visited.append(node)

        if node == goal:
            break

        for neighbour, weight in graph[node]:
            new_cost = cost_so_far[node] + weight

            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                came_from[neighbour] = node
                heapq.heappush(frontier, (new_cost, neighbour))

    path = reconstruct_path(came_from, start, goal)
    return path, visited
