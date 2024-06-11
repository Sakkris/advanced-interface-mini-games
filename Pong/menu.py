import pygame
import utility

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


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.modes_x, self.modes_y = self.mid_w, self.mid_h + 50
        self.settings_x, self.settings_y = self.mid_w, self.mid_h + 100
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 150
        self.cursor_rect.midtop = (self.modes_x + self.offset, self.modes_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            #self.check_input()
            utility.DISPLAY.fill(utility.BACKGROUND_COLOR)
            utility.draw_text('PONG', 120, utility.WINDOW_WIDTH / 2, utility.WINDOW_HEIGHT / 2 - 20)
            utility.draw_text("Modes", 48, self.modes_x, self.modes_y)
            utility.draw_text("Settings", 48, self.settings_x, self.settings_y)
            utility.draw_text("Quit", 48, self.quit_x, self.quit_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.up = True
            self.move_cursor()
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.down = True
            self.move_cursor()
        elif keys[pygame.K_KP_ENTER]:
            self.select = True
            self.change_state()

    def move_cursor(self):
        return

    def change_state(self):
        return
