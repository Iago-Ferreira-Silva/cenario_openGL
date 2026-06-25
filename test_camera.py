import os
# Configura o pygame para rodar de modo headless (sem abrir janela física)
os.environ["SDL_VIDEODRIVER"] = "dummy"

import unittest
from collections import defaultdict
import pygame
from camera import Camera

class TestCameraLogic(unittest.TestCase):
    def setUp(self):
        """Inicializa uma nova câmera antes de cada teste."""
        self.camera = Camera()

    def test_initial_state(self):
        """Verifica se os valores iniciais da câmera estão corretos."""
        self.assertEqual(self.camera.x, 0.0)
        self.assertEqual(self.camera.y, 8.0)
        self.assertEqual(self.camera.z, 12.0)
        self.assertEqual(self.camera.yaw, 0.0)
        self.assertEqual(self.camera.pitch, -30.0)

    def test_camera_rotation_limits(self):
        """Garante que a rotação vertical (pitch) respeita os limites de -90 e 90 graus."""
        # Usamos defaultdict para simular teclas sem erro de limite de índice
        keys_up = defaultdict(bool)
        keys_up[pygame.K_UP] = True

        # Rotaciona para cima repetidamente para tentar ultrapassar o limite de 90°
        for _ in range(100):
            self.camera.update(keys_up)
        
        self.assertEqual(self.camera.pitch, 90.0, "O pitch da câmera ultrapassou o limite superior de 90°!")

        # Reinicia e simula tecla DOWN pressionada
        self.camera.pitch = -30.0
        keys_down = defaultdict(bool)
        keys_down[pygame.K_DOWN] = True

        for _ in range(100):
            self.camera.update(keys_down)

        self.assertEqual(self.camera.pitch, -90.0, "O pitch da câmera ultrapassou o limite inferior de -90°!")

    def test_camera_yaw_rotation(self):
        """Verifica se a rotação horizontal acumula corretamente."""
        keys_left = defaultdict(bool)
        keys_left[pygame.K_a] = True

        initial_yaw = self.camera.yaw
        self.camera.update(keys_left)
        
        self.assertEqual(self.camera.yaw, initial_yaw + self.camera.rot_speed)

if __name__ == '__main__':
    pygame.init()
    unittest.main()
