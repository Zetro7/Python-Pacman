# CSC 308 Python
# Rudolph Hanzes, Kristen Hartz, Stacy Hartz
# Final Project

import pygame
from game import playGame

SCREENWIDTH = 608
SCREENHEIGHT = 800

# Pacman Game
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("CSC 308 Final Project: Pacman")
    
gameOver = False
game = playGame()

clock = pygame.time.Clock()         # Manages how fast the screen updates
    
while not gameOver:
    gameOver = game.update()        # Processes updates
    game.runLogic()                 # Runs game
    game.display(screen)            # Updates screen
    clock.tick(45)                  # 45 frames/second

pygame.quit()
