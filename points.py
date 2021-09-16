import pygame
import math

class Points:
    def __init__(self, screen):
        self.screen = screen
        self.points = []
        self.RADIUS = 10
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                print(pos)
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