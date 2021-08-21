import pygame
from pygame import mixer
import random

pygame.init()
mixer.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Mission: Kill Typescript")
icon = pygame.image.load("javascript.png")
pygame.display.set_icon(icon)

# Player Image
playerImg = pygame.image.load("javascript.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy Image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append( pygame.image.load("typescript.png") )
    enemyX.append( random.randint(1,800) )
    enemyY.append(0)
    enemyX_change.append( 0.3 )
    enemyY_change.append( 0.1 ) 

# Bullet Image
bulletImg = pygame.image.load("javascript.png")
bulletX = 0
bulletY = 0
bulletX_change = 2
bulletY_change = 2
bullet_state = "READY!"

# Score
score_value = 0

font = pygame.font.Font('startFont.ttf', 28)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value) , True, (255,255,34))
    screen.blit(score, (x, y))
def player(x,y):
    screen.blit(playerImg, (x , y))
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "FIRE!"
    screen.blit(bulletImg, (x ,y))
def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x2 > w1 + x1 or x1 > w2 + x2 or y2 > h1 + y1 or y1 > h2 + y2:
        return False
    else:
        return True
def game_over():
    score = font.render("Game Over lol", True, (255,255,34))
    screen.blit(score, (300, 300))
playing = False
def intro_game():
    global playing
    intro_font = pygame.font.Font('lowbatt.ttf', 60)
    intro_font2 = pygame.font.Font('intro2.otf', 60)
    intro_text = intro_font.render("Mission: ", True, (255,255,34))
    intro_text2 = intro_font2.render("KILL TYPESCRIPT", True, (255,255,34))
    screen.blit(intro_text, (200, 100))
    screen.blit(intro_text2, (200, 200))


music_played = False
runnning = True
intro = True
while runnning:
    screen.fill((50,149,255))
    if playing == False:
        playing = True 
        mixer.Sound("./audio/ambi.wav").play()

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            runnning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                if intro == True:
                    intro = False
                    print("Game is Started...")
                    print("press Y on your keyboard to play game...")
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1  
            if event.key == pygame.K_SPACE:
                if bullet_state == "READY!":
                    bullet_state = "FIRE!"
                    random_shoot_list = ["./audio/sound.wav", "./audio/sound2.wav" , "./audio/shoot3.wav"]
                    random_shoot_music = random.choice(random_shoot_list)
                    mixer.Sound(random_shoot_music).play()
                    bulletX = playerX
                    bulletY = playerY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_y:
                playerX_change = 0 
    if intro == False:
        playerX += playerX_change  

        if playerX <=0:
            playerX = 0
        elif playerX >=800 - 64:
            playerX = 800 - 64
        if score_value < 0:
            game_over()
            if music_played == False:
                mixer.Sound("./audio/gameover.wav").play()
                music_played = True
            num_of_enemies = 0

            
        for i in range(num_of_enemies):

            # Game over

            if enemyY[i] > 600:
                for j in range(num_of_enemies):
                    num_of_enemies = 0
                    game_over()
                    break
            if enemyX[i]<=0:
                enemyX_change[i] = 0.3
            elif enemyX[i] >=800 - 64:
                enemyX_change[i] = -0.1
            if enemyY[i]<=0:
                enemyY_change[i] = 0.1
            elif enemyY[i] >=600 - 64:
                mixer.Sound("./audio/onedge_hit.wav").play()
                score_value -= 1
                enemyY[i] = 0
            enemyY[i] += enemyY_change[i]
            enemyX[i] += enemyX_change[i]
            if check_collision(playerX, playerY, 64, 64, enemyX[i], enemyY[i], 64, 64):
                game_over()
                if music_played == False:
                    mixer.Sound("./audio/gameover.wav").play()
                    music_played = True
                break
            elif check_collision(bulletX, bulletY, 64, 64, enemyX[i], enemyY[i], 64, 64):
                bulletY = 0
                bulletX = 0
                bullet_state = "READY!"
                score_value += 1
                enemyX[i] = random.randint(0,800)
                enemyY[i] = random.randint(50,150)
            enemy(enemyX[i], enemyY[i], i)

        # Bullet Move
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "READY!"

        if bullet_state == "FIRE!":
            bulletY -= bulletY_change
            fire_bullet(bulletX, bulletY)

        player(playerX,playerY)
        show_score(textX,textY)
    else:
        intro_game()
    pygame.display.update()
