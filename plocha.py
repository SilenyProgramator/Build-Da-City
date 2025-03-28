import pygame
import tkinter as tk
from tkinter import simpledialog

# Initialize pygame
pygame.init()

# Constants
ROWS, COLS = 6, 6  # Grid size
BG_COLOR = (153, 0, 0)  # CHERRY background
PLAYER_COLOR = (255, 127, 127)  # Red player
GRID_COLOR = (192, 192, 192)  # Grid lines color
WHITE = (255, 255, 255)
BUTTON_COLOR = (5, 5 , 2)
GOODCOLOR = (0, 66, 37)

# Ideologies
IDEOLOGIES = {
    "communism": ("Communism", (255, 0, 0)),
    "nazism": ("Nazism", (0, 0, 0)),
    "dumbassism": ("Dumbassism", (0, 0, 255)),
    "capitalism": ("Capitalism", (0, 255, 0))
}

# Create screen (Resizable)
WIDTH, HEIGHT = 800, 600  # Increased window size for better visibility
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BuildACity")

# Game states
MENU = "menu"
POLITICAL_SELECTION = "political_selection"
GAME = "game"
state = MENU

# Player starting position
tile_x, tile_y = 0, 0
city_name = ""
city_ideology = ""

# Function to get city name
def get_city_name():
    global city_name
    root = tk.Tk()
    root.withdraw()
    city_name = simpledialog.askstring("City Name", "Enter your city name:")
    if city_name is None:
        city_name = "Unnamed City"

def political_compass():
    global state, city_ideology
    compass_width, compass_height = 600, 600
    compass_surface = pygame.Surface((compass_width, compass_height))  # Create a surface for compass
    compass_rect = pygame.Rect(0, 0, compass_width, compass_height)
    
    marker_x, marker_y = compass_width // 2, compass_height // 2
    marker_radius = 20  # Increased size of the circle
    marker_color = (135, 206, 250)  # Light blue color for the marker
    movement_speed = 20  # Increase speed of movement
    running = True
    
    font = pygame.font.Font(None, 31)  # Increased font size for better visibility
    label_color = WHITE  # Set text color to white for visibility
    
    while running:
        screen.fill(BG_COLOR)  # Clear the screen
        
        # Draw "Choose Ideology" label above the compass
        title_text = font.render("Choose Ideology", True, label_color)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - compass_height // 2 - 30))  # Move lower for better visibility
        
        # Draw "Enter:vyber" label next to the compass
        enter_text = font.render("Enter", True, label_color)
        screen.blit(enter_text, (WIDTH // 2 + compass_width // 2 + 18, HEIGHT // 2 - compass_height // 2))
        
        compass_surface.fill(WHITE)
        
        # Draw quadrants
        pygame.draw.rect(compass_surface, IDEOLOGIES["communism"][1], (0, 0, compass_width // 2, compass_height // 2))
        pygame.draw.rect(compass_surface, IDEOLOGIES["nazism"][1], (compass_width // 2, 0, compass_width // 2, compass_height // 2))
        pygame.draw.rect(compass_surface, IDEOLOGIES["dumbassism"][1], (0, compass_height // 2, compass_width // 2, compass_height // 2))
        pygame.draw.rect(compass_surface, IDEOLOGIES["capitalism"][1], (compass_width // 2, compass_height // 2, compass_width // 2, compass_height // 2))
        
        # Draw labels for each ideology
        for ideology, (name, color) in IDEOLOGIES.items():
            text = font.render(name, True, label_color)
            if ideology == "communism":
                compass_surface.blit(text, (20, 20))
            elif ideology == "nazism":
                compass_surface.blit(text, (compass_width - text.get_width() - 20, 20))
            elif ideology == "dumbassism":
                compass_surface.blit(text, (20, compass_height - text.get_height() - 20))
            elif ideology == "capitalism":
                compass_surface.blit(text, (compass_width - text.get_width() - 20, compass_height - text.get_height() - 20))
        
        # Draw marker (circle)
        pygame.draw.circle(compass_surface, marker_color, (marker_x, marker_y), marker_radius)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and marker_y > marker_radius:
                    marker_y -= movement_speed
                elif event.key == pygame.K_DOWN and marker_y < compass_height - marker_radius:
                    marker_y += movement_speed
                elif event.key == pygame.K_LEFT and marker_x > marker_radius:
                    marker_x -= movement_speed
                elif event.key == pygame.K_RIGHT and marker_x < compass_width - marker_radius:
                    marker_x += movement_speed
                elif event.key == pygame.K_RETURN:
                    if marker_x < compass_width // 2 and marker_y < compass_height // 2:
                        city_ideology = "Communism"
                    elif marker_x >= compass_width // 2 and marker_y < compass_height // 2:
                        city_ideology = "Nazism"
                    elif marker_x < compass_width // 2 and marker_y >= compass_height // 2:
                        city_ideology = "Dumbassism"
                    else:
                        city_ideology = "Capitalism"
                    running = False
        
        # Blit compass surface to the screen
        screen.blit(compass_surface, (WIDTH // 2 - compass_width // 2, HEIGHT // 2 - compass_height // 2))
        pygame.display.flip()

    state = GAME  # Switch state to GAME

# Game loop
running = True
while running:
    WIDTH, HEIGHT = screen.get_size()
    CELL_SIZE = min(WIDTH // COLS, HEIGHT // ROWS)
    FONT_SIZE = CELL_SIZE // 2
    font = pygame.font.Font(None, FONT_SIZE)
    font2 = pygame.font.Font(None, FONT_SIZE + 24)
    
    screen.fill(BG_COLOR)
    
    if state == MENU:
        title_text = font2.render("Create a City", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        
        button_width, button_height = CELL_SIZE * 2, CELL_SIZE // 2
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        
        button_text = font.render("Start", True, WHITE)
        screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) // 2, 
                                  button_rect.y + (button_height - button_text.get_height()) // 2))
    
    elif state == GAME:
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        
        player_rect = pygame.Rect(tile_x * CELL_SIZE, tile_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        
        city_text = font.render(f"{city_name} ({city_ideology})", True, WHITE)
        screen.blit(city_text, (WIDTH - city_text.get_width() - 20, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and state == MENU:
            if button_rect.collidepoint(event.pos):
                get_city_name()
                political_compass()

    pygame.display.flip()

pygame.quit()
