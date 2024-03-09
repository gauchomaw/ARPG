from constants import *

class Skill:
    def __init__(self, name, key, damage = 1, area_damage = 0):
        self.name = name
        self.key = key
        self.damage = damage
        self.area_damage = area_damage
        self.backgound_color = BLUE

