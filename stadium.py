from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from utils import draw_cube

def draw_field(grass_tex=None):
    if grass_tex is not None:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, grass_tex)

    largura_listra = 4
    for z in range(-40, 40, largura_listra):
        if (z // largura_listra) % 2 == 0:
            glColor3f(0.8, 1.0, 0.8)
        else:
            glColor3f(0.6, 0.9, 0.6)
            
        glNormal3f(0, 1, 0)
        glBegin(GL_QUADS)
        
        glTexCoord2f(-7.5, z / 4.0); glVertex3f(-30, 0, z)
        glTexCoord2f(-7.5, (z + largura_listra) / 4.0); glVertex3f(-30, 0, z + largura_listra)
        glTexCoord2f(7.5, (z + largura_listra) / 4.0); glVertex3f(30, 0, z + largura_listra)
        glTexCoord2f(7.5, z / 4.0); glVertex3f(30, 0, z)
        glEnd()

    if grass_tex is not None:
        glDisable(GL_TEXTURE_2D)

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)
    
    def draw_circle(cx, cy, cz, radius, segments=40):
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            theta = 2.0 * math.pi * float(i) / float(segments)
            glVertex3f(cx + radius * math.cos(theta), cy, cz + radius * math.sin(theta))
        glEnd()

    def draw_arc(cx, cy, cz, radius, start_angle, end_angle, segments=20):
        glBegin(GL_LINE_STRIP)
        for i in range(segments + 1):
            theta = start_angle + (end_angle - start_angle) * float(i) / float(segments)
            glVertex3f(cx + radius * math.cos(theta), cy, cz + radius * math.sin(theta))
        glEnd()

    glBegin(GL_LINES)
    glVertex3f(-28, 0.01, -38); glVertex3f(28, 0.01, -38)
    glVertex3f(28, 0.01, -38);  glVertex3f(28, 0.01, 38)
    glVertex3f(28, 0.01, 38);   glVertex3f(-28, 0.01, 38)
    glVertex3f(-28, 0.01, 38);  glVertex3f(-28, 0.01, -38)
    glVertex3f(-28, 0.01, 0);   glVertex3f(28, 0.01, 0)
    
    glVertex3f(-12, 0.01, -38); glVertex3f(-12, 0.01, -26)
    glVertex3f(-12, 0.01, -26); glVertex3f(12, 0.01, -26)
    glVertex3f(12, 0.01, -26);  glVertex3f(12, 0.01, -38)
    glVertex3f(-6, 0.01, -38); glVertex3f(-6, 0.01, -32)
    glVertex3f(-6, 0.01, -32); glVertex3f(6, 0.01, -32)
    glVertex3f(6, 0.01, -32);  glVertex3f(6, 0.01, -38)

    glVertex3f(-12, 0.01, 38); glVertex3f(-12, 0.01, 26)
    glVertex3f(-12, 0.01, 26); glVertex3f(12, 0.01, 26)
    glVertex3f(12, 0.01, 26);  glVertex3f(12, 0.01, 38)
    glVertex3f(-6, 0.01, 38); glVertex3f(-6, 0.01, 32)
    glVertex3f(-6, 0.01, 32); glVertex3f(6, 0.01, 32)
    glVertex3f(6, 0.01, 32);  glVertex3f(6, 0.01, 38)
    glEnd()
    
    draw_circle(0, 0.01, 0, 5)
    draw_arc(0, 0.01, -26, 5, 0, math.pi)
    draw_arc(0, 0.01, 26, 5, math.pi, 2*math.pi)

    for cx in [-30, 30]:
        for cz in [-40, 40]:
            glColor3f(1.0, 1.0, 0.0)
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glVertex3f(cx, 0, cz)
            glVertex3f(cx, 1.5, cz)
            glEnd()
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_TRIANGLES)
            glVertex3f(cx, 1.5, cz)
            glVertex3f(cx, 1.0, cz)
            dir_x = 0.8 if cx < 0 else -0.8
            dir_z = 0.8 if cz < 0 else -0.8
            glVertex3f(cx + dir_x, 1.25, cz + dir_z)
            glEnd()

def draw_grandstands():
    colors = [
        (0.02, 0.02, 0.02),
        (0.0, 0.12, 0.0),
        (0.2, 0.2, 0.0),
        (0.0, 0.0, 0.16),
        (0.16, 0.16, 0.16)
    ]
    
    for i in range(5):
        altura = i * 2.5 + 1.0
        distancia_x = 30 + i * 4
        distancia_z = 40 + i * 4
        largura = 4.0
        
        glColor3f(*colors[i])
        glBegin(GL_QUADS)
        
        glNormal3f(-1, 1, 0)
        glVertex3f(distancia_x, altura, -distancia_z)
        glVertex3f(distancia_x + largura, altura + 2.5, -distancia_z)
        glVertex3f(distancia_x + largura, altura + 2.5, distancia_z)
        glVertex3f(distancia_x, altura, distancia_z)
        
        glNormal3f(1, 1, 0)
        glVertex3f(-distancia_x, altura, -distancia_z)
        glVertex3f(-distancia_x - largura, altura + 2.5, -distancia_z)
        glVertex3f(-distancia_x - largura, altura + 2.5, distancia_z)
        glVertex3f(-distancia_x, altura, distancia_z)

        glNormal3f(0, 1, -1)
        glVertex3f(-distancia_x, altura, distancia_z)
        glVertex3f(-distancia_x, altura + 2.5, distancia_z + largura)
        glVertex3f(distancia_x, altura + 2.5, distancia_z + largura)
        glVertex3f(distancia_x, altura, distancia_z)

        glNormal3f(0, 1, 1)
        glVertex3f(-distancia_x, altura, -distancia_z)
        glVertex3f(-distancia_x, altura + 2.5, -distancia_z - largura)
        glVertex3f(distancia_x, altura + 2.5, -distancia_z - largura)
        glVertex3f(distancia_x, altura, -distancia_z)
        
        glEnd()

    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(46, 15, -56)
    glVertex3f(30, 15, -56)
    glVertex3f(30, 15, 56)
    glVertex3f(46, 15, 56)
    
    glVertex3f(-46, 15, -56)
    glVertex3f(-30, 15, -56)
    glVertex3f(-30, 15, 56)
    glVertex3f(-46, 15, 56)

    glVertex3f(-30, 15, 56)
    glVertex3f(-30, 15, 40)
    glVertex3f(30, 15, 40)
    glVertex3f(30, 15, 56)

    glVertex3f(-30, 15, -56)
    glVertex3f(-30, 15, -40)
    glVertex3f(30, 15, -40)
    glVertex3f(30, 15, -56)
    glEnd()

    for z_pil in range(-50, 60, 20):
        draw_cube(44, 7.5, z_pil, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))
        draw_cube(-44, 7.5, z_pil, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))
    for x_pil in [-15, 0, 15]:
        draw_cube(x_pil, 7.5, 54, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))
        draw_cube(x_pil, 7.5, -54, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))

    glColor3f(0.05, 0.05, 0.05)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glVertex3f(-46, 0, 56)
    glVertex3f(46, 0, 56)
    glVertex3f(46, 15, 56)
    glVertex3f(-46, 15, 56)
    
    glNormal3f(0, 0, 1)
    glVertex3f(-46, 0, -56)
    glVertex3f(46, 0, -56)
    glVertex3f(46, 15, -56)
    glVertex3f(-46, 15, -56)
    
    glNormal3f(-1, 0, 0)
    glVertex3f(46, 0, -56)
    glVertex3f(46, 0, 56)
    glVertex3f(46, 15, 56)
    glVertex3f(46, 15, -56)
    
    glNormal3f(1, 0, 0)
    glVertex3f(-46, 0, -56)
    glVertex3f(-46, 0, 56)
    glVertex3f(-46, 15, 56)
    glVertex3f(-46, 15, -56)
    glEnd()

def draw_goal(z_pos):
    glColor3f(0.9, 0.9, 0.9)
    draw_cube(-4, 1.5, z_pos, 0.15, 1.5, 0.15, (0.9, 0.9, 0.9))
    draw_cube(4, 1.5, z_pos, 0.15, 1.5, 0.15, (0.9, 0.9, 0.9))
    draw_cube(0, 3.15, z_pos, 4.15, 0.15, 0.15, (0.9, 0.9, 0.9))

    glColor3f(0.8, 0.8, 0.8)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    z_net = z_pos - 2 if z_pos < 0 else z_pos + 2
    
    for i in range(17):
        x = -4 + (i * 0.5)
        glVertex3f(x, 0, z_net)
        glVertex3f(x, 3.0, z_net)
        glVertex3f(x, 3.0, z_net)
        glVertex3f(x, 3.0, z_pos)
        
    for i in range(7):
        y = i * 0.5
        glVertex3f(-4, y, z_net)
        glVertex3f(4, y, z_net)
        glVertex3f(-4, y, z_net)
        glVertex3f(-4, y, z_pos)
        glVertex3f(4, y, z_net)
        glVertex3f(4, y, z_pos)
    glEnd()

crowd_list = None

def build_crowd_list():
    global crowd_list
    crowd_list = glGenLists(1)
    glNewList(crowd_list, GL_COMPILE)
    
    quadric = gluNewQuadric()
    colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0), (1.0, 1.0, 1.0), (1.0, 0.5, 0.0), (0.0, 1.0, 1.0), (1.0, 0.0, 1.0)]
    
    for i in range(1, 5): 
        altura = i * 2.5 + 1.0 
        dist_x_start = 30 + i * 4
        dist_z_start = 40 + i * 4
        
        for z in range(int(-dist_z_start + 2), int(dist_z_start - 2), 3):
            if random.random() > 0.4:
                glColor3f(*random.choice(colors))
                glPushMatrix()
                glTranslatef(dist_x_start + 2.0, altura, z)
                glRotatef(-90, 1, 0, 0)
                gluCylinder(quadric, 0.4, 0.4, 1.0, 8, 1)
                glTranslatef(0, 0, 1.0)
                gluSphere(quadric, 0.4, 8, 8)
                glPopMatrix()
            if random.random() > 0.4:
                glColor3f(*random.choice(colors))
                glPushMatrix()
                glTranslatef(-dist_x_start - 2.0, altura, z)
                glRotatef(-90, 1, 0, 0)
                gluCylinder(quadric, 0.4, 0.4, 1.0, 8, 1)
                glTranslatef(0, 0, 1.0)
                gluSphere(quadric, 0.4, 8, 8)
                glPopMatrix()

        for x in range(int(-dist_x_start + 2), int(dist_x_start - 2), 3):
            if random.random() > 0.4:
                glColor3f(*random.choice(colors))
                glPushMatrix()
                glTranslatef(x, altura, dist_z_start + 2.0)
                glRotatef(-90, 1, 0, 0)
                gluCylinder(quadric, 0.4, 0.4, 1.0, 8, 1)
                glTranslatef(0, 0, 1.0)
                gluSphere(quadric, 0.4, 8, 8)
                glPopMatrix()
            if random.random() > 0.4:
                glColor3f(*random.choice(colors))
                glPushMatrix()
                glTranslatef(x, altura, -dist_z_start - 2.0)
                glRotatef(-90, 1, 0, 0)
                gluCylinder(quadric, 0.4, 0.4, 1.0, 8, 1)
                glTranslatef(0, 0, 1.0)
                gluSphere(quadric, 0.4, 8, 8)
                glPopMatrix()
                
    gluDeleteQuadric(quadric)
    glEndList()

def draw_crowd():
    if crowd_list is not None:
        glCallList(crowd_list)
