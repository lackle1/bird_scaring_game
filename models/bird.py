import math

import pygame as pg
from pygame.math import Vector2 as Vec2
import globals
import random
from pygame.constants import RLEACCEL
import numpy as np

from models.entity import Entity
from models.animated_sprite import AnimatedSprite


class Bird(Entity):

    FLY_SPEED = 6
    DIST_BEFORE_DECEL = 180
    DECELERATION = (FLY_SPEED**2) / (2 * DIST_BEFORE_DECEL)

    LANDING_MARGIN = 0.025
    LANDING_BOUNDS = pg.Rect(globals.SCREEN_WIDTH * LANDING_MARGIN, globals.SCREEN_HEIGHT * LANDING_MARGIN,
                             globals.SCREEN_WIDTH * (1 - LANDING_MARGIN * 2), globals.SCREEN_HEIGHT * (1 - LANDING_MARGIN * 2))

    @staticmethod
    def get_start_pos(target):
        closest_edge = np.argmin((target.x, globals.SCREEN_WIDTH - target.x,
                                  target.y, globals.SCREEN_HEIGHT - target.y))

        dist_from_edge = 200
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

        return start_pos

    @staticmethod
    def random_spawn():
        target_pos = pg.math.Vector2(
            random.randint(Bird.LANDING_BOUNDS.left, Bird.LANDING_BOUNDS.right),
            random.randint(Bird.LANDING_BOUNDS.top, Bird.LANDING_BOUNDS.bottom))

        return Bird.get_start_pos(target_pos), target_pos

    def __init__(self):

        self.animated_sprite = AnimatedSprite('content/crow.png', Vec2(24, 24), 2)
        self.animated_sprite.add_animation('idle', 1, 0)
        self.animated_sprite.add_animation('fly', 2, 2)

        self.sprite_dims = self.animated_sprite.frame_dims

        self.pos, self.target_pos = Bird.random_spawn()

        diff = self.target_pos - self.pos
        self.vel = diff.normalize() * Bird.FLY_SPEED
        self.dir = self.get_dir()
        self.animated_sprite.set_animation('fly', self.dir)

        # Flag for conditional movement
        self.scared = False

        self.decelerating = False

    def update(self):

        self.animated_sprite.update()

        dist_to_target_sqrd = (self.target_pos - self.pos).length_squared()

        if self.vel != 0:
            if dist_to_target_sqrd < self.vel.length_squared() and not self.scared:
                self.pos = self.target_pos
                self.vel = 0
                self.animated_sprite.set_animation('idle', self.dir)
            elif not self.scared and (self.decelerating or math.sqrt(dist_to_target_sqrd) < Bird.DIST_BEFORE_DECEL):
                self.decelerating = True
                speed = self.vel.length() - Bird.DECELERATION
                if speed < 0:
                    self.vel = 0
                    self.animated_sprite.set_animation('idle', self.dir)
                else:
                    self.vel = self.vel.normalize() * speed
                    self.pos += self.vel
            else:
                self.pos += self.vel

    def render(self, screen):
        # screen.blit(self.sprite, self.pos)
        self.animated_sprite.render(screen, self.pos)

    def get_dir(self):
        return 1 if self.vel.x >= 0 else 0

    def fly_away(self, direction):
        """
        The bird will be scared and fly away
        in the opposite direction of the player's
        """
        if not self.scared:
            self.scared = True
            self.vel = direction.normalize() * Bird.FLY_SPEED
            self.dir = self.get_dir()
            self.animated_sprite.set_animation('fly', self.dir)