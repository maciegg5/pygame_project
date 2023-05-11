import pygame
import random  # generowanie losowe
import math

pygame.font.init()  # czczionki gotowe do uzycia

# start game
pygame.init()

dirtyRects = []

# punkty
score = 0
main_font = pygame.font.SysFont("comicsans", 50)

# zycia
live = 3

# zegar
clock = pygame.time.Clock()

# create game screen
screen = pygame.display.set_mode((800, 600))

# nazwa gry
pygame.display.set_caption("Defending Island")

# ikonka
icon = pygame.image.load("assets/swords.png")
pygame.display.set_icon(icon)

# gracz
playerImg = pygame.image.load("assets/viking.png")
playerX = 368
playerY = 480
# predkosc poczatkowa
speed = 0
speed2 = 0

#gracz down
playerImg_down = pygame.image.load("assets/viking_down.png")

# przeciwnicy
pirateImg = pygame.image.load("assets/pirate.png")
# devilImg=pygame.image.load("assets/devil.png")
pirateX = random.randint(1, 735)
pirateY = 0
speed_pX = random.choice([0.2, 0.3])
speed_pY = 20

# bron
spearImg = pygame.image.load('assets/spear.png')
spearX = -50
spearY = -50
speed_sY = 1
spearState = "ready"  # stoi


# funkcje dla poszczegolnych elementow gry
def player(x, y):
    screen.blit(playerImg, (x, y))  # bilt-rysowanie


def enemy(x, y):
    screen.blit(pirateImg, (x, y))


def throw_spear(x, y):
    global spearState
    spearState = "throw"
    r = screen.blit(spearImg, (x + 16, y + 10))
    global dirtyRects
    dirtyRects.append(r)


def is_collision(enemyX, enemyY, spearX, spearY):
    distance = math.sqrt((math.pow(enemyX - spearX, 2) + math.pow(enemyY - spearY, 2)))
    if distance < 50:
        return True
    else:
        return False


def gen_enemy():
    global pirateX, pirateY, speed_pX
    pirateX = random.randint(1, 735)
    pirateY = random.randint(1, 100)
    speed_pX = random.choice([-0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4])
    speed_pY = 20

def caption(w, x, y, o):
    label = main_font.render(f"{o}: {w}", True, (255, 0, 0))
    screen.blit(label, (x, y))

pause = False

def paused():

    pause = True

    screen.fill((0, 0, 0))
    label2 = main_font.render(f"GAME OVER", True, (255, 0, 0))
    screen.blit(label2, (300 - 32, 220 - 32))

    while pause:
        # musi byc jakis warunke bo nic nie moglibysmy zrobic -> blad
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

running = True

while running:  # nieskonczona petla do momentu kiedy jest True
    screen.fill((255, 255, 155))  # rgb
    caption(score, 10, 10, "score")
    caption(live, 650, 10, "live")
    for event in pygame.event.get():  # dla wszystkich zdarzen
        if event.type == pygame.QUIT:  # jesli przycisk zamknij
            running = False  # zmieniamy na falsz i glowna petla sie skonczy

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spearY = playerY
                spearX = playerX
                throw_spear(playerX, spearY)

        keys = pygame.key.get_pressed()
        speed = 0
        speed2 = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            speed = -1
            playerImg = pygame.image.load("assets/viking_left.png")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            speed = 1
            playerImg = pygame.image.load("assets/viking_right.png")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed2 = -1
            playerImg = pygame.image.load("assets/viking.png")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            speed2 = 1
            thrw='down'
            playerImg = pygame.image.load("assets/viking_down.png")

    playerX += speed
    playerY += speed2

    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0
    if playerY >= 536:  # nie moze tu byc elif !!! bo odnosimy sie juz do czegos innego
        playerY = 536
    elif playerY <= 0:
        playerY = 0

    if pirateX <= 0:
        speed_pX *= -1
        pirateY += speed_pY
    elif pirateX >= 736:
        speed_pX *= -1
        pirateY += speed_pY

    pirateX += speed_pX

    if spearY <= -32:
        spearY = -50
        spearState = "ready"

    # wywolanie funkcji
    player(playerX, playerY)

    if spearState == "throw":
        throw_spear(spearX, spearY)
        if thrw='down'
            spearY += speed_sY
        else
            spearY -= speed_sY


    # kolizja
    collision = is_collision(pirateX, pirateY, spearX, spearY)
    if collision:
        spearState = "ready"
        spearY = -50
        score += 1
        #print(score)
        gen_enemy()
        speed_pX += 1
        speed_pY += 10

    collision_2 = is_collision(pirateX, pirateY, playerX, playerY)

    if collision_2:
        print("KOLIZJA")
        live -= 1
        gen_enemy()

    if live < 1:
        paused()

    if pirateY >= 568:
        paused()
    enemy(pirateX, pirateY)
    # aby wszystko sie narysowalo
    pygame.display.flip()
    clock.tick(1000)
