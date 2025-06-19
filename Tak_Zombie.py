#A COMMENT

import pygame
from random import randint

pygame.init()
pygame.key.set_repeat(1, 0)
clock = pygame.time.Clock()

SW = 640
SH = 480
screen = pygame.display.set_mode((SW, SH))
exitGame = False
size = 30
colour = (100, 100, 100)
xPos = 0
yPos = 0
controls = {'up':False, 'down':False, 'left':False, 'right':False}
speed = 5
mySquare = pygame.draw.rect(screen, colour, pygame.Rect(xPos, yPos, size, size))
spriteGroup = pygame.sprite.Group()
heroGroup = pygame.sprite.Group()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (255, 0, 200)
FONTSIZE = 20
FONT = pygame.font.Font("freesansbold.ttf", FONTSIZE)

ticks = pygame.time.get_ticks()
roundTime = 10
timeLeft = roundTime


# FUNCTIONS #

def changeColour():
    return((randint(10, 255), randint(10, 255), randint(10, 255)))

def showTimer():
    timerSurface = FONT.render("Time: %s" %(timeLeft), True, WHITE)
    timerRect = timerSurface.get_rect()
    timerRect.topleft = (SW / 2 - 30, 25)
    screen.blit(timerSurface, timerRect)

# end of functions #


# CLASSES #
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.direction = "L"
        self.image = pygame.Surface([self.width, self.height])
        self.image = pygame.image.load("hero.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = xPos
        self.rect.y = yPos

    def move(self):
        global xPos, yPos
        self.rect.x = xPos
        self.rect.y = yPos
        
        

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

        if self.rect.y == target.y:
            yMove = 0

        elif self.rect.y - target.y > 0:
            yMove = -1

        else:
            yMove = 1
        

        self.rect.y += yMove
        self.rect.x += xMove

    def collide(self, target):
        if self.rect.colliderect(target):
            print("WHAAAAAA!")

    
        
    


hero = Hero()
heroGroup.add(hero)

zombieOne = Zombie(hero.rect)
spriteGroup.add(zombieOne)


# end of classses #


# MAIN GAME LOOP #
while not exitGame:

    seconds = int((pygame.time.get_ticks() - ticks) / 1000)
    timeLeft = roundTime - seconds
    
   
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exitGame = True

        #Checks for key DOWN 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                colour = changeColour()
            elif event.key == pygame.K_RIGHT:
                controls['right'] = True
            elif event.key == pygame.K_LEFT:
                controls['left'] = True
            elif event.key == pygame.K_UP:
                controls['up'] = True
            elif event.key == pygame.K_DOWN:
                controls['down'] = True

        #Checks for key UP 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                controls['right'] = False

            elif event.key == pygame.K_LEFT:
                controls['left'] = False
            
            elif event.key == pygame.K_UP:
                controls['up'] = False
            
            elif event.key == pygame.K_DOWN:
                controls['down'] = False

        #If control input is detected, react
        if controls['up']:
            if yPos > 0:
                yPos -= speed
            
        if controls['down']:
            if yPos < SH - size:
                yPos += speed
            
        if controls['left']:
            if xPos > 0:
                xPos -= speed
    
        if controls['right']:
            if xPos < SW - size:
                xPos += speed

        
    pygame.Surface.fill(screen, BLACK)
    zombieOne.move(hero.rect)
    hero.move()
    zombieOne.collide(hero.rect)

    for zombie in spriteGroup:
        zombie.move(hero.rect)
        zombie.collide(hero.rect)
        
    if seconds > roundTime:
        seconds = 0
        ticks = pygame.time.get_ticks()
        zombie = Zombie(hero.rect)
        spriteGroup.add(zombie)
    

    spriteGroup.draw(screen)
    heroGroup.draw(screen)
    
    showTimer()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()



