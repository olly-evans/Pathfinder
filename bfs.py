from collections import deque
import pygame
from reconstructPath import reconstruct_path


def bfs(draw, grid, start, end):
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False