import pygame

class ControlPoints:
    def __init__(self, screen):
        self.prev_points = None
        self.points = []
        self.screen = screen
        self.selecting_point_index = None
        self.RADIUS = 10

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                if len(self.points) < 3:
                    pos = pygame.mouse.get_pos()
                    self.points.append(pos)
                    print(pos)
                elif len(self.points) == 3:
                    pos = pygame.mouse.get_pos()
                    for idx, point in enumerate(self.points):
                        dx = pos[0] - point[0]
                        dy = pos[1] - point[1]
                        if dx**2 + dy**2 < self.RADIUS**2:
                            self.selecting_point_index = idx
                            break
            elif event.type == pygame.KEYDOWN:
                # when ESC is pressed
                if event.key == pygame.K_ESCAPE:
                    self.points = []
                    self.selecting_point_index = None
                    self.prev_points = None
                # when a point is selected
                if self.selecting_point_index != None and \
                    event.key in [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w]:

                    x, y = self.points[self.selecting_point_index]
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        vel = 5
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

                    if not self.prev_points:
                        self.prev_points = self.points[:]

                    self.points[self.selecting_point_index] = (x, y)

    def draw(self):
        for idx, point in enumerate(self.points):
            if idx == self.selecting_point_index:
                color = (0,0,255)  # blue
            else:
                color = (0,255,0)  # green
            pygame.draw.circle(self.screen, color, point, self.RADIUS, width=1)
            pygame.draw.circle(self.screen, color, point, 1)