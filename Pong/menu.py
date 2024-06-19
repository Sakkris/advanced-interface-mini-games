import pygame
import utility
from match import *
import os

pygame.init()
pygame.mixer.init()

navigationSound = pygame.mixer.Sound(os.path.join(utility.SOUND_FOLDER, 'buttonNav.mp3'))
navigationSound.set_volume(0.1)

selectSound = pygame.mixer.Sound(os.path.join(utility.SOUND_FOLDER, 'buttonSelect.mp3'))
selectSound.set_volume(0.1)


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
        self.chosen_diff = "medium"

    def reset_keys(self):
        self.up = False
        self.down = False
        self.select = False

    # draws the title of the current menu
    def draw_cursor(self):
        utility.draw_text(">", 48, self.cursor_rect.x, self.cursor_rect.y, False)

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
        self.modes_x, self.modes_y = self.mid_w, self.mid_h + 20
        self.settings_x, self.settings_y = self.mid_w, self.mid_h + 60
        self.manual_x, self.manual_y = self.mid_w, self.mid_h + 100
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 140
        self.cursor_rect.midtop = (self.modes_x + self.offset, self.modes_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text("Go up: W Key", 14, 55, 20, False)
            utility.draw_text("Go down: S Key", 14, 63, 34, False)
            utility.draw_text("Select: Space Key", 14, 75, 48, False)
            utility.draw_text('PONG', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 80, False)
            utility.draw_text("Modes", 30, self.modes_x, self.modes_y, False)
            utility.draw_text("Diff", 30, self.settings_x, self.settings_y, False)
            utility.draw_text("Controls", 30, self.manual_x, self.manual_y, False)
            utility.draw_text("Quit", 30, self.quit_x, self.quit_y, False)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            pygame.mixer.Sound.play(selectSound)
            self.change_state()
        if self.up or self.down:
            pygame.mixer.Sound.play(navigationSound)
            self.move_cursor()

    def move_cursor(self):
        if self.up:
            if self.state == "Modes":
                self.cursor_rect.midtop = (self.quit_x + self.offset, self.quit_y)
                self.state = "Quit"
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.modes_x + self.offset, self.modes_y)
                self.state = "Modes"
            elif self.state == "Manual":
                self.cursor_rect.midtop = (self.settings_x + self.offset, self.settings_y)
                self.state = "Settings"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.manual_x + self.offset, self.manual_y)
                self.state = "Manual"

        if self.down:
            if self.state == "Modes":
                self.cursor_rect.midtop = (self.settings_x + self.offset, self.settings_y)
                self.state = "Settings"
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.manual_x + self.offset, self.manual_y)
                self.state = "Manual"
            elif self.state == "Manual":
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
        elif self.state == "Manual":
            self.game.current_menu = self.game.manual_menu
        elif self.state == "Modes":
            self.game.current_menu = self.game.mode_menu
        self.run_display = False


class SettingsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Easy"
        self.easy_x, self.easy_y = self.mid_w, self.mid_h + 20
        self.medium_x, self.medium_y = self.mid_w, self.mid_h + 60
        self.hard_x, self.hard_y = self.mid_w, self.mid_h + 100
        self.back_x, self.back_y = self.mid_w, self.mid_h + 140
        self.cursor_rect.midtop = (self.easy_x + self.offset, self.easy_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text("Go up: W Key", 14, 55, 20, False)
            utility.draw_text("Go down: S Key", 14, 63, 34, False)
            utility.draw_text("Select: Space Key", 14, 75, 48, False)
            utility.draw_text('Diff', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 80, False)

            if self.chosen_diff == "easy":
                utility.draw_text("Easy", 30, self.easy_x, self.easy_y, True)
            else:
                utility.draw_text("Easy", 30, self.easy_x, self.easy_y, False)

            if self.chosen_diff == "medium":
                utility.draw_text("Medium", 30, self.medium_x, self.medium_y, True)
            else:
                utility.draw_text("Medium", 30, self.medium_x, self.medium_y, False)

            if self.chosen_diff == "hard":
                utility.draw_text("Hard", 30, self.hard_x, self.hard_y, True)
            else:
                utility.draw_text("Hard", 30, self.hard_x, self.hard_y, False)

            utility.draw_text("Back", 30, self.back_x, self.back_y, False)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            pygame.mixer.Sound.play(selectSound)
            self.change_state()
        if self.up or self.down:
            pygame.mixer.Sound.play(navigationSound)
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
        elif self.state == "Easy":
            self.game.dificulty = self.game.read_game_settings("easy")
            self.chosen_diff = "easy"
        elif self.state == "Medium":
            self.game.dificulty = self.game.read_game_settings("medium")
            self.chosen_diff = "medium"
        elif self.state == "Hard":
            self.game.dificulty = self.game.read_game_settings("hard")
            self.chosen_diff = "hard"
        self.run_display = False


class ModesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Single"
        self.single_x, self.single_y = self.mid_w, self.mid_h + 20
        self.multi_x, self.multi_y = self.mid_w, self.mid_h + 60
        self.back_x, self.back_y = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.single_x + self.offset, self.single_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text("Go up: W Key", 14, 55, 20, False)
            utility.draw_text("Go down: S Key", 14, 63, 34, False)
            utility.draw_text("Select: Space Key", 14, 75, 48, False)
            utility.draw_text('Modes', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 80, False)
            utility.draw_text("P1 V AI", 30, self.single_x, self.single_y, False)
            utility.draw_text("P1 VS P2", 30, self.multi_x, self.multi_y, False)
            utility.draw_text("Back", 30, self.back_x, self.back_y, False)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            pygame.mixer.Sound.play(selectSound)
            self.change_state()
        if self.up or self.down:
            pygame.mixer.Sound.play(navigationSound)
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
            self.game.match = Match(self.game, "single")
            self.game.isPlaying = True
        elif self.state == "Multi":
            self.game.current_menu = self.game.main_menu
            self.game.match = Match(self.game, "multi")
            self.game.isPlaying = True
        self.run_display = False


class ManualMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Back"
        self.back_x, self.back_y = self.mid_w, utility.WINDOW_HEIGHT - 100
        self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_events()
            self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text("Go up: W Key", 14, 55, 20, False)
            utility.draw_text("Go down: S Key", 14, 63, 34, False)
            utility.draw_text("Select: Space Key", 14, 75, 48, False)
            utility.draw_text('Controls', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 80, False)
            utility.draw_text('Move up paddle: P1 - W, P2 - UP',
                              20, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2, False)
            utility.draw_text('Move down paddle: P1 - S, P2 - Down',
                              20, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 + 40, False)
            utility.draw_text('Or Use your hands to guide the paddles!',
                              20, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 + 80, False)
            utility.draw_text("Back", 30, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT - 100, False)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.select:
            pygame.mixer.Sound.play(selectSound)
            self.change_state()

    def change_state(self):
        if self.state == "Back":
            self.game.current_menu = self.game.main_menu
        self.run_display = False
