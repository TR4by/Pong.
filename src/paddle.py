import pygame
from src.config import *


class Paddle:
    def __init__(self, x, y, width, height, speed, up_key, down_key, color):
        self.rect = pygame.Rect(x, y - height // 2, width, height)
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key
        self.initial_y = y
        self.score = 0
        self.color = color

    def move(self, pressed_keys):
        if pressed_keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
            if self.rect.top < 0:
                self.rect.top = 0
        if pressed_keys[self.down_key] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

    def reset(self):
        self.rect.centery = self.initial_y

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.rect)
