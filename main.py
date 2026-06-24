import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# Configurações da Janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Variáveis da Câmera
cam_x, cam_y, cam_z = 0.0, 5.0, 15.0  # Começa um pouco atrás e no alto para ver o boneco
cam_yaw = 0.0
cam_pitch = -15.0 # Olhando um pouco para baixo
move_speed = 0.5
rot_speed = 2.0

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

def draw_boneco():
    cor_pele = (0.9, 0.7, 0.6)
    cor_camisa = (1.0, 1.0, 0.0) # Amarelo
    cor_short = (0.0, 0.0, 1.0)  # Azul
    cor_meia = (1.0, 1.0, 1.0)   # Branco
    cor_cabelo = (0.1, 0.1, 0.1) # Preto
    cor_chuteira = (0.1, 0.1, 0.1) # Preto

    glPushMatrix()
    glTranslatef(0, 0, 0) # Base
    glScalef(0.6, 0.6, 0.6) # Deixa o jogador com 60% do tamanho original para ficar mais proporcional

    # Sombra do jogador
    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.4, 0.1) # Sombra no gramado
    glBegin(GL_QUADS)
    glVertex3f(-1.0, 0.02, -1.0)
    glVertex3f(1.0, 0.02, -1.0)
    glVertex3f(1.0, 0.02, 1.0)
    glVertex3f(-1.0, 0.02, 1.0)
    glEnd()
    glEnable(GL_LIGHTING)

    # Cabelo
    draw_cube(0, 3.9, 0, 0.42, 0.1, 0.42, cor_cabelo)
    # Cabeça
    draw_cube(0, 3.5, 0, 0.4, 0.4, 0.4, cor_pele)
    
    # Tronco (inclinado levemente para frente)
    glPushMatrix()
    glTranslatef(0, 2.0, 0)
    glRotatef(10, 1, 0, 0)
    draw_cube(0, 0, 0, 0.6, 0.8, 0.3, cor_camisa)
    glPopMatrix()
    
    # Braço Esquerdo (balançando)
    glPushMatrix()
    glTranslatef(-0.8, 2.4, 0)
    glRotatef(-20, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0, -1.4, 0, 0.15, 0.4, 0.15, cor_pele)
    glPopMatrix()
    
    # Braço Direito
    glPushMatrix()
    glTranslatef(0.8, 2.4, 0)
    glRotatef(20, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0, -1.4, 0, 0.15, 0.4, 0.15, cor_pele)
    glPopMatrix()
    
    # Perna Esquerda (apoiada)
    draw_cube(-0.3, 1.0, 0, 0.25, 0.4, 0.25, cor_short)
    draw_cube(-0.3, 0.4, 0, 0.2, 0.4, 0.2, cor_meia)
    draw_cube(-0.3, 0.1, 0.1, 0.22, 0.1, 0.3, cor_chuteira)
    
    # Perna Direita (chutando levemente)
    glPushMatrix()
    glTranslatef(0.3, 1.4, 0)
    glRotatef(-30, 1, 0, 0)
    draw_cube(0, -0.4, 0, 0.25, 0.4, 0.25, cor_short)
    draw_cube(0, -1.0, 0, 0.2, 0.4, 0.2, cor_meia)
    draw_cube(0, -1.3, 0.1, 0.22, 0.1, 0.3, cor_chuteira)
    glPopMatrix()
    
    glPopMatrix()

def draw_field():
    # Gramado com listras alternadas
    largura_listra = 4
    for z in range(-40, 40, largura_listra):
        if (z // largura_listra) % 2 == 0:
            glColor3f(0.15, 0.65, 0.15) # Verde mais claro
        else:
            glColor3f(0.1, 0.55, 0.1) # Verde mais escuro
            
        glNormal3f(0, 1, 0)
        glBegin(GL_QUADS)
        glVertex3f(-30, 0, z)
        glVertex3f(-30, 0, z + largura_listra)
        glVertex3f(30, 0, z + largura_listra)
        glVertex3f(30, 0, z)
        glEnd()

    # Linhas do campo
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)
    
    # Função auxiliar para círculos
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
    # Bordas externas
    glVertex3f(-28, 0.01, -38); glVertex3f(28, 0.01, -38)
    glVertex3f(28, 0.01, -38);  glVertex3f(28, 0.01, 38)
    glVertex3f(28, 0.01, 38);   glVertex3f(-28, 0.01, 38)
    glVertex3f(-28, 0.01, 38);  glVertex3f(-28, 0.01, -38)
    # Meio campo
    glVertex3f(-28, 0.01, 0);   glVertex3f(28, 0.01, 0)
    
    # Grande área Z=-38
    glVertex3f(-12, 0.01, -38); glVertex3f(-12, 0.01, -26)
    glVertex3f(-12, 0.01, -26); glVertex3f(12, 0.01, -26)
    glVertex3f(12, 0.01, -26);  glVertex3f(12, 0.01, -38)
    # Pequena área Z=-38
    glVertex3f(-6, 0.01, -38); glVertex3f(-6, 0.01, -32)
    glVertex3f(-6, 0.01, -32); glVertex3f(6, 0.01, -32)
    glVertex3f(6, 0.01, -32);  glVertex3f(6, 0.01, -38)

    # Grande área Z=38
    glVertex3f(-12, 0.01, 38); glVertex3f(-12, 0.01, 26)
    glVertex3f(-12, 0.01, 26); glVertex3f(12, 0.01, 26)
    glVertex3f(12, 0.01, 26);  glVertex3f(12, 0.01, 38)
    # Pequena área Z=38
    glVertex3f(-6, 0.01, 38); glVertex3f(-6, 0.01, 32)
    glVertex3f(-6, 0.01, 32); glVertex3f(6, 0.01, 32)
    glVertex3f(6, 0.01, 32);  glVertex3f(6, 0.01, 38)
    glEnd()
    
    # Círculo central e arcos (meia-lua)
    draw_circle(0, 0.01, 0, 5)
    draw_arc(0, 0.01, -26, 5, 0, math.pi)
    draw_arc(0, 0.01, 26, 5, math.pi, 2*math.pi)

    # Bandeirinhas de escanteio
    for cx in [-30, 30]:
        for cz in [-40, 40]:
            glColor3f(1.0, 1.0, 0.0) # Mastro amarelo
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glVertex3f(cx, 0, cz)
            glVertex3f(cx, 1.5, cz)
            glEnd()
            # Bandeira
            glColor3f(1.0, 0.0, 0.0) # Vermelha
            glBegin(GL_TRIANGLES)
            glVertex3f(cx, 1.5, cz)
            glVertex3f(cx, 1.0, cz)
            # A bandeira aponta para o meio do campo
            dir_x = 0.8 if cx < 0 else -0.8
            dir_z = 0.8 if cz < 0 else -0.8
            glVertex3f(cx + dir_x, 1.25, cz + dir_z)
            glEnd()

def draw_ball():
    # Sombra da bola
    glDisable(GL_LIGHTING)
    glColor3f(0.1, 0.4, 0.1) # Cor verde mais escura para sombra
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
    
    # Detalhes da bola (pentágonos pretos)
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

def draw_grandstands():
    colors = [
        (0.02, 0.02, 0.02), # Concreto escuro base
        (0.0, 0.12, 0.0), # Verde 80% mais escuro
        (0.2, 0.2, 0.0), # Amarelo 80% mais escuro
        (0.0, 0.0, 0.16), # Azul 80% mais escuro
        (0.16, 0.16, 0.16)  # Concreto anel superior 80% mais escuro
    ]
    
    # Desenhando degraus ao redor do campo
    for i in range(5):
        altura = i * 2.5 + 1.0
        distancia_x = 30 + i * 4
        distancia_z = 40 + i * 4
        largura = 4.0
        
        glColor3f(*colors[i])
        glBegin(GL_QUADS)
        
        # Lado Direito
        glNormal3f(-1, 1, 0)
        glVertex3f(distancia_x, altura, -distancia_z)
        glVertex3f(distancia_x + largura, altura + 2.5, -distancia_z)
        glVertex3f(distancia_x + largura, altura + 2.5, distancia_z)
        glVertex3f(distancia_x, altura, distancia_z)
        
        # Lado Esquerdo
        glNormal3f(1, 1, 0)
        glVertex3f(-distancia_x, altura, -distancia_z)
        glVertex3f(-distancia_x - largura, altura + 2.5, -distancia_z)
        glVertex3f(-distancia_x - largura, altura + 2.5, distancia_z)
        glVertex3f(-distancia_x, altura, distancia_z)

        # Fundo (Gols)
        glNormal3f(0, 1, -1)
        glVertex3f(-distancia_x, altura, distancia_z)
        glVertex3f(-distancia_x, altura + 2.5, distancia_z + largura)
        glVertex3f(distancia_x, altura + 2.5, distancia_z + largura)
        glVertex3f(distancia_x, altura, distancia_z)

        # Frente (Gols)
        glNormal3f(0, 1, 1)
        glVertex3f(-distancia_x, altura, -distancia_z)
        glVertex3f(-distancia_x, altura + 2.5, -distancia_z - largura)
        glVertex3f(distancia_x, altura + 2.5, -distancia_z - largura)
        glVertex3f(distancia_x, altura, -distancia_z)
        
        glEnd()

    # Cobertura do estádio
    glColor3f(0.8, 0.8, 0.8) # Branco/cinza claro para o teto
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0) # Normal para baixo
    # Direita
    glVertex3f(46, 15, -56)
    glVertex3f(30, 15, -56)
    glVertex3f(30, 15, 56)
    glVertex3f(46, 15, 56)
    
    # Esquerda
    glVertex3f(-46, 15, -56)
    glVertex3f(-30, 15, -56)
    glVertex3f(-30, 15, 56)
    glVertex3f(-46, 15, 56)

    # Fundo
    glVertex3f(-30, 15, 56)
    glVertex3f(-30, 15, 40)
    glVertex3f(30, 15, 40)
    glVertex3f(30, 15, 56)

    # Frente
    glVertex3f(-30, 15, -56)
    glVertex3f(-30, 15, -40)
    glVertex3f(30, 15, -40)
    glVertex3f(30, 15, -56)
    glEnd()

    # Pilares de sustentação
    for z_pil in range(-50, 60, 20):
        draw_cube(44, 7.5, z_pil, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))
        draw_cube(-44, 7.5, z_pil, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))
    for x_pil in [-15, 0, 15]:
        draw_cube(x_pil, 7.5, 54, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))
        draw_cube(x_pil, 7.5, -54, 0.5, 7.5, 0.5, (0.4, 0.4, 0.4))

    # Muros fechando o estádio por trás das arquibancadas
    glColor3f(0.05, 0.05, 0.05) # Cor escura para o muro externo
    glBegin(GL_QUADS)
    # Parede Fundo (Z=56)
    glNormal3f(0, 0, -1)
    glVertex3f(-46, 0, 56)
    glVertex3f(46, 0, 56)
    glVertex3f(46, 15, 56)
    glVertex3f(-46, 15, 56)
    
    # Parede Frente (Z=-56)
    glNormal3f(0, 0, 1)
    glVertex3f(-46, 0, -56)
    glVertex3f(46, 0, -56)
    glVertex3f(46, 15, -56)
    glVertex3f(-46, 15, -56)
    
    # Parede Direita (X=46)
    glNormal3f(-1, 0, 0)
    glVertex3f(46, 0, -56)
    glVertex3f(46, 0, 56)
    glVertex3f(46, 15, 56)
    glVertex3f(46, 15, -56)
    
    # Parede Esquerda (X=-46)
    glNormal3f(1, 0, 0)
    glVertex3f(-46, 0, -56)
    glVertex3f(-46, 0, 56)
    glVertex3f(-46, 15, 56)
    glVertex3f(-46, 15, -56)
    glEnd()

def draw_goal(z_pos):
    glColor3f(0.9, 0.9, 0.9) # Branco
    # Trave Esquerda
    draw_cube(-4, 1.5, z_pos, 0.15, 1.5, 0.15, (0.9, 0.9, 0.9))
    # Trave Direita
    draw_cube(4, 1.5, z_pos, 0.15, 1.5, 0.15, (0.9, 0.9, 0.9))
    # Travessão
    draw_cube(0, 3.15, z_pos, 4.15, 0.15, 0.15, (0.9, 0.9, 0.9))

    # Rede do gol
    glColor3f(0.8, 0.8, 0.8)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    z_net = z_pos - 2 if z_pos < 0 else z_pos + 2
    
    # Linhas verticais
    for i in range(17):
        x = -4 + (i * 0.5)
        glVertex3f(x, 0, z_net)
        glVertex3f(x, 3.0, z_net)
        glVertex3f(x, 3.0, z_net)
        glVertex3f(x, 3.0, z_pos)
        
    # Linhas horizontais
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
    
    for i in range(1, 5): # degraus 1 a 4 (pula o 0 pra não atrapalhar a visão do campo)
        altura = i * 2.5 + 1.0 # Altura base do degrau
        dist_x_start = 30 + i * 4
        dist_z_start = 40 + i * 4
        
        # Lateral Direita e Esquerda
        for z in range(int(-dist_z_start + 2), int(dist_z_start - 2), 3):
            if random.random() > 0.4: # 60% de chance de ter uma pessoa no assento
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

        # Fundo e Frente
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

def update_camera(keys):
    global cam_x, cam_y, cam_z, cam_yaw, cam_pitch
    
    # Rotação da Câmera (Setinhas)
    if keys[K_LEFT]:
        cam_yaw += rot_speed # Invertido
    if keys[K_RIGHT]:
        cam_yaw -= rot_speed # Invertido
    if keys[K_UP]:
        cam_pitch += rot_speed
        if cam_pitch > 90: cam_pitch = 90
    if keys[K_DOWN]:
        cam_pitch -= rot_speed
        if cam_pitch < -90: cam_pitch = -90

    # Movimento (WASD)
    yaw_rad = math.radians(cam_yaw)
    pitch_rad = math.radians(cam_pitch)
    
    # Vetores de direção
    forward_x = math.sin(yaw_rad) * math.cos(pitch_rad)
    forward_y = -math.sin(pitch_rad)
    forward_z = -math.cos(yaw_rad) * math.cos(pitch_rad)
    
    right_x = math.sin(yaw_rad - math.pi/2)
    right_z = -math.cos(yaw_rad - math.pi/2)

    if keys[K_w]:
        cam_x += forward_x * move_speed
        cam_y += forward_y * move_speed
        cam_z += forward_z * move_speed
    if keys[K_s]:
        cam_x -= forward_x * move_speed
        cam_y -= forward_y * move_speed
        cam_z -= forward_z * move_speed
    if keys[K_a]:
        cam_x += right_x * move_speed
        cam_z += right_z * move_speed
    if keys[K_d]:
        cam_x -= right_x * move_speed
        cam_z -= right_z * move_speed

    # Colisão: Impedir de afundar no gramado
    if cam_y < 1.0:
        cam_y = 1.0
        
    # Colisão: Impedir de sair dos limites do estádio
    if cam_x < -35.0: cam_x = -35.0
    if cam_x > 35.0: cam_x = 35.0
    if cam_z < -45.0: cam_z = -45.0
    if cam_z > 45.0: cam_z = 45.0

def main():
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Estádio de Futebol OpenGL")

    # Configuração da projeção 3D
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, (display[0] / display[1]), 0.1, 200.0)
    
    # Habilitar teste de profundidade (para objetos não sobreporem errado)
    glEnable(GL_DEPTH_TEST)
    
    # Habilitar iluminação
    setup_lighting()
    
    # Construir display list da torcida (para não lagar o jogo)
    build_crowd_list()
    
    # Cor de fundo (Céu azul claro radiante de dia)
    glClearColor(0.4, 0.75, 1.0, 1.0)

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        update_camera(keys)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Rotação e Translação da Câmera
        glRotatef(-cam_pitch, 1, 0, 0)
        glRotatef(-cam_yaw, 0, 1, 0)
        glTranslatef(-cam_x, -cam_y, -cam_z)
        
        # Desenhando o Cenário
        draw_field()
        draw_grandstands()
        draw_crowd() # Desenha a multidão de pessoas
        draw_goal(-38)
        draw_goal(38)
        
        # Desenhando o Boneco no centro
        draw_boneco()
        
        # Desenhando a bola
        draw_ball()
        
        pygame.display.flip()
        clock.tick(60) # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
