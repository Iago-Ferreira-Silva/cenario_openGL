import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

#Imports
from camera import Camera
from utils import setup_lighting, load_texture
from stadium import draw_field, draw_grandstands, draw_goal, build_crowd_list, draw_crowd
from entities import draw_boneco, draw_ball

#Tam.janela
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def main():
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Estádio de Futebol OpenGL")

    #Proj.3D
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, (display[0] / display[1]), 0.1, 200.0)
    
    #Z-buffer
    glEnable(GL_DEPTH_TEST)
    
    #Luz
    setup_lighting()
    
    #Otimiz.torcida
    build_crowd_list()
    
    #Texturas
    grass_tex = load_texture("grass.png")
    
    #Cor.fundo
    glClearColor(0.4, 0.75, 1.0, 1.0)

    clock = pygame.time.Clock()
    running = True
    
    #Cam
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
        
        #Transf.cam
        glRotatef(-cam.pitch, 1, 0, 0)
        glRotatef(-cam.yaw, 0, 1, 0)
        glTranslatef(-cam.x, -cam.y, -cam.z)
        
        #Cenario
        draw_field(grass_tex)
        draw_grandstands()
        draw_crowd()
        draw_goal(-38)
        draw_goal(38)
        
        #Jogador
        draw_boneco()
        
        #Bola
        draw_ball()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
