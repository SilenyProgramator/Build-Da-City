import pygame
import tkinter as tk
from tkinter import simpledialog

# Initialize pygame
pygame.init()

# Constants
ROWS, COLS = 6, 6  # Grid size
BG_COLOR = (153, 0, 0)  # Background
GRID_COLOR = (192, 192, 192)  # Grid lines
WHITE = (255, 255, 255)
BUTTON_COLOR = (5, 5, 2)
PLAYER_ALPHA = 150  # Transparency level (0 = fully transparent, 255 = solid)

# Colors for selection
COLOR_OPTIONS = [(255, 127, 127), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
COLOR_NAMES = ["Red", "Green", "Blue", "Yellow"]
selected_color_index = 0  # Tracks the selected color in the menu

# Icon setup
icon = pygame.image.load("teplars.jpg") 
pygame.display.set_icon(icon)

# Create screen (Resizable)
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BuildACity")

# Game states
MENU = "menu"
GAME = "game"
COLOR_MENU = "color_menu"
state = MENU

# Player starting position
tile_x, tile_y = 0, 0
city_name = ""

# Create a grid where each tile starts as the default grid color
DEFAULT_TILE_COLOR = (220, 220, 220)  # Light gray for uncolored tiles
tile_colors = [[DEFAULT_TILE_COLOR for _ in range(COLS)] for _ in range(ROWS)]


# Function to get city name
def get_city_name():
    global city_name
    root = tk.Tk()
    root.withdraw()  # Hide main window
    city_name = simpledialog.askstring("City Name", "Enter your city name:")
    if city_name is None:
        city_name = "Unnamed City"

# Create a semi-transparent player surface
def create_transparent_surface(color, size, alpha):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill((*color, alpha))  # Add transparency
    return surface

# Game loop
running = True
while running:
    WIDTH, HEIGHT = screen.get_size()  # Update dimensions if resized
    CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)  # Scale cells proportionally
    FONT_SIZE = CELL_SIZE // 2  # Adjust font size
    font = pygame.font.Font(None, FONT_SIZE)
    font2 = pygame.font.Font(None, FONT_SIZE + 24)

    screen.fill(BG_COLOR)
    
    if state == MENU:
        # Draw menu screen
        title_text = font2.render("Create a City", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        # Scale button
        button_width, button_height = CELL_SIZE * 2, CELL_SIZE // 2
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        
        button_text = font.render("Start", True, WHITE)
        screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) // 2, 
                                  button_rect.y + (button_height - button_text.get_height()) // 2))
    
    elif state == GAME:
        # Draw grid with tile colors
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, tile_colors[row][col], rect)  # Use stored color
                pygame.draw.rect(screen, GRID_COLOR, rect, 2)  # Draw grid lines (thicker for visibility)
        
        # Draw semi-transparent player
        player_surface = create_transparent_surface(WHITE, CELL_SIZE, PLAYER_ALPHA)
        screen.blit(player_surface, (tile_x * CELL_SIZE, tile_y * CELL_SIZE))
        
        # Display city name
        city_text = font.render(city_name, True, WHITE)
        screen.blit(city_text, (WIDTH - city_text.get_width() - 20, 20))

    elif state == COLOR_MENU:
        # Show the color selection menu
        screen.fill(BG_COLOR)  # Background color
        menu_title = font2.render("Select a Tile Color", True, WHITE)
        screen.blit(menu_title, (WIDTH // 2 - menu_title.get_width() // 2, HEIGHT // 6))

        for i, color_name in enumerate(COLOR_NAMES):
            text_color = WHITE if i == selected_color_index else (180, 180, 180)
            option_text = font.render(color_name, True, text_color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 3 + i * 40))

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
        elif event.type == pygame.KEYDOWN:
            if state == GAME:
                if event.key == pygame.K_UP and tile_y > 0:
                    tile_y -= 1
                elif event.key == pygame.K_DOWN and tile_y < ROWS - 1:
                    tile_y += 1
                elif event.key == pygame.K_LEFT and tile_x > 0:
                    tile_x -= 1
                elif event.key == pygame.K_RIGHT and tile_x < COLS - 1:
                    tile_x += 1
                elif event.key == pygame.K_e:  # Open color selection for the current tile
                    state = COLOR_MENU

            elif state == COLOR_MENU:
                if event.key == pygame.K_UP:
                    selected_color_index = (selected_color_index - 1) % len(COLOR_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    selected_color_index = (selected_color_index + 1) % len(COLOR_OPTIONS)
                elif event.key == pygame.K_RETURN:  # Confirm selection
                    tile_colors[tile_y][tile_x] = COLOR_OPTIONS[selected_color_index]
                    state = GAME  # Return to the game

    pygame.display.flip()
    pygame.time.delay(100)  # Small delay to control movement speed

pygame.quit()
