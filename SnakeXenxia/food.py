import random
import pygame
import assets

class Food:
    def __init__(self, map_name, snake):
        self.foodsize = 8
        self.foodcount = 0
        self.foodoscillator = [4, 1]

        self.bigfood = False
        self.bigfoodsize = 16
        self.bigfoodoscillator = [4, 1]
        self.bigfoodcounter = None

        self.snake = snake
        self.game_map = assets.maps[map_name]
        self.foodcolor = assets.mapcolor[map_name][2]
        self.bigfoodcolor = assets.mapcolor[map_name][3]

        self.position = self.__spawn(self.foodsize)
        self.bigfoodposition = None

    def __spawn(self, size):
        while True:
            x, y = random.randint(size, (len(self.game_map[0]) - 1) * 32), \
                    random.randint(size, (len(self.game_map) - 1) * 32)

            # Avoid spawning food on the bricks.
            if not self.game_map[(y - size) // 32][x // 32] \
                and not self.game_map[(y + size) // 32][x // 32] \
                and not self.game_map[y // 32][(x + size) // 32] \
                and not self.game_map[y // 32][(x - size) // 32]:

                # Avoid spawning food on the snake.
                snake = self.snake.body
                while snake:
                    if x in range(snake.x - size, snake.x + 2 * size)  and \
                        y in range(snake.y - size, snake.y + 2 * size):
                        break
                    snake = snake.next
                else:
                    break

        self.foodcount += 1
        return (x, y)

    def draw(self, window):
        # Oscillate and draw normal food.
        if self.foodoscillator[0] <= -4:
            self.foodoscillator[1] = -1
        elif self.foodoscillator[0] >= 4:
            self.foodoscillator[1] = 1

        pygame.draw.circle(window, self.foodcolor, self.position, \
                            self.foodsize - self.foodoscillator[0])

        self.foodoscillator[0] -= self.foodoscillator[1]

        # Oscillate and draw special food.
        if self.bigfood:
            if self.bigfoodoscillator[0] <= -4:
                self.bigfoodoscillator[1] = -1
            elif self.bigfoodoscillator[0] >= 4:
                self.bigfoodoscillator[1] = 1

            pygame.draw.circle(window, self.bigfoodcolor, self.bigfoodposition, \
                                self.bigfoodsize - self.bigfoodoscillator[0])

            self.bigfoodoscillator[0] -= self.bigfoodoscillator[1]

            if (pygame.time.get_ticks() - self.bigfoodcounter) // 3000:
                self.eaten(False, True)

    def eaten(self, foodeaten: bool, bigfood: bool):
        if foodeaten:
            self.snake.grow()
            self.position = self.__spawn(self.foodsize)
            self.foodoscillator = [4, 1]
        if bigfood:
            self.bigfood = False
            self.foodcount = 0
            self.bigfoodcounter = None
            self.bigfoodposition = None
        if self.foodcount == 5 and not self.bigfood:
            self.bigfood = True
            self.bigfoodposition = self.__spawn(self.bigfoodsize)
            self.bigfoodcounter = pygame.time.get_ticks()
