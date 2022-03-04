# Ghost
#from setup import *
#from game import *
#from player import *
import player
import game
import setup
import pygame
import random
from setup import *
from random import randrange      # To randomly load the ghost sprites

# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
AQUA = (0,245,255)
PINK = (255,52,179)
PURPLE = (191,62,255)

# Screen Set Up
SCREENWIDTH = 608   # 32 * 19
SCREENHEIGHT = 800  # 32 * 26

class Ghost(pygame.sprite.Sprite):   # Simple base class for visible game objects
    def __init__(self, x, y, deltaX, deltaY):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Initialize direction of ghost
        self.deltaX = deltaX
        self.deltaY = deltaY

        # Randomly loads ghost sprites
        num = random.randint(0,5)
        if num == 0:
            self.image = pygame.image.load("clyde.png")
        elif num == 1:
            self.image = pygame.image.load("funky.png")
        elif num == 2:
            self.image = pygame.image.load("blinky.png")
        elif num == 3:
            self.image = pygame.image.load("inky.png")
        else:
            self.image = pygame.image.load("pinky.png")

        # A rect with the dimensions of the image (x & y)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    # Updates position of ghost on screen
    def update(self, xBlocks, yBlocks):
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY

        # Falls off top of screen, returns on bottom
        if self.rect.top > SCREENHEIGHT:
            self.rect.bottom = 0

        # Falls off bottom of screen, returns on top
        elif self.rect.bottom < 0:
            self.rect.top = SCREENHEIGHT
            
        # Falls off left side of screen, returns on right side
        if self.rect.right < 0:
            self.rect.left = SCREENWIDTH

        # Falls off right side of screen, returns on left side
        elif self.rect.left > SCREENWIDTH:
            self.rect.right = 0

        if self.rect.topleft in self.getCross():
            # Randomly decides ghost's direction
            decision = random.choice(('+y', '-y', '+x', '-x'))

            # Up
            if decision == "+y" and self.deltaY == 0:
                self.deltaX = 0
                self.deltaY = -3

            # Down
            elif decision == "-y" and self.deltaY == 0:
                self.deltaX = 0
                self.deltaY = 3

            # Left
            elif decision == "+x" and self.deltaX == 0:
                self.deltaX = -3
                self.deltaY = 0

            # Right
            elif decision == "-x" and self.deltaX == 0:
                self.deltaX = 3
                self.deltaY = 0

                
    def getCross(self):
        items = []
        for i, row in enumerate(world()):
            for j, value in enumerate(row):
                if value == '+':
                    items.append((j*32, i*32))
        return items
        







            
        
        

        




