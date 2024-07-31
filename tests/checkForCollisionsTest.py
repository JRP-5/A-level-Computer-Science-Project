import gameMap


# File for testing the functionality of the checkForCollisons algorithm

# Creating a test tank class so we can test the algorithm
class TestTank:
    def __init__(self, x, y, sizeX, sizeY, velocityX, velocityY, ip):
        self.x = x
        self.y = y
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.ip = ip
        self.type = "tank"

    def checkForCollisions(self, entities, gameMap):
        applyXVelocity = True
        applyYVelocity = True
        # These two loops compare all the entities in the game in the most efficient way
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                if entities[i].type == "projectile" and entities[j].type == "projectile" and self.ip == "localhost":
                    # If the projectiles are touching (using pythagoras' theorem)
                    if (entities[i].x - entities[j].x) ** 2 + (entities[i].y - entities[j].y) ** 2 < (
                            entities[i].sizeX // 2) ** 2:
                        pass
                    # entities[i].destroy() TODO send to clients - only the host should do this
                    # entities[j].destroy()
                # If we are comparing our projectile and a tank
                elif entities[i].type == "projectile" and entities[i].ip == self.ip and entities[j] == "tank":
                    # If they are touching in the x plane
                    touchingX = entities[i].x + (entities[i].sizeX // 2) >= entities[j].x - (entities[j].sizeX // 2) and \
                                entities[i].x - (entities[i].sizeX // 2) <= entities[j].x + (entities[j].sizeX // 2)
                    # If they are touching in the y plane
                    touchingY = entities[i].y + (entities[i].sizeY // 2) >= entities[j].y - (entities[j].sizeY // 2) and \
                                entities[i].y - (entities[i].sizeY // 2) <= entities[j].y + (entities[j].sizeY // 2)
                    # TODO improve using SAT
                    if touchingX and touchingY:
                        pass
                        #  entities[j].verifyDeath()  # TODO
                # If we are comparing our tank and another tank
                elif entities[i].type == "tank" and entities[i].ip == self.ip and entities[j].type == "tank":
                    self.x += self.velocityX  # Apply the movement for this tick
                    # If applying this movement causes a collision
                    if self.tanksColliding(entities[i], entities[j]):
                        applyXVelocity = False  # Remove the movement
                    self.x -= self.velocityX  # Remove the movement afterwards

                    # Doing the same for the y-axis
                    self.y += self.velocityY
                    # If applying this movement causes a collision
                    if self.tanksColliding(entities[i], entities[j]):
                        applyYVelocity = False  # Remove the movement
                    self.y -= self.velocityY  # Remove the movement afterwards

                    # Now we must test whether applying both together causes a collision
                    self.x += self.velocityX
                    self.y += self.velocityY
                    if self.tanksColliding(entities[i], entities[j]):
                        self.y -= self.velocityY
                        # Determining whether a collision is caused after applying the X velocity
                        touchingAfterX = self.tanksColliding(entities[i], entities[j])
                        self.y += self.velocityY
                        # Determining whether a collision is caused after applying the Y velocity
                        touchingAfterY = self.tanksColliding(entities[i], entities[j])
                        # If applying the y velocity causes the collision we can apply the X velocity
                        if not touchingAfterX and touchingAfterY:
                            applyYVelocity = False
                        else:
                            # Otherwise the X velocity must cause the collision so we don't apply that
                            applyXVelocity = False

        # Checking for OUR tank collisions against boundaries
        bnds = gameMap.boundaryList
        for x in range(len(bnds)):
            self.x += self.velocityX  # Temporarily apply the movement
            # If the tank is now touching the boundary
            if self.tankCollidingBoundary(self, bnds[x]):
                applyXVelocity = False  # Cancel the x velocity as it will cause an intersection
            self.x -= self.velocityX

            # Now checking whether the y velocity could cause an intersection
            self.y += self.velocityY  # Temporarily apply the movement
            if self.tankCollidingBoundary(self, bnds[x]):
                applyYVelocity = False  # Cancel the y velocity as it will cause an intersection
            self.y -= self.velocityY  # Remove the velocity

            # Now we must test whether applying both together causes a collision
            self.x += self.velocityX
            self.y += self.velocityY
            if self.tankCollidingBoundary(self, bnds[x]):
                self.y -= self.velocityY
                # Determining whether a collision is caused after applying the X velocity
                touchingAfterX = self.tankCollidingBoundary(self, bnds[x])
                self.y += self.velocityY
                # Determining whether a collision is caused after applying the Y velocity
                touchingAfterY = self.tankCollidingBoundary(self, bnds[x])
                # If applying the y velocity causes the collision we can apply the X velocity
                if not touchingAfterX and touchingAfterY:
                    applyYVelocity = False
                else:
                    # Otherwise the X velocity must cause the collision so we don't apply that
                    applyXVelocity = False

        return applyXVelocity, applyYVelocity

    # Method takes in 2 tanks and returns whether they are colliding or not
    def tanksColliding(self, tank1, tank2):
        return tank1.x + (tank1.sizeX // 2) >= tank2.x - (tank2.sizeX // 2) and tank1.x - (tank1.sizeX // 2) <= tank2.x + (tank2.sizeX // 2) and tank1.y + (tank1.sizeY // 2) >= tank2.y - (tank2.sizeY // 2) and tank1.y - (tank1.sizeY // 2) <= tank2.y + (tank2.sizeY // 2)

    # Method which takes in a tank and a boundary and returns whether they are colliding or not
    def tankCollidingBoundary(self, tank, bound):
        if bound.boundType == "vertical":  # Dealing with a vertical boundary
            return tank.x - (tank.sizeX // 2) <= bound.x <= tank.x + (tank.sizeX // 2) and tank.y - (
                        tank.sizeY // 2) <= bound.maxY and tank.y + (tank.sizeY // 2) >= bound.minY
        else:  # Dealing with a horizontal boundary
            return tank.y - (tank.sizeY // 2) <= bound.y <= tank.y + (tank.sizeY // 2) and tank.y - (
                        tank.sizeY // 2) <= bound.maxX and tank.y + (tank.sizeY // 2) >= bound.minX


# Test no 7
testTank = TestTank(40, 40, 11, 11, 0, -1, "localhost")  # Create a tank that belongs to us
testTank2 = TestTank(28, 42, 11, 11, 0, 0, "8373737")  # Create another tank to test against
entityList = [testTank, testTank2]  # Create an entity list to pass to the function
gameMap = gameMap.getMap()
gameMap.boundaryList = []  # Create an empty boundary list
result = testTank.checkForCollisions(entityList, gameMap)
print(result)


# # Test no 5
# # Creating a boundary list for testing
# testTank = TestTank(40, 40, 11, 11, 0, -1, "localhost")  # Create a tank that belongs to us
# bnd = gameMap.HorizontalBoundary(33, 30, 50)
# gameMap = gameMap.getMap()  # Create a map to pass to the function
# gameMap.boundaryList = [bnd]  # Change that boundary list to our test data
# # Call the algorithm with an empty entity list and our test map
# result = testTank.checkForCollisions([], gameMap)
# print(result)



