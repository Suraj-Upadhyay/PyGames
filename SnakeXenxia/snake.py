import random
import pygame
import assets

class Snake:

    class Body:
        def __init__(self, x, y, d, c, v, limx, limy, p=None, n=None):
            self.x = x
            self.y = y
            self.direction = d
            self.prev = p
            self.next = n
            self.color = c
            self.velocity = v
            self.limx = limx
            self.limy = limy

            # Variables to propogate info across the linked-list.
            self.inflexion = None
            self.changedirection = None
            self.nowmove = True

        def draw(self, window):
            pygame.draw.rect(window, self.color, (self.x, self.y, 12, 12))

        def move(self):
            if self.inflexion == (self.x, self.y):
                self.setdirection(self.changedirection)
            mov_x = mov_y = 0
            if self.direction == 'right':
                mov_x = 1
                if self.x >= self.limx * 32:
                    self.x = -self.velocity
            elif self.direction == 'left':
                mov_x = -1
                if self.x + 12 <= 0:
                    self.x += self.limx * 32 + self.velocity
            elif self.direction == 'up':
                mov_y = -1
                if self.y + 12 <= 0:
                    self.y += self.limy * 32 + self.velocity
            elif self.direction == 'down':
                mov_y = 1
                if self.y >= self.limy * 32:
                    self.y = -self.velocity

            self.x += mov_x * self.velocity
            self.y += mov_y * self.velocity

        def setdirection(self, d):
            self.direction = d
            if self.next:
                self.next.inflexion = (self.x, self.y)
                self.next.changedirection = d
            if self.prev:
                self.prev.changed()
            return pygame.time.get_ticks()

        def changed(self):
            self.nowmove = True

    def __init__(self, map_name: str, vel: int):

        self.map_name = map_name
        self.game_map = assets.maps[self.map_name]
        self.color = assets.mapcolor[self.map_name][0]
        self.velocity = vel
        self.body, self.tail = self.__create_body()

    def __create_body(self):
        px, py = self.__spawn()
        limx = len(self.game_map[0])
        limy = len(self.game_map)
        head = self.Body(px, py, 'right', self.color, self.velocity, limx, limy)
        body = self.Body(px - 12, py, 'right', self.color, self.velocity, limx, limy)
        tail = self.Body(px - 24, py, 'right', self.color, self.velocity, limx, limy)
        head.next = body
        body.prev = head
        body.next = tail
        tail.prev = body
        return head, tail

    def __spawn(self):
        dimx = len(self.game_map[0])
        dimy = len(self.game_map)

        while True:
            x = random.randint(1, dimx - 2)
            y = random.randint(0, dimy - 1)
            if not (self.game_map[y][x] or self.game_map[y][x - 2]):
                break

        return (x * 32, y * 32)

    def grow(self):
        limx, limy = len(self.game_map[0]), len(self.game_map)
        mov_x = mov_y = 0

        if self.tail.direction == 'right':
            mov_x = 1
        elif self.tail.direction == 'left':
            mov_x = -1
        elif self.tail.direction == 'up':
            mov_y = -1
        elif self.tail.direction == 'down':
            mov_y = 1
        body = self.Body(self.tail.x - mov_x * 12, self.tail.y - mov_y * 12,\
               self.tail.direction, self.color, self.velocity, limx, limy)
        self.tail.next = body
        body.prev = self.tail
        self.tail = body

    def draw(self, window: pygame.Surface) -> None:
        body = self.body
        while body:
            body.draw(window)
            body = body.next

    def move(self, direction, food) -> None:
        # Check if we should change the direction or not.
        if  self.body.direction in ('left', 'right') and direction in ('up', 'down') or \
            self.body.direction in ('up', 'down') and direction in ('left', 'right'):
            if self.body.nowmove:
                self.body.setdirection(direction)
                self.body.nowmove = False

        # Move the snake body-part by body-part.
        body = self.body
        while body:
            body.move()
            body = body.next

        # Check for food.
        body = self.body
        foodeaten = False
        bigfoodeaten = False
        if food.bigfood:
            if  body.x in range(food.bigfoodposition[0] - 16, food.bigfoodposition[0] + 33) and \
                body.y in range(food.bigfoodposition[1] - 16, food.bigfoodposition[1] + 33) or \
                (body.x + 12) in range(food.bigfoodposition[0] - 16, food.bigfoodposition[0] + 33) and \
                (body.y + 12) in range(food.bigfoodposition[1] - 16, food.bigfoodposition[1] + 33):
                bigfoodeaten = True

        if  body.x in range(food.position[0] - 8, food.position[0] + 9) and \
            body.y in range(food.position[1] - 8, food.position[1] + 9) or \
            (body.x + 12) in range(food.position[0] - 8, food.position[0] + 9) and \
            (body.y + 12) in range(food.position[1] - 8, food.position[1] + 9):
            foodeaten = True

        food.eaten(foodeaten, bigfoodeaten)

        # Check for self collision.
        headRect = pygame.Rect(self.body.x, self.body.y, 12, 12)
        body = self.body.next.next
        while body:
            if headRect.colliderect(pygame.Rect(body.x, body.y, 12, 12)):
                return False
            body = body.next

        # Check for collision with the squares.
        limx, limy = len(self.game_map[0]), len(self.game_map)

        index_y, index_x = (self.body.y + 6) // 32, (self.body.x + 6) // 32
        if index_y < limy and index_x < limx and self.game_map[index_y][index_x]:
            return False

        return True
