import pygame
from pygame.locals import *

pygame.init()   #initialize module

white = (255, 255, 255)   #colors
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screen = pygame.display.set_mode((600, 450))    #set screen dimensions
pygame.display.set_caption("Paint")    #set caption of screen

erasing = False   #flags to keep checked if mode is drawing/erasing
drawing = False
color = black   #initial drawing color
radius = 12   #initial fixed radius of brush

mode = "line"  #initial drawing mode (or circle/rectangle)
start_pos = None   #starting position of brush

screen.fill(white)   #fill screen with white

running = True
while running:   #game loop
    
    for e in pygame.event.get():   
        if e.type == QUIT:   #quit the game if it is closed
            running = False
            
        elif e.type == MOUSEBUTTONDOWN:   #if mouse button ispressed start drawing
            drawing = True
            start_pos = e.pos   #start from mouse position
            
        elif e.type == MOUSEBUTTONUP:   #if button is released
            end_pos = e.pos   #stop drawing
            
            if mode == "rectangle":   #if mode is rectangle, end position is end corner
                rect_width = abs(end_pos[0] - start_pos[0])   #width based on mouse position
                rect_height = abs(end_pos[1] - start_pos[1])   #height
                pygame.draw.rect(screen, color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), rect_width, rect_height), 12)   #draw rectangle of given radius
           
            elif mode == "circle":   #if mode is circle calculate the radius basen on mouse position
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)   #math formula
                pygame.draw.circle(screen, color, start_pos, radius, 12)   #draw the circle of given radius
            
            drawing = False   #stop drawing process
        
        elif e.type == KEYDOWN:   #if key is pressed
            if e.key == K_r:    #red color mode
                color = red
            elif e.key == K_g:  #green color mode
                color = green
            elif e.key == K_b:   #blue color mode
                color = blue
            elif e.key == K_e:   #erasing mode
                erasing = not erasing   #press once to turn on and twice to turn off
            elif e.key == K_l:
                mode = "line"   #switch back to line drawing mode
            elif e.key == K_t:
                mode = "rectangle"   #rectangle drawing mode
            elif e.key == K_o:
                mode = "circle"   #circle drawing mode

    if drawing and mode == "line":   #mode for drawing and erasing lines
        mouse_pos = pygame.mouse.get_pos()   #position of the mouse
        if erasing:   #draw white circles brush when erasing
            pygame.draw.circle(screen, white, mouse_pos, radius)  
        else:  #and colored when drawing
            pygame.draw.circle(screen, color, mouse_pos, radius)  

    pygame.display.update()  #update the screen

pygame.quit()   #quit the game
