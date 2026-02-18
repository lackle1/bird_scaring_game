import pygame
from pygame.constants import RLEACCEL


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.sprite = pygame.image.load("content/player.png").convert()
        self.sprite.set_colorkey((0, 0, 0), RLEACCEL)
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * 2, self.sprite.get_height() * 2))
        self.rect = self.sprite.get_rect()

        self.rect.x = x - self.rect.width/2
        self.rect.y = y - self.rect.height/2



    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.sprite, self.rect)

