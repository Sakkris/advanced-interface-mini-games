import pygame
import utility

class Paddle:
    COLOR = utility.WHITE_COLOR

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
        elif not up and (self.y + self.speed + self.height <= utility.WINDOW_HEIGHT):
            self.y += self.speed

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

