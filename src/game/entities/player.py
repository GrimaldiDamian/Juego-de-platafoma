import pygame
import math

class Player():

    def __init__(self) -> None:
        self.posicion_nivel = {"1" : (384,320)}
        self.rectangulo = pygame.Rect(384,320,16,24)
        self.angulo = 0
        self.nivel_actual = None
        self.posicion_inicial_salto = 320
        self.en_salto = False

    def movimiento(self,key):
        if key[pygame.K_d]:
            self.rectangulo.x += 5
        if key[pygame.K_a]:
            self.rectangulo.x -= 5

        arriba, abajo, izquierda, derecha = self.colision_orientacion(self.nivel_actual)
        if self.en_salto:
            self.salto()
        if arriba:
            self.rectangulo.y = self.obtener_posicion_arriba(self.nivel_actual)
        else:
            self.rectangulo.y += 5
        if derecha:
            self.rectangulo.x = self.obtener_posicion_derecha(self.nivel_actual) - self.rectangulo.width
        if izquierda:
            self.rectangulo.x = self.obtener_posicion_izquierda(self.nivel_actual)

    def salto(self):
        self.rectangulo.y = self.posicion_inicial_salto - (math.sin(self.angulo) * 64)
        arriba,abajo,_,_ = self.colision_orientacion(self.nivel_actual)
        if self.angulo > 0:
            self.angulo += 0.1
        if self.angulo >= math.pi or arriba:
            self.angulo = 0
            self.en_salto = False
        if self.angulo < math.pi/2 and abajo:
            self.angulo = math.pi/2

    def colision_orientacion(self, nivel):
        arriba, abajo, izquierda, derecha = False, False, False, False

        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo

            # Detectar si el jugador está justo encima del bloque
            if (self.rectangulo.y + self.rectangulo.height >= y and 
                self.rectangulo.y + self.rectangulo.height <= y + 5) and (
                self.rectangulo.x + self.rectangulo.width > x and 
                self.rectangulo.x < x + 32):
                arriba = True

            # Detectar si el jugador está justo debajo del bloque
            if (self.rectangulo.y <= y + 32 and 
                self.rectangulo.y >= y + 32 - 5) and (
                self.rectangulo.x + self.rectangulo.width > x and 
                self.rectangulo.x < x + 32):
                abajo = True

        return arriba, abajo, izquierda, derecha

    def obtener_posicion_arriba(self,nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            x,y = suelo
            if (self.rectangulo.y + self.rectangulo.height >= y and 
                self.rectangulo.y + self.rectangulo.height <= y + 5) and (
                self.rectangulo.x + self.rectangulo.width > x and 
                self.rectangulo.x < x + 32):
                return y - self.rectangulo.height
        return self.rectangulo.y

    def obtener_posicion_izquierda(self,nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo
            if (self.rectangulo.x <= x + 32 and 
                self.rectangulo.x >= x + 32 - 5) and (
                self.rectangulo.y + self.rectangulo.height > y and 
                self.rectangulo.y < y + 32):
                return x
        return self.rectangulo.x

    def obtener_posicion_derecha(self,nivel):
        for suelo in nivel.suelo_colision["solidos"]:
            x, y = suelo
            if (self.rectangulo.x + self.rectangulo.width >= x and 
                self.rectangulo.x + self.rectangulo.width <= x + 5) and (
                self.rectangulo.y + self.rectangulo.height > y and 
                self.rectangulo.y < y + 32):
                return x - self.rectangulo.width
        return self.rectangulo.x

    def dibujar(self,screen):
        pygame.draw.rect(screen,"red",self.rectangulo)