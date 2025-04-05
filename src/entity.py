import pygame
import random
import sys
import base
class AirFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = 0
        self.health = 1
        self.attack = 1

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)




class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(base.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        """出界检查"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

