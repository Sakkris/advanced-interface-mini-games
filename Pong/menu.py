import pygame
import utility

pygame.init()

# Menus display buttons for the players to navigate with
# Contains a list of buttons to be displayed depending on the menu
# isChanged refers to when the menu changes and new buttons need to be generated to be displayed
class Menu:
    def __init__(self):
        self.menu_title = "PONG"
        self.menu_buttons = []
        self.isChanged = False

    # displays the Title of the menu + buttons of the menu
    def display_menu(self, menu_type):
        utility.WINDOW.fill(utility.BACKGROUND_COLOR)
        self.draw_title(utility.TITLE_POS)
        pygame.display.update()

    # draws the title of the current menu
    def draw_title(self, pos):
        text_surface = utility.TITLE_FONT.render(f"{self.menu_title}", 1, utility.WHITE_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (pos[0], pos[1])
        utility.WINDOW.blit(text_surface, text_rect)
