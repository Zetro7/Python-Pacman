# Set Up
#from ghost import *
#from game import *
#from player import *
import pygame
import random
import ghost
import player
import game

# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
AQUA = (0,245,255)
PINK = (255,52,179)
PURPLE = (191,62,255)

SCREENWIDTH = 608       # 32 * 19
SCREENHEIGHT = 800      # 32 * 26

# Create World with Dimension 26 x 19
def world():
    # 0 - Blank Space
    # - - Horizontal Line
    # | - Vertical Line
    # + - Cross in the Road

    world = (('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('-','+','-','-','-','+','-','-','-','+','-','-','-','+','-','-','-','+','-'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('-','+','-','-','-','+','-','-','-','+','-','-','-','+','-','-','-','+','-'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('-','+','-','-','-','+','-','-','-','+','-','-','-','+','-','-','-','+','-'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('-','+','-','-','-','+','-','-','-','+','-','-','-','+','-','-','-','+','-'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('-','+','-','-','-','+','-','-','-','+','-','-','-','+','-','-','-','+','-'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'),
             ('-','+','-','-','-','+','-','-','-','+','-','-','-','+','-','-','-','+','-'),
             ('0','|','0','0','0','|','0','0','0','|','0','0','0','|','0','0','0','|','0'))

    return world


def createWorld(screen):
    for i, row in enumerate(world()):
        for j, item in enumerate(row):
            # Draws horizontal walls
            if item == '-':
                pygame.draw.line(screen, PINK, [j*32, i*32], [j*32+32, i*32], 3)
                pygame.draw.line(screen, PINK, [j*32, i*32+32], [j*32+32, i*32+32], 3)
            # Draws vertical walls
            elif item == '|':
                pygame.draw.line(screen, PINK, [j*32, i*32], [j*32, i*32+32], 3)
                pygame.draw.line(screen, PINK, [j*32+32, i*32], [j*32+32, i*32+32], 3)                                 


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


class Pellets(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, number):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        if number == 1:
        # Set the background color and set it to be transperant
            self.image = pygame.Surface([width, height])
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            self.image = pygame.image.load("pellet.png")

        elif number == 2:
            self.image = pygame.Surface([width, height])
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            self.image = pygame.image.load("orange.png")

        else:
            self.image = pygame.Surface([width, height])
            self.image.fill(BLACK)
            self.image.set_colorkey(BLACK)
            self.image = pygame.image.load("cherry.png")
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


class Menu(object):
    position = 0

    # Set default font, color & size
    def __init__(self, options, fontColor = (0,255,0), choiceColor = (255,255,255), ttfFont = None, fontSize = 25):
        self.fontColor = fontColor
        self.choiceColor = choiceColor
        self.options = options
        self.font = pygame.font.Font(ttfFont, fontSize)         # needs ttfFont argument, set it to none


    def displayHomeScreen(self,screen):
        for index, value in enumerate(self.options):
            # Regular color
            if self.position == index:
                message = self.font.render(value, True, self.choiceColor)   

            # Choice color
            else:
                message = self.font.render(value, True, self.fontColor)
      
            posX = (SCREENWIDTH / 2) - (message.get_width() / 2)
            posY = (SCREENHEIGHT / 2) - (len(self.options)* message.get_height() / 2) + (index * message.get_height())
            
            screen.blit(message,(posX,posY))

    # Retrieves user keystroke from the Main Menu
    def getAction(self, action):
        if action.type == pygame.KEYDOWN:
            if action.key == pygame.K_UP:
                if self.position > 0:
                    self.position -= 1

            elif action.key == pygame.K_DOWN:
                if self.position < 1:
                    self.position += 1
