import pygame
from reconstructPath import reconstruct_path

def dfs(draw, grid, start, end):
    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False