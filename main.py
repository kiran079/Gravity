import pygame
from game_file import *

# initialize pygame
pygame.init()
window = pygame.display.set_mode(SCREEN)

pygame.display.set_caption("Planet simulation")

# initialize a Game object and call mainMenu
game = Game(window)
game.mainMenu()

pygame.quit()