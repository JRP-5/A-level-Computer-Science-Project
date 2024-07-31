import pygame


class testPlayer:
    def __init__(self, rotation):
        self.rotation = rotation


# Handles rotation input of the tank
def handleRotationInput(self, inpDict):
    rotationSpeed = 2  # Rendering at 30 FPS causes the tank to rotate 360 degrees in 6 seconds
    addedRotation = 0
    if inpDict[pygame.K_d]:
        addedRotation += 1  # If d is pressed rotate the tank to the right
    if inpDict[pygame.K_a]:
        addedRotation -= 1  # If a is pressed rotate to the left
    self.rotation += addedRotation * rotationSpeed  # Rotate the tank by the calculated amount


inputDict = {  # Test dictionary
    pygame.K_w: False,
    pygame.K_a: False,
    pygame.K_s: True,
    pygame.K_d: True,
    pygame.K_SPACE: False
}

player = testPlayer()