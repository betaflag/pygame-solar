import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class Object():
    def draw():
        pass
    
    def load_texture(self, path):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pygame.image.load(path)
        image = pygame.transform.flip(image, False, True)
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture

class Planet(Object):
    sphere = gluNewQuadric() 
    rotation = 1.0
    texture = None
    size = 1
    position = (0,0,0)
    
    def __init__(self, texture, size = None, position = None):
        gluQuadricTexture(self.sphere, GL_TRUE);
        gluQuadricNormals(self.sphere, GLU_SMOOTH); 
        self.texture = self.load_texture(texture)
        if size:
            self.size = size
        if position:
            self.position = position
        
    def draw(self):
        self.rotation += 0.1
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotation, 0, 0, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(self.sphere, self.size, 32, 16) 
        glPopMatrix()
        
class SkyDome(Object):
    sphere = gluNewQuadric() 
    texture = None
    
    def __init__(self):
        gluQuadricTexture(self.sphere, GL_TRUE);
        gluQuadricNormals(self.sphere, GLU_SMOOTH);
        self.texture = self.load_texture("./textures/sky.png")
        
    def draw(self):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glDepthMask(False)
        glTranslatef(0, 0, 0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        gluSphere(self.sphere, 150, 32, 16) 
        glEnable(GL_LIGHTING)
        glDepthMask(True)
        glPopMatrix()