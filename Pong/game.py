import pygame
from menu import Menu
from match import Match

pygame.init()
pygame.display.set_caption("Pong")


# Game class is responsible for managing Menus and matches
# All the game logic behind menus and matches are made by their respective classes
# Game States: Menu, Single Play, Multi Play (local only for now)
# Match keeps track of which match is to be displayed (multi player or single player)
class Game:
    def __init__(self):
        self.isRunning = True
        self.game_menu = Menu()
        self.match = None
        self.game_state = "single"
        self.current_menu = "main"

    def run(self):
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if self.game_state == "menu":
                self.game_menu.display_menu(self.current_menu)
            elif self.game_state == "local":
                self.match = Match("local")
                self.match.start_match()
            elif self.game_state == "single":
                self.match = Match("single")
                self.match.start_match()
