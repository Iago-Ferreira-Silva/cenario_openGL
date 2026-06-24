from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

def load_texture(image_path):
    textureSurface = pygame.image.load(image_path)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    
    return texid

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    #Luz.pos.cor
    light_pos = [20.0, 100.0, 20.0, 0.0]
    light_ambient = [0.5, 0.5, 0.5, 1.0]
    light_diffuse = [0.9, 0.9, 0.8, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    #Sem.reflexo
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    
    #Mat.padrao
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 0)

def draw_cube(x, y, z, width, height, depth, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(width, height, depth)
    glColor3f(*color)
    
    vertices = [
        [1, 1, -1], [-1, 1, -1], [-1, 1, 1], [1, 1, 1],
        [1, -1, 1], [-1, -1, 1], [-1, -1, -1], [1, -1, -1],
        [1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
        [1, -1, -1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, -1], [-1, -1, 1],
        [1, 1, -1], [1, 1, 1], [1, -1, 1], [1, -1, -1]
    ]
    
    normals = [
        [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1], [-1, 0, 0], [1, 0, 0]
    ]

    glBegin(GL_QUADS)
    for i in range(6):
        glNormal3f(*normals[i])
        for j in range(4):
            glVertex3f(*vertices[i*4 + j])
    glEnd()
    
    glPopMatrix()
