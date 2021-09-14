# -*- coding: utf-8 -*-
import pygame
import numpy as np
from skimage import io
import math

# set image path, img1 is fixed, img2 can move
path1 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_35_31_138-9.png"
path2 = "ToMatch/MER-503-36U3C(NT0170120068)_2021-09-11_20_36_27_261-51.png"
# set image transparency
transparency1 = 128  # set 50% transparency
transparency2 = 128  # set 50% transparency
# set color temperature
temperature1 = 7000
temperature2 = 2000

kelvin_table = {
    1000: (255, 56, 0),
    1500: (255, 109, 0),
    2000: (255, 137, 18),
    2500: (255, 161, 72),
    3000: (255, 180, 107),
    3500: (255, 196, 137),
    4000: (255, 209, 163),
    4500: (255, 219, 186),
    5000: (255, 228, 206),
    5500: (255, 236, 224),
    6000: (255, 243, 239),
    6500: (255, 249, 253),
    7000: (245, 243, 255),
    7500: (235, 238, 255),
    8000: (227, 233, 255),
    8500: (220, 229, 255),
    9000: (214, 225, 255),
    9500: (208, 222, 255),
    10000: (204, 219, 255)
}


def convert_color_temperature(img, temperature):
    r, g, b = kelvin_table[temperature]
    matrix = np.array([r / 255, g / 255, b / 255])
    img = img * matrix
    return img


pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Image Alignment")
pygame.mouse.set_cursor(pygame.cursors.tri_left)

# path1 = "imgs/1.png"
img1 = io.imread(path1)
print(img1.shape, img1.dtype)
img1 = convert_color_temperature(img1, temperature1)
print(img1.shape, img1.dtype)
img1 = pygame.image.frombuffer(img1.astype(np.uint8), (img1.shape[1], img1.shape[0]), 'RGB').convert()
img1.set_alpha(transparency1)

# path2 = "imgs/2.png"
img2 = io.imread(path2)
img2 = convert_color_temperature(img2, temperature2)
img2 = pygame.image.frombuffer(img2.astype(np.uint8), (img2.shape[1], img2.shape[0]), 'RGB').convert()
img2.set_alpha(transparency2)

x0, y0 = -750, -550
x, y = 0, 0

show_state = 3

class Points:
    def __init__(self, screen):
        self.screen = screen
        self.points = []
        self.RADIUS = 10
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                in_circle = False
                for idx, point in enumerate(self.points):
                    dx = pos[0] - point[0]
                    dy = pos[1] - point[1]
                    r = math.sqrt(dx**2 + dy**2)
                    if r < self.RADIUS:
                        in_circle = True
                        del self.points[idx]
                        break
                if not in_circle:
                    self.points.append(pos)
    def draw(self):
        for point in self.points:
            pygame.draw.circle(self.screen, (255,0,0), point, self.RADIUS, width=1)
            pygame.draw.circle(self.screen, (255,0,0), point, 1)

points = Points(screen)

run = True
while run:
    pygame.time.delay(50)
    events = pygame.event.get()
    points.update(events)
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                vel = 50
            else:
                vel = 1

            if event.key == pygame.K_a:
                x -= vel
            elif event.key == pygame.K_d:
                x += vel
            elif event.key == pygame.K_w:
                y -= vel
            elif event.key == pygame.K_s:
                y += vel

            # 按1：只显示img1
            # 按2：只显示img2
            # 按3：都显示
            elif event.key == pygame.K_1:
                show_state = 1
            elif event.key == pygame.K_2:
                show_state = 2
            elif event.key == pygame.K_3:
                show_state = 3

    screen.fill((0, 0, 0))
    if show_state == 1:
        screen.blit(img1, (x0, y0))
    elif show_state == 2:
        screen.blit(img2, (x0 + x, y0 + y))
    else:  # show_state == 3
        screen.blit(img1, (x0, y0))
        screen.blit(img2, (x0 + x, y0 + y))
    points.draw()

    pygame.display.update()
