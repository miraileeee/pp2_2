import pygame as pg
import psycopg2
import time
import random
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT

conn = psycopg2.connect(host='localhost', database='suppliers', user='postgres', password='fhbufnj444')
cur = conn.cursor()

snake_speed = 10   

window_x = 720      
window_y = 480

black = pg.Color(0, 0, 0)     
white = pg.Color(255, 255, 255)
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
blue = pg.Color(0, 0, 255)

pg.init()  
pg.display.set_caption('Snake')  
game_window = pg.display.set_mode((window_x, window_y))  
fps = pg.time.Clock()   
snake_pos = [100, 50]  

snake_body = [[100, 50],     
            [90, 50],
            [80, 50],
            [70, 50]
            ]
def fruit():

    while True:
        fruit_size = random.choice([10, 20, 30])
        fruit_pos = [random.randrange(1, (window_x//10)) * 10,    
                    random.randrange(1, (window_y//10)) * 10]
        return fruit_pos, fruit_size, time.time()
        
fruit_pos, fruit_size, spawn_time = fruit()
fruit_spawn = True 
direction = 'RIGHT'  
change_to = direction 
score = 0   
level = 0     

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                user_name VARCHAR(50) NOT NULL,
                score INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1)
        """)
    conn.commit()

def edit_table(user_name):
    cur.execute("SELECT id, level, score FROM users where user_name = %s", (user_name,))
    user = cur.fetchone()
    if user:
        id, level, score = user
        print('User:', user_name, '. Level:', level, '. Score:', score)
    else:
        cur.execute(
            "INSERT INTO users (user_name, level, score) VALUES (%s, %s, %s)", (user_name, 1, 0)
        )
        conn.commit()
        cur.execute("SELECT id FROM users WHERE user_name = %s", (user_name,))
        id = cur.fetchone()[0]
        level = 1
        score = 0
        print('New user: ', user_name, '. Level: 1. Score: 0.')
    
    return id, level, score

def pause(id, level, score):
    cur.execute("UPDATE users SET level = %s, score = %s WHERE id = %s", (level, score, id))
    conn.commit()
    print('Game paused')

     
def show_score(choice, color, font, size):  
 
    score_font = pg.font.SysFont(font, size)  
   
    score_surface = score_font.render('Score : ' + str(score), True, color)   
    score_level = score_font.render('Level: ' + str(level), True, green)     
   
    game_window.blit(score_surface, (0, 0))  
    game_window.blit(score_level, (0, 20))
   
def game_over():   
 
    my_font = pg.font.SysFont('times new roman', 50) 

    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)  
    game_over_level = my_font.render('Your level is : ' + str(level), True, red)

    game_window.blit(game_over_surface, (150, 250)) 
    game_window.blit(game_over_level, (150, 190))
    pg.display.update()  

    cur.execute("UPDATE users SET level = %s, score = %s WHERE id = %s", (level, score, id))
    conn.commit()

    time.sleep(2)   

    pg.quit()  

    quit()   

if __name__ == "__main__":
    create_table()
    user_name = input('Enter the username: ')
    id, level, score = edit_table(user_name)
    paused = False

    while True:  
    
        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
            if e.type == KEYDOWN:   
                if e.key == K_UP:    
                    change_to = 'UP'
                if e.key == K_DOWN:
                    change_to = 'DOWN'
                if e.key == K_LEFT:
                    change_to = 'LEFT'
                if e.key == K_RIGHT:
                    change_to = 'RIGHT'
                if e.key == pg.K_p:
                    pause(id, level, score)
                    paused = True
        
        while paused:
            for e in pg.event.get():
                if e.type == QUIT:
                    pg.quit()
                    quit()
                if e.type == KEYDOWN:
                    if e.key == pg.K_p:  
                        paused = False
               
                   

        
        if change_to == 'UP' and direction != 'DOWN':   
            direction = 'UP'                
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        
    
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))  
        if (snake_pos[0] in range(fruit_pos[0], fruit_pos[0] + fruit_size) and   
            snake_pos[1] in range(fruit_pos[1], fruit_pos[1] + fruit_size)):
            score += 10   
            fruit_spawn = False  
            if score % 30 == 0:   
                level += 1
                snake_speed += 3    
        else:  
            snake_body.pop() 
        
        if time.time() - spawn_time > 5:   
            fruit_spawn = False

        if not fruit_spawn:        
            fruit_pos, fruit_size, spawn_time = fruit()
            fruit_spawn = True
        

        game_window.fill(black)    
    
        for pos in snake_body: 
            pg.draw.rect(game_window, green,
                            pg.Rect(pos[0], pos[1], 10, 10))  
        pg.draw.rect(game_window, white, pg.Rect(
            fruit_pos[0], fruit_pos[1], fruit_size, fruit_size))  

        if snake_pos[0] < 0 or snake_pos[0] > window_x - 10:   
            game_over()  
        if snake_pos[1] < 0 or snake_pos[1] > window_y - 10:
            game_over()

        for block in snake_body[1:]:  
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score(1, white, 'times new roman', 20)  

        pg.display.update() 

        fps.tick(snake_speed) 