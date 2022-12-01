# A_Star_Pathfinding.py
import pygame
import sys
import time
from math import sqrt
from queue import PriorityQueue

# CONSTANTS
HEIGHT = 800
WIDTH = 800
COLS = 25
ROWS = 25
BOX_WIDTH = WIDTH // COLS
BOX_HEIGHT = HEIGHT // ROWS

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
START_COLOR = BLUE
END_COLOR = GREEN


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
        self.color = CYAN

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = MAGENTA

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN

    def get_pos(self):
        return (self.col, self.row)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
                                                                                            

    def is_barrier(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == GREEN
    
    def is_closed(self):
        return self.color == RED
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.row * BOX_WIDTH, self.col * BOX_HEIGHT, BOX_WIDTH - 2, BOX_HEIGHT - 2))


class Button:
    def __init__(self, text, x, y, width, height, font_size, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font_size
        self.color = color
        self.draw_box()

    def draw_box(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("microsofthimalaya", self.font)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, self.y + self.height / 2))
        WINDOW.blit(text, text_rect)
        pygame.display.update()


def draw_boxes(grid):
    WINDOW.fill(BLACK)

    for i in range(COLS):
        for j in range(ROWS):
            current_box = grid[i][j]
            current_box.draw(WINDOW, current_box.color)
    pygame.display.update()


def draw_menu():
    pygame.font.init()
    WINDOW.fill(WHITE)
    font = pygame.font.SysFont("microsofthimalaya", 60)
    text = font.render("Welcome to the pathfinding visualizer!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH/2, 100))
    WINDOW.blit(text, text_rect)

# Creating Grid
for i in range(COLS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    grid.append(arr)
grid[1][1].color = START_COLOR


def HEURISTIC( p1, p2 ):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt( (x1 - x2)**2 + (y1 - y2)**2 )


def reconstruct_path(grid, came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()


"""
PSEUDOCODE

function reconstruct_path(cameFrom, current)
    total_path := {current}
    while current in cameFrom.Keys:
        current := cameFrom[current]
        total_path.prepend(current)
    return total_path

function A_Star(start, goal, h)

    openSet := {start} //PriorityHeap
    cameFrom := an empty map
    gScore := map with default value of Infinity
    gScore[start] := 0
    fScore := map with default value of Infinity
    fScore[start] := h(start)

    while openSet is not empty
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)

        openSet.Remove(current)
        for each neighbor of current
            tentative_gScore := gScore[current] + d(current, neighbor) heuristic distance formula between the neighbors
            if tentative_gScore < gScore[neighbor]
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := tentative_gScore + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)

    return failure
"""

def A_STAR(draw_boxes, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # f score, current_node
    cameFrom = {}
    gScore = {spot:float('inf') for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot:float('inf') for row in grid for spot in row}
    fScore[start] = HEURISTIC(start.get_pos(), end.get_pos())
    open_set_map = {start}

    while not open_set.empty():
        curr = open_set.get()[2]
        if curr == end:
            end.make_end()
            reconstruct_path(grid, cameFrom, curr)
            return True

        open_set_map.remove(curr)
        for neighbor in curr.neighbors:
            temp_g_score = gScore[curr] + HEURISTIC(curr.get_pos(), neighbor.get_pos())
            if temp_g_score < gScore[neighbor]:
                cameFrom[neighbor] = curr
                gScore[neighbor] = temp_g_score
                fScore[neighbor] = temp_g_score + HEURISTIC(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_map:
                    count += 1
                    open_set.put((fScore[neighbor], count, neighbor))
                    open_set_map.add(neighbor)
                    neighbor.make_open()

        draw_boxes()
        if curr != start:
            curr.make_closed()

    return False


def DIJKSTRA(draw_boxes, grid, start, end):
    print("CODE HERE")
    return


def BFS(draw_boxes, grid, start, end):
    print("CODE HERE")
    return
    


def main():
    # Standard pygame event loop
    algorithm = ""
    inMenu = True
    started = False
    start = grid[1][1]
    end = None
    end_exists = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if inMenu:
                draw_menu()
                a_star_button = Button("A*", WIDTH / 2 - 100, 300, 200, 50, 40, "navy")
                dijkstra_button = Button("Dijkstra", WIDTH / 2 - 100, 400, 200, 50, 40, "navy")
                BFS_button = Button("BFS", WIDTH / 2 - 100, 500, 200, 50, 40, "navy")


                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    if x >= WIDTH / 2 - 100 and x <= (WIDTH / 2 - 100) + 200 and y >= 300 and y <= 350:
                        inMenu = False
                        algorithm = "A*"

                    if x >= WIDTH / 2 - 100 and x <= (WIDTH / 2 - 100) + 200 and y >= 400 and y <= 450:
                        inMenu = False
                        algorithm = "Dijkstra"

                    if x >= WIDTH / 2 - 100 and x <= (WIDTH / 2 - 100) + 200 and y >= 500 and y <= 550:
                        inMenu = False
                        algorithm = "BFS"


            else:
                if event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    
                    # LEFT CLICK -- setting barriers
                    if event.buttons[0]:
                        i = x // BOX_WIDTH
                        j = y // BOX_HEIGHT
                        if grid[i][j].color != START_COLOR and grid[i][j].color != END_COLOR:
                            grid[i][j].color = BLACK

                    # RIGHT CLICK -- setting end position
                    if event.buttons[2]:
                        i = x // BOX_WIDTH
                        j = y // BOX_HEIGHT
                        if grid[i][j].color != START_COLOR and grid[i][j].color != END_COLOR:
                            grid[i][j].color = END_COLOR
                            end = grid[i][j]
                            end_exists = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        i = x // BOX_WIDTH
                        j = y // BOX_HEIGHT
                        if grid[i][j].color != START_COLOR and grid[i][j].color != END_COLOR and not end_exists:
                            grid[i][j].color = END_COLOR
                            end = grid[i][j]
                            end_exists = True


                draw_boxes(grid)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not started and end != None:
                        
                        for i in grid:
                            for spot in i:
                                spot.update_neighbors(grid)

                        if algorithm == "A*":
                            A_STAR(lambda: draw_boxes(grid),  grid, start, end)
                        elif algorithm == "Dijkstra":
                            DIJKSTRA(lambda: draw_boxes(grid),  grid, start, end)
                        elif algorithm == "BFS":
                            BFS(lambda: draw_boxes(grid),  grid, start, end)
  
        pygame.display.flip()
main()