import gameMap


class testTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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


tank = testTank(40, 40)
boundary = gameMap.HorizontalBoundary(70, 20, 50)
print(tank.getShortestPointToBoundary(boundary))


