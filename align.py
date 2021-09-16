# -*- coding: utf-8 -*-
import pygame
import numpy as np
from control_points import ControlPoints
from points import Points
from utils import *
from images import Images
import cv2

## Global Setting ##
# set image path, img1 is fixed, img2 can move
path1 = "ToMatch/1.PNG"
path2 = "ToMatch/2.PNG"
# path1 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_35_31_138-9.png"
# path2 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_36_27_261-51.png"
# set color temperature
temperature1 = 7000
temperature2 = 2000
# set origin point (top left corner)
# x0, y0 = -750, -550
x0, y0 = -10, -10
# x0, y0 = 0, 0

## Read Image ##
img1 = cv2.imread(path1)
img1 = convert_color_temperature(img1, temperature1, 'BGR')
img2 = cv2.imread(path2)
img2 = convert_color_temperature(img2, temperature2, 'BGR')

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

dx, dy = 0, 0
prev_control_points = None
prev_num = 0
Ms = []

run = True
while run:
    pygame.time.delay(50)

    ## Update ##
    num = control_points.get_num()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and num == 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                vel = 50
            else:
                vel = 1

            if event.key == pygame.K_a:
                dx -= vel
            elif event.key == pygame.K_d:
                dx += vel
            elif event.key == pygame.K_w:
                dy -= vel
            elif event.key == pygame.K_s:
                dy += vel

    points.update(events)
    control_points.update(events)
    images.update(events)
    if num == 3:
        if prev_control_points == None:
            pass
        # record shift affine
        elif prev_num == 0:
            Ms.append(get_shift_affine(dx, dy))
            dx, dy = 0, 0
        # record 3-point affine
        elif not equal_points(prev_control_points, control_points.points):
            # print('diff')
            Ms.append(get_3point_affine(prev_control_points, control_points.points, x0, y0))
            dx, dy = 0, 0

    # print(dx, dy)
    print(len(Ms))
    print(Ms)
    # print(prev_control_points)
    # print(control_points.points)

    prev_control_points = control_points.points[:]
    prev_num = num

    M = combine_affine(Ms[::1])
    img2_show = cv2.warpAffine(img2, M, (img2.shape[1], img2.shape[0]))

    ## Draw ##
    screen.fill((0, 0, 0))
    images.draw(img1, img2_show, dx, dy)
    points.draw()
    control_points.draw()
    pygame.display.update()
