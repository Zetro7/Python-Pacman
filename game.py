# Game
#from ghost import *
#from setup import *
#from player import *
#from game import *
import ghost
import game
import setup
import pygame
from setup import *
from player import *
from ghost import Ghost
import random


# Define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
AQUA = (0,245,255)
PINK = (255,52,179)
PURPLE = (191,62,255)

MAXSCORE = 4790

# Screen Set Up
SCREENWIDTH = 608   # 32 * 19
SCREENHEIGHT = 800  # 32 * 26


# Runs Pacman
class playGame(object):
    def __init__(self):
        # Load the sound effects
        self.pacmanPellet = pygame.mixer.Sound("pacmanSound.ogg")
        self.gameOverSound = pygame.mixer.Sound("gameOver.ogg")
        self.pacmanFruit = pygame.mixer.Sound("eatFruit.ogg")
        self.winnerSound = pygame.mixer.Sound("winner.ogg")
        
        # Initalize Game
        self.player = Player(32, 64, "player.png")
        self.gameOver = True
        self.score = 0
        
        # Create a new font object from a file
        self.font = pygame.font.Font(None, 40)
        # Create the home page
        self.menu = Menu(("Play Game", "Quit Game"), fontColor = AQUA, fontSize = 75)
        
        # Create the blocks that will set the paths where the player can go
        # Group: A container class to hold and managae multiple sprite objects
        self.xBlocks = pygame.sprite.Group()
        self.yBlocks = pygame.sprite.Group()
        
        # Creates groups for the different types of pellets
        self.pelletGroup = pygame.sprite.Group()
        self.orangeGroup = pygame.sprite.Group()
        self.cherryGroup = pygame.sprite.Group()
        
        # Create the group for the ghosts
        self.ghostGroup = pygame.sprite.Group()

        #Add ghosts

        #self.ghostGroup.add(Ghost(544,736,0,-3))
        #self.ghostGroup.add(Ghost(288,64,0,3))
        #self.ghostGroup.add(Ghost(544,608,-3,0))
        #self.ghostGroup.add(Ghost(32,320,3,0))
        #self.ghostGroup.add(Ghost(116,480,3,0))
        #self.ghostGroup.add(Ghost(416,320,0,3))
        #self.ghostGroup.add(Ghost(416,736,0,-3))
        #self.ghostGroup.add(Ghost(32,320,-3,0))
        #self.ghostGroup.add(Ghost(416,64,0,3))
        #self.ghostGroup.add(Ghost(288,736,0,-3))
        #self.ghostGroup.add(Ghost(161,192,3,0))
        #self.ghostGroup.add(Ghost(288,480,0,-3))

        
        
        # Set the world:
        for i, row in enumerate(world()):
            for j, item in enumerate(row):
                if item == '-':
                    self.xBlocks.add(Background(j*32+8, i*32+8, 16, 16))
                elif item == '|':
                    self.yBlocks.add(Background(j*32+8, i*32+8, 16, 16))

                    
        # Add the pellets inside the game
        for i, row in enumerate(world()):
            for j, item in enumerate(row):
                if item == '+':
                    num = random.randint(0,1)
                    if num == 0:
                          self.cherryGroup.add(Pellets(j*32,i*32,10,10,3))
                    if num == 1:
                        self.orangeGroup.add(Pellets(j*32, i*32,10,10,2))
                elif item == '|' or item == '-':
                    self.pelletGroup.add(Pellets(j*32+12, i*32+12, 10, 10, 1))

    def update(self):
        for action in pygame.event.get():   # Player did something

            if action.type == pygame.QUIT:  # Player exited window
                return True
            else:                           # Player continued game play
                self.menu.getAction(action)
                if action.type == pygame.KEYDOWN:           # Player presses a key
                    if action.key == pygame.K_SPACE:
                        if self.gameOver:
                            if self.menu.position == 0:     # Player choose 'Play Game'
                                self.__init__()
                                self.gameOver = False
                            else:                           # Player choose 'Quit Game'
                                return True
                                
                    elif action.key == pygame.K_w or action.key == pygame.K_UP:
                        self.player.goUp()
                        
                    elif action.key == pygame.K_s or action.key == pygame.K_DOWN:
                        self.player.goDown()
                        
                    elif action.key == pygame.K_a or action.key == pygame.K_LEFT:
                        self.player.goLeft()

                    elif action.key == pygame.K_d or action.key == pygame.K_RIGHT:
                        self.player.goRight()

                    elif action.key == pygame.K_ESCAPE:
                        self.gameOver = True

        return False


    def runLogic(self):
        if not self.gameOver:
            self.player.update(self.xBlocks, self.yBlocks)
            hitBlock = pygame.sprite.spritecollide(self.player, self.pelletGroup, True)     # Removes pellet from screen

            if len(hitBlock) > 0:               # Player hit pellet
                self.pacmanPellet.play()         # Pellet Sound effect
                self.score += 10                # Pellets are worth 10 points

                if self.score == MAXSCORE:           # Won game, ate all pellets 
                    self.winnerSound.play()
                    self.player.explosion = True

            hitBlock = pygame.sprite.spritecollide(self.player,self.cherryGroup,True)

            if len(hitBlock) > 0:               # Player hit cherry
                self.pacmanFruit.play()         # Fruit Sound Effect
                self.score += 100               # Fruit are worth 100 points

                if self.score == MAXSCORE:           # Won game, ate everything
                    self.winnerSound.play()
                    self.player.explosion = True


            hitBlock = pygame.sprite.spritecollide(self.player,self.orangeGroup,True)

            if len(hitBlock) > 0:               # Player hit orange
                self.pacmanFruit.play()         # Fruit Sound Effect
                self.score += 100               # Fruit are worth 100 points

                if self.score == MAXSCORE:          # Won game, ate everything
                    self.winnerSound.play()
                    self.player.explosion = True
                        

            hitBlock = pygame.sprite.spritecollide(self.player,self.ghostGroup,True)

            if len(hitBlock) > 0:               # Player hit ghost
                    self.player.explosion = True
                    self.gameOverSound.play()

            # Ends Game    
            self.gameOver = self.player.gameOver
            # Updates Ghosts' Positions
            self.ghostGroup.update(self.xBlocks,self.yBlocks)

    def display(self,screen):
        # Clears screen to black
        screen.fill(BLACK)

        # Game Over
        if self.gameOver:
            if self.score == MAXSCORE:
                self.displayInfo(screen,"CONGRATULATIONS!!!", PINK, 200, 200)
                self.displayInfo(screen, "You won the game!", PINK, 220, 225)
# 5 at the end is how far over from the left of the screen it is
            self.displayInfo(screen, "Score: " + str(self.score), PINK, 5, 10)
            self.displayInfo(screen, "Directions:", PURPLE, 10, 590)
            self.displayInfo(screen, "Avoid the ghosts", PURPLE, 50, 620)
            self.displayInfo(screen, "Yellow pellets are worth 10 points", PURPLE, 50, 650)
            self.displayInfo(screen, "Fruit are worth 100 points", PURPLE, 50, 680)
            self.displayInfo(screen, "Eat all the pellets & fruit to win", PURPLE, 50, 710)
            self.displayInfo(screen, "Press enter to begin!", PURPLE, 50, 740)
            self.displayInfo(screen, "Good luck!", PURPLE, 10, 770)
            self.menu.displayHomeScreen(screen)

        # Game On
        else:
            self.xBlocks.draw(screen)
            self.yBlocks.draw(screen)
            createWorld(screen)
            self.pelletGroup.draw(screen)
            self.cherryGroup.draw(screen)
            self.orangeGroup.draw(screen)
            self.ghostGroup.draw(screen)
            screen.blit(self.player.image,self.player.rect)
# CHANGE COORDINATES TO BE IN A BLANK BOX
            self.displayInfo(screen, "Score: ", AQUA, 70, 5)
            self.displayInfo(screen, str(self.score), AQUA, 87, 35)

        # Updates the contents of the entire display
        pygame.display.flip()

    def displayInfo(self, screen, info, color, x, y):
        message = self.font.render(info, True, color)
        screen.blit(message,(x,y))               # Draws the message onto the screen's surface

                            
                    
