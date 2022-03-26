import os
import ctypes.util
uname = os.uname()

if uname.sysname == "Darwin" and uname.release >= "20.":
    uname = os.uname()
    real_find_library = ctypes.util.find_library
    def find_library(name):
        if name in {"OpenGL", "GLUT"}:  # add more names here if necessary
            return f"/System/Library/Frameworks/{name}.framework/{name}"
        return real_find_library(name)
    ctypes.util.find_library = find_library

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import *

import math





pygame.init()
display = (800, 480)
scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.FULLSCREEN)
pygame.mouse.set_visible(False)


glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_TEXTURE_2D)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])


sphere = gluNewQuadric() 
gluQuadricTexture(sphere, GL_TRUE);
gluQuadricNormals(sphere, GLU_SMOOTH);

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 75.0)

def setup_view_matrix():
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    return viewMatrix

viewMatrix = setup_view_matrix()

## Get count of joysticks
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

if joystick_count:
    controller = pygame.joystick.Joystick(0) 
    controller.init()
    button = {}
    for i in range(controller.get_numbuttons()):
        button[i] = False

prot = 1.0
axis_x = 1
axis_y = 0
axis = {}
rot_x = 0.0
rot_y = 0.0
rot_scale = 1.0
rotx_scale =  1 * rot_scale
roty_scale = -1 * rot_scale
rotz_scale = -1 * 180



up_down_angle = 0.0
paused = False
run = True


# textures
def load_texture(path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = pygame.image.load(path)
    image = pygame.transform.flip(image, False, True)
    image_width, image_height = image.get_rect().size
    img_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

texture = load_texture("./jupiter.jpg")
sky = load_texture("./sky.png")
planet_textures = [
    load_texture("./textures/planet-1.jpg"),
    load_texture("./textures/planet-2.jpg"),
    load_texture("./textures/planet-3.jpg"),
    load_texture("./textures/planet-4.jpg"),
]


def generate_planets():
    planets = []
    for i in range(0, 30):
        x = randint(-60,60)
        y = randint(-60,60)
        z = randint(-60,60)
        tex = choice(planet_textures)
        rad = randint(1, 9)
        planets.append({"x": x, "y": y, "z": z, "rot": 1, "texture": tex, "radius": rad})
    return planets

planets = generate_planets()



def draw_planet(p):
    glPushMatrix()
    glTranslatef(p["x"], p["y"], p["z"])
    glBindTexture(GL_TEXTURE_2D, planet["texture"])
    planet["rot"] = planet["rot"] + 0.1
    glRotatef(prot, 0, 0, 1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    gluSphere(sphere, planet["radius"], 32, 16) 
    glPopMatrix()

sounds = [
    pygame.mixer.Sound("sounds/sound-1.wav"),
    pygame.mixer.Sound("sounds/sound-2.wav"),
]

while run:
    axis[axis_x] = rot_x
    axis[axis_y] = rot_y

    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            axis[event.axis] = round(event.value,2)
        if event.type == pygame.JOYBUTTONDOWN:
            button[event.button] = True
            pygame.mixer.Sound.play(choice(sounds))
        if event.type == pygame.JOYBUTTONUP:
            button[event.button] = False
            pygame.mixer.music.stop()
        # if button[8] and button[9]:
        #     run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused

    if not paused:
        # get keys
        keypress = pygame.key.get_pressed()
    
        # init model view matrix
        glLoadIdentity()

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movment 
        if keypress[pygame.K_w]: #or button[0]:
            glTranslatef(0,0,0.1)
        if keypress[pygame.K_s]: #or button[1]:
            glTranslatef(0,0,-0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1,0,0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1,0,0)
        # if button[8] or button[9]:
        #     planets = generate_planets()
        #     viewMatrix = setup_view_matrix()

        # apply the left and right rotation
        rot_x = axis[axis_x]
        rot_y = axis[axis_y]
        glRotatef(rotx_scale * rot_x, 0, 1, 0)
        glRotatef(roty_scale * rot_y, 1, 0, 0)

        # multiply the current matrix by the get the new view matrix and store the final vie matrix 
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        # draw planet
        glPushMatrix()
        glTranslatef(-1.5, 0, 0)
        prot += 0.5
        glRotatef(prot, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        gluSphere(sphere, 1.0, 32, 16) 
        glPopMatrix()

        for planet in planets:
            draw_planet(planet)

        
        # Draw the skybox
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glDepthMask(False)
        glTranslatef(0, 0, 0)
        glBindTexture(GL_TEXTURE_2D, sky)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        gluSphere(sphere, 55.0, 32, 16) 
        glEnable(GL_LIGHTING)
        glDepthMask(True)
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()
