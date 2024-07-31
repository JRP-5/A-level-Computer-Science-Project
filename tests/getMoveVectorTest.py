import math
import sys
sys.path.insert(0, 'F:/Pycharm/Projects/Tanks/src/')
import gameMap
import projectile


class testTank:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.type = "tank"

    def getMoveVector(self, entityList, boundaryList):
        moveVectorX = 0
        moveVectorY = 0
        dangerDist = 20
        for ent in entityList:
            if ent.type == "projectile":
                grad = ent.velocityY / ent.velocityX
                intersectionX = (grad * ent.x - ent.y + (self.x / grad) + self.y) / (grad + (1 / grad))
                intersectionY = grad * (intersectionX - ent.x) + ent.y
                # The above lines find the shortest path from the tank to the projectile's path via substitution
                # This is so we can find the shortest distance from the tank to the projectile
                if (self.x - intersectionX) ** 2 + (self.y - intersectionY) ** 2 < dangerDist**2:
                    # If the shortest distance to the projectile's path is less than 20
                    if intersectionX - self.x < 0:  # Finding the 2d vector from the tank to the bullet's path
                        moveVectorX -= dangerDist + (intersectionX - self.x)
                    elif intersectionX - self.x > 0:
                        moveVectorX += dangerDist - (intersectionX - self.x)
                    # Adjusting the size of the direction vector based on how far the danger is
                    if intersectionY - self.y < 0:
                        moveVectorY -= dangerDist + (intersectionY - self.y)
                    elif intersectionY - self.y > 0:
                        moveVectorY += dangerDist - (intersectionY - self.y)
                    if intersectionX - self.x == 0 and intersectionY - self.y == 0:  # If they are both zero
                        moveVectorX += 20
                        moveVectorY += 20
            elif ent.type == "tank" and ent.team != self.team:
                dist = math.sqrt((ent.x - self.x) ** 2 + (ent.y - self.y) ** 2)  # Finding the distance between the 2 tanks
                if dist < dangerDist:  # If the distance between the 2 tanks is less than 20
                    if ent.x - self.x < 0:
                        moveVectorX -= dangerDist + (ent.x - self.x)  # same as with projectiles above
                    elif ent.x - self.x > 0:
                        moveVectorX += dangerDist - (ent.x - self.x)
                    # Adjusting the size of the direction vector based on how far the danger is
                    if ent.y - self.y < 0:
                        moveVectorY -= dangerDist + (ent.y - self.y)
                    elif ent.y - self.y > 0:
                        moveVectorY += dangerDist - (ent.y - self.y)
        for bound in boundaryList:  # TODO fix once implemented method
            # Finds the point on the boundary closest to the tank
            point = self.getShortestPointToBoundary(bound)
            if (point[0] - self.x) ** 2 + (point[1] - self.y) ** 2 < dangerDist ** 2:
                deltaX = point[0] - self.x  # Finding the distance between the 2 points on the boundary and tank
                deltaY = point[1] - self.y
                if deltaX < 0:
                    moveVectorX -= dangerDist + deltaX
                elif deltaX > 0:
                    moveVectorX += dangerDist - deltaX
                if deltaY < 0:
                    moveVectorY -= dangerDist + deltaY
                elif deltaY > 0:
                    moveVectorY += dangerDist - deltaY
        return [moveVectorX, moveVectorY]

    def getShortestPointToBoundary(self, bound):
        if bound.boundType == "vertical":
            # Finding the closest distance from the tank to an infinitely long boundary
            closestY = self.y
            if closestY <= bound.minY:
                # IF the tank's Y value is less than the boundary's minimum value the closest point must be the boundary's minimum value
                closestY = bound.minY
            elif closestY >= bound.maxY:
                # If the tank's Y value is past the max boundary Y the closest Y value is the boundary's max Y value
                closestY = bound.maxY
            return [bound.x, closestY]
        else:  # Dealing with a horizontal boundary
            # Same as with a vertical boundary but rotated 180 degrees in the x plane
            closestX = self.x
            if closestX <= bound.minX:
                closestX = bound.minX
            elif closestX >= bound.maxX:
                closestX = bound.maxX
            return [closestX, bound.y]


# Test 1.1
AITank = testTank(40, 40, "AI")
proj = projectile.Projectile(30, 30, 0, "none", "none")
proj.velocityX = 0.707
proj.velocityY = 0.707
entities = [testTank(50, 50, "other"), testTank(23, 40, "other"), proj]
boundaries = [gameMap.HorizontalBoundary(55, 30, 50)]
print("Test 1.1", AITank.getMoveVector(entities, boundaries))

# Test 1.2
AITank = testTank(40, 40, "AI")
proj = projectile.Projectile(30, 30, 0, "none", "none")
proj.velocityX = 0.866
proj.velocityY = 0.5
entities = [proj]
boundaries = []
print("Test 1.2", AITank.getMoveVector(entities, boundaries))

# Test 2.1
AITank = testTank(40, 40, "AI")
entities = [testTank(60, 60, "other")]
boundaries = [gameMap.HorizontalBoundary(65, 30, 50)]
print("Test 2.1", AITank.getMoveVector(entities, boundaries))
