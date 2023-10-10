import pygame
import math

# Pygame presets
pygame.init()
WIDTH, HEIGHT = 1720, 880  
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

class Planet:
    AU = 149.6e6 * 1000 # Distance in meters from the Earth to the Sun
    G = 6.67428e-11 # Gravitational Constant
    SCALE = 25 / AU # Defines how many pixels represent an Astronomical Unit
    TIMESTEP =  3600*24*5
    # Change the scale value to make the model smaller or bigger, keeping apropriate proportions
    # Change the timestep to make the model travel faster or slower on time

    def __init__(self, x, y, radius, mass, color):
        self.x = x
        self.y = y
        self.radius = radius # m
        self.mass = mass # Kg
        self.color = color
        self.xVel = 0
        self.yVel = 0
        self.isSun = False
        self.distanceToSun = 0
        self.orbit = []

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)
    
    def attraction(self, other):
        # Caclulates the distance between one planet to another:
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.isSun:
            self.distanceToSun = distance

        # Calculates the gravitational force between planets:
        force = (self.G * self.mass * other.mass) / (distance ** 2)

        # Splits the force vector into X and Y vectors
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def updatePosition(self, planets):
        # Total force components
        total_fx = total_fy = 0
        
        for planet in planets:
            if self != planet:
                # Calculates the gravitational attraction between self and the current planet
                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy

        # Updates the velocity components based on the total forces
        self.xVel += total_fx / self.mass * self.TIMESTEP
        self.yVel += total_fy / self.mass * self.TIMESTEP

        # Updates the position of the planet based on the new velocity
        self.x += self.xVel * self.TIMESTEP
        self.y += self.yVel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    # Planet: x, y, radius, mass, color

    sun = Planet(0, 0, 7.5, 1.98892 * 10**30, YELLOW)
    sun.isSun = True

    mercury = Planet(-0.39 * Planet.AU, 0, 2, 3.3011 * 10**23, DARK_GREY)
    venus = Planet(-0.72 * Planet.AU, 0, 3, 4.8675 * 10**24, ORANGE)
    earth = Planet(-1 * Planet.AU, 0, 4, 5.9742 * 10**24, BLUE)
    mars = Planet(-1.524 * Planet.AU, 0, 3, 6.39 * 10**23, RED)
    jupiter = Planet(-5.203 * Planet.AU, 0, 5, 1.898 * 10**27, ORANGE)
    saturn = Planet(-9.537 * Planet.AU, 0, 4.5, 5.683 * 10**26, GOLD)
    uranus = Planet(-19.22 * Planet.AU, 0, 3.5, 8.681 * 10**25, LIGHT_BLUE)
    neptune = Planet(-30.05 * Planet.AU, 0, 3.5, 1.02413 * 10**26, DARK_BLUE)

    earth.yVel = 29.783 * 1000
    mars.yVel = 24.077 * 1000
    mercury.yVel = 47.4 * 1000
    venus.yVel = 35.02 * 1000
    jupiter.yVel = 13.07 * 1000  
    saturn.yVel = 9.69 * 1000
    uranus.yVel = 6.81 * 1000 
    neptune.yVel = 5.43 * 1000  # m/s


    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60) # Limits the loop execution to 60Hz
        WIN.fill((0, 0, 0))

        for event in pygame.event.get(): # Stops while run loop in a quit event
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.updatePosition(planets)
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()

main()