import pygame
from pygame.locals import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    clock = pygame.time.Clock()
    
    r = 15
    mode = 'blue'
    points = []
    
    
    drawing_rect = False
    drawing_circle = False
    erasing = False
    drawing = False

    
    rect_start = (0, 0)
    rect_end = (0, 0)
    circle_center = (0, 0)
    circle_r = 0
    
    last_pos = (0, 0)

    
    
    while True:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        alt = keys[K_LALT] or keys[K_RALT]
        ctrl = keys[K_LCTRL] or keys[K_RCTRL]
        
        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN:
                if e.key == K_w and ctrl:
                    return
                if e.key == K_F4 and alt:
                    return
                if e.key == K_ESCAPE:
                    return
                
                if e.key == K_r:
                    mode = 'red'
                elif e.key == K_g:
                    mode = 'green'
                elif e.key == K_b:
                    mode = 'blue'
                elif e.key == K_t:
                    drawing_rect = True
                    rect_start = pygame.mouse.get_pos()
                elif e.key == K_c:
                    drawing_circle = True
                    circle_center = pygame.mouse.get_pos()

                elif e.key == K_e:
                    erasing = not erasing

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    drawing = True
            
                
            if e.type == MOUSEMOTION:
                position = e.pos
                if drawing:
                    points += [position]
                    points = points[-256:]
                last_pos = e.pos
                if erasing:
                    pygame.draw.circle(screen, (0, 0, 0), position, r * 2)
     
                    
                    
            if e.type == MOUSEBUTTONUP:
                drawing = False
                drawing_circle = False
                drawing_rect = False

        
        if not drawing_circle and not drawing_rect and not erasing:
            for i in range(len(points) - 1):
                drawline(screen, i, points[i], points[i + 1], r, mode)
                    
        if drawing_rect:
            rect_end= pygame.mouse.get_pos()
            drawrect(screen, rect_start, rect_end, mode, r)
        if drawing_circle:
            pos = pygame.mouse.get_pos()
            circle_r = int(((circle_center[0] - pos[0]) ** 2 + (circle_center[1] - pos[1]) ** 2)** 0.5)
            drawcircle(screen, circle_center, circle_r, mode, r) 
        
        pygame.display.flip()
        clock.tick(60)

    
def drawline(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)    
        
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iter = max(abs(dx), abs(dy))
    
    for i in range(iter):
        progress = 1.0 * i / iter
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)            

def drawrect(screen, start, end, color_mode, r):
    if color_mode == 'blue':
        color = (0, 0, 255)
    elif color_mode == 'red':
        color = (255, 0, 0)
    elif color_mode == 'green':
        color = (0, 255, 0)    
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    dw = abs(end[0] - start[0])
    dh = abs(end[1] - start[1])
    rect = pygame.Rect(x, y, dw, dh)
    pygame.draw.rect(screen, color, rect, r)

def drawcircle(screen, center, radius, color_mode, r):
    if color_mode == 'blue':
        color = (0, 0, 255)
    elif color_mode == 'red':
        color = (255, 0, 0)
    elif color_mode == 'green':
        color = (0, 255, 0)    
    pygame.draw.circle(screen, color, center, radius, r)

main()