import pygame
import math
from pygame.locals import *

SCREEN = (1000, 600)
BG = (0, 0, 0)

class Button:
    """
    Acts as a super class for button types
    """
    def __init__(self, x: int, y: int):
        # x,y represent the position of the button rect
        self.x = x
        self.y = y

    def mouseOnButton(self, pos: tuple):
        pass

    def display(self):
        pass

        
class TextButton(Button):
    """
    Stores the properties of a text button.
    """
    def __init__(self, x: int, y: int, text: str, purpose: int, 
                myfont: str = "Comic Sans MS", font_size: int = 15, 
                textcolor: tuple = (255, 0, 0), bgcolor: tuple = (255, 255, 255), cursor_type = pygame.SYSTEM_CURSOR_HAND):
        super().__init__(x, y)
        # defalult_bgcolor stores the background color given by the user
        # bgcolor stores the current color of the button used for displaying purposes,
        # this may be different from defalult_bgcolor when the user cursor is on the button
        self.default_bgcolor = bgcolor
        self.bgcolor = bgcolor
        # x and y coordinate of the button
        self.x = x
        self.y = y
        # color of the text on the button
        self.textcolor = textcolor
        # actual text on the button
        self.text = text
        # font and font size of the text
        self.font = myfont
        self.font_size = font_size
        # create the text
        self.updateText()
        # create the background rectangle
        self.updateRect()
        # cursor type is what the user cursor should look when hovering over the button
        self.cursor_type = cursor_type
        # purpose is an integer refering to what the button does when pressed
        self.purpose = purpose

    def updateText(self):
        """
        Updates the text with its data members
        """
        self.myfont = pygame.font.SysFont(self.font, self.font_size)
        self.mytext = self.myfont.render(" " + self.text + " ", False, self.textcolor, self.bgcolor)

    def updateRect(self):
        """
        Updates the rectangle with its data members
        """
        self.myrect = self.mytext.get_rect()
        self.myrect.topleft = (self.x, self.y)

    def updateColor(self, color: tuple):
        """
        Updates the color of rectangle to the given color
        """
        self.bgcolor = color
        self.updateText()
        self.updateRect()

    def updateTextColor(self, color: tuple):
        """
        Updates the color of the text with the given color
        """
        self.textcolor = color
        # update the text to apply the change
        self.updateText()

    def getHalfColor(self, color: tuple):
        """
        Returns a color with half the r,g, and b values
        """
        return (int(color[0]/2)), int(color[1]/2), int(color[2]/2)

    def mouseOnButton(self, pos: tuple):
        """
        Returns True if the given position is on the text rectangle, false otherwise
        """
        return self.myrect.collidepoint(pos)

    def display(self, win):
        """
        Displays the text onto the window
        """
        # first display the background rectangle, then blit the text at the same location
        #pygame.draw.rect(win, self.bgcolor, pygame.Rect(self.myrect))
        win.blit(self.mytext, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), self.myrect.copy(), 1)
    

class InputBox(TextButton):
    """
    A button where the user can type give input
    """
    def __init__(self, x: int, y: int, text: str, purpose: int, 
                myfont: str = "Comic Sans MS", font_size: int = 15, 
                textcolor: tuple = (255,0,0), bgcolor: tuple = (255,255,255), cursor_type = pygame.SYSTEM_CURSOR_IBEAM):
        super().__init__(x, y, text, purpose, myfont=myfont, font_size=font_size, textcolor=textcolor, bgcolor=bgcolor, cursor_type=cursor_type)
        # is_typing indicats if the user is typing on this button
        self.is_typing = False

    def display(self, win):
        """
        Displays the input button on the window
        """
        # if the user is typing on this box, set the color to half color regardless of where the mouse on the button
        if (self.is_typing):
            self.updateColor(self.getHalfColor(self.default_bgcolor))
        else:
            self.updateColor(self.default_bgcolor)
        super().display(win)
    

class InfoBox:
    """
    Infobox stores the properties of an object and takes any input to change the object's properties
    """
    def __init__(self, obj: object):
        self.obj = obj
        # input boxes
        self.iboxes = []
        # length of iboxes
        self.size = 0
        # color of the object and stores the input color
        self.temp_color = self.colorToString(obj.color)
        # mass of the object and stores the input mass
        self.temp_mass = str(obj.mass)
        self.checkVelocity()
        self.defaultButtons()

    def checkVelocity(self):
        """
        Check if the object is a planet, and defines velocity and angle if it is
        """
        if (self.obj.getType() == "P"):
            self.vel = str(self.obj.getVelocityMagnitude())[:4]
            self.angle = str(self.obj.getVelocityAngle())[:3]

    def addBox(self, bx: Button):
        """
        Adds the given button/box to the list and increments size
        """
        self.iboxes.append(bx)
        self.size += 1

    def resetToObject(self):
        """
        Resets the color and mass to the object's color and mass
        """
        # get color and mass from object
        self.temp_color = self.colorToString(self.obj.color)
        self.temp_mass = str(self.obj.mass)
        for button in self.iboxes:
            if (button.purpose == 401):
                button.text = self.colorToString(self.obj.color)
            elif (button.purpose == 402):
                button.text = str(self.obj.mass)
            # no need to update velocity and angle since it's done every frame anyways
            # update the text on the button
            button.updateText()

    def colorToString(self, color: tuple):
        """
        Returns the given color tuple as string
        """
        return str(color[0]) + ", " + str(color[1]) + ", " + str(color[2])

    def stringToColor(self, str: str):
        """
        Returns the given string as color tuple
        """
        temp = str.split(",")
        return (int(temp[0]), int(temp[1]), int(temp[2]))

    def getColor(self):
        """
        Returns the stored string color as a tuple
        """
        return self.stringToColor(self.temp_color)

    def isValidColor(self, color: str):
        """
        Returns True if the given string color is a valid color
        """
        try:
            temp = [int(i.strip()) for i in color.split(",")]
            if (len(temp) != 3):
                return False
            for i in temp:
                if not (0 <= i <= 255):
                    return False
            return True
        except:
            return False

    def updateColor(self, event_key):
        """
        Updates the color with the given input from keyboard
        Returns False if the user presses Enter, True otherwise
        """
        if (event_key == K_RETURN):
            # if the user presses enter but the color is not valid, reset the color
            if not self.isValidColor(self.temp_color):
                self.temp_color = self.colorToString(self.obj.color)
            self.iboxes[1].text = self.temp_color
            self.iboxes[1].is_typing = False
            self.iboxes[1].updateColor(self.iboxes[1].default_bgcolor)
            self.obj.updateColor()
            return False
        elif (event_key == K_BACKSPACE):
            # delete last character if backspace is pressed
            self.temp_color = self.temp_color[:-1]
        elif ((48 <= event_key <= 57) or (event_key == 44) or (event_key == 32)):
            # add letter if it is a digit, a comma, or a space character
            self.temp_color += chr(event_key)

        # update text of the input box
        self.iboxes[1].text = self.temp_color
        self.iboxes[1].updateText()
        return True

    def isValidMass(self, mass_string: str):
        """
        Returs True if the given mass as a string is valid, False otherwise
        """
        try:
            mass = float(mass_string)
            if (mass < 0):
                return False
            return True
        except:
            return False

    def updateMass(self, event_key):
        """
        Updates the mass with the given input from keyboard
        Returns False if the user presses Enter, True otherwise
        """
        if (event_key == K_RETURN):
            # if the user presses enter but the mass is not valid, reset the mass
            if not (self.isValidMass(self.temp_mass)):
                self.temp_mass = str(self.obj.mass)
            self.iboxes[2].text = self.temp_mass
            self.iboxes[2].is_typing = False
            self.iboxes[2].updateColor(self.iboxes[2].default_bgcolor)
            self.obj.setMass(float(self.temp_mass))
            return False
        elif (event_key == K_BACKSPACE):
            # delete last character if backspace is pressed
            self.temp_mass = self.temp_mass[:-1]
        elif ((48 <= event_key <= 57) or (event_key == 46)):
            # add the digit if it is a digit or a period
            self.temp_mass += chr(event_key)
        # update text of input box
        self.iboxes[2].text = self.temp_mass
        self.iboxes[2].updateText()
        return True

    def isValidNumber(self, num: str):
        """
        Returns true if the given string is a valid number, False otherwise
        """
        try:
            float(num)
            return True
        except:
            return False

    def updateVelocity(self, event_key):
        if (event_key == K_RETURN):
            # if the user presses enter but the velocity is not valid, reset the velocity
            if not (self.isValidNumber(self.vel)):
                self.vel = str(self.obj.getVelocityMagnitude())[:4]
            # set the velocity of object to what the user entered
            self.obj.setVelocity(float(self.vel)*math.cos(math.radians(float(self.angle))), -float(self.vel)*math.sin(math.radians(float(self.angle))))
            self.iboxes[3].text = self.vel
            self.iboxes[3].is_typing = False
            self.iboxes[3].updateColor(self.iboxes[3].default_bgcolor)
            return False
        elif (event_key == K_BACKSPACE):
            # delete last character if backspace is pressed
            self.vel = self.vel[:-1]
        elif ((48 <= event_key <= 57) or (event_key == 46)):
            # add the digit if it is a digit or a period
            self.vel += chr(event_key)
        # update the text of input box
        self.iboxes[3].text = self.vel
        self.iboxes[3].updateText()
        return True

    def updateAngle(self, event_key):
        if (event_key == K_RETURN):
            # if the user presses enter but the angle is not valid, reset the angle
            if not (self.isValidNumber(self.angle)):
                self.angle = str(self.obj.getVelocityAngle())[:3]
            # set the velocity of object based on the angle user entered
            self.obj.setVelocity(float(self.vel)*math.cos(2*math.pi - math.radians(float(self.angle))), float(self.vel)*math.sin(2*math.pi - math.radians(float(self.angle))))
            self.iboxes[4].text = self.angle + "°"
            self.iboxes[4].is_typing = False
            self.iboxes[4].updateColor(self.iboxes[3].default_bgcolor)
            return False
        elif (event_key == K_BACKSPACE):
            # delete last character if backspace is pressed
            self.angle = self.angle[:-1]
        elif ((48 <= event_key <= 57) or (event_key == 46)):
            # add the digit if it is a digit or a period
            self.angle += chr(event_key)
        # update text of the box
        self.iboxes[4].text = self.angle + "°"
        self.iboxes[4].updateText()
        return True

    def takeInput(self, event_key, purpose_num: int):
        """
        Calls the correct function based on which button is pressed
        """
        # color button has purpose 401
        if (purpose_num == 401):
            return self.updateColor(event_key)
        # mass button has purpose 402
        elif (purpose_num == 402):
            return self.updateMass(event_key)
        # velocity button has purpose 403
        elif (purpose_num == 403):
            return self.updateVelocity(event_key)
        # angle button has purpose 404
        elif (purpose_num == 404):
            return self.updateAngle(event_key)


    def defaultButtons(self):
        """
        Sets up input boxes
        """
        self.addBox(TextButton(SCREEN[0] - 200, 0, "Close", purpose=499, font_size = 10))
        self.addBox(InputBox(SCREEN[0] - 150, 30, self.temp_color, purpose = 401, font_size=12))
        self.addBox(InputBox(SCREEN[0] - 150, 50, self.temp_mass, purpose = 402, font_size=12 ))
        # if the object is an planet, add velocity and angle input boxes
        if (self.obj.getType() == "P"):
            self.addBox(InputBox(SCREEN[0] - 150, 70, self.vel, purpose = 403, font_size=12))
            self.addBox(InputBox(SCREEN[0] - 90, 70, self.angle + "°", purpose = 404, font_size=12))
        self.rect = pygame.Rect(SCREEN[0] - 200, 0, 150, 100)

    def update(self):
        """
        Updates the velocity and angle values based on object's values
        """
        for button in self.iboxes[1:]:
            # if the user is not typing and it is a velocity box (purpose is 403), update the box
            if (not button.is_typing and button.purpose == 403):
                self.vel = str(self.obj.getVelocityMagnitude())[:4]
                button.text = self.vel
                button.updateText()
            # if the user is not typing and it is a angle box (purpose is 404), update the box
            elif (not button.is_typing and button.purpose == 404):
                self.angle = str(self.obj.getVelocityAngle())[:3]
                button.text = self.angle + "°"
                button.updateText()

    def getButtons(self):
        """
        Returns the list of buttons and boxes
        """
        return self.iboxes

    def display(self, win):
        """
        Displays the text and outline for the infoBox
        """
        pygame.draw.rect(win, (250, 250, 250), self.rect, 2)
        win.blit((pygame.font.SysFont("calibri", 17)).render(" Color:", False, (255,100,100), BG), (SCREEN[0] - 195, 32))
        win.blit((pygame.font.SysFont("calibri", 17)).render(" Mass:", True, (255,100,100), BG), (SCREEN[0] - 195, 52))
        if (self.obj.getType() == "P"):
            win.blit((pygame.font.SysFont("calibri", 12)).render(" Velocity:              @", True, (255,100,100)), (SCREEN[0] - 195, 75))
