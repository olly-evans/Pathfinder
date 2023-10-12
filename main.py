import pygame
from reconstructPath import reconstruct_path

# Algorithms
from algorithms import dijkstra, bfs, dfs, astar

# Initialise font
pygame.font.init()

# Setup display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finder")

# Background color and global font
BACKGROUND_COLOR = (220, 200, 255)
GLOBAL_FONT = pygame.font.Font("NextBro.ttf", 36) 

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == BLUE
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = GLOBAL_FONT
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

def is_over_button(pos, button):
    if pos[0] > button.x and pos[0] < button.x + button.width:
        if pos[1] > button.y and pos[1] < button.y + button.height:
            return True
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# Function to display the main menu
def main_menu(win, width):
    buttons = [Button(WIDTH // 2 - 100, 250, 200, 50, "Dijkstra", (255, 255, 255)),
               Button(WIDTH // 2 - 100, 320, 200, 50, "BFS", (255, 255, 255)),
               Button(WIDTH // 2 - 100, 390, 200, 50, "DFS", (255, 255, 255)),
               Button(WIDTH // 2 - 100, 460, 200, 50, "A*", (255, 255, 255)),
               Button(WIDTH // 2 - 100, 530, 200, 50, "Quit", (255, 255, 255))]

    text = GLOBAL_FONT.render("WHICH ALGORITHM?", 1, (0, 0, 0))
    text_pos = (WIDTH // 2 - text.get_width() // 2, 150)

    while True:
        win.fill(BACKGROUND_COLOR)

        
        win.blit(text, text_pos)  

        for button in buttons:
            button.draw(win, (0, 0, 0))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for button in buttons:
                    if is_over_button(pos, button):
                        return button.text

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    selected_algorithm = None

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Show the main menu
        selected_algorithm = main_menu(win, width)  

        if selected_algorithm == "Quit":
            break

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Left mouse button
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()
                # Right mouse button
                elif pygame.mouse.get_pressed()[2]:  
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)

                        if selected_algorithm == "Dijkstra":
                            dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        elif selected_algorithm == "BFS":
                            bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        elif selected_algorithm == "DFS":
                            dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        elif selected_algorithm == "A*":
                            astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if event.key == pygame.K_r:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)

            draw(win, grid, ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)