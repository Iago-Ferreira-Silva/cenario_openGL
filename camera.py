import math
from pygame.locals import *

class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 8.0
        self.z = 12.0
        self.yaw = 0.0
        self.pitch = -30.0
    
        self.move_speed = 0.5
        self.rot_speed = 2.0

    def update(self, keys):
        
        if keys[K_LEFT] or keys[K_a]:
            self.yaw += self.rot_speed
        if keys[K_RIGHT] or keys[K_d]:
            self.yaw -= self.rot_speed
            
        if keys[K_UP] or keys[K_w]:
            self.pitch += self.rot_speed
            if self.pitch > 90: self.pitch = 90
        if keys[K_DOWN] or keys[K_s]:
            self.pitch -= self.rot_speed
            if self.pitch < -90: self.pitch = -90
