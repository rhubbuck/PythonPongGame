import pygame

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Paddle:
    velocity = 6
    width = 20
    height = 100

    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, window):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, down=True):
        if down:
            self.y += self.velocity
        else:
            self.y -= self.velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    max_velocity = 6
    color = WHITE
    radius = 8

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_velocity = self.max_velocity
        self.y_velocity = 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0
        self.x_velocity *= -1
