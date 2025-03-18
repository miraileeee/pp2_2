import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((600, 450))
clock = pygame.time.Clock()

image = pygame.image.load('C://Users/User/pp2_2/Lab7/clock.png')
image = pygame.transform.scale(image, (600, 450))
s_hand = pygame.image.load('C://Users/User/pp2_2/Lab7/leftarm.png')
m_hand = pygame.image.load('C://Users/User/pp2_2/Lab7/rightarm.png')
s_hand = pygame.transform.scale(s_hand, (40, 500))
m_hand = pygame.transform.scale(m_hand, (500, 650))

cent = (300, 225)

def rotate(hand, angle, cent):
    rotated_hand = pygame.transform.rotate(hand, angle)
    rect = rotated_hand.get_rect(center = cent)  #rotation center same as cent
    return rotated_hand, rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(image, (0,0))

    now = datetime.datetime.now()
    min = now.minute
    sec = now.second
    m_angle = -30 - min * 6
    s_angle = -6 - sec * 6

    m_rotated, m_rect = rotate(m_hand, m_angle, cent)
    s_rotated, s_rect = rotate(s_hand, s_angle, cent)

    screen.blit(m_rotated, m_rect)
    screen.blit(s_rotated, s_rect)

    pygame.display.update()

    clock.tick(1)

