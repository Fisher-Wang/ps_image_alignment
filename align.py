# -*- coding: utf-8 -*-
import pygame
import numpy as np
from skimage import io
from control_points import ControlPoints
from points import Points
from utils import convert_color_temperature
from images import Images

## Global Setting ##
# set image path, img1 is fixed, img2 can move
# path1 = "imgs/1.png"
# path2 = "imgs/2.png"
path1 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_35_31_138-9.png"
path2 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_36_27_261-51.png"
# set color temperature
temperature1 = 7000
temperature2 = 2000
# set origin point (top left corner)
x0, y0 = -750, -550

## Read Image ##
img1 = io.imread(path1)
img1 = convert_color_temperature(img1, temperature1)

img2 = io.imread(path2)
img2 = convert_color_temperature(img2, temperature2)

## Initialize Pygame ##
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Image Alignment")
pygame.mouse.set_cursor(pygame.cursors.tri_left)

## Register Objects ##
points = Points(screen)
control_points = ControlPoints(screen)
images = Images(screen, (x0, y0))

## Main Loop ##
run = True
while run:
    pygame.time.delay(50)

    ## Update ##
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    points.update(events)
    control_points.update(events)
    images.update(events)

    ## Draw ##
    screen.fill((0, 0, 0))
    images.draw(img1, img2)
    points.draw()
    control_points.draw()
    pygame.display.update()
