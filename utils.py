from OpenGL.GL import *
from OpenGL.GLU import *

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL) # Permite usar glColor junto com iluminação
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    # Configuração da luz (posição e cor)
    light_pos = [20.0, 100.0, 20.0, 0.0] # Luz direcional simulando o sol a pino
    light_ambient = [0.5, 0.5, 0.5, 1.0] # Ambiente mais iluminado (dia)
    light_diffuse = [0.9, 0.9, 0.8, 1.0] # Luz difusa levemente amarelada

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    # Remover o reflexo branco (specular) da luz
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    
    # Material padrão sem reflexo
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 0)

def draw_cube(x, y, z, width, height, depth, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(width, height, depth)
    glColor3f(*color)
    
    vertices = [
        [1, 1, -1], [-1, 1, -1], [-1, 1, 1], [1, 1, 1], # Topo
        [1, -1, 1], [-1, -1, 1], [-1, -1, -1], [1, -1, -1], # Base
        [1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1], # Frente
        [1, -1, -1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1], # Trás
        [-1, 1, 1], [-1, 1, -1], [-1, -1, -1], [-1, -1, 1], # Esquerda
        [1, 1, -1], [1, 1, 1], [1, -1, 1], [1, -1, -1] # Direita
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
