import gameMap


class testProjectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Method to find the shortest point on a given boundary to a projectile
    def getShortestPointProjectileToBoundary(self, bound):
        if bound.boundType == "vertical":
            closestY = self.y
            # Simple logic to determine whether the projectile is inline with the boundary vertically, if it is not we determine which side it is
            if closestY <= bound.minY:
                closestY = bound.minY
            elif closestY >= bound.maxY:
                closestY = bound.maxY
            return [bound.x, closestY]
        else:  # Dealing with a horizontal boundary
            closestX = self.x
            if closestX <= bound.minX:
                closestX = bound.minX
            elif closestX >= bound.maxX:
                closestX = bound.maxX
            return [closestX, bound.y]


proj = testProjectile(35, 44)
bound = gameMap.HorizontalBoundary(42, 20, 60)
print(proj.getShortestPointProjectileToBoundary(bound))
