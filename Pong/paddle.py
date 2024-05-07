import pygame
import constants

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

class Paddle:
    COLOR = constants.WHITE_COLOR 
    velocity = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x 
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up and (self.y - self.velocity >= 0):
            self.y -= self.velocity
        elif not up and (self.y + self.velocity + self.height <= constants.WINDOW_HEIGHT):
            self.y += self.velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

