import pygame
import numpy as np

class Images:
    def __init__(self, screen, origin_point):
        self.origin_point = origin_point
        self.shift = (0, 0)
        self.show_state = 3
        self.screen = screen

    def update(self, events):
        x, y = self.shift
        for event in events:
            if event.type == pygame.KEYDOWN:

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

        self.shift = (x, y)

    def draw(self, img1, img2):
        img1 = pygame.image.frombuffer(img1.astype(np.uint8), (img1.shape[1], img1.shape[0]), 'RGB').convert()
        img1.set_alpha(128)
        img2 = pygame.image.frombuffer(img2.astype(np.uint8), (img2.shape[1], img2.shape[0]), 'RGB').convert()
        img2.set_alpha(128)

        x0, y0 = self.origin_point
        x, y = self.shift
        if self.show_state == 1:
            self.screen.blit(img1, (x0, y0))
        elif self.show_state == 2:
            self.screen.blit(img2, (x0 + x, y0 + y))
        else:  # show_state == 3
            self.screen.blit(img1, (x0, y0))
            self.screen.blit(img2, (x0 + x, y0 + y))