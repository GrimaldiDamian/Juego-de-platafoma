import pygame
import math

class Player():

    def __init__(self) -> None:
        self.posicion_nivel = {"1" : (384,320)}
        self.rectangulo = pygame.Rect(384,320,32,32)
        self.angulo = 0
        self.nivel_actual = None
        self.posicion_inicial_salto = 320

    def movimiento(self,key):
        if key[pygame.K_d]:
            self.rectangulo.x += 10
        if key[pygame.K_a]:
            self.rectangulo.x -= 10

        self.salto()
        if not self.colision_suelo(self.nivel_actual):
            self.rectangulo.y += 10
        # elif self.colision_suelo(self.nivel_actual):
        #     pass
        # else:
        #     self.rectangulo.y += 10

    def salto(self):
        self.rectangulo.y = self.posicion_inicial_salto - (math.sin(self.angulo) * 64)
        if self.angulo > 0:
            self.angulo += 0.1
        if self.angulo >= math.pi:
            self.angulo = 0
            self.en_salto = False

    def colision_suelo (self,nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            if self.rectangulo.colliderect(suelo):
                return True
        return False

    def dibujar(self,screen):
        pygame.draw.rect(screen,"red",self.rectangulo)