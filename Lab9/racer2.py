import pygame as pg
import sys
import random
import time
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT


pg.init()   #initialize pg modules

fps = 60        #frames per second
clock = pg.time.Clock()

black = (0, 0, 0)       #colors
white = (255, 255, 255)
red = (255, 0, 0)

width = 400     #display dimensions
height = 600
v = 1.5      #initial speed of the enemy(red car)
score = 0    #score after passing the enemy 
coin_score = 0    #number of collected coins

FONT = pg.font.SysFont('Times New Roman', 60)    #fonts used for rendering text (large)
font = pg.font.SysFont('Times New Roman', 20)    #(small)
gameover = FONT.render('Game Over', True, black)     #render text as a surface when called

image = pg.image.load(r'C://Users/User/pp2_2-1/Lab8/background.png')    #load road image
screen = pg.display.set_mode((width, height))    #set a game screen of given dimensions
screen.fill(white)    #color the screen white
pg.display.set_caption('Racer game')    #caption of the game screen

class enemy(pg.sprite.Sprite):    #class of enemy(red car)
    def __init__(self):       #initialize the class
        super().__init__()    #inherit from the parent sprite class
        self.image = pg.image.load(r'C://Users/User/pp2_2-1/Lab8/Enemy.png')   #load image for red car
        self.rect = self.image.get_rect()     #create a rectangle covering car surface
        self.rect.center = (random.randint(40, width - 40), 0)   #random position of enemy car horizontally at the top
       
    def move(self):
        global score     #global scope of score variable
        self.rect.move_ip(0, v)   #move car in place vertically by v
        if (self.rect.top > height):
            score += 1   #if red car reaches bottom plus score
            self.rect.top = 0    #get car back to top
            self.rect.center = (random.randint(40, width- 40), 0)   #at a random position horizontally
           
class player(pg.sprite.Sprite):   #player class(blue car)
    def __init__(self):   #initializing function
        super().__init__()
        self.image = pg.image.load(r'C://Users/User/pp2_2-1/Lab8/Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)   #initial position of the blue car
       
    def move(self):    #function of movement
        keys = pg.key.get_pressed()    #for events when keys are pressed
        if keys[K_UP] and self.rect.top > 0:  #within the screen boundaries
            self.rect.move_ip(0, -4)   #car moves up by 4
        if keys[K_DOWN] and self.rect.bottom < height:  
            self.rect.move_ip(0, 4)    #down by 4
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-4, 0)   #left by 4
        if keys[K_RIGHT] and self.rect.right < width:
            self.rect.move_ip(4, 0)    #right by 4
           
class coin(pg.sprite.Sprite):    #collecting coins class
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(r'C://Users/User/pp2_2-1/Lab9/coin.png')
        self.image = pg.transform.scale(self.image, (30, 30))    #scale the image of coin to a certain size
        self.rect = self.image.get_rect()
       
        self.rect.center = (random.randint(40, width - 40), random.randint(80, height - 80))  #random position of spawning coins not to close to edges
   
    def respawn(self):   #respawn the coin when collided with
        size1 = (20, 20)
        size2 = (35, 35)
        size3 = (50, 50)
        size = random.choice([size1, size2, size3])
        self.image = pg.transform.scale(self.image, size)
        self.rect.center = (random.randint(40, width - 40), random.randint(80, height - 80))
               
p1 = player()   #creating objects
e1 = enemy()
c = coin()

enemies = pg.sprite.Group()  #group to store certain class sprites
enemies.add(e1)   #add objects to the group
coins = pg.sprite.Group()
coins.add(c)
all = pg.sprite.Group()   #group to store all sprites
all.add(e1,p1, c)   #add player, enemy and coin objects



running = True   #flag to keep gam erunning unless something happens
while running:    #game loop
    for e in pg.event.get():
       
        if e.type == QUIT:   #if event is to close the game
            running = False  #flag is unchecked and loop stops closing the game
   
    screen.blit(image, (0, 0))   #set a background of road image
    points = font.render(str(score), True, black)   #render score text
    screen.blit(points, (10, 10))   #display the score text on the game screen(left top)
    coin_points = font.render(str(coin_score), True, black)
    screen.blit(coin_points, (370, 10))   #display coin score a tthe right top of the screen
   
    for entity in all:    #for each object in all sprites group
        screen.blit(entity.image, entity.rect)   #display objects on the screen
        p1.move()   #update posiions of p1 and e1
        e1.move()
       
    if pg.sprite.spritecollideany(p1, coins):   #if p1 touches the coin
        coin_score += 1   #collected coins score up
        if score % 3 == 0:
          v += 0.5
        c.respawn()   #move the coin to a new random position
       
    if pg.sprite.spritecollideany(p1, enemies):    #if p1 collides with enemy car
        time.sleep(0.5)  #short pause before enfing the game
        screen.fill(red)     #display a red screen
        screen.blit(gameover, (55, 250))   #with a 'gameover' text on it
       
        pg.display.update()    #update the screen
       
        for entity in all:   #objects of all sprites group
            entity.kill()    #kill(delete) all objects(p1,e1,coin)
        time.sleep(2)   #2 seconds pause
        pg.quit()   #quits the game
        sys.exit()      #exits the program
       
    pg.display.update()   #update the screen
    clock.tick(fps)  #fps set at 60