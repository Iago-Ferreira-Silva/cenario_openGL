import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Imports modulares
from camera import Camera
from utils import setup_lighting, load_texture
from stadium import draw_field, draw_grandstands, draw_goal, build_crowd_list, draw_crowd
from entities import draw_boneco, draw_ball

# Configurações da Janela
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

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
    
    # Carregar texturas
    grass_tex = load_texture("grass.png")
    
    # Cor de fundo (Céu azul claro radiante de dia)
    glClearColor(0.4, 0.75, 1.0, 1.0)

    clock = pygame.time.Clock()
    running = True
    
    # Inicializa a câmera
    cam = Camera()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        keys = pygame.key.get_pressed()
        cam.update(keys)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Rotação e Translação da Câmera
        glRotatef(-cam.pitch, 1, 0, 0)
        glRotatef(-cam.yaw, 0, 1, 0)
        glTranslatef(-cam.x, -cam.y, -cam.z)
        
        # Desenhando o Cenário
        draw_field(grass_tex)
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
