import pygame
import numpy as np

class Images:
    def __init__(self, screen, origin_point):
        self.origin_point = origin_point
        self.show_state = 3
        self.screen = screen

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 按1：只显示img1
                # 按2：只显示img2
                # 按3：都显示
                if event.key == pygame.K_1:
                    self.show_state = 1
                elif event.key == pygame.K_2:
                    self.show_state = 2
                elif event.key == pygame.K_3:
                    self.show_state = 3


    def draw(self, img1, img2, dx, dy):
        img1 = pygame.image.frombuffer(img1.astype(np.uint8), (img1.shape[1], img1.shape[0]), 'BGR').convert()
        # img1.set_alpha(128)
        img2 = pygame.image.frombuffer(img2.astype(np.uint8), (img2.shape[1], img2.shape[0]), 'BGR').convert()
        # img2.set_alpha(128)

        x0, y0 = self.origin_point
        if self.show_state == 1:
            self.screen.blit(img1, (x0, y0))
        elif self.show_state == 2:
            self.screen.blit(img2, (x0 + dx, y0 + dy))
        else:  # show_state == 3
            self.screen.blit(img1, (x0, y0))
            self.screen.blit(img2, (x0 + dx, y0 + dy))