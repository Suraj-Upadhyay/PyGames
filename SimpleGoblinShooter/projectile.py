import pygame as pg

class Projectile:

    def __init__(self, player):
        x, y = player.get_coordinates()
        w, h = player.get_dimensions()
        self.x = x + w / 2
        self.y = y + h / 2
        self.width = 10
        self.height = 10
        self.color = (0, 0, 102)
        self.exists = True
        if not player.get_direction():
            self.velocity = 8
        else:
            self.velocity = 8 * player.get_direction()

    def move(self, game_dimensions):
        if self.x + self.width > game_dimensions[0] or self.x < 0 or not self.exists:
            return False
        self.x += self.velocity
        return True

    def draw(self, window):
        pg.draw.ellipse(window, self.color, (self.x, self.y, self.width, self.height))

    def collided(self):
        self.exists = False

    def get_coordinates(self):
        return (self.x, self.y)

    def get_dimensions(self):
        return (self.width, self.height)
