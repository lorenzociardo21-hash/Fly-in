import pygame


class Text:
    def __init__(self, text: str, center: tuple[int, int]):
        self.font = pygame.font.Font(None, 24)
        self.center = pygame.Vector2(center)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.rect = self.text.get_rect(center=center)
        self.speed = 10

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.text, self.rect)

    def move(self):
        moved_x = self.rect.center[0] + self.speed
        moved_y = self.rect.center[1] + self.speed
        self.rect.center = pygame.Vector2(x=moved_x, y=moved_y)

    def reset_center(self):
        self.rect.center = self.center

    def change_center(self, new_center: tuple[int, int]):
        self.center = new_center


pygame.init()

screen = pygame.display.set_mode((640, 640))
x = 320
y = 320
dx = 10
dy = 10
clock = pygame.time.Clock()
running = True
dt = 0
text = Text("cazzo", (x, y))
while running:
    screen.fill('white')
    # pygame.draw.circle(screen, 'white', (x, y), 15)
    text.render(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                x += dx
                y += dy
                text.move()
            if event.key == pygame.K_r:
                dx = -dx
                dy = -dy
                text.reset_center()
            if event.key == pygame.K_a:
                x -= dx
                y -= dy
                text.change_center((x, y))
            if event.key == pygame.K_ESCAPE:
                running = False
    if x == 315:
        break
            
    dt = clock.tick(60)
pygame.quit()