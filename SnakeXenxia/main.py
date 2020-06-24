import os
import sys
import pygame as pg
import assets
import snake
import food

dimension = 1024, 512
window = pg.display.set_mode(dimension)
pg.display.set_caption('Snake Xenxia')
clock = pg.time.Clock()
white = (255, 255, 255)
map_name = 'rails'
path = os.path.join("assets", map_name)
squares = [pg.image.load(path + "/square0.png"), pg.image.load(path + "/square1.png")]
texture = pg.image.load(path + "/texture.png")
black = (0, 0, 0)
game_map = assets.maps[map_name]
Snake = snake.Snake(map_name, 4)
pg.time.set_timer(pg.USEREVENT + 1, 4000)
gameover = True
Food = food.Food(map_name, Snake)
while True:
    clock.tick(60)
    window.fill(white)
    for i, _i in enumerate(game_map):
        for j, _j in enumerate(_i):
            position = j * 32, i * 32
            if game_map[i][j] == 1:
                window.blit(squares[0], position)
            elif game_map[i][j] == -1:
                window.blit(squares[1], position)
            elif game_map[i][j] == 0:
                window.blit(texture, position)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    direction = None
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        direction = 'up'
    elif keys[pg.K_s]:
        direction = 'down'
    elif keys[pg.K_a]:
        direction = 'left'
    elif keys[pg.K_d]:
        direction = 'right'

    if gameover:
        gameover = Snake.move(direction, Food)

    Food.draw(window)
    Snake.draw(window)
    pg.display.update()

pg.quit()
