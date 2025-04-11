import pygame
import tkinter as tk
from tkinter import simpledialog

# Minihra funkce
def hra():
    # Vytvoření samostatného okna pro minihru bez zavření hlavní hry
    okno = pygame.display.set_mode((600, 600), pygame.SHOWN)
    pygame.display.set_caption("Minihra: Poraz kapitalismus")

    zapadni = (0,131,109)
    ruda = (190,25,24)
    zelena = (100, 230, 90)
    bila = (255, 255, 255)
    rychlost_x = 10
    rychlost_y = 10

    class Plosina:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 100, 15)

        def pohyb(self, x):
            self.rect.x += x
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > 600:
                self.rect.right = 600

    class Mic:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 15, 15)
            self.rychlost_x = rychlost_x
            self.rychlost_y = rychlost_y

        def pohyb(self):
            self.rect.x += self.rychlost_x
            self.rect.y += self.rychlost_y
            if self.rect.left <= 0 or self.rect.right >= 600:
                self.rychlost_x = -self.rychlost_x
            if self.rect.top <= 0:
                self.rychlost_y = -self.rychlost_y

        def reset(self):
            self.rect.x = 300 - 7
            self.rect.y = 300 - 7
            self.rychlost_x = rychlost_x
            self.rychlost_y = rychlost_y

    class Kostka:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 60, 20)

    plosina = Plosina(300 - 50, 600 - 40)
    mic = Mic(300 - 7, 300 - 7)
    kostky = [Kostka((i * 74) + 10, (j * 29) + 10) for i in range(8) for j in range(4)]

    hra_bezi = True
    plosina_x = 0

    while hra_bezi:
        pygame.time.delay(30)
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                hra_bezi = False

        klik = pygame.key.get_pressed()
        if klik[pygame.K_LEFT]:
            plosina_x = -rychlost_x
        elif klik[pygame.K_RIGHT]:
            plosina_x = rychlost_x
        else:
            plosina_x = 0

        plosina.pohyb(plosina_x)
        mic.pohyb()

        if mic.rect.colliderect(plosina.rect):
            mic.rychlost_y = -mic.rychlost_y

        for kostka in kostky[:]:
            if mic.rect.colliderect(kostka.rect):
                mic.rychlost_y = -mic.rychlost_y
                kostky.remove(kostka)

        if mic.rect.bottom >= 600:
            mic.reset()
            kostky = [Kostka((i * 74) + 10, (j * 29) + 10) for i in range(1) for j in range(1)]

        okno.fill(bila)
        pygame.draw.rect(okno, ruda, plosina.rect)
        pygame.draw.circle(okno, zapadni, mic.rect.center, 10)
        for kostka in kostky:
            pygame.draw.rect(okno, zelena, kostka.rect)

        if not kostky:
            font = pygame.font.SysFont(None, 50)
            text = font.render("Porazil si kapitalismus!", True, ruda)
            okno.blit(text, (300 - text.get_width() // 2, 300 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            hra_bezi = False

        pygame.display.flip()

    # NEVOLÁME pygame.quit() ANI pygame.display.quit()!


# -------------------- HLAVNÍ HRA ------------------------

# Initialize pygame
pygame.init()

# Constants
ROWS, COLS = 6, 6
BG_COLOR = (153, 0, 0)
PLAYER_COLOR = (255, 127, 127)
GRID_COLOR = (192, 192, 192)
WHITE = (255, 255, 255)
BUTTON_COLOR = (5, 5 , 2)

IDEOLOGIES = {
    "communism": ("Communism", (255, 0, 0)),
    "nazism": ("Nazism", (0, 0, 0)),
    "dumbassism": ("Dumbassism", (0, 0, 255)),
    "capitalism": ("Capitalism", (0, 255, 0))
}

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("BuildACity")

MENU = "menu"
POLITICAL_SELECTION = "political_selection"
GAME = "game"
state = MENU

tile_x, tile_y = 0, 0
city_name = ""
city_ideology = ""

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
    compass_surface = pygame.Surface((compass_width, compass_height))
    marker_x, marker_y = compass_width // 2, compass_height // 2
    marker_radius = 20
    marker_color = (135, 206, 250)
    movement_speed = 20
    running = True
    font = pygame.font.Font(None, 31)
    label_color = WHITE

    while running:
        screen.fill(BG_COLOR)
        title_text = font.render("Choose Ideology", True, label_color)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - compass_height // 2 - 30))
        enter_text = font.render("Enter", True, label_color)
        screen.blit(enter_text, (WIDTH // 2 + compass_width // 2 + 18, HEIGHT // 2 - compass_height // 2))

        compass_surface.fill(WHITE)
        pygame.draw.rect(compass_surface, IDEOLOGIES["communism"][1], (0, 0, compass_width // 2, compass_height // 2))
        pygame.draw.rect(compass_surface, IDEOLOGIES["nazism"][1], (compass_width // 2, 0, compass_width // 2, compass_height // 2))
        pygame.draw.rect(compass_surface, IDEOLOGIES["dumbassism"][1], (0, compass_height // 2, compass_width // 2, compass_height // 2))
        pygame.draw.rect(compass_surface, IDEOLOGIES["capitalism"][1], (compass_width // 2, compass_height // 2, compass_width // 2, compass_height // 2))

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

        pygame.draw.circle(compass_surface, marker_color, (marker_x, marker_y), marker_radius)

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

        screen.blit(compass_surface, (WIDTH // 2 - compass_width // 2, HEIGHT // 2 - compass_height // 2))
        pygame.display.flip()

    state = GAME

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
        screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) // 2, button_rect.y + (button_height - button_text.get_height()) // 2))

    elif state == GAME:
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

        player_rect = pygame.Rect(tile_x * CELL_SIZE, tile_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        city_text = font.render(f"{city_name} ({city_ideology})", True, WHITE)
        screen.blit(city_text, (WIDTH - city_text.get_width() - 20, 20))

        # Tlačítko pro spuštění minihry
        mini_button = pygame.Rect(WIDTH - 150, HEIGHT - 60, 140, 40)
        pygame.draw.rect(screen, (0, 0, 0), mini_button)
        mini_text = font.render("Minihra", True, WHITE)
        screen.blit(mini_text, (mini_button.x + (140 - mini_text.get_width()) // 2, mini_button.y + 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU and button_rect.collidepoint(event.pos):
                get_city_name()
                political_compass()
            elif state == GAME and mini_button.collidepoint(event.pos):
                hra()  # Spustit minihru

    pygame.display.flip()

pygame.quit()
