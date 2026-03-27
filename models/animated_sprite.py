import pygame as pg
import pygame.time
from pygame.math import Vector2 as Vec2

class AnimationData:
    def __init__(self, num_frames, row):
        self.num_frames = num_frames
        self.row = row

class AnimatedSprite:

    FRAME_DURATION = 150

    def __init__(self, texture_file, frame_dims: Vec2, scale: int):
        self.texture = pg.image.load(texture_file)
        self.texture = pg.transform.scale(self.texture, (self.texture.get_width() * scale, self.texture.get_height() * scale))
        self.frame_dims = frame_dims * scale
        self.src_rect = pg.Rect(0, 0, self.frame_dims.x, self.frame_dims.y)

        self.animations = {}
        self.current_anim = AnimationData(1,0)
        self.current_anim_start = pygame.time.get_ticks()
        self.row_offset = 0     # For different versions of the same animation (mostly used for different directions)

    def update(self):
        elapsed_time = pygame.time.get_ticks() - self.current_anim_start
        current_frame = (elapsed_time // AnimatedSprite.FRAME_DURATION) % self.current_anim.num_frames
        self.src_rect.x = current_frame * self.src_rect.width
        self.src_rect.y = (self.current_anim.row + self.row_offset) * self.src_rect.height

    def add_animation(self, name, num_frames, row):
        self.animations[name] = AnimationData(num_frames, row)

    def set_animation(self, name, row_offset = 0):
        self.current_anim = self.animations[name]
        self.current_anim_start = pygame.time.get_ticks()
        self.row_offset = row_offset

    def render(self, screen, pos):
        screen.blit(self.texture, pos, self.src_rect)