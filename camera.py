import math
from pygame.locals import *

class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 5.0
        self.z = 15.0
        self.yaw = 0.0
        self.pitch = -15.0
        self.move_speed = 0.5
        self.rot_speed = 2.0

    def update(self, keys):
        # Rotação da Câmera (Setinhas)
        if keys[K_LEFT]:
            self.yaw += self.rot_speed
        if keys[K_RIGHT]:
            self.yaw -= self.rot_speed
        if keys[K_UP]:
            self.pitch += self.rot_speed
            if self.pitch > 90: self.pitch = 90
        if keys[K_DOWN]:
            self.pitch -= self.rot_speed
            if self.pitch < -90: self.pitch = -90

        # Movimento (WASD)
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)
        
        # Vetores de direção
        forward_x = math.sin(yaw_rad) * math.cos(pitch_rad)
        forward_y = -math.sin(pitch_rad)
        forward_z = -math.cos(yaw_rad) * math.cos(pitch_rad)
        
        right_x = math.sin(yaw_rad - math.pi/2)
        right_z = -math.cos(yaw_rad - math.pi/2)

        if keys[K_w]:
            self.x += forward_x * self.move_speed
            self.y += forward_y * self.move_speed
            self.z += forward_z * self.move_speed
        if keys[K_s]:
            self.x -= forward_x * self.move_speed
            self.y -= forward_y * self.move_speed
            self.z -= forward_z * self.move_speed
        if keys[K_a]:
            self.x += right_x * self.move_speed
            self.z += right_z * self.move_speed
        if keys[K_d]:
            self.x -= right_x * self.move_speed
            self.z -= right_z * self.move_speed

        # Colisão: Impedir de afundar no gramado
        if self.y < 1.0:
            self.y = 1.0
            
        # Colisão: Impedir de sair dos limites do estádio
        if self.x < -35.0: self.x = -35.0
        if self.x > 35.0: self.x = 35.0
        if self.z < -45.0: self.z = -45.0
        if self.z > 45.0: self.z = 45.0
