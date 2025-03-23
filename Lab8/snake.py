import pygame
import time
import random

snake_speed = 10    #initial speed of snake

window_x = 720      #window size
window_y = 480

black = pygame.Color(0, 0, 0)      #colors
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()   #initialize pygame modules
pygame.display.set_caption('Snake')   #set caption of the game screen
game_window = pygame.display.set_mode((window_x, window_y))  #set a display of given dimensions
fps = pygame.time.Clock()   #frames per second
snake_position = [100, 50]   #initial position of snake

snake_body = [[100, 50],     #forming initial body(4 blocks of 10 pixels)
            [90, 50],
            [80, 50],
            [70, 50]
            ]
           
#random spawning position of fruit
fruit_position = [random.randrange(1, (window_x//10)) * 10,    #10 pixel grid, so snake's body could touch it
                  random.randrange(1, (window_y//10)) * 10]

fruit_spawn = True  #flag to track fruit presence
direction = 'RIGHT'  #initial direction of movement
change_to = direction  #next direction
score = 0     #score counter
level = 0     #added level counter
     
def show_score(choice, color, font, size):    #function to show the score and level
 
    score_font = pygame.font.SysFont(font, size)  #font object specified later
   
    score_surface = score_font.render('Score : ' + str(score), True, color)   #render score text as a surface
    score_level = score_font.render('Level: ' + str(level), True, green)     #render level counter text 
   
    game_window.blit(score_surface, (0, 0))  #dispa score and level counter at the left top
    game_window.blit(score_level, (0, 20))
   
def game_over():   #function of what to write on the screen after loss
 
    my_font = pygame.font.SysFont('times new roman', 50)  #font object of times new roman font and 50 size

    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)   #render gameover text(fina score and level)
    game_over_level = my_font.render('Your level is : ' + str(level), True, red)

    game_window.blit(game_over_surface, (150, 250))   #display the text
    game_window.blit(game_over_level, (150, 190))
    pygame.display.update()   #update the screen

    time.sleep(2)   #2 seconds pause

    pygame.quit()   #quit the game

    quit()   #exit the program
   
while True:   #game loop
   
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:   #if the certain key is pressed face a certain direction
            if event.key == pygame.K_UP:    
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
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

    #move for 10 pixels according ot the direction
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))   #increase the size of snake's body and maintain the lsit of all blocks
                                                 #by adding a new head block in the beginning   
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:  #if snake touches the fruit
        score += 10   #score up
        fruit_spawn = False   #remove the fruit
        if score % 30 == 0:    #level up after each 30 points
          level += 1
          snake_speed += 3     #increase speed after passing the level
    else:  #if no collision, remove last block, so it remains previous size
        snake_body.pop() 
       
    if not fruit_spawn:        #spawn a new fruit after preious was eaten
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                          random.randrange(1, (window_y//10)) * 10]

   
    fruit_spawn = True  
    game_window.fill(black)    #fill the screen with black 
   
    for pos in snake_body:  #for each block in snake's body
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))  #draw the blocks green
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))   #draw the fruit

    if snake_position[0] < 0 or snake_position[0] > window_x-10:   #checking for collision with window
        game_over()  #if it does collide, call gameover function
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()

    for block in snake_body[1:]:  #if snake touches itself also gameover
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)   #display the score on the screen

    pygame.display.update()  #update the screen

    fps.tick(snake_speed)  #framse per second basen on snake's speed