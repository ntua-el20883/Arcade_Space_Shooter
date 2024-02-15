import pygame
import math
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background for the main game
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

# Load the game over sound
game_over_sound = mixer.Sound("game_over_sound.wav")

explosionImg = pygame.image.load('explosion.png')

# Title and Icon
pygame.display.set_caption("Arcade Space Shooter - A.S.S.")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Colors
white = (255, 255, 255)
green = (3, 168, 3)
red = (168, 3, 3)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y, score_value):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER >:)", True, red)
    retry_text = font.render("Close this window to try again", True, white)
    screen.blit(over_text, (180, 250))
    screen.blit(retry_text, (170, 320))  # Adjust the position as needed

def player(x, y, playerImg):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i, enemyImg):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y, bulletImg):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = smallText.render(msg, True, black), smallText.render(msg, True, black).get_rect()
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def game_intro():
    intro = True
    intro_background = pygame.image.load('start_screen.jpg')  # Load the start screen background

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.blit(intro_background, (0, 0))  # Draw the background on the screen

        largeText = pygame.font.Font('freesansbold.ttf', 70)
        TextSurf, TextRect = largeText.render("Arcade Space Shooter", True, black), largeText.render("Arcade Space Shooter", True, black).get_rect()
        TextRect.center = ((800 / 2), (600 / 2))
        screen.blit(TextSurf, TextRect)
        
        button("Start", 350, 450, 100, 50, green, red, game_loop)
        
        pygame.display.update()


def game_loop():
    # Game specific variables
    global bullet_state
    bullet_state = "ready"

    playerImg = pygame.image.load('spaceship.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    # Add a flag to track if an explosion is happening and its location
    explosion_active = False
    explosionX = 0
    explosionY = 0


    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    bulletImg = pygame.image.load('bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10

    score_value = 0
    textX = 10
    textY = 10

    running = True
    game_over_sound_played = False

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY, bulletImg)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                if not game_over_sound_played:
                    game_over_sound.play()
                    game_over_sound_played = True
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i, enemyImg)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY, bulletImg)
            bulletY -= bulletY_change
        
        for i in range(num_of_enemies):
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                explosion_active = True
                explosionX = enemyX[i]
                explosionY = enemyY[i]
                enemyX[i] = random.randint(0, 736)  # Reset enemy position or handle as needed
                enemyY[i] = random.randint(50, 150)
                # Show the explosion image instead of the enemy for a brief moment
                screen.blit(explosionImg, (explosionX, explosionY))
                pygame.display.update()
                pygame.time.wait(100)  # Wait for 100 milliseconds to show the explosion

        player(playerX, playerY, playerImg)
        show_score(textX, textY, score_value)
        pygame.display.update()

game_intro()
