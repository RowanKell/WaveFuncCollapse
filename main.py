import os.path

import pygame
import random
import numpy as np
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
import pygame.freetype

pygame.init()

tile_image_list = ["Tiles/blank.png", "Tiles/up.png", "Tiles/right.png", "Tiles/down.png", "Tiles/left.png"]

screen_width = 800
screen_height = 800
global screen
screen = pygame.display.set_mode((screen_width, screen_height))

#Values for adjusting how many tiles we want on screen
tile_width_num = 2
radius = 4
tile_height_num = 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, num):
        super(Tile, self).__init__()
        self.surf = pygame.image.load(tile_image_list[num])
        self.surf = pygame.transform.scale(self.surf, (
            screen_width / radius, screen_height / radius)
        )

    def position(self, num):
        self.rect = self.surf.get_rect(
            center=(num[0], num[1])
        )

    def show(self):
        screen.blit(self.surf, self.rect)


def tile_centering():
    center_of_tile_radius = radius * 2
    odds = [0] * 4
    dimensions = [[(0, 0) for x in range(radius)] for x in range(radius)]
    for i in range(len(odds)):
        odds[i] = 2 * i + 1
    for i in range(radius):
        for j in range(radius):
            dimensions[i][j] = (screen_width * odds[i] / center_of_tile_radius, screen_height * odds[j] / center_of_tile_radius)
    return dimensions


#fill screen with black
def setup():
    screen.fill((255, 255, 255))


running = True
while running:
    setup()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    tileset = [["tile%d" % x for x in range(radius)] for x in range(radius)]
    for i in range(len(tileset)):
        for tile in tileset[i]:
            tile_index = tileset[i].index(tile)
            tile = Tile(tile_index % 4)
            tile_center = tile_centering()[i][tile_index]
            tile.position(tile_center)
            tile.show()
    pygame.display.flip()
pygame.quit()