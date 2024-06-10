import pygame
import menu

# Game class is responsible for managing Menus and matches
# All the game logic behind menus and matches are made by their respective classes
class Game:
    def __init__(self):
        self.isRunning = True
        self.game_state = "menu"
        self.game_menu = menu.MainMenu()

    def run(self):
        while self.isRunning:
            if (self.game_state == "menu"):
                self.game_menu.display_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()