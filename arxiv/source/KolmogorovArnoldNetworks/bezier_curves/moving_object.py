import pygame

class MovingObject:
    def __init__(self, path, speed=0.001):
        self.path = path
        self.speed = speed
        self.position = 0

    def update(self):
        self.position += self.speed
        if self.position >= 1:
            self.position = 0

    def get_position(self):
        index = int(self.position * (len(self.path) - 1))
        return self.path[index]

    def draw(self, screen, color=(150, 100, 100)):
        pos = self.get_position()
        pygame.draw.circle(screen, color, pos, 8)

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed
