from glob import glob
import random
import pygame

# initalizing pygame
pygame.init()

# creating screen
WIDTH = 640
HEIGHT = 480
PADDING = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# title and icon
icon = pygame.image.load("./img/invader.png")
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(icon)

# classes
class Player:
    def __init__(self, pos, scale):
        self.pos = pos
        self.scale = scale
        self.dir = 0
        self.speed = 0.16
        self.sprite = None
        self.initImage()

    def initImage(self):
        img = pygame.image.load("./img/rocket.png")
        (w, h) = img.get_size()
        img = pygame.transform.scale(img, (w * self.scale , h * self.scale))
        self.sprite = img

    def shoot(self):
        bullet = Bullet([self.pos[0] + (self.sprite.get_size()[0] / 2), self.pos[1] - 6 * SCALE], SCALE)
        BULLETS.append(bullet)
        shootSfx.play()

    def borderCheck(self):
        if self.pos[0] < PADDING:
            self.pos[0] = PADDING
        if self.pos[0] > WIDTH - self.sprite.get_size()[0] - PADDING:
            self.pos[0] = WIDTH - self.sprite.get_size()[0] - PADDING

    def update(self):
        self.pos[0] += self.dir * self.speed
        self.borderCheck()
        screen.blit(self.sprite, self.pos)

class Bullet:
    def __init__(self, pos, scale):
        self.pos = pos
        self.scale = scale
        self.speed = 0.3
        self.sprite = None
        self.initImage()
    
    def initImage(self):
        img = pygame.image.load("./img/bullet.png")
        (w, h) = img.get_size()
        img = pygame.transform.scale(img, (w * self.scale , h * self.scale))
        self.sprite = img
    
    def collisionCheck(self):
        rect = self.sprite.get_rect()
        (rect.x, rect.y) = self.pos
        for row in ENEMIES:
            for enemy in row:
                enemy_rect = enemy.sprite.get_rect()
                (enemy_rect.x, enemy_rect.y) = enemy.pos
                if rect.colliderect(enemy_rect):
                    BULLETS.remove(self)
                    enemy.hp -= 1

    def borderCheck(self):
        if self.pos[1] < -100:
            BULLETS.remove(self)

    def update(self):
        self.pos[1] -= self.speed
        self.borderCheck()
        screen.blit(self.sprite, self.pos)
        self.collisionCheck()

class Enemy:
    def __init__(self, pos, row, scale):
        self.pos = pos
        self.row = row
        self.scale = scale
        self.dir = 1
        self.speed = 0.01

        self.hp = 1
        self.isDestroyed = False
        self.destoryTick = 60
        self.shootTick = 0
        self.nextShoot = random.randint(100, 500)

        self.sprite = None
        self.destroySprite = None
        self.initImage()

    def initImage(self):
        img = pygame.image.load("./img/invader.png")
        (w, h) = img.get_size()
        img = pygame.transform.scale(img, (w * self.scale , h * self.scale))
        self.sprite = img

        img = pygame.image.load("./img/destory.png")
        (w, h) = img.get_size()
        img = pygame.transform.scale(img, (w * self.scale, h * self.scale))
        self.destroySprite = img

    def shootCheck(self):
        if not self.isDestroyed:
            rect = self.sprite.get_rect()
            (rect.x, rect.y) = self.pos
            canShoot = True
            for row in range(self.row + 1, len(ROWS)):
                for enemy in ENEMIES[row]:
                    enemyRect = enemy.sprite.get_rect()
                    (enemyRect.x, enemyRect.y) = (enemy.pos[0], self.pos[1])
                    if rect.colliderect(enemyRect):
                        canShoot = False
                    
            if canShoot:
                if self.shootTick > self.nextShoot:
                    self.shoot()
                    self.shootTick = 0
                    self.nextShoot = random.randint(500, 5000)
                else:
                    self.shootTick += 1

    def shoot(self):
        size = self.sprite.get_size()
        bullet = InvaderBullet([self.pos[0] + (size[0] / 2), self.pos[1] + size[1]], SCALE)
        INVADER_BULLETS.append(bullet)
        shootSfx.play()

    def destroy(self):
        if self.hp <= 0:
            self.isDestroyed = True

        if self.isDestroyed:
            if self.destoryTick < 0:
                ENEMIES[self.row].remove(self)
                invaderDestroySfx.play()
                board.score += 1000
            else:
                self.destoryTick -= 1

    def checkCollisionWithPlayer(self):
        rect = self.sprite.get_rect()
        (rect.x, rect.y) = self.pos
        playerRect = player.sprite.get_rect()
        (playerRect.x, playerRect.y) = player.pos
        if rect.colliderect(playerRect):
            board.lives = 0
      
    def update(self):
        self.pos[0] += self.dir * self.speed
        if not self.isDestroyed: screen.blit(self.sprite, self.pos)
        else: screen.blit(self.destroySprite, self.pos)        
        self.shootCheck()
        self.checkCollisionWithPlayer()
        self.destroy()

class InvaderBullet:
    def __init__(self, pos, scale):
        self.pos = pos
        self.scale = scale
        self.speed = 0.3
        self.sprite = None
        self.initImage()
    
    def initImage(self):
        img = pygame.image.load("./img/bullet.png")
        (w, h) = img.get_size()
        img = pygame.transform.scale(img, (w * self.scale , h * self.scale))
        self.sprite = img
    
    def collisionCheck(self):
        rect = self.sprite.get_rect()
        (rect.x, rect.y) = self.pos
        playerRect = player.sprite.get_rect()
        (playerRect.x, playerRect.y) = player.pos

        if rect.colliderect(playerRect):
            INVADER_BULLETS.remove(self)
            explosionSfx.play()
            board.lives -= 1

    def borderCheck(self):
        if self.pos[1] > HEIGHT:
            INVADER_BULLETS.remove(self)

    def update(self):
        self.pos[1] += self.speed
        self.borderCheck()
        screen.blit(self.sprite, self.pos)
        self.collisionCheck()

class InvaderRow:
    def __init__(self, pos, size, row):
        self.pos = pos
        self.size = size
        self.row = row
        self.dir = 1
        self.speed = 0.01
    
    def update(self):
        if self.pos[0] < PADDING:
            self.dir = 1
            self.pos[1] += 10
            for enemy in ENEMIES[self.row]:
                enemy.dir = 1
                enemy.pos[1] += 10
        if self.pos[0] > WIDTH - self.size - PADDING:
            self.dir = -1
            self.pos[1] += 10
            for enemy in ENEMIES[self.row]:
                enemy.dir = -1
                enemy.pos[1] += 10

        self.pos[0] += self.dir * self.speed

class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.textFont = pygame.font.Font("./font/Geo.otf", 20)
        self.numberFont = pygame.font.Font("./font/Geo.otf", 29)
        self.footerFont = pygame.font.Font("./font/Geo.otf", 12)
        self.headingFont = pygame.font.Font("./font/Geo.otf", 75)
        self.headingLgFont = pygame.font.Font("./font/Geo.otf", 122)
        self.lifeImg = pygame.image.load("./img/livesicon.png")
    
    def drawLives(self):
        text = self.textFont.render("LIVES: ", True, (244, 255, 191))
        screen.blit(text, (90, 34))

        for i in range(self.lives):
            screen.blit(self.lifeImg, (143 + (i * self.lifeImg.get_size()[0]) + (i * 7), 40))

    def drawScore(self):
        text = self.textFont.render("SCORE: ", True, (244, 255, 191))
        screen.blit(text, (391, 34))

        text = self.numberFont.render("{:07}".format(self.score), True, (244, 255, 191))
        screen.blit(text, (448, 27))


    def draw(self):
        pygame.draw.rect(screen, (244, 255, 191), pygame.Rect(80, 20, 480, 50), 2)
        self.drawLives()
        self.drawScore()
        self.winCheck()

    def restart(self):
        global gameOver
        gameOver = False
        self.score = 0
        self.lives = 3
        ENEMIES.clear()
        ROWS.clear()
        BULLETS.clear()
        INVADER_BULLETS.clear()
        spawnEnemies()

    def winCheck(self):
        global gameOver
        total = 0
        for row in ENEMIES:
            total += len(row)
        if total == 0:
            gameOver = True

    def home(self):
        global home
        text = self.footerFont.render("made by krsna, radhe radhe", True, (244, 255, 191))
        screen.blit(text, (499, 457))

        text = self.headingLgFont.render("SPACE", True, (244, 255, 191))
        screen.blit(text, (178, 128))
        text = self.headingFont.render("INVADERS", True, (244, 255, 191))
        screen.blit(text, (186, 229))
        pygame.draw.rect(screen, (96, 128, 87), pygame.Rect(276, 322, 100, 30))
        text = self.textFont.render("START", True, (244, 255, 191))
        screen.blit(text, (303, 326))

        mpos = pygame.mouse.get_pos()
        rect = pygame.Rect(276, 322, 100, 30)
        if(rect.collidepoint(mpos)):
            if pygame.mouse.get_pressed()[0] == 1:
                home = False

    def update(self):
        global gameOver
        text = self.footerFont.render("made by krsna, radhe radhe", True, (244, 255, 191))
        screen.blit(text, (499, 457))

        if(self.lives <= 0):
            gameOver = True

        if not gameOver:
            self.draw()
        else:
            text = self.headingFont.render("GAME OVER", True, (244, 255, 191))
            screen.blit(text, (164, 155))
            text = self.numberFont.render("SCORE: {:07}".format(self.score), True, (244, 255, 191))
            screen.blit(text, (237, 230))
            pygame.draw.rect(screen, (96, 128, 87), pygame.Rect(276, 274, 100, 30))
            text = self.textFont.render("RESTART", True, (244, 255, 191))
            screen.blit(text, (293, 278))

            mpos = pygame.mouse.get_pos()
            rect = pygame.Rect(276, 274, 100, 30)
            if(rect.collidepoint(mpos)):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.restart()


# game variables
VOLUME = 0.2
SCALE = 2
player = Player([311, 400], SCALE)
board = ScoreBoard()

# load assets
shootSfx = pygame.mixer.Sound("./audio/shoot.wav")
shootSfx.set_volume(VOLUME)
invaderDestroySfx = pygame.mixer.Sound("./audio/invaderkilled.wav")
invaderDestroySfx.set_volume(VOLUME)
explosionSfx = pygame.mixer.Sound("./audio/explosion.wav")
explosionSfx.set_volume(VOLUME * 2)

pygame.mixer.music.load("./audio/background.wav")
pygame.mixer.music.set_volume(VOLUME)
pygame.mixer.music.play(-1)


# game lists
BULLETS = []
INVADER_BULLETS = []
ENEMIES = []
ROWS = []

# spawn enemies function
def spawnEnemies():
    y = 100
    for i in range(5):
        x = 133
        row = []
        for j in range(12):
            enemy = Enemy([x + (i * SCALE), y], i, SCALE)
            x += 11 * SCALE + 10
            row.append(enemy)

        ENEMIES.append(row)
        ROWS.append(InvaderRow([133 + (i * SCALE), y], (x - 133), i))
        y += 26

# spawing enemies
spawnEnemies()

# game loop
running = True
gameOver = False
home = True
while running:

    # game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.dir = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot()

    # screen background
    screen.fill((0, 43, 64))

    if home:
        board.home()

    elif not gameOver:

        # game input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.dir = -1
        if keys[pygame.K_RIGHT]:
            player.dir = 1

        # draw on screen
        player.update()
        board.update()

        for bullet in BULLETS: bullet.update()
        for bullet in INVADER_BULLETS: bullet.update()

        for row in ENEMIES:
            for enemy in row:
                enemy.update()
        
        for row in ROWS: row.update()
    
    else:
        # draw on screen
        board.update()

    # update frame
    pygame.display.update()