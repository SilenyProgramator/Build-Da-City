import pygame
import tkinter as tk
from tkinter import simpledialog

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400  # Increased screen size
ROWS, COLS = 8, 8  # Grid size
CELL_SIZE = 40  # Increased square size
BG_COLOR = (34, 177, 76)  # Green background
PLAYER_COLOR = (200, 0, 0)  # Red player (Change this to modify the player color)
GRID_COLOR = (0, 100, 0)  # Grid lines color
WHITE = (255, 255, 255)
BUTTON_COLOR = (5, 5 , 2)
GOODCOLOR = (0, 66, 37)

# Create screen (Resizable)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Grid Movement")

# Game states
MENU = "menu"
GAME = "game"
state = MENU

# Player starting position
tile_x, tile_y = 0, 0
city_name = ""

# Fonts
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 60)

# Button setup
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)

# Function to get city name
def get_city_name():
    global city_name
    root = tk.Tk()
    root.withdraw()  # Hide main window
    city_name = simpledialog.askstring("City Name", "Enter your city name:")
    if city_name is None:
        city_name = "Unnamed City"

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    WIDTH, HEIGHT = screen.get_size()  # Update dimensions if resized
    
    if state == MENU:
        # Draw menu screen
        title_text = font2.render("Create a City", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - 140, 70))
        
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        button_text = font.render("Start", True, WHITE)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))
    
    elif state == GAME:
        # Draw grid
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        
        # Draw player
        player_rect = pygame.Rect(tile_x * CELL_SIZE, tile_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        
        # Display city name
        city_text = font.render(city_name, True, GOODCOLOR)
        screen.blit(city_text, (WIDTH - 200, 50))
    
    
    
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and state == MENU:
            if button_rect.collidepoint(event.pos):
                get_city_name()
                state = GAME
        elif event.type == pygame.KEYDOWN and state == GAME:
            if event.key == pygame.K_UP and tile_y > 0:
                tile_y -= 1
            elif event.key == pygame.K_DOWN and tile_y < ROWS - 1:
                tile_y += 1
            elif event.key == pygame.K_LEFT and tile_x > 0:
                tile_x -= 1
            elif event.key == pygame.K_RIGHT and tile_x < COLS - 1:
                tile_x += 1
    
    pygame.display.flip()
    pygame.time.delay(100)  # Small delay to control movement speed

pygame.quit()
