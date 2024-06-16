import pygame

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 500
FPS = 60
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (50,205,50)
BACKGROUND_COLOR = (25, 25, 25)
WINNING_SCORE = 3
BOTTOM_OFFSET = 130

# MENU POSITIONS
TITLE_POS = (200, 200)
BUTTON_X = 200
BUTTON_Y = 300

# WINDOW AND FONT STATIC VALUES
DISPLAY = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FONT_NAME = "visitor1.ttf"
NORMAL_FONT = pygame.font.Font("visitor1.ttf", 48)
TITLE_FONT = pygame.font.Font("visitor1.ttf", 120)


# FUNCTIONS
def draw_text(text, size, x, y, highlighted):
    font = pygame.font.Font(FONT_NAME, size)

    if highlighted:
        text_surface = font.render(text, True, HIGHLIGHT_COLOR)
    else:
        text_surface = font.render(text, True, WHITE_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    DISPLAY.blit(text_surface, text_rect)
