import pygame
import constants

BALL_RADIUS = 7

class Ball:
    COLOR = constants.WHITE_COLOR

    def __init__(self, x, y, radius, starting_speed, max_velocity, speed_modifier):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.starting_speed = starting_speed
        self.x_velocity = starting_speed
        self.y_velocity = 0
        self.max_velocity = max_velocity
        self.speed_modifier = speed_modifier
    
    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0

        if (self.x_velocity < 0):
            self.x_velocity = self.starting_speed
        else:
            self.x_velocity = -self.starting_speed

    def increase_speed(self):
        is_negative = False

        if (self.x_velocity < 0):
            is_negative = True
            self.x_velocity *= -1

        if (self.x_velocity < self.max_velocity):
            self.x_velocity += self.speed_modifier

        if (is_negative):
            self.x_velocity *= -1
