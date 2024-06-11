import pygame
import utility
from match import *

pygame.init()


# Menus display buttons for the players to navigate with
# Contains a list of buttons to be displayed depending on the menu
# isChanged refers to when the menu changes and new buttons need to be generated to be displayed
class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 40, 40)
        self.offset = -100
        self.up, self.down, self.select = False, False, False

    def reset_keys(self):
        self.up = False
        self.down = False
        self.select = False

    # draws the title of the current menu
    def draw_cursor(self):
        utility.draw_text(">", 48, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        utility.WINDOW.blit(utility.DISPLAY, (0, 0))
        pygame.display.update()
        self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.select = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.up = True


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Modes"
        self.modes_x, self.modes_y = self.mid_w, self.mid_h + 50
        self.settings_x, self.settings_y = self.mid_w, self.mid_h + 100
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.modes_x + self.offset, self.modes_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text('PONG', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 20)
            utility.draw_text("Modes", 48, self.modes_x, self.modes_y)
            utility.draw_text("Diff", 48, self.settings_x, self.settings_y)
            utility.draw_text("Quit", 48, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            self.change_state()
        if self.up or self.down:
            self.move_cursor()

    def move_cursor(self):
        if self.up:
            if self.state == "Modes":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "Quit"
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.modes_x + self.offset, self.modes_y)
                self.state = "Modes"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.settings_x + self.offset, self.settings_y)
                self.state = "Settings"

        if self.down:
            if self.state == "Modes":
                self.cursor_rect.midtop = (self.settings_x + self.offset, self.settings_y)
                self.state = "Settings"
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.modes_x + self.offset, self.modes_y)
                self.state = "Modes"

    def change_state(self):
        if self.state == "Quit":
            pygame.quit()
        elif self.state == "Settings":
            self.game.current_menu = self.game.settings_menu
        elif self.state == "Modes":
            self.game.current_menu = self.game.mode_menu
        self.run_display = False


class SettingsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Easy"
        self.easy_x, self.easy_y = self.mid_w, self.mid_h + 50
        self.medium_x, self.medium_y = self.mid_w, self.mid_h + 100
        self.hard_x, self.hard_y = self.mid_w, self.mid_h + 150
        self.back_x, self.back_y = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.easy_x + self.offset, self.easy_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text('Diff', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 20)
            utility.draw_text("Easy", 48, self.easy_x, self.easy_y)
            utility.draw_text("Medium", 48, self.medium_x, self.medium_y)
            utility.draw_text("Hard", 48, self.hard_x, self.hard_y)
            utility.draw_text("Back", 48, self.back_x, self.back_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            self.change_state()
        if self.up or self.down:
            self.move_cursor()

    def move_cursor(self):
        if self.up:
            if self.state == "Easy":
                self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)
                self.state = "Back"
            elif self.state == "Medium":
                self.cursor_rect.midtop = (self.easy_x + self.offset, self.easy_y)
                self.state = "Easy"
            elif self.state == "Hard":
                self.cursor_rect.midtop = (self.medium_x + self.offset, self.medium_y)
                self.state = "Medium"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.hard_x + self.offset, self.hard_y)
                self.state = "Hard"

        if self.down:
            if self.state == "Easy":
                self.cursor_rect.midtop = (self.medium_x + self.offset, self.medium_y)
                self.state = "Medium"
            elif self.state == "Medium":
                self.cursor_rect.midtop = (self.hard_x + self.offset, self.hard_y)
                self.state = "Hard"
            elif self.state == "Hard":
                self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.easy_x + self.offset, self.easy_y)
                self.state = "Easy"

    def change_state(self):
        if self.state == "Back":
            self.game.current_menu = self.game.main_menu
        self.run_display = False


class ModesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Single"
        self.single_x, self.single_y = self.mid_w, self.mid_h + 50
        self.multi_x, self.multi_y = self.mid_w, self.mid_h + 100
        self.back_x, self.back_y = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.single_x + self.offset, self.single_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text('Modes', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 20)
            utility.draw_text("P1 V AI", 48, self.single_x, self.single_y)
            utility.draw_text("P1 VS P2", 48, self.multi_x, self.multi_y)
            utility.draw_text("Back", 48, self.back_x, self.back_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            self.change_state()
        if self.up or self.down:
            self.move_cursor()

    def move_cursor(self):
        if self.up:
            if self.state == "Single":
                self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)
                self.state = "Back"
            elif self.state == "Multi":
                self.cursor_rect.midtop = (self.single_x + self.offset, self.single_y)
                self.state = "Single"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.multi_x + self.offset, self.multi_y)
                self.state = "Multi"

        if self.down:
            if self.state == "Single":
                self.cursor_rect.midtop = (self.multi_x + self.offset, self.multi_y)
                self.state = "Multi"
            elif self.state == "Multi":
                self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.single_x + self.offset, self.single_y)
                self.state = "Single"

    def change_state(self):
        if self.state == "Back":
            self.game.current_menu = self.game.main_menu
        elif self.state == "Single":
            self.game.current_menu = self.game.main_menu
            self.game.match = Match("single")
            self.game.isPlaying = True
        elif self.state == "Multi":
            self.game.current_menu = self.game.main_menu
            self.game.match = Match("multi")
            self.game.isPlaying = True
        self.run_display = False
