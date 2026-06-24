import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

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

    # Configuração da luz (posição e cor)
    light_pos = [10.0, 50.0, 10.0, 1.0] # Luz direcional/pontual vindo de cima
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    # Material padrão
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
    glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 50)

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
    # Cores da camisa do Brasil
    cor_pele = (0.9, 0.7, 0.6)
    cor_camisa = (1.0, 1.0, 0.0) # Amarelo
    cor_short = (0.0, 0.0, 1.0)  # Azul
    cor_meia = (1.0, 1.0, 1.0)   # Branco

    # Cabeça
    draw_cube(0, 3.5, 0, 0.4, 0.4, 0.4, cor_pele)
    # Tronco
    draw_cube(0, 2.0, 0, 0.6, 0.8, 0.3, cor_camisa)
    # Braço Esquerdo
    draw_cube(-0.8, 2.0, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(-0.8, 1.0, 0, 0.15, 0.4, 0.15, cor_pele)
    # Braço Direito
    draw_cube(0.8, 2.0, 0, 0.2, 0.8, 0.2, cor_camisa)
    draw_cube(0.8, 1.0, 0, 0.15, 0.4, 0.15, cor_pele)
    # Perna Esquerda
    draw_cube(-0.3, 0.8, 0, 0.25, 0.6, 0.25, cor_short)
    draw_cube(-0.3, 0.0, 0, 0.2, 0.4, 0.2, cor_meia)
    # Perna Direita
    draw_cube(0.3, 0.8, 0, 0.25, 0.6, 0.25, cor_short)
    draw_cube(0.3, 0.0, 0, 0.2, 0.4, 0.2, cor_meia)

def draw_field():
    # Gramado principal
    glColor3f(0.1, 0.5, 0.1) # Verde escuro
    glNormal3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex3f(-30, 0, -40)
    glVertex3f(-30, 0, 40)
    glVertex3f(30, 0, 40)
    glVertex3f(30, 0, -40)
    glEnd()

    # Linhas do campo (brancas, levemente acima do y=0 para não piscar)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    # Bordas
    glVertex3f(-28, 0.01, -38); glVertex3f(28, 0.01, -38)
    glVertex3f(28, 0.01, -38);  glVertex3f(28, 0.01, 38)
    glVertex3f(28, 0.01, 38);   glVertex3f(-28, 0.01, 38)
    glVertex3f(-28, 0.01, 38);  glVertex3f(-28, 0.01, -38)
    # Meio campo
    glVertex3f(-28, 0.01, 0);   glVertex3f(28, 0.01, 0)
    glEnd()

def draw_grandstands():
    # Arquibancadas nas cores do Brasil (Verde, Amarelo, Azul)
    colors = [
        (0.0, 0.6, 0.0), # Verde
        (1.0, 1.0, 0.0), # Amarelo
        (0.0, 0.0, 0.8)  # Azul
    ]
    
    # Desenhando degraus ao redor do campo
    for i in range(3):
        altura = i * 2.0 + 1.0
        distancia_x = 30 + i * 3
        distancia_z = 40 + i * 3
        largura = 3.0
        
        glColor3f(*colors[i])
        glBegin(GL_QUADS)
        
        # Lado Direito
        glNormal3f(-1, 1, 0)
        glVertex3f(distancia_x, altura, -distancia_z)
        glVertex3f(distancia_x + largura, altura + 2, -distancia_z)
        glVertex3f(distancia_x + largura, altura + 2, distancia_z)
        glVertex3f(distancia_x, altura, distancia_z)
        
        # Lado Esquerdo
        glNormal3f(1, 1, 0)
        glVertex3f(-distancia_x, altura, -distancia_z)
        glVertex3f(-distancia_x - largura, altura + 2, -distancia_z)
        glVertex3f(-distancia_x - largura, altura + 2, distancia_z)
        glVertex3f(-distancia_x, altura, distancia_z)

        # Fundo (Gols)
        glNormal3f(0, 1, -1)
        glVertex3f(-distancia_x, altura, distancia_z)
        glVertex3f(-distancia_x, altura + 2, distancia_z + largura)
        glVertex3f(distancia_x, altura + 2, distancia_z + largura)
        glVertex3f(distancia_x, altura, distancia_z)

        # Frente (Gols)
        glNormal3f(0, 1, 1)
        glVertex3f(-distancia_x, altura, -distancia_z)
        glVertex3f(-distancia_x, altura + 2, -distancia_z - largura)
        glVertex3f(distancia_x, altura + 2, -distancia_z - largura)
        glVertex3f(distancia_x, altura, -distancia_z)
        
        glEnd()

def draw_goal(z_pos):
    glColor3f(0.9, 0.9, 0.9) # Branco
    # Trave Esquerda
    draw_cube(-4, 1.5, z_pos, 0.2, 1.5, 0.2, (0.9, 0.9, 0.9))
    # Trave Direita
    draw_cube(4, 1.5, z_pos, 0.2, 1.5, 0.2, (0.9, 0.9, 0.9))
    # Travessão
    draw_cube(0, 3.2, z_pos, 4.2, 0.2, 0.2, (0.9, 0.9, 0.9))

def update_camera(keys):
    global cam_x, cam_y, cam_z, cam_yaw, cam_pitch
    
    # Rotação da Câmera (Setinhas)
    if keys[K_LEFT]:
        cam_yaw -= rot_speed
    if keys[K_RIGHT]:
        cam_yaw += rot_speed
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
        cam_x -= right_x * move_speed
        cam_z -= right_z * move_speed
    if keys[K_d]:
        cam_x += right_x * move_speed
        cam_z += right_z * move_speed

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
    
    # Cor de fundo (Céu azul)
    glClearColor(0.5, 0.7, 1.0, 1.0)

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
        draw_goal(-38)
        draw_goal(38)
        
        # Desenhando o Boneco no centro
        draw_boneco()
        
        pygame.display.flip()
        clock.tick(60) # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
