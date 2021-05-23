import pygame
import math
from draw import *
from button import *

WHITE = (255,255,255)
RED = (255,0,0)
HALFRED = (128, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
LIME = (81, 255, 13)
G = 2

class Object:
    """
    Super class for objects that appear on the screen
    """
    def __init__(self, x: int, y: int, radius: int, mass: float, color: tuple = HALFRED):
        # x,y coordinate of the center of the object
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.glow = False
        self.show_stats = False
        self.obj_on_mouse = False

    def setPosition(self, pos: tuple):
        """
        Sets the position of the object to the given position
        """
        self.x = pos[0]
        self.y = pos[1]

    def setMass(self, mass: float):
        """
        Sets the mass of the object to the given mass
        """
        self.mass = mass

    def display(self, win):
        """
        Displays the object as a circle at the location (x,y)
        """

        pygame.gfxdraw.aacircle(win, int(self.x), int(self.y), self.radius, self.color)
        pygame.gfxdraw.filled_circle(win, int(self.x), int(self.y), self.radius, self.color)
        # if self.glow is true, draw a outline 
        if (self.glow):
            pygame.gfxdraw.circle(win, int(self.x), int(self.y), self.radius, (255-self.color[0], 255-self.color[1], 255-self.color[2]))
        # display info_box
        if (self.show_stats):
            self.info_box.display(win)

    def findForce(self, obj: object):
        """
        Returns the force exerted by obj onto self
        """
        return (G * self.mass * obj.mass / (math.pow(obj.x - self.x, 2) + math.pow(obj.y - self.y, 2)))

    def findUnitDist(self, obj: object):
        """
        return the unit vector <x, y> pointing in the direction of the given obj
        """
        dist = math.sqrt((obj.x - self.x)**2 + (obj.y - self.y)**2)
        return (obj.x - self.x) / dist, (obj.y - self.y) / dist

    def mouseOnObj(self, pos: tuple):
        """
        Returns true if the given position is on the object, false otherwise
        """
        return ((pos[0] - self.x)**2 + (pos[1] - self.y)**2 <= self.radius**2)

    def getButtons(self):
        """
        Returns the buttons in the object's InfoBox
        """
        return self.info_box.getButtons()

    def getType(self):
        """
        Returns a character refering to the object's type
        """ 
        return "O"

    def update(self):
        pass

    def updateTrial(self):
        pass

    def updateColor(self):
        self.color = self.info_box.getColor()

    def resetTrial(self):
        pass

    def displayTrial(self, win):
        pass

    def drawVelocity(self, win):
        pass


class Attractor(Object):
    """
    An Attractor stays at rest and does not move but exerts force onto other objects
    """
    def __init__(self, x: int, y: int, radius: int, mass: float = 200, color: tuple = HALFRED):
        super().__init__(x, y, radius, mass, color)
        self.info_box = InfoBox(self)

    def getType(self):
        return "A"


class Planet(Object):
    """
    A Planet objects stores an object that can move
    """
    def __init__(self, x: int, y: int, radius: int, velx: float = 0, vely: float = 0, 
                accx: float = 0, accy: float = 0, mass: float = 1, color: tuple = BLUE):
        super().__init__(x, y, radius, mass, color)
        self.velx = velx
        self.vely = vely
        self.accx = accx
        self.accy = accy
        # trial is a list of a tuple containing the position and color of every past position of the planet
        self.trial = []

        self.info_box = InfoBox(self)

    def getType(self):
        return "P"

    def setMass(self, mass: float):
        """
        changes the mass
        """
        self.mass = mass

    def setVelocity(self, vx: float, vy: float):
        """
        Sets the velocity of object with the given components
        """
        self.velx = vx
        self.vely = vy

    def getVelocityMagnitude(self):
        """
        Returns the magnitude of the object's velocity
        """
        return (sqrt(self.velx**2 + self.vely**2))

    def getVelocityAngle(self):
        """
        Returns the direction of object's velocity in degrees
        """
        ang = -1 * math.atan2(self.vely , self.velx)
        if (ang < 0):
            ang += 2*math.pi
        return math.degrees(ang)

    def update(self):
        """
        updates the velocity and position
        """
        if (not self.obj_on_mouse):
            self.velx += self.accx
            self.vely += self.accy
            self.x += self.velx
            self.y += self.vely

    def updateTrial(self):
        """
        Updates the trial of object
        """
        # insert the current position in the trial
        self.trial.insert(0, [(int(self.x), int(self.y)), 160])
        # remove the last trial if longer than 160
        if (len(self.trial) >= 159):
            self.trial.pop()
        # decrease the color value by 1
        for trl in self.trial:
            trl[1] -=1

    def resetTrial(self):
        """
        Resets the trial by emptying it
        """
        self.trial = []


    def updateAcc(self, accx: float, accy: float):
        """
        Sets the acceleration to the given values
        """
        self.accx = accx
        self.accy = accy

    def drawVelocity(self, win):
        """
        Draws a arrow representing the velocity, proportional to velocity's magnitude
        """
        vel_mag = math.sqrt(self.velx**2 + self.vely**2)
        drawArrow(win, self.x, self.y, vel_mag*10, (self.velx, self.vely))

    def displayTrial(self, win):
        """
        Displays the trial of the planet
        """
        # for each instance, a line is drawn from previous to the next
        # then, it's color is decreased by one
        for i in range(len(self.trial) - 1):
            color_temp = (self.trial[i][1], self.trial[i][1], self.trial[i][1])
            pygame.draw.line(win, color_temp, self.trial[i][0], self.trial[i+1][0], 3)         
