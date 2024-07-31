import pygame
import math


class testPlayer:
    def __init__(self, rotation, velocityX, velocityY):
        self.rotation = rotation
        self.velocityX = velocityX
        self.velocityY = velocityY


# Method which handles user input with respect to tank movement
def handleMovementInput(self, inpDict):
    moveSpeed = 0.5  # Setting a default movement speed
    xMove = 0
    yMove = 0
    if inpDict[pygame.K_w]:
        yMove -= 1  # If W key pressed move forward
    if inpDict[pygame.K_s]:
        yMove += 1  # If S key pressed move backwards

    # Rotating the tank's movement with respect to its rotation
    theta = self.rotation
    self.velocityX = -math.sin(math.radians(theta)) * yMove * moveSpeed
    self.velocityY = math.cos(math.radians(theta)) * yMove * moveSpeed


inputDict = {  # Test dictionary
        pygame.K_w: False,
        pygame.K_a: False,
        pygame.K_s: True,
        pygame.K_d: True,
        pygame.K_SPACE: False
    }
# Creating a test player with rotation 220 degrees and 0 velocity
tank = testPlayer(50, 0, 0)

handleMovementInput(tank, inputDict)
print(round(tank.velocityX, 3), round(tank.velocityY, 3))



