import random
import pygame as pg

class HealthBar:
    def __init__(self, player):

        w, h = player.get_dimensions()
        self.player = player
        # Keep the width of the health bar at 70 % of the character width.
        self.width = 0.7 * w
        # Keep the height of the health bar at 10 % of the character height.
        self.height = 0.1 * h
        self.move()

    def move(self):
        x, y = self.player.get_coordinates()
        w, h = self.player.get_dimensions()
        self.x = x + 0.20 * w
        self.y = y + 0.05 * h

    def update(self, window):
        rectRed = pg.Rect(self.x, self.y, self.width, self.height)
        rectWhite = pg.Rect(self.x, self.y, self.width * self.player.health / 100, self.height)
        pg.draw.rect(window, (255, 0, 0), rectRed)
        pg.draw.rect(window, (255, 255, 255), rectWhite)

class Player:

    # pylint: disable=too-many-instance-attributes

    def __init__(self, x, y, w, h, a=10, v=5):

        # pylint: disable=too-many-arguments

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.velocity = v
        self.acceleration = a   # Gravitational Acceleration.
        # Attributes with hard coded initial values.
        self.direction = random.choice([-1, 1])
        self.walk_count = 0
        self.health = 100

    def is_dead(self):
        if self.health <= 0:
            return True
        return False

    def draw(self, window):
        pg.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

    def get_coordinates(self):
        # No settor for the variables x and y as
        # these are meant to be changed only by the player movement.
        return (self.x, self.y)

    def get_dimensions(self):
        # Returns a tuple as the dimensions are not meant to be changed.
        return (self.width, self.height)

    def get_direction(self):
        return self.direction

class Human(Player):
    def __init__(self, x, y, w, h, a=10, v=5):

        # pylint: disable=too-many-arguments

        super().__init__(x, y, w, h, a, v)
        self.__load_sprites()
        self.healthBar = HealthBar(self)
        self.isCollidedLeft = False
        self.isCollidedRight = False
        self.isCollidedUp = False
        self.jumping = False
        self.Score = 0

    def __load_sprites(self):
        self.left_facing_sprites = [pg.image.load("assets/L{0}.png".format(i)) \
                                    for i in range(1, 10)]
        self.right_facing_sprites = [pg.image.load("assets/R{0}.png".format(i)) \
                                     for i in range(1, 10)]

    def move_left(self):
        if self.x < -20:
            return
        self.direction = -1
        if self.is_jumping():
            self.x += (self.velocity + 4) * self.direction
        else:
            self.x += self.velocity * self.direction
        self.walk_count += 1

    def move_right(self, dimensions):
        if self.x + self.width - 20 > dimensions[0]:
            return
        self.direction = 1
        if self.is_jumping():
            self.x += (self.velocity + 4) * self.direction
        else:
            self.x += self.velocity * self.direction
        self.walk_count += 1

    def is_jumping(self):
        return self.jumping

    def jump(self, lim: int):
        self.jumping = True
        if self.acceleration < -lim:
            self.jumping = False
            self.acceleration = 10
            return

        quadratic = (self.acceleration ** 2) / 2
        if self.acceleration < 0:
            self.y += quadratic
        else:
            self.y -= quadratic

        self.acceleration -= 1

    def draw(self, window):
        sprites = self.right_facing_sprites if self.direction == 1 else self.left_facing_sprites
        if self.is_jumping():
            sprite = sprites[0]
        else:
            sprite = sprites[self.walk_count % len(sprites)]
        window.blit(sprite, self.get_coordinates())
        self.healthBar.move()
        self.healthBar.update(window)

    def collided(self, goblin):
        if goblin.walk_count % 100000:
            self.Score -= 1
            self.health -= 0.5

    def increase_Score(self):
        self.Score += 5

    def get_Score(self):
        return self.Score

class Goblin(Player):
    def __init__(self, player, v=3):

        #pylint: disable=too-many-arguments
        x = random.randrange(0, 5000, 1) % 500
        super().__init__(x, 425, 64, 64, 10, v)
        self.__load_sprites()
        self.player = player
        self.direction = 1 if x < player.get_coordinates()[0] else -1
        self.healthbar = HealthBar(self)

    def __load_sprites(self):
        self.left_facing_sprites = [pg.image.load("assets/L{0}E.png".format(i)) \
                                    for i in range(1, 10)]
        self.right_facing_sprites = [pg.image.load("assets/R{0}E.png".format(i)) \
                                     for i in range(1, 10)]

    def move(self, game_dimensions):
        if self.x < -20:
            self.direction = 1
        elif self.x + self.width - 20 > game_dimensions[0]:
            self.direction = -1

        self.x += self.velocity * self.direction
        self.walk_count += 1
        if self.is_dead():
            return False
        return True

    def draw(self, window):
        sprites = self.right_facing_sprites if self.direction == 1 else self.left_facing_sprites
        sprite = sprites[self.walk_count % len(sprites)]
        window.blit(sprite, self.get_coordinates())
        self.healthbar.move()
        self.healthbar.update(window)

    def decrease_health(self):
        self.health -= 10

    def collision(self, bullets=None):
        if bullets:
            for sprite in bullets:
                if self.__check_collision(sprite):
                    self.decrease_health()
                    sprite.collided()
                    self.player.increase_Score()
                    return

        if self.__check_collision(self.player):
            self.player.collided(self)
            self.direction = 0
        else:
            self.direction = 1 if self.x < self.player.get_coordinates()[0] else -1

    def __check_collision(self, sprite):
        sprite_x, sprite_y = sprite.get_coordinates()
        sprite_w, sprite_h = sprite.get_dimensions()

        left_x = self.x + self.width - 20 >= sprite_x and \
                    self.x + self.width - 20 <= sprite_x + sprite_w
        right_x = self.x >= sprite_x and self.x <= sprite_x + sprite_w
        enclose_x = self.x <= sprite_x and self.x + self.width >= sprite_x + sprite_w
        collision_x = left_x or enclose_x or right_x

        up_x = self.y + self.height >= sprite_y and \
                self.y + self.height <= sprite_y + sprite_h
        down_x = self.y >= sprite_y and self.y <= sprite_y + sprite_h
        enclose_y = self.y <= sprite_y and self.y + self.height >= sprite_y + sprite_h
        collision_y = up_x or enclose_y or down_x

        return collision_x and collision_y
