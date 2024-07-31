import entity
import math
import gameMap


class Projectile(entity.Entity):
    def __init__(self, x, y, angle, ip):
        super().__init__(x, y, "projectile")  # Create superclass
        self.x = x  # Save arguments
        self.y = y
        self.moveSpeed = 8
        self.ip = ip
        self.bounced = 0
        self.sizeX = 10
        self.sizeY = 10
        self.velocityX = 0  # Set the projectile as moving straight upwards
        self.velocityY = -1
        self.velocityX = -math.sin(math.radians(angle))  # Rotate it
        self.velocityY = math.cos(math.radians(angle))

    def tickProjectile(self, boundaryList):
        self.x += self.velocityX
        self.y += self.velocityY
        bounced = False  # This variable tracks whether a projectile has bounced in a certain frame
        destroyed = False  # Tracks whether a projectile has been destroyed or not
        for bound in boundaryList:  # Cycles through every boundary on the map to detect whether the projectile has hit it and so must bounce off it
            if destroyed:
                break
            if bound.boundType == "vertical":
                # If the distance between the projectile and the boundary in the x axis is less than the radius of the projectile then we per form a more precise collision check
                if abs(bound.x - self.x) < self.sizeX:
                    point = self.getShortestPointProjectileToBoundary(bound)
                    # If the distance from the prjectile to the boundary is less than the projectile's radius the
                    # projectile must be touching the boundary
                    # So we make it bounce assuming it has not done so already this tick
                    if (self.x - point[0])**2 + (self.y - point[1])**2 <= self.sizeX**2 and not bounced:
                        # Bouncing the projectile
                        if self.bounced > 2:  # If the projectile is now touching a boundary and it has already bounced twice it should be destroyed
                            self.destroy()
                        if point[1] == bound.minY or point[1] == bound.maxY:  # Dealing with the case that the projectile is touching the end of a boundary
                            # Finding theta, the angle of projectile approach
                            theta = math.asin(math.radians(abs(bound.x - self.x)/math.sqrt(self.x - point[0])**2 + (self.y - point[1])**2))
                            if theta > 45:  # If angle of approach is greater than 45
                                self.velocityX *= -1  # Flip X velocity to make it bounce off the side of the boundary
                            elif theta < 45:  # If the angle of approach is less than 45
                                self.velocityY *= -1  # Flip the Y velocity to make it bounce of the end of the boundary
                            else:
                                self.velocityX *= -1  # If approaching at exactly 45 degrees flip both of them
                                self.velocityY *= -1
                        else:
                            self.velocityX *= -1  # If closest point is on the side then flip the X velocity
                        self.bounced += 1
                        bound = True

            else:  # Dealing with a horizontal boundary
                if abs(bound.y - self.y) < self.sizeY and not bounced:  # Here we use a comparison to avoid comparing projectiles which are definitely not touching the boundary
                    point = self.getShortestPointProjectileToBoundary(bound)
                    if (self.x - point[0])**2 + (self.y - point[1]) ^ 2 <= self.sizeY**2:  # If the projectile is touching the boundary
                        if self.bounced > 2:
                            self.destroy()
                        if point[0] == bound.minX or point[0] == bound.maxX:
                            theta = math.asin(math.radians(abs(bound.y - self.y)/math.sqrt((self.x - point[0])**2 + (self.y - point[1])**2)))
                            if theta > 45:
                                self.velocityY *= -1  # Flip velocity in Y direction
                            elif theta < 45:
                                self.velocityX *= -1  # Flip in X direction
                            else:
                                self.velocityX *= -1  # Hitting a corner of the boundary so reverse both
                                self.velocityY *= -1
                        else:
                            self.velocityY *= -1
                        self.bounced += 1
                        bound = True

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

    def destroy(self):
        pass  # TODO


proj = Projectile(18, 42, 0, None)
proj.sizeX = 5
proj.sizeY = 5
proj.velocityX = 1
proj.velocityY = 0
boundList = [gameMap.HorizontalBoundary(42, 20, 60)]
proj.tickProjectile(boundList)
print(proj.velocityX, proj.velocityY)

