# A_Star_Pathfinding.py
import pygame
import sys
from queue import PriorityQueue

# CONSTANTS
HEIGHT = 800
WIDTH = 800
COLS = 25
ROWS = 25
BOX_WIDTH = WIDTH // COLS
BOX_HEIGHT = HEIGHT // ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (116, 1, 113)
ORANGE = (255, 103, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
START_COLOR = ORANGE
END_COLOR = RED


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
grid = []


class Box:
    def __init__(self, x, y):
        self.row = x
        self.col = y
        self.color = WHITE
        self.neighbors = []

# Setters
    def make_start(self):
        self.color = START_COLOR
    
    def make_end(self):
        self.color = END_COLOR

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = PURPLE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN

    def get_pos(self):
        return (self.col, self.row)

    def update_neighbors(self, grid):
        self.neighbors = []

        if (self.row > 0 and not grid[self.col][self.row - 1].is_barrier()):                    # Up 
            self.neighbors.append(grid[self.col][self.row - 1])
        if (self.row < ROWS - 1 and not grid[self.col][self.row + 1].is_barrier()):             # Down 
            self.neighbors.append(grid[self.col][self.row + 1])
        if (self.col > 0 and not grid[self.col - 1][self.row].is_barrier()):                    # Left
            self.neighbors.append(grid[self.col - 1][self.row])
        if (self.col < COLS - 1 and not grid[self.col + 1][self.row].is_barrier()):             # Right
            self.neighbors.append(grid[self.col + 1][self.row])

    def is_barrier(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == GREEN
    
    def is_closed(self):
        return self.color == RED
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.row * BOX_WIDTH, self.col * BOX_HEIGHT, BOX_WIDTH - 2, BOX_HEIGHT - 2))


def draw_boxes(grid):
    WINDOW.fill(BLACK)

    for i in range(COLS):
        for j in range(ROWS):
            current_box = grid[i][j]
            current_box.draw(WINDOW, current_box.color)
    pygame.display.update()

# Creating Grid
for i in range(COLS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    grid.append(arr)
grid[1][1].color = START_COLOR


#   draw_boxes: function callback    grid: List[List]    start: class Box()    end: class Box()

"""
PriorityQueue() METHODS:
    put() – Puts an item into the queue.
    get() – Removes and returns an item from the queue.
    qsize() – Returns the current queue size.
    empty() – Returns True if the queue is empty, False otherwise. It is equivalent to qsize()==0.
    full() – Returns True if the queue is full, False otherwise.

PSEUDOCODE
function A_Star(start, goal)

    openSet := {start} (PRIORITY QUEUE)
    cameFrom := an empty map
    gScore := map with default value of Infinity
    gScore[start] := 0
    fScore := map with default value of Infinity
    fScore[start] := h(start, end)

    while openSet is not empty
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)

        openSet.Remove(current)
        for each neighbor of current
            tentative_gScore := gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := tentative_gScore + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)

"""
def HEURISTIC( p1, p2 ):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) - abs(y2 - y1)


def ALGORITHM(draw_boxes, grid, start, end):
    openSet = PriorityQueue()
    openSet.put((0, start)) # 0 is the starting f score and start is the position of starting node
    cameFrom = {}
    # default each gScore[spot] = infinity and start node is 0
    gScore = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = HEURISTIC(start.get_pos(), end.get_pos())



def main():
    # Standard pygame event loop
    started = False
    start = grid[1][1]
    end = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                # LEFT CLICK -- setting barriers
                if event.buttons[0] :
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    if grid[i][j].color != START_COLOR:
                        grid[i][j].color = BLACK

                # RIGHT CLICK -- setting end position
                if event.buttons[2]:
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    if grid[i][j].color != START_COLOR:
                        grid[i][j].color = END_COLOR
                        end = grid[i][j]

            draw_boxes(grid)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and end != None:
                    
                    for i in grid:
                        for spot in i:
                            spot.update_neighbors(grid)

                    ALGORITHM(lambda: draw_boxes(grid),  grid, start, end)
                    
                
        pygame.display.flip()
main()