# A_Star_Pathfinding.py
import pygame
import sys

# CONSTANTS
HEIGHT = 800
WIDTH = 800
COLS = 25
ROWS = 25
BOX_WIDTH = WIDTH // COLS
BOX_HEIGHT = HEIGHT // ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
grid = []


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False
        self.start = False
        self.end = False
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH - 2, BOX_HEIGHT - 2))


# Creating Grid
for i in range(COLS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    grid.append(arr)

grid[0][0].start = True



def main():
    # Standard pygame event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                # LEFT CLICK
                if event.buttons[0]:
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    grid[i][j].wall = True

                # RIGHT CLICK
                if event.buttons[2]:
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    grid[i][j].end = True

        
        WINDOW.fill((0,0,0))

        #Fills the black screen with white boxes
        for i in range(COLS):
            for j in range(ROWS):
                current_box = grid[i][j]
                current_box.draw(WINDOW, WHITE)
                
                
                if current_box.wall:                        # If the current box is a barrier
                    current_box.draw(WINDOW, BLACK)
                elif current_box.end:                       # If the current box is the target
                    current_box.draw(WINDOW, END_COLOR)
                elif current_box.start:                     # If the current box is the starting position
                    current_box.draw(WINDOW, START_COLOR)

        pygame.display.flip()
main()