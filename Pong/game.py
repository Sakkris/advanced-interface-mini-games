import pygame
from menu import *
from match import Match

pygame.init()
pygame.display.set_caption("Pong")


# Game class is responsible for managing Menus and matches
# All the game logic behind menus and matches are made by their respective classes
# Game States: Menu, Single Play, Multi Play (local only for now)
# Match keeps track of which match is to be displayed (multi player or single player)
class Game:
    def __init__(self):
        self.isRunning, self.isPlaying = True, False
        self.main_menu = MainMenu(self)
        self.settings_menu = None
        self.mode_menu = None
        self.current_menu = self.main_menu
        self.match = None

    def run(self):
        while self.isRunning:
            self.current_menu.display_menu()
            # run game
