from OpenGL.GL import *
from OpenGL.GLU import *
import math
from utils import draw_cube, sol_pos

def draw_boneco():
    cor_pele = (0.9, 0.7, 0.6)
    cor_camisa = (1.0, 1.0, 0.0)
    cor_short = (0.0, 0.0, 1.0)
    cor_meia = (1.0, 1.0, 1.0)
    cor_cabelo = (0.1, 0.1, 0.1)
    cor_chuteira = (0.1, 0.1, 0.1)

    glPushMatrix()
    glTranslatef(0, 0, 0)
    #Escala
    glScalef(0.6, 0.6, 0.6)

    #Sombra
    player_x = 0
    player_z = 0

    offset_x = -(sol_pos[0] - player_x) * 0.02
    offset_z = -(sol_pos[2] - player_z) * 0.006

    shadow_x = offset_x
    shadow_z = offset_z     


    glDisable(GL_LIGHTING)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.0, 0.0, 0.0, 0.55)

    glBegin(GL_POLYGON)

    for i in range(40):
        ang = 2.0 * math.pi * i / 40

        glVertex3f(
            shadow_x + 1.25 * math.cos(ang),
            0.02,
            shadow_z + 0.75 * math.sin(ang)
        )

    glEnd()

    glDisable(GL_BLEND)

    glEnable(GL_LIGHTING)

    #Cabelo
    draw_cube(0, 3.9, 0, 0.42, 0.1, 0.42, cor_cabelo)
    #Cabeca
    draw_cube(0, 3.5, 0, 0.4, 0.4, 0.4, cor_pele)
    
    #Tronco
    glPushMatrix()
    glTranslatef(0, 2.0, 0)
    glRotatef(10, 1, 0, 0)
    draw_cube(0, 0, 0, 0.6, 0.8, 0.3, cor_camisa)
    glPopMatrix()
    
    #Braco.esq
    glPushMatrix()
    glTranslatef(-0.8, 2.4, 0)
    glRotatef(-20, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0, -1.4, 0, 0.15, 0.4, 0.15, cor_pele)
    glPopMatrix()
    
    #Braco.dir
    glPushMatrix()
    glTranslatef(0.8, 2.4, 0)
    glRotatef(20, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0, -1.4, 0, 0.15, 0.4, 0.15, cor_pele)
    glPopMatrix()
    
    #Perna.esq
    draw_cube(-0.3, 1.0, 0, 0.25, 0.4, 0.25, cor_short)
    draw_cube(-0.3, 0.4, 0, 0.2, 0.4, 0.2, cor_meia)
    draw_cube(-0.3, 0.1, 0.1, 0.22, 0.1, 0.3, cor_chuteira)
    
    #Perna.dir
    glPushMatrix()
    glTranslatef(0.3, 1.4, 0)
    glRotatef(-30, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.25, 0.4, 0.25, cor_short)
    draw_cube(0, -1.0, 0, 0.2, 0.4, 0.2, cor_meia)
    draw_cube(0, -1.3, 0.1, 0.22, 0.1, 0.3, cor_chuteira)
    glPopMatrix()
    
    glPopMatrix()

def draw_ball():
    # Sombra orientada pelo Sol

    ball_x = 0
    ball_y = 0.5
    ball_z = -8

    offset_x = -(sol_pos[0] - ball_x) * 0.006
    offset_z = -(sol_pos[2] - ball_z) * 0.006

    glDisable(GL_LIGHTING)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.0, 0.0, 0.0, 0.35)

    glBegin(GL_POLYGON)

    for i in range(30):
        theta = 2.0 * math.pi * i / 30

        glVertex3f(
            ball_x + offset_x + 0.45 * math.cos(theta),
            0.02,
            ball_z + offset_z + 0.30 * math.sin(theta)
        )

    glEnd()

    glDisable(GL_BLEND)

    glEnable(GL_LIGHTING)

    glPushMatrix()
    glTranslatef(0, 0.5, -8)
    glColor3f(1.0, 1.0, 1.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.5, 32, 32)
    gluDeleteQuadric(quadric)
    
    #Detalhes
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
