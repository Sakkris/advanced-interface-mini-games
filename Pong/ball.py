import pygame
import constants

BALL_RADIUS = 7

class Ball:
    MAX_VELOCITY = 5
    COLOR = constants.WHITE_COLOR

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0
    
    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1