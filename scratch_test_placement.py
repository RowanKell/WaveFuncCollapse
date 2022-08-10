import os.path

import pygame
import random
import numpy as np
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
import pygame.freetype

pygame.init()

tile_image_list = ["Tiles/blank.png", "Tiles/up.png", "Tiles/right.png", "Tiles/down.png", "Tiles/left.png"]

screen_width = 800
screen_height = 600
global screen
screen = pygame.display.set_mode((screen_width, screen_height))

#Values for adjusting how many tiles we want on screen
radius = 5
BLANK = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4


options_list = [BLANK, LEFT, UP, RIGHT, DOWN]
collapsed = False
init_collapsed = False
running = True


class Space(pygame.sprite.Sprite):
    def __init__(self, number):
        super(Space, self).__init__()
        self.type = None
        self.collapsed = False
        self.options = []
        self.position = []
        self.entropy = None
        self.number = number


tile_type_dict = {
        0: [0, 0, 0, 0],
        1: [1, 1, 1, 0],
        2: [1, 1, 1, 0],
        3: [0, 1, 1, 1],
        4: [1, 0, 1, 1]
        }
class Tile(pygame.sprite.Sprite):
    def __init__(self, num):
        super(Tile, self).__init__()
        if num == None:
            self.surf = pygame.image.load("Tiles/black.png")
        else:
            self.surf = pygame.image.load(tile_image_list[num])
        self.surf = pygame.transform.scale(self.surf, (
            screen_width / radius, screen_height / radius)
        )
        self.type = None

    def position(self, num):
        self.rect = self.surf.get_rect(
            center=(num[0], num[1])
        )

    def show(self):
        screen.blit(self.surf, self.rect)


def tile_centering():
    center_of_tile_radius = radius * 2
    odds = [0] * radius
    dimensions = [[(0, 0) for x in range(radius)] for x in range(radius)]
    for i in range(len(odds)):
        odds[i] = 2 * i + 1
    for i in range(radius):
        for j in range(radius):
            dimensions[i][j] = (screen_width * odds[i] / center_of_tile_radius, screen_height * odds[j] / center_of_tile_radius)
    return dimensions


def restart():
    pygame.quit()
#add code that restarts the program so I can call this in collapse function in case any spaces have no options


#side_num tells which side is being looked at (0 is left for instance)
def compare(_tile: Space, side_num):
    tile_type = _tile.type
    values = tile_type_dict[tile_type]
    compare_num = (side_num + 2) % 4
    compatible_list = []
    for i in range(len(options_list)):
        #value is the 0 or 1 value of the input (collapsed) tile side
        value = values[side_num - 1]
        compare_tile = options_list[i]
        compare_values = tile_type_dict[compare_tile]
        compare_value = compare_values[compare_num]
        if value == compare_value:
            compatible_list.append(compare_tile)
    return compatible_list


def connecting(space_list):
    for i in range(radius):
        for j in range(radius):
            space = space_list[i][j]
            space.options.clear()

    for i in range(radius):
        for j in range(radius):
            space = space_list[i][j]
            space.position = [i, j]
            print("space position: ", space.position)
            #For spaces that have another space at top border
            if j > 0:
                test_left_space = space_list[i][j - 1]
                test_right_space.position = [i, j - 1]
                print("test left:", test_left_space.position)
                if test_left_space.collapsed:
                    left_options = compare(test_left_space, 0)
                elif not test_left_space.collapsed:
                    left_options = options_list
            else:
                left_options = options_list
            # For spaces that have another space at bottom border
            if j < radius - 1:
                test_right_space = space_list[i][j + 1]
                test_right_space.position = [i, j + 1]
                print("test right:", test_right_space.position)
                if test_right_space.collapsed:
                    right_options = compare(test_right_space, 2)
                elif not test_right_space.collapsed:
                    right_options = options_list
            else:
                right_options = options_list
            if i > 0:
                test_up_space = space_list[i - 1][j]
                test_up_space.position = [i - 1, j]
                print("test up:", test_up_space.position)
                if test_up_space.collapsed:
                    up_options = compare(test_up_space, 1)
                elif not test_up_space.collapsed:
                    up_options = options_list
            else:
                up_options = options_list
            if i < radius - 1:
                test_down_space = space_list[i + 1][j]
                test_down_space.position = [i + 1, j]
                print("test down:", test_down_space.position)
                if test_down_space.collapsed:
                    down_options = compare(test_down_space, 3)
                elif not test_down_space.collapsed:
                    down_options = options_list
            else:
                down_options = options_list
            for k in range(5):
                if k in (left_options and right_options and up_options and down_options):
                    space.options.append(k)
            space.entropy = len(space.options)


#collapsing is recursive with connecting() within
def collapsing(space_list):
    connecting(space_list)
    global init_collapsed
    if not init_collapsed:
        randi = random.randint(0, radius - 1)
        randj = random.randint(0, radius - 1)
        randk = random.randint(0, radius - 1)
        space_list[randi][randj].type = randk
        space_list[randi][randj].collapsed = True
        space_list[randi][randj].entropy = -1
        init_collapsed = True
    entropy_list = [[len(options_list)] * radius] * radius
#    for space_row_index in range(len(space_list)):
#        for space in space_list[space_row_index]:
#            space_index = space_list[space_row_index].index(space)
#            space.entropy_init()
    min_entropy = [5, 0, 1]
    multiple_min_entropy_list = []
    multiple_min_entropy_bool = False
    entropy_count = 0
    collapsed_count = 0
    for i in range(radius):
        for j in range(radius):
            space = space_list[i][j]
            space.position = [i, j]
            if space.collapsed:
                entropy_list[i][j] = -1
                continue
            if not space.collapsed:
                entropy_list[i][j] = space.entropy
                entropy_count += 1
    for i in range(radius):
        for j in range(radius):
            space = space_list[i][j]
            if space.collapsed:
                continue
            entropy = entropy_list[i][j]
            if entropy < min_entropy[0]:
                min_entropy[0] = entropy
                min_entropy[1] = i
                min_entropy[2] = j
                multiple_min_entropy_list.clear()
                multiple_min_entropy_bool = False
            elif entropy == min_entropy[0]:
                multiple_min_entropy_list.append([i, j])
                min_entropy[0] = entropy
                multiple_min_entropy_bool = True
            elif entropy > min_entropy[0]:
                continue
    if multiple_min_entropy_bool:
        min_amount = len(multiple_min_entropy_list)
        pick = random.randint(0, min_amount - 1)
        collapse_space = space_list[multiple_min_entropy_list[pick][0]][multiple_min_entropy_list[pick][1]]
    else:
        collapse_space = space_list[min_entropy[1]][min_entropy[2]]
    if len(collapse_space.options) > 1:
        pick = random.randint(0, len(collapse_space.options) - 1)
        collapse_tile = options_list[pick]
    elif len(collapse_space.options) == 0:
        restart()
    else:
        collapse_tile = options_list[collapse_space.options]
    collapse_space.collapsed = True
    collapse_space.type = collapse_tile
    all_collapsed = True
    for i in range(radius):
        for j in range(radius):
            if space_list[i][j].collapsed:
                continue
            elif not space_list[i][j].collapsed:
                all_collapsed = False
                break
        if not all_collapsed:
            break
    if all_collapsed:
        return
    elif not all_collapsed:
        collapsing(space_list)


#fill screen with black
def setup():
    screen.fill((255, 255, 255))



while running:
    setup()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False


#    _space_list = [[Space()] * radius] * radius
    if not collapsed:
        _space_list = []
        for a in range(radius):
            _space_list.append([Space(a * b) for b in range(radius)])
        collapsing(_space_list)
        collapsed = True

    tileset = [["tile%d" % x for x in range(radius)] for x in range(radius)]
    print(tileset)
    tile = Tile(_space_list[0][1].type)
    tile_center = tile_centering()[0][1]
    tile.position(tile_center)
    tile.show()
    pygame.display.flip()
pygame.quit()
