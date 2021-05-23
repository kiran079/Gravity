import time
from pygame.locals import *
from classes import *
from button import *
import math as mth

class Game:
    """
    Contains the game loop 
    """
    def __init__(self, window):
        # window to display on
        self.window = window
        # stores all the objects on the screen
        self.objects = []
        # stores all the buttons on the screen
        self.buttons = []
        # boolean indicating whether trial should be shown
        self.show_trial = True
        self.running = True
        # indicates whether velocity arrow should be drawn
        self.draw_velocity = True
        # indicates if the user has paused
        self.paused = False
        # indicates if the user is typing
        self.is_typing = False
        # stores the object that the user has pressed and moved
        self.obj_on_mouse = None
        # stores the object whose stats are shown
        self.showing_stat_of = None
        # stores the button that is pressed
        self.pressedButton = None
        # indicates which menu the user navigates to
        self.menu_choice = -1
        # indicates if the user is relocating an object
        self.relocating = False

    def reset(self):
        """
        Clears objects and buttons, and resets all values to default
        """
        self.objects = []
        self.buttons = []
        self.show_trial = True
        self.running = True
        self.draw_velocity = True
        self.paused = False
        self.show_trial = True
        self.is_typing = False
        self.obj_on_mouse = None
        self.showing_stat_of = None
        self.relocating = False


    def addObject(self, obj: Object):
        """
        Adds the given object to the object list
        """
        self.objects.append(obj)

    def addButton(self, button: Button):
        """
        Adds the given button to the button list
        """
        self.buttons.append(button)

    def update(self):
        """
        Updates the positions of the objects 
        """
        # iterate through every object in self.objects
        for i in range(len(self.objects)):
            # ingore attractor since their position does not change
            if type(self.objects[i]) == Attractor:
                continue
            temp_accx = 0
            temp_accy = 0
            # for every other object, calculate the force exerted onto the current object
            for j in range(len(self.objects)):
                if (i != j):
                    # get the magnitude of the force
                    force = self.objects[i].findForce(self.objects[j])
                    # get the direction of the force
                    unit_direction = self.objects[i].findUnitDist(self.objects[j])
                    # add the components to their respective variables
                    temp_accx += unit_direction[0] * force / self.objects[i].mass
                    temp_accy += unit_direction[1] * force / self.objects[i].mass
            # update the object's acceleration
            self.objects[i].updateAcc(temp_accx, temp_accy)

        for obj in self.objects:
            # use the object's update function to update velocity and position
            obj.update()
            obj.info_box.update()
            # update trial if show_trial is true, empty the trial otherwise
            if (self.show_trial):
                obj.updateTrial()
            else:
                obj.resetTrial()
            
    def renderCenterOfMass(self):
        """
        Displays the center of mass of the system as a circle
        """
        if len(self.objects) == 0:
            return

        # track the m*r in x direction and y direction and track the total mass
        x_total = 0.0
        y_total = 0.0
        mass_total = 0.0
        for obj in self.objects:
            # ignore attractors
            if type(obj) == Attractor:
                continue
            x_total += obj.x * obj.mass
            y_total += obj.y * obj.mass
            mass_total += obj.mass
        # sum of m*r / M
        x_cm = int(x_total / mass_total)
        y_cm = int(y_total / mass_total)

        # draw the center of mass
        pygame.draw.circle(self.window, BLUE, (x_cm, y_cm), 5)

    def render(self):
        """
        Displays the objects and buttons
        """
        # fill the background
        self.window.fill(BLACK)
        # display the trial
        if (self.show_trial):
            for obj in self.objects:
                obj.displayTrial(self.window)

        # display the object
        for obj in self.objects:
            obj.display(self.window)
        # draw the velocity arrow if the toggle is on
        if (self.draw_velocity):
            for obj in self.objects:
                obj.drawVelocity(self.window)
        # draw the button on the screen
        for button in self.buttons:
            button.display(self.window)

        # renders object on mouse when the user is creating custom system
        self.renderObjOnMouse()
        pygame.display.update()

    def addBasicButtons(self):
        """
        Adds some baasic buttons to the list
        """
        self.addButton(TextButton(10, 10, "Toggle Arrow", 0))
        self.addButton(TextButton(20 + self.buttons[0].myrect.width, 10, "Toggle Trial", 1))
        self.addButton(TextButton(30 +self.buttons[0].myrect.width+self.buttons[1].myrect.width, 10, "Play/Pause", 2))

    def basicSetup(self):
        """
        Setup of a system with Sun, planet, and moon
        """
        self.addBasicButtons()
        mass_attractor = 400
        self.addObject(Attractor(400, 300, 20, mass = mass_attractor, color=YELLOW))
        vel_temp = mth.sqrt(G * mass_attractor / (500 - 300))
        mass_planet = 10
        self.addObject(Planet(400, 500, 7, velx = vel_temp, color = BLUE, mass=mass_planet))
        vel_temp_moon = vel_temp + mth.sqrt(G * mass_planet / (515 - 500))
        self.addObject(Planet(400, 515, 3, velx = vel_temp_moon, color = GREEN, mass = 0.1))

    def binarySun(self):
        """
        Binary sun system with a planet rotating around them
        """
        self.addBasicButtons()
        self.addObject(Planet(350, 280, 10, vely=1.4, color = BLUE, mass = 200))
        self.addObject(Planet(400, 300, 10, vely=-1.4, color = YELLOW, mass=200))
        self.addObject(Planet(400, 450, 6, velx = 2.4, color = GREEN, mass = 1))

    def doButtonAction(self, num: int):
        """
        Does an action depending on the purpose num of a button given
        """
        if (num == 0): # 0 is toggle velocity
            self.draw_velocity = not self.draw_velocity
        elif (num == 1): # 1 is toggle trial
            self.show_trial = not self.show_trial
        elif (num == 2): # 2 is pause/play
            self.paused = not self.paused
        elif (100 < num < 300): # this range is for buttons that go from one menu to another
            self.running = False
            self.menu_choice = num
        elif (300 <= num < 400): # this range is for buttons when user is creating custon screen
            if (num == 399): # user starts simulation
                self.running = False
                self.menu_choice = 0
            elif (num == 398):
                self.relocating = False
                if (self.showing_stat_of):
                    self.doButtonAction(499)
                if (self.objects.count(self.obj_on_mouse) != 0):
                    self.objects.remove(self.obj_on_mouse)
                self.obj_on_mouse = None
            elif (num == 301):
                self.obj_on_mouse = Attractor(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, mass=400)
            elif (num == 302):
                self.obj_on_mouse = Planet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 10, mass=400)
            elif (num == 303):
                self.obj_on_mouse = Planet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 7, mass=10)
        elif (400 <= num < 500): # this range is for buttons and input boxes on an object's InfoBox
            if (num == 499): # 499 is the closing the stats button
                self.showing_stat_of.show_stats = False
                for i in range(self.showing_stat_of.info_box.size):
                    self.buttons.pop()
                self.showing_stat_of = None
            else:
                self.is_typing = True
                self.pressedButton.is_typing = True

    def checkEvent(self):
        """
        Checks for events in the game
        """
        mouseDown = False
        mouseUp = False
        hovering = False

        for event in pygame.event.get():
            # set running to false if quit
            if event.type == pygame.QUIT:
                self.running = False
            # set mouseDown to True
            if event.type == MOUSEBUTTONDOWN:
                mouseDown = True
            # set mouseUp to True
            if event.type == MOUSEBUTTONUP:
                mouseUp = True

            if event.type == KEYDOWN:
                if (self.is_typing):
                    # if the user is on a input button typing, take the input
                    self.is_typing = self.showing_stat_of.info_box.takeInput(event.key, self.pressedButton.purpose)
                    if (not self.is_typing):
                        # if the user is no longer typing, set pressedButton to None
                        self.pressedButton = None
                if event.key == K_p:
                    # if p is pressed, change the bool in paused
                    self.paused = not self.paused

        keys = pygame.key.get_pressed()
        # escape key also stops the game
        if keys[pygame.K_ESCAPE]:
            self.running = False

        # get the (x,y) position of mouse
        mouse_pos = pygame.mouse.get_pos()

        for obj in self.objects:
            if (obj.mouseOnObj(mouse_pos)):
                # if the mouse is on an object change the cursor
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                obj.glow = True
                hovering = True
                # if the user clicks on an object whose stats is being shown, the user may relocate the object
                if (mouseDown and self.showing_stat_of == obj):
                    self.obj_on_mouse = obj
                    self.obj_on_mouse.obj_on_mouse = True
                    self.relocating = True
                    break
                # if the user clicks on an object whose stats is not shown, show the stats
                elif (mouseDown and self.showing_stat_of != obj):
                    # close the Infobox of any other object first
                    if (self.showing_stat_of != None):
                        self.showing_stat_of.show_stats = False
                        self.doButtonAction(499) # 499 is to disable showing stats
                    self.showing_stat_of = obj
                    obj.show_stats = True
                    # add buttons to self.buttons
                    obj_buttons = obj.getButtons()
                    for button in obj_buttons:
                        self.addButton(button)
                    break
                mouseDown = False
            # if the mouse is not on the object, set its glow to False
            else:
                obj.glow = False

        for button in self.buttons:
            # if the mouse is on a button, change the color, change the cursor
            if (button.mouseOnButton(mouse_pos)):
                button.updateColor(button.getHalfColor(button.default_bgcolor))
                pygame.mouse.set_system_cursor(button.cursor_type)
                hovering = True
                if mouseDown:
                    # if mouse is pressed on a button, but the user had been typing on another input box,
                    #  reset the input box and stop typing on that input box
                    if (self.pressedButton and (400 <= self.pressedButton.purpose < 500)):
                        self.pressedButton.is_typing = False
                        if (self.showing_stat_of):
                            self.showing_stat_of.info_box.resetToObject()
                    self.pressedButton = button
                    self.doButtonAction(button.purpose)
                    mouseDown = False
                # if the user drags an object onto the delete/cancle button, and lets go of mouse, do its action
                elif (mouseUp and button.purpose == 398):
                    self.doButtonAction(button.purpose)
                break
            else:
                #if the mosue is not on the button, change the color of the button to default
                button.updateColor(button.default_bgcolor)

        # if the mouse is not on any objects or buttons, set cursor to an arrow
        if (not hovering):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # if the user was relocating an object and lets go of mouse, stop relocating that object
        if (mouseUp and self.relocating and self.obj_on_mouse):
            self.obj_on_mouse.obj_on_mouse = False
            self.obj_on_mouse = None
            self.relocating = False

        # used when user is making custom system
        # if the user clicks on the screen when theres an object on the mouse, add the object to the list
        # and remove it from the mouse
        if (mouseDown and self.obj_on_mouse and not self.relocating):
            self.addObject(self.obj_on_mouse)
            self.obj_on_mouse = None
            # if the object is an planet, let the user set its velocity by dragging the mouse
            if (type(self.objects[len(self.objects) - 1]) != Attractor):
                self.userSettingVelocity(self.objects[len(self.objects) - 1])

    def mainMenu(self):
        """
        Sets up the main menu where the user can either choose an template or create an custon system
        """
        # add two buttons 
        self.addButton(TextButton(SCREEN[0]/ 2, SCREEN[1]/2, "Choose Template", 101))
        self.addButton(TextButton(SCREEN[0]/ 2, SCREEN[1]/2 - 30, "Custom System", 102))
        # check for events and render
        while (self.running):
            self.checkEvent()
            self.render()

        # if the user clicks "Choose Template"
        if self.menu_choice == 101:
            self.templateScreen()
        # if the user clicks "Custon System"
        elif self.menu_choice == 102:
            self.userEdit()

    def templateScreen(self):
        """
        Sets up screen where user can choose a template to run
        """
        self.reset()
        self.menu_choice = -1
        # add buttons for systems
        self.addButton(TextButton(SCREEN[0]/2, SCREEN[1]/2 - 30, "Binary Sun", 201))
        self.addButton(TextButton(SCREEN[0]/2, SCREEN[1]/2, "Sun Earth Moon", 202))
        while (self.running):
            self.checkEvent()
            self.render()
        self.reset()
        # if user chooses binary sun system
        if (self.menu_choice == 201):
            self.binarySun()
        # if user chooses sun earth mood system
        elif (self.menu_choice == 202):
            self.basicSetup()

        # if the user had choosen an system, run
        if (self.menu_choice != -1):
            self.run()

    def renderObjOnMouse(self):
        """
        Renders the object on the mouse
        """
        if (self.obj_on_mouse):
            self.obj_on_mouse.display(self.window)

    def updateObjOnMouse(self):
        """
        Updates position of the object on mouse to the position of mouse
        """
        if (self.obj_on_mouse):
            self.obj_on_mouse.setPosition(pygame.mouse.get_pos())

    def userSettingVelocity(self, obj: Object):
        """
        Handles the user setting velocity of an object when creating a custom system
        """
        settingVel = True
        while(settingVel):
            # if the user lets go of mouse, stop setting velocity
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    settingVel = False
            # change velocity of object based on how far the user drags the mouse
            pos = pygame.mouse.get_pos()
            obj.setVelocity((obj.x - pos[0])/50, (obj.y - pos[1])/50)
            self.render()

    def userEdit(self):
        """
        Creates screen where the user creates a custom system
        """
        self.reset()
        # add the buttons need for the user
        self.addButton(TextButton(SCREEN[0]-70, 200, "Attractor", 301))
        self.addButton(TextButton(SCREEN[0] - 70, 230, "Star", 302))
        self.addButton(TextButton(SCREEN[0] - 70, 260, "Planet", 303))
        self.addButton(TextButton(0, 0, "START", 399))
        self.addButton(TextButton(SCREEN[0] - 150, SCREEN[1] - 40, "Delete / Cancel", 398, font_size=20))
        while (self.running):
            self.checkEvent()
            self.updateObjOnMouse()
            self.render()
        # if the user presses start
        if (self.menu_choice == 0):
            self.buttons = []
            # stop showing stats of any object
            if(self.showing_stat_of):
                self.showing_stat_of.show_stats = False
                self.showing_stat_of = None
            # add basic buttons and run
            self.addBasicButtons()
            self.run()

    def run(self):
        """
        Runs a user drawn system or a template system
        """
        clock = pygame.time.Clock()        
        # render and sleep for few seconds to let the user see the setup
        self.render()
        self.checkEvent()
        time.sleep(2)
    
        self.running = True
        self.draw_velocity = False
        while(self.running):
            clock.tick(60)
            # checkEvent tracks keyboard and mouse presses
            self.checkEvent()
            self.updateObjOnMouse()
            
            # dont update when the game is paused
            # update and render
            if not self.paused:
                self.update()
            self.render()
