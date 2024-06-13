import pygame

import utility


class Button:
    def __init__(self, pos, desc, preferences, index):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.desc = desc
        self.prefs = preferences
        self.index = index
