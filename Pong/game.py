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
        self.settings_menu = SettingsMenu(self)
        self.mode_menu = ModesMenu(self)
        self.manual_menu = ManualMenu(self)
        self.current_menu = self.main_menu
        self.match = None
        self.dificulty = None

    def run(self):
        while self.isRunning:
            while self.isPlaying and self.match is not None:
                self.match.start_match()
            self.current_menu.display_menu()

    def read_game_settings(self, dificulty: str):
        with io.open("game_settings.yaml", "r") as stream:
            data = yaml.safe_load(stream)

        dificulty_settings = data['dificulties'][dificulty]
        return dificulty_settings
