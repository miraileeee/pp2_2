import pygame

pygame.init()
screen = pygame.display.set_mode((450, 350))

color = (255, 0, 0)
r = 25
x, y = 25, 25
move = 20
clock = pygame.time.Clock()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                if y - move >= r:
                    y -= move
            if e.key == pygame.K_DOWN:
                if y + move <= 350 - r:
                    y += move
            if e.key == pygame.K_LEFT:
                if x - move >= r:
                    x -= move
            if e.key == pygame.K_RIGHT:
                if x + move <= 450 - r:
                    x += move

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, color, (x, y), 25)
    pygame.display.flip()


