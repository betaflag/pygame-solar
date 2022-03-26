import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from objects import Planet, SkyDome
from random import randint

class Game():
    AXIS_X = 1
    AXIS_Y = 0
    run = False
    objects = []
    view = None
    speed = 1
    axis = {0: 0, 1: 0}
    button = {0: False, 1: False,2: False,3: False,4: False,5: False,6: False,7: False,8: False,9: False}
    
    def __init__(self, fullscreen=False, size_x=800, size_y=600, speed=1):
        pygame.init()
        mode = DOUBLEBUF | OPENGL
        if fullscreen:
            mode = mode | pygame.FULLSCREEN
        pygame.display.set_mode((size_x, size_y), mode)
        pygame.mouse.set_visible(False)
        self.init_controls();
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, size_x/size_y, 0.1, 300)
        self.init_lighting()
        self.init_view()
        sun = Planet(size=8, texture="./textures/sun.jpeg", position=(10, 0, 0))
        mercury = Planet(size=0.5, texture="./textures/mercury.jpeg", position=(-10, 0, 0))
        venus = Planet(size=0.8, texture="./textures/venus.jpeg", position=(-20, 0, 0))
        earth = Planet(size=1.2, texture="./textures/earth.jpeg", position=(-30, 0, 0))
        mars = Planet(size=0.7, texture="./textures/mars.jpeg", position=(-40, 0, 0))
        jupiter = Planet(size=2, texture="./textures/jupiter.jpeg", position=(-50, 0, 0))
        saturn = Planet(size=1.7, texture="./textures/saturn.jpeg", position=(-60, 0, 0))
        uranus = Planet(size=1, texture="./textures/uranus.jpeg", position=(-70, 0, 0))
        neptune = Planet(size=1, texture="./textures/neptune.jpeg", position=(-80, 0, 0))
        self.objects = [SkyDome(), sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
        self.speed = speed
        
    def init_controls(self):
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        if joystick_count:
            controller = pygame.joystick.Joystick(0) 
            controller.init()
            for i in range(controller.get_numbuttons()):
                self.button[i] = False
                
    def init_view(self):
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, -20, 0, 0, 0, 0, 0, 0, 1)
        glTranslatef(33, 75 ,0)
        self.view = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
    
    def init_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis[event.axis] = round(event.value,2)
            if event.type == pygame.JOYBUTTONDOWN:
                self.button[event.button] = True
            if event.type == pygame.JOYBUTTONUP:
                self.button[event.button] = False

    def handle_keys(self):
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_ESCAPE] or (self.button[0] and self.button[1] and self.button[8] and self.button[9]):
            self.run = False
        if keypress[pygame.K_w] or self.button[0]:
            glTranslatef(0,0, self.speed * 0.1)
        if keypress[pygame.K_s] or self.button[1]:
            glTranslatef(0,0,-self.speed * 0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-self.speed * 0.1,0,0)
        if keypress[pygame.K_a]:
            glTranslatef(self.speed * 0.1,0,0)
        if self.button[8] or self.button[9] or keypress[pygame.K_SPACE]:
            self.init_view()

    def handle_joystick(self):
        glRotatef(self.axis[self.AXIS_X], 0, 1, 0)
        glRotatef(-self.axis[self.AXIS_Y], 1, 0, 0)
    
    def draw(self):
        
        glLoadIdentity()
        
        glPushMatrix()
        glLoadIdentity()
        self.handle_events()
        self.handle_keys()
        self.handle_joystick()
        glMultMatrixf(self.view)
        self.view = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()

        glMultMatrixf(self.view)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        for objects in self.objects:
            objects.draw()

    def run(self):
        self.run = True
        while self.run:
            self.draw()
            pygame.display.flip()
            pygame.time.wait(10)
