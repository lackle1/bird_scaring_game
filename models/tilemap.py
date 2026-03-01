import pygame as pg
import numpy as np
import globals

class Tilemap:
    def __init__(self, file):
        self.size = (int(globals.SCREEN_HEIGHT/globals.TILE_SIZE), int(globals.SCREEN_WIDTH/globals.TILE_SIZE))
        self.tiles_img = pg.image.load(file).convert()
        self.img_width = self.tiles_img.get_width()
        self.img_height = self.tiles_img.get_height()
        self.tileset = self.load_tiles()

        """
        Here we initialize a map that show the layout of our tileset
        Each different tile will be encoded with a number (the index in the tilset)
        """
        self.map = np.zeros(self.size, dtype=int)

        h, w = self.size
        self.surf = pg.Surface((globals.TILE_SIZE * w, globals.TILE_SIZE * h))

        self.rect = self.surf.get_rect()

    def load_tiles(self) -> list[pg.Surface]:
        """
        This will extract the various tiles from the image
        and store them in a list
        :return: the tiles list
        """
        # Load a single tile for now
        tiles = []
        for i in range(0, self.img_height, globals.TILE_SIZE):
            for j in range(0, self.img_width, globals.TILE_SIZE):
                tile = pg.Surface((globals.TILE_SIZE, globals.TILE_SIZE))
                tile.blit(self.tiles_img, (0, 0), (i, j, *(globals.TILE_SIZE, globals.TILE_SIZE)))
                tiles.append(tile)

        return tiles



    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset[self.map[i, j]]
                self.surf.blit(tile, (j * globals.TILE_SIZE, i * globals.TILE_SIZE))