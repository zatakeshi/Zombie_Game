import pygame
from random import randint

pygame.init()

#variables
SW = 640
SH = 480
screen = pygame.display.set_mode((SW, SH))
#pygame.key.set_repeat(10, 50)
exitGame = False
colour = (randint(0, 255), randint(0, 255), randint(0, 255))
xPos = 30 #260
yPos = 30 #180
speed = 10
BLACK = (0, 0, 0)
controls = {'up': False, 'down': False, 'right': False, 'left': False}
clock = pygame.time.Clock()
spriteGroup = pygame.sprite.Group()
WHITE = (255, 255, 255)
FONTSIZE = 20
FONT = pygame.font.Font("freesansbold.ttf", FONTSIZE)
roundTime = 5
timeLeft = roundTime
ticks = pygame.time.get_ticks()
myShape = pygame.draw.rect(screen, colour, pygame.Rect(xPos, yPos, 20, 20))
gameOver = False
zombieCount = 1

#powerups
powerupGroup = pygame.sprite.Group()
POWERUPMOVESPEED = [2, 2]
invincible = False
powerupCounter = 0

#class
#################################################################################################################################
class Zombie(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.width = 50
        self.height = 77
        self.direction = "L"
        self.image = pygame.Surface([self.width, self.height])
        self.image = pygame.image.load("zombie.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        if target.x < SW / 2:
            self.rect.x = randint(SW / 2, SW - self.rect.width)
            self.rect.y = randint(0, SH - self.rect.height)
        else:
            self.rect.x = randint(0, SW / 2)
            self.rect.y = randint(0, SH - self.rect.height)

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def move(self, target):
        if self.rect.x == target.x:
            xMove = 0
        elif self.rect.x - target.x > 0:
            if self.direction == "R":
                self.flip()
                self.direction = "L"
            xMove = -1
        else:
            if self.direction == "L":
                self.flip()
                self.direction = "R"
            xMove = 1
        if self.rect.y - target.y > 0:
            yMove = -1
        else:
            yMove = 1
        self.rect.x += xMove
        self.rect.y += yMove

    def checkCollide(self, target):
        if self.rect.colliderect(target):
            return True
        
#################################################################################################################################
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = 40
        self.speed = POWERUPMOVESPEED
        self.imageCounter = 1
        self.types = ["invicible", "speed"]
        self.type = self.types[randint(0, len(self.types) - 1)]
        self.image = pygame.Surface([self.size, self.size])

        if self.type == "invincible":
            self.image = pygame.image.load("./Yellow/frame 1.png").convert_alpha()
        elif self.type == "speed":
            self.image = pygame.image.load("./Blue/frame 1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = randint(SW / 2, SW - self.size)
        self.rect.y = randint(0, SH - self.size)

    def move(self):
        if self.rect.x < 0 or self.rect.x > SW - self.size:
            self.speed[0] *= -1
        if self.rect.y < 0 or self.rect.y > SH - self.size:
            self.speed[1] *= -1
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def checkCollide(self, target):
        if self.rect.colliderect(target):
            if self.type == "invincible":
                global invincible
                invincible = True
            elif self.type == "speed":
                global speed
                speed = 7

    def animate(self):
        if not self.imageCounter == 6:
            self.imageCounter += 1
        else:
            self.imageCounter = 1
        if self.type == "invincible":
            self.image = pygame.image.load("./Yellow/frame " + str(self.imageCounter) + ".png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        elif self.type == "speed":
            self.image = pygame.image.load("./Blue/frame " + str(self.imageCounter) + ".png").convert_alpha()
            self.image = pygame.transform.scale(self.image (self.size, self.size))

#################################################################################################################################

zombieOne = Zombie(myShape)
spriteGroup.add(zombieOne)

#characters
#character = pygame.Surface([50, 77])
#character = pygame.image.load("Anime-Fairy-Tail-Happy-2.png").convert_alpha()
#character = pygame.transform.scale(character, (85, 77))


def changeColour():     #define after variables
    return(randint(0, 255), randint(0, 255), randint(0, 255))

def showTimer():
    timerSurface = FONT.render("Time: %s" %(timeLeft), True, WHITE)
    timerRect = timerSurface.get_rect()
    timerRect.topleft = (SW / 2 - 30, 25)
    screen.blit(timerSurface, timerRect)
    
    scoreSurface = FONT.render("Zombies: %s" %(zombieCount), True, WHITE)
    scoreRect = timerSurface.get_rect()
    scoreRect.topleft = (25, 25)
    screen.blit(scoreSurface, scoreRect)
    
powerup = Powerup()
powerupGroup.add(powerup)

while not exitGame:
    seconds = int((pygame.time.get_ticks() - ticks) / 1000)
    timeLeft = roundTime - seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame = True
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_SPACE:
                #colour = changeColour()
            if event.key == pygame.K_RIGHT:
                controls['right'] = True
            elif event.key == pygame.K_LEFT:
                 controls['left'] = True
            elif event.key == pygame.K_UP:
                controls['up'] = True
            elif event.key == pygame.K_DOWN:
                controls['down'] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                controls['right'] = False
            elif event.key == pygame.K_LEFT:
                 controls['left'] = False
            elif event.key == pygame.K_UP:
                controls['up'] = False
            elif event.key == pygame.K_DOWN:
                controls['down'] = False
    if controls['left']:
        if xPos > 0:
            xPos -= speed
    if controls['right']:
        if xPos < SW - myShape.width:
            xPos += speed
    if controls['up']:
        if yPos > 0:
            yPos -= speed
    if controls['down']:
        if yPos < SH - myShape.height:
            yPos += speed
    pygame.Surface.fill(screen, BLACK)
    #screen.blit(character, (500, 350))
    for zombie in spriteGroup:
        zombie.move(myShape)
        if zombie.checkCollide(myShape):
            if invincible:
                zombie.kill()
            else:
                gameOver = True

    if seconds > roundTime:
        seconds = 0
        ticks = pygame.time.get_ticks()
        zombie = Zombie(myShape)
        spriteGroup.add(zombie)
        zombieCount += 1
        
    if gameOver:
        exitGame = True
        endSplash = pygame.image.load("gameover2.png").convert_alpha()
        endSplash = pygame.transform.rotate(endSplash, randint(-45, 45))
        screen.blit(endSplash, (SW / 8, SH / 6))
    if invincible == True:
        myShape = pygame.draw.rect(screen, changeColour(), pygame.Rect(xPos, yPos, 60, 60))
        powerupCounter += 1
    else:
        myShape = pygame.draw.rect(screen, colour, pygame.Rect(xPos, yPos, 60, 60))
        
    spriteGroup.draw(screen)
    powerupGroup.draw(screen)
    showTimer()
    pygame.display.flip()
    clock.tick(100)
    
pygame.time.wait(2000)
pygame.quit()
