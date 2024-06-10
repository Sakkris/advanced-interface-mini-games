import pygame
import constants

class Menu:
    def __init__(self, title, buttons):
        self.menu_title = title
        self.menu_buttons = buttons

    def display_menu(self):
        constants.WINDOW.fill(constants.BACKGROUND_COLOR)
        title_text = constants.TEXT_FONT.render(f"{self.menu_title}", 1, constants.WHITE_COLOR)
        pygame.display.update()


class MainMenu(Menu):
    def __init__(self):
        super().__init__("PONG", [])