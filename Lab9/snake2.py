import pygame as pg
import time
import random
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT

snake_speed = 10    #initial speed of snake

window_x = 720      #window size
window_y = 480

black = pg.Color(0, 0, 0)      #colors
white = pg.Color(255, 255, 255)
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
blue = pg.Color(0, 0, 255)

pg.init()   #initialize pg modules
pg.display.set_caption('Snake')   #set caption of the game screen
game_window = pg.display.set_mode((window_x, window_y))  #set a display of given dimensions
fps = pg.time.Clock()   #frames per second
snake_pos = [100, 50]   #initial position of snake

snake_body = [[100, 50],     #forming initial body(4 blocks of 10 pixels)
            [90, 50],
            [80, 50],
            [70, 50]
            ]
def fruit():

    while True:
        fruit_size = random.choice([10, 20, 30])
        fruit_pos = [random.randrange(1, (window_x//10)) * 10,    #10 pixel grid, so snake's body could touch it
                    random.randrange(1, (window_y//10)) * 10]
        return fruit_pos, fruit_size, time.time()
        
fruit_pos, fruit_size, spawn_time = fruit()
fruit_spawn = True  #flag to track fruit presence
direction = 'RIGHT'  #initial direction of movement
change_to = direction  #next direction
score = 0     #score counter
level = 0     #added level counter
     
def show_score(choice, color, font, size):    #function to show the score and level
 
    score_font = pg.font.SysFont(font, size)  #font object specified later
   
    score_surface = score_font.render('Score : ' + str(score), True, color)   #render score text as a surface
    score_level = score_font.render('Level: ' + str(level), True, green)     #render level counter text 
   
    game_window.blit(score_surface, (0, 0))  #dispa score and level counter at the left top
    game_window.blit(score_level, (0, 20))
   
def game_over():   #function of what to write on the screen after loss
 
    my_font = pg.font.SysFont('times new roman', 50)  #font object of times new roman font and 50 size

    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)   #render gameover text(fina score and level)
    game_over_level = my_font.render('Your level is : ' + str(level), True, red)

    game_window.blit(game_over_surface, (150, 250))   #display the text
    game_window.blit(game_over_level, (150, 190))
    pg.display.update()   #update the screen

    time.sleep(2)   #2 seconds pause

    pg.quit()   #quit the game

    quit()   #exit the program
   
while True:   #game loop

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
        if e.type == KEYDOWN:   #if the certain key is pressed face a certain direction
            if e.key == K_UP:    
                change_to = 'UP'
            if e.key == K_DOWN:
                change_to = 'DOWN'
            if e.key == K_LEFT:
                change_to = 'LEFT'
            if e.key == K_RIGHT:
                change_to = 'RIGHT'

    #when 2 keys are pressed simultaneously, choose one
    if change_to == 'UP' and direction != 'DOWN':    #so it does not move in opposite directions
        direction = 'UP'                
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    #move for 10 pixels according to the direction
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))   #increase the size of snake's body and maintain the lsit of all blocks
                                                 #by adding a new head block in the beginning   
    if (snake_pos[0] in range(fruit_pos[0], fruit_pos[0] + fruit_size) and     #check if snake touches fruit
        snake_pos[1] in range(fruit_pos[1], fruit_pos[1] + fruit_size)):
        score += 10   #score up
        fruit_spawn = False   #remove the fruit
        if score % 30 == 0:    #level up after each 30 points
            level += 1
            snake_speed += 3     #increase speed after passing the level
    else:  #if no collision, remove last block, so it remains previous size
        snake_body.pop() 
       
    if time.time() - spawn_time > 5:    #if snake doesn't touch fruit in 5 seconds remove it
        fruit_spawn = False

    if not fruit_spawn:        #spawn a new fruit after preious was eaten or disappeared
        fruit_pos, fruit_size, spawn_time = fruit()
        fruit_spawn = True
    

    game_window.fill(black)    #fill the screen with black 
   
    for pos in snake_body:  #for each block in snake's body
        pg.draw.rect(game_window, green,
                         pg.Rect(pos[0], pos[1], 10, 10))  #draw the blocks green
    pg.draw.rect(game_window, white, pg.Rect(
        fruit_pos[0], fruit_pos[1], fruit_size, fruit_size))   #draw the fruit

    if snake_pos[0] < 0 or snake_pos[0] > window_x - 10:   #checking for collision with window
        game_over()  #if it does collide, call gameover function
    if snake_pos[1] < 0 or snake_pos[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:  #if snake touches itself also gameover
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)   #display the score on the screen

    pg.display.update()  #update the screen

    fps.tick(snake_speed)  #frames per second basen on snake's speed