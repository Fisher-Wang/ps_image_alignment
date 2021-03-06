# -*- coding: utf-8 -*-
import pygame
import numpy as np
from control_points import ControlPoints
from points import Points
from utils import *
from images import Images
import cv2
from rotate_point import RotatePoint
import copy
import os

## Global Setting ##
# set image path, img1 is fixed, img2 can move
# path1 = "ToMatch/1.PNG"
# path2 = "ToMatch/2.PNG"
# path1 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_35_31_138-9.png"
# path2 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_36_27_261-51.png"

# !!!
# You need to change this!
# path_dic = {
#     'nutsball_abs' : '../../../research/diligent_v2/nutsBall/abs/MER-503-36U3C(NT0170120068)_2021-09-19_22_28_41_841-59.png',
#     'nutsball_Al' : '../../../research/diligent_v2/nutsBall/Al/MER-503-36U3C(NT0170120068)_2021-09-20_13_57_41_598-473.png',
#     'nutsball_bakelite' : '../../../research/diligent_v2/nutsBall/bakelite/MER-503-36U3C(NT0170120068)_2021-09-19_22_38_04_596-48.png',
#     'nutsball_Cu' : '../../../research/diligent_v2/nutsBall/Cu/MER-503-36U3C(NT0170120068)_2021-09-20_14_03_45_624-168.png',
#     'nutsball_nilon' : '../../../research/diligent_v2/nutsBall/nilon/MER-503-36U3C(NT0170120068)_2021-09-19_22_46_01_980-31.png',
# }
# path1 = path_dic['nutsball_bakelite']
# path2 = path_dic['nutsball_abs']
result_dir = 'result'

path1 = '../../../research/diligent_v2/other/fans2/bakelitePNG/5.png'
path2 = '../../../research/diligent_v2/other/fans2_aligned/absPNG/1.png'

objname = 'fans2'
texturename = 'abs'

# set color temperature
temperature1 = 10000
temperature2 = 7000
# set origin point (top left corner)
x0, y0 = 0, 0
# x0, y0 = -10, -10
# x0, y0 = 0, 0

## Read Image ##
img1 = cv2.imread(path1)
# img1 = convert_color_temperature(img1, temperature1, 'BGR')
img2 = cv2.imread(path2)
img2 = sharpen(img2, 5)
# img2 = convert_color_temperature(img2, temperature2, 'BGR')

## Initialize Pygame ##
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Image Alignment")
pygame.mouse.set_cursor(pygame.cursors.tri_left)

## Register Objects ##
points = Points(screen)
control_points = ControlPoints(screen)
images = Images(screen, (x0, y0))
rotate_point = RotatePoint(screen)

## Main Loop ##

dx, dy = 0, 0
angle = 0
prev_control_points = None
prev_rotate_point = None
prev_num = 0
Ms = []
M = None


def save_info():
    f = open(os.path.join(result_dir, objname+'_'+texturename), 'w+')
    f.write('dx = {}, dy = {}\n'.format(dx, dy))
    f.write('rotation_point = {}\n'.format(prev_rotate_point))
    f.write('degree = %.1f\n' % (angle))
    f.close()

    np.save(os.path.join(result_dir, objname+'_'+texturename+'.npy'), M)

run = True
while run:
    pygame.time.delay(50)

    ## Update ##
    num = control_points.get_num()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            save_info()
            run = False
        elif event.type == pygame.KEYDOWN and num == 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                vel = 50
                vel_angle = 1
            else:
                vel = 1
                vel_angle = 0.2

            # shift
            if event.key == pygame.K_a:
                dx -= vel
            elif event.key == pygame.K_d:
                dx += vel
            elif event.key == pygame.K_w:
                dy -= vel
            elif event.key == pygame.K_s:
                dy += vel
            # rotate
            elif event.key == pygame.K_LEFTBRACKET:
                angle += vel_angle
            elif event.key == pygame.K_RIGHTBRACKET:
                angle -= vel_angle


    points.update(events)
    control_points.update(events)
    rotate_point.update(events)
    images.update(events)
    if num == 3:
        if prev_control_points == None:
            pass
        elif not equal_points(prev_control_points, control_points.points):
            # record shift affine
            if (dx, dy) != (0, 0):
                Ms.append(get_shift_affine(dx, dy))
                dx, dy = 0, 0
            # record 3-point affine
            Ms.append(get_3point_affine(prev_control_points, control_points.points, x0, y0))
    else:
        # only concern rotate when there is no control points
        if prev_rotate_point == None and rotate_point.point != None:
            if (dx, dy) != (0, 0):
                print('rotate begin')
                Ms.append(get_shift_affine(dx, dy))
                dx, dy = 0, 0
        if prev_rotate_point != None and rotate_point.point == None:
            if angle != 0:
                print('rotate end')
                px, py = prev_rotate_point
                Ms.append(cv2.getRotationMatrix2D((px - x0, py - y0), angle, 1.0))
                angle = 0


    print(dx, dy)
    print("%.1f degree" % (angle))
    print(len(Ms))
    # print(Ms)
    # print(prev_control_points)
    # print(control_points.points)

    prev_control_points = copy.deepcopy(control_points.points)
    prev_rotate_point = copy.deepcopy(rotate_point.point)
    prev_num = num

    # TODO
    if rotate_point.point != None:
        p = rotate_point.point
    else:
        p = (0, 0)
    M_rotate = cv2.getRotationMatrix2D((p[0] - x0, p[1] - y0), angle, 1.0)

    M = combine_affine(Ms + [M_rotate])

    img2_show = cv2.warpAffine(img2, M, (img2.shape[1], img2.shape[0]))

    ## Draw ##
    screen.fill((0, 0, 0))
    images.draw(img1, img2_show, dx, dy)
    points.draw()
    control_points.draw()
    rotate_point.draw()
    pygame.display.update()

