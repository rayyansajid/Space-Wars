import pygame
import random
import math

pygame.init()

displayWindow = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Wars")

icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("player.png")

bckgrnd = pygame.image.load("background.png")

bulletImg = pygame.image.load("bullet.png")

font = pygame.font.Font("freesansbold.ttf", 32)

def displayscore(x,y,score_value):
    score = font.render("Score: "+str(score_value), True, (0,200,0),(15,0,0))
    displayWindow.blit(score,(x,y))

def gameover(x,y,score_value):
    text1 = font.render("GAME OVER", True, (0,200,0),(15,0,0))
    text2 = font.render(" SCORE: "+str(score_value), True, (0,200,0),(15,0,0))
    displaystart("Press ENTER to play again!!",(0,200,0),180,380)
    displayWindow.blit(text1,(x,y))  
    displayWindow.blit(text2,(x,y+80)) 
    with open ("highest_score.txt","r") as f:
        maxy = f.read()
        if score_value > int(maxy):
            with open ("highest_score.txt","w") as k:
                maxy = score_value
                k.write(str(score_value))
    with open ("highest_score.txt","r") as f:
        scores= f.read()          
    score = font.render("Highest Score: "+str(scores), True, (0,200,0),(15,0,0))
    displayWindow.blit(score,(275,300))
    pygame.display.update()  

def player(x, y):
    displayWindow.blit(playerImg,(x,y))

def enemy(enemyImg,x, y,i):                                 
    displayWindow.blit(enemyImg[i],(x,y))

def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    displayWindow.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2))+(math.pow((enemyY - bulletY),2)))
    if distance <= 24:
        return True
    return False

def displaystart(text,colour,x,y):
        start=font.render(text,True,colour)
        displayWindow.blit(start,(x,y))

def bubble(Array):
    n = len(Array)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if Array[j] > Array[j + 1]:
                tmp = Array[j]
                Array[j] = Array[j + 1]
                Array[j + 1] = tmp



pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)
def welcomeWindow():
    displayWindow.fill((0,0,0))
    displaystart("Welcome to GALAXY WARS!!",(150,150,150),160,255)
    displaystart("Press ENTER to play...",(0,200,0),160,295)
    pygame.display.update()
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    gameloop()

def gameloop():
    PlayerX = 370
    PlayerY = 480
    PlayerX_change = 0
    PlayerY_change = 0

    bckgrnd = pygame.image.load("background.png")

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []


    for i in range(6):
        enemyImg.append(pygame.image.load("enemy.png"))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(10,150))
        enemyX_change.append(2.5)
        enemyY_change.append(40)

    bubble(enemyX)
    bubble(enemyY)
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 5
    bullet_state = "ready"


    score_value = 0

    game_over = False
    running = True
    while running:
        if not game_over:
            displayWindow.fill((0,0,0))
            displayWindow.blit(bckgrnd,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        PlayerX_change = 3.5
                    if event.key == pygame.K_LEFT:
                        PlayerX_change = -3.5
                    if event.key == pygame.K_SPACE:
                        bullet_Sound = pygame.mixer.Sound("laser.wav")
                        bullet_Sound.play()
                        bulletX = PlayerX
                        bullet_state = "fire"

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        PlayerX_change = 0
            PlayerX += PlayerX_change
            PlayerY += PlayerY_change
            

            if PlayerX < 0:
                PlayerX = 0
            elif PlayerX >= 736:
                PlayerX = 736

            
            for i in range(6):
                if enemyX[i] < 0:
                    enemyX_change[i] = 2.5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -2.5
                    enemyY[i] += enemyY_change[i]

                collide = isCollision(enemyX[i],enemyY[i],PlayerX,PlayerY)
                if not collide:
                    collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
                    if collision:
                        collision_Sound = pygame.mixer.Sound("explosion.wav")
                        collision_Sound.play()
                        bulletY = 480
                        bullet_state = "ready"
                        score_value += 1
                        enemyX[i] = random.randint(0,735)
                        enemyY[i] = random.randint(10,150)
                    enemyX[i] += enemyX_change[i]
                    enemy(enemyImg,enemyX[i],enemyY[i],i)
                else:
                    game_over = True

            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fireBullet(bulletX,bulletY)
                bulletY -= bulletY_change
            

            player(PlayerX,PlayerY)
            displayscore(10, 10, score_value)
            pygame.display.update()
        else:
            displayWindow.blit(bckgrnd,(0,0))       
            gameover(275,258,score_value)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcomeWindow()
welcomeWindow()
