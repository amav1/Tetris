import pygame
import sys
import random
from block import Block, Colors



# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Catching Falling Objects')


# Create grid 
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

#Draw grid
ROWS, COLS = 12, 9
Square = 53
Res = COLS*Square, ROWS * Square


def draw_grid():
    for x in range(0, COLS):
        for y in range(0, ROWS):
            grid = pygame.Rect(x * Square, y * Square, Square, Square)
            pygame.draw.rect(screen, (128, 128, 128), grid, 1)


# Define colors
background_color = (0, 0, 0)  
object_color = (255, 0, 0)        



# Define the falling object and player properties
object_size = 50
object_x = screen_width // 2
object_y = 0
object_speed = 5
is_paused = False



# Game clock

start_time = pygame.time.get_ticks()  
font = pygame.font.SysFont('cambria', 30)



# Main game loop
global grid
locked_positions = {}
grid = create_grid(locked_positions)

running = True
object_block = None  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                object_x -= object_size
            elif event.key == pygame.K_RIGHT:
                object_x += object_size

    # Calculate falling speed
    elapsed_time = pygame.time.get_ticks() - start_time
    elapsed_seconds = elapsed_time / 1000  
    if elapsed_seconds % 50 == 0 and elapsed_seconds != 0:
        object_speed += 1  

    if object_block is None or object_y >= screen_height - object_size:  
        object_block = Block(random.randint(0, screen_width - object_size), 0)  
        object_x = object_block.x * Square
        object_y = object_block.y * Square
    else:
        object_y += object_speed  

    # Boundary checking
    if object_x <= 0:
        object_x = 0
    if object_x >= screen_width - object_size:
        object_x = screen_width - object_size

    # Drawing
    screen.fill(background_color)
    draw_grid()
    pygame.draw.rect(screen, object_block.color, (object_x, object_y, object_size, object_size))  

    timer_text = font.render("Time: " + str(elapsed_seconds), True, (255, 255, 255))
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
