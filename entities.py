from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import draw_cube

def draw_boneco():
    cor_pele = (0.9, 0.7, 0.6)
    cor_camisa = (1.0, 1.0, 0.0)
    cor_short = (0.0, 0.0, 1.0)
    cor_meia = (1.0, 1.0, 1.0)
    cor_cabelo = (0.1, 0.1, 0.1)
    cor_chuteira = (0.1, 0.1, 0.1)

    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(0.6, 0.6, 0.6)

    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.4, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(-1.0, 0.02, -1.0)
    glVertex3f(1.0, 0.02, -1.0)
    glVertex3f(1.0, 0.02, 1.0)
    glVertex3f(-1.0, 0.02, 1.0)
    glEnd()
    glEnable(GL_LIGHTING)

    draw_cube(0, 3.9, 0, 0.42, 0.1, 0.42, cor_cabelo)
    draw_cube(0, 3.5, 0, 0.4, 0.4, 0.4, cor_pele)
    
    glPushMatrix()
    glTranslatef(0, 2.0, 0)
    glRotatef(10, 1, 0, 0)
    draw_cube(0, 0, 0, 0.6, 0.8, 0.3, cor_camisa)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.8, 2.4, 0)
    glRotatef(-20, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0, -1.4, 0, 0.15, 0.4, 0.15, cor_pele)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0.8, 2.4, 0)
    glRotatef(20, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0, -1.4, 0, 0.15, 0.4, 0.15, cor_pele)
    glPopMatrix()
    
    draw_cube(-0.3, 1.0, 0, 0.25, 0.4, 0.25, cor_short)
    draw_cube(-0.3, 0.4, 0, 0.2, 0.4, 0.2, cor_meia)
    draw_cube(-0.3, 0.1, 0.1, 0.22, 0.1, 0.3, cor_chuteira)
    
    glPushMatrix()
    glTranslatef(0.3, 1.4, 0)
    glRotatef(-30, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.25, 0.4, 0.25, cor_short)
    draw_cube(0, -1.0, 0, 0.2, 0.4, 0.2, cor_meia)
    draw_cube(0, -1.3, 0.1, 0.22, 0.1, 0.3, cor_chuteira)
    glPopMatrix()
    
    glPopMatrix()

def draw_ball():
    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.4, 0.1)
    glBegin(GL_POLYGON)
    for i in range(20):
        theta = 2.0 * math.pi * float(i) / 20.0
        glVertex3f(0.5 * math.cos(theta), 0.02, -8 + 0.5 * math.sin(theta))
    glEnd()
    glEnable(GL_LIGHTING)

    glPushMatrix()
    glTranslatef(0, 0.5, -8)
    glColor3f(1.0, 1.0, 1.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.5, 32, 32)
    gluDeleteQuadric(quadric)
    
    glColor3f(0.1, 0.1, 0.1)
    for rot in range(0, 360, 45):
        glPushMatrix()
        glRotatef(rot, 1, 1, 0)
        glTranslatef(0, 0, 0.5)
        quad = gluNewQuadric()
        gluDisk(quad, 0, 0.15, 5, 1)
        gluDeleteQuadric(quad)
        glPopMatrix()
    
    glPopMatrix()
