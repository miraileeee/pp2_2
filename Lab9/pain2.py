import pygame as pg
import math
from pygame.locals import *

pg.init()   #initialize module

white = (255, 255, 255)   #colors
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

screen = pg.display.set_mode((600, 450))    #set screen dimensions
pg.display.set_caption("Paint")    #set caption of screen

erasing = False   #flags to keep checked if mode is drawing/erasing
drawing = False
color = black   #initial drawing color
radius = 12   #initial fixed radius of brush

mode = "line"  #initial drawing mode (or circle/rectangle)
start_pos = None   #starting position of brush

screen.fill(white)   #fill screen with white

running = True
while running:   #game loop
    
    for e in pg.event.get():   
        if e.type == QUIT:   #quit the game if it is closed
            running = False
            
        elif e.type == MOUSEBUTTONDOWN:   #if mouse button ispressed start drawing
            drawing = True
            start_pos = e.pos   #start from mouse position
            
        elif e.type == MOUSEBUTTONUP:   #if button is released
            end_pos = e.pos   #stop drawing
            
            if mode == 'rectangle':   #if mode is rectangle, end position is end corner
                w = abs(end_pos[0] - start_pos[0])   #width based on mouse position
                h = abs(end_pos[1] - start_pos[1])   #height
                pg.draw.rect(screen, color, (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), w, h), 5)   #draw rectangle of given radius
           
            elif mode == 'circle':   #if mode is circle calculate the radius based on mouse position
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)   #math formula
                pg.draw.circle(screen, color, start_pos, radius, 5)   #draw the circle of given radius
            
            elif mode == 'square':
                side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))   #takes the smaller difference of points
                pg.draw.rect(screen, color, (start_pos[0], start_pos[1], side, side), 5)
                
            elif mode == 'right_t':
                pg.draw.polygon(screen, color, [start_pos, (start_pos[0], end_pos[1]), end_pos], 5)     #draw a triangle basen on firstt and last points and second that keeps x of 1st and y of 2nd point

            elif mode == 'equi_t':
                x1, y1 = start_pos   #center point coordinates
                x2, y2 = end_pos
                side = abs(y2 - y1)   #half the side
                h = (math.sqrt(3) / 2) * side    #height
                top = (x1, y1 - h)     #top vertex  start y + half height y up
                left = (x1 - side, y1 + h)      #start x - half side x, start y + half height y down
                right = (x1 + side, y1 + h)     # start x + half side x, start y + half height y down
                 
                pg.draw.polygon(screen, color, [top, left, right], 5)

            elif mode == 'rhombus':
                x1, y1 = start_pos      #center
                x2, y2 = end_pos
                w = abs(x2 - x1)        #width
                h = abs(y2 - y1)        #height
                top = (x1, y1 - h)      #start x, y half height up
                bottom = (x1, y1 + h)       #start x, y half height down
                left = (x1 - w, y1)     #start x left for half width, start y
                right = (x1 + w, y1)    #start x right for half width, start y

                pg.draw.polygon(screen, color, [top, right, bottom, left], 5)

            drawing = False   #stop drawing process
        
        elif e.type == KEYDOWN:     #if key is pressed
            if e.key == K_1:        #red color mode
                color = red
            elif e.key == K_2:      #green color mode
                color = green
            elif e.key == K_3:      #blue color mode
                color = blue
            elif e.key == K_e:      #erasing mode
                erasing = not erasing   #press once to turn on and twice to turn off
            elif e.key == K_l:
                mode = "line"       #switch back to line drawing mode
            elif e.key == K_r:
                mode = "rectangle"  #rectangle drawing mode
            elif e.key == K_c:
                mode = "circle"     #circle drawing mode
            elif e.key == K_t:
                mode = 'right_t'    #right triangle mode
            elif e.key == K_q:
                mode = 'equi_t'     #equilateral triangle mode
            elif e.key == K_s:
                mode = 'square'     #square mode
            elif e.key == K_m:
                mode = 'rhombus'    #rhombus mode

    if drawing and mode == "line":   #mode for drawing and erasing lines
        mouse_pos = pg.mouse.get_pos()   #position of the mouse
        if erasing:   #draw white circles brush when erasing
            pg.draw.circle(screen, white, mouse_pos, radius)  
        else:  #and colored when drawing
            pg.draw.circle(screen, color, mouse_pos, radius)  

    pg.display.update()  #update the screen

pg.quit()   #quit the game
