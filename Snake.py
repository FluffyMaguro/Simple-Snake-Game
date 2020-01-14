import pygame
import sys
import random

### VARIABLES
WIDTH = 800
HEIGHT = 600
TILE = 15

bg_color = (0,0,0)
snake_color = (255,255,255)
tile_color = (255,150,0)
score = 0
speed = 1
game_over = False

direction = 'left'
fps = 8
counter = 0

### INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('The game of Snake')
icon = pygame.image.load('Snake.png')
pygame.display.set_icon(icon)

bg_image = pygame.image.load('BG.png')
screen.blit(bg_image,(0,0))

clock = pygame.time.Clock()
gameOverFont = pygame.font.SysFont("verdana",45)
gameOverFont2 = pygame.font.SysFont("verdana",14)
scoreFont = pygame.font.SysFont("verdana",16)

snake = list() #list containing all points (top-left tile coordinates)
spawned_tiles = list()

def saveScore():
    try:
        f = open('BestScore.txt','r')
        best_score = int(f.read())
        f.close()
    except:
        best_score = 0

    if score > best_score:
        f = open('BestScore.txt','w')
        f.write(str(score))
        f.close()

def crashCheck():
    if snake[0][0] < 0 or snake[0][0]*TILE >= WIDTH or snake[0][1] < 0 or snake[0][1]*TILE >= HEIGHT:
        return True
    if snake[0] in snake[1:]:
        return True
    return False

def resetGame():
    global spawned_tiles
    global snake
    global score
    global game_over

    game_over = False
    score = 0
    snake = [[20,10],[20+1,10],[20+2,10],[20+3,10]]
    spawned_tiles = []
    for a in range(0,10):
        spawnTile()
    
def spawnTile():
    #spawn tile randomly. It cannot be inside the snake, other spawned tiles, and it cannot be infront of him
    while True:
        test_tile = [random.randint(0,int(WIDTH/TILE) - 1),random.randint(0,int(HEIGHT/TILE) - 1)]      
        if not(test_tile in spawned_tiles) and not(test_tile in snake) and not(test_tile in predictSnake(4)):
            spawned_tiles.append(test_tile)
            break

def predictSnake(ahead):
    #predict new ahead-times tiles where the snake is going
    predicted = list()
    new_tile = snake[0].copy()
    for a in range(0,ahead): #4x predict
        if direction == 'left':
            new_tile[0] -= speed
        elif direction == 'right':
            new_tile[0] += speed  
        elif direction == 'up':
            new_tile[1] -= speed    
        elif direction == 'down':
            new_tile[1] += speed
        next_tile = new_tile.copy()
        predicted.append(next_tile)

    return predicted

def drawSnake(snake):
    for point in snake:
        pygame.draw.rect(screen, snake_color,(point[0]*TILE,point[1]*TILE,TILE,TILE))

def drawSpawnedTiles(spawned_tiles):
    for point in spawned_tiles:
        pygame.draw.rect(screen, tile_color,(point[0]*TILE,point[1]*TILE,TILE,TILE))

def moveSnake(snake, direction):  
    global score  

    tile_ahead = predictSnake(1)[0] #eating
    if tile_ahead in spawned_tiles:
        score += 1
        spawned_tiles.remove(tile_ahead)
        snake.insert(0,tile_ahead)
    else:                           #not eating
        if len(snake) > 1:
            last_tile = snake.pop()
            last_tile[0] = snake[0][0]
            last_tile[1] = snake[0][1]
        else:
            last_tile = [0,0]
            last_tile[0] = snake[0][0]
            last_tile[1] = snake[0][1]
            snake.pop()

        if direction == 'left':
            last_tile[0] -= speed
        elif direction == 'right':
            last_tile[0] += speed  
        elif direction == 'up':
            last_tile[1] -= speed    
        elif direction == 'down':
            last_tile[1] += speed

        snake.insert(0,last_tile)
    return snake

### START
resetGame()
while True:   
    for event in pygame.event.get():
        #exit
        if event.type == pygame.QUIT:
            sys.exit()
        #control       
        if event.type == pygame.KEYDOWN:
            # print(event.key)
            if event.key == pygame.K_LEFT and direction != 'right':
                direction = 'left'
            elif event.key == pygame.K_RIGHT and direction != 'left':
                direction = 'right'
            elif event.key == pygame.K_UP and direction != 'down':
                direction = 'up'
            elif event.key == pygame.K_DOWN and direction != 'up':
                direction = 'down'
            elif event.key == pygame.K_SPACE and game_over == True:
                print('reset')
                resetGame()

    screen.blit(bg_image,(0,0)) 

    if game_over == False: 
        snake = moveSnake(snake, direction)
        counter += 1

        if counter % (3*fps) == 0:
            spawnTile()

        if crashCheck() == True:
            game_over = True
        saveScore()

    score_label = scoreFont.render('Score: ' + str(score), 1, (255,255,255))
    screen.blit(score_label, (WIDTH - 100, 0))
    
    drawSnake(snake)
    drawSpawnedTiles(spawned_tiles)

    if game_over == True:
        pygame.draw.rect(screen, (40,40,40),(WIDTH/2 - 145, HEIGHT/2 - 50,305,90))
        label = gameOverFont.render('Game over!', 1, (255,255,255))
        screen.blit(label, (WIDTH/2 - 120, HEIGHT/2 - 50))
        label = gameOverFont2.render('(press space to reset)', 1, (255,255,255))
        screen.blit(label, (WIDTH/2 - 75, HEIGHT/2 + 5))

    clock.tick(fps)
    pygame.display.update()