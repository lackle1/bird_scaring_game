import pygame as pg
import globals
import random
from pygame.constants import RLEACCEL

from entity import Entity


class Bird(Entity):

    FLY_SPEED = 2
    LANDING_BOUNDS = pg.Rect(globals.SCREEN_WIDTH * 0.1, globals.SCREEN_HEIGHT * 0.1,
                             globals.SCREEN_WIDTH * 0.8, globals.SCREEN_HEIGHT * 0.8)

    @staticmethod
    def random_spawn():
        start_pos = pg.math.Vector2(0,0)
        dist_from_edge = random.randint(50, 200)

        side = random.randint(0, 4) # 0: Left, 1: Right, 2: Top, 3: Bottom
        if side == 4: side = 0

        match side:
            case 0:
                start_pos = pg.math.Vector2(-dist_from_edge, random.randint(0, globals.SCREEN_HEIGHT))
            case 1:
                start_pos = pg.math.Vector2(globals.SCREEN_WIDTH + dist_from_edge, random.randint(0, globals.SCREEN_HEIGHT))
            case 2:
                start_pos = pg.math.Vector2(random.randint(0, globals.SCREEN_WIDTH), -dist_from_edge)
            case 3:
                start_pos = pg.math.Vector2(random.randint(0, globals.SCREEN_WIDTH), globals.SCREEN_HEIGHT + dist_from_edge)


        target_pos = pg.math.Vector2(random.randint(Bird.LANDING_BOUNDS.left, Bird.LANDING_BOUNDS.right),
                                     random.randint(Bird.LANDING_BOUNDS.top, Bird.LANDING_BOUNDS.bottom))

        print(start_pos, side)
        return start_pos, target_pos

    def __init__(self):
        self.sprite = pg.image.load("content/crow.png").convert()
        self.sprite.set_colorkey((0, 0, 0), RLEACCEL)
        self.sprite = pg.transform.scale(self.sprite, (self.sprite.get_width() * 2, self.sprite.get_height() * 2))
        self.rect = self.sprite.get_rect()

        self.pos, self.target_pos = Bird.random_spawn()

        diff = self.target_pos - self.pos
        self.vel = diff.normalize() * Bird.FLY_SPEED

        # Flag for conditional movement
        self.scared = False

    def update(self):
        if self.vel != 0:
            if (self.target_pos - self.pos).length_squared() < self.vel.length_squared() and not self.scared:
                self.pos = self.target_pos
                self.vel = 0
            else:
                self.pos += self.vel

    def render(self, screen):
        screen.blit(self.sprite, self.pos)

    def fly_away(self, direction):
        """
        The bird will be scared and fly away
        in the opposite direction of the player's
        """
        if not self.scared:
            self.scared = True
            self.vel = direction.normalize() * Bird.FLY_SPEED