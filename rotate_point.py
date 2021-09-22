import pygame

class RotatePoint:
    def __init__(self, screen):
        self.screen = screen
        self.point = None
        self.RADIUS = 10

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_MIDDLE:
                pos = pygame.mouse.get_pos()
                if self.point == None:
                    self.point = pos
                else:
                    dx = pos[0] - self.point[0]
                    dy = pos[1] - self.point[1]
                    if dx**2 + dy**2 < self.RADIUS**2:
                        self.point = None
                break

    def draw(self):
        if self.point != None:
            color = (238, 238, 0)  # yellow
            pygame.draw.circle(self.screen, color, self.point, self.RADIUS, width=1)
            pygame.draw.circle(self.screen, color, self.point, 1)