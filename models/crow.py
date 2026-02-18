import pygame
from pygame.constants import RLEACCEL

from models.bird import Bird

class Crow(Bird):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.sprite = pygame.image.load("content/crow.png").convert()
        self.sprite.set_colorkey((0, 0, 0), RLEACCEL)
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * 2, self.sprite.get_height() * 2))
        self.rect = self.sprite.get_rect()

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))