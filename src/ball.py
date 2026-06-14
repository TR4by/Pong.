import pygame
import random
from src.config import *

class Ball:
    def __init__(self, size, speed, color):
        self.size = size
        self.base_speed = speed
        self.rect = pygame.Rect(0, 0, size, size)
        self.position = pygame.math.Vector2(0.0, 0.0)
        self.velocity = pygame.math.Vector2(0.0, 0.0)
        self.color = color
        self.reset()

    def reset(self):
        self.set_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        dir_x = 1 if random.randint(0, 1) == 1 else -1
        self.velocity = pygame.math.Vector2(self.base_speed * dir_x, 0.0)

    def update(self):
        self.position += self.velocity
        self.rect.center = (int(self.position.x), int(self.position.y))

    def bounce_edges(self):
        has_hit_top = self.rect.top <= 0 and self.velocity.y < 0
        has_hit_bottom = self.rect.bottom >= SCREEN_HEIGHT and self.velocity.y > 0
        
        if has_hit_top or has_hit_bottom:
            self.velocity.y *= -1
    
    def check_paddle_collision(self, left_paddle, right_paddle):
        paddle = left_paddle if self.velocity.x < 0 else right_paddle

        if self.rect.colliderect(paddle.rect):
            normalized_hit_position = (self.position.y - paddle.rect.centery) / (paddle.rect.height / 2)
            max_bounce_speed = 8
            bounce_speed = int(normalized_hit_position * max_bounce_speed)
            self.velocity.y = bounce_speed + random.randint(-1, 1)
            self.velocity.x *= -1

    def draw(self):
        self.rect.center = (int(self.position.x), int(self.position.y))
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.rect)

    def set_position(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.rect.center = (int(self.position.x), int(self.position.y))
