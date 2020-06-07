import os
import pygame as pg
from player import Human, Goblin
from projectile import Projectile

# Initialize pygame and the clock.
pg.init()
Clock = pg.time.Clock()
BulletClock = pg.time.Clock()
fps = 27
NEW_GOBLIN = pg.USEREVENT + 1

background = pg.image.load(os.path.join("assets", "bg.jpg"))

class Game_Window:
    def __init__(self, dimensions: tuple, title: str):
        self.dimensions = dimensions
        self.title = title
        self.window = pg.display.set_mode(dimensions)

        pg.display.set_caption(title)

    def redraw(self, objects):
        player = objects["Player"]
        goblins = objects["Goblins"]
        bullets = objects["Bullets"]

        self.window.blit(background, (0, 0))

        if player.is_dead():
            myfont = pg.font.SysFont("Comic Sans MS", 90)
            label = myfont.render("Game Over", 1, (255, 0, 0))
            self.window.blit(label, (100, 200))
            pg.display.update()
            return

        Score = player.get_Score()
        myfont = pg.font.SysFont("Comic Sans MS", 30)
        label = myfont.render("Score {}".format(Score), 1, (0, 173, 52))

        labelWidth = 0
        while Score > 0:
            Score //= 10
            labelWidth += 1

        self.window.blit(label, (400 - labelWidth * 5, 25))

        player.draw(self.window)
        for x in goblins:
            x.draw(self.window)

        for x in bullets:
            x.draw(self.window)

        pg.display.update()

    def get_dimensions(self):
        return self.dimensions

# The gameplay that gets executed 27 times a second.
def gameplay(game_window: Game_Window, objects: list) -> list:
    #pylint: disable=too-many-branches
    Clock.tick(fps)

    player = objects["Player"]
    # Check for events here
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return -1
        if event.type == NEW_GOBLIN:
            objects["Goblins"].append(Goblin(player))

    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        player.move_left()
    elif keys[pg.K_d]:
        player.move_right(game_window.get_dimensions())

    if not player.is_jumping():
        if keys[pg.K_SPACE]:
            player.jump(10)
    else:
        player.jump(10)

    if keys[pg.K_w] and BulletClock.tick() > 100:
        objects["Bullets"].append(Projectile(player))

    for bullet in objects["Bullets"]:
        if not bullet.move(game_window.get_dimensions()):
            objects["Bullets"].remove(bullet)

    for goblin in objects["Goblins"]:
        if not goblin.move(game_window.get_dimensions()):
            objects["Goblins"].remove(goblin)
        goblin.collision(objects["Bullets"])

    game_window.redraw(objects)
    return objects

def main():
    # Initialize Player.
    player = Human(200, 420, 64, 64)
    goblin = Goblin(player)
    win = Game_Window((500, 480), "First Game")
    objects = {"Player" : player, "Goblins" : [goblin], "Bullets" : []}
    pg.time.set_timer(NEW_GOBLIN, 8000)
    # Execute the mainloop.
    while True:
        objects = gameplay(win, objects)
        if objects == -1:
            break

    pg.quit()

main()
