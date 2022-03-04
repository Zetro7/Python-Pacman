# from ghost import *
# from game import *
# from setup import *
import ghost
import game
import setup
import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AQUA = (0, 245, 255)
PINK = (255, 52, 179)
PURPLE = (191, 62, 255)

SCREENWIDTH = 608  # 32 * 19
SCREENHEIGHT = 800  # 32 * 26


#
class animatePlayer(object):
    def __init__(self, image, width, height):
        self.spriteSheet = image  # Load the sprite sheet
        self.imageList = []  # Create a list to store the images
        self.loadImage(width, height)
        self.position = 0  # Create a variable which will hold the current image of the list
        self.clock = 1  # Create a variable that will hold the time

    def loadImage(self, width, height):
        # Get each image in the sprite sheet
        for y in range(0, self.spriteSheet.get_height(), height):
            for x in range(0, self.spriteSheet.get_width(), width):
                image = self.getImage(x, y, width, height)  # Load images into a list

                self.imageList.append(image)

    def getImage(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()  # Create a new blank image
        image.blit(self.spriteSheet, (0, 0),
                   (x, y, width, height))  # Copy the sprite from the large sheet onto the smaller
        image.set_colorkey((0, 0, 0))  # Assuming black works as the transparent color
        return image  # Return the image

    def getCurrentImage(self):
        return self.imageList[self.position]

    def getLength(self):
        return len(self.imageList)

    def update(self, fps=45):
        step = 45 // fps
        l = range(1, 45, step)
        if self.clock == 45:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            self.position += 1  # Increase position
            if self.position == len(self.imageList):
                self.position = 0


class Player(pygame.sprite.Sprite):
    deltaX = 0
    deltaY = 0
    explosion = False
    gameOver = False

    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)  # Call the parent class (sprite) constructor
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        image = pygame.image.load("walk.png").convert()  # Load image which will be for the animation
        # self.goRightAnimation = animatePlayer(image, 32, 32)                # Create the animations objects
        # self.goLeftAnimation = animatePlayer(pygame.transform.flip(image, True, False), 32, 32)
        # self.goUpAnimation = animatePlayer(pygame.transform.rotate(image, 90) , 32, 32)
        # self.goDownAnimation = animatePlayer(pygame.transform.rotate(image, 270), 32, 32)
        image = pygame.image.load("explosion.png").convert()  # Load explosion image
        # self.explosionAnimation = animatePlayer(image, 30, 30)
        self.playerImage = pygame.image.load(filename).convert()  # Save the player image
        self.playerImage.set_colorkey(BLACK)

    def update(self, xBlocks, yBlocks):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREENWIDTH
            elif self.rect.left > SCREENWIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREENHEIGHT
            elif self.rect.top > SCREENHEIGHT:
                self.rect.bottom = 0

            self.rect.x += self.deltaX
            self.rect.y += self.deltaY

            # This will stop the user for go up or down when it is inside of the box
            for piece in pygame.sprite.spritecollide(self, xBlocks, False):
                self.rect.centery = piece.rect.centery
                self.deltaY = 0

            for piece in pygame.sprite.spritecollide(self, yBlocks, False):
                self.rect.centerx = piece.rect.centerx
                self.deltaX = 0

            # This will cause the animation to start
            # if self.deltaX > 0:
            # self.goRightAnimation.update(10)
            # self.image = self.goRightAnimation.getCurrentImage()

            # elif self.deltaX < 0:
            # self.goLeftAnimation.update(10)
            # self.image = self.goLeftAnimation.getCurrentImage()

            # if self.deltaY > 0:
            # self.goDownAnimation.update(10)
            # self.image = self.goDownAnimation.getCurrentImage()

            # elif self.deltaY < 0:
            # self.goUpAnimation.update(10)
            # self.image = self.goUpAnimation.getCurrentImage()

        #else:
        #   if self.explosionAnimation.position == self.explosionAnimation.getLength() - 1:
        #        pygame.time.wait(500)
        #        self.gameOver = True
        #
        #    self.explosionAnimation.update(12)
        #    self.image = self.explosionAnimation.getCurrentImage()

    def goRight(self):
        self.deltaX = 3

    def goLeft(self):
        self.deltaX = -3

    def goUp(self):
        self.deltaY = -3

    def goDown(self):
        self.deltaY = 3

    def rightStop(self):
        if self.deltaX != 0:  # LEAVE PAGE
            self.image = self.playerImage
        self.deltaX = 0

    def leftStop(self):
        if self.deltaX != 0:  # LEAVE PAGE
            self.image = pygame.transform.flip(self.playerImage, True, False)
        self.deltaX = 0

    def upStop(self):
        if self.deltaY != 0:  # LEAVE PAGE
            self.image = pygame.transform.rotate(self.playerImage, 90)
        self.deltaY = 0

    def downStop(self):
        if self.deltaY != 0:  # LEAVE PAGE
            self.image = pygame.transform.rotate(self.playerImage, 270)
        self.deltaY = 0