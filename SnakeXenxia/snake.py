import random
import pygame
import assets

class Snake:

    class Body:
        def __init__(self, x, y, d, c, v, p=None, n=None):
            self.x = x
            self.y = y
            self.direction = d
            self.prev = p
            self.next = n
            self.color = c
            self.velocity = v

            # Variables to propogate info across the linked-list.
            self.inflexion = None
            self.changedirection = None
            self.nowmove = True

        def draw(self, window):
            pygame.draw.rect(window, self.color, (self.x, self.y, 16, 16))

        def move(self):
            if self.inflexion == (self.x, self.y):
                self.setdirection(self.changedirection)
            mov_x = mov_y = 0
            if self.direction == 'right':
                mov_x = 1
            elif self.direction == 'left':
                mov_x = -1
            elif self.direction == 'up':
                mov_y = -1
            elif self.direction == 'down':
                mov_y = 1
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
        head = self.Body(px, py, 'right', self.color, self.velocity)
        body = self.Body(px - 16, py, 'right', self.color, self.velocity)
        tail = self.Body(px - 32, py, 'right', self.color, self.velocity)
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
        mov_x = mov_y = 0

        if self.tail.direction == 'right':
            mov_x = 1
        elif self.tail.direction == 'left':
            mov_x = -1
        elif self.tail.direction == 'up':
            mov_y = -1
        elif self.tail.direction == 'down':
            mov_y = 1
        body = self.Body(self.tail.x - mov_x * 16, self.tail.y - mov_y * 16,\
               self.tail.direction, self.color, self.velocity)
        self.tail.next = body
        body.prev = self.tail
        self.tail = body

    def draw(self, window: pygame.Surface) -> None:
        body = self.body
        while body:
            body.draw(window)
            body = body.next

    def move(self, direction) -> None:
        if  self.body.direction in ('left', 'right') and direction in ('up', 'down') or \
            self.body.direction in ('up', 'down') and direction in ('left', 'right'):
            if self.body.nowmove:
                self.body.setdirection(direction)
                self.body.nowmove = False
        body = self.body
        while body:
            body.move()
            body = body.next
