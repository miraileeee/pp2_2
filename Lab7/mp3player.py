import pygame
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 300))

playing = True
path = r'C:\Users\User\pp2_2\Lab7\songs'
lib = [song for song in os.listdir(path)]
font = pygame.font.SysFont('Times New Roman', 25)



now = 0
vol = 0.5

def player(now):
    pygame.mixer.music.load(os.path.join(path, lib[now]))
    pygame.mixer.music.play()
    
player(now)

while playing:
    screen.fill((0, 0, 0))

    t1 = font.render('Space: Pause/Play', True, (255, 255, 0))
    t2 = font.render('Left arrow: Previous song', True, (255, 255, 0))
    t3 = font.render('Right arrow: Next song', True, (255, 255, 0))

    screen.blit(t1, (30, 30))
    screen.blit(t2, (30, 70))
    screen.blit(t3, (30, 110))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        
        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_SPACE:    #pause/play
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_LEFT:    #previous song
                now -= 1
                if now < 0:
                    now = len(lib) - 1
                player(now)
            if event.key == pygame.K_RIGHT:     #next song
                now += 1
                if now >= len(lib):
                    now = 0
                player(now)

    pygame.display.flip()