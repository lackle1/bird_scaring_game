import math

import pygame as pg
import globals
import random
from pygame.constants import RLEACCEL
import numpy as np

from entity import Entity


class Bird(Entity):

    FLY_SPEED = 6
    DIST_BEFORE_DECEL = 100
    DECELERATION = (FLY_SPEED**2) / (2 * DIST_BEFORE_DECEL)

    LANDING_MARGIN = 0.025
    LANDING_BOUNDS = pg.Rect(globals.SCREEN_WIDTH * LANDING_MARGIN, globals.SCREEN_HEIGHT * LANDING_MARGIN,
                             globals.SCREEN_WIDTH * (1 - LANDING_MARGIN * 2), globals.SCREEN_HEIGHT * (1 - LANDING_MARGIN * 2))

    @staticmethod
    def get_start_pos(target):
        closest_edge = np.argmin((target.x, globals.SCREEN_WIDTH - target.x,
                                  target.y, globals.SCREEN_HEIGHT - target.y))

        dist_from_edge = 50
        match closest_edge:
            case 0:
                start_pos = pg.math.Vector2(
                    -dist_from_edge,
                    sorted((0, target.y + random.randint(-100, 100), globals.SCREEN_HEIGHT))[1])
            case 1:
                start_pos = pg.math.Vector2(
                    globals.SCREEN_WIDTH + dist_from_edge,
                    sorted((0, target.y + random.randint(-100, 100), globals.SCREEN_HEIGHT))[1])
            case 2:
                start_pos = pg.math.Vector2(
                    sorted((0, target.x + random.randint(-100, 100), globals.SCREEN_WIDTH))[1],
                    -dist_from_edge)
            case 3:
                start_pos = pg.math.Vector2(
                    sorted((0, target.x + random.randint(-100, 100), globals.SCREEN_WIDTH))[1],
                    globals.SCREEN_HEIGHT + dist_from_edge)

        print(f'Edge: {closest_edge}')
        print(f'Pos: {start_pos}')
        return start_pos

    @staticmethod
    def random_spawn():
        target_pos = pg.math.Vector2(
            random.randint(Bird.LANDING_BOUNDS.left, Bird.LANDING_BOUNDS.right),
            random.randint(Bird.LANDING_BOUNDS.top, Bird.LANDING_BOUNDS.bottom))

        return Bird.get_start_pos(target_pos), target_pos

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
        self.decelerating = False

    def update(self):

        dist_to_target_sqrd = (self.target_pos - self.pos).length_squared()

        if self.vel != 0:
            if dist_to_target_sqrd < self.vel.length_squared() and not self.scared:
                self.pos = self.target_pos
                self.vel = 0
            elif not self.scared and (self.decelerating or math.sqrt(dist_to_target_sqrd) < Bird.DIST_BEFORE_DECEL):
                self.decelerating = True
                speed = self.vel.length() - Bird.DECELERATION
                if speed < 0: self.vel = 0
                else:
                    self.vel = self.vel.normalize() * speed
                    self.pos += self.vel
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