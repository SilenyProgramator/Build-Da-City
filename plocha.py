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
HUD_COLOR = (255, 255, 255)  # HUD text color

# Colors for selection
COLOR_OPTIONS = [(255, 127, 127), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow
COLOR_NAMES = ["Marx´s Statue", "Bank", "Sky Scraper", "Farm"]
selected_color_index = 0  # Tracks the selected color in the menu

# Earnings per second
EARNINGS = {
    (0, 255, 0): {"money": 50, "pop": 0, "wheat": 0},  # Green 🟩 → +50 Money
    (0, 0, 255): {"money": 0, "pop": 100, "wheat": 0},  # Blue 🟦 → +100 Population
    (255, 255, 0): {"money": 0, "pop": 0, "wheat": 1}   # Yellow 🟨 → +1 Wheat
}

# Icon setup
icon = pygame.image.load("teplars.jpg") 
pygame.display.set_icon(icon)

# Create screen (Resizable)
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BuildACity")

# Game states
MENU = "menu"
GAME = "game"
COLOR_MENU = "color_menu"
ABSOLUTNIPROHRA = "win"
state = MENU

# Player starting position
tile_x, tile_y = 0, 0
city_name = ""

# Resources
money = 1000  # You can change this to 0 if you want to start with no money
population = 0
wheat = 0
communism = 0  # communism percentage (starts at 0)

# Create a grid where each tile starts as the default color
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

# Timer for resource gain
pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 second interval

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
                pygame.draw.rect(screen, tile_colors[row][col], rect)  # Tile fill
                pygame.draw.rect(screen, GRID_COLOR, rect, 2)  # Grid lines (only borders)
        
        # Draw semi-transparent player
        player_surface = create_transparent_surface(WHITE, CELL_SIZE, PLAYER_ALPHA)
        screen.blit(player_surface, (tile_x * CELL_SIZE, tile_y * CELL_SIZE))
        
        # Display city name & resources
        city_text = font.render(city_name, True, WHITE)
        screen.blit(city_text, (WIDTH - city_text.get_width() - 20, 20))
        
        money_text = font.render(f"Money = {money} $", True, HUD_COLOR)
        pop_text = font.render(f"Population = {population} Mil", True, HUD_COLOR)
        wheat_text = font.render(f"Wheat = {wheat} Tons", True, HUD_COLOR)
        communism_text = font.render(f"Communism: {communism}%", True, HUD_COLOR)

        screen.blit(money_text, (WIDTH - money_text.get_width() - 20, 100))
        screen.blit(pop_text, (WIDTH - pop_text.get_width() - 20, 200))
        screen.blit(wheat_text, (WIDTH - wheat_text.get_width() - 20, 300))
        screen.blit(communism_text, (WIDTH - communism_text.get_width() - 20, 400))

        # Check for win condition
        if communism >= 100:
            state = ABSOLUTNIPROHRA  # Switch to win state
    
    elif state == COLOR_MENU:
        # Show the color selection menu
        screen.fill(BG_COLOR)  # Background color
        menu_title = font2.render("Select a Building", True, WHITE)
        screen.blit(menu_title, (WIDTH // 2 - menu_title.get_width() // 2, HEIGHT // 6))

        spacing = 100  # Increase the spacing between options
        for i, color_name in enumerate(COLOR_NAMES):
            text_color = WHITE if i == selected_color_index else (180, 180, 180)
            option_text = font.render(color_name, True, text_color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 3 + i * spacing))


    elif state == ABSOLUTNIPROHRA:
        # Display "You Win!" message
        win_text = font2.render("Communism has taken over! You were executed :(", True, (0, 255, 0))  # Green text for win
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))

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
                elif event.key == pygame.K_e:
                    state = COLOR_MENU

            elif state == COLOR_MENU:
                if event.key == pygame.K_UP:
                    selected_color_index = (selected_color_index - 1) % len(COLOR_OPTIONS)
                elif event.key == pygame.K_DOWN:
                    selected_color_index = (selected_color_index + 1) % len(COLOR_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if money >= 100:  # Check if you have enough money
                        tile_colors[tile_y][tile_x] = COLOR_OPTIONS[selected_color_index]
                        money -= 100  # Subtract 100 money when you change a tile
                        state = GAME  
                    else:
                        print("Not enough money!")

        elif event.type == pygame.USEREVENT and state == GAME:
            for row in tile_colors:
                for color in row:
                    if color in EARNINGS:
                        money += EARNINGS[color]["money"]
                        population += EARNINGS[color]["pop"]
                        wheat += EARNINGS[color]["wheat"]
                    if color == (255, 127, 127):  # Red 🟥 → Increase communism by 1% per second
                        communism += 1

    # Make sure communism does not exceed 100%
    communism = min(communism, 100)

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
