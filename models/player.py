import pygame as pg
from pygame.constants import RLEACCEL

import globals
from entity import Entity


class Player(Entity):
    START_SPEED = 4
    def __init__(self):
        super(Player, self).__init__()
        self.sprite = pg.image.load("content/player.png").convert()
        self.sprite.set_colorkey((0, 0, 0), RLEACCEL)
        self.sprite = pg.transform.scale(self.sprite, (self.sprite.get_width() * 2, self.sprite.get_height() * 2))
        self.rect = self.sprite.get_rect()

        self.pos = pg.math.Vector2(globals.SCREEN_WIDTH/2 - self.rect.width/2,
                                   globals.SCREEN_HEIGHT/2 - self.rect.height/2)

        self.speed = Player.START_SPEED


    def update(self):
        keys = pg.key.get_pressed()

        vel = pg.math.Vector2(0, 0)

        if keys[pg.K_w]:
            vel.y -= 1
        elif keys[pg.K_s]:
            vel.y += 1

        if keys[pg.K_a]:
            vel.x -= 1
        elif keys[pg.K_d]:
            vel.x += 1

        if vel.length() != 0:
            vel = vel.normalize() * self.speed

        self.pos += vel


    def render(self, screen):
        screen.blit(self.sprite, self.pos)

    def scare_bird(self, bird):
        """
        Compute the vector from the player to the bird
        and scare it away
        """
        target = bird.pos - self.pos

        bird.fly_away(target)

    def check_birds(self, grid):
        """
        Check all the birds in adjacent cells
        """
        cell_x, cell_y = self.get_cell_coords()
        for unit in grid.get_unit_from_adjacent_cells(cell_x, cell_y):
            if (unit.pos - self.pos).length() <= 100 and unit != self:
                self.scare_bird(unit)