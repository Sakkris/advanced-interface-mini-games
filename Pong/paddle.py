import pygame
import constants

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

class Paddle:
    COLOR = constants.WHITE_COLOR

    def __init__(self, x, y, width, height, speed):
        self.x = self.original_x = x 
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up and (self.y - self.speed >= 0):
            self.y -= self.speed
        elif not up and (self.y + self.speed + self.height <= constants.WINDOW_HEIGHT):
            self.y += self.speed

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

