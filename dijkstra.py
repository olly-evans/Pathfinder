import heapq
import pygame
from reconstructPath import reconstruct_path

def dijkstra(draw, grid, start, end):
    heap = [(0, start)]
    visited = {start}
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    while heap:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cost, current = heapq.heappop(heap)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            new_cost = current_cost + 1
            if neighbor not in visited or new_cost < g_score[neighbor]:
                g_score[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(heap, (new_cost, neighbor))
                visited.add(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False